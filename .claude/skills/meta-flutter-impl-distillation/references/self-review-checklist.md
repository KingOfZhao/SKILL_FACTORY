# 自检闭环 / Guardrail（self-review-checklist.md）

> 蒸馏对象：强模型"交付前的自我校验"。普通模型在阶段 7 必须执行，并把结果写入 self-review.md。
> 思路来自官方 best practices：用 Flutter 工具给 AI 加 guardrail（"Morgan's Law：模型终会出错，故需护栏"）。

## A. 负向自查（先做）
逐条对照 `anti-patterns.md`（AP-1 ~ AP-14），标注 命中/未命中：

- [ ] AP-1 build() 内无网络/重计算
- [ ] AP-2 可 const 处已加 const
- [ ] AP-3 长列表用 builder/Sliver
- [ ] AP-4 无裸 `!`（除非保证非空）
- [ ] AP-5 私有 Widget 类而非返回 Widget 的方法
- [ ] AP-6 用 logging 而非 print
- [ ] AP-7 异步有 try/catch，不静默失败
- [ ] AP-8 异步 UI 覆盖 loading/empty/error/success
- [ ] AP-9 controller/subscription 已 dispose/cancel
- [ ] AP-10 无巨型 build()
- [ ] AP-11 逻辑在 ViewModel/UseCase，不在 Widget
- [ ] AP-12 未无故引第三方状态库
- [ ] AP-13 重解析用 compute()
- [ ] AP-14 命名/行宽/函数长度合规

## A.0 自动化反模式扫描（先跑，无需 Flutter SDK）
本 Skill 自带零依赖扫描器，可直接对生成的 Dart 代码做 AP-1/3/4/6/9/13 自动检测：

```bash
# 扫描目录或文件，命中 major/critical 时退出码为 1
python3 scripts/flutter_lint_scan.py lib/ --format text
python3 scripts/flutter_lint_scan.py lib/ --format json --json scan.json
# 脚本自检（约 10 秒）
python3 scripts/flutter_lint_scan.py --selftest
```
把 JSON 报告并入 distillation-report.md；扫描器为启发式补充，不替代 `flutter analyze`。

## B. 正向 Guardrail（命令）
**若 Dart/Flutter MCP 已连接**：优先用 MCP 的 `dart_format` / `dart_fix` / `analyze_files` 工具执行，并标注"已使用 Dart/Flutter MCP …"。
**否则**用本地 SDK 命令：

```bash
# 1. 格式化（统一风格，行宽 80）
dart format .

# 2. 自动修复可修项
dart fix --apply

# 3. 静态分析（目标：0 error / 0 warning）
flutter analyze

# 4. 测试
flutter test

# 5.（可选）集成测试
flutter test integration_test
```

预期：`flutter analyze` 输出 `No issues found!`；`flutter test` 全绿。

## C. analysis_options.yaml 基线（官方）
确保项目启用官方 lint：
```yaml
include: package:flutter_lints/flutter.yaml

linter:
  rules:
    # 按需追加，例如：
    # prefer_single_quotes: true
```

## D. 交付门槛（全部满足才算"接近 Opus 级"）
1. 负向自查 14 条全部"未命中"（或命中项已修正并记录）。
2. `flutter analyze` 0 error / 0 warning。
3. `dart format` 已应用，无格式 diff。
4. 至少 1 个 widget test 通过；关键流有 integration test。
5. 异步 UI 四态齐全；资源已释放。
6. 选型有 decision-record 记录且映射官方 skill/rule。

## E. self-review.md 输出模板
```md
# Self Review
## 负向自查
| AP | 状态 | 备注 |
|----|------|------|
| AP-1 | 未命中 | — |
| AP-4 | 命中→已修正 | user!.name → user?.name ?? '' |
## Guardrail
- dart format: applied (0 diff)
- flutter analyze: No issues found!
- flutter test: 5 passed
## 结论
达到交付门槛 ✔ / 未达（列出阻塞项）
```

## 降级声明
未连接 MCP 且无本地 Flutter SDK 时：B/C 仅输出"建议命令"，self-review.md 标注
"guardrail 为命令建议，未实际执行"，并在 SKILL Limitations 中体现。
