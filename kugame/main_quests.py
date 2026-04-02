"""主线任务和支线任务定义

定义游戏中的主线剧情任务和支线任务。
"""
# -*- coding: utf-8 -*-

from typing import List, Dict, Any
from .quest_system import Quest, QuestObjective, QuestObjectiveType, QuestType, QuestStatus


# 主线任务定义
MAIN_QUESTS = [
    {
        "id": "main_chapter_1",
        "name": "初入青云",
        "description": "完成第一章故事，学习基础的Deployment管理命令",
        "objectives": [
            (QuestObjectiveType.学习命令, 5, "学习5个新命令"),
        ],
        "rewards": {"experience": 500, "title": "青云弟子"},
        "level_requirement": 1,
    },
    {
        "id": "main_chapter_2",
        "name": "服务之道",
        "description": "完成第二章故事，掌握Service服务发现",
        "objectives": [
            (QuestObjectiveType.学习命令, 5, "学习5个新命令"),
            (QuestObjectiveType.完成战斗, 3, "完成3场战斗"),
        ],
        "rewards": {"experience": 800, "title": "服务学徒"},
        "level_requirement": 5,
        "prerequisite_quests": ["main_chapter_1"],
    },
    {
        "id": "main_chapter_3",
        "name": "配置精通",
        "description": "完成第三章故事，学会使用ConfigMap和Secret",
        "objectives": [
            (QuestObjectiveType.学习命令, 5, "学习5个新命令"),
            (QuestObjectiveType.答题正确, 15, "答对15道题"),
        ],
        "rewards": {"experience": 1000, "title": "配置大师"},
        "level_requirement": 10,
        "prerequisite_quests": ["main_chapter_2"],
    },
    {
        "id": "main_combat_master",
        "name": "战斗大师",
        "description": "通过战斗磨练，成为真正的战斗大师",
        "objectives": [
            (QuestObjectiveType.赢得战斗, 20, "赢得20场战斗"),
            (QuestObjectiveType.连续答题, 10, "连续答对10道题"),
        ],
        "rewards": {"experience": 2000, "title": "战斗大师"},
        "level_requirement": 15,
        "prerequisite_quests": ["main_chapter_3"],
    },
    {
        "id": "main_tower_climber",
        "name": "通天之路",
        "description": "挑战之塔达到30层，证明你的实力",
        "objectives": [
            (QuestObjectiveType.挑战塔层, 30, "达到挑战塔30层"),
        ],
        "rewards": {"experience": 3000, "title": "通天者"},
        "level_requirement": 25,
        "prerequisite_quests": ["main_combat_master"],
    },
    {
        "id": "main_equipment_collector",
        "name": "装备大师",
        "description": "收集各种品质的装备，强化自身实力",
        "objectives": [
            (QuestObjectiveType.获得装备, 30, "获得30件装备"),
            (QuestObjectiveType.强化装备, 10, "强化装备10次"),
        ],
        "rewards": {"experience": 2500, "title": "装备大师"},
        "level_requirement": 30,
        "prerequisite_quests": ["main_tower_climber"],
    },
    {
        "id": "main_final",
        "name": "飞升大成",
        "description": "完成所有主线任务，达到修仙巅峰",
        "objectives": [
            (QuestObjectiveType.学习命令, 50, "学习50个命令"),
            (QuestObjectiveType.赢得战斗, 50, "赢得50场战斗"),
            (QuestObjectiveType.挑战塔层, 50, "达到挑战塔50层"),
        ],
        "rewards": {"experience": 10000, "title": "一代宗师"},
        "level_requirement": 50,
        "prerequisite_quests": ["main_equipment_collector"],
    },
]

