# 测试用例

**迭代ID**: flutter-factory-iteration-002
**生成时间**: 2026-02-27T20:00:00Z

---

## 单元测试用例建议

### 测试组 1: Bluetooth Service 测试

```dart
import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_blue_plus/flutter_blue_plus.dart';
import '../lib/data/services/bluetooth_service.dart';
import '../lib/core/utils/log_service.dart';

void main() {
  group('BluetoothService', () {
    late BluetoothService service;

    setUp(() {
      service = BluetoothService();
    });

    test('should start scanning', () async {
      // Arrange
      final scanStarted = false;

      service.scanStateStream.listen((isScanning) {
        if (isScanning) scanStarted = true;
      });

      // Act
      await service.startScan();

      // Assert
      expect(scanStarted, true);
    });

    test('should stop scanning', () async {
      // Arrange
      await service.startScan();
      await Future.delayed(const Duration(milliseconds: 100));

      // Act
      await service.stopScan();

      // Assert
      expect(service.isScanning, false);
    });

    test('should handle connection retry with exponential backoff', () async {
      // Arrange
      final delays = <Duration>[];
      // Mock connection failures...

      // Act
      await service.connectWithRetry(mockDevice);

      // Assert
      expect(delays.length, greaterThanOrEqualTo(1));
      // Verify delays increase: 1s, 2s, 4s
    });

    test('should emit RSSI stream', () async {
      // Arrange
      final rssiValues = <int>[];

      service.getRssi(mockDevice).listen((rssi) {
        rssiValues.add(rssi);
      });

      // Act
      // Simulate RSSI updates...

      // Assert
      expect(rssiValues, isNotEmpty);
    });
  });
}
```

### 测试组 2: Device Notifier 测试

```dart
import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../lib/presentation/providers/device_provider.dart';
import '../lib/domain/entities/device.dart';

void main() {
  group('DeviceNotifier', () {
    late DeviceNotifier notifier;

    setUp(() {
      notifier = DeviceNotifier(BluetoothService());
    });

    test('should update device list on scan results', () {
      // Act
      notifier.state = notifier.state.copyWith(
        devices: [mockDevice1, mockDevice2],
      );

      // Assert
      expect(notifier.state.devices.length, equals(2));
    });

    test('should trim RSSI data to 10 second window', () async {
      // Arrange
      final baseTime = DateTime.now();
      final dataPoints = List.generate(
        20,
        (i) => RssiPoint(
          timestamp: baseTime.add(Duration(seconds: i)),
          rssi: -70 - i,
        ),
      );

      // Act
      notifier.state = notifier.state.copyWith(rssiData: dataPoints);

      // Assert
      expect(notifier.state.rssiData.length, lessThanOrEqualTo(10));
    });

    test('should update connection status', () {
      // Act
      notifier.state = notifier.state.copyWith(
        connectedDevice: mockDevice1,
      );

      // Assert
      expect(notifier.state.connectedDevice, isNotNull);
      expect(notifier.state.connectedDevice!.isConnected, true);
    });
  });
}
```

### 测试组 3: Log Service 测试

```dart
import 'package:flutter_test/flutter_test.dart';
import '../lib/core/utils/log_service.dart';

void main() {
  group('LogService', () {
    late LogService logService;

    setUp(() {
      logService = LogService();
    });

    test('should add log entry', () {
      // Act
      logService.info('Test message');

      // Assert
      expect(logService.logs.length, equals(1));
      expect(logService.logs.last.message, equals('Test message'));
      expect(logService.logs.last.level, equals(LogLevel.info));
    });

    test('should trim to max size', () {
      // Act
      for (int i = 0; i < 1100; i++) {
        logService.debug('Log $i');
      }

      // Assert
      expect(logService.logs.length, lessThanOrEqualTo(1000));
    });

    test('should notify listeners', () {
      // Arrange
      LogEntry? capturedEntry;

      logService.addListener((entry) {
        capturedEntry = entry;
      });

      // Act
      logService.warning('Warning message');

      // Assert
      expect(capturedEntry, isNotNull);
      expect(capturedEntry!.level, equals(LogLevel.warning));
    });
  });
}
```

---

## Widget 测试用例建议

### 测试组 1: Device Card Widget 测试

