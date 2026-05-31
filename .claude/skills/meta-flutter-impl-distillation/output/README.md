# output/

应用本 Skill（`full` / `review` 模式）后，按迭代 id 在此生成产物：

```
output/<iteration-id>/
├── decision-record.md      # 选型决策 + 官方 skill/rule 映射（来自 decision-trees.md）
├── implementation/         # 生成或修改的 .dart 代码
├── distillation-report.md  # 已应用 patterns/rules 清单 + 反模式自查（命中/修正）
└── self-review.md          # guardrail 结果（dart format / flutter analyze / flutter test）
```

`<iteration-id>` 建议格式：`flutter-impl-<功能名>-<序号>`，例如 `flutter-impl-cart-001`。

> 本目录仅保留说明文件；实际产物由具体调用生成，可纳入 .gitignore 或按需保留示例。
