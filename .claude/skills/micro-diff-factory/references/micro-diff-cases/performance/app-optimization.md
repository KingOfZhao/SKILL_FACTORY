---
# Flutter 应用性能优化

## 问题描述
Flutter 应用存在多处性能瓶颈：
1. 长列表滚动时卡顿（FPS 降至 30 以下）
2. 页面切换时内存未释放导致 OOM
3. 图片加载缓慢且重复下载
4. 复杂 Widget 重建频繁导致性能损耗
5. 网络请求未缓存导致重复加载

## 变量分析

### 性能相关变量
- `build_frequency` (Float): Widget 构建频率（次/秒）
- `memory_leak_rate` (Float): 内存泄漏率（MB/分钟）
- `cache_hit_rate` (Float): 缓存命中率（0-1）
- `image_load_time` (Int): 图片加载时间（毫秒）
- `widget_rebuild_count` (Int): Widget 重建次数

### 优化目标
- 最大化列表滚动流畅度（FPS ≥ 55）
- 最小化内存占用（避免 OOM）
- 最大化缓存命中率（> 80%）
- 最小化 Widget 重建次数
- 提升应用启动速度（< 2 秒）

## 微分拆解方案

### 变量定义

#### 1. 列表渲染复杂度
```
变量 list_rendering_complexity: Float = 0.0

计算公式：
list_rendering_complexity = (
  w1 * normalized(item_count, 0, 10000) +
  w2 * normalized(item_complexity, 0, 10) +
  w3 * normalized(animating_items, 0, 100)
)

其中：
- item_count = 列表项总数
- item_complexity = 每项的复杂度（子 Widget 数量）
- animating_items = 同时动画的项数
```

#### 2. 内存健康分数
```
变量 memory_health_score: Float = 0.0

计算公式：
memory_health_score = (
  w1 * (1 - memory_leak_rate / max_leak_rate) +
  w2 * cache_efficiency +
  w3 * resource_cleanup_score
)

其中：
- cache_efficiency = cache_hit_rate
- resource_cleanup_score = 已清理资源 / 总资源
```

#### 3. Widget 优化分数
```
变量 widget_optimization_score: Float = 0.0

计算公式：
widget_optimization_score = (
  w1 * const_ratio +
  w2 * memoized_ratio +
  w3 * (1 - unnecessary_rebuild_ratio)
)

其中：
- const_ratio = 使用 const 的 Widget 比例
- memoized_ratio = 使用 memoized 的 Widget 比例
- unnecessary_rebuild_ratio = 不必要重建的比例
```

---

## 求解策略

### 策略一：列表懒加载与虚拟化
```
list_strategy: LAZY_LOADING + VIRTUALIZATION

实现：
1. 使用 ListView.builder 而非 ListView
2. 实现自定义的 itemExtent 或 prototypeItem
3. 使用 AutomaticKeepAliveClientMixin 保持状态
4. 实现分页加载（每页 20-50 项）
5. 预加载机制：滚动到底部前加载下一页

优化目标：只渲染可见项，减少内存和渲染开销
```

