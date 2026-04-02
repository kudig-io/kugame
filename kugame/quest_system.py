"""任务系统

提供每日任务、每周任务、主线任务和支线任务功能，
为玩家提供明确的短期目标和额外奖励。
"""
# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Callable
from enum import Enum, auto
from datetime import datetime, timedelta
import random
import json


class QuestType(Enum):
    """任务类型枚举"""
    每日任务 = "daily"
    每周任务 = "weekly"
    主线任务 = "main"
    支线任务 = "side"


class QuestStatus(Enum):
    """任务状态枚举"""
    未接受 = "not_accepted"
    进行中 = "in_progress"
    已完成 = "completed"
    已领奖 = "rewarded"


class QuestObjectiveType(Enum):
    """任务目标类型"""
    学习命令 = "learn_command"           # 学习指定数量的命令
    完成战斗 = "complete_combat"         # 完成指定次数的战斗
    赢得战斗 = "win_combat"              # 赢得指定次数的战斗
    挑战塔层 = "tower_level"             # 达到指定挑战塔层
    完成副本 = "complete_dungeon"        # 完成指定副本
    签到天数 = "checkin_days"            # 累计签到天数
    答题正确 = "correct_answers"         # 答对指定数量题目
    连续答题 = "streak_answers"          # 连续答对题目
    获得装备 = "obtain_equipment"        # 获得指定品质装备
    强化装备 = "upgrade_equipment"       # 强化装备次数
    消耗体力 = "consume_stamina"         # 消耗体力
    获得经验 = "gain_experience"         # 获得经验值


@dataclass
class QuestObjective:
    """任务目标
    
    Attributes:
        objective_type: 目标类型
        target_value: 目标数值
        current_value: 当前进度
        description: 目标描述
    """
    objective_type: QuestObjectiveType
    target_value: int
    current_value: int = 0
    description: str = ""
    
    @property
    def is_completed(self) -> bool:
        """检查目标是否完成"""
        return self.current_value >= self.target_value
    
    @property
    def progress_percentage(self) -> float:
        """获取进度百分比"""
        if self.target_value <= 0:
            return 100.0
        return min(100.0, (self.current_value / self.target_value) * 100)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "objective_type": self.objective_type.value,
            "target_value": self.target_value,
            "current_value": self.current_value,
            "description": self.description,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "QuestObjective":
        """从字典创建"""
        return cls(
            objective_type=QuestObjectiveType(data["objective_type"]),
            target_value=data["target_value"],
            current_value=data.get("current_value", 0),
            description=data.get("description", ""),
        )


@dataclass
class Quest:
    """任务
    
    Attributes:
        id: 任务唯一ID
        name: 任务名称
        description: 任务描述
        quest_type: 任务类型
        objectives: 任务目标列表
        rewards: 奖励字典
        status: 任务状态
        created_at: 创建时间
        expires_at: 过期时间（可选）
        prerequisite_quests: 前置任务ID列表
        level_requirement: 等级要求
    """
    id: str
    name: str
    description: str
    quest_type: QuestType
    objectives: List[QuestObjective] = field(default_factory=list)
    rewards: Dict[str, Any] = field(default_factory=dict)
    status: QuestStatus = QuestStatus.未接受
    created_at: Optional[str] = None
    expires_at: Optional[str] = None
    prerequisite_quests: List[str] = field(default_factory=list)
    level_requirement: int = 1
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()
    
    @property
    def is_completed(self) -> bool:
        """检查所有目标是否完成"""
        return all(obj.is_completed for obj in self.objectives)
    
    @property
    def overall_progress(self) -> float:
        """获取整体进度百分比"""
        if not self.objectives:
            return 0.0
        return sum(obj.progress_percentage for obj in self.objectives) / len(self.objectives)
    
    def update_progress(self, objective_type: QuestObjectiveType, value: int = 1) -> bool:
        """更新任务进度
        
        Args:
            objective_type: 目标类型
            value: 增加的值
            
        Returns:
            bool: 是否有目标完成
        """
        if self.status not in [QuestStatus.未接受, QuestStatus.进行中]:
            return False
        
        completed_before = self.is_completed
        
        for objective in self.objectives:
            if objective.objective_type == objective_type:
                objective.current_value = min(
                    objective.target_value,
                    objective.current_value + value
                )
        
        # 检查是否刚完成
        if not completed_before and self.is_completed:
            self.status = QuestStatus.已完成
            return True
        
        if self.status == QuestStatus.未接受:
            self.status = QuestStatus.进行中
        
        return False
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "quest_type": self.quest_type.value,
            "objectives": [obj.to_dict() for obj in self.objectives],
            "rewards": self.rewards,
            "status": self.status.value,
            "created_at": self.created_at,
            "expires_at": self.expires_at,
            "prerequisite_quests": self.prerequisite_quests,
            "level_requirement": self.level_requirement,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Quest":
        """从字典创建"""
        return cls(
            id=data["id"],
            name=data["name"],
            description=data["description"],
            quest_type=QuestType(data["quest_type"]),
            objectives=[QuestObjective.from_dict(obj) for obj in data.get("objectives", [])],
            rewards=data.get("rewards", {}),
            status=QuestStatus(data.get("status", "not_accepted")),
            created_at=data.get("created_at"),
            expires_at=data.get("expires_at"),
            prerequisite_quests=data.get("prerequisite_quests", []),
            level_requirement=data.get("level_requirement", 1),
        )


