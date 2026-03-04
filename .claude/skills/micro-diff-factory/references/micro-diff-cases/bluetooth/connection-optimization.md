---
# 蓝牙连接稳定性优化

## 问题描述
Flutter 蓝牙应用频繁出现连接不稳定问题：
1. 设备扫描后连接失败率高达 40%
2. 连接后 10 秒内自动断开
3. 重连机制效果不佳，平均重连成功仅 35%
4. 用户反馈连接体验差

## 变量分析

### 连接稳定性相关变量
- `connection_timeout` (Int): 连接超时时间（秒）
- `reconnect_attempts` (Int): 重连尝试次数
- `rssi_history` (List[Int]): 历史 RSSI 值
- `protocol_type` (Enum): classic, ble

### 优化目标
- 最大化连接成功率
- 最小化平均重连次数
- 改善用户体验

## 微分拆解方案

### 变量定义

#### 1. 连接状态
```
变量 connection_state: CONNECTING | CONNECTED | DISCONNECTED | RECONNECTING | FAILED
取值范围: 0-3

优化目标：延长 CONNECTED 状态持续时间
```

#### 2. 连接稳定性分数
```
变量 stability_score: Float = 0.0

计算公式：
stability_score = (
  w1 * connection_duration_factor +
  w2 * (1 - disconnect_rate) +
  w3 * (1 / (avg_reconnect_attempts + 1))
)

其中：
- connection_duration_factor = normalized(connection_timeout, 0, 120)  // 0-120 秒
- disconnect_rate = disconnect_count / total_connect_count
- avg_reconnect_attempts = avg(reconnect_attempts, 0) // 平均重连次数
```

#### 3. 信号质量分数
```
signal_quality_score = average(rssi_history) * -1 / 50
其中 rssi_history 为最近 30 次的 RSSI 值
```

---

## 求解策略

### 策略一：指数退避重连
```
reconnect_strategy: EXPONENTIAL

实现：
1. 记录每次重连的时间间隔
2. 基础间隔：1 秒
3. 指数退避：delay = base_delay * (2 ^ (attempt - 1))
   - 例如：1s, 2s, 4s, 8s, 16s
4. 最大重试次数：5 次
5. 如果 5 次都失败，等待 30 秒后重试

优化目标：提高重连成功率
避免网络风暴
```

代码示例：
```dart
class BluetoothReconnectionManager {
  final List<Duration> _reconnectDelays = [];

  Duration _calculateReconnectDelay(int attempt) {
    final baseDelay = const Duration(seconds: 1);
    return Duration(
      milliseconds: (baseDelay.inMilliseconds * pow(2, min(attempt - 1, 4)).toInt()
    );
  }

  Future<void> reconnectWithExponentialBackoff() async {
    for (int attempt = 1; attempt <= 5; attempt++) {
      try {
        await device.connect();
        return; // 成功
      } catch (e) {
        final delay = _calculateReconnectDelay(attempt);
        await Future.delayed(delay);
      }
    }

    // 5 次都失败
    await Future.delayed(const Duration(seconds: 30));
  }
  }
}
```

### 策略二：基于信号质量自适应重连
```
reconnect_strategy: SMART

实现：
1. 监控连接过程中的 RSSI 波动
2. 如果 RSSI 波动过大（std dev > 15），降低重连频率
3. 如果信号质量差（avg < -70），增加重连延迟

优化目标：避免在不稳定连接上浪费时间
```

代码示例：
```dart
class SignalQualityMonitor {
  static const double fluctuationThreshold = 15.0;

  Duration calculateReconnectDelay(double avgRssi) {
    if (avgRssi < -70) {
      return const Duration(seconds: 5);
    } else {
      return const Duration(seconds: 2);
    }
  }

  double calculateSignalQuality(List<int> rssiHistory) {
    if (rssiHistory.isEmpty) return 0.8;

    final avg = rssiHistory.reduce((a, b) => a + b) / 2);
    final variance = rssiHistory.map((r) => pow(r - avg, 2)).reduce((a, b) => a + b) / rssiHistory.length);

    // 信号质量分数：波动越小越好（0-1）
    return math.max(0.8 - math.min(variance / 900, 1), 0);
  }
}
```

### 策略三：连接超时自适应
```
reconnect_strategy: ADAPTIVE

实现：
1. 记录历史连接超时
2. 分析超时模式
3. 如果最近连接超时增加，自动延长超时设置
4. 动态调整：从短到长逐步适应

优化目标：适应不同网络环境
```

