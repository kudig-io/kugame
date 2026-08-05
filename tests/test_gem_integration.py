"""宝石系统与玩家/游戏引擎的集成测试"""
# -*- coding: utf-8 -*-

import pytest

from kugame.game_engine import GameEngine
from kugame.player import Player, Sect
from kugame.gem_system import create_gem, GemType, GemQuality


@pytest.fixture
def engine():
    """构造带玩家的引擎"""
    engine = GameEngine()
    engine.player = Player(name="宝石测试侠", sect=Sect.青云宗)
    return engine


class TestGemIntegration:
    """宝石系统接入游戏引擎"""

    def test_menu_contains_gem(self, engine):
        """主菜单包含宝石阁入口"""
        ids = [opt["id"] for opt in engine.get_menu_options()]
        assert "gem" in ids

    def test_overview_without_player(self):
        """无玩家时概览返回None"""
        engine = GameEngine()
        assert engine.gem_overview() is None

    def test_default_slots_and_empty_inventory(self, engine):
        """默认4个槽位、背包为空、无加成"""
        overview = engine.gem_overview()
        assert len(overview["slots"]) == 4
        assert overview["gems"] == []
        # 等级1时仅槽1解锁
        unlocked = [s for s in overview["slots"] if not s["is_locked"]]
        assert [s["slot_id"] for s in unlocked] == [1]
        assert all(v == 0 for v in overview["bonuses"].values())

    def test_mine_gem_consumes_stamina(self, engine):
        """采矿消耗体力并入库"""
        stamina_before = engine.player.stamina
        result = engine.mine_gem()

        assert result["success"] is True
        assert engine.player.stamina == stamina_before - engine.GEM_MINE_STAMINA_COST
        assert len(engine.player.gem_inventory.gems) == 1

    def test_mine_fails_without_stamina(self, engine):
        """体力不足时采矿失败"""
        from datetime import datetime
        engine.player.stamina = engine.GEM_MINE_STAMINA_COST - 1
        engine.player.last_stamina_refresh = datetime.now().isoformat()

        result = engine.mine_gem()
        assert result["success"] is False
        assert len(engine.player.gem_inventory.gems) == 0

    def test_socket_gem_boosts_attack(self, engine):
        """镶嵌攻击宝石提升总攻击力"""
        gem = create_gem(GemType.攻击宝石, GemQuality.普通, level=1)
        engine.player.gem_inventory.add_gem(gem)
        base_attack = engine.player.total_attack

        result = engine.socket_gem(gem.id, 1)
        assert result["success"] is True
        # 普通攻击宝石 base 5 * 1.0 * 1.0 = 5
        assert engine.player.total_attack == base_attack + 5
        # 背包中该宝石已移除
        assert engine.player.gem_inventory.get_gems_by_type(GemType.攻击宝石) == []

    def test_socket_locked_slot_fails(self, engine):
        """向未解锁槽位镶嵌失败"""
        gem = create_gem(GemType.防御宝石, GemQuality.普通)
        engine.player.gem_inventory.add_gem(gem)

        result = engine.socket_gem(gem.id, 2)  # 槽2需等级10
        assert result["success"] is False
        assert "解锁" in result["message"]

    def test_socket_replaces_existing_gem(self, engine):
        """槽位已有宝石时替换并退回背包"""
        gem1 = create_gem(GemType.攻击宝石, GemQuality.普通)
        gem2 = create_gem(GemType.生命宝石, GemQuality.普通)
        engine.player.gem_inventory.add_gem(gem1)
        engine.player.gem_inventory.add_gem(gem2)

        engine.socket_gem(gem1.id, 1)
        result = engine.socket_gem(gem2.id, 1)

        assert result["success"] is True
        # gem1 退回背包
        ids = [g.id for g in engine.player.gem_inventory.gems]
        assert gem1.id in ids
        assert gem2.id not in ids

    def test_unsocket_gem(self, engine):
        """卸下宝石回背包"""
        gem = create_gem(GemType.攻击宝石, GemQuality.普通)
        engine.player.gem_inventory.add_gem(gem)
        engine.socket_gem(gem.id, 1)

        result = engine.unsocket_gem(1)
        assert result["success"] is True
        assert engine.player.gem_slots[0].is_empty
        assert any(g.id == gem.id for g in engine.player.gem_inventory.gems)

    def test_merge_same_gems(self, engine):
        """合成同类型同品质同等级宝石升级"""
        gem1 = create_gem(GemType.攻击宝石, GemQuality.普通, level=1)
        gem2 = create_gem(GemType.攻击宝石, GemQuality.普通, level=1)
        engine.player.gem_inventory.add_gem(gem1)
        engine.player.gem_inventory.add_gem(gem2)

        result = engine.merge_inventory_gems(gem1.id, gem2.id)
        assert result["success"] is True
        assert len(engine.player.gem_inventory.gems) == 1
        merged = engine.player.gem_inventory.gems[0]
        assert merged.level == 2

    def test_merge_different_gems_fails(self, engine):
        """不同类型宝石无法合成"""
        gem1 = create_gem(GemType.攻击宝石, GemQuality.普通)
        gem2 = create_gem(GemType.防御宝石, GemQuality.普通)
        engine.player.gem_inventory.add_gem(gem1)
        engine.player.gem_inventory.add_gem(gem2)

        result = engine.merge_inventory_gems(gem1.id, gem2.id)
        assert result["success"] is False
        assert len(engine.player.gem_inventory.gems) == 2

    def test_gem_persistence_roundtrip(self, engine, tmp_path):
        """宝石数据随玩家存档往返保持一致"""
        gem = create_gem(GemType.经验宝石, GemQuality.稀有, level=2)
        engine.player.gem_inventory.add_gem(gem)
        engine.socket_gem(gem.id, 1)

        save_path = str(tmp_path / "gem_save.json")
        assert engine.player.save(save_path) is True
        restored = Player.load(save_path)
        assert restored is not None

        # 槽位中的宝石被恢复
        slot1 = restored.gem_slots[0]
        assert slot1.equipped_gem is not None
        assert slot1.equipped_gem.gem_type == GemType.经验宝石
        assert slot1.equipped_gem.level == 2
        # 加成生效
        assert restored.gem_bonuses["exp"] > 0