# 每日任务模板
DAILY_QUEST_TEMPLATES = [
    {
        "name": "今日修炼",
        "description": "学习3个新的Kubernetes命令",
        "objectives": [
            (QuestObjectiveType.学习命令, 3, "学习3个命令")
        ],
        "rewards": {"experience": 200, "stamina": 10},
    },
    {
        "name": "战斗历练",
        "description": "完成5场战斗",
        "objectives": [
            (QuestObjectiveType.完成战斗, 5, "完成5场战斗")
        ],
        "rewards": {"experience": 300, "gold": 100},
    },
    {
        "name": "答题挑战",
        "description": "答对10道题目",
        "objectives": [
            (QuestObjectiveType.答题正确, 10, "答对10道题")
        ],
        "rewards": {"experience": 250},
    },
    {
        "name": "连击大师",
        "description": "连续答对5道题目",
        "objectives": [
            (QuestObjectiveType.连续答题, 5, "连续答对5道题")
        ],
        "rewards": {"experience": 400},
    },
    {
        "name": "装备收集",
        "description": "获得2件装备",
        "objectives": [
            (QuestObjectiveType.获得装备, 2, "获得2件装备")
        ],
        "rewards": {"experience": 150, "stamina": 5},
    },
    {
        "name": "副本探索",
        "description": "完成1次副本挑战",
        "objectives": [
            (QuestObjectiveType.完成副本, 1, "完成1次副本")
        ],
        "rewards": {"experience": 500},
    },
    {
        "name": "体力消耗",
        "description": "消耗50点体力",
        "objectives": [
            (QuestObjectiveType.消耗体力, 50, "消耗50点体力")
        ],
        "rewards": {"experience": 200, "gold": 50},
    },
]

# 每周任务模板
WEEKLY_QUEST_TEMPLATES = [
    {
        "name": "周常修炼",
        "description": "学习20个新的Kubernetes命令",
        "objectives": [
            (QuestObjectiveType.学习命令, 20, "学习20个命令")
        ],
        "rewards": {"experience": 1500, "stamina": 50},
    },
    {
        "name": "战斗狂人",
        "description": "赢得20场战斗",
        "objectives": [
            (QuestObjectiveType.赢得战斗, 20, "赢得20场战斗")
        ],
        "rewards": {"experience": 2000, "gold": 500},
    },
    {
        "name": "答题达人",
        "description": "答对50道题目",
        "objectives": [
            (QuestObjectiveType.答题正确, 50, "答对50道题")
        ],
        "rewards": {"experience": 1500},
    },
    {
        "name": "挑战塔攀登者",
        "description": "挑战之塔达到10层",
        "objectives": [
            (QuestObjectiveType.挑战塔层, 10, "达到第10层")
        ],
        "rewards": {"experience": 2000, "stamina": 30},
    },
    {
        "name": "装备强化",
        "description": "强化装备3次",
        "objectives": [
            (QuestObjectiveType.强化装备, 3, "强化3次装备")
        ],
        "rewards": {"experience": 1000, "gold": 300},
    },
]


