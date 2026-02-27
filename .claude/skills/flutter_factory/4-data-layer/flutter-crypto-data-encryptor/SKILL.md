---
name: flutter-crypto-data-encryptor
description: 敏感数据加密
version: 1.0
category: data
---

# 数据加密器（Crypto Data Encryptor）

## Capabilities（单一职责）
- 根据数据和密钥生成加密代码
- 使用 AES/加密算法
- 实现加解密接口

## 执行流程（5 步骤）
1. 解析数据和密钥
2. 选择加密算法
3. 生成加密代码
4. 实现解密代码
5. 输出到 output/crypto/

## 10 分钟验证指南
运行加密器 → 加密测试数据 → 解密验证结果

## Limitations
依赖 encrypt 包，密钥管理需额外考虑
