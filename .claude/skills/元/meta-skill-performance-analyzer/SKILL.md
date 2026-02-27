---
name: meta-skill-performance-analyzer
description: 元-Skill 性能分析，监控执行效率和资源使用
---

# 元-Skill 性能分析器（Meta-Skill Performance Analyzer）

## Capabilities（单一职责）
- 分析元-Skill 的执行效率
- 监控资源使用情况
- 计算性能指标（执行时间、吞吐量）
- 生成性能优化建议

## 执行前必须读取
common/underlying-convention.md

## 执行流程（5 步骤）

```
1. 收集元-Skill 执行日志
2. 分析执行时间分布
3. 计算性能指标
4. 识别性能瓶颈
5. 输出性能报告
```

## 输入规范

| 类型 | 格式 | 说明 |
|------|------|------|
| 日志路径 | 字符串 | 元-Skill 执行日志路径 |
| 分析时间范围 | 字符串 | 分析的时间范围 |

## 输出规范

**性能报告**：
```json
{
  "analysis_time": "2026-02-27T18:30:00Z",
  "time_range": {
    "start": "2026-02-27T00:00:00Z",
    "end": "2026-02-27T23:59:59Z"
  },
  "performance_metrics": {
    "total_executions": 150,
    "avg_execution_time_ms": 5200,
    "median_execution_time_ms": 4800,
    "p95_execution_time_ms": 8000,
    "max_execution_time_ms": 15000,
    "throughput_per_hour": 6
  },
  "skill_performance": [
    {
      "skill_name": "元-skill-生成器",
      "executions": 45,
      "avg_time_ms": 4500,
      "slowest_ms": 8000,
      "fastest_ms": 2000,
      "bottleneck": "文件 IO"
    },
    {
      "skill_name": "元-skill-扫描器",
      "executions": 30,
      "avg_time_ms": 1800,
      "slowest_ms": 3000,
      "fastest_ms": 1000,
      "bottleneck": "无"
    },
    {
      "skill_name": "元-skill-检查器",
      "executions": 25,
      "avg_time_ms": 6000,
      "slowest_ms": 10000,
      "fastest_ms": 3000,
      "bottleneck": "JSON 解析"
    }
  ],
  "bottleneck_analysis": {
    "common_bottlenecks": [
      "文件系统 IO",
      "JSON 序列化/反序列化",
      "MCP 连接延迟"
    ],
    "recommendations": [
      "优化元-skill-生成器的文件读取逻辑",
      "使用更高效的 JSON 库",
      "实现 MCP 连接池"
    ]
  },
  "summary": {
    "overall_performance": "good",
    "avg_efficiency": 82,
    "potential_improvement": "15%"
  }
}
```

## 性能指标说明

| 指标 | 说明 | 计算 |
|------|------|------|
| avg_execution_time_ms | 平均执行时间 | 总时间 / 执行次数 |
| median_execution_time_ms | 中位数执行时间 | 执行时间排序后取中间值 |
| p95_execution_time_ms | 95分位执行时间 | 95% 的请求完成时间 |
| throughput_per_hour | 吞吐量 | 每小时执行次数 |
| bottleneck | 性能瓶颈 | 最慢的操作类型 |

## 10 分钟快速验证指南

### 验证步骤

1. **运行分析器**（<2 分钟）
   ```bash
   /meta-skill-performance-analyzer --logs /path/to/logs
   ```

2. **检查性能报告**（<2 分钟）
   ```bash
   cat output/performance-report.json | jq .performance_metrics
   # 预期: 看到各项指标
   ```

3. **验证瓶颈分析**（<2 分钟）
   ```bash
   jq '.bottleneck_analysis.common_bottlenecks' output/performance-report.json
   # 预期: 看到常见瓶颈
   ```

4. **检查技能性能**（<2 分钟）
   ```bash
   jq '.skill_performance[] | select(.bottleneck != null)' output/performance-report.json
   # 预期: 识别有瓶颈的技能
   ```

5. **查看优化建议**（<2 分钟）
   ```bash
   jq '.bottleneck_analysis.recommendations' output/performance-report.json
   ```

**总耗时：≤ 10 分钟**

成功标志：
- 性能指标计算正确
- 瓶颈识别准确
- 优化建议可执行

## Limitations（必须声明）
- 依赖日志文件的质量和完整性
- 性能分析为历史数据，不实时监控
- 不执行实际的性能优化

## 使用方法

### 分析一天的性能
```bash
/meta-skill-performance-analyzer --logs /path/to/logs/2026-02-27
```

### 分析所有日志
```bash
/meta-skill-performance-analyzer --logs /path/to/logs/
```

### 输出详细报告
```bash
/meta-skill-performance-analyzer --verbose
```

## 输出文件位置
```
output/
└── performance-report.json    # 性能分析报告
```
