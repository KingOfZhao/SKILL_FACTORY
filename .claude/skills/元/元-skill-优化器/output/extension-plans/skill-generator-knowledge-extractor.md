# skill-generator 知识提取器 (skill-generator-knowledge-extractor)

## 描述
从 skill-generator 的生成历史中提取结构化知识，构建知识库。

## 提取类型

### 1. 模式提取
- 元认知模式
- 交互模式
- 验证模式

### 2. 模板提取
- SKILL.md 模板结构
- 脚本模板
- 输出格式模板

### 3. 最佳实践提取
- 常见的成功模式
- 常见的失败原因
- 优化技巧

### 4. MCP 关联提取
- 工具调用模式
- MCP 需求规律
- 集成最佳实践

## 使用方法

### 提取所有类型
```
/skill-generator-knowledge-extractor --all
```

### 指定提取类型
```
/skill-generator-knowledge-extractor --type patterns
/skill-generator-knowledge-extractor --type templates
/skill-generator-knowledge-extractor --type best-practices
```

### 更新知识库
```
/skill-generator-knowledge-extractor --update
```

## 输出格式

### 知识库结构
```json
{
  "metadata": {
    "version": "1.0",
    "extracted_at": "2026-02-26T22:00:00Z",
    "source_count": 10,
    "total_patterns": 45
  },
  "patterns": {
    "meta-cognitive": [
      {
        "id": "mc-001",
        "name": "树状无限穷举",
        "description": "横向（同层变体）+ 纵向（深度递进）的树状结构",
        "applicable_scenarios": ["生成类", "分析类"],
        "frequency": "high"
      }
    ],
    "interaction": [
      {
        "id": "in-001",
        "name": "模式选择询问",
        "description": "首次运行时强制询问模式选择",
        "applicable_scenarios": ["双模式 Skill"],
        "frequency": "medium"
      }
    ],
    "verification": [
      {
        "id": "v-001",
        "name": "10 分钟验证原则",
        "description": "10 分钟内可完成验证的快速检查",
        "applicable_scenarios": ["所有 Skill"],
        "frequency": "high"
      }
    ]
  },
  "templates": {
    "skill_md": {
      "structure": [
        "name", "description", "version",
        "Capabilities", "Input Specification",
        "Output Specification", "Limitations"
      ],
      "common_sections": [
        "使用方法", "10 分钟验证指南", "Limitations"
      ]
    },
    "scripts": {
      "bash_template": "set -euo pipefail\n\ncolors definition\n\n# main function",
      "error_handling": "error checking, cleanup"
    }
  },
  "best_practices": [
    {
      "category": "结构完整性",
      "practice": "单一职责原则",
      "description": "一个 Skill 只解决一个明确问题域",
      "anti_patterns": ["职责过多", "边界模糊"]
    },
    {
      "category": "可维护性",
      "practice": "400 行限制",
      "description": "SKILL.md 控制在 400 行以内",
      "anti_patterns": ["过长文档", "缺乏拆分"]
    }
  ],
  "mcp_associations": [
    {
      "capability": "图像分析",
      "required_mcp": "4.5v-mcp",
      "common_usage": "分析设计稿截图"
    },
    {
      "capability": "文件读写",
      "required_mcp": "local-files",
      "common_usage": "读取/保存配置和输出"
    }
  ]
}
```

### 知识分类索引
```
按类型索引:
  - 元认知模式 (meta-cognitive)
  - 交互模式 (interaction)
  - 验证模式 (verification)

按频率索引:
  - 高频 (high)
  - 中频 (medium)
  - 低频 (low)

按场景索引:
  - 生成类 Skill
  - 修复类 Skill
  - 分析类 Skill
  - 验证类 Skill
```

## 10 分钟验证指南

### 验证知识提取器

1. **运行提取器**（<2 分钟）
   ```bash
   /skill-generator-knowledge-extractor --all
   ```

2. **查看知识库**（<3 分钟）
   - 确认包含至少 3 个知识类别
   - 检查分类索引完整
   - 验证 JSON 格式正确

3. **验证知识质量**（<3 分钟）
   - 检查描述是否清晰
   - 确认适用场景合理
   - 验证反模式准确

4. **测试检索**（<2 分钟）
   - 搜索一个已知模式
   - 确认能正确检索
   - 检查返回结果完整

**总耗时：≤ 10 分钟**

成功标志：知识库 JSON 格式正确，且至少包含 10 个知识条目。

## Limitations

- 提取质量依赖生成历史数量
- 模糊或错误的模式难以识别
- 需要人工验证提取的知识
- 知识的适用性可能随时间降低
- 无法自动判断最佳实践的时效性
