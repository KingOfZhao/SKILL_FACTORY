# meta-capability-distillation（元-能力蒸馏器）

领域无关的"强模型 → 普通模型"蒸馏方法模板。是 `meta-flutter-impl-distillation` 的泛化。

## 文件结构

```
meta-capability-distillation/
├── SKILL.md                         # 方法定位、流程、机器可读规则块
├── description.md                   # 设计说明
├── README.md
├── references/
│   ├── distillation-method.md       # 4 载体 + 规范片段（领域无关定义）
│   ├── instantiation-guide.md       # 通用槽位→领域取值（含 Flutter 对照）
│   ├── anti-pattern-template.md     # 反模式条目模板
│   └── self-review-template.md      # 自检闭环模板
└── output/                          # 实例化产物落点
```

## 用法

```bash
# 为新领域产出一个领域蒸馏 Skill 骨架
/meta-capability-distillation "FastAPI 后端接口实现"

# 审查既有领域蒸馏 Skill 是否合规
/meta-capability-distillation --mode audit --path .claude/skills/meta-flutter-impl-distillation
```

## 快速验证

1. `ls references/` 含 4 个文件。
2. `instantiation-guide.md` 以 `meta-flutter-impl-distillation` 为完整对照。
3. `distillation-method.md` 的 4 载体与 Flutter 实例文件一一对应。

## 限制

提示蒸馏，非权重蒸馏；只产出方法与骨架，领域知识需人工/样本填充。
