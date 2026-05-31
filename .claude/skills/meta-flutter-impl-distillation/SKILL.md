---
name: meta-flutter-impl-distillation
description: 元-Flutter 代码实现蒸馏器 - 将强模型(Opus 级)的隐性 Flutter 实现策略蒸馏为显式决策树/实现 playbook/反模式库/自检闭环，叠加在 Flutter 官方 Skill 与 AI Rules 之上，使普通模型在 Flutter 代码实现上接近强模型质量。
---

# 元-Flutter 代码实现蒸馏器（Meta Flutter Implementation Distiller）

## 定位（元 Skill）

本 Skill 属于**元 Skill**（`meta-` 前缀），按 `common/underlying-convention.md` 第 5 条**豁免 10 分钟验证原则**。
它不直接生成某一个具体 App，而是输出一套"实现强化层"——把强模型写 Flutter 代码时的隐性决策外化为可被普通模型逐步执行的显式知识，并**编排调用 Flutter 官方 Skill / AI Rules**。

> 与 `flutter_factory` 的关系：`flutter_factory` 负责"生成什么"（脚手架/模板/粒度）；本 Skill 负责"如何把代码实现到 Opus 级质量"（决策、反模式、自检）。两者可串联使用。

## Capabilities（单一职责）

- 将"强模型隐性实现策略"蒸馏为 4 类显式知识：决策树、实现 playbook、反模式库（负知识）、自检 guardrail。
- 在每个实现阶段**映射到官方资源**：`flutter/skills` 对应 skill + 官方 AI Rules 对应条款。
- 驱动普通模型按固定流程产出代码，并生成可对比的"蒸馏报告"（applied rules/patterns + 自检结果）。

## 蒸馏方法说明（Opus → 普通模型）

无法在线连接强模型做权重蒸馏，故采用 **prompt / knowledge distillation（提示蒸馏）**：
把强模型在实现时"默默做对"的事，转写为普通模型"必须照做"的显式步骤与检查项。蒸馏的 4 个载体：

| 载体 | 文件 | 蒸馏的是 |
|------|------|---------|
| 决策树 | `references/decision-trees.md` | 强模型的"选型直觉"（架构/状态/异步/性能） |
| 实现 playbook | `references/implementation-playbook.md` | 强模型的"分阶段实现顺序与思考" |
| 反模式库 | `references/anti-patterns.md` | 强模型"不会犯"的错误（负知识，价值最高） |
| 自检闭环 | `references/self-review-checklist.md` | 强模型"交付前的自我校验" |
| 规范片段 | `references/distilled-patterns.md` | 强模型偏好的 canonical 写法 |

## 核心蒸馏实践（关键约定，不可降级）

本 Skill 蒸馏出的不可降级项，普通模型必须落实（详见各 reference）：

- **分层架构**：按 `domain/entities`、`data/models`、`data/repositories`、`presentation/pages` 分层；依赖指向 domain。
- **Repository 模式**：数据访问统一经 Repository 接口（接口在 domain，实现在 data），通过构造函数注入（便于测试）。
- **MVVM / Observer**：业务逻辑下沉到 ViewModel/Model；状态用 `ChangeNotifier` + `notifyListeners`（Observer）驱动 UI 重建。
- **错误处理**：异步统一 `try` / `catch` + 自定义异常，覆盖 loading/empty/error 四态，不静默失败（fallback 可恢复）。
- **性能**：能 `const` 就 `const`（优先 `const Widget` 构造），长列表用 `ListView.builder`，重计算用 `compute()`。
- **可测性**：至少一个 widget test（`flutter test`）；依赖可注入 fake/mock。

## 执行前必须读取

1. `common/underlying-convention.md`（仓库统一底层约定，第一步必读）
2. 本 `SKILL.md`
3. `references/official-skills-map.md`（官方 Skill / Rules 映射）

## MCP 依赖声明（强关联检查）

本 Skill 强关联 **Dart & Flutter MCP server**（用于 `dart format` / `analyze_files` / `pub` / widget 预览等）。
按底层约定执行 MCP 强关联检查：

- 关键词强关联：`flutter / dart / widget / pub / analyze` → Dart & Flutter MCP。
- **若已连接**：执行 guardrail（格式化、analyze、测试）时强制优先使用该 MCP，并在输出标注"已使用 Dart/Flutter MCP 执行 …"。
- **若未连接**：降级为"纯描述 + 手动命令建议"（输出等价的 `dart format .` / `flutter analyze` / `flutter test` 命令），并在 Limitations 声明降级。
- 禁止本 Skill 自行安装/启动/修改任何 MCP server。

## Input Specification（输入规范）

| 参数 | 格式 | 说明 |
|------|------|------|
| 需求描述 | 文本 | 要实现的 Flutter 功能/组件/模块 |
| 模式 | enum | `full`(默认,全流程) / `review`(只对已有代码做蒸馏自查) / `decide`(只做选型决策) |
| 既有代码路径 | 路径(可选) | `review` 模式下指向待审查代码 |