```dart
import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../lib/presentation/widgets/device_card.dart';
import '../lib/domain/entities/device.dart';
import '../lib/core/theme/app_theme.dart';

void main() {
  testWidgets('DeviceCard displays device info', (WidgetTester tester) async {
    // Arrange
    final device = Device(
      id: '00:11:22:33:44:55',
      name: 'Test Device',
      rssi: -70,
    );

    // Act
    await tester.pumpWidget(
      ProviderScope(
        child: MaterialApp(
          home: Scaffold(
            body: DeviceCard(
              device: device,
              onTap: () {},
            ),
          ),
        ),
      ),
    );

    // Assert
    expect(find.text('Test Device'), findsOneWidget);
    expect(find.text('00:11:22:33:44:55'), findsOneWidget);
    expect(find.text('-70 dBm'), findsOneWidget);
  });

  testWidgets('DeviceCard color changes with RSSI', (WidgetTester tester) async {
    // Arrange
    final strongSignal = Device(id: '1', name: 'Strong', rssi: -60);
    final weakSignal = Device(id: '2', name: 'Weak', rssi: -85);

    // Act - Test strong signal
    await tester.pumpWidget(
      ProviderScope(
        child: MaterialApp(
          home: Scaffold(
            body: DeviceCard(device: strongSignal, onTap: () {}),
          ),
        ),
      ),
    );

    Text strongRssiText = tester.widget<Text>(find.text('-60 dBm'));
    expect(strongRssiText.style?.color, equals(Colors.green));

    // Act - Test weak signal
    await tester.pumpWidget(
      ProviderScope(
        child: MaterialApp(
          home: Scaffold(
            body: DeviceCard(device: weakSignal, onTap: () {}),
          ),
        ),
      ),
    );

    Text weakRssiText = tester.widget<Text>(find.text('-85 dBm'));
    expect(weakRssiText.style?.color, equals(Colors.red));
  });
}
```

### 测试组 2: RSSI Chart Widget 测试

```dart
import 'package:flutter_test/flutter_test.dart';
import '../lib/presentation/widgets/rssi_chart.dart';
import '../lib/domain/entities/rssi_point.dart';

void main() {
  testWidgets('RssiChart displays data points', (WidgetTester tester) async {
    // Arrange
    final data = [
      RssiPoint(DateTime.now().subtract(const Duration(seconds: 10)), -80),
      RssiPoint(DateTime.now().subtract(const Duration(seconds: 5)), -75),
      RssiPoint(DateTime.now(), -70),
    ];

    // Act
    await tester.pumpWidget(
      const MaterialApp(
        home: Scaffold(
          body: RssiChart(),
        ),
      ),
    );

    // Assert
    expect(find.byType(LineChart), findsOneWidget);
  });

  testWidgets('RssiChart handles empty data', (WidgetTester tester) async {
    // Act
    await tester.pumpWidget(
      const MaterialApp(
        home: Scaffold(
          body: RssiChart(),
        ),
      ),
    );

    // Assert
    expect(find.byType(LineChart), findsOneWidget);
    expect(find.text('Connect to a device to see RSSI data'), findsOneWidget);
  });
}
```

---

## 集成测试用例建议

### 测试组 1: 完整蓝牙扫描流程集成测试

```dart
void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  testWidgets('Bluetooth scan flow integration test', (WidgetTester tester) async {
    // Setup
    await tester.pumpWidget(
      const ProviderScope(
        child: MaterialApp(
          home: MainPage(),
        ),
      ),
    );

    // Test 1: Initial state
    expect(find.text('Start Scan'), findsOneWidget);
    expect(find.byType(DeviceCard), findsNothing);

    // Test 2: Start scan
    await tester.tap(find.text('Start Scan'));
    await tester.pumpAndSettle(const Duration(seconds: 1));

    expect(find.text('Scanning...'), findsOneWidget);

    // Test 3: Stop scan
    await tester.tap(find.text('Stop Scan'));
    await tester.pumpAndSettle();

    expect(find.text('Start Scan'), findsOneWidget);

    // Test 4: Switch to Logs tab
    await tester.tap(find.text('Logs'));
    await tester.pumpAndSettle();

    expect(find.byType(LogsView), findsOneWidget);

    // Test 5: Switch back to Bluetooth tab
    await tester.tap(find.text('Bluetooth'));
    await tester.pumpAndSettle();

    expect(find.byType(BluetoothTab), findsOneWidget);
  });
}
```

### 测试组 2: RSSI 图表实时更新集成测试

