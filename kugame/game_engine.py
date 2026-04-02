"""游戏引擎

KuGame的核心游戏逻辑引擎，负责处理游戏状态管理、挑战生成、答案验证等核心功能。
"""
# -*- coding: utf-8 -*-

from typing import Dict, List, Optional, Any
from enum import Enum
from dataclasses import dataclass
from .player import Player, Sect
from .story import StoryManager, Chapter
from .kubernetes_commands import KubernetesCommandManager
from .equipment import EquipmentManager, Equipment, EquipmentType
from .dungeon import DungeonManager, Dungeon
from .tower import ChallengeTower, TowerProgress
import random
import os
import json


class GameState(Enum):
    """游戏状态枚举

    定义游戏的各种状态，用于状态管理和流程控制。
    """
    MENU = "menu"  # 主菜单
    STORY = "story"  # 故事模式
    PRACTICE = "practice"  # 练习模式
    CHALLENGE = "challenge"  # 挑战模式
    QUIZ = "quiz"  # 测验模式
    PROGRESS = "progress"  # 进度查看
    QUIT = "quit"  # 退出游戏


@dataclass
class Challenge:
    """挑战数据类

    表示游戏中的一个挑战任务，包含挑战的各种属性。

    Attributes:
        challenge_id: 挑战唯一标识
        title: 挑战标题
        description: 挑战描述
        question: 挑战问题
        expected_command: 预期的命令答案
        options: 挑战选项列表
        correct_option_index: 正确选项索引
        hint: 提示信息
        reward_exp: 完成挑战获得的经验值
        difficulty: 挑战难度（1-10）
    """
    challenge_id: str
    title: str
    description: str
    question: str
    expected_command: str
    options: List[str]
    correct_option_index: int
    hint: str
    reward_exp: int
    difficulty: int


