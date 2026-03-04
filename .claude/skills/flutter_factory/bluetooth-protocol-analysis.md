# 蓝牙协议支持问题 - 改进方案

**问题**: 生成的项目仅支持 BLE（低功耗蓝牙），不支持经典蓝牙
**发现时间**: 2026-02-27T20:10:00Z

---

## 问题分析

### 当前实现（仅 BLE）

```yaml
# pubspec.yaml
dependencies:
  flutter_blue_plus: ^1.31.0  # ❌ 仅支持 BLE
```

### 需求要求

用户需求明确指出：
> "Flutter App 通过蓝牙（BLE 或 Classic）与电脑端通信"

**PC 端 Mac** = 经典蓝牙设备类型

---

## 解决方案

### 方案 1: 使用 `flutter_bluetooth_serial`（推荐）

```yaml
# pubspec.yaml
dependencies:
  flutter_bluetooth_serial: ^0.4.0  # ✅ 支持经典蓝牙
```

**优点**:
- ✅ 原生支持经典蓝牙（SPP 协议）
- ✅ 可与 PC/Mac 通信
- ✅ 稳定可靠

**缺点**:
- ❌ 不支持 BLE 扫描

---

### 方案 2: 混合方案 - 同时支持 BLE 和 Classic（最佳）

```yaml
# pubspec.yaml
dependencies:
  # BLE 支持
  flutter_blue_plus: ^1.31.0

  # 经典蓝牙支持
  flutter_bluetooth_serial: ^0.4.0
```

**架构调整**:

```dart
// lib/core/constants/bluetooth_constants.dart
enum BluetoothProtocol {
  ble,
  classic,
}

// lib/data/services/bluetooth_service.dart
class BluetoothService {
  // BLE 服务
  final BleService _bleService;

  // 经典蓝牙服务
  final ClassicBluetoothService _classicService;

  // 当前协议
  BluetoothProtocol _currentProtocol = BluetoothProtocol.ble;

  Future<void> startScan({
    BluetoothProtocol protocol = BluetoothProtocol.ble,
  }) async {
    _currentProtocol = protocol;

    switch (protocol) {
      case BluetoothProtocol.ble:
        await _bleService.startScan();
        break;
      case BluetoothProtocol.classic:
        await _classicService.startScan(); // 经典蓝牙无扫描，直接连接
        break;
    }
  }
}
```

**优点**:
- ✅ **同时支持 BLE 和 Classic**
- ✅ 动态切换协议
- ✅ 满足所有需求场景

---

## 推荐实现

### 蓝牙服务层重构

```
lib/
└── data/
    └── services/
        ├── bluetooth_service.dart           # 统一蓝牙服务
        ├── ble_service.dart              # BLE 服务（flutter_blue_plus）
        └── classic_bluetooth_service.dart   # 经典蓝牙服务（flutter_bluetooth_serial）
```

### 协议选择 UI

```dart
// lib/presentation/widgets/protocol_selector.dart
class ProtocolSelector extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return SegmentedButton<BluetoothProtocol>(
      segments: {
        BluetoothProtocol.ble: SegmentedButtonSegment(
          label: 'BLE',
          icon: Icon(Icons.bluetooth),
        ),
        BluetoothProtocol.classic: SegmentedButtonSegment(
          label: 'Classic',
          icon: Icon(Icons.laptop),
        ),
      },
      selected: BluetoothProtocol.ble,
      onSelectionChanged: (protocol) {
        // 切换蓝牙协议
        context.read(deviceNotifierProvider.notifier).switchProtocol(protocol);
      },
    );
  }
}
```

---

## 需要修改的文件

| 文件 | 修改内容 |
|------|---------|
| **pubspec.yaml** | 添加 `flutter_bluetooth_serial: ^0.4.0` |
| **lib/core/constants/bluetooth_constants.dart** | 添加 `BluetoothProtocol` 枚举 |
| **lib/data/services/bluetooth_service.dart** | 重构为支持双协议 |
| **lib/data/services/ble_service.dart** | 新建 - BLE 服务封装 |
| **lib/data/services/classic_bluetooth_service.dart** | 新建 - 经典蓝牙服务封装 |
| **lib/presentation/widgets/protocol_selector.dart** | 新建 - 协议选择器 |

---

## 使用场景

### 场景 1: 连接 BLE 设备（智能设备）
```
1. 选择协议: BLE
2. 点击 Start Scan
3. 连接 BLE 设备
4. RSSI 图表显示（BLE 特有功能）
```

### 场景 2: 连接经典蓝牙设备（PC/Mac）
```
1. 选择协议: Classic
2. 输入设备 MAC 地址或从列表选择
3. 点击 Connect
4. 建立 SPP 连接
5. 开始数据传输
```

---

## 验证计划

### 1. BLE 验证
```bash
flutter test test/unit/ble_service_test.dart
```

### 2. 经典蓝牙验证
```bash
flutter test test/unit/classic_bluetooth_service_test.dart
```

### 3. 协议切换验证
```bash
flutter test test/widget/protocol_selector_test.dart
```

---

## 注意事项

1. **iOS 限制**: 经典蓝牙在 iOS 上有额外限制
2. **权限配置**: 经典蓝牙不需要位置权限，需要移除
3. **UI 调整**: 经典蓝牙不支持 RSSI，需要隐藏 RSSI 图表
4. **功能差异**:
   - BLE: 支持扫描、RSSI、连接参数
   - Classic: 直接连接、SPP 通信、无 RSSI

---

**建议优先级**: P0（高）
**预计工作量**: 1-2 小时
