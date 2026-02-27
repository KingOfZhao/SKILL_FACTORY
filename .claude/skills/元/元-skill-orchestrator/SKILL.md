---
name: 元-skill-orchestrator
description: 元 Skill 全链路编排器 - 自动串联问题穷举、生成、扫描、检查、优化流程
---

# 元-Skill 编排器（Skill Orchestrator）

## Capabilities（单一职责）
- 接收用户需求输入
- 自动调用并串联元 Skill 全链路
- 协调各环节的数据流转
- 输出完整的链路执行报告

## 执行前必须读取
common/underlying-convention.md

## 全链路定义

根据底层约定中的 `rules.skill_chain.full_chain`，完整链路如下：

```
用户需求输入
    ↓
[问题穷举器]
    ↓ 输出 Skill 树建议
[生成器]
    ↓ 生成具体 Skill
[扫描器]
    ↓ 生成能力清单
[检查器]
    ↓ 输出 diagnosis.json
[优化器]
    ↓
优化报告
```

## 执行流程（自动编排）

### 模式 1：完整自动链路（--full-chain）

```
1. 接收用户需求输入
2. 调用问题穷举器（物理实践/Skill 树模式）
3. 穷举器输出传递给生成器
4. 生成器生成技能并调用扫描器
5. 扫描器完成后调用检查器
6. 检查器输出 diagnosis.json 传递给优化器
7. 优化器生成优化报告
8. 输出完整链路报告
```

### 模式 2：从中间环节开始（--start-at）

```
--start-at generator : 从生成器开始
--start-at scanner  : 从扫描器开始
--start-at checker  : 从检查器开始
--start-at optimizer  : 从优化器开始
```

### 模式 3：单步执行（--single-step）

```
只执行指定的单个环节，不继续后续环节
```

## 输入规范

| 类型 | 格式 | 说明 |
|------|------|------|
| 需求描述 | 纯文本 | 用户的需求问题 |
| 模式选择 | --full-chain / --start-at / --single-step | 执行模式 |

示例：
```bash
# 完整自动链路
/元-skill-orchestrator "生成一个 Flutter 登录技能" --full-chain

# 从生成器开始
/元-skill-orchestrator --start-at generator --input "skill 树建议"

# 单步执行检查器
/元-skill-orchestrator --single-step checker --target .claude/skills/元
```

## 输出格式

### 链路执行报告（output/chain-execution-report.md）

```markdown
# 元 Skill 链路执行报告

## 执行概览
- 执行时间: 2026-02-27T17:00:00Z
- 执行模式: full-chain
- 总耗时: 15 分钟

## 执行步骤

### 1. 问题穷举器
- **状态**: ✓ 完成
- **耗时**: 3 分钟
- **输出**: 30 个技能建议

### 2. 生成器
- **状态**: ✓ 完成
- **耗时**: 5 分钟
- **生成技能**: 30 个
- **位置**: 待应用-skill/flutter_factory/

### 3. 扫描器
- **状态**: ✓ 完成
- **耗时**: 2 分钟
- **扫描结果**: 37 个技能

### 4. 检查器
- **状态**: ✓ 完成
- **耗时**: 3 分钟
- **通过**: 35
- **警告**: 2
- **失败**: 0

### 5. 优化器
- **状态**: ✓ 完成
- **耗时**: 2 分钟
- **Skill 优化方案**: 2 个
- **底层约定优化方案**: 1 个（需确认）

## 数据流转

```
需求 → 问题穷举 → Skill树 → 生成器 → 技能文件 → 扫描器 → 能力清单 → 检查器 → diagnosis.json → 优化器 → 优化报告
```

## 生成物

| 物品 | 位置 | 说明 |
|------|------|------|
| 问题穷举输出 | 元-skill-问题穷举器/output/ | 穷举建议 |
| 生成的技能 | 待应用-skill/flutter_factory/ | 30 个技能 |
| 扫描清单 | 元-skill-扫描器/output/ | 能力清单 |
| 检查报告 | 元-skill-检查器/check-results/ | diagnosis.json |
| 优化报告 | 元-skill-优化器/output/ | 优化方案 |

## 建议后续操作

### 1. 底层约定优化
查看 `元-skill-优化器/output/convention-optimization.md`
确认后手动修改 `common/underlying-convention.md`

### 2. 技能应用
`待应用-skill/` 目录下的技能可直接移动到正式位置

### 3. 验证
运行 `元-skill-检查器` 验证所有优化后的技能
```

## 输出目录结构

```
output/
└── chain-execution-report.md    # 完整链路报告
```

## 10 分钟快速验证指南

### 验证步骤

1. **运行编排器**（<2 分钟）
   ```bash
   /元-skill-orchestrator "生成 Flutter 登录技能" --full-chain
   ```

2. **检查链路报告**（<2 分钟）
   ```bash
   cat output/chain-execution-report.md
   ```
   预期：包含 5 个环节的执行状态

3. **验证数据流转**（<2 分钟）
   ```bash
   grep "数据流转" output/chain-execution-report.md
   ```
   预期：看到完整的数据流转图

4. **检查生成物**（<2 分钟）
   ```bash
   ls -la 待应用-skill/flutter_factory/
   ```
   预期：包含 30 个技能

5. **查看建议操作**（<2 分钟）
   ```bash
   grep "建议后续操作" output/chain-execution-report.md
   ```

**总耗时：≤ 10 分钟**

成功标志：
- 链路报告包含 5 个环节的执行状态
- 每个环节都有明确的耗时和输出
- 生成物目录包含完整的技能文件

## 命令行参数

| 参数 | 说明 |
|------|------|
| `--full-chain` | 完整自动链路（默认） |
| `--start-at <stage>` | 从指定环节开始 |
| `--single-step <stage>` | 仅执行单步 |
| `--input <data>` | 指定环节的输入数据 |
| `--target <path>` | 指定扫描/检查的目标路径 |
| `--verbose` | 输出详细日志 |

## 使用方法示例

### 完整链路
```bash
/元-skill-orchestrator "生成一个 Flutter 电商技能" --full-chain
```

### 从生成器开始
```bash
/元-skill-orchestrator --start-at generator --input "skill 树建议"
```

### 仅运行检查器
```bash
/元-skill-orchestrator --single-step checker --target .claude/skills/待应用-skill/flutter_factory
```

### 查看链路定义
```bash
/元-skill-orchestrator --show-chain
```

## Limitations（必须声明）

- 本编排器负责调用和串联，不替代各环节的具体功能
- 依赖各元 Skill 的可用性
- 链路执行时间取决于任务复杂度
- 需确保底层约定中的 skill_chain 定义正确
- 优化器的底层约定优化方案需人工确认后手动应用

## 输出文件位置
```
output/
└── chain-execution-report.md    # 完整链路报告
```
