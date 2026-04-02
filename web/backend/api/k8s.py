"""K8s Learning API Routes"""
from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List
from pydantic import BaseModel

router = APIRouter(prefix="/api/k8s", tags=["k8s"])


class CommandRequest(BaseModel):
    command: str
    namespace: str = "default"


# K8s 学习关卡
K8S_LEVELS = [
    {
        "id": "pods",
        "name": "Pod 基础",
        "description": "学习 Kubernetes 最基本的部署单元",
        "difficulty": 1,
        "rewards": {"exp": 100, "spirit_stones": 50},
        "objectives": [
            "了解什么是 Pod",
            "创建一个 Nginx Pod",
            "查看 Pod 状态",
        ],
    },
    {
        "id": "deployments",
        "name": "Deployment 管理",
        "description": "学习如何管理应用的部署和更新",
        "difficulty": 2,
        "rewards": {"exp": 200, "spirit_stones": 100},
        "objectives": [
            "创建 Deployment",
            "扩容副本数量",
            "执行滚动更新",
        ],
    },
    {
        "id": "services",
        "name": "Service 暴露",
        "description": "学习如何将应用暴露给外部访问",
        "difficulty": 2,
        "rewards": {"exp": 200, "spirit_stones": 100},
        "objectives": [
            "创建 ClusterIP Service",
            "创建 NodePort Service",
            "理解 Service 类型区别",
        ],
    },
    {
        "id": "configmaps",
        "name": "配置管理",
        "description": "学习 ConfigMap 和 Secret 的使用",
        "difficulty": 3,
        "rewards": {"exp": 300, "spirit_stones": 150},
        "objectives": [
            "创建 ConfigMap",
            "在 Pod 中使用 ConfigMap",
            "创建 Secret",
        ],
    },
]


@router.get("/levels")
async def get_levels():
    """获取 K8s 学习关卡"""
    return {
        "status": "success",
        "data": K8S_LEVELS,
    }


@router.get("/levels/{level_id}")
async def get_level(level_id: str):
    """获取特定关卡详情"""
    level = next((l for l in K8S_LEVELS if l["id"] == level_id), None)
    if not level:
        raise HTTPException(status_code=404, detail="关卡不存在")
    
    return {
        "status": "success",
        "data": level,
    }


@router.post("/execute")
async def execute_command(request: CommandRequest):
    """执行 K8s 命令（模拟）"""
    # 这里应该连接到真实的 K8s 集群或模拟环境
    # 现在返回模拟结果
    
    valid_commands = ["kubectl", "k", "helm"]
    cmd_parts = request.command.split()
    
    if not cmd_parts or cmd_parts[0] not in valid_commands:
        return {
            "status": "error",
            "message": "无效的命令，请使用 kubectl 或 helm",
        }
    
    # 模拟命令执行结果
    mock_outputs = {
        "get pods": """NAME                    READY   STATUS    RESTARTS   AGE
nginx-7854ff8877-abc12   1/1     Running   0          5m
nginx-7854ff8877-def34   1/1     Running   0          5m""",
        "get nodes": """NAME       STATUS   ROLES                  AGE   VERSION
minikube   Ready    control-plane,master   10d   v1.25.0""",
        "get svc": """NAME         TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)        AGE
kubernetes   ClusterIP   10.96.0.1       <none>        443/TCP        10d
nginx        NodePort    10.96.123.45    <none>        80:30080/TCP   5m""",
    }
    
    output = mock_outputs.get(" ".join(cmd_parts[1:3]), "命令执行成功")
    
    return {
        "status": "success",
        "data": {
            "command": request.command,
            "namespace": request.namespace,
            "output": output,
        },
    }


@router.get("/cluster")
async def get_cluster_status():
    """获取集群状态"""
    return {
        "status": "success",
        "data": {
            "nodes": 3,
            "pods": 12,
            "services": 5,
            "namespaces": 4,
            "health": "healthy",
        },
    }


@router.get("/namespaces")
async def get_namespaces():
    """获取命名空间列表"""
    return {
        "status": "success",
        "data": [
            {"name": "default", "status": "Active"},
            {"name": "kube-system", "status": "Active"},
            {"name": "kube-public", "status": "Active"},
            {"name": "kugame", "status": "Active"},
        ],
    }


@router.get("/pods")
async def get_pods(namespace: str = "default"):
    """获取 Pod 列表"""
    return {
        "status": "success",
        "data": [
            {"name": "nginx-7854ff8877-abc12", "status": "Running", "ready": "1/1", "restarts": 0},
            {"name": "nginx-7854ff8877-def34", "status": "Running", "ready": "1/1", "restarts": 0},
        ],
    }


@router.get("/nodes")
async def get_nodes():
    """获取节点列表"""
    return {
        "status": "success",
        "data": [
            {
                "name": "minikube",
                "status": "Ready",
                "roles": ["control-plane", "master"],
                "cpu": "4",
                "memory": "8Gi",
            },
        ],
    }
