---
name: flutter-sqlite-optimizer
description: SQLite 数据库优化
version: 1.0
category: data
---

# SQLite 优化器（SQLite Optimizer）

## Capabilities（单一职责）
- 根据数据库文件生成优化建议
- 创建索引
- 优化查询语句

## 执行流程（5 步骤）
1. 分析数据库文件
2. 识别慢查询
3. 生成索引 SQL
4. 优化查询语句
5. 输出到 output/sqlite/

## 10 分钟验证指南
运行优化器 → 执行优化 SQL → 对比查询性能

## Limitations
只生成建议，需手动执行
