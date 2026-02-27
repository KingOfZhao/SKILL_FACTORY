---
name: flutter-background-sync-handler
description: 后台同步处理
version: 1.0
category: data
---

# 后台同步处理器（Background Sync Handler）

## Capabilities（单一职责）
- 根据同步队列生成后台同步 Worker
- 实现离线数据同步
- 处理冲突解决

## 执行流程（5 步骤）
1. 解析同步队列
2. 生成 SyncWorker
3. 实现同步逻辑
4. 处理冲突
5. 输出到 output/sync/

## 10 分钟验证指南
运行处理器 → 模拟离线操作 → 验证同步结果

## Limitations
依赖 workmanager 包，需网络连接
