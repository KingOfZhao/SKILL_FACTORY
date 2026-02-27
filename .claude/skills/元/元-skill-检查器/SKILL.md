---
name: 元-skill-检查器
description: 按照底层约定检查所有 Skill，自动区分元 Skill / 非元 Skill / 非 Skill 内容
---

# 元-Skill 检查器（v1.1）

## Capabilities（单一职责）
- 扫描指定目录
- 自动识别：元 Skill / 非元 Skill / 非 Skill 内容
- 严格按照 underlying-convention.md 中的 rules YAML 块进行检查
- 生成结构化合规报告

## 执行前必须读取
common/underlying-convention.md

## 执行流程（6 步骤）

```
1. 读取底层约定中的 rules YAML 块
2. 扫描目录，分类每个目录/文件：
   - 元 Skill（以 "元-" 开头或包含 meta 关键词）
   - 非元 Skill（普通技能）
   - 非 Skill 内容（其他文件/文件夹）
3. 对**非元 Skill** 执行完整 10 分钟验证检查
4. 对**元 Skill** 只检查命名、结构、MCP 声明等通用规则（豁免 10 分钟验证）
5. 对**非 Skill** 内容只做警告提示
6. 输出 JSON 报告 + Markdown 总结
```

## 分类判断逻辑

### 1. 元 Skill 识别
- 文件夹名称以 `元-` 开头
- SKILL.md 的 name/description 包含 `元`、`meta`、`生成器`、`enumerator`、`profiler`、`检查器`、`扫描器`、`穷举器`、`修复器`、`优化器` 等关键词
- **豁免范围**：10 分钟验证原则检查

### 2. 非元 Skill 识别
- 文件夹名称不以 `元-` 开头
- 不包含上述 meta 关键词
- **强制检查**：10 分钟验证原则（完整的 5 维度检查）

### 3. 非 Skill 内容识别
- 不含 SKILL.md 的目录
- 非 Markdown/代码文件
- **处理方式**：仅警告，不执行检查

## 输出格式（check-results/skill-compliance-report.json）

```json
{
  "scan_info": {
    "timestamp": "2026-02-27T16:30:00Z",
    "scan_path": "/path/to/skills",
    "total_items": 10
  },
  "classification": {
    "meta_skills": {
      "count": 5,
      "checked": true,
      "validation_mode": "basic_only"
    },
    "non_meta_skills": {
      "count": 3,
      "checked": true,
      "validation_mode": "full_10min_validation"
    },
    "non_skill_content": {
      "count": 2,
      "checked": false,
      "warning_only": true
    }
  },
  "rule_source": "underlying-convention.md",
  "summary": {
    "total_checked": 8,
    "passed": 6,
    "warnings": 1,
    "failed": 1
  },
  "skills": [
    {
      "item_name": "元-skill-生成器",
      "skill_type": "meta",
      "status": "passed",
      "checked_dimensions": ["naming", "structure", "mcp_declaration"],
      "violations": [],
      "exemptions": ["10min_validation"]
    },
    {
      "item_name": "skill-figma-html",
      "skill_type": "non_meta",
      "status": "warning",
      "checked_dimensions": ["file_integrity", "content_structure", "validation_mechanism", "failure_handling", "output_verifiability"],
      "violations": [
        "verify.sh script not found",
        "failure scenarios not documented"
      ],
      "exemptions": [],
      "suggestions": [
        "Add verify.sh script for automated verification",
        "Document failure scenarios in SKILL.md"
      ]
    }
  ],
  "non_skill_warnings": [
    {
      "item_name": "docs/",
      "warning": "Non-skill content detected, skipped"
    }
  ]
}
```

## 10 分钟快速验证指南

**本检查器自身为元 Skill，豁免 10 分钟验证原则**

### 验证步骤

1. **运行检查器**（<1 分钟）
   ```bash
   /元-skill-检查器
   # 默认扫描: /Users/administruter/Desktop/skill_factory/.claude/skills/
   ```

2. **查看 check-results/skill-compliance-report.json**（<3 分钟）
   ```bash
   cat check-results/skill-compliance-report.json | jq .
   ```

3. **查看 summary.passed / warnings / failed**（<1 分钟）
   ```bash
   jq '.summary' check-results/skill-compliance-report.json
   ```

4. **验证分类统计**（<2 分钟）
   ```bash
   jq '.classification' check-results/skill-compliance-report.json
   ```
   预期：meta_skills / non_meta_skills / non_skill_content 都有正确统计

5. **检查元 Skill 的豁免是否正确应用**（<3 分钟）
   ```bash
   jq '.skills[] | select(.skill_type=="meta") | .exemptions' check-results/skill-compliance-report.json
   ```
   预期：exemptions 包含 "10min_validation"

**总耗时：≤ 10 分钟**

成功标志：
- JSON 包含 skill_type 和 rule_source 字段
- classification 正确区分三类内容
- meta Skills 的 exemptions 包含 "10min_validation"
- non_meta Skills 执行了完整的 5 维度检查

### 失败场景

- **目标目录不存在** → 错误："指定目录不存在"
- **无权限访问** → 错误："权限不足"
- **JSON 生成失败** → 错误："报告生成失败"
- **底层约定读取失败** → 错误："无法读取 underlying-convention.md"

## Limitations（必须声明）

- 本 Skill 只负责静态检查，不执行 skill 实际功能
- 检查结果基于文件内容和结构分析，不验证实际运行效果
- 元 Skill 自动豁免 10 分钟验证原则
- 依赖底层约定中的 rules YAML 块准确性
- 不修改被检查的 skill 文件
- 非 Skill 内容仅警告，不执行检查

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

### 仅检查非元 Skill
```bash
/元-skill-检查器 --non-meta-only
```

## 输出文件位置
```
check-results/
└── skill-compliance-report.json    # 合规报告
```
