"""Combat API Routes"""
from fastapi import APIRouter, HTTPException
from typing import Dict, Any, Optional, List
from pydantic import BaseModel
from enum import Enum

router = APIRouter(prefix="/api/combat", tags=["combat"])


class CombatAction(str, Enum):
    ATTACK = "attack"
    SKILL = "skill"
    ITEM = "item"
    DEFEND = "defend"
    FLEE = "flee"


class CombatStartRequest(BaseModel):
    enemy_id: str


class CombatActionRequest(BaseModel):
    action: CombatAction
    target: Optional[str] = None
    skill_id: Optional[str] = None
    item_id: Optional[str] = None


# 模拟战斗状态存储
active_combats: Dict[str, Dict[str, Any]] = {}


@router.post("/start")
async def start_combat(request: CombatStartRequest):
    """开始战斗"""
    combat_id = f"combat_{request.enemy_id}_{hash(request.enemy_id) % 10000}"
    
    combat_state = {
        "id": combat_id,
        "enemy": {
            "id": request.enemy_id,
            "name": "妖兽",
            "hp": 100,
            "max_hp": 100,
            "level": 5,
        },
        "player_hp": 100,
        "player_mp": 50,
        "turn": 1,
        "status": "active",
        "log": ["战斗开始！遭遇了妖兽！"],
    }
    
    active_combats[combat_id] = combat_state
    
    return {
        "status": "success",
        "data": combat_state,
    }


@router.post("/action")
async def combat_action(request: CombatActionRequest):
    """执行战斗动作"""
    # 模拟战斗逻辑
    import random
    
    result = {
        "action": request.action,
        "damage_dealt": 0,
        "damage_taken": 0,
        "effects": [],
        "log": [],
    }
    
    if request.action == CombatAction.ATTACK:
        damage = random.randint(15, 25)
        result["damage_dealt"] = damage
        result["log"].append(f"你发动了攻击，造成 {damage} 点伤害！")
        
        # 敌人反击
        enemy_damage = random.randint(5, 15)
        result["damage_taken"] = enemy_damage
        result["log"].append(f"敌人反击，你受到 {enemy_damage} 点伤害！")
        
    elif request.action == CombatAction.SKILL:
        if request.skill_id:
            damage = random.randint(25, 40)
            result["damage_dealt"] = damage
            result["effects"].append("skill_used")
            result["log"].append(f"你使用了技能，造成 {damage} 点伤害！")
        else:
            result["log"].append("未选择技能")
            
    elif request.action == CombatAction.DEFEND:
        result["effects"].append("defending")
        result["damage_taken"] = random.randint(0, 5)
        result["log"].append("你进入防御姿态，受到的伤害大幅降低！")
        
    elif request.action == CombatAction.FLEE:
        success = random.random() > 0.5
        if success:
            result["effects"].append("fled")
            result["log"].append("你成功逃离了战斗！")
        else:
            result["log"].append("逃跑失败！")
            result["damage_taken"] = random.randint(5, 10)
    
    return {
        "status": "success",
        "data": result,
    }


@router.get("/enemies")
async def get_enemies():
    """获取可战斗的敌人列表"""
    return {
        "status": "success",
        "data": [
            {"id": "wild_beast", "name": "妖兽", "level": 5, "reward": {"exp": 30}},
            {"id": "bandit", "name": "强盗", "level": 8, "reward": {"exp": 50}},
            {"id": "demon", "name": "魔修", "level": 15, "reward": {"exp": 100}},
        ],
    }


@router.get("/skills")
async def get_skills():
    """获取可用技能"""
    return {
        "status": "success",
        "data": [
            {"id": "basic_attack", "name": "普通攻击", "damage": 20, "mp_cost": 0},
            {"id": "fireball", "name": "火球术", "damage": 35, "mp_cost": 10},
            {"id": "heal", "name": "治愈术", "heal": 30, "mp_cost": 15},
        ],
    }
