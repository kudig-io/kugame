---
id: q006
type: short_answer
difficulty: 4
category: scheduling
question: 请解释Kubernetes中的资源请求（Request）和资源限制（Limit）的区别，以及为什么需要同时设置这两个值？
answer: >-
  Request是Pod启动时保证能够获得的资源量，用于调度决策。
  Limit是Pod能够使用的最大资源量，用于限制资源使用。
  
  需要同时设置的原因：
  1. Request确保Pod有足够资源运行
  2. Limit防止单个Pod占用过多资源影响其他Pod
  3. 提高集群资源利用率和稳定性
  
  配置示例：
  resources:
    requests:
      memory: "64Mi"
      cpu: "250m"
    limits:
      memory: "128Mi"
      cpu: "500m"
explanation: 这是Kubernetes资源管理的核心概念，理解Request和Limit的区别对于资源规划和集群稳定性至关重要。
tags:
  - 面试
  - 调度
  - 资源
  - 进阶
related_commands:
  - kubectl top pod
  - kubectl describe node
---
