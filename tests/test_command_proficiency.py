"""命令掌握度三态模型（learning/familiar/mastered）测试"""
# -*- coding: utf-8 -*-

import pytest

from kugame.game_engine import GameEngine
from kugame.player import Player, Sect


@pytest.fixture
def player():
    return Player(name="掌握度测试侠", sect=Sect.青云宗)


class TestCommandProficiency:
    """Player 掌握度三态模型"""

    def test_first_success_to_familiar(self, player):
        """首次答对进入熟悉"""
        assert player.record_command_attempt("kubectl get pods", True) == "familiar"
        assert player.get_command_proficiency("kubectl get pods") == "familiar"

    def test_first_failure_to_learning(self, player):
        """首次答错进入学习中"""
        assert player.record_command_attempt("kubectl run", False) == "learning"

    def test_learning_success_to_familiar(self, player):
        """学习中答对升为熟悉"""
        player.record_command_attempt("kubectl run", False)
        assert player.record_command_attempt("kubectl run", True) == "familiar"

    def test_familiar_success_to_mastered(self, player):
        """熟悉后答对升为掌握并写入掌握列表"""
        player.record_command_attempt("kubectl run", True)   # familiar
        assert player.record_command_attempt("kubectl run", True) == "mastered"
        assert "kubectl run" in player.kubectl_commands_mastered
        assert player.has_mastered_command("kubectl run")

    def test_familiar_failure_demotes_to_learning(self, player):
        """熟悉后答错生疏降级为学习中"""
        player.record_command_attempt("kubectl run", True)   # familiar
        assert player.record_command_attempt("kubectl run", False) == "learning"
        assert "kubectl run" not in player.kubectl_commands_mastered

    def test_mastered_protected_from_failure(self, player):
        """已掌握命令答错不降级"""
        player.record_command_attempt("kubectl run", True)
        player.record_command_attempt("kubectl run", True)   # mastered
        assert player.record_command_attempt("kubectl run", False) == "mastered"
        assert "kubectl run" in player.kubectl_commands_mastered

    def test_learn_command_sets_mastered(self, player):
        """learn_command 直接置为掌握（兼容旧路径）"""
        player.learn_command("kubectl apply")
        assert player.get_command_proficiency("kubectl apply") == "mastered"

    def test_proficiency_summary(self, player):
        """掌握度统计"""
        player.record_command_attempt("c1", False)          # learning
        player.record_command_attempt("c2", True)           # familiar
        player.record_command_attempt("c3", True)
        player.record_command_attempt("c3", True)           # mastered

        summary = player.get_proficiency_summary()
        assert summary == {"learning": 1, "familiar": 1, "mastered": 1}

    def test_invalid_command_raises(self, player):
        """非法命令抛异常"""
        with pytest.raises(ValueError):
            player.record_command_attempt("", True)

    def test_proficiency_persistence(self, player, tmp_path):
        """掌握度随存档往返保持"""
        player.record_command_attempt("kubectl run", True)
        save_path = str(tmp_path / "prof_save.json")
        assert player.save(save_path) is True

        loaded = Player.load(save_path)
        assert loaded is not None
        assert loaded.get_command_proficiency("kubectl run") == "familiar"


class TestProficiencyEngineIntegration:
    """掌握度模型与引擎集成"""

    def test_commands_info_has_proficiency(self):
        """命令信息包含掌握度字段"""
        engine = GameEngine()
        engine.player = Player(name="侠", sect=Sect.青云宗)
        engine.player.record_command_attempt("kubectl get pods", True)

        info = engine.get_all_commands_info()
        target = next((c for c in info if c["name"] == "kubectl get pods"), None)
        assert target is not None
        assert target["proficiency"] == "familiar"

    def test_progress_has_proficiency_summary(self):
        """进度包含掌握度统计"""
        engine = GameEngine()
        engine.player = Player(name="侠", sect=Sect.青云宗)
        engine.player.record_command_attempt("kubectl run", False)

        progress = engine.get_progress()
        assert "proficiency_summary" in progress
        assert progress["proficiency_summary"]["learning"] == 1
