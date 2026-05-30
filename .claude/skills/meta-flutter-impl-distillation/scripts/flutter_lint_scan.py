#!/usr/bin/env python3
"""flutter_lint_scan.py — 蒸馏器的可执行校验脚本（A）。

按 references/anti-patterns.md 中的高频反模式，对 Dart 源码做轻量静态扫描，
输出结构化结果（JSON 或文本），并用退出码反映严重程度：
  exit 0 = 无 major/critical 命中
  exit 1 = 存在 major/critical 命中
  exit 2 = 用法错误

设计原则：
- 仅依赖 Python 标准库，零安装；
- 启发式检测，宁可漏报不过度误报（关键反模式优先）；
- 与 anti-patterns.md 的 AP 编号一一对应，便于回链。

用法：
  python3 flutter_lint_scan.py <path-or-file> [--format json|text] [--json out.json]
  python3 flutter_lint_scan.py --selftest        # 用内置样例自检（约 10 秒）
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass, asdict
from typing import List, Optional


SEVERITY_ORDER = {"critical": 3, "major": 2, "minor": 1, "info": 0}


@dataclass
class Finding:
    ap_id: str
    severity: str
    message: str
    file: str
    line: int
    snippet: str
    fix: str


# ---------------------------------------------------------------------------
# 单行启发式规则：(ap_id, severity, 编译后正则, message, fix, 反向排除正则)
# ---------------------------------------------------------------------------
_BANG = re.compile(r"!\s*[.\);,]")          # foo!. / foo!) / foo!; / foo!,
_BANG_EXCLUDE = re.compile(r"(!=|\bassert\b)")  # 排除 != 与 assert

LINE_RULES = [
    (
        "AP-6",
        "minor",
        re.compile(r"(^|[^.\w])print\s*\("),
        "使用 print 调试，应改用 logging 包",
        "import 'package:logging/logging.dart'; 用 Logger 替代 print",
        None,
    ),
    (
        "AP-3",
        "major",
        re.compile(r"\.map\s*\(.*\)\s*\.toList\s*\(\)"),
        "可能用 Column/children + map().toList() 渲染列表，长列表应懒加载",
        "改用 ListView.builder / SliverList",
        None,
    ),
    (
        "AP-13",
        "minor",
        re.compile(r"jsonDecode\s*\("),
        "同步 jsonDecode 可能阻塞 UI 线程（大数据时）",
        "重解析放入 compute() 的独立 isolate",
        re.compile(r"compute\s*\("),
    ),
]


def _scan_bang(line: str) -> bool:
    return bool(_BANG.search(line)) and not _BANG_EXCLUDE.search(line)


def _strip_comments(src: str) -> str:
    """去掉 // 行注释与 /* */ 块注释，降低误报（保留行数）。"""
    src = re.sub(r"/\*.*?\*/", lambda m: "\n" * m.group(0).count("\n"), src, flags=re.S)
    out_lines = []
    for ln in src.splitlines():
        out_lines.append(re.sub(r"//.*$", "", ln))
    return "\n".join(out_lines)


def _find_build_body(src: str) -> List[tuple]:
    """粗略提取 `Widget build(...)` 方法体，返回 [(start_line, body_str)]。"""
    bodies = []
    for m in re.finditer(r"Widget\s+build\s*\([^)]*\)\s*(?:async\s*)?\{", src):
        start = m.end() - 1  # 指向 '{'
        depth = 0
        i = start
        while i < len(src):
            c = src[i]
            if c == "{":
                depth += 1
            elif c == "}":
                depth -= 1
                if depth == 0:
                    break
            i += 1
        body = src[start : i + 1]
        start_line = src[: m.start()].count("\n") + 1
        bodies.append((start_line, body))
    return bodies


def scan_text(content: str, path: str) -> List[Finding]:
    findings: List[Finding] = []
    src = _strip_comments(content)
    lines = src.splitlines()

    # 逐行规则
    for idx, raw in enumerate(lines, start=1):
        line = raw.rstrip()
        if not line.strip():
            continue
        for ap_id, sev, pat, msg, fix, exclude in LINE_RULES:
            if pat.search(line) and not (exclude and exclude.search(line)):
                findings.append(
                    Finding(ap_id, sev, msg, path, idx, line.strip()[:160], fix)
                )
        # AP-4 滥用 null 断言
        if _scan_bang(line):
            findings.append(
                Finding(
                    "AP-4",
                    "major",
                    "滥用 null 断言操作符 `!`，运行时可能抛 Null check 异常",
                    path,
                    idx,
                    line.strip()[:160],
                    "改用 `?.` + `??` 提供默认值，或先做非空判断",
                )
            )

    # AP-1 build() 内发请求 / 重活
    for start_line, body in _find_build_body(src):
        m = re.search(r"(http\.(get|post|put|delete)\s*\(|\.fetch\s*\(|await\s)", body)
        if m:
            rel_line = start_line + body[: m.start()].count("\n")
            findings.append(
                Finding(
                    "AP-1",
                    "critical",
                    "在 build() 内执行网络请求/await 重活，每次 rebuild 都会触发",
                    path,
                    rel_line,
                    body[m.start() : m.start() + 80].replace("\n", " ").strip(),
                    "把请求移到 initState / ViewModel，只触发一次；UI 用 FutureBuilder/状态监听",
                )
            )

    # AP-9 创建 controller/subscription 但文件内无 dispose/cancel
    creates_ctrl = re.search(r"(TextEditingController|AnimationController|ScrollController)\s*\(", src)
    has_subscription = re.search(r"\.listen\s*\(", src)
    has_dispose = re.search(r"void\s+dispose\s*\(", src)
    has_cancel = re.search(r"\.cancel\s*\(\)|\.dispose\s*\(\)", src)
    if creates_ctrl and not has_dispose:
        ln = src[: creates_ctrl.start()].count("\n") + 1
        findings.append(
            Finding(
                "AP-9",
                "major",
                "创建了 *Controller 但未发现 dispose()，可能内存泄漏",
                path,
                ln,
                creates_ctrl.group(0),
                "在 State.dispose() 中释放 controller",
            )
        )
    if has_subscription and not has_cancel:
        ln = src[: has_subscription.start()].count("\n") + 1
        findings.append(
            Finding(
                "AP-9",
                "major",
                "存在 stream.listen 订阅但未发现 cancel()，可能内存泄漏",
                path,
                ln,
                has_subscription.group(0),
                "保存 StreamSubscription 并在 dispose() 中 cancel()",
            )
        )

    return findings


