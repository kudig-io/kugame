---
id: q003
type: fill_blank
difficulty: 3
category: storage
question: 查看所有PersistentVolume的命令是 kubectl ______ pv
answer: 
  - get
  - "get -A"
explanation: kubectl get pv 用于查看所有PV，加上 -A 可以查看所有命名空间的PV。
tags:
  - 命令
  - 存储
  - PV
related_commands:
  - kubectl get pv
  - kubectl get pvc
---
