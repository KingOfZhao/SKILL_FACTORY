---
name: meta-skill-validator-advanced
description: 元-Skill 深度验证，检查元-Skill 自身的质量
---

# 元-Skill 高级验证器（Meta-Skill Validator - Advanced）

## Capabilities（单一职责）
- 验证元-Skill 的命名规范
- 检查 SKILL.md 结构完整性
- 验证 MCP 声明和使用一致性
- 评估元-Skill 的输出质量

## 执行前必须读取
common/underlying-convention.md

## 执行流程（5 步骤）

```
1. 读取元-Skill 目录
2. 解析 SKILL.md 头部信息
3. 执行命名规范检查
4. 执行 MCP 声明验证
5. 输出验证报告
```

## 输入规范

| 类型 | 格式 | 说明 |
|------|------|------|
| 元-Skill 路径 | 字符串 | 元-Skill 目录路径 |

## 输出规范

**验证报告**：
```json
{
  "validation_time": "2026-02-27T18:30:00Z",
  "meta_skill": "元-skill-检查器",
  "checks": [
    {
      "category": "naming",
      "check": "meta_prefix",
      "result": "pass",
      "details": "名称以'元-'开头"
    },
    {
      "category": "structure",
      "check": "skill_md_exists",
      "result": "pass",
      "details": "SKILL.md 文件存在"
    },
    {
      "category": "content",
      "check": "has_capabilities",
      "result": "pass",
      "details": "包含 Capabilities 章节"
    },
    {
      "category": "mcp",
      "check": "mcp_declared",
      "result": "pass",
      "details": "MCP 声明清晰"
    }
  ],
  "summary": {
    "total_checks": 4,
    "passed": 4,
    "warnings": 0,
    "failed": 0
  }
}
```

## 10 分钟快速验证指南

### 验证步骤

1. **运行验证器**（<2 分钟）
   ```bash
   /meta-skill-validator-advanced 元-skill-检查器
   ```

2. **检查验证报告**（<2 分钟）
   ```bash
   cat output/meta-validation-report.json | jq .summary
   # 预期: passed > 0
   ```

3. **查看检查项**（<2 分钟）
   ```bash
   jq '.checks[] | "\(.category): \(.result)"' output/meta-validation-report.json
   # 预期: 所有项都显示 pass
   ```

4. **验证 MCP 声明**（<2 分钟）
   ```bash
   grep -i "mcp" 元-skill-检查器/SKILL.md
   # 预期: 找到 MCP 声明
   ```

5. **检查豁免说明**（<2 分钟）
   ```bash
   grep -i "豁免\|exempt" 元-skill-检查器/SKILL.md
   # 预期: 有豁免 10 分钟验证的说明
   ```

**总耗时：≤ 10 分钟**

成功标志：
- summary.passed 大于 0
- 所有检查项都通过
- MCP 声明存在且正确

## Limitations（必须声明）
- 本 Skill 只负责元-Skill 验证
- 不验证普通 Skill
- 不执行元-Skill 功能

## 使用方法

### 验证单个元-Skill
```bash
/meta-skill-validator-advanced 元-skill-检查器
```

### 验证所有元-Skills
```bash
/meta-skill-validator-advanced /path/to/meta-skills/
```

### 输出详细模式
```bash
/meta-skill-validator-advanced 元-skill-检查器 --verbose
```

## 输出文件位置
```
output/
└── meta-validation-report.json    # 元-Skill 验证报告
```
