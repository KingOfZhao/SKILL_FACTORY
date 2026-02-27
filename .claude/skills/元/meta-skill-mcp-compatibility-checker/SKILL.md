---
name: meta-skill-mcp-compatibility-checker
description: MCP 兼容性检查，验证元-Skill 与 MCP 的集成正确性
---

# 元-Skill MCP 兼容性检查器（Meta-Skill MCP Compatibility Checker）

## Capabilities（单一职责）
- 验证元-Skill 的 MCP 需求声明
- 检查 MCP 使用优先应用规则
- 验证 MCP 检查机制
- 生成兼容性报告

## 执行前必须读取
common/underlying-convention.md

## 执行流程（5 步骤）

```
1. 读取元-Skill 的 SKILL.md
2. 提取 MCP 相关信息
3. 验证 MCP 声明完整性
4. 检查 MCP 优先应用规则
5. 输出兼容性报告
```

## 输入规范

| 类型 | 格式 | 说明 |
|------|------|------|
| 元-Skill 路径 | 字符串 | 元-Skill 目录路径 |

## 输出规范

**兼容性报告**：
```json
{
  "check_time": "2026-02-27T18:30:00Z",
  "meta_skill": "元-skill-问题穷举器",
  "mcp_analysis": {
    "has_mcp_section": true,
    "has_mcp_check": true,
    "declared_mcps": ["filesystem"],
    "mcp_priority_applied": true
  },
  "compliance": {
    "naming": {
      "status": "pass",
      "details": "元-Skill 命名符合规范"
    },
    "mcp_declaration": {
      "status": "pass",
      "details": "MCP 部分声明清晰"
    },
    "mcp_usage": {
      "status": "pass",
      "details": "使用优先应用规则明确"
    }
  },
  "recommendations": [
    "MCP 检查机制实现正确",
    "优先应用规则在执行时遵循"
  ],
  "summary": {
    "total_checks": 3,
    "passed": 3,
    "warnings": 0,
    "failed": 0
  }
}
```

## MCP 兼容性检查项

| 检查项 | 说明 | 状态 |
|--------|------|------|
| has_mcp_section | SKILL.md 是否有 MCP 部分 | pass/fail |
| has_mcp_check | 是否有 MCP 检查机制 | pass/fail |
| mcp_priority_applied | 是否优先应用已连接的 MCP | pass/fail |
| declared_mcps | 声明的 MCP 列表 | [MCP 名称] |
| mcp_check_errors | 检查错误列表 | [] |

## 10 分钟快速验证指南

### 验证步骤

1. **运行检查器**（<2 分钟）
   ```bash
   /meta-skill-mcp-compatibility-checker 元-skill-问题穷举器
   ```

2. **检查兼容性报告**（<2 分钟）
   ```bash
   cat output/mcp-compatibility-report.json | jq .summary
   # 预期: passed > 0
   ```

3. **查看 MCP 声明**（<2 分钟）
   ```bash
   jq '.mcp_analysis' output/mcp-compatibility-report.json
   ```

4. **验证优先应用规则**（<2 分钟）
   ```bash
   grep -i "优先应用" 元-skill-问题穷举器/SKILL.md
   # 预期: 找到相关说明
   ```

5. **检查建议项**（<2 分钟）
   ```bash
   jq '.recommendations' output/mcp-compatibility-report.json
   ```

**总耗时：≤ 10 分钟**

成功标志：
- summary.passed 大于 0
- MCP 检查项都通过
- 建议合理

## Limitations（必须声明）
- 本 Skill 只负责兼容性验证
- 不实际检查 MCP 连接状态
- 不修改元-Skill 文件

## 使用方法

### 检查所有元-Skills
```bash
/meta-skill-mcp-compatibility-checker
```

### 检查指定元-Skill
```bash
/meta-skill-mcp-compatibility-checker 元-skill-生成器
```

### 输出详细模式
```bash
/meta-skill-mcp-compatibility-checker --verbose
```

## 输出文件位置
```
output/
└── mcp-compatibility-report.json    # MCP 兼容性报告
```
