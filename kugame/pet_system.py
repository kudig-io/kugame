"""宠物系统

提供宠物获取、培养、战斗、进化等功能。
"""
# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from enum import Enum
import random


class PetType(Enum):
    """宠物类型"""
    攻击型 = "attack"
    防御型 = "defense"
    辅助型 = "support"
    平衡型 = "balanced"


class PetRarity(Enum):
    """宠物稀有度"""
    普通 = (1, "白色", 1.0)
    稀有 = (2, "绿色", 1.2)
    精良 = (3, "蓝色", 1.5)
    史诗 = (4, "紫色", 2.0)
    传说 = (5, "橙色", 3.0)
    神话 = (6, "红色", 5.0)
    
    def __init__(self, level, color, multiplier):
        self.level = level
        self.color_name = color
        self.multiplier = multiplier


class PetStatus(Enum):
    """宠物状态"""
    休息中 = "resting"
    跟随中 = "following"
    战斗中 = "fighting"
    训练中 = "training"


@dataclass
class PetSkill:
    """宠物技能
    
    Attributes:
        skill_id: 技能ID
        name: 技能名称
        description: 技能描述
        effect_type: 效果类型
        effect_value: 效果数值
        cooldown: 冷却回合
        current_cooldown: 当前冷却
    """
    skill_id: str
    name: str
    description: str
    effect_type: str  # attack, heal, buff, debuff
    effect_value: float
    cooldown: int = 3
    current_cooldown: int = 0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "skill_id": self.skill_id,
            "name": self.name,
            "description": self.description,
            "effect_type": self.effect_type,
            "effect_value": self.effect_value,
            "cooldown": self.cooldown,
            "current_cooldown": self.current_cooldown,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PetSkill":
        return cls(
            skill_id=data["skill_id"],
            name=data["name"],
            description=data["description"],
            effect_type=data["effect_type"],
            effect_value=data["effect_value"],
            cooldown=data.get("cooldown", 3),
            current_cooldown=data.get("current_cooldown", 0),
        )