代码示例：
```dart
class OptimizedDeviceList extends StatefulWidget {
  final List<Device> devices;

  const OptimizedDeviceList({
    super.key,
    required this.devices,
  });

  @override
  State<OptimizedDeviceList> createState() => _OptimizedDeviceListState();
}

class _OptimizedDeviceListState extends State<OptimizedDeviceList> {
  final ScrollController _scrollController = ScrollController();
  final int _pageSize = 20;
  int _currentPage = 1;

  List<Device> get _visibleDevices {
    final endIndex = (_currentPage * _pageSize).clamp(0, widget.devices.length);
    return widget.devices.sublist(0, endIndex);
  }

  @override
  void initState() {
    super.initState();
    _scrollController.addListener(_onScroll);
  }

  void _onScroll() {
    if (_scrollController.position.pixels >=
        _scrollController.position.maxScrollExtent - 200) {
      // 滚动接近底部，加载更多
      _loadMore();
    }
  }

  void _loadMore() {
    if (_currentPage * _pageSize >= widget.devices.length) {
      return; // 已加载全部
    }

    setState(() {
      _currentPage++;
    });
  }

  @override
  Widget build(BuildContext context) {
    return ListView.builder(
      controller: _scrollController,
      // 优化：指定 itemExtent 避免计算高度
      itemExtent: 80,
      // 优化：预加载范围
      cacheExtent: 500,
      itemCount: widget.devices.length,
      itemBuilder: (context, index) {
        // 使用 key 帮助复用
        return DeviceListItem(
          key: ValueKey(widget.devices[index].id),
          device: widget.devices[index],
        );
      },
    );
  }

  @override
  void dispose() {
    _scrollController.dispose();
    super.dispose();
  }
}

// 优化：使用 AutomaticKeepAliveClientMixin 保持状态
class DeviceListItem extends StatefulWidget {
  final Device device;

  const DeviceListItem({
    super.key,
    required this.device,
  });

  @override
  State<DeviceListItem> createState() => _DeviceListItemState();
}

class _DeviceListItemState extends State<DeviceListItem>
    with AutomaticKeepAliveClientMixin {
  @override
  bool get wantKeepAlive => true;

  @override
  Widget build(BuildContext context) {
    super.build(context); // 必须调用

    return ListTile(
      leading: const CircleAvatar(child: Icon(Icons.bluetooth)),
      title: Text(widget.device.name ?? '未知设备'),
      subtitle: Text(widget.device.id),
      trailing: Text('${widget.device.rssi} dBm'),
    );
  }
}
```

### 策略二：缓存策略（图片、网络请求）
```
cache_strategy: MULTI_LEVEL_CACHE

实现：
1. 图片缓存：
   - 使用 cached_network_image 包
   - 配置缓存大小（100MB）
   - 配置缓存时长（7 天）
   - 实现内存缓存 + 磁盘缓存两级缓存

2. 网络请求缓存：
   - 使用 HTTP 缓存头
   - 实现本地缓存（SharedPreferences 或 SQLite）
   - 缓存 TTL：5-30 分钟
   - ETag/Last-Modified 支持

3. 对象缓存：
   - 使用 Riverpod .cache() 装饰器
   - 缓存计算结果
   - 设置缓存过期时间

优化目标：减少重复请求，提升加载速度
```

代码示例：
```dart
// 1. 图片缓存配置
import 'package:cached_network_image/cached_network_image.dart';

class CachedImageWidget extends StatelessWidget {
  final String imageUrl;
  final double? width;
  final double? height;

  const CachedImageWidget({
    super.key,
    required this.imageUrl,
    this.width,
    this.height,
  });

  @override
  Widget build(BuildContext context) {
    return CachedNetworkImage(
      imageUrl: imageUrl,
      width: width,
      height: height,
      // 内存缓存配置
      memCacheWidth: width?.toInt(),
      memCacheHeight: height?.toInt(),
      // 占位符
      placeholder: (context, url) => const CircularProgressIndicator(),
      // 错误处理
      errorWidget: (context, url, error) => const Icon(Icons.error),
      // 图片缓存配置
      maxWidthDiskCache: 1000,
      maxHeightDiskCache: 1000,
    );
  }
}

// 2. 网络请求缓存
import 'package:dio/adapter.dart';
import 'package:dio/browser_imp.dart';
import 'package:dio/io.dart';

class CachedHttpClient {
  static final Dio _dio = Dio(BaseOptions(
    connectTimeout: const Duration(seconds: 10),
    receiveTimeout: const Duration(seconds: 10),
  ));

  static void setupCache() {
    _dio.interceptors.add(
      DioCacheManager(
        CacheConfig(
          baseUrl: 'https://api.example.com',
          defaultMaxAge: const Duration(minutes: 30),
          defaultMaxStale: const Duration(days: 7),
        ),
      ).interceptor,
    );
  }

  static Future<T> get<T>(String path, {Map<String, dynamic>? queryParameters}) async {
    final response = await _dio.get<T>(
      path,
      queryParameters: queryParameters,
      options: Options(
        extra: {
          // 启用缓存
          'dio_cache_policy': CachePolicy.request,
        },
      ),
    );
    return response.data!;
  }
}

// 3. Riverpod 缓存提供者
import 'package:riverpod_annotation/riverpod_annotation.dart';

part 'cache_provider.g.dart';

@riverpod
Future<List<Device>> cachedDevices(CachedDevicesRef ref) async {
  // Riverpod 自动缓存结果
  // 设置缓存时间为 5 分钟
  final devices = await DeviceRepository.fetchDevices();
  return devices;
}

// 使用 @riverpodKeepAlive 保持缓存
@Riverpod(keepAlive: true)
List<Device> staticDevices(StaticDevicesRef ref) {
  return [
    Device(id: '1', name: '设备 1'),
    Device(id: '2', name: '设备 2'),
  ];
}
```

