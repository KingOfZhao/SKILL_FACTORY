"""统一命令行入口：``skill-factory``。

子命令：
  lint       扫描 Dart 源码中的反模式（A）
  scan       扫描技能目录、生成/校验能力清单（C）
  check      校验 SKILL.md 是否符合元 Skill 规范（B）
  recommend  根据问题描述推荐技能（D）

各子命令的实现位于对应模块，CLI 仅做参数解析与分发；子模块同时各自提供
向后兼容的 ``main()``，供 skill 目录下的薄壳脚本直接调用。
"""

from __future__ import annotations

import argparse

from . import __version__


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="skill-factory",
        description="工程级 Skill 工厂统一命令行工具",
    )
    parser.add_argument("--version", action="version", version=f"skill-factory {__version__}")
    sub = parser.add_subparsers(dest="command", metavar="<command>")

    p_lint = sub.add_parser("lint", help="扫描 Dart 源码中的反模式")
    p_lint.add_argument("path", nargs="?", help="要扫描的 .dart 文件或目录")
    p_lint.add_argument("--format", choices=["json", "text"], default="text")
    p_lint.add_argument("--json", dest="json_out", help="把 JSON 报告写入指定文件")
    p_lint.add_argument("--selftest", action="store_true", help="用内置样例自检")

    p_scan = sub.add_parser("scan", help="扫描技能目录并生成/校验能力清单")
    p_scan.add_argument("root", nargs="?", help="技能根目录（默认自动定位 .claude/skills）")
    p_scan.add_argument("--out", help="输出目录")
    p_scan.add_argument("--check", action="store_true", help="只校验清单是否最新")

    p_check = sub.add_parser("check", help="校验 SKILL.md 是否符合元 Skill 规范")
    p_check.add_argument("path", help="单个 SKILL.md 文件，或包含多个 Skill 的目录")
    p_check.add_argument("--summary", action="store_true", help="输出批量汇总报告")
    p_check.add_argument("--json", dest="json_out", help="将报告写入 JSON 文件")

    p_rec = sub.add_parser("recommend", help="根据问题描述推荐技能")
    p_rec.add_argument("request", help="问题 / 需求描述")
    p_rec.add_argument("--json", dest="json_out", help="将推荐结果写入 JSON 文件")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "lint":
        from . import lint

        return lint.run(
            path=args.path,
            fmt=args.format,
            json_out=args.json_out,
            selftest=args.selftest,
        )
    if args.command == "scan":
        from . import catalog

        return catalog.run(root=args.root, out=args.out, check=args.check)
    if args.command == "check":
        from . import checker

        return checker.run(path=args.path, summary=args.summary, json_out=args.json_out)
    if args.command == "recommend":
        from . import recommend

        return recommend.run(request=args.request, json_out=args.json_out)

    parser.print_help()
    return 0


if __name__ == "__main__":
    import sys

    sys.exit(main())
