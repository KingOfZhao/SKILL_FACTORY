# Skill 验证器 (Skill-Validator)

## 描述
严格验证 Skill 配置的合规性，确保符合底层约定和最佳实践。

## 检测项目

### 结构完整性
- [ ] SKILL.md 存在
- [ ] description.md 存在
- [ ] README.md 存在
- [ ] scripts/ 目录存在（如有脚本）
- [ ] common/ 目录存在（如有底层约定）

### 命名约定
- [ ] 文件夹名称使用 kebab-case
- [ ] 文件名称使用 kebab-case
- [ ] SKILL.md 文件名准确

### 内容验证
- [ ] SKILL.md 行数 < 400
- [ ] 包含 Capabilities 章节
- [ ] 包含 Limitations 章节
- [ ] 包含 10 分钟验证指南

### 约定遵守
- [ ] 包含单一职责声明
- [ ] 遵守底层约定
- [ ] 不包含自我修改代码

## 使用方法

### 严格验证（完整检查）
```
/skill-验证器 <skill-path> --strict
```

### 轻量检查（快速检查）
```
/skill-验证器 <skill-path> --quick
```

### 增量验证（仅检查变更）
```
/skill-验证器 <skill-path> --incremental
```

## 输出

### 验证报告格式
```json
{
  "skill_path": "path/to/skill",
  "status": "pass" | "fail" | "warning",
  "checks": {
    "structure": {
      "status": "pass",
      "items": [...]
    },
    "naming": {
      "status": "pass",
      "items": [...]
    },
    "content": {
      "status": "warning",
      "items": [
        {
          "check": "SKILL.md 行数",
          "expected": "< 400",
          "actual": "450",
          "status": "fail"
        }
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
    "将 SKILL.md 拆分为多个文件",
    "添加 README.md",
    "修正文件命名"
  ]
}
```

## 10 分钟验证指南

1. **运行验证器**（<2 分钟）
   ```bash
   /skill-验证器 path/to/skill
   ```

2. **检查输出**（<3 分钟）
   - 确认状态为 pass 或 warning
   - 查看失败的检查项
   - 阅读建议列表

3. **修复问题**（<5 分钟）
   - 修复失败的检查项
   - 处理警告项

4. **重新验证**（<1 分钟）
   - 确认所有检查通过

**总耗时：≤ 10 分钟**

成功标志：status 为 pass 或 warning，且 fail 项为空。

## Limitations

- 只验证静态文件，不执行代码
- 无法检测逻辑错误
- 需要人工确认建议的适用性
- 依赖底层约定的正确性
