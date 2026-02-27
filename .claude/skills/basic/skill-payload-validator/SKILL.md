---
name: skill-payload-validator
description: 数据包校验，验证数据完整性
---

# Skill 载荷验证器（Payload Validator）

## Capabilities（单一职责）
- 验证事件消息的数据完整性
- 检查必需字段是否存在
- 验证数据类型和格式
- 生成验证报告

## 执行前必须读取
common/underlying-convention.md
skill-protocol-adapter/output/protocol-spec.json

## 执行流程（5 步骤）

```
1. 读取事件消息文件
2. 加载协议规范
3. 验证必需字段
4. 检查数据类型
5. 输出验证结果
```

## 输入规范

| 类型 | 格式 | 说明 |
|------|------|------|
| 事件消息 | JSON | 事件消息文件路径 |

## 输出规范

**验证报告**：
```json
{
  "validation_time": "2026-02-27T18:00:00Z",
  "message_id": "msg-001",
  "validation_result": {
    "is_valid": true,
    "errors": [],
    "warnings": []
  },
  "field_checks": [
    {
      "field": "event_type",
      "present": true,
      "type": "string",
      "valid": true
    },
    {
      "field": "source",
      "present": true,
      "type": "string",
      "valid": true
    },
    {
      "field": "timestamp",
      "present": true,
      "type": "string",
      "format": "ISO8601",
      "valid": true
    },
    {
      "field": "payload",
      "present": true,
      "type": "object",
      "valid": true
    }
  ],
  "summary": {
    "total_fields": 4,
    "required_fields": 4,
    "missing_fields": 0,
    "invalid_fields": 0
  }
}
```

## 10 分钟快速验证指南

### 验证步骤

1. **运行验证器**（<2 分钟）
   ```bash
   /skill-payload-validator output/event-message.json
   ```

2. **检查验证结果**（<2 分钟）
   ```bash
   cat output/validation-report.json | jq '.validation_result.is_valid'
   # 预期: true
   ```

3. **查看字段检查**（<2 分钟）
   ```bash
   jq '.field_checks[] | select(.valid == false)' output/validation-report.json
   # 预期: 空数组
   ```

4. **验证错误报告**（<2 分钟）
   ```bash
   jq '.validation_result.errors' output/validation-report.json
   # 预期: 空数组
   ```

5. **检查汇总**（<2 分钟）
   ```bash
   jq '.summary' output/validation-report.json
   ```

**总耗时：≤ 10 分钟**

成功标志：
- is_valid 为 true
- errors 数组为空
- 所有字段检查通过

## Limitations（必须声明）
- 本 Skill 只负责数据验证，不执行事件
- 验证规则基于协议规范
- 不处理数据的业务逻辑

## 使用方法

### 验证事件消息
```bash
/skill-payload-validator output/event-message.json
```

### 验证批量消息
```bash
/skill-payload-validator /path/to/events/*.json
```

## 输出文件位置
```
output/
└── validation-report.json    # 验证报告
```
