"""Combat API Routes（封装 kugame 核心战斗系统）

战斗采用"答题驱动攻击"模式：每次攻击伴随一道命令测验题，
答对造成双倍伤害，答错伤害减半。怪物取自故事系统的战斗事件。
"""
from typing import Any, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from kugame.story import Monster

from .deps import get_engine, persist

router = APIRouter(prefix="/api/combat", tags=["combat"])


class CombatStartRequest(BaseModel):
    enemy_id: Optional[str] = None


class CombatAttackRequest(BaseModel):
    answer: Any  # 题目答案（单选为字母字符串，多选为列表）


def _combat_monsters() -> list:
    """从故事系统收集战斗事件怪物"""
    engine = get_engine()
    events = engine.story_manager.random_events
    return [e for e in events if getattr(e, "event_type", None) == "combat" and e.monster]


@router.get("/enemies")
async def get_enemies():
    """获取可战斗的敌人列表（来自故事战斗事件）"""
    data = []
    for event in _combat_monsters():
        m: Monster = event.monster
        data.append({
            "id": event.event_id,
            "name": m.name,
            "level": m.level,
            "description": m.description,
            "reward": {"exp": m.experience_reward},
        })
    return {
        "status": "success",
        "data": data,
    }


@router.post("/start")
async def start_combat(request: CombatStartRequest):
    """开始战斗"""
    engine = get_engine()
    events = _combat_monsters()
    if not events:
        raise HTTPException(status_code=404, detail="没有可用的战斗")

    event = next((e for e in events if e.event_id == request.enemy_id), None)
    if event is None:
        event = events[0]

    # 重建怪物实例，避免污染故事事件中的共享对象
    src: Monster = event.monster
    monster = Monster(
        name=src.name,
        health=src.health,
        attack=src.attack,
        defense=src.defense,
        experience_reward=src.experience_reward,
        command_challenge=src.command_challenge,
        description=src.description,
        level=src.level,
    )

    try:
        state = engine.start_combat(monster)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {
        "status": "success",
        "data": state,
    }


@router.post("/attack")
async def combat_attack(request: CombatAttackRequest):
    """执行一次攻击（伴随一道题库测验题判定）"""
    engine = get_engine()
    if not getattr(engine, "current_monster", None):
        raise HTTPException(status_code=400, detail="没有正在进行的战斗，请先开始战斗")

    question = engine.generate_bank_question()
    if not question:
        raise HTTPException(status_code=400, detail="暂无可用的命令测验题")

    is_correct, _ = question.check_answer(request.answer)
    result = engine.player_attack(engine.current_monster, is_correct)

    if result.get("status") in ("victory", "combat_victory"):
        persist()

    return {
        "status": "success",
        "data": {
            "quiz": {
                "id": question.id,
                "question": question.question,
                "options": question.options,
            },
            "answer_correct": is_correct,
            "combat": result,
        },
    }


@router.post("/flee")
async def flee_combat():
    """逃离战斗"""
    engine = get_engine()
    if not getattr(engine, "current_monster", None):
        raise HTTPException(status_code=400, detail="没有正在进行的战斗")
    result = engine.flee_combat(engine.current_monster)
    return {
        "status": "success",
        "data": result,
    }
