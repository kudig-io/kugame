"""技能系统

管理游戏中的门派技能，包括技能效果、冷却时间和使用逻辑。
"""
# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Callable
from enum import Enum
import random

from .player import Sect


class SkillType(Enum):
    """技能类型枚举"""
    攻击 = "attack"      # 增加攻击力
    防御 = "defense"     # 增加防御力
    恢复 = "heal"        # 恢复生命值
    特殊 = "special"     # 特殊效果


@dataclass
class Skill:
    """技能数据类
    
    Attributes:
        id: 技能唯一标识
        name: 技能名称
        description: 技能描述
        sect: 所属门派
        skill_type: 技能类型
        cooldown: 冷却时间（回合数）
        current_cooldown: 当前冷却回合数
        effect_value: 效果数值
        duration: 持续时间（回合数）
        mana_cost: 消耗法力值（可选）
    """
    id: str
    name: str
    description: str
    sect: Sect
    skill_type: SkillType
    cooldown: int
    effect_value: int
    duration: int = 1
    mana_cost: int = 0
    current_cooldown: int = 0
    
    def is_available(self) -> bool:
        """检查技能是否可用（冷却完毕）"""
        return self.current_cooldown <= 0
    
    def use(self) -> bool:
        """使用技能
        
        Returns:
            bool: 使用成功返回True
        """
        if self.is_available():
            self.current_cooldown = self.cooldown
            return True
        return False
    
    def tick_cooldown(self) -> None:
        """减少冷却时间"""
        if self.current_cooldown > 0:
            self.current_cooldown -= 1
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "sect": self.sect.value,
            "skill_type": self.skill_type.value,
            "cooldown": self.cooldown,
            "effect_value": self.effect_value,
            "duration": self.duration,
            "mana_cost": self.mana_cost,
            "current_cooldown": self.current_cooldown,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Skill":
        """从字典创建技能"""
        skill = cls(
            id=data["id"],
            name=data["name"],
            description=data["description"],
            sect=Sect(data["sect"]),
            skill_type=SkillType(data["skill_type"]),
            cooldown=data["cooldown"],
            effect_value=data["effect_value"],
            duration=data.get("duration", 1),
            mana_cost=data.get("mana_cost", 0),
        )
        skill.current_cooldown = data.get("current_cooldown", 0)
        return skill


# 门派技能库
SECT_SKILLS = {
    Sect.青云宗: [
        Skill(
            id="qingyun_steady",
            name="稳如泰山",
            description="【被动】受到的伤害减少20%",
            sect=Sect.青云宗,
            skill_type=SkillType.防御,
            cooldown=0,
            effect_value=20,
        ),
        Skill(
            id="qingyun_dao",
            name="道法自然",
            description="【主动】接下来3场战斗获得30%额外经验",
            sect=Sect.青云宗,
            skill_type=SkillType.特殊,
            cooldown=5,
            effect_value=30,
            duration=3,
        ),
        Skill(
            id="qingyun_counter",
            name="以柔克刚",
            description="【主动】反弹下一次受到的伤害",
            sect=Sect.青云宗,
            skill_type=SkillType.防御,
            cooldown=4,
            effect_value=100,
            duration=1,
        ),
    ],
    Sect.炼狱门: [
        Skill(
            id="liyu_berserk",
            name="狂暴",
            description="【主动】本回合攻击力翻倍",
            sect=Sect.炼狱门,
            skill_type=SkillType.攻击,
            cooldown=3,
            effect_value=100,
            duration=1,
        ),
        Skill(
            id="liyu_lifesteal",
            name="嗜血",
            description="【被动】造成伤害的20%恢复为生命值",
            sect=Sect.炼狱门,
            skill_type=SkillType.恢复,
            cooldown=0,
            effect_value=20,
        ),
        Skill(
            id="liyu_resurrect",
            name="不屈",
            description="【被动】死亡时有30%概率复活，恢复30%生命",
            sect=Sect.炼狱门,
            skill_type=SkillType.特殊,
            cooldown=0,
            effect_value=30,
        ),
    ],
    Sect.玄天宗: [
        Skill(
            id="xuantian_dodge",
            name="变化莫测",
            description="【主动】接下来2回合有50%概率闪避攻击",
            sect=Sect.玄天宗,
            skill_type=SkillType.防御,
            cooldown=4,
            effect_value=50,
            duration=2,
        ),
        Skill(
            id="xuantian_insight",
            name="天机洞察",
            description="【主动】下一道题目的正确答案会高亮显示",
            sect=Sect.玄天宗,
            skill_type=SkillType.特殊,
            cooldown=3,
            effect_value=1,
            duration=1,
        ),
        Skill(
            id="xuantian_transfer",
            name="乾坤挪移",
            description="【主动】将下一次受到的伤害转移给怪物",
            sect=Sect.玄天宗,
            skill_type=SkillType.防御,
            cooldown=5,
            effect_value=100,
            duration=1,
        ),
    ],
    Sect.逍遥派: [
        Skill(
            id="xiaoyao_escape",
            name="逍遥游",
            description="【被动】逃跑成功率提升至100%",
            sect=Sect.逍遥派,
            skill_type=SkillType.特殊,
            cooldown=0,
            effect_value=100,
        ),
        Skill(
            id="xiaoyao_teach",
            name="因材施教",
            description="【被动】学习新命令时额外获得50%经验",
            sect=Sect.逍遥派,
            skill_type=SkillType.特殊,
            cooldown=0,
            effect_value=50,
        ),
        Skill(
            id="xiaoyao_random",
            name="随性而为",
            description="【主动】随机获得以下一种效果：攻击+50%/防御+50%/恢复30%生命/经验+50%",
            sect=Sect.逍遥派,
            skill_type=SkillType.特殊,
            cooldown=3,
            effect_value=50,
            duration=2,
        ),
    ],
}


