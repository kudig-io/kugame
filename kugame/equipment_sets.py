"""装备套装系统

提供装备套装效果，收集多件同套装装备激活额外属性加成。
"""
# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import Dict, List, Optional, Any
from enum import Enum


class SetBonusType(Enum):
    """套装加成类型"""
    攻击力 = "attack"
    防御力 = "defense"
    生命值 = "health"
    经验加成 = "exp_bonus"
    连击加成 = "streak_bonus"
    暴击率 = "crit_rate"
    闪避率 = "dodge_rate"
    技能冷却 = "cooldown_reduction"


@dataclass
class SetBonus:
    """套装加成效果
    
    Attributes:
        required_pieces: 需要的装备件数
        bonus_type: 加成类型
        bonus_value: 加成数值（百分比或固定值）
        description: 效果描述
    """
    required_pieces: int
    bonus_type: SetBonusType
    bonus_value: float
    description: str


@dataclass
class EquipmentSet:
    """装备套装
    
    Attributes:
        id: 套装ID
        name: 套装名称
        description: 套装描述
        pieces: 套装包含的装备名称列表
        bonuses: 套装加成效果列表
        quality_level: 套装品质等级
    """
    id: str
    name: str
    description: str
    pieces: List[str]
    bonuses: List[SetBonus]
    quality_level: int = 1  # 1-5, 对应白绿蓝紫橙


# 定义装备套装
EQUIPMENT_SETS = {
    # 新手套装
    "novice_set": EquipmentSet(
        id="novice_set",
        name="新手套装",
        description="初入仙门的弟子所穿的基础装备，虽无特别之处，但胜在稳定可靠",
        pieces=["新手长剑", "新手护甲", "新手护符"],
        bonuses=[
            SetBonus(2, SetBonusType.攻击力, 5, "2件套：攻击+5"),
            SetBonus(3, SetBonusType.生命值, 20, "3件套：生命+20"),
        ],
        quality_level=1,
    ),
    
    # 青云套装
    "qingyun_set": EquipmentSet(
        id="qingyun_set",
        name="青云套装",
        description="青云宗弟子专属装备，蕴含正道之气，攻守兼备",
        pieces=["青云剑", "青云道袍", "青云玉佩"],
        bonuses=[
            SetBonus(2, SetBonusType.防御力, 10, "2件套：防御+10"),
            SetBonus(3, SetBonusType.经验加成, 0.1, "3件套：经验获取+10%"),
        ],
        quality_level=2,
    ),
    
    # 炼狱套装
    "lianyu_set": EquipmentSet(
        id="lianyu_set",
        name="炼狱套装",
        description="炼狱门弟子专属装备，嗜血狂暴，攻击力惊人",
        pieces=["炼狱刀", "炼狱战甲", "炼狱戒指"],
        bonuses=[
            SetBonus(2, SetBonusType.攻击力, 15, "2件套：攻击+15"),
            SetBonus(3, SetBonusType.暴击率, 0.15, "3件套：暴击率+15%"),
        ],
        quality_level=2,
    ),
    
    # 玄天套装
    "xuantian_set": EquipmentSet(
        id="xuantian_set",
        name="玄天套装",
        description="玄天宗弟子专属装备，玄妙莫测，闪避率极高",
        pieces=["玄天扇", "玄天法衣", "玄天珠"],
        bonuses=[
            SetBonus(2, SetBonusType.闪避率, 0.1, "2件套：闪避率+10%"),
            SetBonus(3, SetBonusType.技能冷却, 0.2, "3件套：技能冷却-20%"),
        ],
        quality_level=2,
    ),
    
    # 逍遥套装
    "xiaoyao_set": EquipmentSet(
        id="xiaoyao_set",
        name="逍遥套装",
        description="逍遥派弟子专属装备，逍遥自在，连击效果显著",
        pieces=["逍遥笛", "逍遥衫", "逍遥坠"],
        bonuses=[
            SetBonus(2, SetBonusType.连击加成, 0.1, "2件套：连击加成+10%"),
            SetBonus(3, SetBonusType.经验加成, 0.15, "3件套：经验获取+15%"),
        ],
        quality_level=2,
    ),
    
    # 龙鳞套装
    "dragon_set": EquipmentSet(
        id="dragon_set",
        name="龙鳞套装",
        description="以龙鳞打造的上古神装，稀有品质，属性全面",
        pieces=["龙鳞剑", "龙鳞甲", "龙鳞护符", "龙鳞戒指"],
        bonuses=[
            SetBonus(2, SetBonusType.攻击力, 20, "2件套：攻击+20"),
            SetBonus(3, SetBonusType.防御力, 15, "3件套：防御+15"),
            SetBonus(4, SetBonusType.生命值, 50, "4件套：生命+50"),
        ],
        quality_level=3,
    ),
    
    # 凤羽套装
    "phoenix_set": EquipmentSet(
        id="phoenix_set",
        name="凤羽套装",
        description="以凤凰羽毛编织的史诗装备，火焰之力环绕",
        pieces=["凤羽扇", "凤羽袍", "凤羽项链", "凤羽手镯"],
        bonuses=[
            SetBonus(2, SetBonusType.经验加成, 0.15, "2件套：经验获取+15%"),
            SetBonus(3, SetBonusType.连击加成, 0.15, "3件套：连击加成+15%"),
            SetBonus(4, SetBonusType.攻击力, 30, "4件套：攻击+30"),
        ],
        quality_level=4,
    ),
    
    # 混元套装（传说）
    "hunyuan_set": EquipmentSet(
        id="hunyuan_set",
        name="混元套装",
        description="传说中的混元级装备，集天地精华，拥有毁天灭地之力",
        pieces=["混元剑", "混元甲", "混元护符", "混元戒指", "混元腰带"],
        bonuses=[
            SetBonus(2, SetBonusType.攻击力, 50, "2件套：攻击+50"),
            SetBonus(3, SetBonusType.防御力, 40, "3件套：防御+40"),
            SetBonus(4, SetBonusType.生命值, 100, "4件套：生命+100"),
            SetBonus(5, SetBonusType.经验加成, 0.3, "5件套：经验获取+30%"),
        ],
        quality_level=5,
    ),
}


