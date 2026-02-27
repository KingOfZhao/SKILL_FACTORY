---
name: skill-catalog-scanner
description: 扫描指定文件夹下的所有 skills，生成能力清单和树状结构
version: 1.0
author: 元-skill-生成器生成
---

# Skill 目录扫描器（Skill Catalog Scanner）

## Capabilities（单一职责）
- 扫描指定文件夹下的所有 skill 目录
- 解析每个 skill 的 SKILL.md 和 description.md
- 生成统一的 skill 能力清单（包含路径、名称、能力描述）
- 输出树状 skill 结构
- 生成 JSON 格式清单，供 Claude Code 程序化读取和调用

## 执行前必须读取
common/underlying-convention.md

## MCP 依赖
**必须**：文件系统 MCP（用于读取 SKILL.md 文件）

## 执行流程（6 步骤）

```
1. 扫描目标文件夹，识别所有 skill 目录（含 SKILL.md）
2. 解析每个 skill 的基础信息（名称、描述、类型）
3. 构建树状结构（基于目录层级）
4. 生成 Markdown 格式能力清单（人类可读）
5. 生成 JSON 格式清单（机器可读）
6. 输出到 scan-results/ 目录
```

## 输入规范

| 类型 | 格式 | 说明 |
|------|------|------|
| 目录路径 | 绝对或相对路径 | 扫描的技能文件夹 |

## 输出规范

### 1. Markdown 能力清单（人类可读）
文件：`scan-results/skill-catalog.md`

### 2. JSON 清单（机器可读）
文件：`scan-results/skill-catalog.json`

## 10 分钟快速验证指南

1. **运行扫描器**（<2 分钟）
2. **检查 Markdown 输出**（<2 分钟）
3. **验证 JSON 格式**（<2 分钟）
4. **检查关键字段**（<2 分钟）
5. **对比目录结构**（<2 分钟）

**总耗时：≤ 10 分钟**

## Limitations
- 只负责扫描，不执行验证
- 依赖 SKILL.md 规范性
- 不反映依赖关系

## 使用方法
```bash
/skill-catalog-scanner /path/to/skills
```
