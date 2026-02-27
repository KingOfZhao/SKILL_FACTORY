---
name: skill-pipeline-retry
description: 环节失败自动重试，提升容错性
---

# Skill 管道重试器（Pipeline Retry）

## Capabilities（单一职责）
- 监听环节失败事件
- 自动重试失败的环节
- 配置重试策略（次数、间隔、指数退避）
- 记录重试历史

## 执行前必须读取
common/underlying-convention.md
skill-protocol-adapter/output/protocol-spec.json

## 执行流程（5 步骤）

```
1. 读取重试配置
2. 监听失败事件
3. 评估是否需要重试
4. 执行重试或记录失败
5. 输出重试报告
```

## 输入规范

| 类型 | 格式 | 说明 |
|------|------|------|
| 重试配置 | JSON | 最大重试次数、间隔时间 |

**重试配置示例**：
```json
{
  "max_retries": 3,
  "initial_delay_ms": 1000,
  "max_delay_ms": 10000,
  "exponential_backoff": true,
  "retryable_errors": ["timeout", "network_error", "temp_failure"]
}
```

## 输出规范

**重试报告**：
```json
{
  "retry_time": "2026-02-27T18:00:00Z",
  "original_event": {
    "event_type": "failed",
    "source": "检查器",
    "target": "优化器",
    "error": "timeout"
  },
  "retry_attempts": [
    {
      "attempt": 1,
      "timestamp": "2026-02-27T18:00:01Z",
      "delay_ms": 1000,
      "status": "failed",
      "error": "timeout"
    },
    {
      "attempt": 2,
      "timestamp": "2026-02-27T18:00:02Z",
      "delay_ms": 2000,
      "status": "failed",
      "error": "timeout"
    },
    {
      "attempt": 3,
      "timestamp": "2026-02-27T18:00:04Z",
      "delay_ms": 4000,
      "status": "succeeded"
    }
  ],
  "final_status": "succeeded",
  "total_duration_ms": 4000,
  "attempts_count": 3
}
```

## 10 分钟快速验证指南

### 验证步骤

1. **运行重试器**（<2 分钟）
   ```bash
   /skill-pipeline-retry --event '{"event_type":"failed","source":"检查er","error":"timeout"}'
   ```

2. **检查重试报告**（<2 分钟）
   ```bash
   cat output/retry-report.json | jq '.final_status'
   # 预期: "succeeded" 或 "gave_up"
   ```

3. **验证重试次数**（<2 分钟）
   ```bash
   jq '.attempts_count' output/retry-report.json
   # 预期: <= max_retries
   ```

4. **检查延迟策略**（<2 分钟）
   ```bash
   jq '.retry_attempts[].delay_ms' output/retry-report.json
   # 预期: 指数增长或固定间隔
   ```

5. **查看错误类型**（<2 分钟）
   ```bash
   jq '.retry_attempts[-1].status' output/retry-report.json
   ```

**总耗时：≤ 10 分钟**

成功标志：
- final_status 为 succeeded 或 gave_up
- 重试次数不超过最大值
- 延迟符合配置

## Limitations（必须声明）
- 重试逻辑基于配置的 error 类型
- 非可重试错误会立即放弃
- 不修改原始事件的错误信息

## 使用方法

### 重试失败事件
```bash
/skill-pipeline-retry --event '{"event_type":"failed","source":"检查er","error":"timeout"}'
```

### 自定义重试策略
```bash
/skill-pipeline-retry --config custom-retry-config.json --event '{"event_type":"failed"}'
```

### 查看重试历史
```bash
cat output/retry-history.json
```

## 输出文件位置
```
output/
├── retry-report.json     # 最新重试报告
└── retry-history.json     # 重试历史记录
```
