---
id: q001
type: single_choice
difficulty: 1
category: pod
question: Kubernetes中最小的部署单元是什么？
options:
  - A. Node
  - B. Pod
  - C. Container
  - D. Cluster
answer: B
explanation: Pod是Kubernetes中最小的部署单元，一个Pod可以包含一个或多个容器，它们共享网络和存储。
tags:
  - 基础
  - 概念
  - pod
related_commands:
  - kubectl get pods
  - kubectl describe pod
---

# 补充说明

Pod是Kubernetes的核心概念之一，理解Pod对于掌握Kubernetes至关重要。

## 相关概念

- **Container**: 容器是运行应用的实际环境
- **Pod**: 容器的封装，提供共享环境
- **Node**: 运行Pod的工作节点
- **Cluster**: 由多个Node组成的集群
