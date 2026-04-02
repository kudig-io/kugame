"""挑战塔系统

无尽挑战塔，100层，每层难度递增。
"""
# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from enum import Enum
import random

from .story import Monster


@dataclass
class TowerLevel:
    """挑战塔层数据
    
    Attributes:
        level: 层数
        monster_name: 怪物名称
        monster_health: 怪物生命值
        monster_attack: 怪物攻击力
        monster_defense: 怪物防御力
        experience_reward: 经验奖励
        equipment_quality: 装备品质
        recommended_cultivation: 推荐境界等级
        clear_bonus: 通关奖励倍率
    """
    level: int
    monster_name: str
    monster_health: int
    monster_attack: int
    monster_defense: int
    experience_reward: int
    equipment_quality: int
    recommended_cultivation: int
    clear_bonus: float = 1.0
    
    def create_monster(self) -> Monster:
        """创建该层的怪物"""
        return Monster(
            name=f"第{self.level}层守卫·{self.monster_name}",
            health=self.monster_health,
            attack=self.monster_attack,
            defense=self.monster_defense,
            experience_reward=self.experience_reward,
            command_challenge="kubectl get pods",
            description=f"镇守着挑战塔第{self.level}层的强大怪物",
            level=self.level,
        )
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "level": self.level,
            "monster_name": self.monster_name,
            "monster_health": self.monster_health,
            "monster_attack": self.monster_attack,
            "monster_defense": self.monster_defense,
            "experience_reward": self.experience_reward,
            "equipment_quality": self.equipment_quality,
            "recommended_cultivation": self.recommended_cultivation,
            "clear_bonus": self.clear_bonus,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TowerLevel":
        return cls(
            level=data["level"],
            monster_name=data["monster_name"],
            monster_health=data["monster_health"],
            monster_attack=data["monster_attack"],
            monster_defense=data["monster_defense"],
            experience_reward=data["experience_reward"],
            equipment_quality=data["equipment_quality"],
            recommended_cultivation=data["recommended_cultivation"],
            clear_bonus=data.get("clear_bonus", 1.0),
        )


# 怪物名称库
MONSTER_NAMES = [
    "Pod傀儡", "Service幽灵", "Deployment巨兽", "ConfigMap守护者",
    "Secret潜伏者", "Volume吞噬者", "Namespace领主", "Node支配者",
    "Cluster核心", "Ingress看门人", "Scheduler裁决者", "Controller管理者",
]

# BOSS名称（每10层）
BOSS_NAMES = [
    "Pod之王", "Service女王", "Deployment霸主", "ConfigMap贤者",
    "Secret魔王", "Volume巨龙", "Namespace主宰", "Node泰坦",
    "Cluster之神", "Ingress天尊",
]