示例：
```bash
/meta-flutter-impl-distillation "实现一个带分页与下拉刷新的商品列表页"
/meta-flutter-impl-distillation --mode review --path lib/features/cart
```

## 执行流程（7 步骤）

```
1. 读取底层约定 + 本 SKILL + official-skills-map
2. MCP 强关联检查（Dart/Flutter MCP 是否连接）
3. 需求澄清与约束提取（自上而下解构：目标平台/状态范围/数据来源/边界条件）
4. 按 decision-trees 选型（架构/状态管理/异步/列表性能）→ 标注对应官方 skill+rule
5. 按 implementation-playbook 分阶段实现代码（每阶段引用 distilled-patterns）
6. 负向自查（anti-patterns）+ 正向 guardrail（self-review-checklist：format/analyze/test）
7. 输出代码 + 蒸馏报告到 output/
```

## 与官方 Skill 的编排（核心）

本 Skill 不复制官方内容，只做"何时调用何者"的映射。详见 `references/official-skills-map.md`。摘要：

| 实现阶段 | 调用的官方 Skill (flutter/skills) | 遵循的官方 Rule |
|---------|----------------------------------|----------------|
| 架构分层 | flutter-apply-architecture-best-practices | Application Architecture / 分层 |
| 响应式 UI | flutter-build-responsive-layout | Composition / 私有 Widget 类 |
| 布局报错 | flutter-fix-layout-issues | constraints/overflow 处理 |
| 路由 | flutter-setup-declarative-routing | go_router/auto_route |
| 数据模型 | flutter-implement-json-serialization | null-safety / records |
| 测试 | flutter-add-widget-test / flutter-add-integration-test | "Testing in mind" guardrail |
| 预览 | flutter-add-widget-preview | — |

官方安装命令：
```bash
npx skills add flutter/skills --skill '*' --agent universal
# Dart 任务可同时安装 dart-lang/skills
```

## Output Specification（输出规范）

应用本 Skill 后产出到 `output/<iteration-id>/`：

```
output/<iteration-id>/
├── decision-record.md     # 选型决策 + 对应官方 skill/rule（来自步骤 4）
├── implementation/        # 生成/修改的 .dart 代码
├── distillation-report.md # 已应用的 patterns/rules 清单 + 反模式自查结果
└── self-review.md         # guardrail 结果（format/analyze/test 输出或命令建议）
```

## 快速验证指南（可选，元 Skill 已豁免但仍提供）

1. **结构完整性**（<2 分钟）
   ```bash
   ls .claude/skills/meta-flutter-impl-distillation/references
   ```
   预期：6 个 reference 文件（official-skills-map / implementation-playbook / decision-trees / anti-patterns / self-review-checklist / distilled-patterns）。
2. **决策树可用性**（<3 分钟）：打开 `references/decision-trees.md`，对"本地单值状态"应得出 `ValueNotifier + ValueListenableBuilder`。
3. **反模式覆盖**（<3 分钟）：打开 `references/anti-patterns.md`，确认含 `build()` 内网络请求、缺 `const`、滥用 `!`、长列表用 `Column` 等条目，且每条有"错误→修正"对照。
4. **自检命令可运行**（<2 分钟）：`references/self-review-checklist.md` 中的 `dart format .`、`flutter analyze`、`flutter test` 为标准命令，可直接复制执行。
5. **扫描器自检**（<1 分钟）：`python3 scripts/flutter_lint_scan.py --selftest` 应输出 `SELFTEST PASS`（零依赖，验证反模式检测有效）。

成功标志：以上 5 项齐全且内容自洽。

## Limitations（必须声明）

- 采用提示蒸馏，非权重蒸馏；不连接、不调用任何模型权重，效果上限取决于宿主模型的基础能力。
- 仅覆盖 Flutter/Dart 代码实现领域，不处理后端、原生平台深度定制等非 Flutter 问题。
- 官方 Skill 映射基于 `flutter/skills` 当前清单，官方更新后需同步 `references/official-skills-map.md`。
- Guardrail 的真实执行依赖 Dart/Flutter MCP 或本地 Flutter SDK；未连接时为降级（仅命令建议）。
- 不修改自身元文件，不修改 `underlying-convention.md`（遵守底层约定第 3 条）。

## 机器可读规则块（供检查器/优化器解析）

```yaml
skill:
  id: meta-flutter-impl-distillation
  type: meta
  domain: flutter
  distillation: prompt_knowledge   # 非权重蒸馏
  validation_exempt: true          # meta- 前缀，豁免 10 分钟验证
  composes_with:
    official_skills_repo: "github.com/flutter/skills"
    official_rules: "docs.flutter.dev/ai/ai-rules"
    sibling_skills: ["flutter_factory"]
  references:
    - references/official-skills-map.md
    - references/implementation-playbook.md
    - references/decision-trees.md
    - references/anti-patterns.md
    - references/self-review-checklist.md
    - references/distilled-patterns.md
  mcp:
    related: ["dart-flutter-mcp"]
    must_check: true
    must_use_if_connected: true
  modes: ["full", "review", "decide"]
```
