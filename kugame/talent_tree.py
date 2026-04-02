"""天赋系统

管理玩家的天赋树，提供长期的角色成长路线。
"""
# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import Dict, List, Optional, Any
from enum import Enum

from .player import Sect


class TalentBranch(Enum):
    """天赋分支"""
    攻击 = "attack"
    防御 = "defense"
    辅助 = "support"


@dataclass
class Talent:
    """天赋节点
    
    Attributes:
        id: 天赋ID
        name: 天赋名称
        description: 天赋描述
        branch: 所属分支
        tier: 天赋层级（1-3）
        max_points: 最大投入点数
        current_points: 当前投入点数
        effect_per_point: 每点效果值
    """
    id: str
    name: str
    description: str
    branch: TalentBranch
    tier: int
    max_points: int
    current_points: int = 0
    effect_per_point: float = 1.0
    
    @property
    def total_effect(self) -> float:
        """计算总效果"""
        return self.effect_per_point * self.current_points
    
    def can_add_point(self, available_points: int) -> bool:
        """检查是否可以加点"""
        return self.current_points < self.max_points and available_points > 0
    
    def add_point(self) -> bool:
        """添加天赋点"""
        if self.current_points < self.max_points:
            self.current_points += 1
            return True
        return False
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "branch": self.branch.value,
            "tier": self.tier,
            "max_points": self.max_points,
            "current_points": self.current_points,
            "effect_per_point": self.effect_per_point,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Talent":
        return cls(
            id=data["id"],
            name=data["name"],
            description=data["description"],
            branch=TalentBranch(data["branch"]),
            tier=data["tier"],
            max_points=data["max_points"],
            current_points=data.get("current_points", 0),
            effect_per_point=data.get("effect_per_point", 1.0),
        )


# 天赋树定义
TALENT_TEMPLATES: Dict[Sect, Dict[TalentBranch, List[Talent]]] = {
    Sect.青云宗: {
        TalentBranch.攻击: [
            Talent("qy_atk_1", "剑气初成", "攻击力+2/级", TalentBranch.攻击, 1, 5, 0, 2),
            Talent("qy_atk_2", "剑意通明", "攻击力+4/级", TalentBranch.攻击, 2, 3, 0, 4),
            Talent("qy_atk_3", "剑道通神", "攻击力+8/级", TalentBranch.攻击, 3, 1, 0, 8),
        ],
        TalentBranch.防御: [
            Talent("qy_def_1", "气沉丹田", "防御力+2/级", TalentBranch.防御, 1, 5, 0, 2),
            Talent("qy_def_2", "金刚不坏", "防御力+4/级", TalentBranch.防御, 2, 3, 0, 4),
            Talent("qy_def_3", "万法不侵", "受到伤害-10%/级", TalentBranch.防御, 3, 1, 0, 10),
        ],
        TalentBranch.辅助: [
            Talent("qy_sup_1", "悟道", "经验获取+5%/级", TalentBranch.辅助, 1, 5, 0, 5),
            Talent("qy_sup_2", "心法", "连击加成+5%/级", TalentBranch.辅助, 2, 3, 0, 5),
            Talent("qy_sup_3", "天人合一", "全属性+10%", TalentBranch.辅助, 3, 1, 0, 10),
        ],
    },
    Sect.炼狱门: {
        TalentBranch.攻击: [
            Talent("ly_atk_1", "嗜血", "攻击力+3/级", TalentBranch.攻击, 1, 5, 0, 3),
            Talent("ly_atk_2", "狂暴", "暴击率+5%/级", TalentBranch.攻击, 2, 3, 0, 5),
            Talent("ly_atk_3", "血祭", "攻击力+15%，但每回合损失5%生命", TalentBranch.攻击, 3, 1, 0, 15),
        ],
        TalentBranch.防御: [
            Talent("ly_def_1", "铁骨", "防御力+3/级", TalentBranch.防御, 1, 5, 0, 3),
            Talent("ly_def_2", "不屈", "生命值+10/级", TalentBranch.防御, 2, 3, 0, 10),
            Talent("ly_def_3", "浴血", "生命低于30%时防御翻倍", TalentBranch.防御, 3, 1, 0, 100),
        ],
        TalentBranch.辅助: [
            Talent("ly_sup_1", "掠夺", "战斗经验+8%/级", TalentBranch.辅助, 1, 5, 0, 8),
            Talent("ly_sup_2", "威慑", "敌人攻击力-5%/级", TalentBranch.辅助, 2, 3, 0, 5),
            Talent("ly_sup_3", "战神", "战斗开始时攻击力+50%，持续3回合", TalentBranch.辅助, 3, 1, 0, 50),
        ],
    },
    Sect.玄天宗: {
        TalentBranch.攻击: [
            Talent("xt_atk_1", "灵动", "攻击力+2/级，闪避+2%/级", TalentBranch.攻击, 1, 5, 0, 2),
            Talent("xt_atk_2", "幻影", "攻击时有20%概率造成2倍伤害", TalentBranch.攻击, 2, 3, 0, 20),
            Talent("xt_atk_3", "瞬杀", "闪避后下一次攻击必暴击", TalentBranch.攻击, 3, 1, 0, 100),
        ],
        TalentBranch.防御: [
            Talent("xt_def_1", "轻身", "防御力+1/级，闪避+3%/级", TalentBranch.防御, 1, 5, 0, 3),
            Talent("xt_def_2", "虚无", "有15%概率完全闪避攻击", TalentBranch.防御, 2, 3, 0, 15),
            Talent("xt_def_3", "不灭", "受到致命伤害时有50%概率保留1点生命", TalentBranch.防御, 3, 1, 0, 50),
        ],
        TalentBranch.辅助: [
            Talent("xt_sup_1", "推演", "答题时间+3秒/级", TalentBranch.辅助, 1, 5, 0, 3),
            Talent("xt_sup_2", "洞察", "错误选项有20%概率被标记", TalentBranch.辅助, 2, 3, 0, 20),
            Talent("xt_sup_3", "预知", "每5道题可以查看正确答案", TalentBranch.辅助, 3, 1, 0, 1),
        ],
    },
    Sect.逍遥派: {
        TalentBranch.攻击: [
            Talent("xy_atk_1", "随性", "攻击力+1~3/级（随机）", TalentBranch.攻击, 1, 5, 0, 2),
            Talent("xy_atk_2", "逍遥", "每次攻击附加当前经验值1%的伤害", TalentBranch.攻击, 2, 3, 0, 1),
            Talent("xy_atk_3", "破天", "有5%概率一击必杀（对BOSS无效）", TalentBranch.攻击, 3, 1, 0, 5),
        ],
        TalentBranch.防御: [
            Talent("xy_def_1", "自在", "防御力+1~3/级（随机）", TalentBranch.防御, 1, 5, 0, 2),
            Talent("xy_def_2", "逍遥游", "逃跑成功率+15%/级", TalentBranch.防御, 2, 3, 0, 15),
            Talent("xy_def_3", "无我", "每回合恢复5%生命值", TalentBranch.防御, 3, 1, 0, 5),
        ],
        TalentBranch.辅助: [
            Talent("xy_sup_1", "机缘", "装备掉落率+10%/级", TalentBranch.辅助, 1, 5, 0, 10),
            Talent("xy_sup_2", "造化", "商店价格-10%/级", TalentBranch.辅助, 2, 3, 0, 10),
            Talent("xy_sup_3", "超脱", "每升1级额外获得1点天赋点", TalentBranch.辅助, 3, 1, 0, 1),
        ],
    },
}


