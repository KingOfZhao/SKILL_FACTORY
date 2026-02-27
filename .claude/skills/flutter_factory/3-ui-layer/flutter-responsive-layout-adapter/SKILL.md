---
name: flutter-responsive-layout-adapter
description: 多端响应式适配
version: 1.0
category: ui
---

# 响应式适配器（Responsive Layout Adapter）

## Capabilities（单一职责）
- 根据基础布局生成响应式适配代码
- 支持多屏幕尺寸适配
- 输出 LayoutBuilder/MediaQuery 代码

## 执行流程（5 步骤）
1. 解析基础布局
2. 定义断点
3. 生成适配代码
4. 处理 overflow
5. 输出到 output/responsive/

## 10 分钟验证指南
运行适配器 → 在不同尺寸设备测试 → 验证布局正确性

## Limitations
只生成适配代码，需手动调整细节
