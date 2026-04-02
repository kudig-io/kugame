"""每日签到系统测试

测试每日签到功能的各项功能。
"""
# -*- coding: utf-8 -*-

import pytest
import os
import sys
from datetime import datetime, timedelta

# 确保可以导入 kugame 模块
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from kugame.daily_checkin import DailyCheckin, DAILY_REWARDS
from kugame.player import Player


class TestDailyCheckin:
    """测试每日签到系统"""
    
    def test_initial_checkin_status(self):
        """测试初始签到状态"""
        checkin = DailyCheckin()
        
        assert checkin.consecutive_days == 0
        assert checkin.total_checkins == 0
        assert checkin.last_checkin_date is None
        assert checkin.can_checkin() is True
    
    def test_first_checkin(self):
        """测试首次签到"""
        checkin = DailyCheckin()
        result = checkin.checkin()
        
        assert result["success"] is True
        assert result["consecutive_days"] == 1
        assert result["total_checkins"] == 1
        assert "experience" in result["rewards"]
        assert "stamina" in result["rewards"]
        assert checkin.can_checkin() is False
    
    def test_duplicate_checkin_same_day(self):
        """测试同一天重复签到"""
        checkin = DailyCheckin()
        checkin.checkin()
        
        # 尝试再次签到
        result = checkin.checkin()
        assert result["success"] is False
    
    def test_consecutive_checkin(self):
        """测试连续签到"""
        checkin = DailyCheckin()
        
        # 第一次签到
        checkin.checkin()
        assert checkin.consecutive_days == 1
        
        # 模拟第二天
        yesterday = (datetime.now() - timedelta(days=1)).isoformat()
        checkin.last_checkin_date = yesterday
        
        result = checkin.checkin()
        assert result["success"] is True
        assert result["consecutive_days"] == 2
    
    def test_broken_streak(self):
        """测试断签重置"""
        checkin = DailyCheckin()
        checkin.consecutive_days = 5
        
        # 模拟两天前签到
        two_days_ago = (datetime.now() - timedelta(days=2)).isoformat()
        checkin.last_checkin_date = two_days_ago
        
        result = checkin.checkin()
        assert result["success"] is True
        assert result["consecutive_days"] == 1  # 重置为1
    
    def test_get_checkin_status(self):
        """测试获取签到状态"""
        checkin = DailyCheckin()
        
        status = checkin.get_checkin_status()
        assert status["can_checkin"] is True
        assert status["consecutive_days"] == 0
        assert "next_reward" in status
        assert "weekly_progress" in status
    
    def test_monthly_reward_status(self):
        """测试月度奖励状态"""
        checkin = DailyCheckin()
        checkin.monthly_checkins = 10
        
        status = checkin.get_monthly_reward_status()
        assert status["monthly_checkins"] == 10
        assert "milestones" in status
        assert len(status["milestones"]) == 4
    
    def test_to_dict_and_from_dict(self):
        """测试数据序列化和反序列化"""
        checkin = DailyCheckin()
        checkin.checkin()
        
        data = checkin.to_dict()
        assert "last_checkin_date" in data
        assert data["consecutive_days"] == 1
        
        # 从字典恢复
        restored = DailyCheckin.from_dict(data)
        assert restored.consecutive_days == 1
        assert restored.can_checkin() is False


class TestPlayerCheckin:
    """测试玩家签到集成"""
    
    def test_player_has_checkin_data(self):
        """测试玩家有签到数据"""
        player = Player(name="测试", sect="青云宗")
        
        assert player.checkin_data is not None
        assert "last_checkin_date" in player.checkin_data
    
    def test_player_checkin(self):
        """测试玩家执行签到"""
        player = Player(name="测试", sect="青云宗")
        initial_exp = player.experience
        
        result = player.checkin()
        
        assert result["success"] is True
        assert player.experience >= initial_exp
    
    def test_player_checkin_status(self):
        """测试玩家获取签到状态"""
        player = Player(name="测试", sect="青云宗")
        
        status = player.get_checkin_status()
        assert status["can_checkin"] is True
        assert "next_reward" in status
    
    def test_player_monthly_status(self):
        """测试玩家月度签到状态"""
        player = Player(name="测试", sect="青云宗")
        
        status = player.get_monthly_checkin_status()
        assert "monthly_checkins" in status
        assert "milestones" in status


class TestDailyRewards:
    """测试每日奖励配置"""
    
    def test_daily_rewards_length(self):
        """测试奖励配置数量"""
        assert len(DAILY_REWARDS) == 7
    
    def test_daily_rewards_increasing(self):
        """测试奖励递增"""
        for i in range(1, len(DAILY_REWARDS)):
            assert DAILY_REWARDS[i].experience >= DAILY_REWARDS[i-1].experience
