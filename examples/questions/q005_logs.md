---
id: q005
type: command_complete
difficulty: 2
category: troubleshooting
question: 实时跟踪Pod nginx日志的命令是 kubectl logs nginx ______
answer: -f
explanation: |- 
  -f 参数表示"follow"，会持续跟踪日志输出。
  常用参数：
  - --tail=100：显示最后100行
  - --previous：查看上一次容器的日志
  - --timestamps：显示时间戳
  
  示例：kubectl logs nginx -f --tail=50
tags:
  - 日志
  - 排查
  - 命令
related_commands:
  - kubectl logs
  - kubectl exec
---
