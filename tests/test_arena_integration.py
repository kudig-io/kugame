"""竞技场系统与游戏引擎的集成测试"""
# -*- coding: utf-8 -*-

import pytest

from kugame.game_engine import GameEngine
from kugame.player import Player, Sect


@pytest.fixture
def engine(tmp_path):
    """构造带隔离竞技场数据目录的引擎与玩家"""
    engine = GameEngine()
    engine.arena_data_dir = str(tmp_path)
    engine.player = Player(name="竞技测试侠", sect=Sect.青云宗)
    return engine


class TestArenaIntegration:
    """竞技场接入游戏引擎"""

    def test_menu_contains_arena(self, engine):
        """主菜单包含竞技场入口"""
        ids = [opt["id"] for opt in engine.get_menu_options()]
        assert "arena" in ids

    def test_arena_lazy_init(self, engine, tmp_path):
        """竞技场系统懒加载且数据文件写入隔离目录"""
        assert engine.arena_system is None
        engine.arena_sync_player()
        assert engine.arena_system is not None
        assert (tmp_path / "arena_data.json").exists()

    def test_sync_player_registers(self, engine):
        """同步玩家属性到竞技场"""
        info = engine.arena_sync_player()
        assert info is not None
        assert info["player_name"] == "竞技测试侠"
        assert info["rating"] == 1000
        assert info["win_count"] == 0

    def test_sync_without_player(self, tmp_path):
        """无玩家时同步返回None"""
        engine = GameEngine()
        engine.arena_data_dir = str(tmp_path)
        assert engine.arena_sync_player() is None

    def test_challenge_full_flow(self, engine):
        """匹配挑战完整流程：战斗结算+经验奖励+历史记录"""
        exp_before = engine.player.experience
        level_before = engine.player.level
        result = engine.arena_challenge()

        assert result["success"] is True
        assert result["exp_reward"] > 0
        # 经验已发放（升级会重置经验，两种情况都算发放成功）
        assert (engine.player.experience > exp_before
                or engine.player.level > level_before)

        # 战斗历史有记录
        history = engine.arena_battle_history()
        assert len(history) == 1

    def test_challenge_without_player(self, tmp_path):
        """无玩家时挑战失败"""
        engine = GameEngine()
        engine.arena_data_dir = str(tmp_path)
        result = engine.arena_challenge()
        assert result["success"] is False

    def test_ranking_contains_player(self, engine):
        """排行榜包含已注册玩家"""
        engine.arena_sync_player()
        ranking = engine.arena_ranking()
        names = [r["player_name"] for r in ranking]
        assert "竞技测试侠" in names

    def test_season_info(self, engine):
        """赛季信息可用"""
        season = engine.arena_season_info()
        assert "season_name" in season
        assert season["is_active"] is True

    def test_rating_persists_across_engines(self, engine, tmp_path):
        """竞技场数据跨引擎实例持久化"""
        engine.arena_challenge()
        rating = engine.arena_sync_player()["rating"]

        engine2 = GameEngine()
        engine2.arena_data_dir = str(tmp_path)
        engine2.player = Player(name="竞技测试侠", sect=Sect.青云宗)
        info = engine2.arena_sync_player()
        assert info["rating"] == rating
        assert info["win_count"] + info["lose_count"] == 1
