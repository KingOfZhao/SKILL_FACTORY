---
name: flutter-design-token-generator
description: 生成设计系统 Token
version: 1.0
category: ui
---

# Design Token 生成器（Design Token Generator）

## Capabilities（单一职责）
- 根据设计规范生成 DesignToken 类
- 定义颜色、字体、间距等 Token
- 输出可复用的 Token 代码

## 执行流程（5 步骤）
1. 解析设计规范
2. 定义颜色 Token
3. 定义字体 Token
4. 定义间距 Token
5. 输出到 output/tokens/

## 10 分钟验证指南
运行生成器 → 检查 output/tokens/design_tokens.dart → 验证 Token 可编译

## Limitations
只生成 Token 类，不实际应用
