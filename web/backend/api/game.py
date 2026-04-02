"""Game API Routes"""
from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any, Optional
from pydantic import BaseModel

router = APIRouter(prefix="/api/game", tags=["game"])


class ActionRequest(BaseModel):
    action: str
    data: Optional[Dict[str, Any]] = None


@router.post("/explore")
async def explore():
    """探索世界"""
    return {
        "status": "success",
        "data": {
            "location": "青云山脉",
            "events": ["发现灵草", "遭遇妖兽"],
            "rewards": {"exp": 50, "spirit_stones": 10},
        },
    }


@router.post("/cultivate")
async def cultivate():
    """修炼"""
    return {
        "status": "success",
        "data": {
            "cultivation_gain": 100,
            "exp": 20,
            "message": "修炼了一周天，修为有所提升",
        },
    }


@router.post("/rest")
async def rest():
    """休息恢复"""
    return {
        "status": "success",
        "data": {
            "hp_restored": 50,
            "mp_restored": 30,
            "message": "休息片刻，精神恢复",
        },
    }


@router.get("/locations")
async def get_locations():
    """获取可探索地点"""
    return {
        "status": "success",
        "data": [
            {"id": "qingyun", "name": "青云山脉", "level": 1, "danger": "low"},
            {"id": "forbidden", "name": "禁地森林", "level": 10, "danger": "high"},
            {"id": "ancient", "name": "古修遗迹", "level": 20, "danger": "extreme"},
        ],
    }


@router.get("/events")
async def get_random_events():
    """获取随机事件"""
    import random
    
    events = [
        {"type": "treasure", "message": "发现宝箱", "reward": "随机道具"},
        {"type": "combat", "message": "遭遇敌人", "enemy": "wild_beast"},
        {"type": "blessing", "message": "灵气充沛", "buff": "cultivation_speed_up"},
        {"type": "npc", "message": "遇到神秘修士", "action": "trade"},
    ]
    
    return {
        "status": "success",
        "data": random.sample(events, k=min(3, len(events))),
    }
