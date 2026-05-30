"""仓库根目录与技能目录解析。

替代仓库内多处硬编码的 macOS 绝对路径（如
``/Users/administruter/Desktop/skill_factory/...``），改为从任意调用位置
向上查找仓库标志文件来稳健定位，保证在任意机器 / CI 上都能工作。
"""

from __future__ import annotations

import os
from collections.abc import Iterable
from pathlib import Path

# 仓库根的标志：命中任一即认为是根目录。
_ROOT_MARKERS: tuple[str, ...] = ("pyproject.toml", ".git", ".claude")


def find_repo_root(start: str | os.PathLike[str] | None = None) -> Path:
    """从 ``start`` 向上查找仓库根目录。

    查找顺序：
    1. 环境变量 ``SKILL_FACTORY_ROOT``（若设置且存在）。
    2. 从 ``start``（默认当前文件所在处）逐级向上，遇到任一标志文件即返回。
    3. 兜底返回 ``start`` 的最顶层父目录。
    """
    env_root = os.environ.get("SKILL_FACTORY_ROOT")
    if env_root:
        p = Path(env_root).expanduser()
        if p.is_dir():
            return p.resolve()

    base = Path(start).resolve() if start is not None else Path(__file__).resolve()
    if base.is_file():
        base = base.parent

    for candidate in (base, *base.parents):
        if _has_any_marker(candidate, _ROOT_MARKERS):
            return candidate
    return base


def _has_any_marker(directory: Path, markers: Iterable[str]) -> bool:
    return any((directory / m).exists() for m in markers)


def skills_dir(start: str | os.PathLike[str] | None = None) -> Path:
    """返回 ``<repo-root>/.claude/skills``。"""
    return find_repo_root(start) / ".claude" / "skills"
