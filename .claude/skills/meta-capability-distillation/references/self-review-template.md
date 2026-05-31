# 自检闭环模板（self-review-checklist.md 填充用）

每个领域实例的自检闭环必须"可执行或可对比"，由三段组成。

## A. 负向自查（逐条勾选反模式）
```
- [ ] AP-1 …
- [ ] AP-2 …
...（覆盖 anti-patterns.md 全部条目）
```

## A.0 自动化扫描（推荐：附零依赖扫描器）
若该领域可静态检测，提供一个 stdlib-only 扫描器，命中 major/critical 时退出码为 1：
```
python3 scripts/<domain>_lint_scan.py <target> --format text
python3 scripts/<domain>_lint_scan.py --selftest
```
参考实现：`meta-flutter-impl-distillation/scripts/flutter_lint_scan.py`。

## B. 正向 Guardrail（领域工具链命令）
列出该领域的格式化 / 静态分析 / 测试命令；若有 MCP 优先用 MCP，并标注已使用。
```
<format 命令>
<lint/analyze 命令>
<test 命令>
```

## C. 交付门槛
明确"满足以下全部条件方可交付"，例如：
- 扫描器无 major/critical；
- 静态分析 0 error/0 warning；
- 关键路径有测试；
- 已产出 self-review.md（含上述结果或命令建议 + 降级声明）。
