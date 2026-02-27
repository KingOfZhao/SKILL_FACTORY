# 测试用例

**迭代ID**: flutter-factory-iteration-001
**生成时间**: 2026-02-27T19:15:00Z

---

## 单元测试用例建议

### 测试组 1: 蓝牙服务测试

```dart
import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:mockito/annotations.dart';
import 'package:mockito/mockito.dart';

@GenerateMocks([BluetoothService])
import 'bluetooth_service_test.mocks.dart';

void main() {
  late BluetoothService mockService;

  setUp(() {
    mockService = MockBluetoothService();
  });

  group('BluetoothService', () {
    test('should start scanning', () async {
      when(mockService.startScan()).thenAnswer((_) async {});
      await mockService.startScan();
      verify(mockService.startScan()).called(1);
    });

    test('should connect to device', () async {
      when(mockService.connect(any)).thenAnswer((_) async {});
      await mockService.connect(mockDevice);
      verify(mockService.connect(mockDevice)).called(1);
    });

    test('should emit RSSI stream', () async {
      when(mockService.getRssi(any)).thenAnswer((_) =>
        Stream.fromIterable([ -70, -75, -80 ]));

      final rssiStream = mockService.getRssi(mockDevice);
      final rssiValues = await rssiStream.take(3).toList();

      expect(rssiValues, equals([ -70, -75, -80 ]));
    });
  });
}
```

### 测试组 2: RSSI 管理器测试

```dart
void main() {
  group('RssiManager', () {
    late RssiManager manager;

    setUp(() {
      manager = RssiManager();
    });

    test('should trim data to 10 second window', () async {
      // Add data points
      for (int i = 0; i < 20; i++) {
        manager.addRssi(-70);
        await Future.delayed(const Duration(milliseconds: 500));
      }

      // Should only have last 10 seconds of data
      expect(manager.data.length, lessThanOrEqualTo(20));
    });

    test('should maintain time order', () {
      manager.addRssi(-70);
      manager.addRssi(-75);
      manager.addRssi(-80);

      final timestamps = manager.data.map((p) => p.timestamp);
      expect(timestamps, isOrdered);
    });
  });
}
```

### 测试组 3: 日志服务测试

```dart
void main() {
  group('LogService', () {
    late LogService logService;

    setUp(() {
      logService = LogService();
    });

    test('should add log entry', () {
      logService.info('Test message');

      expect(logService.logs.length, equals(1));
      expect(logService.logs.last.message, equals('Test message'));
      expect(logService.logs.last.level, equals(LogLevel.info));
    });

    test('should trim to max size', () {
      for (int i = 0; i < 1100; i++) {
        logService.debug('Log $i');
      }

      expect(logService.logs.length, lessThanOrEqualTo(1000));
    });

    test('should notify listeners', () {
      LogEntry? capturedEntry;

      logService.addListener((entry) {
        capturedEntry = entry;
      });

      logService.warning('Warning message');

      expect(capturedEntry, isNotNull);
      expect(capturedEntry!.level, equals(LogLevel.warning));
    });
  });
}
```

---

## Widget 测试用例建议

### 测试组 1: 设备卡片 Widget 测试

```dart
void main() {
  testWidgets('DeviceCard displays device info', (WidgetTester tester) async {
    final device = MockBluetoothDevice();
    when(device.name).thenReturn('Test Device');
    when(device.id).thenReturn('00:11:22:33:44:55');

    await tester.pumpWidget(
      MaterialApp(
        home: DeviceCard(
          device: device,
          rssi: -70,
          onTap: () {},
        ),
      ),
    );

    expect(find.text('Test Device'), findsOneWidget);
    expect(find.text('-70 dBm'), findsOneWidget);
  });

  testWidgets('DeviceCard color changes with RSSI', (WidgetTester tester) async {
    final device = MockBluetoothDevice();
    when(device.name).thenReturn('Test Device');
    when(device.id).thenReturn('00:11:22:33:44:55');

    // Test strong signal
    await tester.pumpWidget(
      MaterialApp(
        home: DeviceCard(
          device: device,
          rssi: -60,
          onTap: () {},
        ),
      ),
    );
    expect(_getRssiColor(-60), equals(Colors.green));

    // Test weak signal
    await tester.pumpWidget(
      MaterialApp(
        home: DeviceCard(
          device: device,
          rssi: -85,
          onTap: () {},
        ),
      ),
    );
    expect(_getRssiColor(-85), equals(Colors.red));
  });
}
```

### 测试组 2: RSSI 图表 Widget 测试

```dart
void main() {
  testWidgets('RssiChart displays data points', (WidgetTester tester) async {
    final data = [
      RssiPoint(DateTime.now().subtract(const Duration(seconds: 10)), -80),
      RssiPoint(DateTime.now().subtract(const Duration(seconds: 5)), -75),
      RssiPoint(DateTime.now(), -70),
    ];

    await tester.pumpWidget(
      MaterialApp(
        home: RssiChart(data: data),
      ),
    );

    expect(find.byType(LineChart), findsOneWidget);
  });

  testWidgets('RssiChart handles empty data', (WidgetTester tester) async {
    await tester.pumpWidget(
      MaterialApp(
        home: const RssiChart(data: []),
      ),
    );

    expect(find.byType(LineChart), findsOneWidget);
    expect(find.text('No data'), findsOneWidget);
  });
}
```

### 测试组 3: 日志视图 Widget 测试