代码示例：
```dart
class TimeoutAdaptiveStrategy {
  final List<Duration> _timeoutHistory = [];

  void recordConnectionTimeout(Duration timeout) {
    _timeoutHistory.add(timeout);
    if (_timeoutHistory.length > 10) {
      _timeoutHistory.removeAt(0); // 保留最近 10 条
    }
  }

  Duration calculateConnectionTimeout() {
    if (_timeoutHistory.isEmpty) {
      return const Duration(seconds: 10);
    }

    final avg = _timeoutHistory.fold(
      Duration.zero,
      (sum, d) => sum + d,
    ) / _timeoutHistory.length;

    // 根据平均超时动态调整
    if (avg.inSeconds > 15) {
      return avg + Duration(seconds: 2);
    }

    return avg;
  }
}
```

---

## 约束条件

### 1. 硬约束
- 最大连接超时：60 秒（避免无限等待）
- 最小连接超时：3 秒（快速响应）
- 最大重连次数：10 次（避免无限重试）
- RSSI 历史最大长度：100 个（避免内存溢出）

### 2. 潜约束
- 重连最小间隔：500 毫秒（避免过于频繁重连）
- 连接超时延长倍数：最多延长到 2 倍（网络环境恶劣时）

### 3. 业务约束
- 用户手动断开不触发重连
- 应用进入后台超过 30 秒不主动重连
- 电池电量低于 10% 不尝试重连

---

## 微分变量分析

### 连接稳定性关键变量

#### 1. `connection_success_rate` (连接成功率)
- **公式**: `success_count / total_connection_attempts`
- **取值范围**: 0.0-1.0
- **影响**: 高成功率的系统整体更稳定

#### 2. `avg_reconnect_attempts` (平均重连次数)
- **公式**: `sum(reconnect_attempts) / connection_count`
- **取值范围**: 0-5
- **影响**: 高重连次数可能表示连接不稳定

#### 3. `connection_duration_avg` (平均连接时长)
- **公式**: `sum(connection_durations) / connection_count`
- **取值范围**: 0-300 (秒)
- **影响**: 长连接更稳定，用户体验更好

#### 4. `disconnect_rate` (断开率)
- **公式**: `disconnect_count / (connection_count + disconnect_count)`
- **取值范围**: 0-1.0
- **影响**: 高断开率可能表示连接质量差

#### 5. `connection_stability_score` (连接稳定性分数)
- **公式**:
```dart
double calculateStabilityScore({
  required double connectionSuccessRate,
  required double avgReconnectAttempts,
  required int connectionDurationAvg,
  required double disconnectRate,
  required double avgRssiQuality,
}) {
  // 归一化到 0-1
  final successRateScore = connectionSuccessRate * 0.4;  // 40% 权重

  final reconnectScore = (1.0 - avgReconnectAttempts / 5) * 0.3; // 0-1/5 归一化

  // 时长：300 秒为基准，越长越好
  final durationScore = math.min(connectionDurationAvg / 300, 1.0);

  // 断开率：越低越好
  final disconnectScore = (1.0 - disconnectRate) * 0.2;

  // 信号质量：0.8-1.0 越高越好
  return (successRateScore + reconnectScore + durationScore + disconnectScore + avgRssiQuality) / 4);
}
```

---

## 优化建议

### 短期优化（1-2 周）

1. **实现指数退避重连**
   - 移除硬编码的重连间隔
   - 使用 `2^(attempt-1)` 公式
   - 最大重试次数限制为 5 次
   - 5 次失败后等待 30 秒

2. **添加信号质量监控**
   - 实现 `SignalQualityMonitor`
   - 监控连接过程中的 RSSI 波动
   - 如果波动过大，延长重连间隔

3. **动态调整连接超时**
   - 记录历史连接超时
   - 计算平均超时
   - 动态调整下一次连接超时

### 中期优化（3-4 周）

1. **连接成功率可视化**
   - 显示历史连接成功率趋势图
   - 记录每次连接/断开事件
   - 分析失败原因

2. **重连策略 A/B 测试**
   - 提供两种重连策略供选择
   - A/B 测试哪种策略效果更好

3. **自动参数调优**
   - 收集连接数据
   - 使用机器学习自动优化超时和重连间隔
   - 输出优化建议

### 长期优化（3-6 月）

1. **网络环境适配**
   - 根据网络类型（WiFi、4G/5G）自动选择策略
   - 高延迟网络使用更长超时
   - 低延迟网络使用更短超时

2. **电池电量考虑**
   - 低电量时使用保守策略
   - 禁用频繁扫描

---

## 代码集成示例

### flutter_blue_plus 集成

