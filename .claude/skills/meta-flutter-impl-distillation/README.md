# meta-flutter-impl-distillation（元-Flutter 代码实现蒸馏器）

把强模型（Opus 级）写 Flutter 代码时的**隐性实现策略**，蒸馏为显式、可被普通模型逐步执行的
**决策树 + 实现 playbook + 反模式库 + 自检闭环**，并**叠加在 Flutter 官方 Skill / AI Rules 之上**，
使普通模型在 Flutter 代码实现上接近强模型质量。

- 类型：元 Skill（`meta-` 前缀，豁免 10 分钟验证原则）
- 蒸馏方式：prompt / knowledge distillation（提示蒸馏，非权重蒸馏）
- 结合对象：[flutter/skills](https://github.com/flutter/skills) + [Flutter/Dart AI Rules](https://docs.flutter.dev/ai/ai-rules)

## 文件结构

```
meta-flutter-impl-distillation/
├── SKILL.md                          # 主定义（流程 / 分类 / 机器可读规则）
├── description.md                    # 问题 / 方案 / 局限
├── README.md                         # 本文件
├── references/
│   ├── official-skills-map.md        # 官方 skill/rule 映射 + 安装命令
│   ├── implementation-playbook.md    # Opus 级"逐步实现"操作流程
│   ├── decision-trees.md             # 架构/状态/异步/性能 选型决策树
│   ├── anti-patterns.md              # 普通模型高频错误 → 修正（负知识）
│   ├── self-review-checklist.md      # 自检闭环 + guardrail 命令
│   └── distilled-patterns.md         # 蒸馏后的 canonical Dart 片段
└── output/                           # 应用时生成的实现/报告
```

## 使用方法

```bash
# 全流程：澄清→选型→实现→自检
/meta-flutter-impl-distillation "实现一个带分页与下拉刷新的商品列表页"

# review 模式：对已有代码做蒸馏式自查
/meta-flutter-impl-distillation --mode review --path lib/features/cart

# decide 模式：只做选型决策
/meta-flutter-impl-distillation --mode decide "实时蓝牙 RSSI 曲线"
```

## 与 flutter_factory 的关系

- `flutter_factory`：负责"生成什么"（脚手架/模板/粒度）。
- 本 Skill：负责"如何把实现做到 Opus 级质量"（决策/反模式/自检），可作为前者的质量增强层串联使用。

## 快速验证

```bash
ls references         # 应有 6 个 reference 文件
```
打开 `decision-trees.md`：对"本地单值状态"应得出 `ValueNotifier + ValueListenableBuilder`；
打开 `anti-patterns.md`：应含 build() 内请求、缺 const、滥用 `!`、长列表用 Column 等"错误→修正"对照。

## 局限

提示蒸馏而非权重蒸馏，效果上限取决于宿主模型基础能力；仅覆盖 Flutter/Dart 实现领域；
官方 skill 清单更新后需同步 `references/official-skills-map.md`；guardrail 真实执行依赖 Dart/Flutter MCP 或本地 SDK。
