"""技能目录扫描 / 清单同步（C）。

扫描技能根目录下所有含 ``SKILL.md`` 的技能，解析名称/描述/类型，生成人类可读的
Markdown 能力清单与机器可读的 JSON 清单，保持目录与索引同步、避免手工维护漂移。

零第三方依赖（手工解析 frontmatter）。退出码：
- ``0`` 正常 / ``--check`` 通过
- ``1`` ``--check`` 检测到清单过期
- ``2`` 用法错误
"""

from __future__ import annotations

import argparse
import json
import os
import re
from dataclasses import asdict, dataclass

from .paths import find_repo_root, skills_dir


@dataclass
class SkillInfo:
    name: str
    description: str
    rel_path: str
    type: str  # "meta" | "task"
    has_description_md: bool
    has_scripts: bool
    line_count: int


def parse_frontmatter(text: str) -> dict[str, str]:
    """解析 SKILL.md 顶部 --- --- 之间的简单 frontmatter。"""
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    block = text[3:end]
    fields: dict[str, str] = {}
    for line in block.splitlines():
        m = re.match(r"\s*([A-Za-z_][\w-]*)\s*:\s*(.*)\s*$", line)
        if m:
            key, val = m.group(1).strip(), m.group(2).strip()
            val = val.strip('"').strip("'")
            fields[key] = val
    return fields


def classify(name: str, rel_path: str) -> str:
    """元 Skill 识别：名称带 meta-/元- 前缀，或位于 元/ 目录下。

    刻意不按 generator/validator 等子串判定，避免把 flutter_factory 下的
    任务型生成器误判为元 Skill。
    """
    low = name.lower()
    if low.startswith("meta-") or name.startswith("元-") or name.startswith("元"):
        return "meta"
    parts = rel_path.replace("\\", "/").split("/")
    if "元" in parts:
        return "meta"
    return "task"


def scan(root: str) -> list[SkillInfo]:
    skills: list[SkillInfo] = []
    for dirpath, _dirs, files in os.walk(root):
        if "SKILL.md" not in files:
            continue
        skill_md = os.path.join(dirpath, "SKILL.md")
        try:
            with open(skill_md, encoding="utf-8") as fh:
                text = fh.read()
        except (OSError, UnicodeDecodeError):
            continue
        fm = parse_frontmatter(text)
        rel = os.path.relpath(dirpath, root)
        name = fm.get("name") or os.path.basename(dirpath)
        desc = fm.get("description", "").strip()
        if not desc:
            # 回退：取首个非空、非标题正文行
            for line in text.splitlines():
                s = line.strip()
                if s and not s.startswith("#") and not s.startswith("---"):
                    desc = s[:200]
                    break
        skills.append(
            SkillInfo(
                name=name,
                description=desc,
                rel_path=rel.replace("\\", "/"),
                type=classify(name, rel),
                has_description_md=os.path.exists(os.path.join(dirpath, "description.md")),
                has_scripts=any(f.endswith(".py") for f in files)
                or os.path.isdir(os.path.join(dirpath, "scripts")),
                line_count=text.count("\n") + 1,
            )
        )
    skills.sort(key=lambda s: (s.type != "meta", s.rel_path))
    return skills


def build_tree(skills: list[SkillInfo]) -> dict:
    tree: dict = {}
    for s in skills:
        node = tree
        for part in s.rel_path.split("/"):
            node = node.setdefault(part, {})
        node["__skill__"] = s.name
    return tree


def _render_tree(node: dict, indent: int = 0) -> list[str]:
    lines = []
    for key in sorted(k for k in node if k != "__skill__"):
        child = node[key]
        marker = "📦" if "__skill__" in child else "📁"
        lines.append(f"{'  ' * indent}- {marker} {key}")
        lines.extend(_render_tree(child, indent + 1))
    return lines