### 策略三：Widget 优化（const、memoized、repaint boundary）
```
widget_strategy: MINIMIZE_REBUILD

实现：
1. 使用 const 构造函数（尽可能多）
2. 使用 RepaintBoundary 隔离重绘区域
3. 使用 ValueKey 帮助 Widget 复用
4. 使用 shouldRebuild 控制 Provider 重建
5. 避免在 build 方法中创建新对象

优化目标：减少不必要的 Widget 重建
```

代码示例：
```dart
// 1. 使用 const 构造函数
class OptimizedCard extends StatelessWidget {
  final String title;
  final String subtitle;

  const OptimizedCard({
    super.key,
    required this.title,
    required this.subtitle,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      // 使用 const 的子组件
      child: Padding(
        padding: const EdgeInsets.all(16), // const
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              title,
              style: const TextStyle( // const
                fontSize: 16,
                fontWeight: FontWeight.bold,
              ),
            ),
            const SizedBox(height: 8), // const
            Text(subtitle),
          ],
        ),
      ),
    );
  }
}

// 2. 使用 RepaintBoundary 隔离重绘
class AnimatedWidgetWrapper extends StatelessWidget {
  final Widget child;
  final bool isAnimating;

  const AnimatedWidgetWrapper({
    super.key,
    required this.child,
    required this.isAnimating,
  });

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        // 静态部分不会重绘
        const Text('静态标题'),

        // 使用 RepaintBoundary 隔离动画部分
        RepaintBoundary(
          child: AnimatedContainer(
            duration: const Duration(milliseconds: 300),
            color: isAnimating ? Colors.blue : Colors.grey,
            child: child,
          ),
        ),

        // 静态部分不会重绘
        const Text('静态底部'),
      ],
    );
  }
}

// 3. 使用 shouldRebuild 控制 Provider 重建
@riverpod
class DeviceFilter extends _$DeviceFilter {
  @override
  DeviceFilter build() {
    return const DeviceFilter(
      searchQuery: '',
      showConnectedOnly: false,
    );
  }

  void updateSearchQuery(String query) {
    // 只有当 query 实际改变时才重建
    if (state.searchQuery != query) {
      state = state.copyWith(searchQuery: query);
    }
  }
}

// 4. 避免在 build 中创建新对象
class BadExample extends StatelessWidget {
  final String title;

  const BadExample({super.key, required this.title});

  @override
  Widget build(BuildContext context) {
    // ❌ 每次构建都创建新对象
    final list = ['item1', 'item2', 'item3'];

    return ListView.builder(
      itemBuilder: (context, index) {
        // ❌ 每次构建都创建新 TextStyle
        final style = TextStyle(fontSize: 16);
        return Text(list[index], style: style);
      },
    );
  }
}

class GoodExample extends StatelessWidget {
  final String title;

  const GoodExample({super.key, required this.title});

  // ✅ 提取为静态常量
  static const _list = ['item1', 'item2', 'item3'];
  static const _textStyle = TextStyle(fontSize: 16);

  @override
  Widget build(BuildContext context) {
    return ListView.builder(
      itemBuilder: (context, index) {
        // ✅ 使用静态常量
        return Text(_list[index], style: _textStyle);
      },
    );
  }
}
```

### 策略四：资源清理与内存管理
```
memory_strategy: PROACTIVE_CLEANUP

实现：
1. 实现 dispose 方法清理资源
2. 取消未完成的 Future 和 Stream 订阅
3. 清理未使用的对象引用
4. 使用 WeakReference 避免强引用
5. 实现内存监控和告警

优化目标：及时释放资源，避免内存泄漏
```

