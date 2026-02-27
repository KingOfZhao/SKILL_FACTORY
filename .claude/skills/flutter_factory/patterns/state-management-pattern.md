# 状态管理模式

## 支持的状态管理库

### 1. Riverpod（推荐）
- **优势**: 类型安全、编译时检查、易于测试
- **适用场景**: 中大型应用、复杂状态管理

### 2. BLoC
- **优势**: 事件驱动、状态可追溯、适合团队协作
- **适用场景**: 大型应用、需要状态历史

### 3. Provider
- **优势**: 简单轻量、学习曲线平缓
- **适用场景**: 小型应用、简单状态

## Riverpod 模式

### Provider 类型
```dart
// 只读 Provider
final configProvider = Provider<AppConfig>((ref) {
  return AppConfig();
});

// StateProvider（简单状态）
final counterProvider = StateProvider<int>((ref) {
  return 0;
});

// StateNotifierProvider（复杂状态）
final devicesProvider = StateNotifierProvider<DeviceNotifier, List<Device>>((ref) {
  return DeviceNotifier(ref.watch(bluetoothServiceProvider));
});

// FutureProvider（异步数据）
final userProfileProvider = FutureProvider<UserProfile>((ref) async {
  return ref.read(apiService).getProfile();
});

// StreamProvider（流数据）
final rssiStreamProvider = StreamProvider<int>((ref) {
  return ref.read(bluetoothService).rssiStream;
});
```

## BLoC 模式

### 核心组件
```dart
// Events
abstract class BluetoothEvent {}
class ScanStarted extends BluetoothEvent {}
class DeviceFound extends BluetoothEvent {}

// States
abstract class BluetoothState {}
class BluetoothInitial extends BluetoothState {}
class BluetoothScanning extends BluetoothState {}

// BLoC
class BluetoothBloc extends Bloc<BluetoothEvent, BluetoothState> {
  final BluetoothService service;

  BluetoothBloc(this.service) : super(BluetoothInitial()) {
    on<ScanStarted>(_onScanStarted);
    on<DeviceFound>(_onDeviceFound);
  }
}
```

## MVVM 模式

### 架构层次
```
┌─────────────────┐
│   View Layer    │  ← Widgets
├─────────────────┤
│  ViewModel      │  ← ChangeNotifier / BLoC
├─────────────────┤
│   Model Layer   │  ← Data Models
└─────────────────┘
```

### 视图模型
```dart
class DeviceListViewModel extends ChangeNotifier {
  final BluetoothService _service;
  List<BluetoothDevice> _devices = [];

  DeviceListViewModel(this._service) {
    _service.deviceStream.listen((devices) {
      _devices = devices;
      notifyListeners();
    });
  }

  List<BluetoothDevice> get devices => _devices;
}
```

## Clean Architecture 模式

### 分层结构
```
lib/
├── domain/          # 领域层（纯 Dart，无 Flutter 依赖）
│   ├── entities/    # 业务实体
│   └── usecases/   # 用例
├── data/            # 数据层
│   ├── models/      # 数据模型
│   ├── repositories/# 仓库实现
│   └── services/    # 外部服务
└── presentation/    # 表现层
    ├── pages/       # 页面
    ├── widgets/    # 组件
    └── providers/  # 状态管理
```

## 状态选择指南

| 场景 | 推荐方案 | 原因 |
|-----|---------|------|
| 简单计数器 | Provider | 轻量级 |
| 表单状态 | StateProvider | 简单状态 |
| 设备列表 | Riverpod StateNotifier | 复杂状态管理 |
| 登录流程 | BLoC | 事件驱动 |
| 全局配置 | Provider | 全局只读 |
| 实时数据 | StreamProvider | 流数据处理 |

## PDF 需求覆盖

| 需求点 | Riverpod 实现 |
|--------|-------------|
| 设备列表 | StateNotifierProvider<List<Device>> |
| RSSI 数据 | StreamProvider<int> |
| 连接状态 | StateProvider<ConnectionState> |
| 日志流 | StreamProvider<LogEntry> |
