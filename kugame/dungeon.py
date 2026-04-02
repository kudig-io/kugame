"""副本系统

管理游戏中的每日副本和挑战内容。
"""
# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from enum import Enum
from datetime import datetime, timedelta
import random

from .story import Monster


class DungeonType(Enum):
    """副本类型"""
    经验副本 = "exp"
    装备副本 = "equipment"
    极限挑战 = "extreme"


@dataclass
class Dungeon:
    """副本数据类
    
    Attributes:
        id: 副本ID
        name: 副本名称
        dungeon_type: 副本类型
        description: 副本描述
        recommended_level: 推荐等级
        stamina_cost: 体力消耗
        reward_exp: 经验奖励
        reward_equipment_quality: 装备奖励品质
        difficulty_multiplier: 难度倍率
        completed: 是否已完成
    """
    id: str
    name: str
    dungeon_type: DungeonType
    description: str
    recommended_level: int
    stamina_cost: int = 10
    reward_exp: int = 500
    reward_equipment_quality: int = 2  # 精良起步
    difficulty_multiplier: float = 1.0
    completed: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "dungeon_type": self.dungeon_type.value,
            "description": self.description,
            "recommended_level": self.recommended_level,
            "stamina_cost": self.stamina_cost,
            "reward_exp": self.reward_exp,
            "reward_equipment_quality": self.reward_equipment_quality,
            "difficulty_multiplier": self.difficulty_multiplier,
            "completed": self.completed,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Dungeon":
        return cls(
            id=data["id"],
            name=data["name"],
            dungeon_type=DungeonType(data["dungeon_type"]),
            description=data["description"],
            recommended_level=data["recommended_level"],
            stamina_cost=data.get("stamina_cost", 10),
            reward_exp=data.get("reward_exp", 500),
            reward_equipment_quality=data.get("reward_equipment_quality", 2),
            difficulty_multiplier=data.get("difficulty_multiplier", 1.0),
            completed=data.get("completed", False),
        )


# 每日副本配置
DAILY_DUNGEONS = [
    Dungeon(
        id="exp_daily",
        name="修炼秘境",
        dungeon_type=DungeonType.经验副本,
        description="灵气充沛的修炼圣地，可获得大量经验",
        recommended_level=10,
        stamina_cost=10,
        reward_exp=1000,
        difficulty_multiplier=1.0,
    ),
    Dungeon(
        id="equipment_daily",
        name="藏宝洞窟",
        dungeon_type=DungeonType.装备副本,
        description="藏有上古神器的洞窟，可获得高品质装备",
        recommended_level=20,
        stamina_cost=15,
        reward_exp=500,
        reward_equipment_quality=3,  # 稀有起步
        difficulty_multiplier=1.3,
    ),
    Dungeon(
        id="extreme_daily",
        name="绝境试炼",
        dungeon_type=DungeonType.极限挑战,
        description="只有真正的强者才能通过的试炼",
        recommended_level=40,
        stamina_cost=20,
        reward_exp=2000,
        reward_equipment_quality=4,  # 史诗起步
        difficulty_multiplier=2.0,
    ),
]


@dataclass
class DungeonRun:
    """副本进行状态"""
    dungeon: Dungeon
    current_wave: int = 1
    total_waves: int = 3
    monsters_defeated: int = 0
    
    def is_complete(self) -> bool:
        return self.current_wave > self.total_waves
    
    def next_wave(self) -> Optional[Monster]:
        """获取下一波怪物"""
        if self.is_complete():
            return None
        
        # 生成怪物
        base_level = self.dungeon.recommended_level
        level = base_level + (self.current_wave - 1) * 5
        
        monster = Monster(
            name=f"第{self.current_wave}波守卫",
            health=50 + level * 10,
            attack=8 + level * 2,
            defense=2 + level,
            experience_reward=100 * self.current_wave,
            command_challenge="kubectl get pods",
            description=f"守护{self.dungeon.name}第{self.current_wave}波的怪物",
            level=level,
        )
        
        self.current_wave += 1
        return monster
    
    def get_final_reward(self) -> Dict[str, Any]:
        """获取最终奖励"""
        return {
            "experience": self.dungeon.reward_exp,
            "equipment_quality": self.dungeon.reward_equipment_quality,
        }