代码示例：
```dart
import 'dart:async';

class ResourceManager extends StatefulWidget {
  const ResourceManager({super.key});

  @override
  State<ResourceManager> createState() => _ResourceManagerState();
}

class _ResourceManagerState extends State<ResourceManager> {
  // 订阅列表
  final List<StreamSubscription> _subscriptions = [];

  // Timer 列表
  final List<Timer> _timers = [];

  // 控制器列表
  final List<StreamController> _controllers = [];

  // Future 列表
  final List<Future> _pendingFutures = [];

  @override
  void initState() {
    super.initState();
    _setupResources();
  }

  void _setupResources() {
    // 1. 设置 Stream 订阅
    final deviceStream = DeviceRepository.deviceStream();
    final subscription = deviceStream.listen((device) {
      // 处理设备更新
    });
    _subscriptions.add(subscription);

    // 2. 设置 Timer
    final timer = Timer.periodic(const Duration(seconds: 5), (timer) {
      // 定期更新
    });
    _timers.add(timer);

    // 3. 设置 StreamController
    final controller = StreamController<String>();
    _controllers.add(controller);

    // 4. 设置 Future
    final future = _loadData();
    _pendingFutures.add(future);
  }

  Future<void> _loadData() async {
    try {
      // 加载数据
    } catch (e) {
      // 处理错误
    }
  }

  @override
  Widget build(BuildContext context) {
    return const Center(child: Text('资源管理示例'));
  }

  @override
  void dispose() {
    print('[资源管理] 开始清理资源...');

    // 1. 取消所有 Stream 订阅
    for (final subscription in _subscriptions) {
      subscription.cancel();
    }
    _subscriptions.clear();

    // 2. 取消所有 Timer
    for (final timer in _timers) {
      timer.cancel();
    }
    _timers.clear();

    // 3. 关闭所有 StreamController
    for (final controller in _controllers) {
      controller.close();
    }
    _controllers.clear();

    // 4. 取消未完成的 Future（如果需要）
    // 注意：Future 本身无法取消，但可以设置标志位
    _pendingFutures.clear();

    print('[资源管理] 资源清理完成');

    super.dispose();
  }
}

// 内存监控工具
class MemoryMonitor {
  static const int warningThreshold = 100; // MB
  static const int criticalThreshold = 150; // MB

  Timer? _monitorTimer;

  void startMonitoring({Duration interval = const Duration(seconds: 10)}) {
    _monitorTimer = Timer.periodic(interval, (_) {
      _checkMemory();
    });
  }

  void _checkMemory() {
    // 注意：在真实设备上使用 platform channels 获取内存
    // 这里仅作示例
    final memoryUsage = _getMemoryUsage(); // 实现获取内存的函数

    if (memoryUsage > criticalThreshold) {
      print('[内存监控] ⚠️ 严重: $memoryUsage MB');
      // 触发紧急清理
      _emergencyCleanup();
    } else if (memoryUsage > warningThreshold) {
      print('[内存监控] ⚠️ 警告: $memoryUsage MB');
      // 触发常规清理
      _regularCleanup();
    }
  }

  double _getMemoryUsage() {
    // 实现获取内存使用量的函数
    // 返回 MB
    return 0.0;
  }

  void _emergencyCleanup() {
    // 清理缓存
    DefaultCacheManager().emptyCache();

    // 触发 GC
    // Flutter 会自动管理 GC，这里仅作示例
  }

  void _regularCleanup() {
    // 常规清理
    DefaultCacheManager().pruneCache();
  }

  void stopMonitoring() {
    _monitorTimer?.cancel();
    _monitorTimer = null;
  }
}

// 使用 WeakReference 避免强引用
import 'dart:collection';

class WeakCache<K, V extends Object> {
  final Map<K, WeakReference<V>> _cache = {};

  void put(K key, V value) {
    _cache[key] = WeakReference(value);
  }

  V? get(K key) {
    final ref = _cache[key];
    return ref?.target;
  }

  void clear() {
    _cache.clear();
  }
}
```

---

## 约束条件

### 1. 硬约束
- 最小 FPS：30（最低可接受）
- 最大内存占用：300MB（避免 OOM）
- 最大缓存大小：200MB（磁盘）
- 最大网络请求并发：5 个

### 2. 潜约束
- 目标 FPS：50-60
- 目标缓存命中率：> 80%
- 目标图片加载时间：< 500ms
- 目标应用启动时间：< 2 秒

