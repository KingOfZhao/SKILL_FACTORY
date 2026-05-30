# 反模式条目模板（anti-patterns.md 填充用）

每个领域实例的 `references/anti-patterns.md` 至少 8 条，按下列模板编写，
尽量让"错误写法"可被静态检测（便于配套扫描器）。

## 单条模板

```
### AP-<n>：<一句话标题>
- 严重度：critical | major | minor
- 错误写法：
  <反例代码/做法（尽量是可正则匹配的特征）>
- 修正写法：
  <正例代码/做法>
- 为什么：<强模型不会这么做的原因，1-2 句>
- 可检测特征：<供扫描器使用的关键词/正则，若可检测>
```

## 示例（取自 Flutter 实例）

```
### AP-1：在 build() 内发起网络请求
- 严重度：critical
- 错误写法：Widget build(...) { http.get(...); ... }
- 修正写法：请求放 initState / ViewModel，UI 用 FutureBuilder/状态监听
- 为什么：build 每次 rebuild 都会执行，导致重复请求与抖动
- 可检测特征：build() 方法体内出现 http./await/.fetch(
```

## 严重度与退出码约定（供配套扫描器统一）
- critical / major → 扫描器退出码 1（阻断交付）
- minor / info → 退出码 0（提示）
