---
name: skill-gap-analyzer
description: 技能缺口分析，发现未被覆盖的需求领域
---

# 技能缺口分析器（Skill Gap Analyzer）

## Capabilities（单一职责）
- 分析现有技能库和需求对比
- 识别未被覆盖的需求领域
- 输出缺口报告
- 提供技能补充建议

## 执行前必须读取
common/underlying-convention.md

## 执行流程（5 步骤）

```
1. 读取需求列表或领域模型
2. 扫描现有技能库
3. 对比需求与技能覆盖
4. 识别覆盖缺口
5. 生成缺口报告
```

## 输入规范

| 类型 | 格式 | 说明 |
|------|------|------|
| 需求列表 | JSON | 功能需求列表 |
| 技能库路径 | 字符串 | 现有技能目录 |

## 输出规范

**缺口报告**：
```json
{
  "analysis_time": "2026-02-27T18:30:00Z",
  "requirements": {
    "total": 10,
    "domains": [
      "authentication", "payment", "data", "ui", "testing",
      "deployment", "documentation", "internationalization", "accessibility", "offline"
    ]
  },
  "coverage": {
    "covered_domains": 8,
    "coverage_rate": 0.8,
    "total_skills": 50
  },
  "gaps": [
    {
      "domain": "internationalization",
      "priority": "medium",
      "description": "缺少多语言支持和国际化能力",
      "suggested_skills": ["flutter-i18n-generator", "flutter-localization-helper"]
    },
    {
      "domain": "accessibility",
      "priority": "high",
      "description": "缺少无障碍支持和 a11y 测试技能",
      "suggested_skills": ["flutter-a11y-builder", "flutter-a11y-tester"]
    },
    {
      "domain": "offline",
      "priority": "medium",
      "description": "缺少离线支持和同步机制",
      "suggested_skills": ["flutter-offline-sync", "flutter-cache-manager"]
    }
  ],
  "summary": {
    "total_gaps": 3,
    "high_priority": 1,
    "medium_priority": 2,
    "suggested_skills": 6
  }
}
```

## 10 分钟快速验证指南

### 验证步骤

1. **运行分析器**（<2 分钟）
   ```bash
   /skill-gap-analyzer --requirements /path/to/requirements.json
   ```

2. **检查缺口报告**（<2 分钟）
   ```bash
   cat output/gap-report.json | jq .gaps
   # 预期: 看到 3 个缺口
   ```

3. **验证优先级**（<2 分钟）
   ```bash
   jq '.gaps[].priority' output/gap-report.json
   # 预期: high/medium/low
   ```

4. **检查覆盖率**（<2 分钟）
   ```bash
   jq '.coverage.coverage_rate' output/gap-report.json
   # 预期: 0.0-1.0
   ```

5. **查看建议**（<2 分钟）
   ```bash
   jq '.gaps[].suggested_skills' output/gap-report.json
   ```

**总耗时：≤ 10 分钟**

成功标志：
- 缺口报告包含明确的领域和优先级
- 覆盖率计算准确
- 建议技能具体可执行

## Limitations（必须声明）
- 依赖需求列表的质量
- 缺口分析基于静态对比
- 不验证建议技能的可行性

## 使用方法

### 基于需求列表分析
```bash
/skill-gap-analyzer --requirements /path/to/requirements.json
```

### 基于领域模型分析
```bash
/skill-gap-analyzer --domain-model /path/to/domains.json
```

### 指定技能库
```bash
/skill-gap-analyzer --skill-lib /path/to/skills --requirements /path/to/requirements.json
```

## 输出文件位置
```
output/
└── gap-report.json    # 缺口分析报告
```