### 3. 业务约束
- 列表必须支持至少 10000 项
- 必须保留最近的操作历史
- 必须支持离线访问缓存数据

---

## 微分变量分析

### 性能关键变量

#### 1. `fps_score` (帧率分数)
- **公式**: `current_fps / target_fps`
- **取值范围**: 0-1.0
- **影响**: 高分数表示流畅，低分数表示卡顿

#### 2. `memory_score` (内存分数)
- **公式**: `1.0 - (current_memory / max_memory)`
- **取值范围**: 0-1.0
- **影响**: 高分数表示内存使用良好

#### 3. `cache_efficiency_score` (缓存效率分数)
- **公式**: `cache_hit_count / cache_request_count`
- **取值范围**: 0-1.0
- **影响**: 高分数表示缓存有效

#### 4. `overall_performance_score` (总体性能分数)
- **公式**:
```dart
double calculateOverallPerformance({
  required double fpsScore,
  required double memoryScore,
  required double cacheEfficiencyScore,
  required double startupSpeedScore,
}) {
  return (fpsScore * 0.35 +
          memoryScore * 0.25 +
          cacheEfficiencyScore * 0.25 +
          startupSpeedScore * 0.15);
}
```

---

## 优化建议

### 短期优化（1-2 周）

1. **实现列表懒加载**
   - 使用 ListView.builder
   - 实现分页加载
   - 添加预加载机制

2. **添加图片缓存**
   - 集成 cached_network_image
   - 配置缓存策略
   - 实现占位符和错误处理

3. **Widget 优化**
   - 添加 const 构造函数
   - 使用 RepaintBoundary
   - 避免在 build 中创建对象

### 中期优化（3-4 周）

1. **网络请求缓存**
   - 实现 HTTP 缓存头支持
   - 添加本地缓存层
   - 配置缓存 TTL

2. **资源清理机制**
   - 实现完整的 dispose
   - 取消所有订阅和 Timer
   - 添加内存监控

3. **性能监控工具**
   - FPS 监控
   - 内存监控
   - 性能分析报告

### 长期优化（3-6 月）

1. **预加载策略**
   - 预加载常用页面
   - 预加载图片资源
   - 智能预测用户行为

2. **性能优化自动化**
   - 自动检测性能问题
   - 自动应用优化策略
   - 性能回归测试

---

## 代码集成示例

### 完整的性能优化页面

