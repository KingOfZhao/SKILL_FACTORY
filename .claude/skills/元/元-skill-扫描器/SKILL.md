---
name: 元-skill-扫描器
description: 扫描指定文件夹下的所有 skills，生成能力清单和树状结构，用于 Claude Code 读取和调用
version: 1.0
author: 元-skill-生成器生成
---

# Skill 目录扫描器（Skill Catalog Scanner）

## Capabilities（单一职责）
- 扫描指定文件夹下的所有 skill 目录
- 解析每个 skill 的 SKILL.md 和 description.md
- 生成统一的 skill 能力清单（包含路径、名称、能力描述）
- 输出树状 skill 结构图
- 生成 JSON 格式清单，供 Claude Code 程序化读取和调用

## 执行前必须读取
common/underlying-convention.md

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
| 可选选项 | `--json-only` | 仅输出 JSON 格式 |

示例：
```bash
/元-skill-目录扫描器 /path/to/skills
/元-skill-目录扫描器 .claude/skills/元/
/元-skill-目录扫描器 .claude/skills/元/ --json-only
```

## 输出规范

### 1. Markdown 能力清单（人类可读）
文件：`scan-results/skill-catalog.md`

格式：
```markdown
# Skill 目录扫描报告

## 扫描概览
- 扫描路径：[路径]
- 扫描时间：[时间戳]
- 总技能数：[数量]

## 树状结构
```
.claude/skills/元/
├── 元-skill-生成器
│   ├── SKILL.md
│   ├── description.md
│   └── common/
└── 元-skill-检查器
    └── SKILL.md
```

## 能力清单

| 路径 | 名称 | 能力描述 | 类型 | 状态 |
|------|------|---------|------|------|
| .claude/skills/元/元-skill-生成器 | 元-Skill生成器 | 基于规则自动生成新技能 | meta | active |
| .claude/skills/元/元-skill-检查器 | 元-Skill检查器 | 验证技能是否符合10分钟原则 | meta | active |
```

### 2. JSON 清单（机器可读）
文件：`scan-results/skill-catalog.json`

格式：
```json
{
  "scan_info": {
    "path": "/path/to/skills",
    "timestamp": "2026-02-27T15:30:00Z",
    "total_skills": 5
  },
  "tree_structure": {
    "name": "skills",
    "children": [
      {
        "name": "元",
        "path": ".claude/skills/元",
        "children": [
          {
            "name": "元-skill-生成器",
            "path": ".claude/skills/元/元-skill-生成器",
            "has_skill_file": true,
            "type": "meta",
            "description": "基于规则自动生成新技能"
          }
        ]
      }
    ]
  },
  "skills_list": [
    {
      "path": ".claude/skills/元/元-skill-生成器",
      "name": "元-Skill生成器",
      "name_en": "元-skill-生成器",
      "type": "meta",
      "category": "generator",
      "description": "基于规则自动生成新技能",
      "has_description": true
    }
  ]
}
```

## MCP 依赖
- **文件系统 MCP**（local-files 或 filesystem）：必须预先连接，用于读取 SKILL.md 文件

## 10 分钟快速验证指南

### 验证步骤

1. **运行扫描器**（<2 分钟）
   ```bash
   /元-skill-目录扫描器 .claude/skills/元/
   ```

2. **检查 Markdown 输出**（<2 分钟）
   ```bash
   cat scan-results/skill-catalog.md
   ```
   预期：看到树状结构和能力清单表格

3. **验证 JSON 格式**（<2 分钟）
   ```bash
   jq . scan-results/skill-catalog.json
   ```
   预期：JSON 格式正确，可解析

4. **检查关键字段**（<2 分钟）
   ```bash
   jq '.scan_info.total_skills' scan-results/skill-catalog.json
   ```
   预期：显示实际扫描到的 skill 数量

5. **对比目录结构**（<2 分钟）
   ```bash
   find .claude/skills/元/ -name "SKILL.md" | wc -l
   jq '.skills_list | length' scan-results/skill-catalog.json
   ```
   预期：两个数字应该相等

**总耗时：≤ 10 分钟**

成功标志：
- Markdown 文件包含完整的树状结构和表格
- JSON 文件格式正确，包含 scan_info、tree_structure、skills_list 三个字段
- total_skills 和 skills_list.length 相等

### 失败场景

- **目标目录不存在** → 错误："指定目录不存在"
- **无 SKILL.md 文件** → 警告："未发现任何 skill"
- **JSON 解析失败** → 错误："JSON 格式错误"
- **MCP 未连接** → 错误："文件系统 MCP 未连接"

## Limitations（必须声明）

- 本 Skill 只负责扫描和生成清单，不执行 skill 内容验证
- 依赖 SKILL.md 文件内容的规范性（必须包含 name 和 description 字段）
- 不修改被扫描的 skill 文件
- 扫描深度受文件系统权限限制
- JSON 输出基于解析 SKILL.md 头部信息，复杂内容可能解析不完整
- 树状结构基于实际目录层级，不反映 skill 之间的依赖关系

## 使用方法

### 基本用法
```bash
/元-skill-目录扫描器 /path/to/skills
```

### 扫描元-skills
```bash
/元-skill-目录扫描器 .claude/skills/元/
```

### 仅输出 JSON（供程序调用）
```bash
/元-skill-目录扫描器 .claude/skills/元/ --json-only
```

### 指定输出目录
```bash
/元-skill-目录扫描器 .claude/skills/元/ --output /custom/output/path
```

## Claude Code 调用示例

```python
# 读取 skill 清单
catalog = read_json("scan-results/skill-catalog.json")

# 遍历所有 skills
for skill in catalog['skills_list']:
    print(f"路径: {skill['path']}")
    print(f"名称: {skill['name']}")
    print(f"能力: {skill['description']}")

# 按类型筛选
meta_skills = [s for s in catalog['skills_list'] if s['type'] == 'meta']
```

## 输出文件位置
```
scan-results/
├── skill-catalog.md      # Markdown 清单（人类可读）
└── skill-catalog.json    # JSON 清单（机器可读）
```