@dataclass
class Pet:
    """宠物
    
    Attributes:
        id: 宠物唯一ID
        name: 宠物名称
        pet_type: 宠物类型
        rarity: 稀有度
        level: 等级
        exp: 当前经验
        exp_to_level: 升级所需经验
        
        # 基础属性
        attack: 攻击力
        defense: 防御力
        health: 生命值
        max_health: 最大生命值
        
        # 成长属性
        attack_growth: 攻击成长
        defense_growth: 防御成长
        health_growth: 生命成长
        
        # 其他
        loyalty: 忠诚度 (0-100)
        mood: 心情 (0-100)
        status: 当前状态
        skills: 技能列表
        evolution_stage: 进化阶段 (0-3)
        is_active: 是否出战
        
        # 外观
        appearance: 外观描述
    """
    id: str
    name: str
    pet_type: PetType
    rarity: PetRarity
    level: int = 1
    exp: int = 0
    exp_to_level: int = 100
    
    attack: int = 10
    defense: int = 5
    health: int = 100
    max_health: int = 100
    
    attack_growth: float = 2.0
    defense_growth: float = 1.0
    health_growth: float = 10.0
    
    loyalty: int = 50
    mood: int = 50
    status: PetStatus = PetStatus.休息中
    skills: List[PetSkill] = field(default_factory=list)
    evolution_stage: int = 0
    is_active: bool = False
    
    appearance: str = ""
    
    @property
    def total_attack(self) -> int:
        """计算总攻击力（包含稀有度加成）"""
        return int(self.attack * self.rarity.multiplier)
    
    @property
    def total_defense(self) -> int:
        """计算总防御力"""
        return int(self.defense * self.rarity.multiplier)
    
    @property
    def total_health(self) -> int:
        """计算总生命值"""
        return int(self.max_health * self.rarity.multiplier)
    
    @property
    def display_name(self) -> str:
        """显示名称"""
        rarity_prefix = {
            PetRarity.普通: "",
            PetRarity.稀有: "[稀有]",
            PetRarity.精良: "[精良]",
            PetRarity.史诗: "[史诗]",
            PetRarity.传说: "[传说]",
            PetRarity.神话: "[神话]",
        }
        prefix = rarity_prefix.get(self.rarity, "")
        stage_suffix = ["", "·改", "·真", "·神"][self.evolution_stage]
        return f"{prefix}{self.name}{stage_suffix} Lv.{self.level}"
    
    def gain_exp(self, amount: int) -> bool:
        """获得经验
        
        Returns:
            bool: 是否升级
        """
        self.exp += amount
        
        if self.exp >= self.exp_to_level:
            self.level_up()
            return True
        return False
    
    def level_up(self):
        """升级"""
        self.exp -= self.exp_to_level
        self.level += 1
        
        # 提升属性
        self.attack += int(self.attack_growth)
        self.defense += int(self.defense_growth)
        self.max_health += int(self.health_growth)
        self.health = self.max_health
        
        # 增加升级所需经验
        self.exp_to_level = int(self.exp_to_level * 1.2)
        
        # 提升心情
        self.mood = min(100, self.mood + 10)
        
        # 检查进化
        if self.level in [20, 40, 60]:
            self.evolve()
    
    def evolve(self) -> bool:
        """进化
        
        Returns:
            bool: 是否成功进化
        """
        if self.evolution_stage >= 3:
            return False
        
        self.evolution_stage += 1
        
        # 进化大幅提升属性
        multiplier = 1.5 ** self.evolution_stage
        self.attack = int(self.attack * multiplier)
        self.defense = int(self.defense * multiplier)
        self.max_health = int(self.max_health * multiplier)
        self.health = self.max_health
        
        # 提升成长率
        self.attack_growth *= 1.2
        self.defense_growth *= 1.2
        self.health_growth *= 1.2
        
        return True
    
    def feed(self, food_quality: int = 1) -> Dict[str, Any]:
        """喂食
        
        Args:
            food_quality: 食物品质 1-5
            
        Returns:
            Dict: 效果信息
        """
        # 增加忠诚度
        loyalty_gain = 5 * food_quality
        self.loyalty = min(100, self.loyalty + loyalty_gain)
        
        # 增加心情
        mood_gain = 10 * food_quality
        self.mood = min(100, self.mood + mood_gain)
        
        # 恢复生命
        heal_amount = 20 * food_quality
        self.health = min(self.max_health, self.health + heal_amount)
        
        return {
            "loyalty_gain": loyalty_gain,
            "mood_gain": mood_gain,
            "heal_amount": heal_amount,
        }
    
    def play(self) -> Dict[str, Any]:
        """玩耍（提升心情）"""
        mood_gain = random.randint(10, 20)
        self.mood = min(100, self.mood + mood_gain)
        
        # 消耗体力
        self.loyalty = min(100, self.loyalty + 2)
        
        return {
            "mood_gain": mood_gain,
            "message": f"你和{self.name}一起玩耍，它看起来很开心！",
        }
    
    def train(self, training_type: str) -> Dict[str, Any]:
        """训练
        
        Args:
            training_type: 训练类型 (attack/defense/health)
        """
        if self.mood < 20:
            return {
                "success": False,
                "message": f"{self.name}心情不佳，不想训练...",
            }
        
        # 消耗心情
        self.mood -= 10
        
        # 获得经验
        exp_gain = 50
        leveled = self.gain_exp(exp_gain)
        
        # 根据训练类型额外提升
        bonus_message = ""
        if training_type == "attack":
            self.attack += 1
            bonus_message = "攻击力提升了！"
        elif training_type == "defense":
            self.defense += 1
            bonus_message = "防御力提升了！"
        elif training_type == "health":
            self.max_health += 5
            bonus_message = "生命值提升了！"
        
        return {
            "success": True,
            "exp_gain": exp_gain,
            "leveled_up": leveled,
            "bonus_message": bonus_message,
        }
    
    def use_skill(self, skill_index: int) -> Optional[Dict[str, Any]]:
        """使用技能
        
        Args:
            skill_index: 技能索引
            
        Returns:
            Optional[Dict]: 技能效果
        """
        if skill_index >= len(self.skills):
            return None
        
        skill = self.skills[skill_index]
        
        if skill.current_cooldown > 0:
            return {
                "success": False,
                "message": f"{skill.name}还在冷却中（{skill.current_cooldown}回合）",
            }
        
        # 设置冷却
        skill.current_cooldown = skill.cooldown
        
        return {
            "success": True,
            "skill_name": skill.name,
            "effect_type": skill.effect_type,
            "effect_value": skill.effect_value,
        }
    
    def update_cooldowns(self):
        """更新技能冷却"""
        for skill in self.skills:
            if skill.current_cooldown > 0:
                skill.current_cooldown -= 1
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "id": self.id,
            "name": self.name,
            "pet_type": self.pet_type.value,
            "rarity": self.rarity.name,
            "level": self.level,
            "exp": self.exp,
            "exp_to_level": self.exp_to_level,
            "attack": self.attack,
            "defense": self.defense,
            "health": self.health,
            "max_health": self.max_health,
            "attack_growth": self.attack_growth,
            "defense_growth": self.defense_growth,
            "health_growth": self.health_growth,
            "loyalty": self.loyalty,
            "mood": self.mood,
            "status": self.status.value,
            "skills": [s.to_dict() for s in self.skills],
            "evolution_stage": self.evolution_stage,
            "is_active": self.is_active,
            "appearance": self.appearance,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Pet":
        """从字典创建"""
        return cls(
            id=data["id"],
            name=data["name"],
            pet_type=PetType(data["pet_type"]),
            rarity=PetRarity[data["rarity"]],
            level=data.get("level", 1),
            exp=data.get("exp", 0),
            exp_to_level=data.get("exp_to_level", 100),
            attack=data.get("attack", 10),
            defense=data.get("defense", 5),
            health=data.get("health", 100),
            max_health=data.get("max_health", 100),
            attack_growth=data.get("attack_growth", 2.0),
            defense_growth=data.get("defense_growth", 1.0),
            health_growth=data.get("health_growth", 10.0),
            loyalty=data.get("loyalty", 50),
            mood=data.get("mood", 50),
            status=PetStatus(data.get("status", "resting")),
            skills=[PetSkill.from_dict(s) for s in data.get("skills", [])],
            evolution_stage=data.get("evolution_stage", 0),
            is_active=data.get("is_active", False),
            appearance=data.get("appearance", ""),
        )


