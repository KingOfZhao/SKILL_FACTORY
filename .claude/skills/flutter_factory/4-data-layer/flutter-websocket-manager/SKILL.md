---
name: flutter-websocket-manager
description: WebSocket 实时连接管理
version: 1.0
category: data
---

# WebSocket 管理器（WebSocket Manager）

## Capabilities（单一职责）
- 根据端点 URL 生成 WebSocket 管理代码
- 处理连接、断开、重连
- 支持消息收发

## 执行流程（5 步骤）
1. 解析端点 URL
2. 生成 WebSocketChannel
3. 实现连接管理
4. 处理消息收发
5. 输出到 output/websocket/

## 10 分钟验证指南
运行管理器 → 连接测试 WebSocket → 验证消息收发

## Limitations
依赖 web_socket_channel 包，需服务端配合
