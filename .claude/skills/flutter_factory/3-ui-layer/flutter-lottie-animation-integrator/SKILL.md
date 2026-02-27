---
name: flutter-lottie-animation-integrator
description: Lottie 动画集成
version: 1.0
category: ui
---

# Lottie 集成器（Lottie Animation Integrator）

## Capabilities（单一职责）
- 根据 Lottie JSON 生成 Widget 代码
- 集成 Lottie 包
- 支持动画控制接口

## 执行流程（5 步骤）
1. 解析 Lottie JSON
2. 生成 LottieWidget
3. 添加播放控制
4. 处理加载状态
5. 输出到 output/lottie/

## 10 分钟验证指南
运行集成器 → 运行 Lottie 动画 → 验证播放效果

## Limitations
依赖 lottie 包，需手动添加依赖