# 宠物模板定义
PET_TEMPLATES = {
    "spirit_fox": {
        "name": "灵狐",
        "type": PetType.辅助型,
        "rarity": PetRarity.稀有,
        "attack": 8,
        "defense": 6,
        "health": 80,
        "attack_growth": 1.5,
        "defense_growth": 1.2,
        "health_growth": 8,
        "skills": [
            PetSkill("heal_1", "治愈之吻", "恢复主人生命值", "heal", 20),
            PetSkill("buff_1", "灵动", "提升主人速度", "buff", 0.1),
        ],
        "appearance": "一只通体雪白的狐狸，眼神灵动",
    },
    "flame_tiger": {
        "name": "烈焰虎",
        "type": PetType.攻击型,
        "rarity": PetRarity.精良,
        "attack": 15,
        "defense": 8,
        "health": 120,
        "attack_growth": 3.0,
        "defense_growth": 1.0,
        "health_growth": 12,
        "skills": [
            PetSkill("fire_1", "火焰爪", "造成火焰伤害", "attack", 25),
            PetSkill("rage_1", "狂暴", "提升攻击力", "buff", 0.2),
        ],
        "appearance": "一只浑身燃烧着火焰的猛虎",
    },
    "steel_turtle": {
        "name": "玄铁龟",
        "type": PetType.防御型,
        "rarity": PetRarity.精良,
        "attack": 5,
        "defense": 15,
        "health": 150,
        "attack_growth": 0.8,
        "defense_growth": 3.0,
        "health_growth": 15,
        "skills": [
            PetSkill("shield_1", "铁壁", "提升防御力", "buff", 0.3),
            PetSkill("taunt_1", "嘲讽", "吸引敌人攻击", "debuff", 0),
        ],
        "appearance": "一只背甲如玄铁般坚硬的巨龟",
    },
    "thunder_eagle": {
        "name": "雷霆雕",
        "type": PetType.攻击型,
        "rarity": PetRarity.史诗,
        "attack": 20,
        "defense": 10,
        "health": 100,
        "attack_growth": 4.0,
        "defense_growth": 1.5,
        "health_growth": 10,
        "skills": [
            PetSkill("thunder_1", "雷霆一击", "造成雷电伤害", "attack", 40),
            PetSkill("speed_1", "疾风", "提升速度", "buff", 0.15),
        ],
        "appearance": "一只羽翼带电的金色大雕",
    },
    "jade_dragon": {
        "name": "碧玉龙",
        "type": PetType.平衡型,
        "rarity": PetRarity.传说,
        "attack": 18,
        "defense": 18,
        "health": 180,
        "attack_growth": 3.5,
        "defense_growth": 3.5,
        "health_growth": 18,
        "skills": [
            PetSkill("dragon_1", "龙息", "造成巨大伤害", "attack", 50),
            PetSkill("bless_1", "龙威", "全面提升属性", "buff", 0.2),
            PetSkill("heal_2", "龙血", "恢复大量生命", "heal", 50),
        ],
        "appearance": "一条通体碧玉的小龙，散发着威严的气息",
    },
}


