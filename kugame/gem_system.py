"""宝石镶嵌系统

提供宝石获取、镶嵌、合成等功能，增强装备属性。
"""
# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from enum import Enum
import random


class GemType(Enum):
    """宝石类型"""
    攻击宝石 = "attack"
    防御宝石 = "defense"
    生命宝石 = "health"
    经验宝石 = "exp"
    连击宝石 = "streak"
    暴击宝石 = "crit"


class GemQuality(Enum):
    """宝石品质"""
    普通 = (1, "白色", 1.0)
    精良 = (2, "绿色", 1.5)
    稀有 = (3, "蓝色", 2.0)
    史诗 = (4, "紫色", 3.0)
    传说 = (5, "橙色", 5.0)
    
    def __init__(self, level, color, multiplier):
        self.level = level
        self.color = color
        self.multiplier = multiplier


@dataclass
class Gem:
    """宝石
    
    Attributes:
        id: 宝石唯一ID
        name: 宝石名称
        gem_type: 宝石类型
        quality: 宝石品质
        level: 宝石等级
        base_value: 基础数值
    """
    id: str
    name: str
    gem_type: GemType
    quality: GemQuality
    level: int = 1
    base_value: float = 0.0
    
    @property
    def total_value(self) -> float:
        """计算总数值（考虑品质和等级）"""
        return self.base_value * self.quality.multiplier * (1 + (self.level - 1) * 0.2)
    
    @property
    def display_name(self) -> str:
        """显示名称"""
        quality_prefix = {
            GemQuality.普通: "",
            GemQuality.精良: "精良",
            GemQuality.稀有: "稀有",
            GemQuality.史诗: "史诗",
            GemQuality.传说: "传说",
        }
        prefix = quality_prefix.get(self.quality, "")
        if prefix:
            return f"[{prefix}]{self.name}+{self.level}"
        return f"{self.name}+{self.level}"
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "id": self.id,
            "name": self.name,
            "gem_type": self.gem_type.value,
            "quality": self.quality.name,
            "level": self.level,
            "base_value": self.base_value,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Gem":
        """从字典创建"""
        return cls(
            id=data["id"],
            name=data["name"],
            gem_type=GemType(data["gem_type"]),
            quality=GemQuality[data["quality"]],
            level=data.get("level", 1),
            base_value=data.get("base_value", 0.0),
        )


# 宝石模板
GEM_TEMPLATES = {
    GemType.攻击宝石: {"name": "红宝石", "base_value": 5},
    GemType.防御宝石: {"name": "蓝宝石", "base_value": 3},
    GemType.生命宝石: {"name": "绿宝石", "base_value": 10},
    GemType.经验宝石: {"name": "黄宝石", "base_value": 0.02},
    GemType.连击宝石: {"name": "紫宝石", "base_value": 0.01},
    GemType.暴击宝石: {"name": "橙宝石", "base_value": 0.01},
}


def create_gem(gem_type: GemType, quality: GemQuality, level: int = 1) -> Gem:
    """创建宝石
    
    Args:
        gem_type: 宝石类型
        quality: 宝石品质
        level: 宝石等级
        
    Returns:
        Gem: 创建的宝石
    """
    template = GEM_TEMPLATES[gem_type]
    gem_id = f"gem_{gem_type.value}_{quality.name}_{random.randint(1000, 9999)}"
    
    return Gem(
        id=gem_id,
        name=template["name"],
        gem_type=gem_type,
        quality=quality,
        level=level,
        base_value=template["base_value"],
    )


def generate_random_gem(min_quality: GemQuality = GemQuality.普通, 
                       max_quality: GemQuality = GemQuality.传说) -> Gem:
    """生成随机宝石
    
    Args:
        min_quality: 最低品质
        max_quality: 最高品质
        
    Returns:
        Gem: 随机宝石
    """
    gem_type = random.choice(list(GemType))
    
    # 根据品质等级随机选择
    qualities = [q for q in GemQuality if min_quality.level <= q.level <= max_quality.level]
    quality = random.choice(qualities)
    
    # 根据品质决定等级范围
    if quality == GemQuality.普通:
        level = random.randint(1, 2)
    elif quality == GemQuality.精良:
        level = random.randint(1, 3)
    elif quality == GemQuality.稀有:
        level = random.randint(1, 4)
    elif quality == GemQuality.史诗:
        level = random.randint(1, 5)
    else:  # 传说
        level = random.randint(1, 6)
    
    return create_gem(gem_type, quality, level)


