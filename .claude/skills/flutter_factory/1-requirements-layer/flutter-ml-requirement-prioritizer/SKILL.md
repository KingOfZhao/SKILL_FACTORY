---
name: flutter-ml-requirement-prioritizer
description: 使用 ML 自动预测需求优先级
version: 1.0
category: requirements
---

# ML 需求优先级预测器（ML Requirement Prioritizer）

## Capabilities（单一职责）
- 接收需求列表和历史数据
- 使用 ML 模型预测需求优先级
- 输出加权优先级排序列表
- 支持优先级调整建议

## 执行前必须读取
common/underlying-convention.md

## MCP 依赖
无（可选：ML inference MCP）

## 执行流程（5 步骤）

```
1. 解析需求列表和历史数据
2. 提取需求特征（复杂度、依赖、价值）
3. 应用 ML 模型计算优先级分数
4. 生成加权优先级排序
5. 输出到 output/priority_list.json
```

## 输入规范

| 类型 | 格式 | 说明 |
|------|------|------|
| 需求列表 | JSON/CSV | 待排序的需求列表 |
| 历史数据 | JSON（可选） | 用于模型训练/调整的历史优先级数据 |

需求列表示例：
```json
[
  {
    "id": "REQ-001",
    "title": "用户注册",
    "description": "支持用户邮箱/手机注册",
    "estimated_hours": 8,
    "dependencies": []
  },
  {
    "id": "REQ-002",
    "title": "商品搜索",
    "description": "支持关键词和分类搜索",
    "estimated_hours": 16,
    "dependencies": ["REQ-001"]
  }
]
```

## 输出规范

**优先级列表格式**：
```json
{
  "prioritized_at": "2026-02-27T15:30:00Z",
  "total_requirements": 2,
  "priorities": [
    {
      "id": "REQ-001",
      "title": "用户注册",
      "priority_score": 0.95,
      "rank": 1,
      "category": "high",
      "reason": "基础功能，无依赖，价值高"
    },
    {
      "id": "REQ-002",
      "title": "商品搜索",
      "priority_score": 0.78,
      "rank": 2,
      "category": "medium",
      "reason": "依赖用户注册，功能价值中等"
    }
  ],
  "suggestions": [
    "建议优先实现 REQ-001（用户注册）"
  ]
}
```

## 10 分钟快速验证指南

### 验证步骤

1. **运行优先级预测器**（<2 分钟）
   ```bash
   /flutter-ml-requirement-prioritizer requirements.json
   ```

2. **检查输出列表**（<2 分钟）
   ```bash
   cat output/priority_list.json | jq '.priorities'
   ```
   预期：列表按 priority_score 降序排列

3. **验证排序合理性**（<3 分钟）
   - 检查 rank 字段是否从 1 开始
   - 检查 priority_score 是否与 reason 匹配

4. **对比手动排序**（<3 分钟）
   ```bash
   # 手动检查排序是否符合直觉
   jq '.priorities[] | "\(.rank): \(.title)"' output/priority_list.json
   ```

**总耗时：≤ 10 分钟**

成功标志：
- 排序 rank 连续且从 1 开始
- priority_score 与 reason 逻辑一致
- 依赖关系正确的需求排在前面

### 失败场景

- **需求列表为空** → 错误："需求列表不能为空"
- **ML 模型加载失败** → 错误："模型加载失败，请检查依赖"
- **分数计算异常** → 警告："部分需求分数异常，请人工审核"

## Limitations（必须声明）

- 本 Skill 只负责预测优先级，不强制执行
- ML 模型依赖历史数据，首次使用可能不准确
- 优先级分数仅供参考，需结合业务判断
- 不考虑资源约束（人力、时间）
- 依赖特征工程质量

## 使用方法

### 基本用法
```bash
/flutter-ml-requirement-prioritizer requirements.json
```

### 指定历史数据
```bash
/flutter-ml-requirement-prioritizer requirements.json --history historical.json
```

### 调整权重
```bash
/flutter-ml-requirement-prioritizer requirements.json --weight-value 0.5 --weight-complexity 0.3
```

### 仅输出高优先级
```bash
/flutter-ml-requirement-prioritizer requirements.json --filter high
```

## 输出文件位置
```
output/
└── priority_list.json    # 优先级排序列表
```