def create_pet(template_id: str, pet_id: str = None) -> Pet:
    """创建宠物
    
    Args:
        template_id: 模板ID
        pet_id: 宠物ID（可选）
        
    Returns:
        Pet: 创建的宠物
    """
    if template_id not in PET_TEMPLATES:
        raise ValueError(f"未知的宠物模板: {template_id}")
    
    template = PET_TEMPLATES[template_id]
    
    if pet_id is None:
        pet_id = f"pet_{template_id}_{random.randint(1000, 9999)}"
    
    return Pet(
        id=pet_id,
        name=template["name"],
        pet_type=template["type"],
        rarity=template["rarity"],
        attack=template["attack"],
        defense=template["defense"],
        health=template["health"],
        max_health=template["health"],
        attack_growth=template["attack_growth"],
        defense_growth=template["defense_growth"],
        health_growth=template["health_growth"],
        skills=template["skills"],
        appearance=template["appearance"],
    )


def generate_random_pet(min_rarity: PetRarity = PetRarity.普通,
                       max_rarity: PetRarity = PetRarity.传说) -> Pet:
    """生成随机宠物
    
    Args:
        min_rarity: 最低稀有度
        max_rarity: 最高稀有度
        
    Returns:
        Pet: 随机宠物
    """
    # 筛选符合条件的模板
    available_templates = [
        tid for tid, t in PET_TEMPLATES.items()
        if min_rarity.level <= t["rarity"].level <= max_rarity.level
    ]
    
    if not available_templates:
        available_templates = list(PET_TEMPLATES.keys())
    
    template_id = random.choice(available_templates)
    return create_pet(template_id)


class PetManager:
    """宠物管理器
    
    管理玩家的所有宠物。
    """
    
    MAX_PETS = 20  # 最大宠物数量
    
    def __init__(self):
        self.pets: List[Pet] = []
        self.active_pet_id: Optional[str] = None
        self.total_pet_exp: int = 0  # 累计宠物经验
    
    def add_pet(self, pet: Pet) -> bool:
        """添加宠物
        
        Returns:
            bool: 是否成功
        """
        if len(self.pets) >= self.MAX_PETS:
            return False
        
        self.pets.append(pet)
        
        # 如果是第一只宠物，自动出战
        if len(self.pets) == 1:
            self.set_active_pet(pet.id)
        
        return True
    
    def remove_pet(self, pet_id: str) -> Optional[Pet]:
        """移除宠物"""
        for i, pet in enumerate(self.pets):
            if pet.id == pet_id:
                removed = self.pets.pop(i)
                if self.active_pet_id == pet_id:
                    self.active_pet_id = None
                return removed
        return None
    
    def get_pet(self, pet_id: str) -> Optional[Pet]:
        """获取指定宠物"""
        for pet in self.pets:
            if pet.id == pet_id:
                return pet
        return None
    
    def get_active_pet(self) -> Optional[Pet]:
        """获取当前出战宠物"""
        if self.active_pet_id:
            return self.get_pet(self.active_pet_id)
        return None
    
    def set_active_pet(self, pet_id: str) -> bool:
        """设置出战宠物
        
        Returns:
            bool: 是否成功
        """
        pet = self.get_pet(pet_id)
        if not pet:
            return False
        
        # 取消之前的出战宠物
        if self.active_pet_id:
            old_pet = self.get_pet(self.active_pet_id)
            if old_pet:
                old_pet.is_active = False
                old_pet.status = PetStatus.休息中
        
        # 设置新的出战宠物
        self.active_pet_id = pet_id
        pet.is_active = True
        pet.status = PetStatus.跟随中
        
        return True
    
    def get_pets_by_type(self, pet_type: PetType) -> List[Pet]:
        """按类型获取宠物"""
        return [p for p in self.pets if p.pet_type == pet_type]
    
    def get_pets_by_rarity(self, rarity: PetRarity) -> List[Pet]:
        """按稀有度获取宠物"""
        return [p for p in self.pets if p.rarity == rarity]
    
    def get_summary(self) -> Dict[str, Any]:
        """获取宠物摘要"""
        return {
            "total_pets": len(self.pets),
            "max_pets": self.MAX_PETS,
            "active_pet": self.active_pet_id,
            "by_type": {
                t.value: len(self.get_pets_by_type(t))
                for t in PetType
            },
            "by_rarity": {
                r.name: len(self.get_pets_by_rarity(r))
                for r in PetRarity
            },
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "pets": [p.to_dict() for p in self.pets],
            "active_pet_id": self.active_pet_id,
            "total_pet_exp": self.total_pet_exp,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PetManager":
        """从字典创建"""
        manager = cls()
        manager.pets = [Pet.from_dict(p) for p in data.get("pets", [])]
        manager.active_pet_id = data.get("active_pet_id")
        manager.total_pet_exp = data.get("total_pet_exp", 0)
        return manager
