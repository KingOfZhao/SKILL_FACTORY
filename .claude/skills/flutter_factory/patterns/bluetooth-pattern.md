# 蓝牙通信通用模式

## 模式描述
提供 Flutter 蓝牙（BLE/Classic）通信的完整实现模式，基于 flutter_blue_plus 库。

## 核心组件

### 1. 蓝牙服务 (BluetoothService)
- **职责**: 扫描、连接、断开、数据收发
- **依赖**: flutter_blue_plus

### 2. RSSI 监听器 (RssiListener)
- **职责**: 实时监听设备信号强度
- **特性**: 10秒滚动窗口、dBm 单位

### 3. 设备管理器 (DeviceManager)
- **职责**: 维护已发现设备列表
- **数据结构**: 名称/MAC地址/RSSI/连接状态

## 状态管理（Riverpod）

### Providers
```dart
// 设备列表 Provider
final devicesProvider = StateNotifierProvider<DeviceNotifier, List<BluetoothDevice>>((ref) {
  return DeviceNotifier();
});

// 连接状态 Provider
final connectionStateProvider = StateProvider<ConnectionState>((ref) {
  return ConnectionState.disconnected;
});

// RSSI 数据 Provider
final rssiDataProvider = StateProvider<List<RssiPoint>>((ref) {
  return [];
});
```

## 异常处理

### 常见异常
- 设备未授权（权限被拒绝）
- 蓝牙未启用
- 连接超时
- 特征值读取失败

### 重试机制
- 指数退避重试
- 最大重试次数：3次
- 重试间隔：1s, 2s, 4s

## 目录结构
```
lib/
├── data/
│   ├── models/
│   │   ├── bluetooth_device.dart
│   │   └── rssi_point.dart
│   ├── repositories/
│   │   └── bluetooth_repository.dart
│   └── services/
│       └── bluetooth_service.dart
└── presentation/
    ├── providers/
    │   └── bluetooth_providers.dart
    └── widgets/
        └── device_list_widget.dart
```

## API 接口

### BluetoothService
```dart
class BluetoothService {
  Future<void> startScan();
  Future<void> stopScan();
  Future<void> connect(BluetoothDevice device);
  Future<void> disconnect();
  Stream<int> getRssi(BluetoothDevice device);
}
```

## PDF 需求覆盖

| 需求点 | 实现 |
|--------|------|
| 蓝牙扫描 | startScan() + 设备列表流 |
| 无手动配对 | 自动连接逻辑 |
| RSSI 实时曲线 | RssiListener + 10秒窗口 |
| 异常处理 | 异常捕获 + 重试机制 |
| 真实设备连接 | flutter_blue_plus 原生集成 |
