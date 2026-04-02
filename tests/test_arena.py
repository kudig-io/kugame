"""PVP竞技场系统测试

测试竞技场功能，包括注册、匹配、战斗、排名等。
"""
# -*- coding: utf-8 -*-

import pytest
import os
import sys
import tempfile
import shutil

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from kugame.arena import (
    ArenaSystem, ArenaPlayer, ArenaBattle, ArenaRank,
    SeasonInfo
)


class TestArenaRank:
    """测试段位系统"""
    
    def test_rank_by_rating(self):
        """测试根据积分获取段位"""
        assert ArenaRank.get_rank_by_rating(500) == ArenaRank.青铜
        assert ArenaRank.get_rank_by_rating(1100) == ArenaRank.白银
        assert ArenaRank.get_rank_by_rating(1300) == ArenaRank.黄金
        assert ArenaRank.get_rank_by_rating(1500) == ArenaRank.铂金
        assert ArenaRank.get_rank_by_rating(1700) == ArenaRank.钻石
        assert ArenaRank.get_rank_by_rating(1900) == ArenaRank.大师
        assert ArenaRank.get_rank_by_rating(2100) == ArenaRank.王者
    
    def test_rank_properties(self):
        """测试段位属性"""
        rank = ArenaRank.黄金
        assert rank.level == 3
        assert rank.cn_name == "黄金"
        assert rank.min_rating == 1200
        assert rank.max_rating == 1400


class TestArenaPlayer:
    """测试竞技场玩家"""
    
    def test_player_creation(self):
        """测试玩家创建"""
        player = ArenaPlayer(
            player_id="test_001",
            player_name="TestPlayer",
            level=10,
            rating=1200,
        )
        
        assert player.player_id == "test_001"
        assert player.rating == 1200
        assert player.rank == ArenaRank.黄金
    
    def test_win_rate_calculation(self):
        """测试胜率计算"""
        player = ArenaPlayer(
            player_id="test_001",
            player_name="TestPlayer",
            win_count=7,
            lose_count=3,
        )
        
        assert player.total_battles == 10
        assert player.win_rate == 0.7
    
    def test_update_rating(self):
        """测试积分更新"""
        player = ArenaPlayer(
            player_id="test_001",
            player_name="TestPlayer",
            rating=1000,
            highest_rating=1200,
        )
        
        player.update_rating(100)
        assert player.rating == 1100
        assert player.highest_rating == 1200  # 未超过最高
        
        player.update_rating(200)
        assert player.rating == 1300
        assert player.highest_rating == 1300  # 更新最高


