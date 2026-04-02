"""玩家角色系统

定义玩家角色、属性、技能和成长体系，管理玩家的游戏进度和Kubernetes命令学习状态。
"""
# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from enum import Enum
from datetime import datetime
import json
import os

# 导入装备系统
from .equipment import Equipment, EquipmentType

# 导入每日签到系统
from .daily_checkin import DailyCheckin

# 前向声明（避免循环导入）
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .skills import SkillManager
    from .talent_tree import TalentTree


class AchievementType(Enum):
    """成就类型枚举

    定义游戏中不同类型的成就。
    """
    命令掌握 = "command_mastery"   # 掌握命令相关成就
    故事进度 = "story_progress"     # 故事进度相关成就
    挑战完成 = "challenge_completion"  # 挑战完成相关成就
    连续成功 = "streak_success"     # 连续成功相关成就
    门派专精 = "sect_specialization"  # 门派专精相关成就
    收集成就 = "collection"         # 装备收集相关成就
    等级成就 = "level_achievement"  # 等级相关成就
    挑战塔成就 = "tower_achievement" # 挑战塔相关成就
    战斗成就 = "combat_achievement" # 战斗相关成就
    特殊成就 = "special_achievement" # 特殊成就


class Achievement:
    """成就类

    定义游戏中的成就，包含名称、描述、类型、条件和奖励。

    Attributes:
        id: 成就唯一标识
        name: 成就名称
        description: 成就描述
        achievement_type: 成就类型
        condition: 完成条件（如掌握命令数量、章节数等）
        reward: 奖励内容（经验值、称号等）
        unlocked: 是否已解锁
    """
    def __init__(self, id: str, name: str, description: str, achievement_type: AchievementType, condition: int, reward: dict):
        self.id = id
        self.name = name
        self.description = description
        self.type = achievement_type
        self.condition = condition
        self.reward = reward
        self.unlocked = False


class CultivationLevel(Enum):
    """修炼境界枚举

    定义玩家的修炼等级，每个等级对应不同的称号和能力。

    Attributes:
        value: 元组，包含等级数值和中文描述
    """
    凡人 = (1, "凡人之躯")       # 等级1-10
    练气期 = (2, "初步入门")       # 等级11-20
    筑基期 = (3, "根基稳固")       # 等级21-30
    金丹期 = (4, "金丹大道")       # 等级31-40
    元婴期 = (5, "元婴初成")       # 等级41-50
    化神期 = (6, "化神飞升")       # 等级51-60
    大乘期 = (7, "大乘圆满")       # 等级61-70
    渡劫期 = (8, "渡劫飞升")       # 等级71-80
    散仙 = (9, "逍遥天地")         # 等级81-90
    金仙 = (10, "金仙不朽")        # 等级91-100


class Sect(Enum):
    """门派枚举

    定义玩家可以选择的门派。
    """
    青云宗 = "青云宗"   # 正派，擅长基础扎实
    玄天宗 = "玄天宗"   # 中立，擅长变化多端
    炼狱门 = "炼狱门"   # 邪派，擅长爆发力强
    逍遥派 = "逍遥派"   # 散修，擅长灵活应变