```dart
void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  testWidgets('RSSI chart updates in real-time', (WidgetTester tester) async {
    await tester.pumpWidget(
      const ProviderScope(
        child: MaterialApp(
          home: MainPage(),
        ),
      ),
    );

    // Initial state
    expect(find.byType(LineChart), findsOneWidget);

    // Simulate RSSI updates
    final container = ProviderContainer();
    // container.read(rssiDataProvider.notifier).updateRssi(-70);
    // await tester.pump();

    // container.read(rssiDataProvider.notifier).updateRssi(-75);
    // await tester.pump();

    // container.read(rssiDataProvider.notifier).updateRssi(-80);
    // await tester.pump();

    // Verify chart updates
    // final chartData = container.read(rssiDataProvider);
    // expect(chartData.length, greaterThan(2));
  });
}
```

---

## PDF 需求特定测试

### 测试: 无手动配对验证

```dart
testWidgets('should connect without manual pairing dialog', (WidgetTester tester) async {
  // Arrange
  final mockService = MockBluetoothService();
  final device = MockBluetoothDevice();

  when(mockService.connect(device)).thenAnswer((_) async {
    // Verify no pairing dialog is shown
    return;
  });

  await tester.pumpWidget(
    MaterialApp(
      home: BluetoothTab(service: mockService),
    ),
  );

  await tester.tap(find.byKey(const Key('device-connect')));
  await tester.pumpAndSettle();

  verify(mockService.connect(device)).called(1);
  // No pairing dialog should appear
  expect(find.byType(PairingDialog), findsNothing);
});
```

### 测试: 10秒滚动窗口验证

```dart
test('DeviceNotifier maintains 10 second window', () async {
  // Arrange
  final notifier = DeviceNotifier(BluetoothService());
  final baseTime = DateTime.now();

  // Act
  // Add 15 data points (15 seconds worth)
  for (int i = 0; i < 15; i++) {
    final point = RssiPoint(
      timestamp: baseTime.add(Duration(seconds: i)),
      rssi: -70 - i,
    );
    // notifier.state = notifier.state.copyWith(
    //   rssiData: [...notifier.state.rssiData, point],
    // );
  }

  // Assert
  // Verify data is trimmed to 10 second window
  final cutoff = DateTime.now().subtract(const Duration(seconds: 10));
  for (final point in notifier.state.rssiData) {
    expect(point.timestamp.isAfter(cutoff), true);
  }
});
```

### 测试: Tab 结构验证

```dart
testWidgets('MainPage has BottomNavigationBar with 2 tabs', (WidgetTester tester) async {
  await tester.pumpWidget(
    const ProviderScope(
      child: MaterialApp(
        home: MainPage(),
      ),
    ),
  );

  expect(find.byType(BottomNavigationBar), findsOneWidget);
  expect(find.text('Bluetooth'), findsOneWidget);
  expect(find.text('Logs'), findsOneWidget);
});

testWidgets('Bluetooth tab displays device list', (WidgetTester tester) async {
  // Mock device discovery
  // when(mockBluetoothService.devices).thenReturn([mockDevice]);

  await tester.pumpWidget(
    ProviderScope(
      child: MainPage(),
    ),
  );

  // Navigate to Bluetooth tab (index 0)
  // await tester.tap(find.text('Bluetooth'));
  // await tester.pumpAndSettle();

  expect(find.byType(BluetoothTab), findsOneWidget);
  // expect(find.byType(DeviceCard), findsWidgets);
});

testWidgets('Logs tab displays scrolling logs', (WidgetTester tester) async {
  // Setup log service with mock logs
  final logService = LogService();
  for (int i = 0; i < 10; i++) {
    logService.info('Log message $i');
  }

  await tester.pumpWidget(
    ProviderScope(
      providers: [logServiceProvider.overrideWithValue(logService)],
      child: MainPage(),
    ),
  );

  // Navigate to Logs tab (index 1)
  // await tester.tap(find.text('Logs'));
  // await tester.pumpAndSettle();

  expect(find.byType(LogsView), findsOneWidget);
  // expect(find.text('Log message 0'), findsOneWidget);
});
```

---

## 测试覆盖率目标

| 测试类型 | 覆盖率目标 | 当前 | 状态 |
|---------|-------------|------|------|
| 单元测试 | ≥ 80% | - | 待实现 |
| Widget 测试 | ≥ 70% | - | 待实现 |
| 集成测试 | ≥ 50% | - | 待实现 |
| 总体 | ≥ 70% | - | 待实现 |

---

## 测试执行命令

```bash
# 运行所有测试
flutter test

# 运行单元测试
flutter test test/unit/

# 运行 Widget 测试
flutter test test/widget/

# 运行集成测试
flutter test integration_test/

# 生成覆盖率报告
flutter test --coverage
genhtml coverage/lcov.info -o coverage/html
```

---

**文档版本**: v1.0
**更新频率**: 每次需求迭代后
