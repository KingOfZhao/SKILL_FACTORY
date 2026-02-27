---
name: meta-skill-dependency-analyzer
description: 元-Skill 依赖关系分析，绘制技能依赖图
---

# 元-Skill 依赖关系分析器（Meta-Skill Dependency Analyzer）

## Capabilities（单一职责）
- 分析元-Skill 之间的依赖关系
- 识别循环依赖
- 生成依赖关系图
- 输出依赖可视化

## 执行前必须读取
common/underlying-convention.md

## 执行流程（5 步骤）

```
1. 扫描元-Skill 目录
2. 读取每个 SKILL.md 提取依赖信息
3. 构建依赖关系矩阵
4. 检测循环依赖
5. 生成依赖图
```

## 输入规范

| 类型 | 格式 | 说明 |
|------|------|------|
| 元-Skill 路径 | 字符串 | 元-Skill 目录路径 |

## 输出规范

**依赖关系矩阵**：
```json
{
  "analysis_time": "2026-02-27T18:30:00Z",
  "total_meta_skills": 6,
  "dependency_matrix": {
    "元-skill-生成器": {
      "depends_on": [],
      "required_by": ["元-skill-扫描器", "元-skill-检查器"],
      "depth": 1
    },
    "元-skill-扫描器": {
      "depends_on": ["元-skill-生成器"],
      "required_by": ["元-skill-检查器"],
      "depth": 2
    },
    "元-skill-检查器": {
      "depends_on": ["元-skill-生成器"],
      "required_by": ["元-skill-优化器"],
      "depth": 2
    },
    "元-skill-优化器": {
      "depends_on": ["元-skill-检查器"],
      "required_by": [],
      "depth": 3
    }
  },
  "circular_dependencies": [],
  "dependency_graph": {
    "nodes": [
      {"id": "生成器", "label": "元-skill-生成器"},
      {"id": "扫描器", "label": "元-skill-扫描器"},
      {"id": "检查器", "label": "元-skill-检查器"},
      {"id": "优化器", "label": "元-skill-优化器"}
    ],
    "edges": [
      {"from": "生成器", "to": "扫描器"},
      {"from": "生成器", "to": "检查器"},
      {"from": "扫描器", "to": "检查器"},
      {"from": "检查器", "to": "优化器"}
    ]
  }
}
```

**依赖图 ASCII 可视化**：
```text
元-skill-生成器 (depth 1)
├── 元-skill-扫描器 (depth 2)
│   └── 元-skill-检查器 (depth 2)
└── 元-skill-检查器 (depth 2)
    └── 元-skill-优化器 (depth 3)
```

## 10 分钟快速验证指南

### 验证步骤

1. **运行分析器**（<2 分钟）
   ```bash
   /meta-skill-dependency-analyzer
   ```

2. **检查依赖矩阵**（<2 分钟）
   ```bash
   cat output/dependency-report.json | jq '.dependency_matrix'
   # 预期: 看到 6 个元-Skill 的依赖
   ```

3. **验证循环依赖检测**（<2 分钟）
   ```bash
   jq '.circular_dependencies' output/dependency-report.json
   # 预期: 空数组
   ```

4. **查看依赖图**（<2 分钟）
   ```bash
   jq '.dependency_graph' output/dependency-report.json
   ```

5. **检查深度计算**（<2 分钟）
   ```bash
   jq '.dependency_matrix[] | .depth' output/dependency-report.json
   ```

**总耗时：≤ 10 分钟**

成功标志：
- 依赖矩阵完整
- 无循环依赖
- 依赖图正确

## Limitations（必须声明）
- 本 Skill 只负责分析依赖关系
- 不执行实际的依赖验证
- 依赖信息从 SKILL.md 提取

## 使用方法

### 分析所有元-Skills
```bash
/meta-skill-dependency-analyzer
```

### 分析指定目录
```bash
/meta-skill-dependency-analyzer /path/to/meta-skills/
```

### 输出可视化图
```bash
/meta-skill-dependency-analyzer --graph
```

## 输出文件位置
```
output/
├── dependency-report.json    # 依赖分析报告
└── dependency-graph.txt     # ASCII 依赖图
```