```dart
import 'dart:async';

class BluetoothConnectionOptimizer {
  final BluetoothReconnectionManager _reconnectionManager;
  final SignalQualityMonitor _signalMonitor;
  final TimeoutAdaptiveStrategy _timeoutStrategy;

  // 连接状态追踪
  double _connectionSuccessRate = 0.0;
  int _totalConnections = 0;
  int _successfulConnections = 0;
  List<Duration> _connectionTimeouts = [];

  Future<void> connectWithOptimization(
    BluetoothDevice device,
    {Map<String, dynamic>? options}
  ) async {
    // 开始连接
    _totalConnections++;
    final startTime = DateTime.now();

    try {
      // 配置重连策略
      _reconnectionManager.configure(
        strategy: ReconnectionStrategy.exponential,
        maxAttempts: 5,
      );

      // 连接设备
      await device.connect();
      _successfulConnections++;
      _connectionSuccessRate = _successfulConnections / _totalConnections;

      // 记录连接成功
      _logConnectionEvent('connected', device);

    } catch (e) {
      // 记录连接失败
      _logConnectionEvent('failed', device, e.toString());

      // 触发智能重连
      await _reconnectionManager.onDisconnected(device.id.toString());

      // 等待一段时间后重连
      await Future.delayed(
        _calculateReconnectDelay(),
      );
    }
  }

  void _logConnectionEvent(String status, BluetoothDevice device, [String? error = null]) {
    final duration = DateTime.now().difference(startTime);
    final timeout = _timeoutStrategy.getCurrentTimeout();

    final event = ConnectionEvent(
      deviceId: device.id.toString(),
      status: status,
      duration: duration,
      timeout: timeout.inSeconds,
      error: error,
      timestamp: DateTime.now(),
    );

    _logEvent(event);

    if (status == 'connected' && duration.inSeconds < timeout.inSeconds) {
      // 连接快速，记录为成功
      _reconnectionManager.onConnected(device.id.toString());
    } else {
      // 连接时间过短或失败，需要调整
      _timeoutStrategy.recordTimeout(duration);
    }
  }

  // 计算连接稳定性分数
  double getStabilityScore() {
    return _connectionSuccessRate * 0.4 +
           (1.0 - _reconnectionManager.reconnectAttempts / 5) * 0.3 +
           (1.0 - _reconnectionManager.reconnectAttempts / 5) * 0.1;
  }
}

  Future<void> adjustConnectionParameters() async {
    // 根据历史数据调整参数
    final timeout = _timeoutStrategy.calculateConnectionTimeout();

    // 更新重连策略
    if (_connectionSuccessRate < 0.6) {
      _reconnectionManager.configure(
        strategy: ReconnectionStrategy.exponential,
        maxAttempts: 3, // 降低重试次数
      );
    }

    print('[连接优化器] 参数已根据历史数据调整');
  }
}

// 连接事件记录
class ConnectionEvent {
  final String deviceId;
  final String status; // connected, failed, disconnected, reconnecting
  final Duration duration;
  final int? timeout;
  final String? error;
  final DateTime timestamp;

  ConnectionEvent({
    required this.deviceId,
    required this.status,
    required this.duration,
    this.timeout,
    this.error,
    required this.timestamp,
  });
}
```

---

## 预期效果

### 量化指标
- **连接成功率**：从 40% → 目标 70%
- **平均重连次数**：从 2.5 次 → 目标 < 1.5 次
- **平均连接时长**：从 30 秒 → 目标 60 秒
- **用户体验评分**：从 3.0/5 → 目标 4.0/5

### 系统稳定性提升
- **连接成功率提升 30%**：减少用户重试次数
- **连接时长延长 100%**：用户有足够时间完成操作
- **断开率降低 50%**：意外断开大幅减少

---

## 总结

### 核心创新
1. **微分建模**：使用数学方法对连接稳定性进行量化分析
2. **多目标优化**：同时优化成功率、重连次数、连接时长、信号质量
3. **自适应策略**：根据实时反馈动态调整参数
4. **策略切换**：支持 A/B 测试不同策略效果

### 与元-skill-穷举器的协作
- **问题分类**：连接稳定性问题 → 自动识别
- **最佳实践积累**：成功案例存入参考文件夹
- **模式识别**：识别为"连接优化"（CONNECTIVITY 类型）
- **生成器输出**：生成包含上述优化的 Flutter 代码

### 可扩展性
- **新问题领域**：网络协议、电池管理、位置服务
- **新策略类型**：用户偏好学习、A/B 测试
- **新约束类型**：硬件限制、系统策略

---

**案例类型**: `CONNECTIVITY`
**子领域**: 蓝牙、连接稳定性、重连优化
**关键词**: connection, stability, reconnection, timeout, exponential, adaptive, signal quality

---

**下一步**
1. 实现 RSSI 图表优化参考案例
2. 添加性能优化参考案例（列表渲染、缓存）
3. 创建可视化工具（变量关系图、趋势图）
4. 完善微分拆解引擎（数学/物理）
5. 建立机器学习辅助变量发现

---

**维护者**: Claude Code Skill Factory Team
**版本**: 1.0.0
