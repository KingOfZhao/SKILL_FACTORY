# Basic Skills - 环节间通信协议

## 概览

本文件夹包含优先级一（Priority 1）的技能，用于建立元-Skill 体系各环节之间的标准化通信机制。

**生成时间**：2026-02-27T18:30:00Z
**总技能数**：5

## 技能清单

| 路径 | 名称 | 能力描述 | 输入 | 输出 |
|------|------|---------|------|------|
| [skill-protocol-adapter](skill-protocol-adapter/) | Skill 协议适配器 | 环节类型 | protocol-spec.json |
| [skill-event-emitter](skill-event-emitter/) | Skill 事件发射器 | 事件类型、来源、目标、载荷 | event-message.json |
| [skill-payload-validator](skill-payload-validator/) | Skill 载荷验证器 | 事件消息文件 | validation-report.json |
| [skill-pipeline-retry](skill-pipeline-retry/) | Skill 管道重试器 | 失败事件、重试配置 | retry-report.json |
| [skill-progress-tracker](skill-progress-tracker/) | Skill 进度追踪器 | 链路 ID | progress-report.json |

## 架构关系

```
数据流转
    ↓
skill-protocol-adapter (协议定义)
    ↓
skill-event-emitter (事件发射)
    ↓
skill-payload-validator (数据验证)
    ↓
skill-pipeline-retry (失败重试)
    ↓
skill-progress-tracker (进度追踪)
```

## 使用流程

### 场景 1：建立环节间通信

```bash
# 1. 定义协议标准
/skill-protocol-adapter

# 2. 发射事件
/skill-event-emitter --type completed --source "问题穷举器" --target "生成器" \
  --payload '{"skills_count": 30}'

# 3. 验证数据包
/skill-payload-validator output/event-message.json

# 4. 更新进度
/skill-progress-tracker --chain-id "flutter-ecommerce-001"
```

### 场景 2：失败自动重试

```bash
# 1. 检测失败
# 自动监听 failed 类型事件

# 2. 执行重试
/skill-pipeline-retry --event '{"event_type":"failed","source":"生成器","error":"timeout"}'

# 3. 更新进度
/skill-progress-tracker --chain-id "flutter-ecommerce-001"
```

### 场景 3：全链路监控

```bash
# 查看实时进度
/skill-progress-tracker --chain-id "flutter-ecommerce-001" --query

# 查看详细进度
cat output/progress-report.json
```

## 集成到全链路

这些技能可以集成到元-Skill 编排器的全链路中：

```
用户需求 → 问题穷举器 → 生成器 → 扫描器 → 检查器 → 优化器
                                   ↓
                           [skill-protocol-adapter]
                           ↓
                           [skill-event-emitter]
                           ↓
                           [skill-payload-validator]
                           ↓
                           [skill-pipeline-retry]
                           ↓
                           [skill-progress-tracker]
```

## 协议标准

### 消息格式

所有环节间的消息都遵循 skill-protocol-adapter 定义的格式：

```json
{
  "event_type": "completed | failed | warning | info",
  "source": "发起环节名称",
  "target": "目标环节名称",
  "timestamp": "ISO8601 时间戳",
  "payload": {
    "数据内容": "对象"
  }
}
```

### 事件类型

- **completed**：环节成功完成
- **failed**：环节执行失败
- **warning**：执行过程中的警告
- **info**：一般信息

## 调用示例

### 从外部调用技能

```bash
# 定义协议
/skill-protocol-adapter

# 发射完成事件
/skill-event-emitter --type completed --source "检查器" --target "优化器" \
  --payload '{"issues_count": 5}'

# 验证消息
/skill-payload-validator output/event-message.json

# 启动进度追踪
/skill-progress-tracker --chain-id "skill-chain-001"
```

### 通过编排器自动调用

```bash
# 使用元-Skill 编排器（已支持自动触发）
/元-skill-orchestrator "生成 Flutter 电商技能" --full-chain

# 编排器会自动调用 basic 下的技能来建立通信机制
```

## 10 分钟快速验证

### 验证步骤

1. **选择任意技能**（<1 分钟）
   - 从上方清单中任选一个

2. **查看 SKILL.md**（<2 分钟）
   - 理解技能的输入输出
   - 确认 10 分钟验证指南

3. **运行技能**（<3 分钟）
   ```bash
   /skill-protocol-adapter
   ```

4. **检查输出**（<2 分钟）
   ```bash
   cat output/protocol-spec.json | jq .
   ```

5. **验证协议格式**（<2 分钟）
   ```bash
   jq '.message_format' output/protocol-spec.json
   ```

**总耗时：≤ 10 分钟**

成功标志：
- 输出文件格式正确
- 协议规范包含完整的 message_format
- 可以用 jq 解析输出

## 目录结构

```
basic/
├── skill-protocol-adapter/     # 协议定义
│   └── SKILL.md
├── skill-event-emitter/        # 事件发射
│   └── SKILL.md
├── skill-payload-validator/    # 数据验证
│   └── SKILL.md
├── skill-pipeline-retry/       # 失败重试
│   └── SKILL.md
└── skill-progress-tracker/     # 进度追踪
    └── SKILL.md
```

## 后续开发

建议下一步实现优先级二的技能：
- 检查器增强（3 个）
- 问题穷举器增强（3 个）
- 生成器增强（3 个）

这些技能将进一步扩展元-Skill 体系的能力。

---

*本文档由 skill-protocol-adapter 自动生成*
