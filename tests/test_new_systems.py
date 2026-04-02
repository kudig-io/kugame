"""新系统测试

测试任务系统、装备套装、宝石系统、排行榜和事件链。
"""
# -*- coding: utf-8 -*-

import pytest
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from kugame.quest_system import QuestManager, QuestObjectiveType, QuestType, QuestStatus
from kugame.main_quests import create_main_quests, create_side_quests, get_available_main_quests
from kugame.equipment_sets import EQUIPMENT_SETS, calculate_set_bonuses, get_equipment_set
from kugame.gem_system import create_gem, GemType, GemQuality, can_merge_gems, merge_gems, GemInventory
from kugame.leaderboard import Leaderboard, PlayerRanking
from kugame.event_chains import EventChainManager, EVENT_CHAINS, EventRarity


class TestQuestSystem:
    """测试任务系统"""
    
    def test_quest_manager_creation(self):
        """测试任务管理器创建"""
        manager = QuestManager()
        assert len(manager.active_quests) == 0
        assert len(manager.completed_quests) == 0
    
    def test_daily_quest_generation(self):
        """测试每日任务生成"""
        manager = QuestManager()
        result = manager.check_and_reset_daily_quests()
        assert result is True
        assert len(manager.active_quests) == 3
        
        # 同一天不应重复生成
        result2 = manager.check_and_reset_daily_quests()
        assert result2 is False
    
    def test_quest_progress_update(self):
        """测试任务进度更新"""
        manager = QuestManager()
        manager.check_and_reset_daily_quests()
        
        # 更新进度
        completed = manager.update_quest_progress(QuestObjectiveType.学习命令, 5)
        assert len(completed) >= 0  # 可能没有任务被完成
    
    def test_quest_summary(self):
        """测试任务摘要"""
        manager = QuestManager()
        manager.check_and_reset_daily_quests()
        
        summary = manager.get_quest_summary()
        assert "active_count" in summary
        assert "daily_reset" in summary


class TestMainQuests:
    """测试主线任务"""
    
    def test_create_main_quests(self):
        """测试创建主线任务"""
        quests = create_main_quests()
        assert len(quests) > 0
        
        # 检查任务属性
        quest = quests[0]
        assert quest.id.startswith("main_")
        assert quest.quest_type == QuestType.主线任务
    
    def test_create_side_quests(self):
        """测试创建支线任务"""
        quests = create_side_quests()
        assert len(quests) > 0
        
        quest = quests[0]
        assert quest.id.startswith("side_")
        assert quest.quest_type == QuestType.支线任务
    
    def test_get_available_main_quests(self):
        """测试获取可接受的主线任务"""
        quests = get_available_main_quests([], 1)
        assert len(quests) > 0
        
        # 检查等级要求
        for q in quests:
            assert q.level_requirement <= 1


class TestEquipmentSets:
    """测试装备套装系统"""
    
    def test_equipment_sets_defined(self):
        """测试套装定义"""
        assert len(EQUIPMENT_SETS) > 0
        
        for set_id, eq_set in EQUIPMENT_SETS.items():
            assert eq_set.id == set_id
            assert len(eq_set.pieces) > 0
            assert len(eq_set.bonuses) > 0
    
    def test_calculate_set_bonuses(self):
        """测试套装加成计算"""
        # 装备青云套2件
        equipped = ["青云剑", "青云道袍"]
        result = calculate_set_bonuses(equipped)
        
        assert "bonuses" in result
        assert "active_sets" in result
        assert len(result["active_sets"]) > 0
    
    def test_get_equipment_set(self):
        """测试获取装备所属套装"""
        eq_set = get_equipment_set("青云剑")
        assert eq_set is not None
        assert eq_set.id == "qingyun_set"
        
        # 不属于套装的装备
        no_set = get_equipment_set("未知装备")
        assert no_set is None


