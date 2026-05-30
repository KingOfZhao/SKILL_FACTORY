# 实现 Playbook（implementation-playbook.md）

> 蒸馏对象：强模型"分阶段实现 Flutter 功能"的隐性顺序与思考。
> 普通模型**必须按阶段顺序执行**，每阶段附"产出物"与"自检问句"。不要跳阶段直接写 UI。

## 阶段 0 — 需求澄清（先想后写）
- 明确：目标平台（mobile/web/desktop）、是否需离线、数据来源（API/本地/蓝牙等）、交互边界与异常场景。
- 若歧义 → 先提一个最关键澄清问题（官方 rule：歧义先澄清），不要臆测。
- 产出物：一句话需求 + 3~6 条显式约束。
- 自检问句：我是否能列出至少 2 个失败/边界场景？

## 阶段 1 — 选型决策（用 decision-trees.md）
- 依次决定：架构分层 → 状态管理 → 异步形态 → 列表/性能策略。
- 每个决策**记录理由**并映射官方 skill/rule（写入 decision-record.md）。
- 默认值：架构=分层(Presentation/Domain/Data/Core)；状态=内置(ValueNotifier/ChangeNotifier)，非显式要求不引第三方。
- 自检问句：有没有为了"炫技"引入不必要的第三方状态库？

## 阶段 2 — 数据层与模型
- 定义不可变 model（`final` 字段 + `const` 构造）；JSON 用 fromJson/toJson（→ flutter-implement-json-serialization）。
- 健全 null-safety：能为非空就别可空；避免 `!`。
- 多返回值优先 `record`，避免临时类。
- Repository 接口放 Domain，实现放 Data；依赖通过构造注入（便于测试注入 fake）。
- 产出物：models + repository 接口/实现。
- 自检问句：model 是否不可变？是否有任何裸 `!`？

## 阶段 3 — 业务逻辑 / ViewModel
- 业务逻辑与 UI 分离（MVVM/分层）；ViewModel 持有状态、暴露不可变视图状态。
- 异步：单次结果用 `Future`，事件序列用 `Stream`；统一 try/catch + 自定义异常；用 `logging` 而非 `print`。
- 重计算（JSON 解析、加解密、图像）用 `compute()` 放独立 isolate。
- 产出物：ViewModel/UseCase + 错误处理路径。
- 自检问句：耗时操作是否在 build() 之外、且不阻塞 UI？

## 阶段 4 — UI 组合
- 组合优于继承；把大 `build()` 拆成**小型私有 Widget 类**（不要用"返回 Widget 的私有方法"）。
- 能 `const` 就 `const`；列表用 `ListView.builder`/`SliverList`，绝不用 `Column` 渲染长列表。
- 状态绑定：单值 `ValueListenableBuilder`；`Listenable` 用 `ListenableBuilder`；单异步 `FutureBuilder`；流 `StreamBuilder`。
- 响应式 → flutter-build-responsive-layout；出现 overflow → flutter-fix-layout-issues。
- 产出物：页面与可复用组件。
- 自检问句：是否存在超过 ~3 层的无谓嵌套可拆成私有 Widget？

## 阶段 5 — 错误、空态、加载态、边界
- 每个异步 UI 显式覆盖：loading / empty / error / success 四态。
- 用户可见错误要有可恢复路径（重试/提示），不静默失败。
- 自检问句：断网/空数据/超长文本/超长列表是否都不崩、不溢出？

## 阶段 6 — 测试（带着可测性写代码）
- 至少一个 widget test 验证渲染与交互（→ flutter-add-widget-test）。
- 关键用户流加 integration test（→ flutter-add-integration-test）。
- 依赖通过构造注入，测试用 fake/in-memory 替身。
- 自检问句：核心交互是否有断言覆盖？

## 阶段 7 — 自检闭环（用 self-review-checklist.md）
- 先做**负向自查**（anti-patterns.md 逐条过），再跑 guardrail：`dart format .` → `flutter analyze` → `flutter test`。
- 产出蒸馏报告：applied rules/patterns 清单 + 反模式自查结果 + guardrail 输出。
- 自检问句：analyze 是否 0 warning？格式化是否已应用？

## 阶段顺序图

```
澄清 → 选型 → 数据/模型 → 逻辑/VM → UI 组合 → 四态/边界 → 测试 → 自检闭环
  │                                                              │
  └────────────（任何阶段发现选型错误，回到"选型"重做）─────────────┘
```
