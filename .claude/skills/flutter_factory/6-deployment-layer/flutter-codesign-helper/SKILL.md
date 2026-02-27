---
name: flutter-codesign-helper
description: 代码签名辅助
version: 1.0
category: deployment
---

# 代码签名助手（Codesign Helper）

## Capabilities（单一职责）
- 根据配置信息生成签名脚本
- 支持 Android/iOS 签名
- 输出签名配置

## 执行流程（5 步骤）
1. 解析配置信息
2. 生成签名脚本
3. 配置证书路径
4. 输出脚本到 output/codesign/
5. 生成签名说明文档

## 10 分钟验证指南
运行助手 → 模拟签名过程 → 验证脚本正确性

## Limitations
需要证书和密钥，仅生成脚本不执行