# 支线任务定义
SIDE_QUESTS = [
    {
        "id": "side_perfect_streak",
        "name": "完美连击",
        "description": "连续答对20道题目，展示你的知识掌握程度",
        "objectives": [
            (QuestObjectiveType.连续答题, 20, "连续答对20道题"),
        ],
        "rewards": {"experience": 1500, "stamina": 30},
        "level_requirement": 5,
    },
    {
        "id": "side_dungeon_explorer",
        "name": "副本探索者",
        "description": "完成10次副本挑战",
        "objectives": [
            (QuestObjectiveType.完成副本, 10, "完成10次副本"),
        ],
        "rewards": {"experience": 2000, "stamina": 50},
        "level_requirement": 15,
    },
    {
        "id": "side_stamina_consumer",
        "name": "体力充沛",
        "description": "累计消耗500点体力",
        "objectives": [
            (QuestObjectiveType.消耗体力, 500, "消耗500点体力"),
        ],
        "rewards": {"experience": 1000, "stamina": 100},
        "level_requirement": 10,
    },
    {
        "id": "side_orange_hunter",
        "name": "传说猎人",
        "description": "获得5件传说品质的装备",
        "objectives": [
            (QuestObjectiveType.获得装备, 5, "获得5件传说装备"),
        ],
        "rewards": {"experience": 3000, "title": "传说猎人"},
        "level_requirement": 30,
    },
    {
        "id": "side_tower_master",
        "name": "塔之征服者",
        "description": "挑战之塔达到100层",
        "objectives": [
            (QuestObjectiveType.挑战塔层, 100, "达到挑战塔100层"),
        ],
        "rewards": {"experience": 5000, "title": "塔之征服者"},
        "level_requirement": 40,
    },
]


def create_main_quests() -> List[Quest]:
    """创建所有主线任务"""
    quests = []
    for data in MAIN_QUESTS:
        quest = Quest(
            id=data["id"],
            name=data["name"],
            description=data["description"],
            quest_type=QuestType.主线任务,
            objectives=[
                QuestObjective(
                    objective_type=obj[0],
                    target_value=obj[1],
                    description=obj[2]
                )
                for obj in data["objectives"]
            ],
            rewards=data["rewards"],
            status=QuestStatus.未接受,
            level_requirement=data["level_requirement"],
            prerequisite_quests=data.get("prerequisite_quests", []),
        )
        quests.append(quest)
    return quests


def create_side_quests() -> List[Quest]:
    """创建所有支线任务"""
    quests = []
    for data in SIDE_QUESTS:
        quest = Quest(
            id=data["id"],
            name=data["name"],
            description=data["description"],
            quest_type=QuestType.支线任务,
            objectives=[
                QuestObjective(
                    objective_type=obj[0],
                    target_value=obj[1],
                    description=obj[2]
                )
                for obj in data["objectives"]
            ],
            rewards=data["rewards"],
            status=QuestStatus.未接受,
            level_requirement=data["level_requirement"],
        )
        quests.append(quest)
    return quests


def get_available_main_quests(completed_quests: List[str], player_level: int) -> List[Quest]:
    """获取可接受的主线任务
    
    Args:
        completed_quests: 已完成的任务ID列表
        player_level: 玩家等级
        
    Returns:
        List[Quest]: 可接受的任务列表
    """
    all_quests = create_main_quests()
    available = []
    
    for quest in all_quests:
        # 检查是否已完成
        if quest.id in completed_quests:
            continue
        
        # 检查等级要求
        if player_level < quest.level_requirement:
            continue
        
        # 检查前置任务
        if quest.prerequisite_quests:
            if not all(prereq in completed_quests for prereq in quest.prerequisite_quests):
                continue
        
        available.append(quest)
    
    return available


def get_available_side_quests(completed_quests: List[str], player_level: int) -> List[Quest]:
    """获取可接受的支线任务"""
    all_quests = create_side_quests()
    available = []
    
    for quest in all_quests:
        if quest.id in completed_quests:
            continue
        if player_level < quest.level_requirement:
            continue
        available.append(quest)
    
    return available
