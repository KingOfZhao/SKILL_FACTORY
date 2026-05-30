# meta-capability-distillation 设计说明

## 问题

`meta-flutter-impl-distillation` 验证了"把强模型隐性策略蒸馏为普通模型可执行知识"在 Flutter 领域有效，
但该方法本身（决策树 / playbook / 反模式 / 自检闭环 4 载体）是**领域无关**的。若每个领域都从零重写，
会重复劳动且质量参差。

## 方案

把蒸馏方法抽象为一个**领域无关的元 Skill**：
- 固化 4 类蒸馏载体 + 1 类规范片段的定义与质量门槛；
- 提供"通用槽位 → 领域取值"的实例化指南（以 Flutter 实例为完整对照）；
- 提供反模式条目与自检闭环的填充模板；
- 用 `--mode audit` 对派生的领域 Skill 做合规自检（反模式≥8、自检可执行、Input/Output 齐全）。

## 与现有技能的关系

- `meta-flutter-impl-distillation`：本 Skill 在 Flutter 领域的**已落地实例**。
- `meta-skill-生成器` / `meta-skill-enhancer`：负责"生成/增强任意 Skill"；本 Skill 专注"蒸馏型 Skill"这一子类的方法学。
- `meta_skill_checker.py`：可用于校验派生实例的章节合规性（已支持中文章节别名）。

## 预期效果

给定一个新领域 + 少量强模型样本，可在不重造方法的情况下，快速产出一个结构合规、含负知识与可执行自检的领域蒸馏 Skill。

## 已知限制

- 提示蒸馏而非权重蒸馏；空骨架不构成可用蒸馏，领域知识仍需人工/样本填充。
- 对"反模式难以客观提炼"的强主观领域收益有限。
