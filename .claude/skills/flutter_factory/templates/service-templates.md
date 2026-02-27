# Service 模板

## 蓝牙服务模板（flutter_blue_plus）

```dart
import 'package:flutter_blue_plus/flutter_blue_plus.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

final bluetoothServiceProvider = Provider<BluetoothService>((ref) {
  return BluetoothService();
});

class BluetoothService {
  BluetoothDevice? _connectedDevice;
  bool _isScanning = false;
  final List<BluetoothDevice> _discoveredDevices = [];

  StreamSubscription<ScanResult>? _scanSubscription;
  StreamSubscription<BluetoothDeviceState>? _stateSubscription;

  // Scanning
  Future<void> startScan({Duration timeout = const Duration(seconds: 30)}) async {
    if (_isScanning) return;

    try {
      await FlutterBluePlus.startScan(timeout: timeout);
      _isScanning = true;
      _scanSubscription = FlutterBluePlus.scanResults.listen((results) {
        for (var result in results) {
          if (!_discoveredDevices.contains(result.device)) {
            _discoveredDevices.add(result.device);
          }
        }
      });
    } catch (e) {
      _logError('Failed to start scan', e);
      rethrow;
    }
  }

  Future<void> stopScan() async {
    await FlutterBluePlus.stopScan();
    await _scanSubscription?.cancel();
    _isScanning = false;
  }

  // Connection
  Future<void> connect(BluetoothDevice device) async {
    try {
      await device.connect();
      _connectedDevice = device;
      _stateSubscription = device.state.listen((state) {
        if (state == BluetoothDeviceState.disconnected) {
          _onDisconnected();
        }
      });
    } catch (e) {
      _logError('Failed to connect', e);
      rethrow;
    }
  }

  Future<void> disconnect() async {
    await _connectedDevice?.disconnect();
    await _stateSubscription?.cancel();
    _connectedDevice = null;
  }

  // RSSI
  Stream<int> getRssi(BluetoothDevice device) async* {
    await for (final rssi in device.rssi) {
      yield rssi;
    }
  }

  // Getters
  bool get isScanning => _isScanning;
  BluetoothDevice? get connectedDevice => _connectedDevice;
  List<BluetoothDevice> get discoveredDevices =>
      List.unmodifiable(_discoveredDevices);

  // Private
  void _onDisconnected() {
    _connectedDevice = null;
  }

  void _logError(String message, dynamic error) {
    print('$message: $error');
  }
}
```

## API Service 模板

```dart
import 'dart:convert';
import 'package:http/http.dart' as http;

class ApiService {
  final String baseUrl;
  final String apiKey;

  ApiService({
    required this.baseUrl,
    required this.apiKey,
  });

  Future<T> get<T>(String endpoint, T Function(Map<String, dynamic>) parser) async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl$endpoint'),
        headers: {
          'Authorization': 'Bearer $apiKey',
          'Content-Type': 'application/json',
        },
      );

      if (response.statusCode == 200) {
        final json = jsonDecode(response.body);
        return parser(json);
      } else {
        throw Exception('Failed to load data: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Network error: $e');
    }
  }

  Future<T> post<T>(
    String endpoint,
    Map<String, dynamic> body,
    T Function(Map<String, dynamic>) parser,
  ) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl$endpoint'),
        headers: {
          'Authorization': 'Bearer $apiKey',
          'Content-Type': 'application/json',
        },
        body: jsonEncode(body),
      );

      if (response.statusCode == 200 || response.statusCode == 201) {
        final json = jsonDecode(response.body);
        return parser(json);
      } else {
        throw Exception('Failed to post data: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Network error: $e');
    }
  }
}
```

## Storage Service 模板

```dart
import 'package:shared_preferences/shared_preferences.dart';

class StorageService {
  static const String _keyPrefix = 'app_';

  Future<void> saveString(String key, String value) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString('$_keyPrefix$key', value);
  }

  Future<String?> getString(String key) async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getString('$_keyPrefix$key');
  }

  Future<void> saveInt(String key, int value) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setInt('$_keyPrefix$key', value);
  }

  Future<int?> getInt(String key) async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getInt('$_keyPrefix$key');
  }

  Future<void> saveBool(String key, bool value) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setBool('$_keyPrefix$key', value);
  }

  Future<bool?> getBool(String key) async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getBool('$_keyPrefix$key');
  }

  Future<void> remove(String key) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove('$_keyPrefix$key');
  }

  Future<void> clear() async {
    final prefs = await SharedPreferences.getInstance();
    final keys = prefs.getKeys().where((k) => k.startsWith(_keyPrefix));
    for (var key in keys) {
      await prefs.remove(key);
    }
  }
}
```

## Log Service 模板

```dart
import 'package:flutter/foundation.dart';

class LogService {
  static const int _maxLogEntries = 1000;
  final List<LogEntry> _logs = [];
  final List<Function(LogEntry)> _listeners = [];

  void debug(String message, {Map<String, dynamic>? context}) {
    _addLog(LogLevel.debug, message, context);
  }

  void info(String message, {Map<String, dynamic>? context}) {
    _addLog(LogLevel.info, message, context);
  }

  void warning(String message, {Map<String, dynamic>? context}) {
    _addLog(LogLevel.warning, message, context);
  }

  void error(String message, {dynamic error, StackTrace? stackTrace}) {
    _addLog(LogLevel.error, message, {'error': error, 'stackTrace': stackTrace});
  }

  void _addLog(LogLevel level, String message, Map<String, dynamic>? context) {
    final entry = LogEntry(
      level: level,
      message: message,
      context: context,
      timestamp: DateTime.now(),
    );

    _logs.add(entry);

    // Trim to max size
    if (_logs.length > _maxLogEntries) {
      _logs.removeAt(0);
    }

    // Notify listeners
    for (var listener in _listeners) {
      try {
        listener(entry);
      } catch (e) {
        // Ignore listener errors
      }
    }

    // Print to console
    _printToConsole(entry);
  }

  void _printToConsole(LogEntry entry) {
    final timestamp = entry.timestamp.toIso8601String();
    final levelStr = entry.level.toString().split('.').last.toUpperCase();
    final contextStr = entry.context != null ? ' ${entry.context}' : '';
    print('[$timestamp] [$levelStr] ${entry.message}$contextStr');
  }

  List<LogEntry> get logs => List.unmodifiable(_logs);

  void addListener(Function(LogEntry) listener) {
    _listeners.add(listener);
  }

  void removeListener(Function(LogEntry) listener) {
    _listeners.remove(listener);
  }
}

enum LogLevel { debug, info, warning, error }

class LogEntry {
  final LogLevel level;
  final String message;
  final Map<String, dynamic>? context;
  final DateTime timestamp;
}
```
