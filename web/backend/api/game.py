"""Game API Routes（封装 kugame 核心题库答题与进度系统）"""
from typing import Any, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from .deps import get_engine, persist

router = APIRouter(prefix="/api/game", tags=["game"])


class AnswerRequest(BaseModel):
    question_id: str
    answer: Any


def _public_question(question: Any) -> dict:
    """题目公开视图（不含答案与解析）"""
    return {
        "id": question.id,
        "type": question.type.value,
        "difficulty": question.difficulty.level,
        "category": question.category.value,
        "question": question.question,
        "options": question.options,
        "tags": question.tags,
    }


@router.get("/question")
async def get_question(use_wrong_only: bool = False):
    """从题库抽取一道题目（默认结合当前章节/错题本）"""
    engine = get_engine()
    question = engine.generate_bank_question(use_wrong_only=use_wrong_only)
    if not question:
        raise HTTPException(status_code=404, detail="没有可用的题目")
    return {
        "status": "success",
        "data": _public_question(question),
    }


@router.post("/answer")
async def answer_question(request: AnswerRequest):
    """判题并更新玩家学习数据（经验/连击/错题本/成就）"""
    engine = get_engine()
    question = engine.question_bank.get_question(request.question_id)
    if not question:
        raise HTTPException(status_code=404, detail="题目不存在")

    result = engine.check_bank_answer(question, request.answer)
    persist()

    return {
        "status": "success",
        "data": {
            **result,
            "correct_answer": question.correct_answer,
        },
    }


@router.get("/story")
async def get_story():
    """获取当前故事章节内容"""
    engine = get_engine()
    return {
        "status": "success",
        "data": engine.get_story_content(),
    }


@router.post("/story/advance")
async def advance_story():
    """推进到下一章节"""
    engine = get_engine()
    advanced = engine.advance_chapter()
    persist()
    return {
        "status": "success",
        "data": {
            "advanced": advanced,
            "message": "已推进到下一章节" if advanced else "当前已是最新章节",
        },
    }


@router.get("/progress")
async def get_progress():
    """获取完整游戏进度"""
    engine = get_engine()
    try:
        progress = engine.get_progress()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {
        "status": "success",
        "data": progress,
    }
