# UI 通用模式

## Tab 结构模式

### BottomNavigationBar + TabBarView

```dart
class MainScreen extends ConsumerStatefulWidget {
  @override
  ConsumerState<MainScreen> createState() => _MainScreenState();
}

class _MainScreenState extends ConsumerState<MainScreen> {
  int _selectedIndex = 0;

  final List<Widget> _pages = [
    const BluetoothTab(),
    const LogsTab(),
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: _pages[_selectedIndex],
      bottomNavigationBar: BottomNavigationBar(
        currentIndex: _selectedIndex,
        onTap: (index) => setState(() => _selectedIndex = index),
        items: const [
          BottomNavigationBarItem(
            icon: Icon(Icons.bluetooth),
            label: 'Bluetooth',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.list),
            label: 'Logs',
          ),
        ],
      ),
    );
  }
}
```

## 设备列表模式

### 卡片视图

```dart
class DeviceCard extends StatelessWidget {
  final BluetoothDevice device;
  final int rssi;
  final VoidCallback onTap;

  const DeviceCard({
    required this.device,
    required this.rssi,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      child: ListTile(
        leading: const Icon(Icons.bluetooth),
        title: Text(device.name ?? 'Unknown'),
        subtitle: Text(device.id.toString()),
        trailing: _buildRssiIndicator(rssi),
        onTap: onTap,
      ),
    );
  }

  Widget _buildRssiIndicator(int rssi) {
    Color color = _getRssiColor(rssi);
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
      decoration: BoxDecoration(
        color: color.withOpacity(0.2),
        borderRadius: BorderRadius.circular(4),
      ),
      child: Text(
        '$rssi dBm',
        style: TextStyle(color: color, fontWeight: FontWeight.bold),
      ),
    );
  }

  Color _getRssiColor(int rssi) {
    if (rssi >= -60) return Colors.green;
    if (rssi >= -80) return Colors.orange;
    return Colors.red;
  }
}
```

## 实时图表模式（RSSI Time Series）

### 使用 fl_chart

```dart
class RssiChart extends StatelessWidget {
  final List<RssiPoint> data;

  const RssiChart({required this.data});

  @override
  Widget build(BuildContext context) {
    return LineChart(
      LineChartData(
        minX: data.first.timestamp,
        maxX: data.last.timestamp,
        minY: -100,
        maxY: -40,
        gridData: const FlGridData(show: true),
        titlesData: const FlTitlesData(show: false),
        borderData: FlBorderData(show: true),
        lineBarsData: [
          LineChartBarData(
            spots: data.map((point) =>
              FlSpot(point.timestamp.toDouble(), point.rssi.toDouble())
            ).toList(),
            isCurved: true,
            color: Colors.blue,
            barWidth: 2,
            dotData: const FlDotData(show: false),
          ),
        ],
      ),
    );
  }
}

// RSSI 数据点
class RssiPoint {
  final DateTime timestamp;
  final int rssi;

  RssiPoint(this.timestamp, this.rssi);
}
```

### 10秒滚动窗口

```dart
class RssiManager extends ChangeNotifier {
  final List<RssiPoint> _data = [];
  static const Duration windowSize = Duration(seconds: 10);

  void addRssi(int rssi) {
    final now = DateTime.now();
    _data.add(RssiPoint(now, rssi));
    _trimToWindowSize();
    notifyListeners();
  }

  void _trimToWindowSize() {
    final cutoff = DateTime.now().subtract(windowSize);
    _data.removeWhere((point) => point.timestamp.isBefore(cutoff));
  }

  List<RssiPoint> get data => List.unmodifiable(_data);
}
```

## 日志显示模式

### 滚动日志视图

```dart
class LogsView extends StatelessWidget {
  final List<LogEntry> logs;

  const LogsView({required this.logs});

  @override
  Widget build(BuildContext context) {
    return ListView.builder(
      reverse: true, // 新日志在底部
      itemCount: logs.length,
      itemBuilder: (context, index) {
        final log = logs[logs.length - 1 - index];
        return LogTile(entry: log);
      },
    );
  }
}

class LogTile extends StatelessWidget {
  final LogEntry entry;

  const LogTile({required this.entry});

  @override
  Widget build(BuildContext context) {
    final color = _getLogColor(entry.level);
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 4),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            entry.timestamp,
            style: TextStyle(
              color: Colors.grey[600],
              fontSize: 12,
            ),
          ),
          const SizedBox(width: 8),
          Expanded(
            child: Text(
              entry.message,
              style: TextStyle(color: color),
            ),
          ),
        ],
      ),
    );
  }

  Color _getLogColor(LogLevel level) {
    switch (level) {
      case LogLevel.error: return Colors.red;
      case LogLevel.warning: return Colors.orange;
      case LogLevel.info: return Colors.blue;
      case LogLevel.debug: return Colors.grey;
    }
  }
}

enum LogLevel { debug, info, warning, error }

class LogEntry {
  final String timestamp;
  final String message;
  final LogLevel level;
}
```

## PDF 需求覆盖

| 需求点 | UI 实现 |
|--------|---------|
| Tab 结构 | BottomNavigationBar + TabBarView |
| 设备列表 | ListView + DeviceCard (名称/MAC/RSSI) |
| RSSI 可视化 | fl_chart LineChart + 10秒滚动 |
| 滚动日志 | ListView(reverse: true) + LogTile |