class TalentTree:
    """天赋树管理器"""
    
    def __init__(self, sect: Sect):
        self.sect = sect
        self.talents: Dict[str, Talent] = {}
        self.available_points: int = 0
        self._initialize_talents()
    
    def _initialize_talents(self) -> None:
        """初始化天赋树"""
        if self.sect in TALENT_TEMPLATES:
            for branch, talents in TALENT_TEMPLATES[self.sect].items():
                for talent in talents:
                    # 创建副本
                    talent_copy = Talent.from_dict(talent.to_dict())
                    self.talents[talent.id] = talent_copy
    
    def get_talent(self, talent_id: str) -> Optional[Talent]:
        return self.talents.get(talent_id)
    
    def get_branch_talents(self, branch: TalentBranch) -> List[Talent]:
        """获取指定分支的所有天赋"""
        return [t for t in self.talents.values() if t.branch == branch]
    
    def add_talent_point(self, talent_id: str) -> Dict[str, Any]:
        """添加天赋点"""
        if self.available_points <= 0:
            return {"success": False, "message": "没有可用的天赋点"}
        
        talent = self.get_talent(talent_id)
        if not talent:
            return {"success": False, "message": "天赋不存在"}
        
        # 检查前置条件（高等级天赋需要低等级天赋投入一定点数）
        if talent.tier > 1:
            lower_tier_points = sum(
                t.current_points for t in self.get_branch_talents(talent.branch)
                if t.tier < talent.tier
            )
            required_points = (talent.tier - 1) * 3
            if lower_tier_points < required_points:
                return {
                    "success": False, 
                    "message": f"需要先在前置天赋投入{required_points}点，当前{lower_tier_points}点"
                }
        
        if talent.add_point():
            self.available_points -= 1
            return {
                "success": True, 
                "message": f"【{talent.name}】提升至{talent.current_points}级",
                "remaining_points": self.available_points
            }
        
        return {"success": False, "message": "该天赋已满级"}
    
    def get_total_bonus(self, bonus_type: str) -> float:
        """获取指定类型的总加成"""
        total = 0.0
        for talent in self.talents.values():
            if bonus_type in talent.id:
                total += talent.total_effect
        return total
    
    def on_level_up(self) -> None:
        """升级时获得天赋点"""
        self.available_points += 1
        # 检查是否有超脱天赋
        if "xy_sup_3" in self.talents and self.talents["xy_sup_3"].current_points > 0:
            self.available_points += 1
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "sect": self.sect.value,
            "talents": {tid: t.to_dict() for tid, t in self.talents.items()},
            "available_points": self.available_points,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TalentTree":
        tree = cls(sect=Sect(data["sect"]))
        tree.available_points = data.get("available_points", 0)
        
        for talent_id, talent_data in data.get("talents", {}).items():
            if talent_id in tree.talents:
                tree.talents[talent_id] = Talent.from_dict(talent_data)
        
        return tree