class TestArenaSystem:
    """测试竞技场系统"""
    
    def setup_method(self):
        """每个测试前创建临时目录"""
        self.temp_dir = tempfile.mkdtemp()
        self.arena = ArenaSystem(data_dir=self.temp_dir)
    
    def teardown_method(self):
        """每个测试后清理临时目录"""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_system_initialization(self):
        """测试系统初始化"""
        assert self.arena is not None
        assert self.arena.current_season is not None
    
    def test_register_player(self):
        """测试注册玩家"""
        player = self.arena.register_player({
            "player_id": "p001",
            "player_name": "Player1",
            "level": 20,
            "attack": 50,
            "defense": 30,
            "health": 200,
        })
        
        assert player.player_id == "p001"
        assert player.rating == 1000  # 默认积分
        assert "p001" in self.arena.players
    
    def test_find_match(self):
        """测试寻找对手"""
        # 注册两个玩家
        self.arena.register_player({
            "player_id": "p001",
            "player_name": "Player1",
            "rating": 1200,
        })
        self.arena.register_player({
            "player_id": "p002",
            "player_name": "Player2",
            "rating": 1250,
        })
        
        opponent = self.arena.find_match("p001")
        assert opponent is not None
    
    def test_battle(self):
        """测试战斗"""
        # 注册玩家
        self.arena.register_player({
            "player_id": "p001",
            "player_name": "Player1",
            "attack": 100,
            "defense": 50,
            "health": 300,
        })
        self.arena.register_player({
            "player_id": "p002",
            "player_name": "Player2",
            "attack": 80,
            "defense": 60,
            "health": 250,
        })
        
        # 进行战斗
        result = self.arena.battle("p001", "p002")
        
        assert result["success"] is True
        assert "battle_id" in result
        assert "winner_id" in result
        assert result["attacker"]["id"] == "p001"
        assert result["defender"]["id"] == "p002"
    
    def test_battle_with_ai(self):
        """测试与AI战斗"""
        # 注册玩家
        self.arena.register_player({
            "player_id": "p001",
            "player_name": "Player1",
        })
        
        # 与AI战斗
        result = self.arena.battle("p001", "ai_1234")
        
        assert result["success"] is True
        assert result["defender"]["id"].startswith("ai_")
    
    def test_get_ranking(self):
        """测试获取排名"""
        # 注册多个玩家并进行战斗来改变积分
        for i in range(5):
            self.arena.register_player({
                "player_id": f"p00{i}",
                "player_name": f"Player{i}",
            })
        
        # 修改积分
        self.arena.players["p004"].rating = 1400
        self.arena.players["p003"].rating = 1300
        self.arena.players["p002"].rating = 1200
        
        ranking = self.arena.get_ranking(3)
        
        assert len(ranking) == 3
        assert ranking[0]["rank"] == 1
        assert ranking[0]["player_id"] == "p004"
    
    def test_get_player_info(self):
        """测试获取玩家信息"""
        self.arena.register_player({
            "player_id": "p001",
            "player_name": "Player1",
            "level": 25,
        })
        
        # 直接修改数据
        self.arena.players["p001"].rating = 1350
        self.arena.players["p001"].win_count = 10
        self.arena.players["p001"].lose_count = 5
        
        info = self.arena.get_player_info("p001")
        
        assert info is not None
        assert info["player_id"] == "p001"
        assert info["level"] == 25
        assert info["rating"] == 1350
        assert info["rank"] == "黄金"  # 1350分在黄金段位
        assert info["win_rate"] == pytest.approx(66.7, 0.1)
    
    def test_get_battle_history(self):
        """测试获取战斗历史"""
        # 注册玩家并进行战斗
        self.arena.register_player({
            "player_id": "p001",
            "player_name": "Player1",
        })
        
        for _ in range(3):
            self.arena.battle("p001", "ai_1234")
        
        history = self.arena.get_battle_history("p001", 5)
        
        assert len(history) == 3
    
    def test_season_info(self):
        """测试赛季信息"""
        info = self.arena.get_season_info()
        
        assert "season_id" in info
        assert "season_name" in info
        assert "days_remaining" in info
    
    def test_rating_calculation(self):
        """测试积分计算"""
        # 注册两个积分相近的玩家
        self.arena.register_player({
            "player_id": "p001",
            "player_name": "Player1",
            "rating": 1500,
        })
        self.arena.register_player({
            "player_id": "p002",
            "player_name": "Player2",
            "rating": 1500,
        })
        
        # 记录战斗前积分
        rating_before = self.arena.players["p001"].rating
        
        # 进行多次战斗
        for _ in range(5):
            self.arena.battle("p001", "p002")
        
        # 检查积分变化
        rating_after = self.arena.players["p001"].rating
        assert rating_after != rating_before


class TestSeasonInfo:
    """测试赛季信息"""
    
    def test_season_creation(self):
        """测试赛季创建"""
        season = SeasonInfo(
            season_id="season_202601",
            season_name="第1赛季",
            start_time="2026-01-01T00:00:00",
            end_time="2026-02-01T00:00:00",
        )
        
        assert season.season_id == "season_202601"
        assert season.is_active is True
    
    def test_season_serialization(self):
        """测试赛季序列化"""
        season = SeasonInfo(
            season_id="season_202601",
            season_name="第1赛季",
            start_time="2026-01-01T00:00:00",
            end_time="2026-02-01T00:00:00",
        )
        
        data = season.to_dict()
        restored = SeasonInfo.from_dict(data)
        
        assert restored.season_id == season.season_id
        assert restored.season_name == season.season_name
