---
name: flutter-three-d-viewer-builder
description: 3D 模型查看器
version: 1.0
category: ui
---

# 3D 查看器构建器（3D Viewer Builder）

## Capabilities（单一职责）
- 根据 3D 模型文件生成 3D Widget
- 集成 flutter_3d 包
- 支持模型加载和渲染

## 执行流程（5 步骤）
1. 解析 3D 模型文件
2. 生成 3DWidget
3. 设置相机和灯光
4. 处理材质
5. 输出到 output/3d/

## 10 分钟验证指南
运行构建器 → 加载 3D 模型 → 验证渲染效果

## Limitations
依赖 3D 渲染包，性能取决于模型复杂度
