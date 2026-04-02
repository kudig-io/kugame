"""Player API Routes"""
from fastapi import APIRouter, HTTPException
from typing import Dict, Any, Optional
from pydantic import BaseModel
from datetime import datetime

router = APIRouter(prefix="/api/player", tags=["player"])


class CreatePlayerRequest(BaseModel):
    name: str
    sect: str


class UpdatePlayerRequest(BaseModel):
    name: Optional[str] = None
    sect: Optional[str] = None


# 模拟玩家数据
MOCK_PLAYER = {
    "id": "player_001",
    "name": "测试玩家",
    "sect": "青云宗",
    "level": 5,
    "cultivation_realm": "练气期",
    "realm_progress": 75,
    "exp": 450,
    "max_exp": 1000,
    "hp": 100,
    "max_hp": 100,
    "mp": 50,
    "max_mp": 50,
    "spirit_stones": 1000,
    "k8s_exp": 200,
    "completed_quests": 5,
    "online_time": "02:34:56",
    "created_at": datetime.now().isoformat(),
    "recent_activities": [
        {"type": "combat", "message": "击败了妖兽，获得 30 经验", "time": "2分钟前"},
        {"type": "cultivation", "message": "修炼了一周天，修为提升", "time": "15分钟前"},
        {"type": "quest", "message": "完成任务：初识 K8s", "time": "1小时前"},
    ],
}


@router.get("")
async def get_player():
    """获取当前玩家信息"""
    # 实际应用中应该从 session 或 token 获取玩家 ID
    return {
        "status": "success",
        "data": MOCK_PLAYER,
    }


@router.post("/create")
async def create_player(request: CreatePlayerRequest):
    """创建新角色"""
    if not request.name or len(request.name) < 2:
        raise HTTPException(status_code=400, detail="角色名称至少需要2个字符")
    
    if request.sect not in ["qingyun", "jianxin", "lingyao", "tianji"]:
        raise HTTPException(status_code=400, detail="无效的门派选择")
    
    sect_names = {
        "qingyun": "青云宗",
        "jianxin": "剑心阁",
        "lingyao": "灵药谷",
        "tianji": "天机阁",
    }
    
    new_player = {
        "id": f"player_{hash(request.name) % 10000}",
        "name": request.name,
        "sect": sect_names[request.sect],
        "level": 1,
        "cultivation_realm": "练气期",
        "realm_progress": 0,
        "exp": 0,
        "max_exp": 100,
        "hp": 100,
        "max_hp": 100,
        "mp": 50,
        "max_mp": 50,
        "spirit_stones": 100,
        "k8s_exp": 0,
        "completed_quests": 0,
        "online_time": "00:00:00",
        "created_at": datetime.now().isoformat(),
        "recent_activities": [],
    }
    
    return {
        "status": "success",
        "data": new_player,
    }


@router.get("/stats")
async def get_player_stats():
    """获取玩家详细统计"""
    stats = {
        "combat": {
            "wins": 15,
            "losses": 3,
            "win_rate": "83.3%",
            "total_damage": 12500,
        },
        "cultivation": {
            "total_sessions": 45,
            "total_gain": 4500,
            "avg_per_session": 100,
        },
        "k8s": {
            "completed_lessons": 3,
            "total_score": 850,
            "commands_executed": 156,
        },
        "achievements": [
            {"id": "first_win", "name": "初战告捷", "description": "赢得第一场战斗", "unlocked_at": "2024-01-15"},
            {"id": "cultivator", "name": "入门修士", "description": "累计修炼10次", "unlocked_at": "2024-01-16"},
            {"id": "k8s_rookie", "name": "K8s 新手", "description": "完成第一个 K8s 课程", "unlocked_at": "2024-01-17"},
        ],
    }
    
    return {
        "status": "success",
        "data": stats,
    }


@router.post("/update")
async def update_player(request: UpdatePlayerRequest):
    """更新玩家信息"""
    updated = {}
    
    if request.name:
        updated["name"] = request.name
    if request.sect:
        updated["sect"] = request.sect
    
    return {
        "status": "success",
        "data": {**MOCK_PLAYER, **updated},
    }
