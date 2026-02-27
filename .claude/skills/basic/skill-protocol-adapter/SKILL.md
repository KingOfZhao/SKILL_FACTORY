---
name: skill-protocol-adapter
description: 环节间数据格式标准化，建立统一的消息格式标准
---

# Skill 协议适配器（Protocol Adapter）

## Capabilities（单一职责）
- 定义环节间数据交换的消息格式标准
- 提供消息序列化和反序列化接口
- 支持事件类型和目标节点配置
- 生成 JSON Schema 验证规则

## 执行前必须读取
common/underlying-convention.md

## 执行流程（5 步骤）

```
1. 读取底层约定中的 skill_chain 定义
2. 分析各环节的数据交换需求
3. 定义统一的消息格式标准
4. 生成 JSON Schema
5. 输出到 output/protocol-spec.json
```

## 输入规范

| 类型 | 格式 | 说明 |
|------|------|------|
| 环节类型 | 字符串 | 发起方的环节名称 |

## 输出规范

**协议格式标准**：
```json
{
  "protocol_version": "1.0",
  "message_format": {
    "event": {
      "type": "object",
      "required": ["event_type", "source", "timestamp", "payload"],
      "properties": {
        "event_type": {
          "type": "string",
          "enum": ["completed", "failed", "warning", "info"]
        },
        "source": {
          "type": "string",
          "description": "发起环节的名称"
        },
        "target": {
          "type": "string",
          "description": "目标环节的名称"
        },
        "timestamp": {
          "type": "string",
          "format": "ISO8601"
        },
        "payload": {
          "type": "object",
          "description": "传递的数据内容"
        }
      }
    }
  },
  "event_types": {
    "completed": "环节成功完成",
    "failed": "环节执行失败",
    "warning": "执行过程中的警告",
    "info": "一般信息"
  },
  "transport": {
    "method": "file-based",
    "description": "通过文件传递消息，便于调试"
  }
}
```

## 消息示例

```json
{
  "event_type": "completed",
  "source": "问题穷举器",
  "target": "生成器",
  "timestamp": "2026-02-27T18:00:00Z",
  "payload": {
    "skill_suggestions": [
      {
        "name": "flutter-login-page",
        "priority": "high"
      }
    ]
  }
}
```

## 10 分钟快速验证指南

### 验证步骤

1. **运行适配器**（<2 分钟）
   ```bash
   /skill-protocol-adapter 生成器
   ```

2. **检查 JSON Schema**（<2 分钟）
   ```bash
   cat output/protocol-spec.json | jq .
   ```
   预期：看到完整的协议定义

3. **验证消息格式**（<2 分钟）
   ```bash
   # 创建测试消息
   echo '{"event_type":"completed","source":"test","timestamp":"2026-02-27T18:00:00Z","payload":{}}' | \
   jq -f 'select(has("event_type") and has("source") and has("timestamp") and has("payload"))'
   # 预期: true
   ```

4. **测试序列化**（<2 分钟）
   ```bash
   # 验证可以正确序列化
   cat test_message.json | jq '.'
   ```

5. **查看 transport 说明**（<2 分钟）
   ```bash
   jq '.transport' output/protocol-spec.json
   ```

**总耗时：≤ 10 分钟**

成功标志：
- protocol-spec.json 包含完整的 message_format 定义
- 消息可以通过 jq 解析
- event_types 定义清晰

## Limitations（必须声明）
- 本 Skill 只负责协议定义，不实际传输消息
- 传输机制由各环节自行实现
- 协议版本需要兼容性管理

## 使用方法

### 生成协议
```bash
/skill-protocol-adapter
# 生成通用协议
```

### 针对特定环节
```bash
/skill-protocol-adapter 生成器
# 生成适合生成器的协议
```

## 输出文件位置
```
output/
└── protocol-spec.json    # 协议规范文件
```
