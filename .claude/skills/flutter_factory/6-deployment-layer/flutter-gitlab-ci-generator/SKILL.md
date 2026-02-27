---
name: flutter-gitlab-ci-generator
description: GitLab CI 配置
version: 1.0
category: deployment
---

# GitLab CI 生成器（GitLab CI Generator）

## Capabilities（单一职责）
- 根据 build spec 生成 .gitlab-ci.yml
- 配置构建、测试、部署阶段
- 支持缓存和 artifacts

## 执行流程（5 步骤）
1. 解析 build spec
2. 定义 CI stages
3. 配置构建任务
4. 添加测试和部署
5. 输出到 output/ci/.gitlab-ci.yml

## 10 分钟验证指南
运行生成器 → 查看 .gitlab-ci.yml → 验证 pipeline 配置

## Limitations
需要 GitLab Runner，首次执行可能失败
