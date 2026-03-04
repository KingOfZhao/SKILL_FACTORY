---
name: 元-Skill推荐器
description: 基于问题类型和上下文，自动推荐最优的技能组合
version: 1.0
author: 元-skill-orchestrator
---

# 元-Skill推荐器 (Skill Recommendation Engine)

## Capabilities（单一职责）

- **智能领域推断**: 根据问题描述自动推断问题领域（支持 13 个领域）
- **技能推荐**: 基于领域和问题类型推荐最相关的技能组合
- **回退机制**: 当没有特定领域技能时，智能推荐合适的元技能组合
- **依赖分析**: 分析技能间的依赖关系，检测循环依赖
- **执行顺序规划**: 提供技能调用的最优顺序建议
- **置信度评估**: 评估推荐结果的置信度
- **执行时间预估**: 预估技能组合的执行时间

## 执行前必须读取

common/underlying-convention.md

## MCP 依赖声明

- filesystem（必需）
- local-files（备选）

## 输入规范

### 问题描述（必需）
```
问题描述: 自由文本，描述需要解决的问题或任务
示例: "蓝牙连接不稳定，需要实现指数退避和自适应超时策略"
```

### 问题领域（可选）
```
问题领域: 指定问题所属的领域
支持: bluetooth, rssi, performance, algorithm, network, database, ui_ux,
       security, testing, optimization, general
```

## 输出规范

### Markdown 格式报告
```
# 技能推荐报告

## 问题分析
- 问题描述: [问题描述]
- 问题领域: [推断的领域]

## 推荐技能
[技能列表]

## 执行顺序
[技能调用顺序]

## 推荐理由
[推荐依据]

## 置信度和预估
- 置信度: [0-1]
- 预估执行时间: [分钟]

## 依赖检查
[技能依赖关系分析]
```

### JSON 格式导出
```json
{
  "timestamp": "ISO 8601 时间戳",
  "recommendations": [
    {
      "skills": [{技能详情}],
      "reasoning": "推荐理由",
      "confidence": 0.8,
      "estimated_duration": 15.0,
      "execution_order": ["技能1", "技能2"]
    }
  ]
}
```

## 10 分钟快速验证指南

1. **运行示例测试**（2 分钟）
   ```bash
   python3 skill_recommender.py
   ```
   验证示例输出是否包含 3-5 个推荐技能

2. **检查领域推断**（2 分钟）
   - 输入蓝牙相关问题，验证是否推断为 "bluetooth" 领域
   - 输入优化相关问题，验证是否推断为 "optimization" 领域

3. **验证回退机制**（3 分钟）
   - 输入无对应领域技能的问题
   - 验证是否推荐了合适的元技能组合

4. **检查依赖分析**（2 分钟）
   - 验证依赖关系分析是否正确
   - 检查循环依赖检测是否正常工作

5. **验证报告格式**（1 分钟）
   - Markdown 报告格式是否正确
   - JSON 导出是否包含所有必需字段

## 使用方法

### 命令行使用
```bash
python3 skill_recommender.py
```

### Python API 使用
```python
from skill_recommender import SkillRecommender

# 初始化
recommender = SkillRecommender("/path/to/skills")

# 推荐技能
recommendation = recommender.recommend_skills(
    "蓝牙连接不稳定，需要实现指数退避和自适应超时策略"
)

# 生成报告
report = recommender.generate_recommendation_report(recommendation)
print(report)

# 导出 JSON
recommender.export_recommendations_to_json(
    [recommendation],
    "/path/to/output.json"
)
```

### 指定领域
```python
recommendation = recommender.recommend_skills(
    "优化性能",
    problem_domain="optimization"
)
```

## 支持的问题领域

| 领域 | 关键词 |
|--------|---------|
| bluetooth | 蓝牙, 连接, 设备, scan |
| rssi | rssi, signal, 信号, 图表, chart, 实时 |
| performance | 性能, 优化, 卡顿, 内存, fps |
| algorithm | 算法, 排序, 搜索, tree, dp, 动态规划 |
| network | 网络, http, 请求, api, 接口 |
| database | 数据库, db, sql, 查询 |
| ui_ux | ui, 界面, design, 布局, 组件, widget |
| security | 安全, 认证, 加密, token |
| testing | 测试, qa, 质量, 单元测试 |
| optimization | 优化, 调优, 微服务, 异步, 缓存 |
| general | 其他通用问题 |

## 推荐的元技能组合

| 问题类型 | 推荐的元技能（按优先级） |
|----------|--------------------------|
| 优化/性能问题 | 问题穷举器 → 优化器 → 生成器 → 检查器 |
| 生成/实现问题 | 问题穷举器 → 生成器 → 检查器 |
| 检查/验证问题 | 问题穷举器 → 检查器 → 扫描器 |
| 修复问题 | 问题穷举器 → 修复器 → 检查器 |
| 通用问题 | 问题穷举器 → 生成器 → 检查器 → 扫描器 |

## Limitations（必须声明）

1. **技能数据库依赖**: 需要预先运行 元-skill-扫描器 生成技能数据库
2. **领域覆盖限制**: 目前支持 13 个领域，超出范围的查询将使用通用推荐
3. **技能能力解析**: 技能能力（capabilities）未从 SKILL.md 解析，目前为空
4. **依赖关系提取**: 简单关键字匹配，可能遗漏复杂的依赖关系
5. **置信度估算**: 基于简单启发式算法，可能与实际需求存在偏差
6. **执行时间预估**: 基于经验值，实际执行时间可能有显著差异

## 示例输出

```
# 技能推荐报告

## 问题分析
- 问题描述: 蓝牙连接不稳定，需要实现指数退避和自适应超时策略
- 问题领域: bluetooth

## 推荐技能

推荐 5 个技能：

### 1. 元-Skill问题穷举器
- **类型**: meta_skill
- **类别**: enumerator
- **路径**: .claude/skills/元/元-skill-问题穷举器/
- **描述**: 对问题进行无限横向或纵向穷举
- **能力**:

### 2. 元-Skill优化器
- **类型**: meta_skill
- **类别**: optimizer
- **路径**: .claude/skills/元/元-skill-优化器/
- **描述**: 分析和优化技能
- **能力**:

## 执行顺序

元-Skill问题穷举器, 元-Skill优化器, 元-Skill生成器, 元-Skill检查器, 元-Skill扫描器

## 推荐理由

基于问题领域 'bluetooth' 的技能推荐：元-Skill问题穷举器, 元-Skill优化器, 元-Skill生成器

## 置信度和预估

- **置信度**: 0.49
- **预估执行时间**: 144.0 分钟

## 依赖检查

技能依赖关系分析：
- 元-Skill问题穷举器: 无直接依赖
- 元-Skill优化器: 无直接依赖
- 元-Skill生成器: 无直接依赖

循环依赖检测：
✓ 无循环依赖
```
