---
name: skill-redundancy-detector
description: 技能冗余检测，识别功能重复的技能
---

# 技能冗余检测器（Skill Redundancy Detector）

## Capabilities（单一职责）
- 分析技能库中的功能重复
- 识别冗余技能
- 评估技能相似度
- 输出优化建议

## 执行前必须读取
common/underlying-convention.md

## 执行流程（5 步骤）

```
1. 扫描技能库
2. 提取每个技能的能力描述
3. 计算技能相似度
4. 识别冗余簇
5. 生成冗余报告
```

## 输入规范

| 类型 | 格式 | 说明 |
|------|------|------|
| 技能库路径 | 字符串 | 技能目录路径 |
| 相似度阈值 | 数字 | 相似度阈值（0-1） |

## 输出规范

**冗余报告**：
```json
{
  "detection_time": "2026-02-27T18:30:00Z",
  "total_skills": 50,
  "similarity_threshold": 0.85,
  "redundant_clusters": [
    {
      "cluster_id": "RC-001",
      "similarity": 0.92,
      "skills": [
        {
          "name": "flutter-login-page",
          "path": "ui/flutter-login",
          "description": "Flutter 登录页面组件"
        },
        {
          "name": "flutter-auth-component",
          "path": "auth/flutter-auth",
          "description": "Flutter 认证组件"
        }
      ],
      "recommendation": {
        "action": "merge",
        "target": "保留 flutter-login-page，合并 flutter-auth-component",
        "reason": "功能高度重叠，可以合并为一个通用认证技能"
      }
    },
    {
      "cluster_id": "RC-002",
      "similarity": 0.88,
      "skills": [
        {
          "name": "flutter-api-client-http",
          "path": "data/flutter-http-client",
          "description": "Flutter HTTP API 客户端"
        },
        {
          "name": "flutter-api-client-dio",
          "path": "data/flutter-dio-client",
          "description": "Flutter Dio API 客户端"
        }
      ],
      "recommendation": {
        "action": "consolidate",
        "target": "提供配置选项选择 HTTP 或 Dio",
        "reason": "实现相同功能，避免维护两套代码"
      }
    }
  ],
  "summary": {
    "total_redundant_clusters": 2,
    "redundant_skills": 4,
    "optimization_potential": 4
  }
}
```

## 10 分钟快速验证指南

### 验证步骤

1. **运行检测器**（<2 分钟）
   ```bash
   /skill-redundancy-detector --threshold 0.85
   ```

2. **检查冗余报告**（<2 分钟）
   ```bash
   cat output/redundancy-report.json | jq .redundant_clusters
   # 预期: 看到冗余簇
   ```

3. **验证相似度**（<2 分钟）
   ```bash
   jq '.redundant_clusters[].similarity' output/redundancy-report.json
   # 预期: 0.85-1.0
   ```

4. **查看优化建议**（<2 分钟）
   ```bash
   jq '.redundant_clusters[].recommendation' output/redundancy-report.json
   # 预期: 看到 merge 或 consolidate 建议
   ```

5. **检查汇总**（<2 分钟）
   ```bash
   jq '.summary' output/redundancy-report.json
   ```

**总耗时：≤ 10 分钟**

成功标志：
- 冗余簇识别准确
- 相似度计算合理
- 优化建议可执行

## Limitations（必须声明）
- 相似度基于文本和名称比较
- 不分析技能的实际代码实现
- 优化建议需要人工审核

## 使用方法

### 默认检测
```bash
/skill-redundancy-detector
```

### 指定相似度阈值
```bash
/skill-redundancy-detector --threshold 0.9
```

### 输出详细报告
```bash
/skill-redundancy-detector --verbose
```

## 输出文件位置
```
output/
└── redundancy-report.json    # 冗余检测报告
```
