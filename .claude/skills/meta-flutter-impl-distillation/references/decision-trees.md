# 选型决策树（decision-trees.md）

> 蒸馏对象：强模型的"选型直觉"。普通模型按树走即可得到与强模型一致的默认选择。
> 原则（官方 rule）：**优先 Flutter 内置方案，非显式要求不引第三方状态库**。

## 1. 架构决策树

```
项目规模？
├─ 单组件 / 一次性脚本        → 单文件，逻辑与 UI 仍分函数
├─ 中小 App（<~10 屏）        → 分层：presentation / domain / data / core
└─ 大型 / 多团队              → 按 feature 组织，每个 feature 内含 presentation/domain/data
                               （→ flutter-apply-architecture-best-practices）
```
依赖方向：presentation → domain ← data；domain 不依赖任何外层（依赖倒置，Repository 接口在 domain）。

## 2. 状态管理决策树

```
状态是什么？
├─ 单个局部值（计数、开关）           → ValueNotifier + ValueListenableBuilder
├─ 一组相关状态、被多处共享           → ChangeNotifier + ListenableBuilder
├─ 单次异步结果（一次请求）           → Future + FutureBuilder
├─ 异步事件序列（实时流/订阅）         → Stream + StreamBuilder
├─ 需要清晰分层的复杂应用状态          → MVVM（ViewModel 持状态，UI 只渲染）
└─ 用户显式要求某第三方库             → 才使用 Riverpod / Bloc / Provider
```
判据：先问"内置能否胜任？" 能则不引第三方。依赖注入默认用**构造注入**（显式、可测）。

## 3. 异步形态决策树

```
异步的性质？
├─ 一次完成的操作（HTTP GET、读文件一次）     → Future + async/await + try/catch
├─ 连续事件（WebSocket、传感器、蓝牙 RSSI）   → Stream + StreamSubscription（记得 cancel）
├─ CPU 密集（JSON 大解析、加解密、图像）       → compute() 放独立 isolate
└─ 多个独立异步并行                          → Future.wait([...])
```
错误处理：统一 try/catch + 自定义异常类型；对用户暴露可恢复信息；用 `logging` 记录，不要 `print`。

## 4. 列表 / 性能决策树

```
要渲染的集合多大？
├─ 固定少量（<~10，且已知）   → Column / Row + children（可全 const）
├─ 可变 / 较长               → ListView.builder（懒加载）
├─ 复杂滚动（混合头部/网格）   → CustomScrollView + Sliver(SliverList/SliverGrid)
└─ 超大数据 + 复杂项          → ListView.builder + 项内尽量 const + 避免重建整树
```
通用性能规则（官方）：
- 能 `const` 就 `const`（减少 rebuild）。
- `build()` 内禁止网络/重计算。
- 重活用 `compute()`。
- 拆分大 `build()` 为小型私有 Widget 类（缩小 rebuild 范围）。

## 5. 路由决策树

```
导航需求？
├─ 简单堆栈（push/pop）               → Navigator 1.0 足够
└─ 深链 / Web URL / 复杂嵌套          → 声明式路由 go_router（→ flutter-setup-declarative-routing）
```

## 6. 数据建模决策树

```
数据形态？
├─ 简单、手写映射         → 普通不可变类 + 手写 fromJson/toJson（→ flutter-implement-json-serialization）
├─ 字段多 / 需要 copyWith → 考虑代码生成（json_serializable/freezed，需显式同意引第三方）
└─ 临时多返回值           → record，避免造一次性类
```

## 选型记录模板（写入 output/<id>/decision-record.md）

```md
| 维度 | 选择 | 理由 | 官方映射 |
|------|------|------|---------|
| 架构 | 分层(P/D/D/C) | 中小 App | flutter-apply-architecture-best-practices |
| 状态 | ChangeNotifier | 多处共享、无需第三方 | rule:内置优先 |
| 异步 | Stream | 实时 RSSI 流 | rule:Stream/StreamBuilder |
| 列表 | ListView.builder | 设备数可变 | rule:长列表懒加载 |
```
