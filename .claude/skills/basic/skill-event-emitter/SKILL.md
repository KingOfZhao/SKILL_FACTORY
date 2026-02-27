---
name: skill-event-emitter
description: 环节完成事件通知，触发下一步骤
---

# Skill 事件发射器（Event Emitter）

## Capabilities（单一职责）
- 监听环节完成状态
- 发射标准化事件消息
- 支持异步事件发送
- 提供事件日志记录

## 执行前必须读取
common/underlying-convention.md
skill-protocol-adapter/output/protocol-spec.json

## 执行流程（5 步骤）

```
1. 读取协议规范
2. 检测环节完成状态
3. 构建事件消息
4. 写入事件队列
5. 触发目标环节
```

## 输入规范

| 类型 | 格式 | 说明 |
|------|------|------|
| 事件类型 | 字符串 | completed/failed/warning/info |
| 来源环节 | 字符串 | 当前环节名称 |
| 目标环节 | 字符串 | 下一步环节名称 |
| 载荷数据 | JSON | 传递的数据内容 |

## 输出规范

**事件消息**：
```json
{
  "event_type": "completed",
  "source": "问题穷举器",
  "target": "生成器",
  "timestamp": "2026-02-27T18:00:00Z",
  "payload": {
    "skills_count": 30,
    "output_path": "待应用-skill/flutter_factory"
  }
}
```

**事件日志**：
```json
{
  "event_id": "evt-001",
  "timestamp": "2026-02-27T18:00:00Z",
  "event_log": [
    {
      "event": "completed",
      "source": "问题穷举器",
      "target": "生成器",
      "status": "sent"
    }
  ]
}
```

## 10 分钟快速验证指南

### 验证步骤

1. **运行发射器**（<2 分钟）
   ```bash
   /skill-event-emitter --type completed --source "问题穷举器" --target "生成器" \
     --payload '{"skills_count": 30}'
   ```

2. **检查事件消息**（<2 分钟）
   ```bash
   cat output/event-message.json | jq .
   ```
   预期：看到完整的事件结构

3. **验证事件日志**（<2 分钟）
   ```bash
   cat output/event-log.json | jq '.event_log[-1].status'
   # 预期: "sent"
   ```

4. **测试目标触发**（<2 分钟）
   ```bash
   # 验证目标环节被正确触发
   # 需要目标环节运行并监听
   ```

5. **查看 payload**（<2 分钟）
   ```bash
   jq '.payload' output/event-message.json
   ```

**总耗时：≤ 10 分钟**

成功标志：
- event-message.json 格式正确
- event-log.json 记录了事件
- 目标环节能接收到事件

## Limitations（必须声明）
- 本 Skill 只负责发射事件，不处理响应
- 目标环节需要实现事件监听机制
- 事件发送依赖文件系统

## 使用方法

### 发射完成事件
```bash
/skill-event-emitter --type completed --source "问题穷举器" --target "生成器" \
  --payload '{"skills_count": 30, "output_path": "待应用-skill/flutter_factory"}'
```

### 发射失败事件
```bash
/skill-event-emitter --type failed --source "检查器" --target "优化器" \
  --error_message "检查失败：10分钟验证缺失"
```

### 查看事件日志
```bash
cat output/event-log.json
```

## 输出文件位置
```
output/
├── event-message.json    # 最新事件消息
└── event-log.json        # 事件历史日志
```
