"""测试游戏引擎

测试GameEngine类的所有功能。
"""


import os
from kugame.game_engine import GameEngine, GameState
from kugame.player import Player, Sect


class TestGameEngine:
    """测试GameEngine类"""

    def setup_method(self):
        """测试初始化"""
        self.engine = GameEngine()
        self.player = Player(name="测试侠客", sect=Sect.青云宗)

    def test_initial_state(self):
        """测试初始状态"""
        assert self.engine.state == GameState.MENU
        assert self.engine.player is None

    def test_initialize_player(self):
        """测试初始化玩家"""
        player = self.engine.initialize_player("新侠客", Sect.玄天宗)

        assert player is not None
        assert player.name == "新侠客"
        assert player.sect == Sect.玄天宗
        assert self.engine.player is not None

    def test_load_player(self):
        """测试加载玩家"""
        test_player = Player(name="存档侠客", sect=Sect.青云宗)
        test_player.save("test_load.json")

        self.engine.player = None
        result = self.engine.load_player("test_load.json")

        assert result is not None
        assert result.name == "存档侠客"

        if os.path.exists("test_load.json"):
            os.remove("test_load.json")

    def test_load_nonexistent_player(self):
        """测试加载不存在的玩家存档"""
        self.engine.player = None
        os.rename("player_save.json", "player_save.json.bak") if os.path.exists("player_save.json") else None

        result = self.engine.load_player()

        assert result is None

        if os.path.exists("player_save.json.bak"):
            os.rename("player_save.json.bak", "player_save.json")

    def test_get_menu_options(self):
        """测试获取菜单选项"""
        options = self.engine.get_menu_options()

        assert len(options) == 14  # 更新：添加了签到、装备、商店、副本、帮助菜单
        option_ids = [opt["id"] for opt in options]
        assert "story" in option_ids
        assert "practice" in option_ids
        assert "challenge" in option_ids
        assert "progress" in option_ids
        assert "save_manager" in option_ids

    def test_get_story_content(self):
        """测试获取故事内容"""
        story = self.engine.get_story_content()

        assert "chapter_id" in story
        assert "title" in story
        assert "introduction" in story
        assert "narrative" in story
        assert "concepts" in story
        assert "commands" in story
        assert story["chapter_id"] == "prologue"

    def test_generate_challenge(self):
        """测试生成挑战"""
        challenge = self.engine.generate_challenge()

        assert challenge is not None
        assert challenge.challenge_id is not None
        assert challenge.title is not None
        assert challenge.question is not None
        assert challenge.expected_command is not None
        assert challenge.hint is not None
        assert challenge.reward_exp > 0

    def test_check_correct_answer(self):
        """测试检查正确答案"""
        self.engine.player = self.player
        self.engine.generate_challenge()

        if self.engine.current_challenge:
            # 找到正确选项的索引（从1开始）
            correct_index = self.engine.current_challenge.correct_option_index + 1
            result = self.engine.check_answer(correct_index)

            assert result["correct"] is True
            assert "经验值" in result["message"]

    def test_check_incorrect_answer(self):
        """测试检查错误答案"""
        self.engine.player = self.player
        self.engine.generate_challenge()

        if self.engine.current_challenge:
            # 选择一个错误的选项索引（从1开始）
            # 确保选择的不是正确选项
            correct_index = self.engine.current_challenge.correct_option_index + 1
            wrong_index = correct_index + 1 if correct_index < 4 else 1
            result = self.engine.check_answer(wrong_index)

            assert result["correct"] is False

    def test_check_answer_no_challenge(self):
        """测试无挑战时检查答案"""
        self.engine.current_challenge = None

        result = self.engine.check_answer("any command")

        assert result["correct"] is False

    def test_advance_chapter(self):
        """测试推进章节"""
        self.engine.player = self.player
        initial_chapter = self.engine.story_manager.current_chapter

        result = self.engine.advance_chapter()

        assert result is True
        assert self.engine.story_manager.current_chapter != initial_chapter

    def test_get_practice_commands(self):
        """测试获取可练习命令"""
        self.player.kubectl_commands_mastered = ["kubectl run", "kubectl get pods"]
        self.engine.player = self.player

        commands = self.engine.get_practice_commands()

        assert len(commands) == 2
        assert "kubectl run" in commands
        assert "kubectl get pods" in commands

    def test_generate_quiz(self):
        """测试生成测验"""
        self.player.kubectl_commands_mastered = ["kubectl run", "kubectl get pods"]
        self.engine.player = self.player

        quiz = self.engine.generate_quiz()

        assert quiz is not None
        assert "question" in quiz
        assert "options" in quiz
        assert len(quiz["options"]) == 4
        assert "correct_index" in quiz

    def test_generate_quiz_no_commands(self):
        """测试无命令时生成测验"""
        self.player.kubectl_commands_mastered = []
        self.engine.player = self.player

        quiz = self.engine.generate_quiz()

        assert quiz is not None
        assert "question" in quiz
        assert "还没有掌握任何命令" in quiz["question"]
        assert "options" in quiz
        assert len(quiz["options"]) == 0

    def test_get_progress(self):
        """测试获取进度"""
        self.player.kubectl_commands_mastered = ["kubectl run"]
        self.player.level = 3
        self.engine.player = self.player

        progress = self.engine.get_progress()

        assert "player" in progress
        assert "story" in progress
        assert "commands" in progress
        assert progress["player"]["level"] == 3

    def test_get_all_commands_info(self):
        """测试获取所有命令信息"""
        # 初始化玩家
        self.engine.player = self.player

        info = self.engine.get_all_commands_info()

        assert len(info) > 0
        assert "name" in info[0]
        assert "category" in info[0]
        assert "description" in info[0]
        assert "syntax" in info[0]
        assert "example" in info[0]
        assert "mastered" in info[0]

    def test_save_game(self):
        """测试保存游戏"""
        self.engine.player = self.player

        result = self.engine.save_game()

        assert result is True
        assert os.path.exists("player_save.json")

    def test_save_game_no_player(self):
        """测试无玩家时保存"""
        self.engine.player = None

        result = self.engine.save_game()

        assert result is False

    def test_reset_streak(self):
        """测试重置连击"""
        self.engine.streak = 5

        self.engine.reset_streak()

        assert self.engine.streak == 0