@dataclass
class GemSlot:
    """宝石槽位
    
    Attributes:
        slot_id: 槽位ID
        gem_type: 允许镶嵌的宝石类型（None表示通用）
        equipped_gem: 已镶嵌的宝石
        is_locked: 是否锁定
        unlock_level: 解锁等级
    """
    slot_id: int
    gem_type: Optional[GemType] = None
    equipped_gem: Optional[Gem] = None
    is_locked: bool = False
    unlock_level: int = 1
    
    @property
    def is_empty(self) -> bool:
        """槽位是否为空"""
        return self.equipped_gem is None
    
    def can_equip(self, gem: Gem) -> bool:
        """检查是否可以镶嵌宝石"""
        if self.is_locked:
            return False
        if self.gem_type is not None and gem.gem_type != self.gem_type:
            return False
        return True
    
    def equip(self, gem: Gem) -> bool:
        """镶嵌宝石
        
        Returns:
            bool: 是否成功
        """
        if not self.can_equip(gem):
            return False
        self.equipped_gem = gem
        return True
    
    def unequip(self) -> Optional[Gem]:
        """卸下宝石
        
        Returns:
            Optional[Gem]: 卸下的宝石
        """
        gem = self.equipped_gem
        self.equipped_gem = None
        return gem
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "slot_id": self.slot_id,
            "gem_type": self.gem_type.value if self.gem_type else None,
            "equipped_gem": self.equipped_gem.to_dict() if self.equipped_gem else None,
            "is_locked": self.is_locked,
            "unlock_level": self.unlock_level,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "GemSlot":
        """从字典创建"""
        return cls(
            slot_id=data["slot_id"],
            gem_type=GemType(data["gem_type"]) if data.get("gem_type") else None,
            equipped_gem=Gem.from_dict(data["equipped_gem"]) if data.get("equipped_gem") else None,
            is_locked=data.get("is_locked", False),
            unlock_level=data.get("unlock_level", 1),
        )


def can_merge_gems(gem1: Gem, gem2: Gem) -> bool:
    """检查两颗宝石是否可以合成
    
    合成规则：
    - 同类型
    - 同品质
    - 同等级
    
    Returns:
        bool: 是否可以合成
    """
    return (gem1.gem_type == gem2.gem_type and
            gem1.quality == gem2.quality and
            gem1.level == gem2.level)


def merge_gems(gem1: Gem, gem2: Gem) -> Optional[Gem]:
    """合成两颗宝石
    
    Args:
        gem1: 第一颗宝石
        gem2: 第二颗宝石
        
    Returns:
        Optional[Gem]: 合成后的宝石，失败返回None
    """
    if not can_merge_gems(gem1, gem2):
        return None
    
    # 等级+1，品质不变
    new_level = gem1.level + 1
    
    # 如果等级超过品质上限，提升品质
    quality_upgrade_threshold = {
        GemQuality.普通: 3,
        GemQuality.精良: 4,
        GemQuality.稀有: 5,
        GemQuality.史诗: 6,
        GemQuality.传说: 10,
    }
    
    new_quality = gem1.quality
    if new_level > quality_upgrade_threshold[gem1.quality]:
        # 尝试提升品质
        quality_order = [GemQuality.普通, GemQuality.精良, GemQuality.稀有, 
                        GemQuality.史诗, GemQuality.传说]
        current_index = quality_order.index(gem1.quality)
        if current_index < len(quality_order) - 1:
            new_quality = quality_order[current_index + 1]
            new_level = 1
    
    return create_gem(gem1.gem_type, new_quality, new_level)


class GemInventory:
    """宝石背包"""
    
    def __init__(self, max_slots: int = 50):
        self.gems: List[Gem] = []
        self.max_slots = max_slots
    
    def add_gem(self, gem: Gem) -> bool:
        """添加宝石到背包"""
        if len(self.gems) >= self.max_slots:
            return False
        self.gems.append(gem)
        return True
    
    def remove_gem(self, gem_id: str) -> Optional[Gem]:
        """从背包移除宝石"""
        for i, gem in enumerate(self.gems):
            if gem.id == gem_id:
                return self.gems.pop(i)
        return None
    
    def get_gems_by_type(self, gem_type: GemType) -> List[Gem]:
        """按类型获取宝石"""
        return [g for g in self.gems if g.gem_type == gem_type]
    
    def get_mergeable_pairs(self) -> List[tuple]:
        """获取可以合成的宝石对"""
        pairs = []
        checked = set()
        
        for i, gem1 in enumerate(self.gems):
            if gem1.id in checked:
                continue
            for j, gem2 in enumerate(self.gems[i+1:], i+1):
                if gem2.id in checked:
                    continue
                if can_merge_gems(gem1, gem2):
                    pairs.append((gem1, gem2))
                    checked.add(gem1.id)
                    checked.add(gem2.id)
                    break
        
        return pairs
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "gems": [g.to_dict() for g in self.gems],
            "max_slots": self.max_slots,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "GemInventory":
        """从字典创建"""
        inventory = cls(data.get("max_slots", 50))
        inventory.gems = [Gem.from_dict(g) for g in data.get("gems", [])]
        return inventory
