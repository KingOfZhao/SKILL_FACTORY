---
name: flutter-firebase-app-distributor
description: Firebase 分发
version: 1.0
category: deployment
---

# Firebase 分发器（Firebase App Distributor）

## Capabilities（单一职责）
- 根据 app 包生成分发配置
- 集成 Firebase App Distribution
- 输出分发脚本

## 执行流程（5 步骤）
1. 解析 app 包
2. 配置 Firebase 项目
3. 生成分发脚本
4. 输出到 output/firebase/
5. 生成分发说明文档

## 10 分钟验证指南
运行分发器 → 查看配置 → 验证 Firebase 项目

## Limitations
依赖 Firebase CLI，需要项目权限
