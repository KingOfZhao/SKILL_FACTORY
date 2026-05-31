"""skill_factory — 工程级 Skill 工厂统一工具包。

把原先散落在各 skill 目录下的可执行能力收敛为一个可安装、可测试、可 CI 的包：

- :mod:`skill_factory.lint`      —— Dart 反模式静态扫描（A）。
- :mod:`skill_factory.catalog`   —— 技能目录扫描 / 清单同步（C）。
- :mod:`skill_factory.checker`   —— 元 Skill 规范校验（B）。
- :mod:`skill_factory.recommend` —— 问题域 → 技能推荐（D）。
- :mod:`skill_factory.cli`       —— 统一命令行入口 ``skill-factory``。
- :mod:`skill_factory.paths`     —— 仓库根 / 技能目录解析（去硬编码路径）。

各 skill 目录下的原脚本保留为薄壳，转调本包，保证既有调用方式不回归。
"""

from __future__ import annotations

__version__ = "0.1.0"

__all__ = ["__version__"]
