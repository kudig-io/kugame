"""装备套装系统与玩家属性的集成测试"""
# -*- coding: utf-8 -*-

from kugame.equipment import Equipment, EquipmentType, EquipmentQuality
from kugame.game_engine import GameEngine
from kugame.player import Player, Sect


def make_piece(name: str, etype: EquipmentType) -> Equipment:
    """构造零属性套装件，隔离套装加成与装备自身加成"""
    return Equipment(
        id=f"test_{name}",
        name=name,
        equipment_type=etype,
        quality=EquipmentQuality.精良,
    )


class TestSetBonusIntegration:
    """套装加成接入玩家属性"""

    def setup_method(self):
        self.player = Player(name="套装测试侠", sect=Sect.青云宗)

    def test_no_set_bonus_without_equipment(self):
        """无装备时套装加成为零"""
        result = self.player.set_bonuses
        assert result["active_sets"] == []
        assert result["bonuses"]["attack"] == 0

    def test_two_piece_qingyun_defense_bonus(self):
        """青云2件套：防御+10"""
        base_defense = self.player.total_defense
        self.player.equip_item(make_piece("青云剑", EquipmentType.武器))
        self.player.equip_item(make_piece("青云道袍", EquipmentType.护甲))

        assert self.player.total_defense == base_defense + 10
        active = self.player.set_bonuses["active_sets"]
        assert len(active) == 1
        assert active[0]["set_name"] == "青云套装"
        assert active[0]["pieces_equipped"] == 2

    def test_three_piece_qingyun_exp_bonus(self):
        """青云3件套：防御+10 且 经验+10%"""
        exp_bonus_before = self.player.exp_bonus
        self.player.equip_item(make_piece("青云剑", EquipmentType.武器))
        self.player.equip_item(make_piece("青云道袍", EquipmentType.护甲))
        self.player.equip_item(make_piece("青云玉佩", EquipmentType.饰品))

        assert abs(self.player.exp_bonus - (exp_bonus_before + 0.1)) < 1e-9
        assert len(self.player.set_bonuses["active_sets"]) == 1

    def test_novice_set_attack_and_health(self):
        """新手3件套：攻击+5 生命+20"""
        base_attack = self.player.total_attack
        base_health = self.player.total_max_health
        self.player.equip_item(make_piece("新手长剑", EquipmentType.武器))
        self.player.equip_item(make_piece("新手护甲", EquipmentType.护甲))
        self.player.equip_item(make_piece("新手护符", EquipmentType.饰品))

        assert self.player.total_attack == base_attack + 5
        assert self.player.total_max_health == base_health + 20

    def test_mixed_pieces_no_bonus(self):
        """混搭不同套装各1件：无加成"""
        base_attack = self.player.total_attack
        self.player.equip_item(make_piece("青云剑", EquipmentType.武器))
        self.player.equip_item(make_piece("新手护甲", EquipmentType.护甲))

        assert self.player.total_attack == base_attack
        assert self.player.set_bonuses["active_sets"] == []

    def test_unequip_removes_bonus(self):
        """卸下套装件后加成消失"""
        self.player.equip_item(make_piece("青云剑", EquipmentType.武器))
        self.player.equip_item(make_piece("青云道袍", EquipmentType.护甲))
        base_defense_with_set = self.player.total_defense

        self.player.unequip_item(EquipmentType.护甲)
        assert self.player.total_defense == base_defense_with_set - 10
        assert self.player.set_bonuses["active_sets"] == []

    def test_engine_set_collection(self):
        """引擎套装图鉴：反映背包与已装备"""
        engine = GameEngine()
        engine.player = self.player
        self.player.equip_item(make_piece("青云剑", EquipmentType.武器))
        self.player.inventory.append(make_piece("青云道袍", EquipmentType.护甲))

        progress = engine.get_set_collection()
        qingyun = next(p for p in progress if p["set_id"] == "qingyun_set")
        assert qingyun["collected_count"] == 2
        assert "青云玉佩" in qingyun["missing_pieces"]

    def test_engine_set_collection_without_player(self):
        """无玩家时图鉴返回全部套装且收集数为0"""
        engine = GameEngine()
        progress = engine.get_set_collection()
        assert len(progress) == 8
        assert all(p["collected_count"] == 0 for p in progress)