def generate_tower_levels(total_levels: int = 100) -> List[TowerLevel]:
    """生成挑战塔所有层数"""
    levels = []
    
    for i in range(1, total_levels + 1):
        # 基础属性随层数增长
        base_health = 50 + i * 8
        base_attack = 5 + i * 1.5
        base_defense = 2 + i * 0.5
        
        # BOSS层（每10层）
        is_boss = i % 10 == 0
        
        if is_boss:
            # BOSS属性大幅提升
            health = int(base_health * 2.5)
            attack = int(base_attack * 2)
            defense = int(base_defense * 2)
            exp_reward = 500 + i * 50
            equipment_quality = min(5, 2 + i // 20)  # BOSS给更好的装备
            monster_name = BOSS_NAMES[(i // 10) - 1] if (i // 10) <= len(BOSS_NAMES) else f"终极守卫{i}"
            clear_bonus = 2.0
        else:
            health = base_health
            attack = base_attack
            defense = base_defense
            exp_reward = 100 + i * 20
            equipment_quality = min(5, 1 + i // 25)
            monster_name = random.choice(MONSTER_NAMES)
            clear_bonus = 1.0
        
        # 推荐境界（每10层一个境界）
        recommended_cultivation = (i - 1) // 10 + 1
        
        level = TowerLevel(
            level=i,
            monster_name=monster_name,
            monster_health=health,
            monster_attack=attack,
            monster_defense=defense,
            experience_reward=exp_reward,
            equipment_quality=equipment_quality,
            recommended_cultivation=recommended_cultivation,
            clear_bonus=clear_bonus,
        )
        levels.append(level)
    
    return levels


@dataclass
class TowerProgress:
    """玩家挑战塔进度"""
    highest_level: int = 0  # 最高通关层数
    current_level: int = 1  # 当前挑战层数
    total_attempts: int = 0  # 总挑战次数
    total_clears: int = 0  # 总通关次数
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "highest_level": self.highest_level,
            "current_level": self.current_level,
            "total_attempts": self.total_attempts,
            "total_clears": self.total_clears,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TowerProgress":
        return cls(
            highest_level=data.get("highest_level", 0),
            current_level=data.get("current_level", 1),
            total_attempts=data.get("total_attempts", 0),
            total_clears=data.get("total_clears", 0),
        )


class ChallengeTower:
    """挑战塔管理器"""
    
    def __init__(self):
        self.levels: List[TowerLevel] = generate_tower_levels(100)
        self.current_run: Optional[TowerLevel] = None
    
    def get_level(self, level: int) -> Optional[TowerLevel]:
        """获取指定层数"""
        if 1 <= level <= len(self.levels):
            return self.levels[level - 1]
        return None
    
    def start_challenge(self, level: int, player_progress: TowerProgress) -> Dict[str, Any]:
        """开始挑战
        
        Args:
            level: 挑战层数
            player_progress: 玩家进度
            
        Returns:
            Dict with success, message, monster
        """
        if level < 1 or level > 100:
            return {"success": False, "message": "无效的层数"}
        
        # 只能挑战已通关层的下一层或以下
        if level > player_progress.highest_level + 1:
            return {
                "success": False, 
                "message": f"需要先通关第{player_progress.highest_level + 1}层"
            }
        
        tower_level = self.get_level(level)
        if not tower_level:
            return {"success": False, "message": "该层不存在"}
        
        self.current_run = tower_level
        player_progress.current_level = level
        player_progress.total_attempts += 1
        
        monster = tower_level.create_monster()
        
        return {
            "success": True,
            "message": f"开始挑战第{level}层！",
            "monster": monster,
            "tower_level": tower_level,
        }
    
    def complete_level(self, player_progress: TowerProgress) -> Dict[str, Any]:
        """完成当前层"""
        if not self.current_run:
            return {"success": False, "message": "没有在进行的挑战"}
        
        level = self.current_run.level
        
        # 更新最高通关层
        if level > player_progress.highest_level:
            player_progress.highest_level = level
        
        player_progress.total_clears += 1
        
        # 计算奖励
        base_exp = self.current_run.experience_reward
        bonus_exp = int(base_exp * self.current_run.clear_bonus)
        
        rewards = {
            "experience": bonus_exp,
            "equipment_quality": self.current_run.equipment_quality,
            "level": level,
            "is_new_record": level == player_progress.highest_level,
        }
        
        self.current_run = None
        
        return {
            "success": True,
            "message": f"恭喜通关第{level}层！" + ("[新纪录！]" if rewards["is_new_record"] else ""),
            "rewards": rewards,
        }
    
    def get_ranking(self, player_progress: TowerProgress) -> str:
        """获取排名描述"""
        level = player_progress.highest_level
        
        if level >= 100:
            return "🏆 通天塔主"
        elif level >= 90:
            return "🥇 塔之王者"
        elif level >= 80:
            return "🥈 塔之大师"
        elif level >= 60:
            return "🥉 塔之勇士"
        elif level >= 40:
            return "⭐ 塔之先锋"
        elif level >= 20:
            return "✨ 塔之新秀"
        else:
            return "💫 初入塔门"
    
    def get_level_status(self, level: int, player_progress: TowerProgress) -> str:
        """获取层数状态"""
        if level <= player_progress.highest_level:
            return "✓ 已通关"
        elif level == player_progress.highest_level + 1:
            return "→ 可挑战"
        else:
            return "✗ 未解锁"
