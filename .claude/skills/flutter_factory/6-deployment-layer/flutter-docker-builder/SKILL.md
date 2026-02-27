---
name: flutter-docker-builder
description: Docker 镜像构建
version: 1.0
category: deployment
---

# Docker 构建器（Docker Builder）

## Capabilities（单一职责）
- 根据 Dockerfile spec 生成 Dockerfile
- 配置多阶段构建
- 优化镜像大小

## 执行流程（5 步骤）
1. 解析 Dockerfile spec
2. 定义多阶段构建
3. 配置依赖和环境
4. 优化镜像层
5. 输出到 output/docker/Dockerfile

## 10 分钟验证指南
运行构建器 → 构建 Docker 镜像 → 验证镜像大小

## Limitations
需要 Docker 环境，镜像大小需实际测试
