# Skill 性能分析器 (Skill-Profiler)

## 描述
分析 Skill 的执行性能，识别瓶颈并提供优化建议。

## 分析维度

### 1. 执行时间分析
- 脚本启动时间
- 各函数执行时间
- 总执行时间
- 分阶段耗时

### 2. 文件 I/O 统计
- 文件读取次数
- 文件写入次数
- I/O 等待时间
- 大文件操作记录

### 3. 内存使用
- 峰值内存
- 平均内存
- 内存增长趋势

### 4. 瓶颈识别
- 慢速操作列表
- I/O 密集型操作
- CPU 密集型操作

## 使用方法

### 基本性能分析
```
/skill-性能分析器 <skill-path>
```

### 分析特定脚本
```
/skill-性能分析器 <skill-path> --script scripts/main.sh
```

### 生成性能报告
```
/skill-性能分析器 <skill-path> --report
```

### 对比模式
```
/skill-性能分析器 <skill-path> --compare <version-a> <version-b>
```

## 输出格式

### 性能报告
```json
{
  "skill_path": "path/to/skill",
  "timestamp": "2026-02-26T21:40:00Z",
  "execution_time": {
    "total": 2.5,
    "startup": 0.3,
    "main": 1.8,
    "cleanup": 0.4
  },
  "file_io": {
    "reads": 15,
    "writes": 8,
    "total_bytes": 524288,
    "wait_time": 0.5
  },
  "memory": {
    "peak_mb": 128,
    "average_mb": 64,
    "growth_trend": "stable"
  },
  "bottlenecks": [
    {
      "function": "process_large_file",
      "time": 0.8,
      "percentage": 44,
      "suggestion": "使用流式处理代替全量加载"
    },
    {
      "function": "json_parse",
      "time": 0.3,
      "percentage": 17,
      "suggestion": "使用更快的 JSON 解析器"
    }
  ],
  "optimization_score": 72
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

```bash
# 检测慢速函数（> 总时间的 10%）
if [[ $function_time -gt $((total_time * 10 / 100)) ]]; then
    BOTTLENECKS+=("$function")
fi

# 检测 I/O 密集操作
if [[ $io_wait_time -gt $((total_time * 30 / 100)) ]]; then
    SUGGESTION="考虑缓存或异步 I/O"
fi

# 检测内存泄漏
if [[ $memory_growth -gt 100 ]]; then
    WARNING="检测到可能的内存泄漏"
fi
```

## 优化建议模板

### I/O 优化
```
当前问题: 文件 I/O 耗时占比 35%

优化建议:
1. 合并多次小文件读取为一次大文件读取
2. 使用文件缓存减少重复读取
3. 考虑使用内存缓存频繁访问的内容

预期改进: I/O 时间减少 40%
```

### 算法优化
```
当前问题: process_data 函数耗时 60%

优化建议:
1. 将 O(n²) 算法优化为 O(n log n)
2. 使用更高效的数据结构（hash map 代替 list）
3. 提前终止不必要的循环

预期改进: 执行时间减少 50%
```

### 并行化优化
```
当前问题: 多个独立操作串行执行

优化建议:
1. 使用并行处理独立任务
2. 考虑多线程或异步处理
3. 批量处理代替逐个处理

预期改进: 总时间减少 30%
```

## 10 分钟验证指南

### 验证性能分析器

1. **运行性能分析**（<2 分钟）
   ```bash
   /skill-性能分析器 path/to/skill
   ```

2. **查看瓶颈列表**（<2 分钟）
   - 确认识别的瓶颈准确
   - 检查优化建议合理性

3. **应用一个优化**（<4 分钟）
   - 选择一个简单的优化建议
   - 修改代码
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