def scan_path(path: str) -> List[Finding]:
    findings: List[Finding] = []
    targets: List[str] = []
    if os.path.isfile(path):
        targets = [path]
    else:
        for root, _dirs, files in os.walk(path):
            for f in files:
                if f.endswith(".dart"):
                    targets.append(os.path.join(root, f))
    for t in targets:
        try:
            with open(t, "r", encoding="utf-8") as fh:
                content = fh.read()
        except (OSError, UnicodeDecodeError):
            continue
        findings.extend(scan_text(content, t))
    return findings


def worst_severity(findings: List[Finding]) -> Optional[str]:
    if not findings:
        return None
    return max(findings, key=lambda f: SEVERITY_ORDER[f.severity]).severity


def to_report(findings: List[Finding]) -> dict:
    counts = {"critical": 0, "major": 0, "minor": 0, "info": 0}
    for f in findings:
        counts[f.severity] += 1
    return {
        "tool": "flutter_lint_scan",
        "total": len(findings),
        "counts": counts,
        "worst_severity": worst_severity(findings),
        "findings": [asdict(f) for f in findings],
    }


def print_text(report: dict) -> None:
    print(f"[flutter_lint_scan] 命中 {report['total']} 项  {report['counts']}")
    for f in report["findings"]:
        print(f"  [{f['severity']:8}] {f['ap_id']} {f['file']}:{f['line']}")
        print(f"             {f['message']}")
        print(f"             > {f['snippet']}")
        print(f"             fix: {f['fix']}")


_SELFTEST_BAD = """
import 'package:flutter/material.dart';

class BadPage extends StatefulWidget {
  @override
  State<BadPage> createState() => _BadPageState();
}

class _BadPageState extends State<BadPage> {
  final controller = TextEditingController();

  @override
  Widget build(BuildContext context) {
    final data = http.get(Uri.parse('https://x'));
    print('building');
    final name = user!.profile!.name;
    return Column(
      children: items.map((e) => Text(e)).toList(),
    );
  }
}
"""

_SELFTEST_GOOD = """
import 'package:flutter/material.dart';

class GoodList extends StatelessWidget {
  const GoodList({super.key, required this.items});
  final List<String> items;

  @override
  Widget build(BuildContext context) {
    return ListView.builder(
      itemCount: items.length,
      itemBuilder: (_, i) => Text(items[i]),
    );
  }
}
"""


def selftest() -> int:
    bad = scan_text(_SELFTEST_BAD, "<bad>")
    good = scan_text(_SELFTEST_GOOD, "<good>")
    bad_ids = {f.ap_id for f in bad}
    ok = True
    for expected in ("AP-1", "AP-3", "AP-4", "AP-6", "AP-9"):
        hit = expected in bad_ids
        print(f"  bad 应命中 {expected}: {'OK' if hit else 'FAIL'}")
        ok = ok and hit
    good_clean = all(f.severity in ("info",) for f in good)
    print(f"  good 无 major/critical: {'OK' if good_clean else 'FAIL'}")
    ok = ok and good_clean
    print("SELFTEST", "PASS" if ok else "FAIL")
    return 0 if ok else 1


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Dart 反模式静态扫描器（蒸馏器配套）")
    parser.add_argument("path", nargs="?", help="要扫描的 .dart 文件或目录")
    parser.add_argument("--format", choices=["json", "text"], default="text")
    parser.add_argument("--json", dest="json_out", help="把 JSON 报告写入指定文件")
    parser.add_argument("--selftest", action="store_true", help="用内置样例自检")
    args = parser.parse_args(argv)

    if args.selftest:
        return selftest()
    if not args.path:
        parser.error("需要提供 path 或 --selftest")
        return 2

    findings = scan_path(args.path)
    report = to_report(findings)

    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as fh:
            json.dump(report, fh, ensure_ascii=False, indent=2)
    if args.format == "json":
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print_text(report)

    worst = report["worst_severity"]
    return 1 if worst in ("major", "critical") else 0


if __name__ == "__main__":
    sys.exit(main())
