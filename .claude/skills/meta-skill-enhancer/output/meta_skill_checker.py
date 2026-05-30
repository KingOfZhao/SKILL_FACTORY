#!/usr/bin/env python3
"""meta_skill_checker.py — 薄壳：转调 ``skill_factory.checker``。

实现已收敛至工程层 ``skill_factory`` 包（见 ``skill_factory/checker.py``）。
本文件仅做 sys.path 兜底 + 委托，保证未安装包时
``python3 meta_skill_checker.py <path> [--summary] [--json out.json]`` 仍可运行。

推荐用法：``skill-factory check <path> [--summary] [--json out.json]``
"""

from __future__ import annotations

import sys
from pathlib import Path


def _ensure_importable() -> None:
    if __package__:
        return
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / "skill_factory" / "__init__.py").exists():
            sys.path.insert(0, str(parent))
            return


_ensure_importable()

from skill_factory.checker import main  # noqa: E402

if __name__ == "__main__":
    sys.exit(main())
