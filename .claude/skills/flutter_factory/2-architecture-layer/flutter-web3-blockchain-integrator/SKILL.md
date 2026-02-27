---
name: flutter-web3-blockchain-integrator
description: Web3/区块链集成设计
version: 1.0
category: architecture
---

# Web3 集成设计师（Web3 Blockchain Integrator）

## Capabilities（单一职责）
- 根据链上需求设计 Web3 集成方案
- 定义智能合约接口
- 生成 DApp 架构
- 输出 Web3 集成规范

## 执行前必须读取
common/underlying-convention.md

## MCP 依赖
无

## 执行流程（5 步骤）

```
1. 解析链上需求
2. 选择区块链网络
3. 设计智能合约接口
4. 规划 DApp 架构
5. 输出到 output/web3/
```

## 输入规范

| 类型 | 格式 | 说明 |
|------|------|------|
| 链上需求 | JSON | 区块链功能需求 |

## 输出规范

**Web3 架构结构**：
```
lib/
├── web3/
│   ├── contracts/          # 合约接口
│   ├── providers/          # Web3 提供者
│   └── services/           # 链上服务
```

## 10 分钟快速验证指南

### 验证步骤

1. **运行设计师**（<2 分钟）
2. **检查合约接口**（<3 分钟）
3. **验证网络配置**（<3 分钟）
4. **查看集成架构**（<2 分钟）

**总耗时：≤ 10 分钟**

## Limitations
- 只设计集成方案，不实现合约
- 需要了解 Web3 基础
- 安全性需专业审核
