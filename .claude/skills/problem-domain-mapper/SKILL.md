---
name: problem-domain-mapper
description: 问题域到技能映射，智能推荐最相关的技能
---

# 问题域映射器（Problem Domain Mapper）

## Capabilities（单一职责）
- 分析问题描述的问题域
- 匹配最相关的技能
- 提供技能推荐列表
- 输出置信度评分

## 执行前必须读取
common/underlying-convention.md

## 执行流程（5 步骤）

```
1. 接收问题描述
2. 识别问题域关键词
3. 匹配技能库中的相关技能
4. 计算匹配置信度
5. 输出推荐列表
```

## 输入规范

| 类型 | 格式 | 说明 |
|------|------|------|
| 问题描述 | 纯文本 | 用户的问题描述 |

## 输出规范

**推荐报告**：
```json
{
  "mapping_time": "2026-02-27T18:30:00Z",
  "input_problem": "需要实现用户登录和购物车功能",
  "detected_domains": {
    "authentication": {
      "keywords": ["登录", "登录", "认证", "用户"],
      "confidence": 0.9
    },
    "e-commerce": {
      "keywords": ["购物车", "电商", "商品", "支付"],
      "confidence": 0.85
    }
  },
  "recommended_skills": [
    {
      "skill_name": "flutter-auth-manager",
      "domain": "authentication",
      "confidence": 0.9,
      "description": "Flutter 用户认证管理"
    },
    {
      "skill_name": "flutter-shopping-cart",
      "domain": "e-commerce",
      "confidence": 0.85,
      "description": "Flutter 购物车组件"
    },
    {
      "skill_name": "flutter-payment-integration",
      "domain": "e-commerce",
      "confidence": 0.8,
      "description": "Flutter 支付集成"
    }
  ],
  "summary": {
    "total_domains": 2,
    "total_recommendations": 3,
    "average_confidence": 0.85
  }
}
```

## 10 分钟快速验证指南

### 验证步骤

1. **运行映射器**（<2 分钟）
   ```bash
   /problem-domain-mapper "需要实现用户登录和购物车功能"
   ```

2. **检查推荐报告**（<2 分钟）
   ```bash
   cat output/recommendation-report.json | jq .recommended_skills
   # 预期: 看到 3 个推荐技能
   ```

3. **验证问题域识别**（<2 分钟）
   ```bash
   jq '.detected_domains' output/recommendation-report.json
   # 预期: 认证和电商两个域
   ```

4. **检查置信度**（<2 分钟）
   ```bash
   jq '.recommended_skills[].confidence' output/recommendation-report.json
   # 预期: 0.8-1.0 之间
   ```

5. **查看汇总**（<2 分钟）
   ```bash
   jq '.summary' output/recommendation-report.json
   ```

**总耗时：≤ 10 分钟**

成功标志：
- 推荐列表非空
- 置信度合理
- 问题域识别准确

## Limitations（必须声明）
- 依赖关键词匹配的准确性
- 推荐基于静态分析，不验证实际可用性
- 置信度需要人工审核

## 使用方法

### 基本推荐
```bash
/problem-domain-mapper "需要实现Flutter电商应用"
```

### 指定技能库路径
```bash
/problem-domain-mapper --skill-lib /path/to/skills "需要实现登录功能"
```

### 输出详细模式
```bash
/problem-domain-mapper --verbose "需要实现API集成"
```

## 输出文件位置
```
output/
└── recommendation-report.json    # 推荐报告
```
