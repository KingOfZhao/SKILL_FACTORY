---
name: flutter-micro-frontend-planner
description: 微前端架构规划
version: 1.0
category: architecture
---

# 微前端规划器（Micro Frontend Planner）

## Capabilities（单一职责）
- 根据 feature 列表规划微前端架构
- 设计模块化结构
- 定义模块间通信机制
- 输出微前端规范文档

## 执行前必须读取
common/underlying-convention.md

## MCP 依赖
无

## 执行流程（5 步骤）

```
1. 分析 feature 列表
2. 划分微前端模块
3. 设计模块依赖关系
4. 定义通信机制
5. 输出到 output/micro_frontend/
```

## 输入规范

| 类型 | 格式 | 说明 |
|------|------|------|
| Feature 列表 | JSON | 功能模块列表 |

## 输出规范

**微前端模块结构**：
```
modules/
├── auth/               # 认证模块
├── product/            # 商品模块
├── cart/               # 购物车模块
└── order/              # 订单模块
```

## 10 分钟快速验证指南

### 验证步骤

1. **运行规划器**（<2 分钟）
2. **检查模块划分**（<3 分钟）
3. **验证依赖关系**（<3 分钟）
4. **查看通信机制**（<2 分钟）

**总耗时：≤ 10 分钟**

## Limitations
- 只负责架构规划，不生成代码
- 依赖 feature 列表质量
- 模块划分需人工审核
