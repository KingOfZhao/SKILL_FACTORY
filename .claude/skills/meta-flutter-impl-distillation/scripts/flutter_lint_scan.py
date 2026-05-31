#!/usr/bin/env python3
"""flutter_lint_scan.py — 薄壳：转调 ``skill_factory.lint``。

实现已收敛至工程层 ``skill_factory`` 包（见 ``skill_factory/lint.py``）。
本文件仅做 sys.path 兜底 + 委托，保证未安装包时
``python3 flutter_lint_scan.py ...`` 仍可运行，命令行参数完全一致。

推荐用法：``skill-factory lint <path> [--format json|text] [--json out.json]``
          ``skill-factory lint --selftest``
"""

from __future__ import annotations

import sys
from pathlib import Path


def _ensure_importable() -> None:
    """未作为包导入时，向上查找仓库根并加入 sys.path。"""
    if __package__:
        return
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / "skill_factory" / "__init__.py").exists():
            sys.path.insert(0, str(parent))
            return


_ensure_importable()

from skill_factory.lint import main  # noqa: E402

if __name__ == "__main__":
    sys.exit(main())
