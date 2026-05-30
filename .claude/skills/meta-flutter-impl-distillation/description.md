# 元-Flutter 代码实现蒸馏器（description.md）

## 核心问题
普通模型能写出"能跑"的 Flutter 代码，但与强模型（Opus 级）相比，常在以下方面拉开差距：
选型不当（架构/状态管理）、性能反模式（`build()` 内做重活、长列表用 `Column`）、
null-safety 不严谨（滥用 `!`）、缺少 `const`、错误处理缺失、不写测试、不自检。
这些差距大多来自"隐性经验"，普通模型缺乏可遵循的显式流程。

## 问题背景
1. 强模型的高质量来自大量隐性决策与自我校验，难以被普通模型复现。
2. Flutter 官方已提供 Agent Skills（flutter/skills）与 AI Rules，但它们是"分散能力"，缺少把它们编排成"一次高质量实现"的上层流程。
3. 本仓库哲学：以"元 Skill 定义 Skill"，把隐性认知结构化为显式、可验证的节点。

## 解决方案
采用 **prompt / knowledge distillation（提示蒸馏）**，把强模型隐性能力外化为 4 类显式知识，并叠加官方资源：
- **决策树**：架构/状态/异步/性能的选型，消除"凭感觉选"。
- **实现 playbook**：固定的分阶段实现顺序（澄清→约束→选型→数据→状态→UI→错误/边界→性能→测试→自检）。
- **反模式库（负知识）**：列出普通模型常犯错误及其修正，价值最高。
- **自检闭环**：交付前 guardrail（dart format / analyze / test）。
- **编排官方 Skill**：每一步指明调用 flutter/skills 哪个 skill、遵循哪条官方 rule。

## 输入
- 需求描述（要实现的 Flutter 功能/组件/模块）
- 模式：full / review / decide
- （review）既有代码路径

## 输出
- `decision-record.md`：选型决策与官方映射
- `implementation/`：生成或修改的 Dart 代码
- `distillation-report.md`：已应用的 patterns/rules + 反模式自查结果
- `self-review.md`：guardrail 结果或命令建议

## 使用场景
1. 让普通模型在缺乏 Flutter 经验时也能产出接近强模型质量的实现。
2. 对已有 Flutter 代码做"蒸馏式 code review"（review 模式）。
3. 在动手前做结构化选型（decide 模式）。
4. 作为 `flutter_factory` 的质量增强层串联使用。

## 预期效果
普通模型按本 Skill 流程实现 Flutter 功能时：
1. 选型有据（决策树 + 官方 rule）。
2. 自动规避高频反模式。
3. 交付前完成 guardrail 自检。
4. 产出可对比的蒸馏报告，便于人工 10 分钟内判断质量。

## 已知局限
- 提示蒸馏而非权重蒸馏，效果上限受宿主模型基础能力限制。
- 仅覆盖 Flutter/Dart 实现领域。
- 官方 Skill 清单更新后需同步映射文件。
- Guardrail 真实执行依赖 Dart/Flutter MCP 或本地 SDK。
