---
name: flutter-hybrid-native-bridge-designer
description: Flutter-原生混合桥接设计
version: 1.0
category: architecture
---

# 混合桥接设计师（Hybrid Native Bridge Designer）

## Capabilities（单一职责）
- 根据原生模块列表设计桥接方案
- 生成 Platform Channel 代码
- 定义消息协议
- 输出桥接规范文档

## 执行前必须读取
common/underlying-convention.md

## MCP 依赖
无

## 执行流程（5 步骤）

```
1. 解析原生模块列表
2. 设计桥接接口
3. 生成 MethodChannel 代码
4. 定义消息格式
5. 输出到 output/bridge/
```

## 输入规范

| 类型 | 格式 | 说明 |
|------|------|------|
| 原生模块列表 | JSON | 需要桥接的模块 |

## 输出规范

**桥接代码结构**：
```
lib/
└── bridge/
    ├── native_bridge.dart      # 桥接主文件
    ├── auth_bridge.dart        # 认证桥接
    └── payment_bridge.dart     # 支付桥接
```

## 10 分钟快速验证指南

### 验证步骤

1. **运行设计师**（<2 分钟）
2. **检查桥接代码**（<3 分钟）
3. **验证 Channel 名称**（<3 分钟）
4. **测试消息格式**（<2 分钟）

**总耗时：≤ 10 分钟**

## Limitations
- 只生成桥接代码模板
- 不实现原生端代码
- 消息协议需双方约定
