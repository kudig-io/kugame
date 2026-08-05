"""测试题库与游戏引擎集成

测试题库加载、出题、判题、错题本闭环以及复活技能门派检查。
"""

import pytest

from kugame.game_engine import GameEngine
from kugame.player import Player, Sect
from kugame.question_bank import Question, QuestionType


@pytest.fixture
def engine():
    """创建带玩家的引擎（不写入工作区存档）"""
    e = GameEngine()
    e.player = Player(name="集成测试", sect=Sect.青云宗)
    return e


class FakeChallenge:
    """check_answer 所需的最小挑战桩对象"""

    def __init__(self, expected="kubectl get pods"):
        self.challenge_id = "test_challenge"
        self.options = [expected, "kubectl delete pods", "kubectl top pods"]
        self.correct_option_index = 0
        self.expected_command = expected
        self.reward_exp = 50
        self.hint = "提示"


class FakeMonster:
    """战斗测试用怪物桩对象"""

    name = "测试妖兽"
    attack = 9999


class TestQuestionBankLoading:
    """测试题库加载"""

    def test_bank_loaded(self, engine):
        """测试引擎启动时加载完整题库"""
        stats = engine.get_question_bank_stats()
        assert stats["total_questions"] >= 300

    def test_chapter_category_map_covers_chapters(self, engine):
        """测试章节分类映射存在且非空"""
        assert "prologue" in engine.CHAPTER_CATEGORY_MAP
        assert "chapter_1" in engine.CHAPTER_CATEGORY_MAP


class TestBankQuestionGeneration:
    """测试题库出题"""

    def test_generate_question(self, engine):
        """测试按当前章节出题"""
        question = engine.generate_bank_question()
        assert question is not None
        assert isinstance(question, Question)

    def test_wrong_only_empty_returns_none(self, engine):
        """测试错题本为空时错题模式返回None"""
        assert engine.generate_bank_question(use_wrong_only=True) is None

    def test_wrong_only_draws_from_wrong_book(self, engine):
        """测试错题模式只从错题本中出题"""
        question = engine.generate_bank_question()
        engine.player.wrong_question_ids = [question.id]

        drawn = engine.generate_bank_question(use_wrong_only=True)
        assert drawn is not None
        assert drawn.id == question.id


class TestBankAnswerChecking:
    """测试题库判题与错题闭环"""

    def _correct_answer_for(self, question):
        """构造题目的正确答案输入"""
        if question.type == QuestionType.多选题:
            return list(question.correct_answer)
        return question.correct_answer

    def test_correct_answer_gains_exp(self, engine):
        """测试答对获得经验且带解析"""
        question = engine.generate_bank_question()
        result = engine.check_bank_answer(question, self._correct_answer_for(question))

        assert result["correct"] is True
        assert result["exp_gained"] == question.difficulty.level * 20
        assert "explanation" in result

    def test_wrong_answer_enters_wrong_book(self, engine):
        """测试答错进入错题本并重置复习进度"""
        question = engine.generate_bank_question()
        result = engine.check_bank_answer(question, "绝对错误的答案XYZ")

        assert result["correct"] is False
        assert question.id in engine.player.wrong_question_ids
        assert engine.player.wrong_review_progress[question.id] == 0

    def test_two_corrects_remove_from_wrong_book(self, engine):
        """测试连续答对2次才移出错题本"""
        question = engine.generate_bank_question()
        correct = self._correct_answer_for(question)

        engine.check_bank_answer(question, "绝对错误的答案XYZ")
        engine.check_bank_answer(question, correct)
        # 第1次答对：仍在错题本，进度为1
        assert question.id in engine.player.wrong_question_ids
        assert engine.player.wrong_review_progress[question.id] == 1

        engine.check_bank_answer(question, correct)
        # 第2次答对：移出错题本
        assert question.id not in engine.player.wrong_question_ids
        assert question.id not in engine.player.wrong_review_progress


class TestChallengeWrongCommandRecording:
    """测试章节挑战错题记录修复"""

    def test_wrong_answer_records_expected_command(self, engine):
        """测试答错记录的是目标命令而非选错的选项"""
        challenge = FakeChallenge(expected="kubectl get pods")
        engine.current_challenge = challenge

        result = engine.check_answer(2)  # 选择错误选项

        assert result["correct"] is False
        assert "kubectl get pods" in engine.player.wrong_commands
        assert "kubectl delete pods" not in engine.player.wrong_commands

    def test_wrong_command_not_duplicated(self, engine):
        """测试重复答错不产生重复错题记录"""
        engine.current_challenge = FakeChallenge()
        engine.check_answer(2)
        engine.current_challenge = FakeChallenge()
        engine.check_answer(2)

        assert engine.player.wrong_commands.count("kubectl get pods") == 1


class TestResurrectSectCheck:
    """测试复活技能门派检查修复"""

    def test_non_liyu_sect_cannot_resurrect(self, engine, monkeypatch):
        """测试非炼狱门玩家死亡不触发复活"""
        import kugame.game_engine as ge
        monkeypatch.setattr(ge.random, "random", lambda: 0.0)

        engine.player.health = 1
        result = engine._monster_counter_attack(FakeMonster(), 10, "攻击")

        assert result["status"] == "combat_lost"
        assert not result.get("resurrected")

    def test_liyu_sect_with_skill_can_resurrect(self, monkeypatch):
        """测试炼狱门持有不屈技能可触发复活"""
        import kugame.game_engine as ge
        monkeypatch.setattr(ge.random, "random", lambda: 0.0)

        e = GameEngine()
        e.player = Player(name="炼狱试炼", sect=Sect.炼狱门)
        assert "liyu_resurrect" in e.player.skill_manager.skills

        e.player.health = 1
        # 玩家伤害为0，避免炼狱门嗜血吸血干扰死亡判定
        result = e._monster_counter_attack(FakeMonster(), 0, "攻击")

        assert result.get("resurrected") is True
        assert e.player.health > 0
