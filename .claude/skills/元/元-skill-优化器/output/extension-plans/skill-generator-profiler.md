# skill-generator 性能分析器 (skill-generator-profiler)

## 描述
分析 skill-generator 的执行性能，识别瓶颈并提供优化建议。

## 分析维度

### 1. 生成时间分析
- 完整生成流程时间
- 各步骤耗时（MCP 检查/穷举/生成/精炼）
- Token 消耗统计
- 上下文利用率

### 2. 输出质量分析
- 生成 Skill 的质量评分
- 认知精炼效果
- 模板复用率

### 3. 认知积累分析
- overlaps/ 增长速度
- 认知质量评估
- 重叠模式识别
- 提案价值分析

### 4. 瓶颈识别
- 慢速操作列表
- I/O 密集型操作
- Token 浪费点
- 并行化机会

## 使用方法

### 基本性能分析
```
/skill-generator-profiler /path/to/skill-generator
```

### 分析特定步骤
```
/skill-generator-profiler /path/to/skill-generator --step generation
/skill-generator-profiler /path/to/skill-generator --step refinement
```

### 对比历史版本
```
/skill-generator-profiler --compare v1.0 v1.2
```

### 分析认知积累
```
/skill-generator-profiler --cognitive
```

## 输出格式

### 性能报告
```json
{
  "generator_path": "/path/to/skill-generator",
  "timestamp": "2026-02-26T22:00:00Z",
  "version": "1.2",
  "execution_time": {
    "total": 45.2,
    "mcp_check": 2.3,
    "enumeration": 15.5,
    "generation": 18.2,
    "refinement": 9.2
  },
  "token_usage": {
    "total_tokens": 250000,
    "input_tokens": 50000,
    "output_tokens": 200000,
    "cache_tokens": 5000,
    "utilization": "85%"
  },
  "output_quality": {
    "average_quality_score": 82,
    "structure_compliance": 90,
    "content_completeness": 78,
    "cognitive_value": 85
  },
  "cognitive_accumulation": {
    "total_patterns": 45,
    "new_this_session": 8,
    "overlap_rate": "15%",
    "proposal_quality": "high"
  },
  "bottlenecks": [
    {
      "step": "generation",
      "time": 18.2,
      "percentage": 40,
      "suggestion": "使用模板预生成"
    },
    {
      "step": "refinement",
      "time": 9.2,
      "percentage": 20,
      "suggestion": "增量式精炼而非每次全量"
    },
    {
      "step": "token_efficiency",
      "time": "N/A",
      "percentage": 15,
      "suggestion": "优化提示词减少 token 消耗"
    }
  ],
  "optimization_score": 75,
  "parallelization_opportunities": [
    {
      "task": "multiple skill generation",
      "potential_speedup": "2x",
      "difficulty": "medium"
    },
    {
      "task": "cognitive pattern extraction",
      "potential_speedup": "1.5x",
      "difficulty": "low"
    }
  ]
}
```

### 性能评分说明
| 分数 | 等级 | 说明 |
|-----|------|------|
| 90-100 | 优秀 | 无明显瓶颈 |
| 70-89 | 良好 | 有少量优化空间 |
| 50-69 | 一般 | 存在明显瓶颈 |
| <50 | 需优化 | 性能问题严重 |

## 瓶颈检测规则

```python
# 检测慢速步骤（> 总时间的 20%）
if step_time > total_time * 0.2:
    bottlenecks.append(step_name)

# 检测 Token 浪费
cache_hit_rate = cache_tokens / total_tokens
if cache_hit_rate < 0.1:
    warning = "缓存命中率过低，建议启用缓存"

# 检测认知积累效率
new_patterns_per_minute = new_patterns / total_time
if new_patterns_per_minute < 0.2:
    warning = "认知积累效率低，建议优化"
```

## 优化建议模板

### 生成时间优化
```
当前问题: generation 步骤耗时占比 40%

优化建议:
1. 使用模板预生成
2. 缓存常用的模式定义
3. 分批次生成而非一次性

预期改进: 生成时间减少 30%
```

### Token 效率优化
```
当前问题: Token 消耗过高，利用率为 85%

优化建议:
1. 优化提示词结构
2. 减少重复内容
3. 使用更简洁的描述

预期改进: Token 消耗减少 20%
```

### 认知积累优化
```
当前问题: 新模式仅 8 个，重叠率 15%

优化建议:
1. 增强模式去重逻辑
2. 深度分析现有认知
3. 建立模式优先级

预期改进: 新模式增加 50%
```

## 并行化建议

```yaml
可并行化任务:
  多 Skill 生成:
    - 难度: 中等
    - 预期加速: 2-3 倍
    - 需要: 多线程或异步处理

  认知模式提取:
    - 难度: 低
    - 预期加速: 1.5 倍
    - 需要: 并行 I/O

  模板验证:
    - 难度: 低
    - 预期加速: 2 倍
    - 需要: 并行文件读取
```

## 10 分钟验证指南

### 验证性能分析器

1. **运行性能分析**（<3 分钟）
   ```bash
   /skill-generator-profiler /path/to/skill-generator
   ```

2. **查看瓶颈列表**（<2 分钟）
   - 确认识别的瓶颈准确
   - 检查优化建议合理性
   - 评估并行化机会

3. **应用一个优化**（<3 分钟）
   - 选择一个简单的优化建议
   - 修改代码或配置
   - 重新运行分析

4. **对比结果**（<2 分钟）
   - 对比优化前后的性能数据
   - 确认改进效果

**总耗时：≤ 10 分钟**

成功标志：优化后性能提升 >10%，且优化评分提高。

## Limitations

- 需要实际执行代码才能获取准确数据
- 不同环境下结果可能不同
- 优化建议基于通用规则，可能不适用
- 无法预测动态负载下的性能
- 认知质量评估为主观判断