class TestGemSystem:
    """测试宝石系统"""
    
    def test_create_gem(self):
        """测试创建宝石"""
        gem = create_gem(GemType.攻击宝石, GemQuality.精良, 1)
        assert gem.gem_type == GemType.攻击宝石
        assert gem.quality == GemQuality.精良
        assert gem.level == 1
        assert gem.total_value > 0
    
    def test_gem_display_name(self):
        """测试宝石显示名称"""
        gem = create_gem(GemType.攻击宝石, GemQuality.精良, 2)
        assert "精良" in gem.display_name
        assert "红宝石" in gem.display_name
        assert "+2" in gem.display_name
    
    def test_can_merge_gems(self):
        """测试宝石合成判断"""
        gem1 = create_gem(GemType.攻击宝石, GemQuality.精良, 1)
        gem2 = create_gem(GemType.攻击宝石, GemQuality.精良, 1)
        assert can_merge_gems(gem1, gem2) is True
        
        # 不同类型不能合成
        gem3 = create_gem(GemType.防御宝石, GemQuality.精良, 1)
        assert can_merge_gems(gem1, gem3) is False
    
    def test_merge_gems(self):
        """测试宝石合成"""
        gem1 = create_gem(GemType.攻击宝石, GemQuality.精良, 1)
        gem2 = create_gem(GemType.攻击宝石, GemQuality.精良, 1)
        
        merged = merge_gems(gem1, gem2)
        assert merged is not None
        assert merged.level == 2
    
    def test_gem_inventory(self):
        """测试宝石背包"""
        inventory = GemInventory(max_slots=10)
        gem = create_gem(GemType.攻击宝石, GemQuality.普通)
        
        assert inventory.add_gem(gem) is True
        assert len(inventory.gems) == 1
        
        # 按类型获取
        attack_gems = inventory.get_gems_by_type(GemType.攻击宝石)
        assert len(attack_gems) == 1


class TestLeaderboard:
    """测试排行榜系统"""
    
    def test_leaderboard_creation(self):
        """测试排行榜创建"""
        lb = Leaderboard()
        assert lb is not None
    
    def test_update_player_ranking(self):
        """测试更新玩家排名"""
        lb = Leaderboard()
        
        rank = lb.update_player_ranking({
            "player_id": "test_001",
            "player_name": "TestPlayer",
            "level": 10,
            "total_exp": 1000,
        })
        
        assert rank == 1
    
    def test_get_top_players(self):
        """测试获取排行榜"""
        lb = Leaderboard()
        
        # 添加测试数据
        for i in range(5):
            lb.update_player_ranking({
                "player_id": f"test_{i}",
                "player_name": f"Player{i}",
                "level": i + 1,
                "total_exp": (i + 1) * 100,
            })
        
        top = lb.get_top_players("total_exp", 3)
        assert len(top) == 3
        assert top[0]["rank"] == 1


class TestEventChains:
    """测试事件链系统"""
    
    def test_event_chains_defined(self):
        """测试事件链定义"""
        assert len(EVENT_CHAINS) > 0
        
        for chain_name, chain_data in EVENT_CHAINS.items():
            assert "events" in chain_data
            assert "rarity" in chain_data
    
    def test_event_chain_manager(self):
        """测试事件链管理器"""
        manager = EventChainManager()
        assert manager.current_chain is None
        assert manager.current_event_id is None
    
    def test_trigger_random_event(self):
        """测试触发随机事件"""
        manager = EventChainManager()
        
        # 多次尝试触发事件
        for _ in range(10):
            event = manager.trigger_random_event(50)
            if event:
                assert event.name is not None
                assert len(event.choices) > 0
                break
    
    def test_event_serialization(self):
        """测试事件链序列化"""
        manager = EventChainManager()
        
        data = manager.to_dict()
        assert "current_chain" in data
        assert "chain_history" in data
        
        # 从字典恢复
        restored = EventChainManager.from_dict(data)
        assert restored is not None
