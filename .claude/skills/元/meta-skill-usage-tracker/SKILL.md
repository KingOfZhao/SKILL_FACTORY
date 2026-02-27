---
name: meta-skill-usage-tracker
description: 元-Skill 使用统计，收集使用数据和反馈
---

# 元-Skill 使用追踪器（Meta-Skill Usage Tracker）

## Capabilities（单一职责）
- 统计元-Skill 的调用次数
- 分析使用模式
- 收集用户反馈
- 生成使用趋势报告

## 执行前必须读取
common/underlying-convention.md

## 执行流程（5 步骤）

```
1. 收集使用日志
2. 统计各元-Skill 的调用次数
3. 分析使用模式
4. 收集用户反馈
5. 生成使用报告
```

## 输入规范

| 类型 | 格式 | 说明 |
|------|------|------|
| 日志路径 | 字符串 | 使用日志路径 |
| 时间范围 | 字符串 | 统计的时间范围 |

## 输出规范

**使用报告**：
```json
{
  "report_time": "2026-02-27T18:30:00Z",
  "time_range": {
    "start": "2026-02-27T00:00:00Z",
    "end": "2026-02-27T23:59:59Z"
  },
  "usage_stats": {
    "total_calls": 1200,
    "unique_users": 45,
    "avg_calls_per_user": 26.7
    "busiest_hour": "14:00-15:00"
    "call_frequency": {
      "high": "每小时 80 次",
      "low": "每小时 10 次"
    }
  },
  "skill_usage": [
    {
      "skill_name": "元-skill-生成器",
      "calls": 300,
      "percentage": 25,
      "avg_calls_per_hour": 12.5,
      "trend": "stable",
      "peak_hours": ["14:00", "15:00", "16:00"]
    },
    {
      "skill_name": "元-skill-扫描器",
      "calls": 200,
      "percentage": 16.7,
      "avg_calls_per_hour": 8.3,
      "trend": "increasing",
      "peak_hours": ["09:00", "10:00", "18:00"]
    },
    {
      "skill_name": "元-skill-检查器",
      "calls": 150,
      "percentage": 12.5,
      "avg_calls_per_hour": 6.25,
      "trend": "decreasing",
      "peak_hours": ["10:00", "11:00"]
    },
    {
      "skill_name": "元-skill-优化器",
      "calls": 100,
      "percentage": 8.3,
      "avg_calls_per_hour": 4.17,
      "trend": "stable",
      "peak_hours": ["14:00", "15:00"]
    },
    {
      "skill_name": "元-skill-问题穷举器",
      "calls": 350,
      "percentage": 29.2,
      "avg_calls_per_hour": 14.6,
      "trend": "stable",
      "peak_hours": ["13:00", "14:00", "18:00"]
    }
  ],
  "user_feedback": {
    "total_feedback": 85,
    "satisfaction_rate": 4.2,
    "common_issues": [
      {
        "issue": "执行时间过长",
        "count": 12,
        "percentage": 14
      },
      {
        "issue": "输出格式不清晰",
        "count": 8,
        "percentage": 9
      },
      {
        "issue": "文档缺失",
        "count": 5,
        "percentage": 6
      }
    ],
    "improvement_suggestions": [
      "优化元-skill-扫描器的性能",
      "改进元-skill-检查器的输出格式",
      "完善文档和示例"
    ]
  },
  "summary": {
    "most_used_skill": "元-skill-问题穷举器",
    "least_used_skill": "元-skill-修复器",
    "overall_satisfaction": 4.2,
    "trend_analysis": "使用量稳定，需提升满意度"
  }
}
```

## 使用趋势类型

| 趋势类型 | 说明 | 检测方法 |
|--------|------|--------|
| stable | 使用量稳定 | 标准差 < 10% |
| increasing | 逐渐增加 | 最近 7 天持续上升 |
| decreasing | 逐渐减少 | 最近 7 天持续下降 |
| volatile | 波动大 | 标准差 > 30% |

## 10 分钟快速验证指南

### 验证步骤

1. **运行追踪器**（<2 分钟）
   ```bash
   /meta-skill-usage-tracker --logs /path/to/usage-logs
   ```

2. **检查使用统计**（<2 分钟）
   ```bash
   cat output/usage-report.json | jq .usage_stats
   # 预期: 看到总调用次数和分布
   ```

3. **查看技能使用排行**（<2 分钟）
   ```bash
   jq '.skill_usage | sort_by(-.calls)' output/usage-report.json
   # 预期: 使用最多的技能在前面
   ```

4. **检查用户反馈**（<2 分钟）
   ```bash
   jq '.user_feedback' output/usage-report.json
   # 预期: 看到满意度统计
   ```

5. **查看改进建议**（<2 分钟）
   ```bash
   jq '.user_feedback.improvement_suggestions' output/usage-report.json
   ```

**总耗时：≤ 10 分钟**

成功标志：
- 使用统计完整
- 技能使用排序正确
- 用户反馈分析到位

## Limitations（必须声明）
- 依赖日志记录的完整性
- 用户反馈需要手动收集
- 不自动发送反馈调查

## 使用方法

### 分析今日使用
```bash
/meta-skill-usage-tracker --date 2026-02-27
```

### 分析一周使用
```bash
/meta-skill-usage-tracker --range 7d
```

### 导出使用数据
```bash
/meta-skill-usage-tracker --export csv --output usage_data.csv
```

## 输出文件位置
```
output/
├── usage-report.json     # 使用报告
└── feedback-summary.json   # 用户反馈汇总
```
