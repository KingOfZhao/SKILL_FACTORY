---
name: flutter-graphql-schema-designer
description: GraphQL schema 设计
version: 1.0
category: architecture
---

# GraphQL Schema 设计师（GraphQL Schema Designer）

## Capabilities（单一职责）
- 根据 API 需求设计 GraphQL schema
- 定义类型、查询、变更、订阅
- 输出 schema.graphql 文件
- 生成类型定义文档

## 执行前必须读取
common/underlying-convention.md

## MCP 依赖
无

## 执行流程（5 步骤）

```
1. 解析 API 需求
2. 定义类型系统
3. 设计查询和变更
4. 添加订阅（如需）
5. 输出到 output/graphql/
```

## 输入规范

| 类型 | 格式 | 说明 |
|------|------|------|
| API 需求 | JSON | API 功能列表 |

## 输出规范

**GraphQL Schema**：
```graphql
type Query {
  user(id: ID!): User
  products(filter: ProductFilter): [Product!]!
}

type Mutation {
  createUser(input: CreateUserInput!): User!
}

type Subscription {
  onProductUpdate: Product!
}
```

## 10 分钟快速验证指南

### 验证步骤

1. **运行设计师**（<2 分钟）
2. **验证 Schema 语法**（<3 分钟）
3. **检查类型定义**（<3 分钟）
4. **测试查询**（<2 分钟）

**总耗时：≤ 10 分钟**

## Limitations
- 只生成 schema，不实现 resolver
- 不处理复杂业务逻辑
- 需配合 GraphQL Server
