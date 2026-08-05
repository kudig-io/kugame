"""K8s Learning API Routes（封装 kugame 核心命令学习系统）"""
from fastapi import APIRouter, HTTPException

from .deps import get_engine

router = APIRouter(prefix="/api/k8s", tags=["k8s"])


@router.get("/commands")
async def get_commands():
    """获取所有 Kubernetes 命令手册（含掌握度）"""
    engine = get_engine()
    try:
        commands = engine.get_all_commands_info()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {
        "status": "success",
        "data": commands,
    }


@router.get("/commands/categories")
async def get_command_categories():
    """按分类聚合命令数量"""
    engine = get_engine()
    try:
        commands = engine.get_all_commands_info()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    categories: dict = {}
    for cmd in commands:
        cat = cmd["category"]
        bucket = categories.setdefault(cat, {"category": cat, "total": 0, "mastered": 0})
        bucket["total"] += 1
        if cmd.get("mastered"):
            bucket["mastered"] += 1

    return {
        "status": "success",
        "data": list(categories.values()),
    }


@router.get("/progress")
async def get_learning_progress():
    """获取命令学习进度与掌握度汇总"""
    engine = get_engine()
    try:
        progress = engine.get_progress()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {
        "status": "success",
        "data": {
            "commands": progress.get("commands", {}),
            "proficiency_summary": progress.get("proficiency_summary", {}),
            "total_score": progress.get("total_score", 0),
        },
    }


@router.get("/quiz")
async def get_quiz():
    """生成一道命令测验题"""
    engine = get_engine()
    try:
        quiz = engine.generate_quiz()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    if not quiz:
        raise HTTPException(status_code=404, detail="暂无可用测验")
    return {
        "status": "success",
        "data": quiz,
    }
