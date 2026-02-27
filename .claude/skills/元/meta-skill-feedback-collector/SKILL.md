---
name: meta-skill-feedback-collector
description: 元-Skill 反馈收集，用户反馈收集和分析
---

# 元-Skill 反馈收集器（Meta-Skill Feedback Collector）

## Capabilities（单一职责）
- 收集用户对元-Skill 的反馈
- 分析反馈情感和主题
- 分类反馈类型
- 生成反馈报告和改进建议

## 执行前必须读取
common/underlying-convention.md

## 执行流程（5 步骤）

```
1. 设计反馈表单
2. 收集用户反馈
3. 分析反馈内容
4. 分类反馈类型
5. 生成反馈报告
```

## 输入规范

| 类型 | 格式 | 说明 |
|------|------|------|
| 反馈表单 | JSON | 反馈收集配置 |

## 反馈类型

| 类型 | 说明 | 示例 |
|------|------|------|
| bug_report | 漏洞报告 | 执行失败、错误输出 |
| feature_request | 功能请求 | 希望添加的功能 |
| performance | 性能反馈 | 执行慢、资源占用高 |
| documentation | 文档反馈 | 文档不清晰、示例缺失 |
| usability | 易用性反馈 | 使用复杂、界面不友好 |
| enhancement | 改进建议 | 提升体验的想法 |

## 输出规范

**反馈报告**：
```json
{
  "collection_time": "2026-02-27T18:30:00Z",
  "feedback_form": {
    "skills": ["元-skill-生成器", "元-skill-扫描器", "元-skill-检查器", "元-skill-优化器"],
    "feedback_types": ["bug_report", "feature_request", "performance", "documentation", "usability", "enhancement"],
    "rating_scale": "1-5"
  },
  "collected_feedback": [
    {
      "id": "FB-001",
      "skill_name": "元-skill-生成器",
      "feedback_type": "feature_request",
      "user_id": "user-123",
      "timestamp": "2026-02-27T15:00:00Z",
      "rating": 4,
      "comment": "希望能支持从 Figma 文件直接生成 Flutter 代码",
      "priority": "medium",
      "status": "pending"
    },
    {
      "id": "FB-002",
      "skill_name": "元-skill-扫描器",
      "feedback_type": "performance",
      "user_id": "user-456",
      "timestamp": "2026-02-27T16:00:00Z",
      "rating": 2,
      "comment": "扫描 100 个技能需要超过 2 分钟，性能太慢",
      "priority": "high",
      "status": "in_review"
    }
  ],
  "analysis": {
    "total_feedback": 2,
    "by_type": {
      "bug_report": 0,
      "feature_request": 1,
      "performance": 1,
      "documentation": 0,
      "usability": 0,
      "enhancement": 0
    },
    "by_skill": {
      "元-skill-生成器": {
        "total": 1,
        "avg_rating": 4.0,
        "status_summary": "1 pending"
      },
      "元-skill-扫描器": {
        "total": 1,
        "avg_rating": 2.0,
        "status_summary": "1 in_review"
      }
    }
  },
  "recommendations": [
    {
      "skill": "元-skill-扫描器",
      "recommendation": "优化扫描算法，考虑增量扫描",
      "priority": "high"
    },
    {
      "skill": "元-skill-生成器",
      "recommendation": "支持 Figma 直接生成功能",
      "priority": "medium"
    }
  ],
  "summary": {
    "overall_rating": 3.0,
    "total_issues": 1,
    "high_priority": 1,
    "medium_priority": 1,
    "suggested_improvements": 2
  }
}
```

## 反馈评级标准

| 评分 | 描述 | 标准 |
|------|------|------|
| 1 | 非常不满意 | 严重问题，无法使用 |
| 2 | 不满意 | 主要问题，影响使用 |
| 3 | 一般 | 小问题，可以接受使用 |
| 4 | 满意 | 整体良好，有小建议 |
| 5 | 非常满意 | 完全符合预期，超出期望 |

## 10 分钟快速验证指南

### 验证步骤

1. **运行收集器**（<2 分钟）
   ```bash
   /meta-skill-feedback-collector --form feedback-form.json
   ```

2. **检查反馈报告**（<2 分钟）
   ```bash
   cat output/feedback-report.json | jq .summary
   # 预期: 看到总体评分和分类
   ```

3. **查看按类型统计**（<2 分钟）
   ```bash
   jq '.analysis.by_type' output/feedback-report.json
   # 预期: 看到各类型的数量分布
   ```

4. **查看改进建议**（<2 分钟）
   ```bash
   jq '.recommendations' output/feedback-report.json
   # 预期: 看到可执行的改进
   ```

5. **查看高优先级问题**（<2 分钟）
   ```bash
   jq '.collected_feedback[] | select(.priority=="high")' output/feedback-report.json
   # 预期: 看到高优先级反馈
   ```

**总耗时：≤ 10 分钟**

成功标志：
- 反馈报告完整
- 按类型统计准确
- 改进建议可执行

## Limitations（必须声明）
- 本 Skill 只负责收集和分析
- 不自动处理反馈
- 不发送用户通知
- 需要人工审核反馈

## 使用方法

### 收集单个反馈
```bash
/meta-skill-feedback-collector --skill 元-skill-生成器 --type feature_request \
  --comment "希望能支持 Figma 直接生成" --rating 4
```

### 批量导入反馈
```bash
/meta-skill-feedback-collector --import /path/to/feedback.json
```

### 查看所有反馈
```bash
/meta-skill-feedback-collector --list-all
```

### 导出反馈数据
```bash
/meta-skill-feedback-collector --export csv --output feedback.csv
```

## 输出文件位置
```
output/
├── feedback-report.json     # 反馈分析报告
└── feedback-logs.json       # 反馈收集日志
```