class GameEngine:
    """游戏引擎

    负责游戏的核心逻辑，包括玩家管理、故事推进、挑战生成、答案验证等。

    Attributes:
        story_manager: 故事管理器，负责故事章节和剧情
        command_manager: Kubernetes命令管理器，负责命令验证和学习
        player: 当前玩家对象
        state: 当前游戏状态
        current_challenge: 当前正在进行的挑战
        score: 玩家总得分
        streak: 连续正确回答的次数
    """
    state: GameState
    player: Optional[Player]
    current_challenge: Optional[Challenge]
    score: float
    streak: int
    story_manager: StoryManager
    command_manager: KubernetesCommandManager
    current_monster: Optional[Any]
    monster_current_health: int

    def __init__(self) -> None:
        """初始化游戏引擎"""
        self.story_manager = StoryManager()
        self.command_manager = KubernetesCommandManager()
        self.player: Optional[Player] = None
        self.state = GameState.MENU
        self.current_challenge: Optional[Challenge] = None
        self.score: float = 0.0
        self.streak: int = 0

        # 战斗系统属性
        self.current_monster: Optional[Any] = None
        self.monster_current_health: int = 0
        
        # 装备系统
        self.equipment_manager = EquipmentManager()
        self.shop_refresh_count = 0  # 商店刷新次数
        
        # 副本系统（延迟初始化，需要玩家数据）
        self.dungeon_manager: Optional[DungeonManager] = None
        self.challenge_tower = ChallengeTower()
        self.tower_progress: Optional[TowerProgress] = None

    def initialize_player(self, name: str, sect: Sect) -> Player:
        """初始化玩家

        创建新玩家并保存到本地。

        Args:
            name: 玩家名称
            sect: 玩家选择的门派

        Returns:
            创建的玩家对象
        """
        if not name or not isinstance(name, str):
            raise ValueError("玩家名称必须是非空字符串")

        if not isinstance(sect, Sect):
            raise ValueError("门派必须是Sect枚举类型")

        self.player = Player(name=name, sect=sect)
        self.player.save()
        
        # 初始化副本系统
        self.dungeon_manager = DungeonManager()
        self.tower_progress = TowerProgress()
        
        return self.player

    def load_player(self, filepath: str = "player_save.json") -> Optional[Player]:
        """加载玩家

        从本地文件加载玩家数据。

        Args:
            filepath: 加载文件路径，默认在当前目录

        Returns:
            加载的玩家对象，如果没有保存的玩家则返回None
        """
        self.player = Player.load(filepath)
        if self.player:
            # 确保当前章节有效
            try:
                self.story_manager.current_chapter = Chapter(self.player.current_chapter)
            except ValueError:
                self.story_manager.current_chapter = Chapter.序章
            
            # 初始化副本系统
            self.dungeon_manager = DungeonManager()
            if self.player.dungeon_manager_data:
                self.dungeon_manager = DungeonManager.from_dict(self.player.dungeon_manager_data)
            
            # 初始化挑战塔进度
            if self.player.tower_progress_data:
                self.tower_progress = TowerProgress.from_dict(self.player.tower_progress_data)
            else:
                self.tower_progress = TowerProgress()
        
        return self.player

    def save_game(self, save_name: Optional[str] = None) -> bool:
        """保存游戏

        保存当前玩家的游戏进度到本地文件。

        Args:
            save_name: 存档名称，不包含文件扩展名

        Returns:
            如果保存成功则返回True，否则返回False
        """
        if not self.player:
            return False

        try:
            # 保存副本系统数据
            if self.dungeon_manager:
                self.player.dungeon_manager_data = self.dungeon_manager.to_dict()
            if self.tower_progress:
                self.player.tower_progress_data = self.tower_progress.to_dict()
            
            # 如果提供了存档名称，使用自定义名称，否则使用默认名称
            if save_name:
                # 确保文件扩展名是.json
                if not save_name.endswith('.json'):
                    save_name += '.json'
                self.player.save(save_name)
            else:
                self.player.save()
            return True
        except Exception as e:
            # 记录保存失败日志
            print(f"保存游戏失败: {str(e)}")
            return False

    def get_menu_options(self) -> List[Dict[str, str]]:
        """获取菜单选项

        返回游戏主菜单的选项列表。

        Returns:
            菜单选项列表，每个选项包含id、name和description
        """
        return [
            {"id": "story", "name": "📖 开始故事", "description": "继续阅读故事，学习Kubernetes命令"},
            {"id": "practice", "name": "⚔️ 修炼场", "description": "练习已学命令"},
            {"id": "challenge", "name": "🏆 挑战关卡", "description": "完成挑战任务"},
            {"id": "quiz", "name": "📝 知识问答", "description": "测试你的知识"},
            {"id": "progress", "name": "📊 修炼进度", "description": "查看学习进度"},
            {"id": "commands", "name": "📚 命令手册", "description": "查看所有命令"},
            {"id": "equipment", "name": "🎒 装备管理", "description": "查看、装备、强化装备"},
            {"id": "shop", "name": "🏪 仙缘商店", "description": "购买装备、出售物品"},
            {"id": "dungeon", "name": "🏰 副本挑战", "description": "每日副本、无尽之塔"},
            {"id": "checkin", "name": "📅 每日签到", "description": "领取每日签到奖励"},
            {"id": "help", "name": "❓ 帮助指南", "description": "游戏帮助和系统说明"},
            {"id": "save", "name": "💾 保存进度", "description": "保存当前进度"},
            {"id": "save_manager", "name": "📁 档案管理", "description": "管理游戏存档"},
            {"id": "quit", "name": "🚪 退出游戏", "description": "退出游戏"},
        ]

    def get_story_content(self) -> Dict[str, Any]:
        """获取当前故事内容

        返回当前章节的故事内容，包括介绍、叙述、概念和命令等。

        Returns:
            当前章节的故事内容字典
        """
        chapter = self.story_manager.get_current_chapter()
        return {
            "chapter_id": chapter.chapter_id.value,
            "title": chapter.title,
            "introduction": chapter.introduction,
            "narrative": chapter.narrative,
            "concepts": chapter.kubernetes_concepts,
            "commands": chapter.commands_to_learn,
            "reward_exp": chapter.reward_exp,
            "ascii_image": chapter.ascii_image,
        }

    def generate_challenge(self) -> Optional[Challenge]:
        """生成挑战

        根据当前章节的命令生成一个挑战任务，包含多个选项。

        Returns:
            生成的挑战对象，如果没有可用命令则返回None
        """
        chapter = self.story_manager.get_current_chapter()
        commands = chapter.commands_to_learn

        if not commands:
            return None

        target_command = random.choice(commands)
        cmd_info = self.command_manager.get_command(target_command)

        if not cmd_info:
            return None

        challenge_id = f"{chapter.chapter_id.value}_challenge_{random.randint(1000, 9999)}"

        # 计算难度，根据章节ID中的数字
        chapter_num = int(chapter.chapter_id.value.split('_')[-1]) if 'chapter_' in chapter.chapter_id.value else 0
        difficulty = min(10, chapter_num + 1)  # 限制难度在1-10之间

        # 生成选项：1个正确选项 + 3-4个干扰选项
        all_commands = list(self.command_manager.commands.keys())

        # 移除正确选项，避免重复
        all_commands = [cmd for cmd in all_commands if cmd != target_command]

        # 随机选择3个干扰选项
        num_distractors = 3
        distractors = random.sample(all_commands, num_distractors) if len(all_commands) >= num_distractors else all_commands

        # 构建选项列表并随机排序
        options = [target_command] + distractors
        random.shuffle(options)

        # 找到正确选项的索引
        correct_index = options.index(target_command)

        # 确保cmd_info是KubectlCommand类型
        from .kubernetes_commands import KubectlCommand
        concept = cmd_info.kubernetes_concept if isinstance(cmd_info, KubectlCommand) else ''

        challenge = Challenge(
            challenge_id=challenge_id,
            title=f"修炼挑战 - {concept if concept else cmd_info.name}",
            description=f"掌握{cmd_info.description}的技巧",
            question=f"如何{cmd_info.description}？",
            expected_command=target_command,
            options=options,
            correct_option_index=correct_index,
            hint=f"使用 {cmd_info.syntax} 格式",
            reward_exp=chapter.reward_exp,
            difficulty=difficulty,
        )

        self.current_challenge = challenge
        return challenge

    def check_answer(self, user_choice: int) -> Dict[str, Any]:
        """检查答案

        验证用户选择的选项索引是否正确，并返回结果。

        Args:
            user_choice: 用户选择的选项索引（从1开始）

        Returns:
            包含验证结果的字典，包括是否正确、消息、连击数、得分和解锁成就等
        """
        if not self.current_challenge:
            return {"correct": False, "message": "没有正在进行的挑战"}

        if not isinstance(user_choice, int):
            return {"correct": False, "message": "答案必须是整数类型"}

        # 转换为0-based索引
        user_index = user_choice - 1

        # 检查索引是否在有效范围内
        if user_index < 0 or user_index >= len(self.current_challenge.options):
            return {
                "correct": False,
                "message": f"✗ 无效选择，请选择1-{len(self.current_challenge.options)}之间的数字",
                "streak": self.streak,
                "score": int(self.score),
                "unlocked_achievements": []
            }

        # 检查答案是否正确
        is_correct = user_index == self.current_challenge.correct_option_index
        unlocked_achievements = []

        expected = self.current_challenge.expected_command
        selected_command = self.current_challenge.options[user_index]

        if is_correct:
            self.streak += 1
            # 连击加成，最多5倍
            streak_bonus = min(5.0, 1.0 + self.streak * 0.1)
            self.score += self.current_challenge.reward_exp * streak_bonus

            if self.player:
                # 更新玩家数据
                self.player.complete_challenge(self.current_challenge.challenge_id)
                self.player.learn_command(expected)
                self.player.gain_experience(self.current_challenge.reward_exp)

                # 更新连续成功次数和统计数据
                self.player.update_streak(True)

                # 检查并解锁成就
                unlocked_achievements = self.player.check_and_unlock_achievements()

                # 更新玩家的streak属性
                self.player.streak = self.streak
        else:
            self.streak = 0
            if self.player:
                # 更新玩家的连续成功次数
                self.player.update_streak(False)
                self.player.streak = self.streak
                # 记录错题
                self.player.wrong_commands.append(selected_command) if hasattr(self.player, 'wrong_commands') else None

        result = {
            "correct": is_correct,
            "streak": self.streak,
            "score": int(self.score),
            "unlocked_achievements": unlocked_achievements,
            "selected_option": user_index + 1,
            "correct_option": self.current_challenge.correct_option_index + 1
        }

        if is_correct:
            result["message"] = f"✓ 回答正确！获得 {int(self.current_challenge.reward_exp)} 经验值"
            result["streak_bonus"] = streak_bonus
        else:
            result["message"] = f"✗ 回答错误。正确答案是选项 {self.current_challenge.correct_option_index + 1}: {expected}"
            result["hint"] = self.current_challenge.hint
            result["expected"] = expected
            result["given"] = selected_command

        return result

    def advance_chapter(self) -> bool:
        """推进章节

        推进到下一个故事章节。

        Returns:
            如果成功推进到下一章节则返回True，否则返回False
        """
        if not self.player:
            raise ValueError("玩家未初始化，无法推进章节")

        if self.story_manager.advance_chapter():
            self.player.current_chapter = self.story_manager.current_chapter.value
            self.player.gain_experience(500)  # 章节奖励
            self.player.save()  # 自动保存进度
            return True
        return False

    def get_practice_commands(self) -> List[str]:
        """获取可练习的命令

        获取玩家已经掌握的命令列表，用于练习模式。

        Returns:
            可练习的命令列表
        """
        if not self.player:
            raise ValueError("玩家未初始化，无法获取练习命令")

        mastered = set(self.player.kubectl_commands_mastered)
        all_commands = set(self.command_manager.get_all_commands())
        return sorted(list(mastered.intersection(all_commands)))

    def generate_quiz(self) -> Optional[Dict[str, Any]]:
        """生成测验

        生成一个知识测验，包含问题、选项、正确答案等。

        Returns:
            测验字典，如果没有足够的命令则返回None
        """
        if not self.player:
            raise ValueError("玩家未初始化，无法生成测验")

        mastered = self.get_practice_commands()

        if not mastered:
            return {
                "question": "还没有掌握任何命令，请先完成故事章节",
                "options": [],
                "correct_index": -1,
                "explanation": "",
                "command": "",
                "concept": ""
            }

        target_command = random.choice(mastered)
        cmd_info = self.command_manager.get_command(target_command)

        if not cmd_info:
            return None

        # 生成干扰选项
        all_commands = self.command_manager.get_all_commands()
        potential_distractors = [c for c in all_commands if c != target_command]

        # 确保有足够的干扰选项
        if len(potential_distractors) < 3:
            distractors = potential_distractors
        else:
            distractors = random.sample(potential_distractors, 3)

        options = distractors + [target_command]
        random.shuffle(options)

        correct_index = options.index(target_command)

        # 确保cmd_info是KubectlCommand类型
        from .kubernetes_commands import KubectlCommand
        concept = cmd_info.kubernetes_concept if isinstance(cmd_info, KubectlCommand) else ''

        return {
            "question": f"以下哪个命令用于：{cmd_info.description}？",
            "options": options,
            "correct_index": correct_index,
            "explanation": f"示例：{cmd_info.example}",
            "command": target_command,
            "concept": concept
        }

    def get_progress(self) -> Dict[str, Any]:
        """获取游戏进度

        获取玩家的游戏进度，包括等级、经验、章节进度、命令掌握情况和成就进度等。

        Returns:
            包含玩家进度的字典
        """
        if not self.player:
            raise ValueError("玩家未初始化，无法获取进度")

        story_progress = self.story_manager.get_story_progress(self.player)
        command_report = self.command_manager.get_progress_report(
            self.player.kubectl_commands_mastered
        )
        achievement_progress = self.player.get_achievement_progress()

        player_progress = self.player.get_progress()

        return {
            "player": {
                "title": self.player.title,
                "level": player_progress["level"],
                "experience": player_progress["experience"],
                "required_exp": player_progress["required_exp"],
                "cultivation": self.player.cultivation.value,
                "custom_titles": self.player.custom_titles,
                "sect_bonus": self.player.sect_bonus,
                "total_correct": self.player.total_correct,
                "total_attempts": self.player.total_attempts,
                "accuracy": round(self.player.total_correct / self.player.total_attempts * 100, 1) if self.player.total_attempts > 0 else 0,
            },
            "story": story_progress,
            "commands": command_report,
            "achievements": achievement_progress,
            "total_score": int(self.score),
            "streak": self.streak,
        }

    def get_all_commands_info(self) -> List[Dict[str, Any]]:
        """获取所有命令信息

        获取所有Kubernetes命令的详细信息，包括语法、示例、描述等。

        Returns:
            命令信息列表
        """
        if not self.player:
            raise ValueError("玩家未初始化，无法获取命令信息")

        commands_info = []
        for cmd in self.command_manager.commands.values():
            # 确保只有KubectlCommand类型才能访问kubernetes_concept属性
            from .kubernetes_commands import KubectlCommand
            concept = cmd.kubernetes_concept if isinstance(cmd, KubectlCommand) else ''

            commands_info.append({
                "name": cmd.name,
                "category": cmd.category.value,
                "description": cmd.description,
                "syntax": cmd.syntax,
                "example": cmd.example,
                "concept": concept,
                "mastered": cmd.name in self.player.kubectl_commands_mastered,
            })

        # 按分类排序
        commands_info.sort(key=lambda x: x["category"])
        return commands_info

    def get_save_list(self) -> List[Dict[str, Any]]:
        """获取所有存档列表

        Returns:
            List[Dict[str, Any]]: 存档信息列表，包含文件名和玩家基本信息
        """
        save_files = Player.get_save_files()
        save_list = []

        for save_file in save_files:
            # 尝试加载存档信息
            try:
                with open(save_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # 提取基本信息
                    save_info = {
                        "filename": save_file,
                        "player_name": data["name"],
                        "level": data["level"],
                        "sect": data["sect"],
                        "cultivation": data.get("cultivation", "凡人"),
                        "experience": data["experience"]
                    }
                    save_list.append(save_info)
            except Exception as e:
                print(f"读取存档信息失败: {str(e)}")

        return save_list

    def delete_save(self, save_name: str) -> bool:
        """删除指定存档

        Args:
            save_name: 存档文件名

        Returns:
            bool: 删除成功返回True，否则返回False
        """
        return Player.delete_save(save_name)

    def rename_save(self, old_name: str, new_name: str) -> bool:
        """重命名存档

        Args:
            old_name: 原存档文件名
            new_name: 新存档文件名

        Returns:
            bool: 重命名成功返回True，否则返回False
        """
        try:
            # 确保新文件名以.json结尾
            if not new_name.endswith('.json'):
                new_name += '.json'

            # 检查原文件是否存在
            if not os.path.exists(old_name):
                return False

            # 检查新文件名是否已存在
            if os.path.exists(new_name):
                return False

            # 执行重命名
            os.rename(old_name, new_name)
            return True
        except Exception as e:
            print(f"重命名存档失败: {str(e)}")
            return False

    def reset_streak(self) -> None:
        """重置连击

        重置连续正确回答的次数。
        """
        self.streak = 0

    # ==================== 装备系统方法 ====================
    
    def handle_equipment_drop(self, monster_level: int) -> Optional[Equipment]:
        """处理装备掉落
        
        战斗胜利后调用，根据怪物等级生成装备。
        
        Args:
            monster_level: 怪物等级
            
        Returns:
            Optional[Equipment]: 掉落的装备，如果没有掉落则返回None
        """
        if not self.player:
            return None
        
        equipment = self.equipment_manager.generate_drop(
            monster_level=monster_level,
            player_level=self.player.level
        )
        
        if equipment:
            self.player.add_to_inventory(equipment)
        
        return equipment
    
    def get_shop_items(self) -> List[Equipment]:
        """获取商店物品
        
        Returns:
            List[Equipment]: 商店装备列表
        """
        if not self.player:
            return []
        
        return self.equipment_manager.get_shop_equipment(self.player.level)
    
    def buy_equipment(self, equipment: Equipment) -> Dict[str, Any]:
        """购买装备
        
        Args:
            equipment: 要购买的装备
            
        Returns:
            Dict[str, Any]: 购买结果
        """
        if not self.player:
            return {"success": False, "message": "玩家未初始化"}
        
        price = self.equipment_manager.calculate_buy_price(equipment)
        
        # 检查是否买得起（使用经验值作为货币）
        if self.player.experience < price:
            return {
                "success": False, 
                "message": f"经验值不足！需要{price}经验值，当前{self.player.experience}"
            }
        
        # 扣除经验值
        self.player.experience -= price
        # 添加装备到背包
        self.player.add_to_inventory(equipment)
        
        return {
            "success": True,
            "message": f"成功购买 {equipment.display_name}！",
            "equipment": equipment,
            "remaining_exp": self.player.experience
        }
    
    def sell_equipment(self, equipment: Equipment) -> Dict[str, Any]:
        """出售装备
        
        Args:
            equipment: 要出售的装备
            
        Returns:
            Dict[str, Any]: 出售结果
        """
        if not self.player:
            return {"success": False, "message": "玩家未初始化"}
        
        # 检查装备是否在背包中
        if equipment not in self.player.inventory:
            return {"success": False, "message": "该装备不在背包中"}
        
        price = self.equipment_manager.calculate_sell_price(equipment)
        
        # 移除装备
        self.player.remove_from_inventory(equipment)
        # 获得经验值
        self.player.experience += price
        
        return {
            "success": True,
            "message": f"成功出售 {equipment.display_name}，获得{price}经验值！",
            "gained_exp": price,
            "total_exp": self.player.experience
        }
    
    def equip_item(self, equipment: Equipment) -> Dict[str, Any]:
        """装备物品
        
        Args:
            equipment: 要装备的装备
            
        Returns:
            Dict[str, Any]: 装备结果
        """
        if not self.player:
            return {"success": False, "message": "玩家未初始化"}
        
        # 检查装备是否在背包中
        if equipment not in self.player.inventory:
            return {"success": False, "message": "该装备不在背包中"}
        
        # 装备物品
        self.player.equip_item(equipment)
        
        return {
            "success": True,
            "message": f"成功装备 {equipment.display_name}！",
            "equipment": equipment
        }
    
    def unequip_item(self, equipment_type: EquipmentType) -> Dict[str, Any]:
        """卸下装备
        
        Args:
            equipment_type: 装备类型
            
        Returns:
            Dict[str, Any]: 卸下结果
        """
        if not self.player:
            return {"success": False, "message": "玩家未初始化"}
        
        unequipped = self.player.unequip_item(equipment_type)
        
        if unequipped:
            return {
                "success": True,
                "message": f"成功卸下 {unequipped.display_name}！",
                "equipment": unequipped
            }
        
        return {"success": False, "message": "该位置没有装备"}
    
    def upgrade_equipment(self, equipment: Equipment) -> Dict[str, Any]:
        """强化装备
        
        Args:
            equipment: 要强化的装备
            
        Returns:
            Dict[str, Any]: 强化结果
        """
        if not self.player:
            return {"success": False, "message": "玩家未初始化"}
        
        # 检查装备是否属于玩家
        in_inventory = equipment in self.player.inventory
        is_equipped = (
            self.player.equipped_weapon == equipment or
            self.player.equipped_armor == equipment or
            self.player.equipped_accessory == equipment
        )
        
        if not in_inventory and not is_equipped:
            return {"success": False, "message": "该装备不属于你"}
        
        cost = equipment.get_upgrade_cost()
        
        # 检查经验值是否足够
        if self.player.experience < cost:
            return {
                "success": False,
                "message": f"经验值不足！需要{cost}经验值"
            }
        
        # 尝试强化
        if equipment.upgrade():
            self.player.experience -= cost
            return {
                "success": True,
                "message": f"强化成功！{equipment.display_name} 升级到 +{equipment.level - 1}",
                "new_level": equipment.level,
                "remaining_exp": self.player.experience
            }
        else:
            return {
                "success": False,
                "message": "该装备已达到最高强化等级"
            }
    
    def get_equipment_summary(self) -> Dict[str, Any]:
        """获取装备汇总信息
        
        Returns:
            Dict[str, Any]: 装备汇总信息
        """
        if not self.player:
            return {"error": "玩家未初始化"}
        
        return self.player.get_equipment_summary()

    # ==================== 副本和挑战塔方法 ====================
    
    def get_available_dungeons(self) -> List[Dungeon]:
        """获取可用的副本列表"""
        if not self.player or not self.dungeon_manager:
            return []
        return self.dungeon_manager.get_available_dungeons(self.player.level)
    
    def start_dungeon(self, dungeon_id: str) -> Dict[str, Any]:
        """开始副本"""
        if not self.player or not self.dungeon_manager:
            return {"success": False, "message": "副本系统未初始化"}
        
        result = self.dungeon_manager.start_dungeon(dungeon_id, self.player.stamina)
        
        if result["success"]:
            # 扣除体力
            self.player.stamina -= result["stamina_cost"]
        
        return result
    
    def get_tower_level(self, level: int) -> Optional[Dict[str, Any]]:
        """获取挑战塔层信息"""
        tower_level = self.challenge_tower.get_level(level)
        if not tower_level:
            return None
        
        status = self.challenge_tower.get_level_status(level, self.tower_progress) if self.tower_progress else "✗ 未解锁"
        
        return {
            "level": tower_level.level,
            "monster_name": tower_level.monster_name,
            "recommended_cultivation": tower_level.recommended_cultivation,
            "status": status,
            "experience_reward": tower_level.experience_reward,
        }
    
    def start_tower_challenge(self, level: int) -> Dict[str, Any]:
        """开始挑战塔挑战"""
        if not self.player or not self.tower_progress:
            return {"success": False, "message": "挑战塔系统未初始化"}
        
        return self.challenge_tower.start_challenge(level, self.tower_progress)
    
    def complete_tower_level(self) -> Dict[str, Any]:
        """完成挑战塔层"""
        if not self.tower_progress:
            return {"success": False, "message": "挑战塔系统未初始化"}
        
        result = self.challenge_tower.complete_level(self.tower_progress)
        
        if result["success"] and self.player:
            # 给予奖励
            rewards = result["rewards"]
            self.player.gain_experience(rewards["experience"])
            
            # 更新最高挑战塔层数
            current_level = self.tower_progress.get("current_level", 0)
            if current_level > self.player.highest_tower_level:
                self.player.highest_tower_level = current_level
                # 检查挑战塔成就
                self.player.check_tower_achievements(self.player.highest_tower_level)
            
            # 装备掉落
            equipment = self.equipment_manager.generate_equipment(
                player_level=self.player.level,
                quality=self._get_quality_from_level(rewards["equipment_quality"])
            )
            if equipment:
                self.player.add_to_inventory(equipment)
                result["equipment_dropped"] = equipment.to_dict()
        
        return result
    
    def _get_quality_from_level(self, level: int):
        """根据等级获取装备品质"""
        from .equipment import EquipmentQuality
        qualities = [EquipmentQuality.普通, EquipmentQuality.精良, EquipmentQuality.稀有, 
                     EquipmentQuality.史诗, EquipmentQuality.传说]
        return qualities[min(len(qualities) - 1, level - 1)]
    
    def get_tower_ranking(self) -> str:
        """获取挑战塔排名"""
        if not self.tower_progress:
            return "💫 初入塔门"
        return self.challenge_tower.get_ranking(self.tower_progress)

    # ==================== 战斗系统方法 ====================
    def start_combat(self, monster: Any) -> Dict[str, Any]:
        """开始战斗

        Args:
            monster: 要战斗的怪物对象

        Returns:
            战斗初始状态字典
        """
        if not self.player:
            raise ValueError("玩家未初始化，无法开始战斗")

        # 保存怪物原始状态，用于战斗中恢复
        self.current_monster = monster
        self.monster_current_health = monster.health

        return {
            "player_health": self.player.health,
            "monster_health": self.monster_current_health,
            "monster_name": monster.name,
            "monster_description": monster.description,
            "player_attack": self.player.total_attack if hasattr(self.player, 'total_attack') else self.player.attack,
            "player_defense": self.player.total_defense if hasattr(self.player, 'total_defense') else self.player.defense,
            "monster_attack": monster.attack,
            "monster_defense": monster.defense,
            "round": 1,
            "status": "combat_started"
        }

    def player_attack(self, monster: Any, answer_correct: bool) -> Dict[str, Any]:
        """玩家攻击

        Args:
            monster: 要攻击的怪物对象
            answer_correct: 命令回答是否正确

        Returns:
            攻击结果字典
        """
        if not self.player:
            raise ValueError("玩家未初始化，无法进行攻击")

        # 获取基础属性
        player_attack = self.player.total_attack if hasattr(self.player, 'total_attack') else self.player.attack
        player_defense = self.player.total_defense if hasattr(self.player, 'total_defense') else self.player.defense
        
        # 应用天赋加成
        talent_bonuses = self.player.get_talent_bonuses()
        player_attack += int(talent_bonuses.get("attack", 0))
        player_defense += int(talent_bonuses.get("defense", 0))
        
        # 炼狱门：狂暴技能 - 攻击力翻倍
        if hasattr(self.player, 'skill_manager') and self.player.skill_manager:
            if self.player.skill_manager.has_active_effect("liyu_berserk"):
                player_attack *= 2
        
        if answer_correct:
            # 回答正确，攻击力翻倍
            damage = max(1, player_attack * 2 - monster.defense)
            self.streak += 1
            attack_message = "你回答正确！发动了强力攻击！"
        else:
            # 回答错误，攻击力减半
            damage = max(1, player_attack // 2 - monster.defense)
            self.streak = 0
            attack_message = "你回答错误！攻击威力大减！"

        # 对怪物造成伤害
        self.monster_current_health = max(0, self.monster_current_health - damage)

        # 检查怪物是否被击败
        if self.monster_current_health <= 0:
            # 战斗胜利
            return self._handle_combat_victory(monster, damage, attack_message)

        # 怪物反击
        return self._monster_counter_attack(monster, damage, attack_message)

    def _monster_counter_attack(self, monster: Any, player_damage: int, attack_message: str) -> Dict[str, Any]:
        """怪物反击

        Args:
            monster: 怪物对象
            player_damage: 玩家造成的伤害
            attack_message: 玩家攻击的消息

        Returns:
            反击结果字典
        """
        if not self.player:
            raise ValueError("玩家未初始化，无法进行怪物反击")

        # 计算怪物造成的伤害
        player_defense = self.player.total_defense if hasattr(self.player, 'total_defense') else self.player.defense
        
        # 应用天赋防御加成
        talent_bonuses = self.player.get_talent_bonuses()
        player_defense += int(talent_bonuses.get("defense", 0))
        
        monster_damage = max(1, monster.attack - player_defense)
        
        # 应用技能减伤效果
        skill_bonuses = self.player.get_skill_bonuses()
        damage_reduction = skill_bonuses.get("damage_reduction", 0.0)
        if damage_reduction > 0:
            monster_damage = int(monster_damage * (1 - damage_reduction))
        
        # 玄天宗：变化莫测 - 闪避概率
        dodge_chance = skill_bonuses.get("dodge_chance", 0.0)
        if hasattr(self.player, 'skill_manager') and self.player.skill_manager:
            if self.player.skill_manager.has_active_effect("xuantian_dodge"):
                dodge_chance = 0.5  # 50%闪避
        
        import random
        if random.random() < dodge_chance:
            # 闪避成功
            return {
                "player_health": self.player.health,
                "monster_health": self.monster_current_health,
                "damage": player_damage,
                "monster_damage": 0,
                "message": f"{attack_message}\n你对{monster.name}造成了{player_damage}点伤害！\n你成功闪避了{monster.name}的攻击！",
                "status": "combat_ongoing",
                "streak": self.streak,
                "dodged": True
            }

        # 对玩家造成伤害
        self.player.health = max(0, self.player.health - monster_damage)
        
        # 炼狱门：嗜血 - 吸血效果
        lifesteal = skill_bonuses.get("lifesteal", 0.0)
        if lifesteal > 0 and player_damage > 0:
            heal_amount = int(player_damage * lifesteal)
            self.player.health = min(self.player.total_max_health, self.player.health + heal_amount)

        # 检查玩家是否被击败
        if self.player.health <= 0:
            # 炼狱门：不屈 - 复活效果
            if random.random() < 0.3:  # 30%概率复活
                self.player.health = int(self.player.total_max_health * 0.3)
                return {
                    "player_health": self.player.health,
                    "monster_health": self.monster_current_health,
                    "damage": player_damage,
                    "monster_damage": monster_damage,
                    "message": f"{attack_message}\n{monster.name}对你造成了{monster_damage}点伤害！\n[炼狱门·不屈]触发！你以30%生命值复活！",
                    "status": "combat_ongoing",
                    "streak": self.streak,
                    "resurrected": True
                }
            
            # 战斗失败
            # 更新战斗统计
            self.player.total_combats += 1
            self.player.combats_lost += 1
            # 清除当前怪物
            self.current_monster = None
            
            return {
                "player_health": self.player.health,
                "monster_health": self.monster_current_health,
                "damage": player_damage,
                "monster_damage": monster_damage,
                "message": f"{attack_message}\n{monster.name}对你造成了{monster_damage}点伤害！\n你被击败了！",
                "status": "combat_lost",
                "streak": self.streak
            }

        # 战斗继续
        message = f"{attack_message}\n你对{monster.name}造成了{player_damage}点伤害！\n{monster.name}对你造成了{monster_damage}点伤害！"
        if lifesteal > 0 and player_damage > 0:
            heal_amount = int(player_damage * lifesteal)
            message += f"\n[炼狱门·嗜血]你恢复了{heal_amount}点生命！"
        
        return {
            "player_health": self.player.health,
            "monster_health": self.monster_current_health,
            "damage": player_damage,
            "monster_damage": monster_damage,
            "message": message,
            "status": "combat_ongoing",
            "streak": self.streak
        }

    def _handle_combat_victory(self, monster: Any, damage: int, attack_message: str) -> Dict[str, Any]:
        """处理战斗胜利

        Args:
            monster: 被击败的怪物对象
            damage: 最后一击的伤害
            attack_message: 最后一击的消息

        Returns:
            战斗胜利结果字典
        """
        if not self.player:
            raise ValueError("玩家未初始化，无法处理战斗胜利")

        # 战斗胜利，获得经验值
        exp_gained = monster.experience_reward
        self.player.gain_experience(exp_gained)
        
        # 更新战斗统计
        self.player.total_combats += 1
        self.player.combats_won += 1
        
        # 检查战斗成就
        self.player.check_combat_achievements(
            self.player.total_combats, 
            self.player.combats_won
        )
        
        # 装备掉落
        dropped_equipment = self.handle_equipment_drop(monster.level)
        
        # 检查装备成就
        if dropped_equipment:
            has_orange = any(
                eq.quality.value == "传说" 
                for eq in self.player.inventory + [
                    self.player.equipped_weapon,
                    self.player.equipped_armor, 
                    self.player.equipped_accessory
                ] if eq
            )
            self.player.check_equipment_achievements(
                len(self.player.inventory),
                has_orange
            )

        # 清除当前怪物
        self.current_monster = None
        
        # 构建详细的结果消息
        message_lines = [
            attack_message,
            f"你对{monster.name}造成了{damage}点伤害！",
            f"{monster.name}被击败了！",
            f"你获得了{exp_gained}经验值！"
        ]
        
        # 添加装备掉落信息（详细版）
        equipment_info = None
        if dropped_equipment:
            eq = dropped_equipment
            message_lines.append(f"\n🎁 掉落装备：{eq.display_name}")
            
            # 添加装备属性信息
            attr_parts = []
            if eq.total_attack > 0:
                attr_parts.append(f"攻击+{eq.total_attack}")
            if eq.total_defense > 0:
                attr_parts.append(f"防御+{eq.total_defense}")
            if eq.total_health > 0:
                attr_parts.append(f"生命+{eq.total_health}")
            if eq.exp_bonus > 0:
                attr_parts.append(f"经验+{int(eq.exp_bonus*100)}%")
            if eq.streak_bonus > 0:
                attr_parts.append(f"连击+{int(eq.streak_bonus*100)}%")
            
            if attr_parts:
                message_lines.append(f"   属性：{' | '.join(attr_parts)}")
            
            message_lines.append(f"   已自动存入背包！")
            
            equipment_info = {
                "name": eq.name,
                "display_name": eq.display_name,
                "quality": eq.quality.name,
                "type": eq.equipment_type.value,
                "attack": eq.total_attack,
                "defense": eq.total_defense,
                "health": eq.total_health,
                "exp_bonus": eq.exp_bonus,
                "streak_bonus": eq.streak_bonus,
            }

        return {
            "player_health": self.player.health,
            "monster_health": 0,
            "damage": damage,
            "monster_damage": 0,
            "message": "\n".join(message_lines),
            "status": "combat_won",
            "exp_gained": exp_gained,
            "streak": self.streak,
            "dropped_equipment": dropped_equipment.to_dict() if dropped_equipment else None
        }

    def flee_combat(self, monster: Any) -> Dict[str, Any]:
        """逃跑

        Args:
            monster: 要逃跑的怪物对象

        Returns:
            逃跑结果字典
        """
        # 逃跑成功率为50%
        flee_success = random.choice([True, False])

        if flee_success:
            # 逃跑成功
            self.current_monster = None
            return {
                "message": f"你成功逃离了{monster.name}的追击！",
                "status": "flee_success"
            }
        else:
            # 逃跑失败，怪物反击
            if not self.player:
                raise ValueError("玩家未初始化，无法处理逃跑失败")

            # 怪物造成的伤害翻倍
            player_defense = self.player.total_defense if hasattr(self.player, 'total_defense') else self.player.defense
            monster_damage = max(1, monster.attack * 2 - player_defense)
            self.player.health = max(0, self.player.health - monster_damage)

            return {
                "player_health": self.player.health,
                "monster_health": self.monster_current_health,
                "message": f"你逃跑失败！{monster.name}对你造成了{monster_damage}点伤害！",
                "status": "flee_failed",
                "monster_damage": monster_damage
            }

    def get_player(self) -> Optional[Player]:
        """获取当前玩家

        Returns:
            当前玩家对象，如果未初始化则返回None
        """
        return self.player

    def set_state(self, state: GameState) -> None:
        """设置游戏状态

        Args:
            state: 新的游戏状态
        """
        if not isinstance(state, GameState):
            raise ValueError("状态必须是GameState枚举类型")

        self.state = state

    def get_state(self) -> GameState:
        """获取当前游戏状态

        Returns:
            当前游戏状态
        """
        return self.state

    # 纯粹答题模式相关方法
    def start_quiz_mode(self, use_wrong_commands_only: bool = False) -> Dict[str, Any]:
        """开始纯粹答题模式

        Args:
            use_wrong_commands_only: 是否只使用错题集

        Returns:
            答题模式初始状态
        """
        if not self.player:
            raise ValueError("玩家未初始化，无法开始答题模式")

        # 根据参数选择使用的命令列表
        if use_wrong_commands_only and self.player.wrong_commands:
            # 只使用错题集
            available_commands = list(set(self.player.wrong_commands))
            mode_name = "错题集模式"
        else:
            # 使用所有命令
            available_commands = list(self.command_manager.commands.keys())
            mode_name = "全部命令模式"

        return {
            "mode": mode_name,
            "total_commands": len(available_commands),
            "status": "quiz_started"
        }

    def generate_quiz_question(self, use_wrong_commands_only: bool = False) -> Optional[Dict[str, Any]]:
        """生成答题模式的问题

        Args:
            use_wrong_commands_only: 是否只使用错题集

        Returns:
            包含问题、选项、正确答案的字典，或None（如果没有可用命令）
        """
        if not self.player:
            raise ValueError("玩家未初始化，无法生成答题模式问题")

        # 根据参数选择使用的命令列表
        if use_wrong_commands_only and self.player.wrong_commands:
            # 只使用错题集
            available_commands = list(set(self.player.wrong_commands))
        else:
            # 使用所有命令
            available_commands = list(self.command_manager.commands.keys())

        if not available_commands:
            return None

        # 随机选择一个命令
        target_command = random.choice(available_commands)
        cmd_info = self.command_manager.get_command(target_command)

        if not cmd_info:
            return None

        # 生成选项
        all_commands = list(self.command_manager.commands.keys())
        all_commands = [cmd for cmd in all_commands if cmd != target_command]

        # 随机选择3个干扰选项
        num_distractors = 3
        distractors = random.sample(all_commands, num_distractors) if len(all_commands) >= num_distractors else all_commands

        # 构建选项列表并随机排序
        options = [target_command] + distractors
        random.shuffle(options)

        # 找到正确选项的索引
        correct_index = options.index(target_command)

        # 确保只有KubectlCommand类型才能访问kubernetes_concept属性
        from .kubernetes_commands import KubectlCommand
        concept = cmd_info.kubernetes_concept if isinstance(cmd_info, KubectlCommand) else ''

        return {
            "question": f"如何{cmd_info.description}？",
            "options": options,
            "correct_index": correct_index,
            "command_info": {
                "name": cmd_info.name,
                "category": cmd_info.category.value,
                "description": cmd_info.description,
                "syntax": cmd_info.syntax,
                "example": cmd_info.example,
                "concept": concept
            }
        }
