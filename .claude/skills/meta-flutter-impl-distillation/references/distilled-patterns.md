# 蒸馏后的规范片段（distilled-patterns.md）

> 蒸馏对象：强模型偏好的 canonical 写法。普通模型实现时直接复用这些骨架。
> 所有片段遵循官方 rule：不可变、null-safe、const、组合优于继承、可测。

## P-1 不可变 Model + JSON
```dart
class Product {
  const Product({required this.id, required this.name, required this.price});

  final String id;
  final String name;
  final double price;

  factory Product.fromJson(Map<String, dynamic> json) => Product(
        id: json['id'] as String,
        name: json['name'] as String,
        price: (json['price'] as num).toDouble(),
      );

  Map<String, dynamic> toJson() => {'id': id, 'name': name, 'price': price};

  Product copyWith({String? name, double? price}) => Product(
        id: id,
        name: name ?? this.name,
        price: price ?? this.price,
      );
}
```

## P-2 Repository（接口在 domain，实现在 data，构造注入）
```dart
// domain/repositories/product_repository.dart
abstract interface class ProductRepository {
  Future<List<Product>> fetchProducts();
}

// data/repositories/product_repository_impl.dart
class ProductRepositoryImpl implements ProductRepository {
  ProductRepositoryImpl(this._client);
  final ApiClient _client;          // 构造注入，测试可换 fake

  @override
  Future<List<Product>> fetchProducts() async {
    final raw = await _client.getJson('/products');
    return raw.map(Product.fromJson).toList();
  }
}
```

## P-3 ViewModel（ChangeNotifier + 密封状态 + 四态）
```dart
sealed class CartState {
  const CartState();
}
class CartLoading extends CartState { const CartLoading(); }
class CartEmpty   extends CartState { const CartEmpty(); }
class CartError   extends CartState { const CartError(this.message); final String message; }
class CartLoaded  extends CartState { const CartLoaded(this.items); final List<Product> items; }

class CartViewModel extends ChangeNotifier {
  CartViewModel(this._repo);
  final ProductRepository _repo;
  static final _log = Logger('CartViewModel');

  CartState _state = const CartLoading();
  CartState get state => _state;

  Future<void> load() async {
    _set(const CartLoading());
    try {
      final items = await _repo.fetchProducts();
      _set(items.isEmpty ? const CartEmpty() : CartLoaded(items));
    } on Exception catch (e, s) {
      _log.warning('load failed', e, s);
      _set(const CartError('加载失败，请重试'));
    }
  }

  void _set(CartState s) {
    _state = s;
    notifyListeners();
  }
}
```

## P-4 UI：四态渲染 + 小型私有 Widget + 懒加载列表
```dart
class CartPage extends StatelessWidget {
  const CartPage({super.key, required this.vm});
  final CartViewModel vm;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('购物车')),
      body: ListenableBuilder(
        listenable: vm,
        builder: (context, _) => switch (vm.state) {
          CartLoading() => const Center(child: CircularProgressIndicator()),
          CartEmpty()   => const Center(child: Text('暂无商品')),
          CartError(:final message) =>
            _RetryView(message: message, onRetry: vm.load),
          CartLoaded(:final items) => _ProductList(items: items),
        },
      ),
    );
  }
}

class _ProductList extends StatelessWidget {
  const _ProductList({required this.items});
  final List<Product> items;

  @override
  Widget build(BuildContext context) => ListView.builder(
        itemCount: items.length,
        itemBuilder: (_, i) => _ProductTile(product: items[i]),
      );
}

class _RetryView extends StatelessWidget {
  const _RetryView({required this.message, required this.onRetry});
  final String message;
  final VoidCallback onRetry;

  @override
  Widget build(BuildContext context) => Center(
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Text(message),
            const SizedBox(height: 8),
            FilledButton(onPressed: onRetry, child: const Text('重试')),
          ],
        ),
      );
}
```

## P-5 单值本地状态：ValueNotifier
```dart
final ValueNotifier<int> _counter = ValueNotifier<int>(0);

ValueListenableBuilder<int>(
  valueListenable: _counter,
  builder: (context, value, _) => Text('Count: $value'),
);
```

## P-6 重计算放 isolate
```dart
final products = await compute(_parseProducts, jsonString);

List<Product> _parseProducts(String raw) =>
    (jsonDecode(raw) as List).map((e) => Product.fromJson(e)).toList();
```

## P-7 实时事件流：Stream + 取消订阅
```dart
StreamSubscription<int>? _rssiSub;

void _listen(Stream<int> rssi) {
  _rssiSub = rssi.listen((v) => _rssi.value = v);
}

@override
void dispose() {
  _rssiSub?.cancel();
  super.dispose();
}
```

## P-8 声明式路由（go_router）
```dart
final router = GoRouter(
  routes: [
    GoRoute(path: '/', builder: (_, __) => const HomePage()),
    GoRoute(path: '/product/:id',
        builder: (_, s) => ProductPage(id: s.pathParameters['id']!)),
  ],
);
// MaterialApp.router(routerConfig: router);
```

## P-9 Widget 测试骨架（注入 fake）
```dart
testWidgets('CartPage 显示商品并响应重试', (tester) async {
  final vm = CartViewModel(FakeRepo());     // 注入 fake
  await tester.pumpWidget(MaterialApp(home: CartPage(vm: vm)));
  await vm.load();
  await tester.pump();
  expect(find.byType(ListView), findsOneWidget);
});
```

> 这些片段是"默认骨架"，实现时按需求替换名称与字段，但**结构（不可变/分层/四态/const/懒加载/可注入）不应降级**。
