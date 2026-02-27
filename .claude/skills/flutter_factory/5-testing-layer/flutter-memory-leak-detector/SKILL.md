---
name: flutter-memory-leak-detector
description: 内存泄漏检测
version: 1.0
category: testing
---

# 内存泄漏检测器（Memory Leak Detector）

## Capabilities（单一职责）
- 根据 profile 数据检测内存泄漏
- 分析对象生命周期
- 生成泄漏报告

## 执行流程（5 步骤）
1. 解析 profile 数据
2. 分析对象引用
3. 识别泄漏点
4. 生成报告
5. 输出到 output/memory/

## 10 分钟验证指南
运行检测器 → 分析报告 → 手动验证泄漏

## Limitations
依赖 DevTools，需要分析经验
