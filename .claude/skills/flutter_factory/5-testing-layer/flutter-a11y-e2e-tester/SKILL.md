---
name: flutter-a11y-e2e-tester
description: 无障碍端到端测试
version: 1.0
category: testing
---

# 无障碍测试器（Accessibility E2E Tester）

## Capabilities（单一职责）
- 根据测试场景生成无障碍测试
- 支持 TalkBack/VoiceOver 测试
- 验证语义标签

## 执行流程（5 步骤）
1. 解析测试场景
2. 生成 a11y 测试
3. 检查语义标签
4. 验证导航顺序
5. 输出到 output/a11y/

## 10 分钟验证指南
运行测试器 → 启用 TalkBack → 验证无障碍

## Limitations
需要辅助功能，平台差异大