def render_markdown(skills: list[SkillInfo], root: str) -> str:
    meta = [s for s in skills if s.type == "meta"]
    task = [s for s in skills if s.type == "task"]
    lines = [
        "<!-- 本文件由 skill_factory.catalog 自动生成，请勿手工编辑 -->",
        "# Skill 能力清单（自动生成）",
        "",
        f"- 扫描根目录：`{root}`",
        f"- 技能总数：**{len(skills)}**（元 Skill {len(meta)} / 任务型 {len(task)}）",
        "",
        "## 技能列表",
        "",
        "| 类型 | 名称 | 描述 | 路径 |",
        "|------|------|------|------|",
    ]
    for s in skills:
        desc = (s.description or "").replace("|", "\\|")[:120]
        tag = "元" if s.type == "meta" else "任务"
        lines.append(f"| {tag} | `{s.name}` | {desc} | `{s.rel_path}` |")
    lines += ["", "## 目录树", ""]
    lines += _render_tree(build_tree(skills))
    lines.append("")
    return "\n".join(lines)


def render_json(skills: list[SkillInfo], root: str) -> str:
    payload = {
        "root": root,
        "total": len(skills),
        "meta_count": sum(1 for s in skills if s.type == "meta"),
        "task_count": sum(1 for s in skills if s.type == "task"),
        "skills": [asdict(s) for s in skills],
    }
    return json.dumps(payload, ensure_ascii=False, indent=2)


def display_root(root: str) -> str:
    """把扫描根目录转为相对仓库根的稳定路径，避免清单嵌入机器相关绝对路径。

    无法定位到仓库根（root 不在仓库内）时回退为 basename。
    """
    abs_root = os.path.abspath(root)
    try:
        repo_root = str(find_repo_root(abs_root))
        rel = os.path.relpath(abs_root, repo_root)
    except (OSError, ValueError):
        return os.path.basename(abs_root.rstrip(os.sep))
    if rel == "." or rel.startswith(".."):
        return os.path.basename(abs_root.rstrip(os.sep))
    return rel.replace("\\", "/")


def default_out_dir() -> str:
    """清单产物的默认输出目录（skill-catalog-scanner/scan-results）。"""
    return str(skills_dir() / "skill-catalog-scanner" / "scan-results")


def run(root: str | None = None, out: str | None = None, check: bool = False) -> int:
    """执行扫描；供 CLI 与薄壳共用。``root`` 为空时自动定位 .claude/skills。"""
    root = root or str(skills_dir())
    if not os.path.isdir(root):
        print(f"错误：目录不存在：{root}", flush=True)
        return 2

    skills = scan(root)
    shown_root = display_root(root)
    md = render_markdown(skills, shown_root)
    js = render_json(skills, shown_root)

    out_dir = out or default_out_dir()
    md_path = os.path.join(out_dir, "skill-catalog.md")
    json_path = os.path.join(out_dir, "skill-catalog.json")

    if check:
        stale = False
        for path, content in ((md_path, md), (json_path, js)):
            existing = ""
            if os.path.exists(path):
                with open(path, encoding="utf-8") as fh:
                    existing = fh.read()
            if existing.strip() != content.strip():
                print(f"[过期] {path}")
                stale = True
        if stale:
            print("清单过期，请运行：skill-factory scan")
            return 1
        print(f"清单已最新（{len(skills)} 个技能）")
        return 0

    os.makedirs(out_dir, exist_ok=True)
    with open(md_path, "w", encoding="utf-8") as fh:
        fh.write(md)
    with open(json_path, "w", encoding="utf-8") as fh:
        fh.write(js)
    print(f"已生成 {len(skills)} 个技能的清单：")
    print(f"  - {md_path}")
    print(f"  - {json_path}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="技能目录扫描器（生成能力清单）")
    parser.add_argument("root", nargs="?", help="要扫描的技能根目录（默认自动定位 .claude/skills）")
    parser.add_argument("--out", help="输出目录（默认 skill-catalog-scanner/scan-results）")
    parser.add_argument("--check", action="store_true", help="只校验清单是否最新，不写入")
    args = parser.parse_args(argv)
    return run(root=args.root, out=args.out, check=args.check)


if __name__ == "__main__":
    import sys

    sys.exit(main())
