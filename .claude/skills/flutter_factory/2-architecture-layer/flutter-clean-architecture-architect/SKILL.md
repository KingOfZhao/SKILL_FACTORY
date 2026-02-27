---
name: flutter-clean-architecture-architect
description: Clean Architecture 架构设计
version: 1.0
category: architecture
---

# Clean Architecture 架构师（Clean Architecture Architect）

## Capabilities（单一职责）
- 根据 app 类型/需求规划 Clean Architecture 结构
- 定义层次划分（Domain, Data, Presentation）
- 生成目录结构和依赖关系图
- 输出 Clean Architecture 规范文档

## 执行前必须读取
common/underlying-convention.md

## MCP 依赖
无

## 执行流程（5 步骤）

```
1. 分析 app 类型和需求复杂度
2. 定义 Clean Architecture 层次
3. 规划目录结构
4. 设计依赖规则
5. 输出到 output/clean_architecture/
```

## 输入规范

| 类型 | 格式 | 说明 |
|------|------|------|
| App 类型 | 字符串 | simple/medium/complex |
| 需求描述 | 文本 | 功能需求概述 |

示例：
```bash
/flutter-clean-architecture-architect medium
```

## 输出规范

**Clean Architecture 目录结构**：
```
lib/
├── domain/               # 领域层
│   ├── entities/         # 实体
│   ├── value_objects/    # 值对象
│   ├── repositories/     # 仓库接口
│   └── usecases/        # 用例
├── data/                # 数据层
│   ├── models/          # 数据模型
│   ├── repositories/     # 仓库实现
│   └── datasources/     # 数据源
└── presentation/        # 表现层
    ├── pages/           # 页面
    ├── widgets/         # 组件
    └── bloc/           # 状态管理
```

## 10 分钟快速验证指南

### 验证步骤

1. **运行架构师**（<2 分钟）
   ```bash
   /flutter-clean-architecture-architect medium
   ```

2. **检查目录结构**（<3 分钟）
   ```bash
   find output/clean_architecture -type d | sort
   ```
   预期：看到 domain, data, presentation 三个层级

3. **验证依赖规则**（<3 分钟）
   ```bash
   cat output/clean_architecture/dependency_rules.md
   ```
   预期：domain 不依赖任何层，data 可依赖 domain

4. **查看结构图**（<2 分钟）
   ```bash
   cat output/clean_architecture/architecture_diagram.md
   ```

**总耗时：≤ 10 分钟**

成功标志：
- 三层结构完整
- 依赖规则清晰
- 结构图可视化正确

## Limitations（必须声明）

- 本 Skill 只负责架构规划，不生成代码
- 依赖需求复杂度判断
- 不考虑第三方集成
- 目录结构可根据项目调整

## 使用方法
```bash
/flutter-clean-architecture-architect [simple|medium|complex]
```