class SkillManager:
    """技能管理器
    
    管理玩家技能的获取、使用和冷却。
    """
    
    def __init__(self, sect: Sect):
        """初始化技能管理器
        
        Args:
            sect: 玩家门派
        """
        self.sect = sect
        self.skills: Dict[str, Skill] = {}
        self.active_effects: Dict[str, Dict[str, Any]] = {}  # 当前激活的效果
        self._initialize_skills()
    
    def _initialize_skills(self) -> None:
        """初始化门派技能"""
        if self.sect in SECT_SKILLS:
            for skill in SECT_SKILLS[self.sect]:
                # 创建技能的副本
                skill_copy = Skill.from_dict(skill.to_dict())
                self.skills[skill.id] = skill_copy
    
    def get_skill(self, skill_id: str) -> Optional[Skill]:
        """获取技能
        
        Args:
            skill_id: 技能ID
            
        Returns:
            Optional[Skill]: 技能对象
        """
        return self.skills.get(skill_id)
    
    def get_all_skills(self) -> List[Skill]:
        """获取所有技能
        
        Returns:
            List[Skill]: 技能列表
        """
        return list(self.skills.values())
    
    def use_skill(self, skill_id: str) -> Dict[str, Any]:
        """使用技能
        
        Args:
            skill_id: 技能ID
            
        Returns:
            Dict[str, Any]: 使用结果
        """
        skill = self.get_skill(skill_id)
        if not skill:
            return {"success": False, "message": "技能不存在"}
        
        if not skill.is_available():
            return {"success": False, "message": f"技能冷却中，还剩{skill.current_cooldown}回合"}
        
        # 使用技能
        skill.use()
        
        # 添加效果到激活列表
        self.active_effects[skill_id] = {
            "skill": skill,
            "remaining_duration": skill.duration,
        }
        
        return {
            "success": True,
            "message": f"使用技能【{skill.name}】成功！",
            "skill": skill,
        }
    
    def tick_all_cooldowns(self) -> None:
        """减少所有技能冷却"""
        for skill in self.skills.values():
            skill.tick_cooldown()
        
        # 减少效果持续时间
        expired_effects = []
        for skill_id, effect in self.active_effects.items():
            effect["remaining_duration"] -= 1
            if effect["remaining_duration"] <= 0:
                expired_effects.append(skill_id)
        
        # 移除过期效果
        for skill_id in expired_effects:
            del self.active_effects[skill_id]
    
    def has_active_effect(self, skill_id: str) -> bool:
        """检查是否有激活的效果
        
        Args:
            skill_id: 技能ID
            
        Returns:
            bool: 有效果激活返回True
        """
        return skill_id in self.active_effects
    
    def get_active_effects(self) -> List[Dict[str, Any]]:
        """获取所有激活的效果
        
        Returns:
            List[Dict[str, Any]]: 激活的效果列表
        """
        return list(self.active_effects.values())
    
    def apply_passive_effects(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """应用被动技能效果
        
        Args:
            context: 当前战斗/游戏上下文
            
        Returns:
            Dict[str, Any]: 应用效果后的上下文
        """
        result = context.copy()
        
        for skill in self.skills.values():
            # 被动技能（冷却为0）
            if skill.cooldown == 0:
                if skill.id == "qingyun_steady":
                    # 稳如泰山：减伤20%
                    if "damage_received" in result:
                        result["damage_received"] = int(result["damage_received"] * 0.8)
                
                elif skill.id == "liyu_lifesteal":
                    # 嗜血：吸血20%
                    if "damage_dealt" in result:
                        lifesteal = int(result["damage_dealt"] * 0.2)
                        result["heal_amount"] = result.get("heal_amount", 0) + lifesteal
                
                elif skill.id == "xiaoyao_teach":
                    # 因材施教：经验加成
                    if "experience_gain" in result:
                        result["experience_gain"] = int(result["experience_gain"] * 1.5)
        
        return result
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "sect": self.sect.value,
            "skills": {sid: skill.to_dict() for sid, skill in self.skills.items()},
            "active_effects": {
                sid: {
                    "skill": effect["skill"].to_dict(),
                    "remaining_duration": effect["remaining_duration"],
                }
                for sid, effect in self.active_effects.items()
            },
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SkillManager":
        """从字典创建技能管理器"""
        manager = cls(sect=Sect(data["sect"]))
        
        # 恢复技能状态
        for skill_id, skill_data in data.get("skills", {}).items():
            if skill_id in manager.skills:
                manager.skills[skill_id] = Skill.from_dict(skill_data)
        
        # 恢复激活效果
        for skill_id, effect_data in data.get("active_effects", {}).items():
            manager.active_effects[skill_id] = {
                "skill": Skill.from_dict(effect_data["skill"]),
                "remaining_duration": effect_data["remaining_duration"],
            }
        
        return manager