class DungeonManager:
    """副本管理器"""
    
    def __init__(self):
        self.daily_dungeons: List[Dungeon] = []
        self.last_refresh: Optional[datetime] = None
        self.current_run: Optional[DungeonRun] = None
        self._refresh_daily_dungeons()
    
    def _refresh_daily_dungeons(self) -> None:
        """刷新每日副本"""
        now = datetime.now()
        
        # 检查是否需要刷新（每天凌晨4点刷新）
        if self.last_refresh:
            last_refresh_date = self.last_refresh.date()
            current_date = now.date()
            
            # 如果已经刷新过今天的，跳过
            if last_refresh_date == current_date and now.hour >= 4:
                return
            # 如果昨天刷新过且现在过了4点
            if last_refresh_date < current_date or (last_refresh_date == current_date and self.last_refresh.hour < 4 <= now.hour):
                pass
            else:
                return
        
        # 刷新副本
        self.daily_dungeons = []
        for template in DAILY_DUNGEONS:
            dungeon = Dungeon.from_dict(template.to_dict())
            dungeon.completed = False
            self.daily_dungeons.append(dungeon)
        
        self.last_refresh = now
    
    def get_available_dungeons(self, player_level: int) -> List[Dungeon]:
        """获取可用的副本列表"""
        self._refresh_daily_dungeons()
        
        available = []
        for dungeon in self.daily_dungeons:
            # 等级相差不超过20级可以挑战
            if player_level >= dungeon.recommended_level - 20:
                available.append(dungeon)
        
        return available
    
    def start_dungeon(self, dungeon_id: str, player_stamina: int) -> Dict[str, Any]:
        """开始副本
        
        Returns:
            Dict with success, message, dungeon_run
        """
        self._refresh_daily_dungeons()
        
        dungeon = None
        for d in self.daily_dungeons:
            if d.id == dungeon_id:
                dungeon = d
                break
        
        if not dungeon:
            return {"success": False, "message": "副本不存在"}
        
        if dungeon.completed:
            return {"success": False, "message": "今日已完成该副本"}
        
        if player_stamina < dungeon.stamina_cost:
            return {"success": False, "message": f"体力不足，需要{dungeon.stamina_cost}点体力"}
        
        self.current_run = DungeonRun(dungeon=dungeon)
        
        return {
            "success": True,
            "message": f"进入{dungeon.name}！",
            "dungeon_run": self.current_run,
            "stamina_cost": dungeon.stamina_cost,
        }
    
    def get_next_monster(self) -> Optional[Monster]:
        """获取下一个怪物"""
        if not self.current_run:
            return None
        return self.current_run.next_wave()
    
    def complete_dungeon(self) -> Dict[str, Any]:
        """完成副本"""
        if not self.current_run:
            return {"success": False, "message": "没有在进行的副本"}
        
        dungeon = self.current_run.dungeon
        dungeon.completed = True
        rewards = self.current_run.get_final_reward()
        self.current_run = None
        
        return {
            "success": True,
            "message": f"完成副本{dungeon.name}！",
            "rewards": rewards,
        }
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "daily_dungeons": [d.to_dict() for d in self.daily_dungeons],
            "last_refresh": self.last_refresh.isoformat() if self.last_refresh else None,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DungeonManager":
        manager = cls()
        manager.daily_dungeons = [Dungeon.from_dict(d) for d in data.get("daily_dungeons", [])]
        
        last_refresh = data.get("last_refresh")
        if last_refresh:
            manager.last_refresh = datetime.fromisoformat(last_refresh)
        
        return manager