@dataclass
class Player:
    """玩家角色类

    管理玩家的基本信息、修炼状态、学习进度和游戏成就。

    Attributes:
        name: 玩家名称
        sect: 玩家所属门派
        level: 当前等级
        experience: 当前经验值
        cultivation: 当前修炼境界
        skills: 掌握的技能列表
        achievements: 获得的成就列表
        achievement_objects: 成就对象列表（包含详细信息）
        current_chapter: 当前故事章节
        kubectl_commands_mastered: 掌握的Kubernetes命令列表
        challenges_completed: 完成的挑战列表
        streak: 连续正确回答次数
        total_correct: 总正确回答次数
        total_attempts: 总尝试次数
        custom_titles: 自定义称号列表
        sect_bonus: 门派加成

        # 战斗属性
        health: 当前生命值
        max_health: 最大生命值
        attack: 攻击力
        defense: 防御力

        # 答题系统
        wrong_commands: 答错的命令列表
        
        # 装备系统
        equipped_weapon: 已装备武器
        equipped_armor: 已装备护甲
        equipped_accessory: 已装备饰品
        inventory: 背包中的装备列表
    """
    name: str
    sect: Sect
    level: int = 1
    experience: int = 0
    cultivation: CultivationLevel = CultivationLevel.凡人
    skills: List[str] = field(default_factory=list)
    achievements: List[str] = field(default_factory=list)
    achievement_objects: List[Achievement] = field(default_factory=list)
    current_chapter: str = "序章"

    # Kubernetes学习进度
    kubectl_commands_mastered: List[str] = field(default_factory=list)
    challenges_completed: List[str] = field(default_factory=list)

    # 游戏统计数据
    streak: int = 0
    total_correct: int = 0
    total_attempts: int = 0

    # 自定义属性
    custom_titles: List[str] = field(default_factory=list)
    sect_bonus: float = 1.0

    # 战斗属性
    health: int = 100
    max_health: int = 100
    attack: int = 10
    defense: int = 5
    
    # 战斗统计
    total_combats: int = 0
    combats_won: int = 0
    combats_lost: int = 0
    highest_tower_level: int = 0

    # 答题系统
    wrong_commands: List[str] = field(default_factory=list)
    
    # 装备系统
    equipped_weapon: Optional[Equipment] = None
    equipped_armor: Optional[Equipment] = None
    equipped_accessory: Optional[Equipment] = None
    inventory: List[Equipment] = field(default_factory=list)
    
    # 技能和天赋系统（延迟初始化）
    skill_manager_data: Optional[Dict[str, Any]] = None
    talent_tree_data: Optional[Dict[str, Any]] = None
    
    # 副本系统
    dungeon_manager_data: Optional[Dict[str, Any]] = None
    tower_progress_data: Optional[Dict[str, Any]] = None
    
    # 体力系统
    stamina: int = 100
    max_stamina: int = 100
    last_stamina_refresh: Optional[str] = None
    
    # 每日签到系统
    checkin_data: Optional[Dict[str, Any]] = None
    
    # 任务系统
    quest_data: Optional[Dict[str, Any]] = None

    def __post_init__(self) -> None:
        """初始化后处理

        确保玩家名称有效，设置默认值，初始化成就系统。
        """
        if not self.name:
            self.name = "无名侠客"

        # 确保属性类型正确
        if not isinstance(self.level, int) or self.level < 1:
            self.level = 1

        if not isinstance(self.experience, int) or self.experience < 0:
            self.experience = 0

        # 战斗属性初始化
        if not isinstance(self.health, int) or self.health < 0:
            self.health = 100
        if not isinstance(self.max_health, int) or self.max_health < 0:
            self.max_health = 100
        if not isinstance(self.attack, int) or self.attack < 0:
            self.attack = 10
        if not isinstance(self.defense, int) or self.defense < 0:
            self.defense = 5

        # 确保列表属性初始化正确
        if not isinstance(self.skills, list):
            self.skills = []

        if not isinstance(self.achievements, list):
            self.achievements = []

        if not isinstance(self.achievement_objects, list):
            self.achievement_objects = []

        if not isinstance(self.kubectl_commands_mastered, list):
            self.kubectl_commands_mastered = []

        if not isinstance(self.challenges_completed, list):
            self.challenges_completed = []

        if not isinstance(self.custom_titles, list):
            self.custom_titles = []

        if not isinstance(self.wrong_commands, list):
            self.wrong_commands = []

        if not isinstance(self.streak, int) or self.streak < 0:
            self.streak = 0

        if not isinstance(self.total_correct, int) or self.total_correct < 0:
            self.total_correct = 0

        if not isinstance(self.total_attempts, int) or self.total_attempts < 0:
            self.total_attempts = 0
        
        # 装备系统初始化
        if not isinstance(self.inventory, list):
            self.inventory = []

        # 技能和天赋系统初始化
        self._initialize_skill_manager()
        self._initialize_talent_tree()

        # 初始化成就系统
        self._initialize_achievements()

        # 设置门派加成
        self._set_sect_bonus()

        # 确保生命值不超过最大值
        if self.health > self.max_health:
            self.health = self.max_health
            
        # 初始化签到系统
        if self.checkin_data is None:
            self.checkin_data = DailyCheckin().to_dict()
            
        # 初始化任务系统
        if self.quest_data is None:
            from .quest_system import QuestManager
            self.quest_data = QuestManager().to_dict()

    def _initialize_achievements(self) -> None:
        """初始化成就系统

        创建所有预定义成就并添加到玩家的成就列表中。
        """
        # 如果成就已经初始化，跳过
        if self.achievement_objects:
            return

        # 预定义成就列表
        predefined_achievements = [
            # 命令掌握类成就
            Achievement(
                id="cmd_master_10",
                name="入门弟子",
                description="掌握10个Kubernetes命令",
                achievement_type=AchievementType.命令掌握,
                condition=10,
                reward={"experience": 500, "title": "命令初学者"}
            ),
            Achievement(
                id="cmd_master_30",
                name="熟练弟子",
                description="掌握30个Kubernetes命令",
                achievement_type=AchievementType.命令掌握,
                condition=30,
                reward={"experience": 1500, "title": "命令熟练者"}
            ),
            Achievement(
                id="cmd_master_50",
                name="命令专家",
                description="掌握50个Kubernetes命令",
                achievement_type=AchievementType.命令掌握,
                condition=50,
                reward={"experience": 3000, "title": "命令专家"}
            ),
            Achievement(
                id="cmd_master_all",
                name="命令大师",
                description="掌握所有Kubernetes命令",
                achievement_type=AchievementType.命令掌握,
                condition=100,  # 设置为一个较大的值，实际会根据总命令数调整
                reward={"experience": 10000, "title": "Kubernetes命令大师"}
            ),

            # 故事进度类成就
            Achievement(
                id="story_chapter_3",
                name="初入江湖",
                description="完成第3章故事",
                achievement_type=AchievementType.故事进度,
                condition=3,
                reward={"experience": 1000, "title": "江湖新秀"}
            ),
            Achievement(
                id="story_chapter_6",
                name="江湖少侠",
                description="完成第6章故事",
                achievement_type=AchievementType.故事进度,
                condition=6,
                reward={"experience": 2500, "title": "江湖少侠"}
            ),
            Achievement(
                id="story_chapter_9",
                name="武林高手",
                description="完成第9章故事",
                achievement_type=AchievementType.故事进度,
                condition=9,
                reward={"experience": 5000, "title": "武林高手"}
            ),

            # 挑战完成类成就
            Achievement(
                id="challenge_10",
                name="挑战新手",
                description="完成10个挑战",
                achievement_type=AchievementType.挑战完成,
                condition=10,
                reward={"experience": 800, "title": "挑战新手"}
            ),
            Achievement(
                id="challenge_50",
                name="挑战达人",
                description="完成50个挑战",
                achievement_type=AchievementType.挑战完成,
                condition=50,
                reward={"experience": 4000, "title": "挑战达人"}
            ),

            # 连续成功类成就
            Achievement(
                id="streak_5",
                name="小有成就",
                description="连续正确回答5次",
                achievement_type=AchievementType.连续成功,
                condition=5,
                reward={"experience": 300, "title": "连击高手"}
            ),
            Achievement(
                id="streak_10",
                name="势如破竹",
                description="连续正确回答10次",
                achievement_type=AchievementType.连续成功,
                condition=10,
                reward={"experience": 800, "title": "连击大师"}
            ),
            Achievement(
                id="streak_20",
                name="无人能挡",
                description="连续正确回答20次",
                achievement_type=AchievementType.连续成功,
                condition=20,
                reward={"experience": 2000, "title": "连击王者"}
            ),
            
            # 装备收集类成就
            Achievement(
                id="equipment_10",
                name="装备收集者",
                description="收集10件装备",
                achievement_type=AchievementType.收集成就,
                condition=10,
                reward={"experience": 500, "title": "装备收集者"}
            ),
            Achievement(
                id="equipment_50",
                name="装备收藏家",
                description="收集50件装备",
                achievement_type=AchievementType.收集成就,
                condition=50,
                reward={"experience": 2000, "title": "装备收藏家"}
            ),
            Achievement(
                id="equipment_orange",
                name="传说装备",
                description="获得一件传说品质装备",
                achievement_type=AchievementType.收集成就,
                condition=1,
                reward={"experience": 3000, "title": "传说拥有者"}
            ),
            
            # 等级类成就
            Achievement(
                id="level_10",
                name="初出茅庐",
                description="达到10级",
                achievement_type=AchievementType.等级成就,
                condition=10,
                reward={"experience": 300, "title": "初入江湖"}
            ),
            Achievement(
                id="level_30",
                name="小有所成",
                description="达到30级",
                achievement_type=AchievementType.等级成就,
                condition=30,
                reward={"experience": 1000, "title": "江湖少侠"}
            ),
            Achievement(
                id="level_50",
                name="一代宗师",
                description="达到50级",
                achievement_type=AchievementType.等级成就,
                condition=50,
                reward={"experience": 3000, "title": "一代宗师"}
            ),
            Achievement(
                id="level_100",
                name="修仙巅峰",
                description="达到100级",
                achievement_type=AchievementType.等级成就,
                condition=100,
                reward={"experience": 10000, "title": "修仙巅峰"}
            ),
            
            # 挑战塔类成就
            Achievement(
                id="tower_10",
                name="塔之新人",
                description="挑战之塔达到10层",
                achievement_type=AchievementType.挑战塔成就,
                condition=10,
                reward={"experience": 500, "title": "塔之新人"}
            ),
            Achievement(
                id="tower_50",
                name="塔之勇士",
                description="挑战之塔达到50层",
                achievement_type=AchievementType.挑战塔成就,
                condition=50,
                reward={"experience": 3000, "title": "塔之勇士"}
            ),
            Achievement(
                id="tower_100",
                name="通天塔主",
                description="挑战之塔达到100层",
                achievement_type=AchievementType.挑战塔成就,
                condition=100,
                reward={"experience": 10000, "title": "通天塔主"}
            ),
            
            # 战斗类成就
            Achievement(
                id="combat_100",
                name="百战老兵",
                description="参加100场战斗",
                achievement_type=AchievementType.战斗成就,
                condition=100,
                reward={"experience": 1000, "title": "百战老兵"}
            ),
            Achievement(
                id="combat_win_50",
                name="常胜将军",
                description="赢得50场战斗",
                achievement_type=AchievementType.战斗成就,
                condition=50,
                reward={"experience": 2000, "title": "常胜将军"}
            ),
            
            # 特殊成就
            Achievement(
                id="first_login",
                name="初入仙门",
                description="第一次登录游戏",
                achievement_type=AchievementType.特殊成就,
                condition=1,
                reward={"experience": 100, "title": "初入仙门"}
            ),
            Achievement(
                id="perfect_answer",
                name="完美答题",
                description="单次答对10道题",
                achievement_type=AchievementType.特殊成就,
                condition=1,
                reward={"experience": 500, "title": "完美答题"}
            ),
        ]

        self.achievement_objects = predefined_achievements
        # 检查并解锁已满足条件的成就
        self.check_and_unlock_achievements()

    def _set_sect_bonus(self) -> None:
        """设置门派加成

        根据玩家选择的门派设置不同的加成系数。
        """
        # 青云宗：基础扎实，经验加成
        if self.sect == Sect.青云宗:
            self.sect_bonus = 1.1
        # 玄天宗：变化多端，挑战加成
        elif self.sect == Sect.玄天宗:
            self.sect_bonus = 1.0
        # 炼狱门：爆发力强，连击加成
        elif self.sect == Sect.炼狱门:
            self.sect_bonus = 1.2
        # 逍遥派：灵活应变，学习加成
        elif self.sect == Sect.逍遥派:
            self.sect_bonus = 1.15
        else:
            self.sect_bonus = 1.0

    @property
    def title(self) -> str:
        """获取玩家称号

        根据门派和修炼境界生成玩家的完整称号。

        Returns:
            str: 玩家的完整称号
        """
        return f"{self.sect.value}{self.cultivation.value[1]}·{self.name}"

    def check_and_unlock_achievements(self) -> List[str]:
        """检查并解锁成就

        检查所有成就条件，解锁满足条件的成就，并返回解锁的成就列表。

        Returns:
            List[str]: 解锁的成就名称列表
        """
        unlocked_achievements = []

        for achievement in self.achievement_objects:
            if achievement.unlocked:
                continue

            # 根据成就类型检查条件
            if achievement.type == AchievementType.命令掌握:
                if len(self.kubectl_commands_mastered) >= achievement.condition:
                    self.unlock_achievement(achievement.id)
                    unlocked_achievements.append(achievement.name)
            elif achievement.type == AchievementType.故事进度:
                # 假设章节ID格式为"第X章"
                try:
                    chapter_num = int(self.current_chapter.split("第")[1].split("章")[0])
                    if chapter_num >= achievement.condition:
                        self.unlock_achievement(achievement.id)
                        unlocked_achievements.append(achievement.name)
                except (IndexError, ValueError):
                    pass
            elif achievement.type == AchievementType.挑战完成:
                if len(self.challenges_completed) >= achievement.condition:
                    self.unlock_achievement(achievement.id)
                    unlocked_achievements.append(achievement.name)
            elif achievement.type == AchievementType.连续成功:
                if self.streak >= achievement.condition:
                    self.unlock_achievement(achievement.id)
                    unlocked_achievements.append(achievement.name)

        return unlocked_achievements

    def unlock_achievement(self, achievement_id: str) -> bool:
        """解锁特定成就

        Args:
            achievement_id: 成就ID

        Returns:
            bool: 解锁成功返回True，否则返回False
        """
        for achievement in self.achievement_objects:
            if achievement.id == achievement_id and not achievement.unlocked:
                achievement.unlocked = True
                self.achievements.append(achievement.id)

                # 应用成就奖励
                if "experience" in achievement.reward:
                    self.gain_experience(achievement.reward["experience"])

                if "title" in achievement.reward:
                    self.custom_titles.append(achievement.reward["title"])

                return True
        return False

    def update_streak(self, correct: bool) -> None:
        """更新连续正确次数

        Args:
            correct: 是否回答正确
        """
        if correct:
            self.streak += 1
            self.total_correct += 1
        else:
            self.streak = 0

        self.total_attempts += 1

        # 检查连续成功成就
        self.check_and_unlock_achievements()

    def get_achievement_progress(self) -> Dict[str, Any]:
        """获取成就进度

        Returns:
            Dict[str, Any]: 成就进度字典
        """
        total_achievements = len(self.achievement_objects)
        unlocked_achievements = sum(1 for a in self.achievement_objects if a.unlocked)

        by_type = {}
        for achievement_type in AchievementType:
            type_achievements = [a for a in self.achievement_objects if a.type == achievement_type]
            type_unlocked = sum(1 for a in type_achievements if a.unlocked)
            by_type[achievement_type.value] = {
                "total": len(type_achievements),
                "unlocked": type_unlocked,
                "percentage": round(type_unlocked / len(type_achievements) * 100, 1) if type_achievements else 0
            }

        return {
            "total_achievements": total_achievements,
            "unlocked_achievements": unlocked_achievements,
            "progress_percentage": round(unlocked_achievements / total_achievements * 100, 1) if total_achievements else 0,
            "by_type": by_type,
            "achievement_list": [{"id": a.id, "name": a.name, "description": a.description, "unlocked": a.unlocked} for a in self.achievement_objects]
        }

    def gain_experience(self, exp: int) -> bool:
        """获得经验值，可能升级

        增加玩家经验值，如果达到升级条件则自动升级。
        应用门派加成和装备加成。

        Args:
            exp: 获得的经验值

        Returns:
            bool: 如果发生升级则返回True，否则返回False
        """
        if not isinstance(exp, (int, float)) or exp < 0:
            raise ValueError("经验值必须是非负数")

        # 应用门派加成和装备加成
        total_bonus = self.sect_bonus + self.exp_bonus
        exp_with_bonus = int(exp * total_bonus)
        self.experience += exp_with_bonus
        required_exp = self._calculate_required_exp()

        if self.experience >= required_exp:
            self.level_up()
            return True
        return False

    def _calculate_required_exp(self) -> int:
        """计算升级所需经验

        根据当前等级计算升级到下一等级所需的经验值。

        Returns:
            int: 升级所需的经验值
        """
        return int(100 * (1.5 ** (self.level - 1)))

    def level_up(self) -> None:
        """升级处理

        处理玩家升级逻辑，包括经验值消耗、等级提升和修炼境界更新。
        支持一次性升级多个等级。
        """
        while self.experience >= self._calculate_required_exp():
            self.experience -= self._calculate_required_exp()
            self.level += 1
            self._update_cultivation()

    def _update_cultivation(self) -> None:
        """根据等级更新修炼境界

        根据玩家当前等级，更新对应的修炼境界。

        等级对应关系：
        - 凡人：等级1-10
        - 练气期：等级11-20
        - 筑基期：等级21-30
        - 金丹期：等级31-40
        - 元婴期：等级41-50
        - 化神期：等级51-60
        - 大乘期：等级61-70
        - 渡劫期：等级71-80
        - 散仙：等级81-90
        - 金仙：等级91-100
        """
        # 按等级从高到低检查
        for cultivation in reversed(list(CultivationLevel)):
            if self.level >= cultivation.value[0] * 10 - 9:  # 调整等级对应关系
                self.cultivation = cultivation
                break

    def learn_command(self, command: str) -> bool:
        """学习命令

        记录玩家学习的Kubernetes命令，并给予经验奖励。

        Args:
            command: 学习的Kubernetes命令

        Returns:
            bool: 如果是新命令则返回True，否则返回False
        """
        if not isinstance(command, str) or not command:
            raise ValueError("命令必须是非空字符串")

        if command not in self.kubectl_commands_mastered:
            self.kubectl_commands_mastered.append(command)
            self.gain_experience(50)  # 学习命令获得50经验值
            return True
        return False

    def complete_challenge(self, challenge_id: str) -> bool:
        """完成挑战

        记录玩家完成的挑战，并给予经验奖励。

        Args:
            challenge_id: 挑战的唯一标识

        Returns:
            bool: 如果是新挑战则返回True，否则返回False
        """
        if not isinstance(challenge_id, str) or not challenge_id:
            raise ValueError("挑战ID必须是非空字符串")

        if challenge_id not in self.challenges_completed:
            self.challenges_completed.append(challenge_id)
            self.gain_experience(100)  # 完成挑战获得100经验值
            return True
        return False

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典

        将玩家对象转换为字典格式，用于保存和序列化。

        Returns:
            Dict[str, Any]: 玩家数据字典
        """
        return {
            "name": self.name,
            "sect": self.sect.value,
            "level": self.level,
            "experience": self.experience,
            "cultivation": self.cultivation.name,
            "skills": self.skills,
            "achievements": self.achievements,
            "achievement_objects": [
                {
                    "id": a.id,
                    "name": a.name,
                    "description": a.description,
                    "type": a.type.value,
                    "condition": a.condition,
                    "reward": a.reward,
                    "unlocked": a.unlocked
                }
                for a in self.achievement_objects
            ],
            "current_chapter": self.current_chapter,
            "kubectl_commands_mastered": self.kubectl_commands_mastered,
            "challenges_completed": self.challenges_completed,
            "streak": self.streak,
            "total_correct": self.total_correct,
            "total_attempts": self.total_attempts,
            "custom_titles": self.custom_titles,
            "sect_bonus": self.sect_bonus,
            # 装备系统
            "equipped_weapon": self.equipped_weapon.to_dict() if self.equipped_weapon else None,
            "equipped_armor": self.equipped_armor.to_dict() if self.equipped_armor else None,
            "equipped_accessory": self.equipped_accessory.to_dict() if self.equipped_accessory else None,
            "inventory": [eq.to_dict() for eq in self.inventory],
            # 技能和天赋系统
            "skill_manager_data": self.skill_manager.to_dict() if hasattr(self, '_skill_manager') and self._skill_manager else None,
            "talent_tree_data": self.talent_tree.to_dict() if hasattr(self, '_talent_tree') and self._talent_tree else None,
            # 副本系统
            "dungeon_manager_data": self.dungeon_manager_data,
            "tower_progress_data": self.tower_progress_data,
            # 体力系统
            "stamina": self.stamina,
            "max_stamina": self.max_stamina,
            "last_stamina_refresh": self.last_stamina_refresh,
        }

    def save(self, filepath: str = "player_save.json") -> bool:
        """保存玩家数据

        将玩家数据保存到本地文件。

        Args:
            filepath: 保存文件路径，默认在当前目录

        Returns:
            bool: 保存成功返回True，失败返回False
        """
        try:
            # 确保文件路径存在
            directory = os.path.dirname(filepath)
            if directory and not os.path.exists(directory):
                os.makedirs(directory)

            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(self.to_dict(), f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"保存玩家数据失败: {str(e)}")
            return False

    @classmethod
    def get_save_files(cls, directory: str = ".") -> List[str]:
        """获取所有存档文件列表

        Args:
            directory: 查找存档的目录，默认在当前目录

        Returns:
            List[str]: 存档文件列表
        """
        save_files = []
        try:
            # 遍历目录，查找以.json结尾的文件
            for file in os.listdir(directory):
                if file.endswith(".json"):
                    # 尝试加载文件，验证是否为有效的存档文件
                    filepath = os.path.join(directory, file)
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                            # 验证必要字段
                            if all(field in data for field in ["name", "sect", "level", "experience"]):
                                save_files.append(file)
                    except (json.JSONDecodeError, ValueError, KeyError):
                        continue
        except Exception as e:
            print(f"获取存档文件列表失败: {str(e)}")
        return save_files

    @classmethod
    def delete_save(cls, filepath: str) -> bool:
        """删除指定存档

        Args:
            filepath: 要删除的存档文件路径

        Returns:
            bool: 删除成功返回True，失败返回False
        """
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
                return True
            return False
        except Exception as e:
            print(f"删除存档失败: {str(e)}")
            return False

    @classmethod
    def load(cls, filepath: str = "player_save.json") -> Optional["Player"]:
        """加载玩家数据

        从本地文件加载玩家数据。

        Args:
            filepath: 加载文件路径，默认在当前目录

        Returns:
            Optional[Player]: 加载的玩家对象，如果失败则返回None
        """
        try:
            if not os.path.exists(filepath):
                return None

            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # 验证必要字段
            required_fields = ["name", "sect", "level", "experience"]
            for field_name in required_fields:
                if field_name not in data:
                    raise ValueError(f"缺少必要字段: {field_name}")

            # 创建玩家对象
            # 安全获取修炼境界
            cultivation_name = data.get("cultivation", "凡人")
            try:
                cultivation = CultivationLevel[cultivation_name]
            except KeyError:
                # 如果获取失败，默认使用凡人
                cultivation = CultivationLevel.凡人

            player = cls(
                name=data["name"],
                sect=Sect(data["sect"]),
                level=int(data["level"]),
                experience=int(data["experience"]),
                cultivation=cultivation,
                skills=data.get("skills", []),
                achievements=data.get("achievements", []),
                current_chapter=data.get("current_chapter", "序章"),
                kubectl_commands_mastered=data.get("kubectl_commands_mastered", []),
                challenges_completed=data.get("challenges_completed", []),
                streak=data.get("streak", 0),
                total_correct=data.get("total_correct", 0),
                total_attempts=data.get("total_attempts", 0),
                custom_titles=data.get("custom_titles", []),
                sect_bonus=data.get("sect_bonus", 1.0),
                # 装备系统
                equipped_weapon=Equipment.from_dict(data["equipped_weapon"]) if data.get("equipped_weapon") else None,
                equipped_armor=Equipment.from_dict(data["equipped_armor"]) if data.get("equipped_armor") else None,
                equipped_accessory=Equipment.from_dict(data["equipped_accessory"]) if data.get("equipped_accessory") else None,
                inventory=[Equipment.from_dict(eq) for eq in data.get("inventory", [])],
                # 技能和天赋系统
                skill_manager_data=data.get("skill_manager_data"),
                talent_tree_data=data.get("talent_tree_data"),
                # 副本系统
                dungeon_manager_data=data.get("dungeon_manager_data"),
                tower_progress_data=data.get("tower_progress_data"),
                # 体力系统
                stamina=data.get("stamina", 100),
                max_stamina=data.get("max_stamina", 100),
                last_stamina_refresh=data.get("last_stamina_refresh"),
            )

            # 加载成就对象
            if "achievement_objects" in data:
                player.achievement_objects = []
                for ach_data in data["achievement_objects"]:
                    ach_type = AchievementType(ach_data["type"])
                    achievement = Achievement(
                        id=ach_data["id"],
                        name=ach_data["name"],
                        description=ach_data["description"],
                        achievement_type=ach_type,
                        condition=ach_data["condition"],
                        reward=ach_data["reward"]
                    )
                    achievement.unlocked = ach_data["unlocked"]
                    player.achievement_objects.append(achievement)
            else:
                # 如果没有成就对象数据，初始化成就系统
                player._initialize_achievements()

            return player
        except FileNotFoundError:
            return None
        except (json.JSONDecodeError, ValueError, TypeError) as e:
            print(f"加载玩家数据失败: {str(e)}")
            return None

    def get_progress(self) -> Dict[str, Any]:
        """获取学习进度

        返回玩家当前的学习进度和游戏状态。

        Returns:
            Dict[str, Any]: 包含当前进度信息的字典
        """
        return {
            "level": self.level,
            "experience": self.experience,
            "required_exp": self._calculate_required_exp(),
            "commands_mastered": len(self.kubectl_commands_mastered),
            "challenges_completed": len(self.challenges_completed),
            "cultivation": self.cultivation.name,
            "cultivation_title": self.cultivation.value,
        }

    def has_mastered_command(self, command: str) -> bool:
        """检查是否已掌握命令

        检查玩家是否已经掌握了指定的Kubernetes命令。

        Args:
            command: 要检查的命令

        Returns:
            bool: 如果已掌握则返回True，否则返回False
        """
        return command in self.kubectl_commands_mastered

    def has_completed_challenge(self, challenge_id: str) -> bool:
        """检查是否已完成挑战

        检查玩家是否已经完成了指定的挑战。

        Args:
            challenge_id: 要检查的挑战ID

        Returns:
            bool: 如果已完成则返回True，否则返回False
        """
        return challenge_id in self.challenges_completed

    def reset_progress(self) -> None:
        """重置进度

        重置玩家的学习进度，但保留基本信息（名称、门派）。
        """
        self.level = 1
        self.experience = 0
        self.cultivation = CultivationLevel.凡人
        self.skills = []
        self.achievements = []
        self.current_chapter = "序章"
        self.kubectl_commands_mastered = []
        self.challenges_completed = []

    # ==================== 装备系统方法 ====================
    
    @property
    def total_attack(self) -> int:
        """计算总攻击力（基础属性 + 装备加成）
        
        Returns:
            int: 总攻击力
        """
        equipment_bonus = 0
        if self.equipped_weapon:
            equipment_bonus += self.equipped_weapon.total_attack
        if self.equipped_accessory:
            equipment_bonus += self.equipped_accessory.total_attack
        return self.attack + equipment_bonus
    
    @property
    def total_defense(self) -> int:
        """计算总防御力（基础属性 + 装备加成）
        
        Returns:
            int: 总防御力
        """
        equipment_bonus = 0
        if self.equipped_armor:
            equipment_bonus += self.equipped_armor.total_defense
        if self.equipped_accessory:
            equipment_bonus += self.equipped_accessory.total_defense
        return self.defense + equipment_bonus
    
    @property
    def total_max_health(self) -> int:
        """计算最大生命值（基础属性 + 装备加成）
        
        Returns:
            int: 最大生命值
        """
        equipment_bonus = 0
        if self.equipped_armor:
            equipment_bonus += self.equipped_armor.total_health
        if self.equipped_accessory:
            equipment_bonus += self.equipped_accessory.total_health
        return self.max_health + equipment_bonus
    
    @property
    def exp_bonus(self) -> float:
        """计算经验值加成
        
        Returns:
            float: 经验值加成百分比
        """
        bonus = 0.0
        if self.equipped_weapon:
            bonus += self.equipped_weapon.exp_bonus
        if self.equipped_armor:
            bonus += self.equipped_armor.exp_bonus
        if self.equipped_accessory:
            bonus += self.equipped_accessory.exp_bonus
        return bonus
    
    @property
    def streak_bonus(self) -> float:
        """计算连击加成
        
        Returns:
            float: 连击加成百分比
        """
        bonus = 0.0
        if self.equipped_weapon:
            bonus += self.equipped_weapon.streak_bonus
        if self.equipped_armor:
            bonus += self.equipped_armor.streak_bonus
        if self.equipped_accessory:
            bonus += self.equipped_accessory.streak_bonus
        return bonus
    
    def equip_item(self, equipment: Equipment) -> bool:
        """装备物品
        
        将装备放入对应的装备槽，原来的装备（如果有）会回到背包。
        
        Args:
            equipment: 要装备的装备
            
        Returns:
            bool: 装备成功返回True
        """
        # 从背包中移除
        if equipment in self.inventory:
            self.inventory.remove(equipment)
        
        # 根据装备类型放入对应槽位
        if equipment.equipment_type == EquipmentType.武器:
            if self.equipped_weapon:
                self.unequip_item(EquipmentType.武器)
            self.equipped_weapon = equipment
            equipment.equipped = True
            
        elif equipment.equipment_type == EquipmentType.护甲:
            if self.equipped_armor:
                self.unequip_item(EquipmentType.护甲)
            self.equipped_armor = equipment
            equipment.equipped = True
            
        elif equipment.equipment_type == EquipmentType.饰品:
            if self.equipped_accessory:
                self.unequip_item(EquipmentType.饰品)
            self.equipped_accessory = equipment
            equipment.equipped = True
        
        # 更新生命值上限
        new_max_health = self.total_max_health
        health_ratio = self.health / self.max_health if self.max_health > 0 else 1
        self.max_health = new_max_health
        self.health = int(self.max_health * health_ratio)
        
        return True
    
    def unequip_item(self, equipment_type: EquipmentType) -> Optional[Equipment]:
        """卸下装备
        
        将指定类型的装备卸下，放回背包。
        
        Args:
            equipment_type: 装备类型
            
        Returns:
            Optional[Equipment]: 卸下的装备，如果没有则返回None
        """
        unequipped = None
        
        if equipment_type == EquipmentType.武器 and self.equipped_weapon:
            unequipped = self.equipped_weapon
            self.equipped_weapon.equipped = False
            self.equipped_weapon = None
            
        elif equipment_type == EquipmentType.护甲 and self.equipped_armor:
            unequipped = self.equipped_armor
            self.equipped_armor.equipped = False
            self.equipped_armor = None
            
        elif equipment_type == EquipmentType.饰品 and self.equipped_accessory:
            unequipped = self.equipped_accessory
            self.equipped_accessory.equipped = False
            self.equipped_accessory = None
        
        # 放回背包
        if unequipped:
            self.inventory.append(unequipped)
        
        return unequipped
    
    def add_to_inventory(self, equipment: Equipment) -> None:
        """添加装备到背包
        
        Args:
            equipment: 要添加的装备
        """
        self.inventory.append(equipment)
    
    def remove_from_inventory(self, equipment: Equipment) -> bool:
        """从背包移除装备
        
        Args:
            equipment: 要移除的装备
            
        Returns:
            bool: 移除成功返回True
        """
        if equipment in self.inventory:
            self.inventory.remove(equipment)
            return True
        return False
    
    def get_equipment_summary(self) -> Dict[str, Any]:
        """获取装备汇总信息
        
        Returns:
            Dict[str, Any]: 装备汇总信息
        """
        return {
            "weapon": self.equipped_weapon.to_dict() if self.equipped_weapon else None,
            "armor": self.equipped_armor.to_dict() if self.equipped_armor else None,
            "accessory": self.equipped_accessory.to_dict() if self.equipped_accessory else None,
            "inventory_count": len(self.inventory),
            "total_attack": self.total_attack,
            "total_defense": self.total_defense,
            "total_max_health": self.total_max_health,
            "exp_bonus": self.exp_bonus,
            "streak_bonus": self.streak_bonus,
        }

    # ==================== 技能和天赋系统方法 ====================
    
    def _initialize_skill_manager(self) -> None:
        """初始化技能管理器"""
        if not hasattr(self, '_skill_manager'):
            from .skills import SkillManager
            if self.skill_manager_data:
                self._skill_manager = SkillManager.from_dict(self.skill_manager_data)
            else:
                self._skill_manager = SkillManager(sect=self.sect)
    
    @property
    def skill_manager(self):
        """获取技能管理器"""
        if not hasattr(self, '_skill_manager') or self._skill_manager is None:
            self._initialize_skill_manager()
        return self._skill_manager
    
    def _initialize_talent_tree(self) -> None:
        """初始化天赋树"""
        if not hasattr(self, '_talent_tree'):
            from .talent_tree import TalentTree
            if self.talent_tree_data:
                self._talent_tree = TalentTree.from_dict(self.talent_tree_data)
            else:
                self._talent_tree = TalentTree(sect=self.sect)
    
    @property
    def talent_tree(self):
        """获取天赋树"""
        if not hasattr(self, '_talent_tree') or self._talent_tree is None:
            self._initialize_talent_tree()
        return self._talent_tree
    
    def get_skill_bonuses(self) -> Dict[str, float]:
        """获取技能加成
        
        Returns:
            Dict[str, float]: 各种加成值
        """
        bonuses = {
            "damage_reduction": 0.0,
            "lifesteal": 0.0,
            "exp_bonus": 0.0,
            "dodge_chance": 0.0,
        }
        
        if hasattr(self, '_skill_manager') and self._skill_manager:
            # 青云宗：稳如泰山 - 减伤20%
            if "qingyun_steady" in self._skill_manager.skills:
                bonuses["damage_reduction"] += 0.2
            
            # 炼狱门：嗜血 - 吸血20%
            if "liyu_lifesteal" in self._skill_manager.skills:
                bonuses["lifesteal"] += 0.2
            
            # 逍遥派：因材施教 - 经验+50%
            if "xiaoyao_teach" in self._skill_manager.skills:
                bonuses["exp_bonus"] += 0.5
        
        return bonuses
    
    def get_talent_bonuses(self) -> Dict[str, float]:
        """获取天赋加成
        
        Returns:
            Dict[str, float]: 各种加成值
        """
        bonuses = {
            "attack": 0.0,
            "defense": 0.0,
            "health": 0.0,
            "exp_bonus": 0.0,
        }
        
        if hasattr(self, '_talent_tree') and self._talent_tree:
            # 攻击天赋加成
            bonuses["attack"] = self._talent_tree.get_total_bonus("atk")
            # 防御天赋加成
            bonuses["defense"] = self._talent_tree.get_total_bonus("def")
            # 辅助天赋的经验加成
            bonuses["exp_bonus"] = self._talent_tree.get_total_bonus("exp")
        
        return bonuses
    
    def on_level_up(self) -> None:
        """升级时的额外处理"""
        # 天赋树获得天赋点
        if hasattr(self, '_talent_tree') and self._talent_tree:
            self._talent_tree.on_level_up()

    # ==================== 体力系统方法 ====================
    
    def recover_stamina(self) -> int:
        """恢复体力
        
        根据时间自动恢复体力，每6分钟恢复1点。
        
        Returns:
            int: 实际恢复的体力点数
        """
        if not self.last_stamina_refresh:
            self.last_stamina_refresh = datetime.now().isoformat()
            return 0
        
        try:
            last = datetime.fromisoformat(self.last_stamina_refresh)
            now = datetime.now()
            elapsed_minutes = (now - last).total_seconds() / 60
            
            # 每6分钟恢复1点
            recovery = int(elapsed_minutes / 6)
            
            if recovery > 0:
                old_stamina = self.stamina
                self.stamina = min(self.max_stamina, self.stamina + recovery)
                self.last_stamina_refresh = now.isoformat()
                return self.stamina - old_stamina
            
            return 0
        except (ValueError, TypeError):
            # 如果解析失败，重置时间戳
            self.last_stamina_refresh = datetime.now().isoformat()
            return 0
    
    def consume_stamina(self, amount: int) -> bool:
        """消耗体力
        
        Args:
            amount: 消耗的体力点数
            
        Returns:
            bool: 消耗成功返回True，体力不足返回False
        """
        # 先尝试恢复体力
        self.recover_stamina()
        
        if self.stamina >= amount:
            self.stamina -= amount
            return True
        return False
    
    def get_stamina_status(self) -> Dict[str, Any]:
        """获取体力状态
        
        Returns:
            Dict[str, Any]: 体力状态信息
        """
        # 先恢复体力以获取最新状态
        recovered = self.recover_stamina()
        
        # 计算下次恢复时间
        time_to_next = 0
        if self.stamina < self.max_stamina:
            try:
                last = datetime.fromisoformat(self.last_stamina_refresh) if self.last_stamina_refresh else datetime.now()
                now = datetime.now()
                elapsed_seconds = (now - last).total_seconds()
                time_to_next = max(0, 360 - int(elapsed_seconds))  # 6分钟 = 360秒
            except (ValueError, TypeError):
                pass
        
        return {
            "stamina": self.stamina,
            "max_stamina": self.max_stamina,
            "percentage": int(self.stamina / self.max_stamina * 100),
            "recovered": recovered,
            "time_to_next_recovery": time_to_next,
            "is_full": self.stamina >= self.max_stamina
        }

    # ==================== 成就系统扩展方法 ====================
    
    def check_level_achievements(self) -> List[str]:
        """检查等级相关成就
        
        Returns:
            List[str]: 解锁的成就名称列表
        """
        unlocked = []
        level_achievements = {
            "level_10": 10,
            "level_30": 30,
            "level_50": 50,
            "level_100": 100,
        }
        
        for ach_id, required_level in level_achievements.items():
            if self.level >= required_level:
                for achievement in self.achievement_objects:
                    if achievement.id == ach_id and not achievement.unlocked:
                        achievement.unlocked = True
                        self.achievements.append(achievement.id)
                        # 应用奖励
                        if "experience" in achievement.reward:
                            self.gain_experience(achievement.reward["experience"])
                        unlocked.append(achievement.name)
        
        return unlocked
    
    def check_equipment_achievements(self, equipment_count: int, has_orange: bool = False) -> List[str]:
        """检查装备收集成就
        
        Args:
            equipment_count: 收集的装备数量
            has_orange: 是否拥有传说装备
            
        Returns:
            List[str]: 解锁的成就名称列表
        """
        unlocked = []
        
        # 装备数量成就
        count_achievements = {
            "equipment_10": 10,
            "equipment_50": 50,
        }
        
        for ach_id, required_count in count_achievements.items():
            if equipment_count >= required_count:
                for achievement in self.achievement_objects:
                    if achievement.id == ach_id and not achievement.unlocked:
                        achievement.unlocked = True
                        self.achievements.append(achievement.id)
                        if "experience" in achievement.reward:
                            self.gain_experience(achievement.reward["experience"])
                        unlocked.append(achievement.name)
        
        # 传说装备成就
        if has_orange:
            for achievement in self.achievement_objects:
                if achievement.id == "equipment_orange" and not achievement.unlocked:
                    achievement.unlocked = True
                    self.achievements.append(achievement.id)
                    if "experience" in achievement.reward:
                        self.gain_experience(achievement.reward["experience"])
                    unlocked.append(achievement.name)
        
        return unlocked
    
    def check_tower_achievements(self, highest_level: int) -> List[str]:
        """检查挑战塔成就
        
        Args:
            highest_level: 最高通关层数
            
        Returns:
            List[str]: 解锁的成就名称列表
        """
        unlocked = []
        tower_achievements = {
            "tower_10": 10,
            "tower_50": 50,
            "tower_100": 100,
        }
        
        for ach_id, required_level in tower_achievements.items():
            if highest_level >= required_level:
                for achievement in self.achievement_objects:
                    if achievement.id == ach_id and not achievement.unlocked:
                        achievement.unlocked = True
                        self.achievements.append(achievement.id)
                        if "experience" in achievement.reward:
                            self.gain_experience(achievement.reward["experience"])
                        unlocked.append(achievement.name)
        
        return unlocked
    
    def check_combat_achievements(self, total_combats: int, wins: int) -> List[str]:
        """检查战斗成就
        
        Args:
            total_combats: 总战斗次数
            wins: 胜利次数
            
        Returns:
            List[str]: 解锁的成就名称列表
        """
        unlocked = []
        
        if total_combats >= 100:
            for achievement in self.achievement_objects:
                if achievement.id == "combat_100" and not achievement.unlocked:
                    achievement.unlocked = True
                    self.achievements.append(achievement.id)
                    if "experience" in achievement.reward:
                        self.gain_experience(achievement.reward["experience"])
                    unlocked.append(achievement.name)
        
        if wins >= 50:
            for achievement in self.achievement_objects:
                if achievement.id == "combat_win_50" and not achievement.unlocked:
                    achievement.unlocked = True
                    self.achievements.append(achievement.id)
                    if "experience" in achievement.reward:
                        self.gain_experience(achievement.reward["experience"])
                    unlocked.append(achievement.name)
        
        return unlocked
    
    def unlock_first_login(self) -> bool:
        """解锁首次登录成就
        
        Returns:
            bool: 是否成功解锁
        """
        for achievement in self.achievement_objects:
            if achievement.id == "first_login" and not achievement.unlocked:
                achievement.unlocked = True
                self.achievements.append(achievement.id)
                if "experience" in achievement.reward:
                    self.gain_experience(achievement.reward["experience"])
                return True
        return False
    
    def check_perfect_answer(self, correct_count: int) -> List[str]:
        """检查完美答题成就
        
        Args:
            correct_count: 连续答对题数
            
        Returns:
            List[str]: 解锁的成就名称列表
        """
        unlocked = []
        
        if correct_count >= 10:
            for achievement in self.achievement_objects:
                if achievement.id == "perfect_answer" and not achievement.unlocked:
                    achievement.unlocked = True
                    self.achievements.append(achievement.id)
                    if "experience" in achievement.reward:
                        self.gain_experience(achievement.reward["experience"])
                    unlocked.append(achievement.name)
        
        return unlocked
    
    def get_achievement_stats(self) -> Dict[str, Any]:
        """获取成就统计
        
        Returns:
            Dict[str, Any]: 成就统计信息
        """
        total = len(self.achievement_objects)
        unlocked = sum(1 for a in self.achievement_objects if a.unlocked)
        
        by_type = {}
        for ach_type in AchievementType:
            type_achievements = [a for a in self.achievement_objects if a.type == ach_type]
            type_unlocked = sum(1 for a in type_achievements if a.unlocked)
            by_type[ach_type.value] = {
                "total": len(type_achievements),
                "unlocked": type_unlocked,
                "percentage": round(type_unlocked / len(type_achievements) * 100, 1) if type_achievements else 0
            }
        
        return {
            "total_achievements": total,
            "unlocked_count": unlocked,
            "locked_count": total - unlocked,
            "completion_percentage": round(unlocked / total * 100, 1) if total else 0,
            "by_type": by_type,
            "recent_unlocked": [
                {"id": a.id, "name": a.name, "description": a.description}
                for a in self.achievement_objects
                if a.unlocked
            ][-5:]  # 最近5个解锁的成就
        }

    # ==================== 每日签到系统 ====================
    
    def get_checkin_manager(self) -> DailyCheckin:
        """获取签到管理器
        
        Returns:
            DailyCheckin: 签到管理器对象
        """
        return DailyCheckin.from_dict(self.checkin_data or {})
    
    def checkin(self) -> Dict[str, Any]:
        """执行每日签到
        
        Returns:
            Dict[str, Any]: 签到结果
        """
        checkin_manager = self.get_checkin_manager()
        
        result = checkin_manager.checkin()
        
        if result["success"]:
            # 更新签到数据
            self.checkin_data = checkin_manager.to_dict()
            
            # 应用奖励
            rewards = result["rewards"]
            
            # 经验奖励
            if "experience" in rewards:
                self.gain_experience(rewards["experience"])
            
            # 体力奖励
            if "stamina" in rewards:
                self.stamina = min(self.max_stamina, self.stamina + rewards["stamina"])
            
            # 添加结果信息
            result["current_exp"] = self.experience
            result["current_level"] = self.level
            result["current_stamina"] = self.stamina
        
        return result
    
    def get_checkin_status(self) -> Dict[str, Any]:
        """获取签到状态
        
        Returns:
            Dict[str, Any]: 签到状态信息
        """
        checkin_manager = self.get_checkin_manager()
        return checkin_manager.get_checkin_status()
    
    def get_monthly_checkin_status(self) -> Dict[str, Any]:
        """获取月度签到状态
        
        Returns:
            Dict[str, Any]: 月度签到状态
        """
        checkin_manager = self.get_checkin_manager()
        return checkin_manager.get_monthly_reward_status()

    # ==================== 任务系统 ====================
    
    def get_quest_manager(self) -> "QuestManager":
        """获取任务管理器
        
        Returns:
            QuestManager: 任务管理器对象
        """
        from .quest_system import QuestManager
        return QuestManager.from_dict(self.quest_data or {})
    
    def refresh_daily_quests(self) -> List[str]:
        """刷新每日任务
        
        Returns:
            List[str]: 新增任务名称列表
        """
        quest_manager = self.get_quest_manager()
        
        if quest_manager.check_and_reset_daily_quests():
            self.quest_data = quest_manager.to_dict()
            return [q.name for q in quest_manager.active_quests if q.quest_type.value == "daily"]
        return []
    
    def refresh_weekly_quests(self) -> List[str]:
        """刷新每周任务
        
        Returns:
            List[str]: 新增任务名称列表
        """
        quest_manager = self.get_quest_manager()
        
        if quest_manager.check_and_reset_weekly_quests():
            self.quest_data = quest_manager.to_dict()
            return [q.name for q in quest_manager.active_quests if q.quest_type.value == "weekly"]
        return []
    
    def update_quest_progress(self, objective_type_str: str, value: int = 1) -> List[Dict[str, Any]]:
        """更新任务进度
        
        Args:
            objective_type_str: 目标类型字符串
            value: 增加的值
            
        Returns:
            List[Dict]: 刚完成的任务信息列表
        """
        from .quest_system import QuestObjectiveType
        
        quest_manager = self.get_quest_manager()
        
        try:
            objective_type = QuestObjectiveType(objective_type_str)
        except ValueError:
            return []
        
        completed = quest_manager.update_quest_progress(objective_type, value)
        
        if completed:
            self.quest_data = quest_manager.to_dict()
            return [
                {
                    "id": q.id,
                    "name": q.name,
                    "rewards": q.rewards
                }
                for q in completed
            ]
        return []
    
    def get_available_main_quests(self) -> List[Dict[str, Any]]:
        """获取可接受的主线任务
        
        Returns:
            List[Dict]: 任务信息列表
        """
        from .main_quests import get_available_main_quests
        
        quest_manager = self.get_quest_manager()
        quests = get_available_main_quests(quest_manager.completed_quests, self.level)
        
        return [
            {
                "id": q.id,
                "name": q.name,
                "description": q.description,
                "level_requirement": q.level_requirement,
                "rewards": q.rewards,
                "prerequisites": q.prerequisite_quests,
            }
            for q in quests
        ]
    
    def get_available_side_quests(self) -> List[Dict[str, Any]]:
        """获取可接受的支线任务
        
        Returns:
            List[Dict]: 任务信息列表
        """
        from .main_quests import get_available_side_quests
        
        quest_manager = self.get_quest_manager()
        quests = get_available_side_quests(quest_manager.completed_quests, self.level)
        
        return [
            {
                "id": q.id,
                "name": q.name,
                "description": q.description,
                "level_requirement": q.level_requirement,
                "rewards": q.rewards,
            }
            for q in quests
        ]
    
    def accept_quest(self, quest_id: str) -> bool:
        """接受任务
        
        Args:
            quest_id: 任务ID
            
        Returns:
            bool: 是否成功接受
        """
        from .main_quests import create_main_quests, create_side_quests
        
        quest_manager = self.get_quest_manager()
        
        # 查找任务
        all_quests = create_main_quests() + create_side_quests()
        quest = None
        for q in all_quests:
            if q.id == quest_id:
                quest = q
                break
        
        if quest is None:
            return False
        
        # 检查是否已接受或已完成
        if any(q.id == quest_id for q in quest_manager.active_quests):
            return False
        
        if quest_id in quest_manager.completed_quests:
            return False
        
        # 接受任务
        quest.status = QuestStatus.进行中
        quest_manager.active_quests.append(quest)
        self.quest_data = quest_manager.to_dict()
        
        return True
    
    def claim_quest_reward(self, quest_id: str) -> Optional[Dict[str, Any]]:
        """领取任务奖励
        
        Args:
            quest_id: 任务ID
            
        Returns:
            Optional[Dict]: 奖励字典
        """
        quest_manager = self.get_quest_manager()
        
        rewards = quest_manager.claim_reward(quest_id)
        
        if rewards:
            self.quest_data = quest_manager.to_dict()
            
            # 应用奖励
            if "experience" in rewards:
                self.gain_experience(rewards["experience"])
            if "stamina" in rewards:
                self.stamina = min(self.max_stamina, self.stamina + rewards["stamina"])
            if "title" in rewards:
                self.custom_titles.append(rewards["title"])
        
        return rewards
    
    def get_quest_summary(self) -> Dict[str, Any]:
        """获取任务摘要
        
        Returns:
            Dict: 任务统计信息
        """
        quest_manager = self.get_quest_manager()
        summary = quest_manager.get_quest_summary()
        
        # 添加主线和支线任务统计
        main_available = len(self.get_available_main_quests())
        side_available = len(self.get_available_side_quests())
        
        return {
            **summary,
            "main_available": main_available,
            "side_available": side_available,
            "daily_active": len([q for q in quest_manager.active_quests if q.quest_type.value == "daily" and q.status.value in ["not_accepted", "in_progress"]]),
            "weekly_active": len([q for q in quest_manager.active_quests if q.quest_type.value == "weekly" and q.status.value in ["not_accepted", "in_progress"]]),
        }
    
    def get_active_quests_info(self) -> List[Dict[str, Any]]:
        """获取进行中的任务信息
        
        Returns:
            List[Dict]: 任务信息列表
        """
        quest_manager = self.get_quest_manager()
        
        return [
            {
                "id": q.id,
                "name": q.name,
                "description": q.description,
                "type": q.quest_type.value,
                "status": q.status.value,
                "progress": q.overall_progress,
                "objectives": [
                    {
                        "description": obj.description,
                        "current": obj.current_value,
                        "target": obj.target_value,
                        "completed": obj.is_completed,
                    }
                    for obj in q.objectives
                ],
                "rewards": q.rewards,
            }
            for q in quest_manager.active_quests
            if q.status.value in ["not_accepted", "in_progress", "completed"]
        ]
