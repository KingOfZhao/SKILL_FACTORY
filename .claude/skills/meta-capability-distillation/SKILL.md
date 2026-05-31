---
name: meta-capability-distillation
description: 元-能力蒸馏器 - 将强模型(如 Opus 级)在任意领域的隐性实现/解题策略蒸馏为显式的决策树/playbook/反模式库/自检闭环，使普通模型在该领域的产出质量接近强模型。是 meta-flutter-impl-distillation 的领域无关泛化模板。
---

# 元-能力蒸馏器（Meta Capability Distiller）

## 定位（元 Skill）

本 Skill 属于**元 Skill**（`meta-` 前缀），按 `common/underlying-convention.md` 第 5 条**豁免 10 分钟验证原则**。
它不直接解决某个具体领域问题，而是输出一套**可被实例化的"能力蒸馏方法论 + 模板"**：把"强模型 → 普通模型"的蒸馏流程抽象出来，套用到任意领域（Flutter、后端、数据分析、写作……）即可派生出一个领域专用蒸馏 Skill。

> 与 `meta-flutter-impl-distillation` 的关系：后者是本 Skill 在 **Flutter 领域的一个实例**。本 Skill 提供领域无关的骨架与实例化指南；领域 Skill 填入该领域的决策树/反模式/规范。

## Capabilities（单一职责）

- 定义"强模型隐性策略 → 普通模型显式知识"的 **4 类蒸馏载体**（决策树 / playbook / 反模式库 / 自检闭环）+ 1 类规范片段，与领域解耦。
- 提供**实例化指南**：给定一个目标领域，产出一个结构合规的领域蒸馏 Skill（目录、文件、机器可读规则块）。
- 约束蒸馏质量：要求每个实例都包含负知识（反模式）与可执行/可对比的自检闭环。

## 蒸馏方法说明（强模型 → 普通模型，领域无关）

无法在线连接强模型做权重蒸馏，故统一采用 **prompt / knowledge distillation（提示蒸馏）**：
把强模型"默默做对"的事，转写为普通模型"必须照做"的显式步骤与检查项。4 个载体 + 1 类片段：

| 载体 | 实例文件（领域 Skill 内） | 蒸馏的是 |
|------|---------------------------|---------|
| 决策树 | `references/decision-trees.md` | 强模型的"选型/取舍直觉" |
| 实现 playbook | `references/implementation-playbook.md` | 强模型的"分阶段顺序与思考" |
| 反模式库 | `references/anti-patterns.md` | 强模型"不会犯"的错误（负知识，价值最高） |
| 自检闭环 | `references/self-review-checklist.md` | 强模型"交付前的自我校验" |
| 规范片段 | `references/distilled-patterns.md` | 强模型偏好的 canonical 写法 |

## 执行前必须读取

1. `common/underlying-convention.md`（仓库统一底层约定，第一步必读）
2. 本 `SKILL.md`
3. `references/instantiation-guide.md`（如何把本方法实例化到目标领域）

## MCP 依赖声明（强关联检查）

本 Skill 本身**领域无关**，无固定 MCP 强关联。
但在**实例化**某领域 Skill 时，必须按底层约定为该领域执行 MCP 强关联检查（如 Flutter→Dart/Flutter MCP），并把结论写入实例的 MCP 依赖声明。
禁止本 Skill 自行安装/启动/修改任何 MCP server。

## Input Specification（输入规范）

| 参数 | 格式 | 说明 |
|------|------|------|
| 目标领域 | 文本 | 要蒸馏的领域（如 "FastAPI 后端实现"、"SQL 优化"、"技术写作"） |
| 强模型样本 | 文本/路径(可选) | 该领域强模型优质产出样本，用于提炼决策与反模式 |
| 模式 | enum | `scaffold`(默认,产出领域 Skill 骨架) / `extract`(从样本提炼载体内容) / `audit`(审查既有领域 Skill 是否合规) |

示例：
```bash
/meta-capability-distillation "FastAPI 后端接口实现"
/meta-capability-distillation --mode audit --path .claude/skills/meta-flutter-impl-distillation
```

## 执行流程（7 步骤）

```
1. 读取底层约定 + 本 SKILL + instantiation-guide
2. 领域 MCP 强关联检查（为目标领域判定是否有强关联 MCP）
3. 领域解构：明确该领域的"选型维度 / 阶段顺序 / 常见错误 / 交付标准"
4. 填充 4 载体：decision-trees / implementation-playbook / anti-patterns / self-review-checklist（+ distilled-patterns）
5. 生成领域 Skill 骨架（kebab-case 命名、meta- 前缀、含机器可读规则块）
6. 用 audit 自检：反模式≥8 条、自检闭环可执行/可对比、Input/Output 规范齐全
7. 输出领域 Skill 目录 + 蒸馏方法报告到 output/
```

## Output Specification（输出规范）

应用本 Skill 后产出到 `output/<iteration-id>/`：

```
output/<iteration-id>/
├── <domain>-distillation-skill/   # 派生的领域蒸馏 Skill（SKILL.md + references/）
├── distillation-method-report.md  # 蒸馏方法应用记录（4 载体覆盖、负知识数量）
└── audit.md                       # 合规自检结果（命名/章节/反模式/自检闭环）
```

## 快速验证指南（可选，元 Skill 已豁免但仍提供）

1. **结构完整性**（<2 分钟）：`ls .claude/skills/meta-capability-distillation/references` 预期含
   `instantiation-guide / distillation-method / anti-pattern-template / self-review-template`。
2. **实例对照**（<3 分钟）：打开 `references/instantiation-guide.md`，确认以
   `meta-flutter-impl-distillation` 为已落地实例，逐项给出"通用槽位 → Flutter 取值"。
3. **方法自洽**（<3 分钟）：`references/distillation-method.md` 的 4 载体与
   `meta-flutter-impl-distillation` 实际文件一一对应（决策树/playbook/反模式/自检）。

## Limitations（必须声明）

- 提示蒸馏，非权重蒸馏；不连接、不调用任何模型权重，效果上限取决于宿主模型基础能力。
- 本 Skill 只产出方法与骨架，**领域知识仍需人工/样本填充**；空骨架不构成可用蒸馏。
- 实例质量依赖目标领域是否有清晰的"反模式"可提炼；强主观领域（如审美）蒸馏收益有限。
- 不修改自身元文件，不修改 `underlying-convention.md`（遵守底层约定第 3 条）。

## 机器可读规则块（供检查器/优化器解析）

```yaml
skill:
  id: meta-capability-distillation
  type: meta
  domain: any                      # 领域无关
  distillation: prompt_knowledge   # 非权重蒸馏
  validation_exempt: true          # meta- 前缀，豁免 10 分钟验证
  generalizes: meta-flutter-impl-distillation
  instances:
    - meta-flutter-impl-distillation
  carriers:                        # 蒸馏 4 载体 + 规范片段
    - decision-trees
    - implementation-playbook
    - anti-patterns
    - self-review-checklist
    - distilled-patterns
  references:
    - references/instantiation-guide.md
    - references/distillation-method.md
    - references/anti-pattern-template.md
    - references/self-review-template.md
  mcp:
    related: []                    # 领域无关；实例化时按领域补充
    must_check: true               # 实例化目标领域时必须做强关联检查
  modes: ["scaffold", "extract", "audit"]
  quality_gate:
    min_anti_patterns: 8
    require_executable_or_comparable_self_review: true
    require_input_output_spec: true
```
