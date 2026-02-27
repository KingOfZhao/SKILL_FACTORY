---
name: skill-progress-tracker
description: 全链路进度追踪，实时监控执行状态
---

# Skill 进度追踪器（Progress Tracker）

## Capabilities（单一职责）
- 追踪全链路的执行状态
- 记录每个步骤的耗时和输出
- 提供实时进度查询接口
- 生成进度汇总报告

## 执行前必须读取
common/underlying-convention.md
skill-protocol-adapter/output/protocol-spec.json

## 执行流程（5 步骤）

```
1. 初始化链路追踪
2. 监听各环节事件
3. 更新步骤状态
4. 计算总耗时和进度百分比
5. 输出进度报告
```

## 输入规范

| 类型 | 格式 | 说明 |
|------|------|------|
| 链路 ID | 字符串 | 唯一标识符 |

## 输出规范

**进度报告**：
```json
{
  "chain_id": "flutter-ecommerce-001",
  "start_time": "2026-02-27T18:00:00Z",
  "current_time": "2026-02-27T18:15:00Z",
  "total_elapsed_ms": 900000,
  "progress_percent": 75,
  "status": "in_progress",
  "steps": [
    {
      "name": "问题穷举器",
      "status": "completed",
      "start_time": "2026-02-27T18:00:00Z",
      "end_time": "2026-02-27T18:03:00Z",
      "duration_ms": 180000,
      "output": "30-skill-suggestions"
    },
    {
      "name": "生成器",
      "status": "completed",
      "start_time": "2026-02-27T18:03:00Z",
      "end_time": "2026-02-27T18:08:00Z",
      "duration_ms": 300000,
      "output": "30-skills-generated"
    },
    {
      "name": "扫描器",
      "status": "completed",
      "start_time": "2026-02-27T18:08:00Z",
      "end_time": "2026-02-27T18:10:00Z",
      "duration_ms": 120000,
      "output": "37-skills-catalog"
    },
    {
      "name": "检查器",
      "status": "completed",
      "start_time": "2026-02-27T18:10:00Z",
      "end_time": "2026-02-27T18:13:00Z",
      "duration_ms": 180000,
      "output": "diagnosis.json"
    },
    {
      "name": "优化器",
      "status": "in_progress",
      "start_time": "2026-02-27T18:13:00Z",
      "end_time": null,
      "duration_ms": 120000,
      "output": "pending"
    }
  ]
}
```

## 10 分钟快速验证指南

### 验证步骤

1. **运行追踪器**（<2 分钟）
   ```bash
   /skill-progress-tracker --chain-id "flutter-ecommerce-001"
   ```

2. **检查进度报告**（<2 分钟）
   ```bash
   cat output/progress-report.json | jq '.status'
   # 预期: "in_progress", "completed", 或 "failed"
   ```

3. **验证进度百分比**（<2 分钟）
   ```bash
   jq '.progress_percent' output/progress-report.json
   # 预期: 0-100
   ```

4. **查看步骤状态**（<2 分钟）
   ```bash
   jq '.steps[] | select(.status == "in_progress")' output/progress-report.json
   ```
   预期：最多一个步骤为 in_progress

5. **检查时间计算**（<2 分钟）
   ```bash
   jq '.total_elapsed_ms' output/progress-report.json
   ```

**总耗时：≤ 10 分钟**

成功标志：
- progress_percent 正确计算
- 步骤状态逻辑正确
- 时间计算准确

## Limitations（必须声明）
- 进度追踪依赖事件消息
- 需要各环节正确发射事件
- 不执行实际的重试或补偿

## 使用方法

### 启动追踪
```bash
/skill-progress-tracker --chain-id "flutter-ecommerce-001" --auto-start
```

### 查询进度
```bash
/skill-progress-tracker --chain-id "flutter-ecommerce-001" --query
```

### 查看详细进度
```bash
cat output/progress-report.json | jq '.steps[]'
```

## 输出文件位置
```
output/
├── progress-report.json     # 进度报告
└── progress-log.json        # 进度日志
```