def get_equipment_set(equipment_name: str) -> Optional[EquipmentSet]:
    """获取装备所属的套装
    
    Args:
        equipment_name: 装备名称
        
    Returns:
        Optional[EquipmentSet]: 所属套装，如果不属于任何套装则返回None
    """
    for eq_set in EQUIPMENT_SETS.values():
        if equipment_name in eq_set.pieces:
            return eq_set
    return None


def calculate_set_bonuses(equipped_names: List[str]) -> Dict[str, Any]:
    """计算当前装备的套装加成
    
    Args:
        equipped_names: 已装备的物品名称列表
        
    Returns:
        Dict: 加成效果字典
    """
    # 统计各套装装备数量
    set_counts: Dict[str, int] = {}
    set_equipment: Dict[str, List[str]] = {}
    
    for name in equipped_names:
        eq_set = get_equipment_set(name)
        if eq_set:
            set_counts[eq_set.id] = set_counts.get(eq_set.id, 0) + 1
            if eq_set.id not in set_equipment:
                set_equipment[eq_set.id] = []
            set_equipment[eq_set.id].append(name)
    
    # 计算加成
    total_bonuses = {
        "attack": 0,
        "defense": 0,
        "health": 0,
        "exp_bonus": 0.0,
        "streak_bonus": 0.0,
        "crit_rate": 0.0,
        "dodge_rate": 0.0,
        "cooldown_reduction": 0.0,
    }
    
    active_sets = []
    
    for set_id, count in set_counts.items():
        eq_set = EQUIPMENT_SETS[set_id]
        active_bonuses = []
        
        for bonus in eq_set.bonuses:
            if count >= bonus.required_pieces:
                # 应用加成
                bonus_key = bonus.bonus_type.value
                if bonus_key in total_bonuses:
                    total_bonuses[bonus_key] += bonus.bonus_value
                active_bonuses.append(bonus.description)
        
        if active_bonuses:
            active_sets.append({
                "set_name": eq_set.name,
                "pieces_equipped": count,
                "total_pieces": len(eq_set.pieces),
                "active_bonuses": active_bonuses,
            })
    
    return {
        "bonuses": total_bonuses,
        "active_sets": active_sets,
    }


def get_set_collection_progress(inventory_names: List[str]) -> List[Dict[str, Any]]:
    """获取套装收集进度
    
    Args:
        inventory_names: 背包中所有装备名称列表
        
    Returns:
        List[Dict]: 各套装的收集进度
    """
    progress = []
    
    for eq_set in EQUIPMENT_SETS.values():
        collected = [name for name in eq_set.pieces if name in inventory_names]
        progress.append({
            "set_id": eq_set.id,
            "set_name": eq_set.name,
            "description": eq_set.description,
            "quality_level": eq_set.quality_level,
            "collected_count": len(collected),
            "total_count": len(eq_set.pieces),
            "collected_pieces": collected,
            "missing_pieces": [name for name in eq_set.pieces if name not in inventory_names],
            "bonuses": [
                {
                    "required": b.required_pieces,
                    "description": b.description,
                    "active": len(collected) >= b.required_pieces,
                }
                for b in eq_set.bonuses
            ],
        })
    
    return sorted(progress, key=lambda x: x["quality_level"])
