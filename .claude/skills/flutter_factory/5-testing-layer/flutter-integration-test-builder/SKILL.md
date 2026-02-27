---
name: flutter-integration-test-builder
description: 集成测试框架
version: 1.0
category: testing
---

# 集成测试构建器（Integration Test Builder）

## Capabilities（单一职责）
- 根据驱动脚本生成集成测试
- 实现端到端测试
- 支持多场景测试

## 执行流程（5 步骤）
1. 解析驱动脚本
2. 生成测试用例
3. 实现页面导航
4. 添加断言
5. 输出到 output/integration/

## 10 分钟验证指南
运行构建器 → 执行 flutter drive → 验证测试结果

## Limitations
需要模拟器/真机，执行时间较长
