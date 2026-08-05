"""宠物系统与玩家/游戏引擎的集成测试"""
# -*- coding: utf-8 -*-

import pytest

from kugame.game_engine import GameEngine
from kugame.player import Player, Sect
from kugame.pet_system import create_pet


@pytest.fixture
def engine():
    """构造带玩家的引擎"""
    engine = GameEngine()
    engine.player = Player(name="灵兽测试侠", sect=Sect.青云宗)
    return engine


class TestPetIntegration:
    """宠物系统接入游戏引擎"""

    def test_menu_contains_pet(self, engine):
        """主菜单包含灵兽园入口"""
        ids = [opt["id"] for opt in engine.get_menu_options()]
        assert "pet" in ids

    def test_pet_manager_lazy_init(self, engine):
        """宠物管理器懒加载，初始为空"""
        manager = engine.player.pet_manager
        assert manager.pets == []
        assert manager.active_pet_id is None

    def test_summary_and_list_empty(self, engine):
        """无宠物时摘要与列表"""
        summary = engine.pet_summary()
        assert summary["total_pets"] == 0
        assert engine.pet_list() == []

    def test_summary_without_player(self):
        """无玩家时摘要返回None、列表为空"""
        engine = GameEngine()
        assert engine.pet_summary() is None
        assert engine.pet_list() == []

    def test_adopt_pet_consumes_stamina(self, engine):
        """寻访灵兽消耗体力并添加宠物（首只自动出战）"""
        stamina_before = engine.player.stamina
        result = engine.adopt_random_pet()

        assert result["success"] is True
        assert engine.player.stamina == stamina_before - engine.PET_ADOPT_STAMINA_COST
        assert len(engine.player.pet_manager.pets) == 1
        # 首只宠物自动出战
        active = engine.player.pet_manager.get_active_pet()
        assert active is not None
        assert active.id == result["pet"]["id"]

    def test_adopt_fails_without_stamina(self, engine):
        """体力不足时寻访失败"""
        engine.player.stamina = engine.PET_ADOPT_STAMINA_COST - 1
        # 防止时间恢复干扰
        from datetime import datetime
        engine.player.last_stamina_refresh = datetime.now().isoformat()

        result = engine.adopt_random_pet()
        assert result["success"] is False
        assert len(engine.player.pet_manager.pets) == 0

    def test_feed_and_train(self, engine):
        """喂食提升忠诚/心情，训练获得经验"""
        pet = create_pet("spirit_fox", pet_id="pet_test_1")
        engine.player.pet_manager.add_pet(pet)

        feed_result = engine.pet_feed("pet_test_1")
        assert feed_result["success"] is True
        assert pet.loyalty > 50

        train_result = engine.pet_train("pet_test_1", "attack")
        assert train_result["success"] is True
        assert train_result["exp_gain"] > 0

    def test_operations_on_missing_pet(self, engine):
        """操作不存在的宠物返回失败"""
        assert engine.pet_feed("nope")["success"] is False
        assert engine.pet_play("nope")["success"] is False
        assert engine.pet_train("nope", "attack")["success"] is False
        assert engine.pet_set_active("nope")["success"] is False

    def test_set_active_pet(self, engine):
        """切换出战宠物"""
        engine.player.pet_manager.add_pet(create_pet("spirit_fox", pet_id="pet_a"))
        engine.player.pet_manager.add_pet(create_pet("flame_tiger", pet_id="pet_b"))

        result = engine.pet_set_active("pet_b")
        assert result["success"] is True
        assert engine.player.pet_manager.active_pet_id == "pet_b"
        assert engine.player.pet_manager.get_pet("pet_a").is_active is False

    def test_pet_persistence_roundtrip(self, engine, tmp_path):
        """宠物数据随玩家存档往返保持一致"""
        pet = create_pet("steel_turtle", pet_id="pet_save_1")
        engine.player.pet_manager.add_pet(pet)
        pet.gain_exp(50)

        data = engine.player.to_dict()
        assert data["pet_manager_data"]["pets"][0]["id"] == "pet_save_1"

        save_path = str(tmp_path / "pet_save.json")
        assert engine.player.save(save_path) is True
        restored = Player.load(save_path)
        assert restored is not None
        manager = restored.pet_manager
        assert len(manager.pets) == 1
        loaded = manager.get_pet("pet_save_1")
        assert loaded.name == "玄铁龟"
        assert loaded.exp == 50
        assert manager.active_pet_id == "pet_save_1"
