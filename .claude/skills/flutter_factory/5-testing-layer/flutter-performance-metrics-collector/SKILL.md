---
name: flutter-performance-metrics-collector
description: 性能指标收集器
version: 1.0
category: testing
---

# 性能指标收集器（Performance Metrics Collector）

## Capabilities（单一职责）
- 根据 app 包收集性能指标
- 输出性能报告
- 支持多种指标类型

## 执行流程（5 步骤）
1. 解析 app 包
2. 运行性能测试
3. 收集指标数据
4. 生成报告
5. 输出到 output/metrics/

## 10 分钟验证指南
运行收集器 → 查看性能报告 → 验证指标数据

## Limitations
需要 DevTools，数据受运行环境影响
