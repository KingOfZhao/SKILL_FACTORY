# skill-generator 验证器 (skill-generator-validator)

## 描述
验证 skill-generator 生成的 Skill 是否符合质量和规范要求。

## 检测项目

### 结构完整性
- [ ] SKILL.md 存在且 < 400 行
- [ ] description.md 存在
- [ ] README.md 存在
- [ ] common/underlying-convention.md 存在（如需）
- [ ] scripts/ 目录存在（如需脚本）

### 内容验证
- [ ] 包含单一职责声明
- [ ] 包含 Capabilities 章节
- [ ] 包含 Limitations 章节
- [ ] 包含 10 分钟验证指南
- [ ] SKILL.md 格式正确（无 version 等不支持字段）

### 约定遵守
- [ ] 不修改 underlying-convention.md
- [ ] 不修改自身元文件
- [ ] 遵守命名约定（kebab-case）
- [ ] JSON I/O + 错误处理（如有脚本）

### MCP 关联
- [ ] MCP 需求声明清晰
- [ ] 工具调用符合 MCP 规范
- [ ] 依赖配置正确

## 使用方法

### 严格验证（完整检查）
```
/skill-generator-validator <skill-path> --strict
```

### 轻量检查（快速检查）
```
/skill-generator-validator <skill-path> --quick
```

### 批量验证
```
/skill-generator-validator /path/to/待应用-skill/ --batch
```

## 输出

### 验证报告格式
```json
{
  "skill_path": "path/to/skill",
  "timestamp": "2026-02-26T22:00:00Z",
  "status": "pass" | "fail" | "warning",
  "checks": {
    "structure": {
      "status": "pass",
      "items": [
        {"check": "SKILL.md 存在", "result": "pass"},
        {"check": "行数 < 400", "result": "pass", "actual": 350}
      ]
    },
    "content": {
      "status": "warning",
      "items": [
        {"check": "10 分钟验证指南", "result": "pass"},
        {"check": "单一职责声明", "result": "fail", "message": "缺少明确声明"}
      ]
    },
    "convention": {
      "status": "pass",
      "items": [
        {"check": "kebab-case 命名", "result": "pass"},
        {"check": "JSON I/O", "result": "pass"}
      ]
    },
    "mcp": {
      "status": "pass",
      "items": [
        {"check": "MCP 需求声明", "result": "pass"}
      ]
    }
  },
  "summary": {
    "total": 10,
    "passed": 8,
    "failed": 1,
    "warnings": 1
  },
  "recommendations": [
    "添加明确的单一职责声明",
    "改进 10 分钟验证指南的可操作性"
  ],
  "quality_score": 85
}
```

### 质量评分说明
| 分数 | 等级 | 说明 |
|-----|------|------|
| 90-100 | 优秀 | 无明显问题 |
| 70-89 | 良好 | 有少量改进空间 |
| 50-69 | 一般 | 存在明显问题 |
| <50 | 需优化 | 质量问题严重 |

## 10 分钟验证指南

### 验证验证器本身

1. **生成测试 Skill**（<2 分钟）
   运行 `skill-generator` 生成一个简单 Skill

2. **运行验证器**（<1 分钟）
   ```bash
   /skill-generator-validator /path/to/generated-skill --strict
   ```

3. **检查输出**（<2 分钟）
   - 确认 status 为 pass 或 warning
   - 查看失败的检查项
   - 阅读建议列表

4. **验证 JSON 格式**（<2 分钟）
   ```bash
   cat validation-report.json | jq empty
   ```

5. **对比验证**（<1 分钟）
   确认建议与实际检查结果一致

**总耗时：≤ 10 分钟**

成功标志：status 为 pass 或 warning，且 JSON 格式正确。

## Limitations

- 只验证静态文件，不执行代码
- 无法检测逻辑错误
- 需要人工确认建议的适用性
- 依赖底层约定的正确性
- 批量验证可能耗时较长
