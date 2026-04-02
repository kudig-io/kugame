"""装备系统

管理游戏中的装备，包括装备类型、品质、属性和强化系统。
"""
# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from enum import Enum
import random


class EquipmentType(Enum):
    """装备类型枚举
    
    定义不同类型的装备及其对应的属性加成。
    """
    武器 = "weapon"      # 增加攻击力
    护甲 = "armor"       # 增加防御力
    饰品 = "accessory"   # 增加生命值或特殊效果


class EquipmentQuality(Enum):
    """装备品质枚举
    
    定义装备的品质等级，从普通到传说。
    """
    普通 = (1, "白色", 1.0)      # 基础属性
    精良 = (2, "绿色", 1.3)      # 属性提升30%
    稀有 = (3, "蓝色", 1.6)      # 属性提升60%
    史诗 = (4, "紫色", 2.0)      # 属性翻倍
    传说 = (5, "橙色", 2.5)      # 属性提升150%
    
    def __init__(self, level: int, color: str, multiplier: float):
        self.level = level
        self.color = color
        self.multiplier = multiplier


@dataclass
class Equipment:
    """装备数据类
    
    存储装备的详细信息，包括名称、类型、品质、属性等。
    
    Attributes:
        id: 装备唯一标识
        name: 装备名称
        equipment_type: 装备类型
        quality: 装备品质
        level: 装备等级（用于强化）
        attack_bonus: 攻击加成
        defense_bonus: 防御加成
        health_bonus: 生命值加成
        exp_bonus: 经验值加成百分比
        streak_bonus: 连击加成百分比
        description: 装备描述
        equipped: 是否已装备
    """
    id: str
    name: str
    equipment_type: EquipmentType
    quality: EquipmentQuality
    level: int = 1
    attack_bonus: int = 0
    defense_bonus: int = 0
    health_bonus: int = 0
    exp_bonus: float = 0.0
    streak_bonus: float = 0.0
    description: str = ""
    equipped: bool = False
    
    def __post_init__(self) -> None:
        """初始化后处理
        
        确保装备等级有效，应用品质加成。
        """
        if self.level < 1:
            self.level = 1
        
        # 如果描述为空，生成默认描述
        if not self.description:
            self.description = f"{self.quality.color}品质的{self.name}"
    
    @property
    def total_attack(self) -> int:
        """计算总攻击力加成（包含等级和品质加成）"""
        base = self.attack_bonus * self.quality.multiplier
        level_bonus = 1 + (self.level - 1) * 0.1  # 每级提升10%
        return int(base * level_bonus)
    
    @property
    def total_defense(self) -> int:
        """计算总防御力加成（包含等级和品质加成）"""
        base = self.defense_bonus * self.quality.multiplier
        level_bonus = 1 + (self.level - 1) * 0.1
        return int(base * level_bonus)
    
    @property
    def total_health(self) -> int:
        """计算总生命值加成（包含等级和品质加成）"""
        base = self.health_bonus * self.quality.multiplier
        level_bonus = 1 + (self.level - 1) * 0.1
        return int(base * level_bonus)
    
    @property
    def display_name(self) -> str:
        """获取显示名称（包含品质和等级）"""
        if self.level > 1:
            return f"[{self.quality.color}]{self.name}+{(self.level - 1)}"
        return f"[{self.quality.color}]{self.name}"
    
    def upgrade(self) -> bool:
        """强化装备
        
        提升装备等级，增强属性。
        
        Returns:
            bool: 强化成功返回True，已达到最高等级返回False
        """
        max_level = 5 + self.quality.level  # 品质越高，可强化次数越多
        if self.level < max_level:
            self.level += 1
            return True
        return False
    
    def get_upgrade_cost(self) -> int:
        """获取升级所需经验值
        
        Returns:
            int: 升级所需的经验值
        """
        base_cost = 100 * self.quality.level
        level_multiplier = 1.5 ** (self.level - 1)
        return int(base_cost * level_multiplier)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典
        
        Returns:
            Dict[str, Any]: 装备数据字典
        """
        return {
            "id": self.id,
            "name": self.name,
            "equipment_type": self.equipment_type.value,
            "quality": self.quality.name,
            "level": self.level,
            "attack_bonus": self.attack_bonus,
            "defense_bonus": self.defense_bonus,
            "health_bonus": self.health_bonus,
            "exp_bonus": self.exp_bonus,
            "streak_bonus": self.streak_bonus,
            "description": self.description,
            "equipped": self.equipped,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Equipment":
        """从字典创建装备
        
        Args:
            data: 装备数据字典
            
        Returns:
            Equipment: 装备对象
        """
        return cls(
            id=data["id"],
            name=data["name"],
            equipment_type=EquipmentType(data["equipment_type"]),
            quality=EquipmentQuality[data["quality"]],
            level=data.get("level", 1),
            attack_bonus=data.get("attack_bonus", 0),
            defense_bonus=data.get("defense_bonus", 0),
            health_bonus=data.get("health_bonus", 0),
            exp_bonus=data.get("exp_bonus", 0.0),
            streak_bonus=data.get("streak_bonus", 0.0),
            description=data.get("description", ""),
            equipped=data.get("equipped", False),
        )


# 装备模板库
EQUIPMENT_TEMPLATES = {
    EquipmentType.武器: [
        {"name": "木剑", "attack": 5, "defense": 0, "health": 0, "exp": 0, "streak": 0},
        {"name": "铁剑", "attack": 10, "defense": 0, "health": 0, "exp": 0, "streak": 0},
        {"name": "精钢剑", "attack": 15, "defense": 0, "health": 0, "exp": 0, "streak": 0},
        {"name": "青云剑", "attack": 20, "defense": 0, "health": 0, "exp": 0.05, "streak": 0},
        {"name": "玄铁重剑", "attack": 25, "defense": 5, "health": 0, "exp": 0, "streak": 0},
        {"name": "赤焰刀", "attack": 30, "defense": 0, "health": 0, "exp": 0, "streak": 0.1},
        {"name": "龙吟剑", "attack": 40, "defense": 0, "health": 10, "exp": 0.1, "streak": 0},
        {"name": "诛仙剑", "attack": 60, "defense": 0, "health": 0, "exp": 0.15, "streak": 0.1},
    ],
    EquipmentType.护甲: [
        {"name": "布衣", "attack": 0, "defense": 3, "health": 10, "exp": 0, "streak": 0},
        {"name": "皮甲", "attack": 0, "defense": 6, "health": 20, "exp": 0, "streak": 0},
        {"name": "铁甲", "attack": 0, "defense": 10, "health": 30, "exp": 0, "streak": 0},
        {"name": "精钢甲", "attack": 0, "defense": 15, "health": 50, "exp": 0, "streak": 0},
        {"name": "玄天战甲", "attack": 5, "defense": 20, "health": 80, "exp": 0.05, "streak": 0},
        {"name": "金刚护体", "attack": 0, "defense": 30, "health": 100, "exp": 0, "streak": 0},
        {"name": "龙鳞甲", "attack": 0, "defense": 40, "health": 150, "exp": 0.08, "streak": 0},
        {"name": "不朽金身", "attack": 10, "defense": 50, "health": 200, "exp": 0.1, "streak": 0},
    ],
    EquipmentType.饰品: [
        {"name": "木戒指", "attack": 0, "defense": 0, "health": 5, "exp": 0.02, "streak": 0},
        {"name": "铁护符", "attack": 2, "defense": 2, "health": 10, "exp": 0, "streak": 0},
        {"name": "玉佩", "attack": 0, "defense": 0, "health": 20, "exp": 0.05, "streak": 0},
        {"name": "灵珠", "attack": 3, "defense": 0, "health": 15, "exp": 0.08, "streak": 0.05},
        {"name": "乾坤戒", "attack": 5, "defense": 5, "health": 30, "exp": 0.1, "streak": 0},
        {"name": "聚灵项链", "attack": 0, "defense": 0, "health": 25, "exp": 0.15, "streak": 0.05},
        {"name": "龙魂玉", "attack": 8, "defense": 8, "health": 50, "exp": 0.12, "streak": 0.08},
        {"name": "混沌至宝", "attack": 15, "defense": 15, "health": 100, "exp": 0.2, "streak": 0.15},
    ],
}


class EquipmentManager:
    """装备管理器
    
    管理装备的生成、强化和商店系统。
    
    Attributes:
        equipment_counter: 装备ID计数器
    """
    
    def __init__(self) -> None:
        """初始化装备管理器"""
        self.equipment_counter = 0
    
    def _generate_equipment_id(self) -> str:
        """生成唯一装备ID
        
        Returns:
            str: 装备唯一标识
        """
        self.equipment_counter += 1
        return f"eq_{self.equipment_counter}_{random.randint(1000, 9999)}"
    
    def generate_equipment(
        self, 
        equipment_type: Optional[EquipmentType] = None,
        quality: Optional[EquipmentQuality] = None,
        player_level: int = 1
    ) -> Equipment:
        """生成装备
        
        根据类型、品质和玩家等级生成装备。
        
        Args:
            equipment_type: 装备类型，随机选择如果为None
            quality: 装备品质，根据玩家等级计算如果为None
            player_level: 玩家等级，影响装备基础属性
            
        Returns:
            Equipment: 生成的装备
        """
        # 随机选择装备类型
        if equipment_type is None:
            equipment_type = random.choice(list(EquipmentType))
        
        # 根据玩家等级计算品质概率
        if quality is None:
            quality = self._calculate_quality(player_level)
        
        # 从模板库选择合适的装备
        templates = EQUIPMENT_TEMPLATES[equipment_type]
        
        # 根据玩家等级选择装备模板
        template_index = min(len(templates) - 1, (player_level - 1) // 10)
        # 随机选择同级或稍低级的装备
        template_index = max(0, template_index - random.randint(0, 1))
        template = templates[template_index]
        
        # 创建装备
        equipment = Equipment(
            id=self._generate_equipment_id(),
            name=template["name"],
            equipment_type=equipment_type,
            quality=quality,
            attack_bonus=template["attack"],
            defense_bonus=template["defense"],
            health_bonus=template["health"],
            exp_bonus=template["exp"],
            streak_bonus=template["streak"],
            description=f"{quality.color}品质的{template['name']}",
        )
        
        return equipment
    
    def _calculate_quality(self, player_level: int) -> EquipmentQuality:
        """根据玩家等级计算装备品质
        
        Args:
            player_level: 玩家等级
            
        Returns:
            EquipmentQuality: 装备品质
        """
        # 品质概率随等级提升
        qualities = list(EquipmentQuality)
        weights = []
        
        for q in qualities:
            # 基础概率
            base_prob = 1.0 / q.level
            # 等级加成（高等级玩家更容易获得高品质）
            level_bonus = player_level / 100.0 * (q.level - 1)
            weights.append(base_prob + level_bonus)
        
        # 归一化权重
        total = sum(weights)
        weights = [w / total for w in weights]
        
        # 根据权重随机选择
        return random.choices(qualities, weights=weights)[0]
    
    def generate_drop(self, monster_level: int, player_level: int) -> Optional[Equipment]:
        """生成战斗掉落装备
        
        Args:
            monster_level: 怪物等级
            player_level: 玩家等级
            
        Returns:
            Optional[Equipment]: 掉落的装备，可能为None
        """
        # 基础掉落概率30%
        drop_chance = 0.3
        # 怪物等级越高，掉落概率越高
        drop_chance += monster_level * 0.02
        
        if random.random() > drop_chance:
            return None
        
        # 根据怪物等级调整品质概率
        effective_level = max(player_level, monster_level)
        return self.generate_equipment(player_level=effective_level)
    
    def get_shop_equipment(self, player_level: int) -> List[Equipment]:
        """获取商店装备列表
        
        根据玩家等级生成商店可购买的装备。
        
        Args:
            player_level: 玩家等级
            
        Returns:
            List[Equipment]: 商店装备列表
        """
        shop_items = []
        
        # 生成6件装备（每种类型2件）
        for eq_type in EquipmentType:
            for _ in range(2):
                # 商店装备品质至少为精良
                quality = self._calculate_shop_quality(player_level)
                equipment = self.generate_equipment(
                    equipment_type=eq_type,
                    quality=quality,
                    player_level=player_level
                )
                shop_items.append(equipment)
        
        return shop_items
    
    def _calculate_shop_quality(self, player_level: int) -> EquipmentQuality:
        """计算商店装备品质
        
        商店装备品质通常比掉落装备好。
        
        Args:
            player_level: 玩家等级
            
        Returns:
            EquipmentQuality: 装备品质
        """
        qualities = list(EquipmentQuality)
        weights = []
        
        for q in qualities:
            # 商店装备品质更高
            if q == EquipmentQuality.普通:
                weights.append(0.1)  # 极低概率出现普通
            elif q == EquipmentQuality.精良:
                weights.append(0.4)
            elif q == EquipmentQuality.稀有:
                weights.append(0.3 + player_level * 0.005)
            elif q == EquipmentQuality.史诗:
                weights.append(0.15 + player_level * 0.003)
            else:  # 传说
                weights.append(0.05 + player_level * 0.002)
        
        # 归一化
        total = sum(weights)
        weights = [w / total for w in weights]
        
        return random.choices(qualities, weights=weights)[0]
    
    def calculate_sell_price(self, equipment: Equipment) -> int:
        """计算装备出售价格
        
        Args:
            equipment: 装备
            
        Returns:
            int: 出售价格（经验值）
        """
        base_price = 50 * equipment.quality.level
        level_bonus = (equipment.level - 1) * 20
        return base_price + level_bonus
    
    def calculate_buy_price(self, equipment: Equipment) -> int:
        """计算装备购买价格
        
        Args:
            equipment: 装备
            
        Returns:
            int: 购买价格（经验值）
        """
        # 购买价格是出售价格的3倍
        return self.calculate_sell_price(equipment) * 3


# 装备品质颜色映射（用于显示）
QUALITY_COLORS = {
    EquipmentQuality.普通: "white",
    EquipmentQuality.精良: "green",
    EquipmentQuality.稀有: "blue",
    EquipmentQuality.史诗: "magenta",
    EquipmentQuality.传说: "yellow",
}