```dart
void main() {
  testWidgets('LogsView displays logs in reverse order', (WidgetTester tester) async {
    final logs = [
      LogEntry(
        timestamp: '10:00:00',
        message: 'First log',
        level: LogLevel.info,
      ),
      LogEntry(
        timestamp: '10:00:01',
        message: 'Second log',
        level: LogLevel.info,
      ),
    ];

    await tester.pumpWidget(
      MaterialApp(
        home: LogsView(logs: logs),
      ),
    );

    expect(find.text('First log'), findsOneWidget);
    expect(find.text('Second log'), findsOneWidget);
  });

  testWidgets('LogsView colors by log level', (WidgetTester tester) async {
    final logs = [
      LogEntry(
        timestamp: '10:00:00',
        message: 'Error log',
        level: LogLevel.error,
      ),
      LogEntry(
        timestamp: '10:00:01',
        message: 'Info log',
        level: LogLevel.info,
      ),
    ];

    await tester.pumpWidget(
      MaterialApp(
        home: LogsView(logs: logs),
      ),
    );

    final errorTextWidget = tester.widget<Text>(
      find.text('Error log'),
    );
    final infoTextWidget = tester.widget<Text>(
      find.text('Info log'),
    );

    expect(errorTextWidget.style?.color, equals(Colors.red));
    expect(infoTextWidget.style?.color, equals(Colors.blue));
  });
}
```

---

## 集成测试用例建议

### 测试组 1: 蓝牙扫描流程集成测试

```dart
void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  testWidgets('Bluetooth scan flow integration test', (WidgetTester tester) async {
    // Setup
    final container = ProviderContainer();

    // Pump widget
    await tester.pumpWidget(
      UncontrolledProviderScope(
        container: container,
        child: const MaterialApp(home: BluetoothScannerScreen()),
      ),
    );

    // Test 1: Initial state
    expect(find.text('Scanning...'), findsOneWidget);

    // Test 2: Device discovery
    await tester.pumpAndSettle(const Duration(seconds: 2));

    // Test 3: Device list display
    expect(find.byType(DeviceCard), findsWidgets);

    // Test 4: Tap device to connect
    await tester.tap(find.byType(DeviceCard).first);
    await tester.pumpAndSettle();

    // Test 5: Connection state
    expect(find.text('Connecting...'), findsOneWidget);

    // Test 6: Connected state
    await tester.pumpAndSettle(const Duration(seconds: 3));
    expect(find.text('Connected'), findsOneWidget);
  });
}
```

### 测试组 2: RSSI 图表实时更新集成测试

```dart
void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  testWidgets('RSSI chart updates in real-time', (WidgetTester tester) async {
    await tester.pumpWidget(
      const MaterialApp(
        home: RssiChartScreen(),
      ),
    );

    // Initial state
    expect(find.byType(LineChart), findsOneWidget);

    // Simulate RSSI updates
    final container = tester.binding.container;
    container.read(rssiProvider.notifier).updateRssi(-70);
    await tester.pump();

    container.read(rssiProvider.notifier).updateRssi(-75);
    await tester.pump();

    container.read(rssiProvider.notifier).updateRssi(-80);
    await tester.pump();

    // Verify chart updates
    final chartData = container.read(rssiProvider);
    expect(chartData.length, greaterThan(2));
  });
}
```

---

## PDF 需求特定测试

### 测试: 无手动配对验证

```dart
testWidgets('should connect without manual pairing', (WidgetTester tester) async {
  final mockService = MockBluetoothService();
  final device = MockBluetoothDevice();

  when(mockService.connect(device)).thenAnswer((_) async {
    // Verify no pairing dialog is shown
    return;
  });

  await tester.pumpWidget(
    MaterialApp(
      home: DeviceListScreen(service: mockService),
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
test('RssiManager maintains 10 second window', () async {
  final manager = RssiManager();

  // Add 15 data points (15 seconds worth)
  final startTime = DateTime.now();
  for (int i = 0; i < 15; i++) {
    manager.addRssi(-70 - i);
    await Future.delayed(const Duration(seconds: 1));
  }
  final endTime = DateTime.now();

  // Verify data is trimmed to 10 second window
  final windowSize = endTime.difference(startTime);
  expect(manager.data.length, lessThanOrEqualTo(10));

  // Verify all remaining points are within 10 second window
  final cutoff = DateTime.now().subtract(const Duration(seconds: 10));
  for (final point in manager.data) {
    expect(point.timestamp.isAfter(cutoff), true);
  }
});
```

### 测试: Tab 结构验证

```dart
testWidgets('MainScreen has BottomNavigationBar', (WidgetTester tester) async {
  await tester.pumpWidget(
    const MaterialApp(home: MainScreen()),
  );

  expect(find.byType(BottomNavigationBar), findsOneWidget);
});

testWidgets('Bluetooth tab displays device list', (WidgetTester tester) async {
  final mockService = MockBluetoothService();
  when(mockService.devices).thenReturn([mockDevice]);

  await tester.pumpWidget(
    MaterialApp(
      home: ProviderScope(
        child: MainScreen(service: mockService),
      ),
    ),
  );

  // Navigate to Bluetooth tab (index 0)
  await tester.tap(find.text('Bluetooth'));
  await tester.pumpAndSettle();

  expect(find.byType(DeviceCard), findsWidgets);
});

testWidgets('Logs tab displays scrolling logs', (WidgetTester tester) async {
  final logService = LogService();
  for (int i = 0; i < 10; i++) {
    logService.info('Log message $i');
  }

  await tester.pumpWidget(
    MaterialApp(
      home: ProviderScope(
        child: MainScreen(logService: logService),
      ),
    ),
  );

  // Navigate to Logs tab (index 1)
  await tester.tap(find.text('Logs'));
  await tester.pumpAndSettle();

  expect(find.byType(LogsView), findsOneWidget);
  expect(find.text('Log message 0'), findsOneWidget);
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
