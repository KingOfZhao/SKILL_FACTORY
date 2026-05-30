# 实例化指南：把方法套到一个目标领域

本指南给出"通用槽位 → 领域取值"的映射表，并以已落地实例
`meta-flutter-impl-distillation` 作为完整对照。

## 步骤

1. 命名：`meta-<domain>-impl-distillation`（kebab-case，`meta-` 前缀，禁用中文目录名）。
2. 复制本 Skill 的目录骨架，建立 `references/` 下 5 个载体文件（见 distillation-method.md）。
3. 为目标领域做 MCP 强关联检查，写入实例 SKILL.md 的"MCP 依赖声明"。
4. 逐个填充 4 载体 + 规范片段（领域知识来自强模型样本 / 官方最佳实践）。
5. 写机器可读规则块（`type: meta`、`validation_exempt: true`、`carriers`、`quality_gate`）。
6. 用本 Skill `--mode audit` 自检，确保达标。

## 通用槽位 → 领域取值（对照表）

| 通用槽位 | 含义 | Flutter 实例取值（meta-flutter-impl-distillation） |
|----------|------|----------------------------------------------------|
| domain | 目标领域 | flutter |
| 决策维度 | 决策树覆盖的取舍点 | 架构分层 / 状态管理 / 异步形态 / 列表性能 / 路由 / 数据建模 |
| 阶段顺序 | playbook 步骤 | 澄清→选型→数据层→逻辑→UI→四态→测试→自检 |
| 反模式来源 | anti-patterns 提炼自 | build() 内请求、缺 const、滥用 `!`、长列表用 Column 等 14 条 |
| 工具链 guardrail | 自检可运行命令 | `dart format` / `flutter analyze` / `flutter test` + 扫描器 |
| 官方资源编排 | 叠加的官方 skill/rules | flutter/skills + docs.flutter.dev/ai/ai-rules |
| 强关联 MCP | 实例的 MCP | Dart & Flutter MCP |
| 配套扫描器 | 可执行自检 | `scripts/flutter_lint_scan.py` |

## 其它领域的快速取值建议（示意）

| 领域 | 决策维度示例 | 反模式来源示例 | guardrail 示例 |
|------|--------------|----------------|----------------|
| FastAPI 后端 | 同步/异步、依赖注入、ORM、错误处理 | 在路由里写业务、N+1 查询、裸 except | `ruff` / `mypy` / `pytest` |
| SQL 优化 | 索引、连接方式、分页 | SELECT *、隐式类型转换、OFFSET 深分页 | `EXPLAIN` 对比 |
| 技术写作 | 结构、受众、示例密度 | 术语未定义、被动堆叠、无示例 | 可读性检查清单 |

> 关键：实例的价值主要来自**反模式库**与**可执行自检**，这两项必须扎实。
