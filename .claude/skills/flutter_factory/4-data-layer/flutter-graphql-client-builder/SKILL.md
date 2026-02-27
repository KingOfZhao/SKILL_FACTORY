---
name: flutter-graphql-client-builder
description: GraphQL 客户端构建
version: 1.0
category: data
---

# GraphQL 客户端构建器（GraphQL Client Builder）

## Capabilities（单一职责）
- 根据 Schema 生成 GraphQL Client
- 支持查询、变更、订阅
- 集成 graphql_flutter 包

## 执行流程（5 步骤）
1. 解析 GraphQL Schema
2. 生成 Client 配置
3. 生成查询封装
4. 实现缓存策略
5. 输出到 output/graphql/

## 10 分钟验证指南
运行构建器 → 发送 GraphQL 查询 → 验证响应

## Limitations
依赖 graphql_flutter 包，需要 GraphQL Server
