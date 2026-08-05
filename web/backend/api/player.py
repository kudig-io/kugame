"""Player API Routes（封装 kugame 核心包）"""
from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from .deps import get_engine, get_player, persist, player_view

router = APIRouter(prefix="/api/player", tags=["player"])

# 门派映射：Web 前端 key -> kugame Sect 枚举名
_SECT_KEYS = {
    "qingyun": "青云宗",
    "xuantian": "玄天宗",
    "lianyu": "炼狱门",
    "xiaoyao": "逍遥派",
}


class CreatePlayerRequest(BaseModel):
    name: str
    sect: str


class UpdatePlayerRequest(BaseModel):
    name: Optional[str] = None
    sect: Optional[str] = None


@router.get("")
async def get_player_info():
    """获取当前玩家信息"""
    return {
        "status": "success",
        "data": player_view(get_player()),
    }


@router.post("/create")
async def create_player(request: CreatePlayerRequest):
    """创建新角色（重置当前玩家）"""
    from kugame.player import Sect

    if not request.name or len(request.name) < 2:
        raise HTTPException(status_code=400, detail="角色名称至少需要2个字符")

    sect_name = _SECT_KEYS.get(request.sect)
    if sect_name is None:
        raise HTTPException(status_code=400, detail="无效的门派选择")

    engine = get_engine()
    engine.initialize_player(request.name, Sect(sect_name))
    persist()

    return {
        "status": "success",
        "data": player_view(engine.player),
    }


@router.get("/stats")
async def get_player_stats():
    """获取玩家详细统计（来自游戏核心进度系统）"""
    engine = get_engine()
    try:
        progress = engine.get_progress()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    player = engine.player
    commands = progress.get("commands", {})
    achievements = progress.get("achievements", {})

    stats = {
        "combat": {
            "total_correct": player.total_correct,
            "total_attempts": player.total_attempts,
            "accuracy": progress["player"]["accuracy"],
            "streak": progress.get("streak", 0),
        },
        "cultivation": {
            "level": progress["player"]["level"],
            "experience": progress["player"]["experience"],
            "required_exp": progress["player"]["required_exp"],
            "sect_bonus": progress["player"]["sect_bonus"],
        },
        "k8s": {
            "commands_mastered": commands.get("mastered_count", len(player.kubectl_commands_mastered)),
            "total_commands": commands.get("total_count", 0),
            "total_score": progress.get("total_score", 0),
        },
        "proficiency": progress.get("proficiency_summary", {}),
        "achievements": achievements,
    }

    return {
        "status": "success",
        "data": stats,
    }


@router.post("/update")
async def update_player(request: UpdatePlayerRequest):
    """更新玩家信息"""
    from kugame.player import Sect

    player = get_player()

    if request.name:
        if len(request.name) < 2:
            raise HTTPException(status_code=400, detail="角色名称至少需要2个字符")
        player.name = request.name

    if request.sect:
        sect_name = _SECT_KEYS.get(request.sect)
        if sect_name is None:
            raise HTTPException(status_code=400, detail="无效的门派选择")
        player.sect = Sect(sect_name)

    persist()

    return {
        "status": "success",
        "data": player_view(player),
    }


@router.post("/save")
async def save_player():
    """保存玩家进度"""
    ok = persist()
    if not ok:
        raise HTTPException(status_code=400, detail="保存失败")
    return {
        "status": "success",
        "data": {"message": "进度已保存"},
    }
