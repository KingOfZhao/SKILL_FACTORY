---
name: flutter-k8s-deployer
description: Kubernetes 部署
version: 1.0
category: deployment
---

# K8s 部署器（Kubernetes Deployer）

## Capabilities（单一职责）
- 根据 K8s spec 生成部署 YAML
- 配置 Service、Ingress
- 支持多副本和 HPA

## 执行流程（5 步骤）
1. 解析 K8s spec
2. 生成 Deployment YAML
3. 配置 Service
4. 添加 Ingress
5. 输出到 output/k8s/

## 10 分钟验证指南
运行部署器 → 查看 YAML → 验证 k8s 配置

## Limitations
需要 K8s 集群，配置需实际部署验证
