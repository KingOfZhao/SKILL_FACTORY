# 反模式库 / 负知识（anti-patterns.md）

> 蒸馏对象：强模型"不会犯"的错误。普通模型在阶段 7 必须逐条自查。
> 每条格式：症状 → ❌ 错误 → ✅ 修正 → 对应官方 rule。

## AP-1 在 build() 内做重活 / 发请求
症状：每次 rebuild 都触发网络或重计算，UI 卡顿。
```dart
// ❌
@override
Widget build(BuildContext context) {
  final data = http.get(url);            // 每帧都请求
  return Text(parseHeavy(data));
}
// ✅ 在 initState / ViewModel 中触发一次，UI 用 FutureBuilder/状态监听
final _future = repository.fetch();      // 仅一次
// ...
FutureBuilder(future: _future, builder: ...);
```
官方 rule：build() 内避免昂贵操作；重计算用 compute()。

## AP-2 缺少 const
症状：可 const 的子树被反复重建。
```dart
// ❌
return Padding(padding: EdgeInsets.all(8), child: Text('Hi'));
// ✅
return const Padding(padding: EdgeInsets.all(8), child: Text('Hi'));
```
官方 rule：尽量用 const 构造，减少 rebuild。

## AP-3 长列表用 Column/ListView(children:)
症状：一次性构建所有项，内存与性能恶化。
```dart
// ❌
Column(children: items.map((e) => ItemTile(e)).toList());
// ✅
ListView.builder(
  itemCount: items.length,
  itemBuilder: (_, i) => ItemTile(items[i]),
);
```
官方 rule：长列表用 ListView.builder / SliverList 懒加载。

## AP-4 滥用 null 断言 `!`
症状：运行时 Null check operator used on a null value。
```dart
// ❌
final name = user!.profile!.name!;
// ✅
final name = user?.profile?.name ?? 'Guest';
```
官方 rule：soundly null-safe，除非保证非空否则不用 `!`。

## AP-5 用返回 Widget 的私有方法而非私有 Widget 类
症状：rebuild 范围过大、无法局部 const、难测试。
```dart
// ❌
Widget _buildHeader() => Row(children: [...]);
// ✅
class _Header extends StatelessWidget {
  const _Header();
  @override
  Widget build(BuildContext context) => Row(children: const [...]);
}
```
官方 rule：用小型私有 Widget 类替代返回 Widget 的 helper 方法。

## AP-6 用 print 调试
```dart
// ❌
print('value=$v');
// ✅
import 'package:logging/logging.dart';
final _log = Logger('Cart');
_log.fine('value=$v');
```
官方 rule：用 logging 包替代 print。

## AP-7 异步无错误处理 / 静默失败
```dart
// ❌
final data = await api.fetch();   // 抛错直接崩
// ✅
try {
  final data = await api.fetch();
} on SocketException catch (e, s) {
  _log.warning('network', e, s);
  state = CartState.error('网络异常，请重试');
}
```
官方 rule：async/await 配健全错误处理；不要静默失败。

## AP-8 缺少异步 UI 的四态
症状：只画 success，loading/empty/error 缺失。
```dart
// ✅ 显式四态
switch (state) {
  Loading() => const CircularProgressIndicator(),
  Empty()   => const Text('暂无数据'),
  Error(:final msg) => RetryView(msg: msg, onRetry: vm.reload),
  Success(:final items) => _List(items: items),
}
```

## AP-9 StatefulWidget 未释放资源
症状：内存泄漏、setState after dispose。
```dart
// ❌ 忘记 dispose
final controller = TextEditingController();
// ✅
@override
void dispose() {
  controller.dispose();
  _subscription.cancel();
  super.dispose();
}
```

## AP-10 巨型 build() 方法
症状：单个 build 上百行，难读难测、rebuild 昂贵。
修正：按 playbook 阶段 4 拆为多个小型私有 Widget 类。
官方 rule：拆分大 build() 为可复用私有 Widget。

## AP-11 业务逻辑塞进 Widget
症状：UI 与逻辑耦合，无法单测。
修正：逻辑下沉到 ViewModel/UseCase，Widget 只渲染 + 转发事件（MVVM/分层）。

## AP-12 非显式要求就引入重型第三方状态库
症状：简单需求引 Bloc/Riverpod，徒增复杂度。
修正：先用内置（ValueNotifier/ChangeNotifier/MVVM）；仅在用户显式要求时引第三方。
官方 rule：默认不引第三方状态管理。

## AP-13 同步阻塞主 isolate 做重解析
```dart
// ❌
final list = parseHugeJson(bigString);     // 卡 UI
// ✅
final list = await compute(parseHugeJson, bigString);
```
官方 rule：昂贵计算放 compute() 的独立 isolate。

## AP-14 魔法值 / 不一致命名 / 超宽行
修正：常量集中到 core/constants；命名 PascalCase/camelCase/snake_case；行宽 ≤ 80；函数 < 20 行单一职责。

## 自查输出
逐条标注 `命中/未命中`，命中项必须在 distillation-report.md 给出修正前后对照。
