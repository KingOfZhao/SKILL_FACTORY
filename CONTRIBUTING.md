# 贡献指南

本仓库是一个 **Claude Code Skill 工厂**：以「元 Skill 定义 / 生成 Skill」为核心的结构化认知体系。
跨技能的可执行能力（反模式扫描、目录同步、元 Skill 校验、问题域推荐）已收敛进可安装、可测试、
可 CI 的统一 Python 包 `skill_factory/`；各技能目录下的原脚本保留为薄壳转调，调用方式不回归。

## 环境要求

- Python ≥ 3.10
- 运行时零第三方依赖（仅标准库）；开发依赖为 `ruff` / `mypy` / `pytest` / `pytest-cov`。

## 快速开始

```bash
make install        # pip install -e ".[dev]"
make ci             # 本地复跑 CI 全部门禁（lint + 格式 + 类型 + 测试覆盖 + 清单漂移）
```

也可使用 `pre-commit`：

```bash
pip install pre-commit
pre-commit install  # 之后每次提交自动跑 ruff / 格式化
```

## 统一命令行

安装后提供 `skill-factory` 命令（亦可 `python3 -m skill_factory.cli`）：

```bash
skill-factory lint <path|--selftest>     # Dart 反模式静态扫描（A）
skill-factory scan [root] [--check]      # 技能目录扫描 / 能力清单同步（C）
skill-factory check <path> [--summary]   # 元 Skill 规范校验（B）
skill-factory recommend "<需求描述>"      # 问题域 → 技能推荐（D）
```

## 包结构

| 模块 | 能力 | 薄壳位置（向后兼容） |
|------|------|----------------------|
| `skill_factory/lint.py` | Dart 反模式扫描 | `.claude/skills/meta-flutter-impl-distillation/scripts/flutter_lint_scan.py` |
| `skill_factory/catalog.py` | 技能目录 / 清单同步 | `.claude/skills/skill-catalog-scanner/scan_skills.py` |
| `skill_factory/checker.py` | 元 Skill 规范校验 | `.claude/skills/meta-skill-enhancer/output/meta_skill_checker.py` |
| `skill_factory/recommend.py` | 问题域 → 技能推荐 | 由 `元/元-skill-orchestrator/orchestrator.py` 复用 |
| `skill_factory/paths.py` | 仓库根 / 技能目录解析（去硬编码路径） | — |
| `skill_factory/cli.py` | 统一命令行入口 | — |

## 提交前检查清单

1. `make ci` 全绿（lint / format / mypy / 测试覆盖 / 清单漂移门禁）。
2. 若新增/改名/删除了技能：运行 `skill-factory scan` 重新生成能力清单并一并提交。
3. 新增代码补充对应 `tests/` 用例；公共函数需类型标注（mypy `disallow_untyped_defs`）。
4. 不要提交 `.DS_Store`、`__pycache__`、构建/覆盖率产物（已在 `.gitignore`）。

## 新增 / 修改技能约定

- 遵循 `.claude/skills/underlying-convention.md`；执行任何 Skill 前先阅读该约定，**不要修改**它本身。
- 目录与命名用 kebab-case 英文；元 Skill 以 `meta-` / `元-` 前缀标识，可豁免 10 分钟可验证要求，
  产出模板/流程/方案而非直接可执行代码。
- 每个技能至少包含 `SKILL.md`、`README.md`、`description.md`，并含必需章节
  （能力 / 输入规范 / 输出规范，支持中英文别名）；可用 `skill-factory check <技能目录>` 自检。

## 工程层与技能脚本的边界（务实原则）

- `skill_factory/` 只收敛**跨技能的工厂级**能力（扫描 / 校验 / 同步 / 推荐）。
- `micro-diff-factory` / `flutter_factory` 等**各技能自有实现**保留在各自目录（单一职责），
  仅要求可运行、无硬编码绝对路径、按需 lint 清理。
