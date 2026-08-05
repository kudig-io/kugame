"""事件链系统与玩家/游戏引擎的集成测试"""
# -*- coding: utf-8 -*-

import pytest

from kugame.game_engine import GameEngine
from kugame.player import Player, Sect


@pytest.fixture
def engine():
    """构造带玩家的引擎"""
    engine = GameEngine()
    engine.player = Player(name="奇遇测试侠", sect=Sect.青云宗)
    return engine


@pytest.fixture
def always_success(monkeypatch):
    """让事件选择必定成功（success_rate 判定通过）"""
    monkeypatch.setattr("kugame.event_chains.random.random", lambda: 0.0)


class TestEventChainIntegration:
    """事件链系统接入游戏引擎"""

    def test_menu_contains_event(self, engine):
        """主菜单包含奇遇探险入口"""
        ids = [opt["id"] for opt in engine.get_menu_options()]
        assert "event" in ids

    def test_available_chains(self, engine):
        """列出全部事件链"""
        chains = engine.available_chains()
        names = [c["name"] for c in chains]
        assert "炼丹奇遇" in names
        assert "古墓探险" in names
        assert "仙人指点" in names

    def test_status_without_player_and_idle(self):
        """无玩家返回None；无进行中事件返回None"""
        assert GameEngine().event_status() is None
        engine = GameEngine()
        engine.player = Player(name="闲人", sect=Sect.青云宗)
        assert engine.event_status() is None

    def test_start_chain_returns_start_event(self, engine):
        """手动开启事件链返回起始事件及选项"""
        event = engine.event_start_chain("炼丹奇遇")
        assert event is not None
        assert event["id"] == "alchemy_start"
        assert len(event["choices"]) == 3

    def test_start_invalid_chain(self, engine):
        """开启不存在的事件链返回None"""
        assert engine.event_start_chain("不存在的链") is None

    def test_choice_no_effect_ends_chain(self, engine, always_success):
        """选择无效果选项后事件链结束"""
        engine.event_start_chain("炼丹奇遇")
        result = engine.event_choose("refuse")

        assert result["success"] is True
        assert result["chain_continues"] is False
        # 事件链已结束
        assert engine.event_status() is None

    def test_exp_reward_and_chain_continue(self, engine, always_success):
        """经验奖励发放且事件链推进到下一环"""
        exp_before = engine.player.experience
        engine.event_start_chain("炼丹奇遇")

        result = engine.event_choose("help_carefully")
        assert result["success"] is True
        assert result["rewards"]["exp"] == 200
        assert result["chain_continues"] is True
        assert engine.player.experience > exp_before

        # 推进到炼丹师的馈赠
        next_event = engine.event_status()
        assert next_event["id"] == "alchemy_success"

    def test_equipment_reward(self, engine, always_success):
        """装备奖励进入背包"""
        engine.event_start_chain("炼丹奇遇")
        engine.event_choose("help_carefully")  # -> alchemy_success

        inventory_before = len(engine.player.inventory)
        result = engine.event_choose("ask_for_reward")

        assert result["success"] is True
        assert "equipment" in result["rewards"]
        assert len(engine.player.inventory) == inventory_before + 1

    def test_gem_reward(self, engine, always_success):
        """宝石奖励进入宝石背包"""
        engine.event_start_chain("炼丹奇遇")
        engine.event_choose("add_ingredient")  # -> alchemy_mystery

        result = engine.event_choose("share_with_master")
        assert result["success"] is True
        assert "gem" in result["rewards"]
        assert len(engine.player.gem_inventory.gems) == 1

    def test_choose_without_event_fails(self, engine):
        """无进行中事件时选择失败"""
        result = engine.event_choose("any")
        assert result["success"] is False

    def test_event_progress_persistence(self, engine, tmp_path, always_success):
        """事件链进度随存档往返保持"""
        engine.event_start_chain("炼丹奇遇")
        engine.event_choose("help_carefully")  # 推进到 alchemy_success

        save_path = str(tmp_path / "event_save.json")
        assert engine.player.save(save_path) is True
        restored = Player.load(save_path)
        assert restored is not None
        assert restored.event_manager.current_chain == "炼丹奇遇"
        assert restored.event_manager.current_event_id == "alchemy_success"
