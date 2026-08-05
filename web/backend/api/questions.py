"""Question Bank API Routes

复用 kugame 核心题库（complete_question_bank.json，300+题），
为 Web 前端提供出题、判题和统计接口。
"""
import json
import os
import sys
from typing import Any, List, Optional

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

# 将项目根目录加入路径，以复用 kugame 核心包
_PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

from kugame.question_bank import (  # noqa: E402
    K8sCategory,
    QuestionBank,
    QuestionDifficulty,
)

router = APIRouter(prefix="/api/questions", tags=["questions"])

# 模块级题库单例
_question_bank = QuestionBank()


def _load_bank() -> None:
    """从项目根目录加载完整题库"""
    bank_path = os.path.join(_PROJECT_ROOT, "complete_question_bank.json")
    if not os.path.exists(bank_path):
        return
    try:
        with open(bank_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        _question_bank.import_from_dict(data, merge=True)
    except (json.JSONDecodeError, OSError) as e:
        print(f"加载题库失败: {e}")


_load_bank()


class CheckAnswerRequest(BaseModel):
    answer: Any


def _resolve_category(value: Optional[str]) -> Optional[K8sCategory]:
    """按分类value解析枚举，无效值返回400"""
    if value is None:
        return None
    for cat in K8sCategory:
        if cat.value == value:
            return cat
    raise HTTPException(status_code=400, detail=f"无效的分类: {value}")


def _resolve_difficulty(level: Optional[int]) -> Optional[QuestionDifficulty]:
    """按难度等级解析枚举，无效值返回400"""
    if level is None:
        return None
    for diff in QuestionDifficulty:
        if diff.level == level:
            return diff
    raise HTTPException(status_code=400, detail=f"无效的难度等级: {level}")


def _public_question(question: Any) -> dict:
    """题目公开视图（不含答案与解析，避免前端泄题）"""
    return {
        "id": question.id,
        "type": question.type.value,
        "difficulty": question.difficulty.level,
        "difficulty_stars": question.difficulty.stars,
        "category": question.category.value,
        "question": question.question,
        "options": question.options,
        "tags": question.tags,
    }


@router.get("/stats")
async def get_stats() -> dict:
    """获取题库统计信息"""
    return _question_bank.get_statistics()


@router.get("/categories")
async def get_categories() -> List[dict]:
    """获取所有知识分类"""
    return [{"name": cat.name, "value": cat.value} for cat in K8sCategory]


@router.get("/random")
async def get_random_question(
    category: Optional[str] = Query(None, description="分类value，如 pod"),
    difficulty: Optional[int] = Query(None, ge=1, le=5, description="难度等级1-5"),
) -> dict:
    """随机抽取一道题目（不含答案）"""
    question = _question_bank.get_random_question(
        category=_resolve_category(category),
        difficulty=_resolve_difficulty(difficulty),
    )
    if not question:
        raise HTTPException(status_code=404, detail="没有符合条件的题目")
    return _public_question(question)


@router.get("/{question_id}")
async def get_question(question_id: str) -> dict:
    """按ID获取题目（不含答案）"""
    question = _question_bank.get_question(question_id)
    if not question:
        raise HTTPException(status_code=404, detail="题目不存在")
    return _public_question(question)


@router.post("/{question_id}/check")
async def check_answer(question_id: str, request: CheckAnswerRequest) -> dict:
    """判题并返回解析"""
    question = _question_bank.get_question(question_id)
    if not question:
        raise HTTPException(status_code=404, detail="题目不存在")

    is_correct, feedback = question.check_answer(request.answer)
    return {
        "correct": is_correct,
        "message": feedback,
        "correct_answer": question.correct_answer,
        "explanation": question.explanation,
        "related_commands": question.related_commands,
    }
