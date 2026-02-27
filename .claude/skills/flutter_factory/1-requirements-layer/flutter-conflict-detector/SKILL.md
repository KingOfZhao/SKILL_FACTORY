---
name: flutter-conflict-detector
description: 自动检测需求冲突
version: 1.0
category: requirements
---

# 需求冲突检测器（Conflict Detector）

## Capabilities（单一职责）
- 接收需求列表
- 分析需求之间的冲突关系
- 输出冲突报告和解决建议
- 支持多种冲突类型检测

## 执行前必须读取
common/underlying-convention.md

## MCP 依赖
无

## 执行流程（5 步骤）

```
1. 解析需求列表
2. 分析需求之间的关系
3. 检测冲突（互斥、依赖循环、资源冲突等）
4. 生成冲突报告
5. 输出到 output/conflict_report.json
```

## 输入规范

| 类型 | 格式 | 说明 |
|------|------|------|
| 需求列表 | JSON | 待检测的需求列表 |

需求列表示例：
```json
[
  {
    "id": "REQ-001",
    "title": "支持深色模式",
    "features": ["深色主题", "自动切换"],
    "priority": "high"
  },
  {
    "id": "REQ-002",
    "title": "固定浅色主题",
    "features": ["仅浅色主题"],
    "priority": "medium"
  },
  {
    "id": "REQ-003",
    "title": "A 功能",
    "dependencies": ["REQ-004"]
  },
  {
    "id": "REQ-004",
    "title": "B 功能",
    "dependencies": ["REQ-003"]
  }
]
```

## 输出规范

**冲突报告格式**：
```json
{
  "detected_at": "2026-02-27T15:30:00Z",
  "total_requirements": 4,
  "conflicts_found": 2,
  "conflicts": [
    {
      "id": "CONF-001",
      "type": "mutually_exclusive",
      "severity": "high",
      "description": "功能互斥冲突",
      "conflicting_requirements": ["REQ-001", "REQ-002"],
      "details": "REQ-001 要求支持深色模式，REQ-002 要求仅支持浅色主题",
      "resolution_suggestions": [
        "移除 REQ-002，保留 REQ-001（推荐）",
        "移除 REQ-001，保留 REQ-002",
        "修改为可选的深色模式切换"
      ]
    },
    {
      "id": "CONF-002",
      "type": "circular_dependency",
      "severity": "medium",
      "description": "依赖循环冲突",
      "conflicting_requirements": ["REQ-003", "REQ-004"],
      "details": "REQ-003 依赖 REQ-004，REQ-004 依赖 REQ-003",
      "resolution_suggestions": [
        "移除其中一个依赖",
        "引入中间层 C 功能",
        "将 A 和 B 功能合并"
      ]
    }
  ],
  "warnings": [],
  "statistics": {
    "mutually_exclusive": 1,
    "circular_dependency": 1,
    "resource_conflict": 0
  }
}
```

## 10 分钟快速验证指南

### 验证步骤

1. **运行冲突检测器**（<2 分钟）
   ```bash
   /flutter-conflict-detector requirements.json
   ```

2. **检查冲突报告**（<2 分钟）
   ```bash
   cat output/conflict_report.json | jq '.conflicts'
   ```
   预期：列出所有检测到的冲突

3. **验证冲突类型**（<3 分钟）
   ```bash
   jq '.conflicts[].type' output/conflict_report.json
   ```
   预期：显示 mutually_exclusive, circular_dependency 等类型

4. **手动检查报告准确性**（<3 分钟）
   - 仔细阅读每个冲突的 details
   - 确认冲突确实存在
   - 评估 resolution_suggestions 的合理性

**总耗时：≤ 10 分钟**

成功标志：
- conflicts 数量准确
- 冲突描述清晰
- 解决建议可行

### 失败场景

- **需求列表为空** → 错误："需求列表不能为空"
- **解析失败** → 错误："需求列表格式错误"
- **未检测到冲突** → 提示："未发现冲突"

## Limitations（必须声明）

- 本 Skill 只负责检测冲突，不自动修复
- 依赖需求信息的完整性
- 不考虑实际实现细节
- 冲突严重度为主观评估
- 解决建议仅供参考

## 使用方法

### 基本用法
```bash
/flutter-conflict-detector requirements.json
```

### 按严重度过滤
```bash
/flutter-conflict-detector requirements.json --severity high
```

### 仅显示高优先级冲突
```bash
/flutter-conflict-detector requirements.json --filter mutually_exclusive,circular_dependency
```

### 输出 Markdown 报告
```bash
/flutter-conflict-detector requirements.json --format markdown
```

## 输出文件位置
```
output/
└── conflict_report.json    # 冲突报告
```
