---
name: flutter-golden-test-generator
description: 视觉回归测试
version: 1.0
category: testing
---

# Golden 测试生成器（Golden Test Generator）

## Capabilities（单一职责）
- 根据 Widget 代码生成 Golden 测试
- 创建快照对比
- 支持多平台 Golden

## 执行流程（5 步骤）
1. 解析 Widget 代码
2. 生成测试文件
3. 创建 Golden 文件
4. 实现对比逻辑
5. 输出到 output/golden/

## 10 分钟验证指南
运行生成器 → 执行 flutter test → 对比 Golden 文件

## Limitations
依赖 golden_toolkit 包，首次需生成 Golden
