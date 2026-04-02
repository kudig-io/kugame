"""测试故事管理器

测试StoryManager类的所有功能。
"""

from kugame.story import StoryManager, Chapter
from kugame.player import Player, Sect


class TestStoryManager:
    """测试StoryManager类"""

    def setup_method(self):
        """测试初始化"""
        self.story_manager = StoryManager()
        self.player = Player(name="测试侠客", sect=Sect.青云宗)

    def test_initial_chapter(self):
        """测试初始章节"""
        assert self.story_manager.current_chapter == Chapter.序章

    def test_get_current_chapter(self):
        """测试获取当前章节"""
        chapter = self.story_manager.get_current_chapter()

        assert chapter is not None
        assert chapter.chapter_id == Chapter.序章
        assert chapter.title == "踏入仙门"

    def test_get_specific_chapter(self):
        """测试获取指定章节"""
        # 当前只实现了序章，后续章节待开发
        chapter = self.story_manager.get_chapter(Chapter.序章)

        assert chapter is not None
        assert chapter.title == "踏入仙门"

    def test_get_nonexistent_chapter(self):
        """测试获取不存在的章节"""
        chapter = self.story_manager.get_chapter(None)

        assert chapter is None

    def test_advance_chapter(self):
        """测试推进章节"""
        initial_chapter = self.story_manager.current_chapter

        result = self.story_manager.advance_chapter()

        assert result is True
        assert self.story_manager.current_chapter != initial_chapter

    def test_advance_to_final_chapter(self):
        """测试推进到最终章节"""
        self.story_manager.current_chapter = Chapter.终章

        result = self.story_manager.advance_chapter()

        assert result is False

    def test_get_all_commands(self):
        """测试获取所有命令"""
        commands = self.story_manager.get_all_commands()

        assert len(commands) > 0
        assert "kubectl run" in commands
        # 后续章节的命令待实现

    def test_get_chapter_commands(self):
        """测试获取指定章节命令"""
        commands = self.story_manager.get_chapter_commands(Chapter.序章)

        assert len(commands) > 0
        assert "kubectl run" in commands

    def test_get_total_chapters(self):
        """测试获取总章节数"""
        total = self.story_manager.get_total_chapters()

        # 当前只实现了序章，后续章节待开发
        assert total >= 1

    def test_get_completed_chapters(self):
        """测试获取已完成章节数"""
        # 基于当前章节值计算已完成章节
        completed = self.story_manager.get_completed_chapters(self.player.current_chapter)

        assert completed >= 0

    def test_get_story_progress(self):
        """测试获取故事进度"""
        progress = self.story_manager.get_story_progress(self.player)

        assert "current_chapter" in progress
        assert "current_title" in progress
        assert "total_chapters" in progress
        assert "completed_chapters" in progress
        assert "all_commands" in progress
        assert "mastered_commands" in progress

    def test_chapter_command_count(self):
        """测试章节命令数量"""
        chapter = self.story_manager.get_current_chapter()

        assert chapter.command_count == len(chapter.commands_to_learn)


class TestChapter:
    """测试Chapter枚举"""

    def test_chapter_order(self):
        """测试章节顺序"""
        chapters = list(Chapter)

        assert chapters[0] == Chapter.序章
        assert chapters[1] == Chapter.第一章
        assert chapters[-1] == Chapter.终章

    def test_chapter_values(self):
        """测试章节值"""
        assert Chapter.序章.value == "prologue"
        assert Chapter.第一章.value == "chapter_1"
        assert Chapter.终章.value == "epilogue"

    def test_chapter_count(self):
        """测试章节数量"""
        assert len(Chapter) == 13
