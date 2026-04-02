[多选][中等][Deployment]

Deployment对象可以实现以下哪些功能？

A. 应用的声明式更新
B. 滚动更新和回滚
C. 自动扩缩容（配合HPA）
D. 服务发现和负载均衡

答案：ABC

解析：Deployment主要负责应用的部署、更新和扩缩容。
- A正确：Deployment使用声明式配置
- B正确：支持滚动更新和版本回滚
- C正确：可以与HPA配合实现自动扩缩容
- D错误：服务发现和负载均衡是Service的功能

**相关命令：**
```bash
kubectl create deployment nginx --image=nginx
kubectl rollout status deployment/nginx
kubectl rollout undo deployment/nginx
```

标签：Deployment, 功能, 进阶
