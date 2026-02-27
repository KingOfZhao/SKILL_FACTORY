---
name: 元-skill-检查器
description: 检查所有非元-前缀的 skill 是否符合 10 分钟可验证原则
---

# 元-Skill 检查器

## 能力定义

扫描指定 skills 目录，识别所有不带"元-"前缀的 skill，并对每个 skill 验证是否符合 10 分钟可验证原则。

### 验证维度

1. **文件完整性**
   - 检查 SKILL.md 文件存在
   - 检查目录结构完整

2. **内容结构**
   - 检查 SKILL.md 包含"10 分钟快速验证指南"章节
   - 检查有明确的验证步骤（≤ 5 步）
   - 检查有时间约束说明（≤ 10 分钟）

3. **验证机制**
   - 检查是否有 verify.sh 或类似验证脚本
   - 检查是否有自校验机制（checksum、成功标志）

4. **失败处理**
   - 检查是否有清晰的失败场景说明
   - 检查是否有预期结果描述

5. **输出可验证性**
   - 检查输出格式是否可直接对比/检查
   - 检查是否有独立的快速验证指南

## 执行前必须读取
common/underlying-convention.md

## 执行流程（5 步骤）

```
1. 扫描 skills 目录，识别所有非元-前缀 skill
2. 对每个 skill 进行 5 维度验证
3. 收集验证结果（通过/警告/失败）
4. 生成 JSON 格式报告
5. 输出到 check-results/
```

## 输出格式

`check-results/skill-compliance-report.json`:

```json
{
  "timestamp": "2026-02-27T12:00:00Z",
  "total_skills": 5,
  "meta_skills_excluded": 4,
  "non_meta_skills_checked": 2,
  "summary": {
    "passed": 0,
    "warnings": 1,
    "failed": 1
  },
  "skills": [
    {
      "name": "skill-figma-html",
      "path": "/path/to/skill-figma-html",
      "status": "warning",
      "missing_items": [
        "verify.sh script not found",
        "failure scenarios not documented"
      ],
      "suggestions": [
        "Add verify.sh script for automated verification",
        "Document failure scenarios in SKILL.md"
      ]
    },
    {
      "name": "skill-优化er",
      "path": "/path/to/skill-优化er",
      "status": "failed",
      "missing_items": [
        "10-minute verification guide not found",
        "no success flag mechanism",
        "output format not clearly defined"
      ],
      "suggestions": [
        "Add '10 分钟快速验证指南' section to SKILL.md",
        "Implement success flag in output",
        "Define clear output verification steps"
      ]
    }
  ]
}
```

## 10 分钟快速验证指南

### 验证步骤

1. **运行检查器**（<2 分钟）
   ```bash
   /元-skill-检查器
   ```

2. **检查输出文件**（<2 分钟）
   ```bash
   cat check-results/skill-compliance-report.json | jq .
   ```

3. **验证 JSON 格式**（<2 分钟）
   ```bash
   jq empty check-results/skill-compliance-report.json
   ```

4. **检查必需字段**（<2 分钟）
   ```bash
   jq 'has("timestamp") and has("skills") and has("summary")' check-results/skill-compliance-report.json
   # 预期: true
   ```

5. **查看汇总结果**（<2 分钟）
   ```bash
   jq '.summary' check-results/skill-compliance-report.json
   ```

**总耗时：≤ 10 分钟**

成功标志：
- JSON 格式正确
- summary 字段包含 passed/warnings/failed
- skills 数组包含每个非元-skill 的验证结果

### 失败场景

- **skills 目录不存在** → 错误："指定目录不存在"
- **无权限访问** → 错误："权限不足"
- **JSON 生成失败** → 错误："报告生成失败"

## Limitations（必须声明）

- 本 Skill 只负责静态检查，不实际执行被检查的 skill
- 检查结果基于文件内容和结构分析，不验证实际运行效果
- 元-前缀的 skill 自动跳过检查（meta-skill 不受 10 分钟原则约束）
- 依赖 SKILL.md 内容的规范性
- 不修改被检查的 skill 文件

## 使用方法

### 基本用法
```bash
/元-skill-检查器
# 默认扫描: /Users/administruter/Desktop/skill_factory/.claude/skills/
```

### 指定目录
```bash
/元-skill-检查器 /path/to/skills
```

### 仅显示失败项
```bash
/元-skill-检查器 --failures-only
```

### 输出详细模式
```bash
/元-skill-检查器 --verbose
```