```dart
import 'package:flutter/material.dart';
import 'package:riverpod_annotation/riverpod_annotation.dart';

part 'performance_optimized_page.g.dart';

// 优化的设备列表提供者
@riverpod
Future<List<Device>> optimizedDeviceList(OptimizedDeviceListRef ref) async {
  // 使用缓存避免重复请求
  final devices = await DeviceRepository.fetchDevices();

  // 排序（在后台线程）
  devices.sort((a, b) => (b.rssi ?? -100).compareTo(a.rssi ?? -100));

  return devices;
}

class PerformanceOptimizedPage extends StatefulWidget {
  const PerformanceOptimizedPage({super.key});

  @override
  State<PerformanceOptimizedPage> createState() =>
      _PerformanceOptimizedPageState();
}

class _PerformanceOptimizedPageState extends State<PerformanceOptimizedPage> {
  final MemoryMonitor _memoryMonitor = MemoryMonitor();
  final ScrollController _scrollController = ScrollController();

  @override
  void initState() {
    super.initState();
    _memoryMonitor.startMonitoring();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('性能优化示例'),
        actions: [
          IconButton(
            icon: const Icon(Icons.speed),
            onPressed: () => _showPerformanceMetrics(context),
          ),
        ],
      ),
      body: _buildDeviceList(),
    );
  }

  Widget _buildDeviceList() {
    return Consumer(
      builder: (context, ref, child) {
        final devicesAsync = ref.watch(optimizedDeviceListProvider);

        return devicesAsync.when(
          data: (devices) => OptimizedDeviceList(
            devices: devices,
            scrollController: _scrollController,
          ),
          loading: () => const Center(child: CircularProgressIndicator()),
          error: (error, stack) => Center(child: Text('错误: $error')),
        );
      },
    );
  }

  void _showPerformanceMetrics(BuildContext context) {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('性能指标'),
        content: const PerformanceMetricsWidget(),
      ),
    );
  }

  @override
  void dispose() {
    _scrollController.dispose();
    _memoryMonitor.stopMonitoring();
    super.dispose();
  }
}

class PerformanceMetricsWidget extends StatefulWidget {
  const PerformanceMetricsWidget({super.key});

  @override
  State<PerformanceMetricsWidget> createState() =>
      _PerformanceMetricsWidgetState();
}

class _PerformanceMetricsWidgetState extends State<PerformanceMetricsWidget> {
  double _fps = 60;
  double _memory = 0;
  int _cacheHits = 0;
  int _cacheMisses = 0;

  Timer? _updateTimer;

  @override
  void initState() {
    super.initState();
    _startMetricsUpdate();
  }

  void _startMetricsUpdate() {
    _updateTimer = Timer.periodic(const Duration(seconds: 1), (_) {
      setState(() {
        _fps = _calculateFps();
        _memory = _calculateMemory();
      });
    });
  }

  double _calculateFps() {
    // 实现 FPS 计算
    return 60;
  }

  double _calculateMemory() {
    // 实现内存计算
    return 50;
  }

  @override
  Widget build(BuildContext context) {
    final cacheHitRate = _cacheHits / (_cacheHits + _cacheMisses);

    return Column(
      mainAxisSize: MainAxisSize.min,
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        _MetricRow(label: 'FPS', value: '$_fps'),
        _MetricRow(label: '内存', value: '${_memory.toStringAsFixed(1)} MB'),
        _MetricRow(label: '缓存命中率', value: '${(cacheHitRate * 100).toStringAsFixed(0)}%'),
        _MetricRow(label: '缓存命中', value: '$_cacheHits'),
        _MetricRow(label: '缓存未命中', value: '$_cacheMisses'),
      ],
    );
  }

  @override
  void dispose() {
    _updateTimer?.cancel();
    super.dispose();
  }
}

class _MetricRow extends StatelessWidget {
  final String label;
  final String value;

  const _MetricRow({required this.label, required this.value});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 4),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Text(label, style: const TextStyle(fontWeight: FontWeight.bold)),
          Text(value),
        ],
      ),
    );
  }
}
```

---

## 预期效果

### 量化指标
- **平均 FPS**: 从 30 → 目标 55+
- **内存占用**: 从 200MB → 目标 < 100MB
- **缓存命中率**: 从 20% → 目标 > 80%
- **列表滚动流畅度**: 卡顿率从 40% → 目标 < 5%
- **应用启动时间**: 从 5 秒 → 目标 < 2 秒

### 用户体验提升
- **滚动流畅度提升 83%**: 卡顿明显减少
- **内存占用降低 50%**: 避免 OOM
- **加载速度提升 4倍**: 缓存命中率高
- **启动速度提升 2.5倍**: 应用快速启动

---

## 总结

### 核心创新
1. **多层优化策略**: 列表、缓存、Widget、内存全面优化
2. **动态自适应**: 根据设备性能和用户行为调整策略
3. **实时监控**: FPS、内存、缓存命中率可视化
4. **渐进式优化**: 短期、中期、长期分阶段实施

### 与元-skill-穷举器的协作
- **问题分类**: 性能优化问题 → 自动识别
- **最佳实践积累**: 成功案例存入参考文件夹
- **模式识别**: 识别为"性能优化"（CODE_PERFORMANCE 类型）
- **生成器输出**: 生成包含上述优化的 Flutter 代码

### 可扩展性
- **新问题领域**: 动画、网络、数据库
- **新策略类型**: 压缩、加密、负载均衡
- **新约束类型**: 网络类型、电池电量、存储空间

---

**案例类型**: `CODE_PERFORMANCE`
**子领域**: 列表渲染、缓存、内存管理、Widget 优化
**关键词**: performance, lazy loading, cache, memory, widget optimization, repaint boundary, dispose

---

**下一步**
1. 实现更多求解策略（模拟退火、粒子群优化）
2. 创建可视化工具（变量关系图、优化轨迹图）
3. 实现基本求解器（梯度下降、线性规划）
4. 添加自动优化建议生成器
5. 建立案例质量评分机制
6. 优化元-skill-orchestrator 调用顺序

---

**维护者**: Claude Code Skill Factory Team
**版本**: 1.0.0