class QuestManager:
    """任务管理器
    
    管理玩家的所有任务，包括生成、更新、完成等操作。
    """
    
    def __init__(self):
        self.active_quests: List[Quest] = []
        self.completed_quests: List[str] = []  # 已完成的任务ID列表
        self.last_daily_reset: Optional[str] = None
        self.last_weekly_reset: Optional[str] = None
    
    def check_and_reset_daily_quests(self) -> bool:
        """检查并重置每日任务
        
        Returns:
            bool: 是否进行了重置
        """
        now = datetime.now()
        
        if self.last_daily_reset:
            last_reset = datetime.fromisoformat(self.last_daily_reset)
            # 检查是否是同一天
            if last_reset.date() == now.date():
                return False
        
        # 清除旧的每日任务
        self.active_quests = [
            q for q in self.active_quests 
            if q.quest_type != QuestType.每日任务
        ]
        
        # 生成新的每日任务（随机3个）
        templates = random.sample(DAILY_QUEST_TEMPLATES, min(3, len(DAILY_QUEST_TEMPLATES)))
        for i, template in enumerate(templates):
            quest = Quest(
                id=f"daily_{now.strftime('%Y%m%d')}_{i}",
                name=template["name"],
                description=template["description"],
                quest_type=QuestType.每日任务,
                objectives=[
                    QuestObjective(
                        objective_type=obj[0],
                        target_value=obj[1],
                        description=obj[2]
                    )
                    for obj in template["objectives"]
                ],
                rewards=template["rewards"],
                status=QuestStatus.进行中,
                expires_at=(now + timedelta(days=1)).isoformat(),
            )
            self.active_quests.append(quest)
        
        self.last_daily_reset = now.isoformat()
        return True
    
    def check_and_reset_weekly_quests(self) -> bool:
        """检查并重置每周任务
        
        Returns:
            bool: 是否进行了重置
        """
        now = datetime.now()
        
        if self.last_weekly_reset:
            last_reset = datetime.fromisoformat(self.last_weekly_reset)
            # 检查是否是同一周
            if last_reset.isocalendar()[1] == now.isocalendar()[1] and last_reset.year == now.year:
                return False
        
        # 清除旧的每周任务
        self.active_quests = [
            q for q in self.active_quests 
            if q.quest_type != QuestType.每周任务
        ]
        
        # 生成新的每周任务（随机2个）
        templates = random.sample(WEEKLY_QUEST_TEMPLATES, min(2, len(WEEKLY_QUEST_TEMPLATES)))
        for i, template in enumerate(templates):
            quest = Quest(
                id=f"weekly_{now.strftime('%Y%W')}_{i}",
                name=template["name"],
                description=template["description"],
                quest_type=QuestType.每周任务,
                objectives=[
                    QuestObjective(
                        objective_type=obj[0],
                        target_value=obj[1],
                        description=obj[2]
                    )
                    for obj in template["objectives"]
                ],
                rewards=template["rewards"],
                status=QuestStatus.进行中,
                expires_at=(now + timedelta(days=7)).isoformat(),
            )
            self.active_quests.append(quest)
        
        self.last_weekly_reset = now.isoformat()
        return True
    
    def update_quest_progress(self, objective_type: QuestObjectiveType, value: int = 1) -> List[Quest]:
        """更新任务进度
        
        Args:
            objective_type: 目标类型
            value: 增加的值
            
        Returns:
            List[Quest]: 刚完成的任务列表
        """
        completed_quests = []
        
        for quest in self.active_quests:
            if quest.update_progress(objective_type, value):
                completed_quests.append(quest)
        
        return completed_quests
    
    def get_available_quests(self) -> List[Quest]:
        """获取可接受的任务列表"""
        return [q for q in self.active_quests if q.status == QuestStatus.未接受]
    
    def get_active_quests(self) -> List[Quest]:
        """获取进行中的任务列表"""
        return [q for q in self.active_quests if q.status == QuestStatus.进行中]
    
    def get_completed_quests(self) -> List[Quest]:
        """获取已完成但未领奖的任务列表"""
        return [q for q in self.active_quests if q.status == QuestStatus.已完成]
    
    def claim_reward(self, quest_id: str) -> Optional[Dict[str, Any]]:
        """领取任务奖励
        
        Args:
            quest_id: 任务ID
            
        Returns:
            Optional[Dict]: 奖励字典，如果不符合条件则返回None
        """
        for quest in self.active_quests:
            if quest.id == quest_id and quest.status == QuestStatus.已完成:
                quest.status = QuestStatus.已领奖
                self.completed_quests.append(quest_id)
                return quest.rewards
        return None
    
    def get_quest_summary(self) -> Dict[str, Any]:
        """获取任务摘要"""
        return {
            "active_count": len(self.get_active_quests()),
            "completed_count": len(self.get_completed_quests()),
            "total_completed": len(self.completed_quests),
            "daily_reset": self.last_daily_reset,
            "weekly_reset": self.last_weekly_reset,
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "active_quests": [q.to_dict() for q in self.active_quests],
            "completed_quests": self.completed_quests,
            "last_daily_reset": self.last_daily_reset,
            "last_weekly_reset": self.last_weekly_reset,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "QuestManager":
        """从字典创建"""
        manager = cls()
        manager.active_quests = [Quest.from_dict(q) for q in data.get("active_quests", [])]
        manager.completed_quests = data.get("completed_quests", [])
        manager.last_daily_reset = data.get("last_daily_reset")
        manager.last_weekly_reset = data.get("last_weekly_reset")
        return manager
