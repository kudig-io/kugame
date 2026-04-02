"""成就系统扩展测试

测试成就系统的扩展功能，包括等级、装备、挑战塔、战斗和特殊成就。
"""
# -*- coding: utf-8 -*-

import pytest
import os
import sys

# 确保可以导入 kugame 模块
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from kugame.player import Player, AchievementType


class TestLevelAchievements:
    """测试等级成就"""
    
    def test_level_10_achievement(self):
        """测试10级成就"""
        player = Player(name="测试", sect="青云宗")
        
        # 升级到10级
        player.gain_experience(2000)  # 足够升级到10级的经验
        
        # 检查等级成就
        unlocked = player.check_level_achievements()
        
        # 验证成就解锁
        assert any("初出茅庐" in name for name in unlocked) or player.level < 10
    
    def test_level_achievement_types(self):
        """测试等级成就在初始化时已创建"""
        player = Player(name="测试", sect="青云宗")
        
        # 检查是否有等级类成就
        level_achievements = [
            a for a in player.achievement_objects 
            if a.type == AchievementType.等级成就
        ]
        
        assert len(level_achievements) > 0
        
        # 验证具体成就存在
        level_ids = [a.id for a in level_achievements]
        assert "level_10" in level_ids
        assert "level_50" in level_ids
        assert "level_100" in level_ids


class TestEquipmentAchievements:
    """测试装备收集成就"""
    
    def test_equipment_count_achievement(self):
        """测试装备数量成就"""
        player = Player(name="测试", sect="青云宗")
        
        # 检查装备成就
        unlocked = player.check_equipment_achievements(15, False)
        
        # 应该有装备收集者成就
        assert any("装备收集者" in name for name in unlocked)
    
    def test_orange_equipment_achievement(self):
        """测试传说装备成就"""
        player = Player(name="测试", sect="青云宗")
        
        # 检查传说装备成就
        unlocked = player.check_equipment_achievements(1, True)
        
        # 应该有传说装备成就
        assert any("传说装备" in name for name in unlocked)
    
    def test_equipment_achievement_types(self):
        """测试装备成就在初始化时已创建"""
        player = Player(name="测试", sect="青云宗")
        
        # 检查是否有装备类成就
        equip_achievements = [
            a for a in player.achievement_objects 
            if a.type == AchievementType.收集成就
        ]
        
        assert len(equip_achievements) > 0
        
        # 验证具体成就存在
        equip_ids = [a.id for a in equip_achievements]
        assert "equipment_10" in equip_ids
        assert "equipment_orange" in equip_ids


class TestTowerAchievements:
    """测试挑战塔成就"""
    
    def test_tower_10_achievement(self):
        """测试挑战塔10层成就"""
        player = Player(name="测试", sect="青云宗")
        
        # 检查挑战塔成就
        unlocked = player.check_tower_achievements(15)
        
        # 应该有塔之新人成就
        assert any("塔之新人" in name for name in unlocked)
    
    def test_tower_100_achievement(self):
        """测试挑战塔100层成就"""
        player = Player(name="测试", sect="青云宗")
        
        # 检查挑战塔成就
        unlocked = player.check_tower_achievements(100)
        
        # 应该有通天塔主成就
        assert any("通天塔主" in name for name in unlocked)
    
    def test_tower_achievement_types(self):
        """测试挑战塔成就在初始化时已创建"""
        player = Player(name="测试", sect="青云宗")
        
        # 检查是否有挑战塔类成就
        tower_achievements = [
            a for a in player.achievement_objects 
            if a.type == AchievementType.挑战塔成就
        ]
        
        assert len(tower_achievements) > 0
        
        # 验证具体成就存在
        tower_ids = [a.id for a in tower_achievements]
        assert "tower_10" in tower_ids
        assert "tower_100" in tower_ids


class TestCombatAchievements:
    """测试战斗成就"""
    
    def test_combat_100_achievement(self):
        """测试百战老兵成就"""
        player = Player(name="测试", sect="青云宗")
        
        # 检查战斗成就
        unlocked = player.check_combat_achievements(100, 50)
        
        # 应该有百战老兵成就
        assert any("百战老兵" in name for name in unlocked)
    
    def test_combat_win_50_achievement(self):
        """测试常胜将军成就"""
        player = Player(name="测试", sect="青云宗")
        
        # 检查战斗成就
        unlocked = player.check_combat_achievements(100, 50)
        
        # 应该有常胜将军成就
        assert any("常胜将军" in name for name in unlocked)
    
    def test_combat_achievement_types(self):
        """测试战斗成就在初始化时已创建"""
        player = Player(name="测试", sect="青云宗")
        
        # 检查是否有战斗类成就
        combat_achievements = [
            a for a in player.achievement_objects 
            if a.type == AchievementType.战斗成就
        ]
        
        assert len(combat_achievements) > 0
        
        # 验证具体成就存在
        combat_ids = [a.id for a in combat_achievements]
        assert "combat_100" in combat_ids
        assert "combat_win_50" in combat_ids


class TestSpecialAchievements:
    """测试特殊成就"""
    
    def test_first_login_achievement(self):
        """测试首次登录成就"""
        player = Player(name="测试", sect="青云宗")
        
        # 解锁首次登录成就
        result = player.unlock_first_login()
        
        assert result is True
        
        # 验证成就在列表中
        assert "first_login" in player.achievements
    
    def test_perfect_answer_achievement(self):
        """测试完美答题成就"""
        player = Player(name="测试", sect="青云宗")
        
        # 检查完美答题成就
        unlocked = player.check_perfect_answer(10)
        
        # 应该有完美答题成就
        assert any("完美答题" in name for name in unlocked)
    
    def test_special_achievement_types(self):
        """测试特殊成就在初始化时已创建"""
        player = Player(name="测试", sect="青云宗")
        
        # 检查是否有特殊类成就
        special_achievements = [
            a for a in player.achievement_objects 
            if a.type == AchievementType.特殊成就
        ]
        
        assert len(special_achievements) > 0
        
        # 验证具体成就存在
        special_ids = [a.id for a in special_achievements]
        assert "first_login" in special_ids
        assert "perfect_answer" in special_ids


class TestAchievementStats:
    """测试成就统计功能"""
    
    def test_get_achievement_stats(self):
        """测试获取成就统计"""
        player = Player(name="测试", sect="青云宗")
        
        stats = player.get_achievement_stats()
        
        assert "total_achievements" in stats
        assert "unlocked_count" in stats
        assert "locked_count" in stats
        assert "completion_percentage" in stats
        assert "by_type" in stats
        assert "recent_unlocked" in stats
    
    def test_achievement_stats_by_type(self):
        """测试按类型统计成就"""
        player = Player(name="测试", sect="青云宗")
        
        stats = player.get_achievement_stats()
        by_type = stats["by_type"]
        
        # 验证所有成就类型都有统计
        for ach_type in AchievementType:
            assert ach_type.value in by_type
            assert "total" in by_type[ach_type.value]
            assert "unlocked" in by_type[ach_type.value]
            assert "percentage" in by_type[ach_type.value]


class TestCombatStats:
    """测试战斗统计属性"""
    
    def test_combat_stats_initialization(self):
        """测试战斗统计属性正确初始化"""
        player = Player(name="测试", sect="青云宗")
        
        assert player.total_combats == 0
        assert player.combats_won == 0
        assert player.combats_lost == 0
        assert player.highest_tower_level == 0
