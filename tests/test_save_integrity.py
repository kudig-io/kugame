"""测试存档完整性

测试原子写入、备份轮转、损坏恢复和新增字段的序列化。
"""

import json
import os

from kugame.player import Player, Sect


class TestAtomicSave:
    """测试原子存档"""

    def test_save_creates_file(self, tmp_path):
        """测试保存成功创建存档文件"""
        filepath = str(tmp_path / "save.json")
        player = Player(name="存档测试", sect=Sect.青云宗)

        assert player.save(filepath) is True
        assert os.path.exists(filepath)

    def test_save_no_tmp_leftover(self, tmp_path):
        """测试保存后不残留临时文件"""
        filepath = str(tmp_path / "save.json")
        player = Player(name="存档测试", sect=Sect.青云宗)
        player.save(filepath)

        assert not os.path.exists(filepath + ".tmp")

    def test_save_version_written(self, tmp_path):
        """测试存档包含schema版本号"""
        filepath = str(tmp_path / "save.json")
        player = Player(name="存档测试", sect=Sect.青云宗)
        player.save(filepath)

        with open(filepath, encoding="utf-8") as f:
            data = json.load(f)
        assert data["save_version"] == 2

    def test_second_save_creates_backup(self, tmp_path):
        """测试二次保存生成.bak备份且内容为上一版"""
        filepath = str(tmp_path / "save.json")
        player = Player(name="存档测试", sect=Sect.青云宗)
        player.save(filepath)

        player.level = 5
        player.save(filepath)

        backup = filepath + ".bak"
        assert os.path.exists(backup)
        with open(backup, encoding="utf-8") as f:
            old_data = json.load(f)
        with open(filepath, encoding="utf-8") as f:
            new_data = json.load(f)
        assert old_data["level"] == 1
        assert new_data["level"] == 5


class TestLoadRecovery:
    """测试损坏恢复"""

    def test_load_recovers_from_backup(self, tmp_path):
        """测试主存档损坏时从备份恢复"""
        filepath = str(tmp_path / "save.json")
        player = Player(name="备份恢复", sect=Sect.玄天宗)
        player.save(filepath)
        player.level = 3
        player.save(filepath)  # 生成 .bak

        # 损坏主存档
        with open(filepath, "w", encoding="utf-8") as f:
            f.write("{corrupted json!!!")

        loaded = Player.load(filepath)
        assert loaded is not None
        assert loaded.name == "备份恢复"

    def test_load_nonexistent_returns_none(self, tmp_path):
        """测试加载不存在的存档返回None"""
        assert Player.load(str(tmp_path / "missing.json")) is None


class TestWrongBookSerialization:
    """测试错题本字段序列化"""

    def test_wrong_fields_roundtrip(self, tmp_path):
        """测试错题字段保存后可完整还原"""
        filepath = str(tmp_path / "save.json")
        player = Player(name="错题测试", sect=Sect.青云宗)
        player.wrong_commands = ["kubectl get pods"]
        player.wrong_question_ids = ["pod_001", "svc_002"]
        player.wrong_review_progress = {"pod_001": 1}
        player.save(filepath)

        loaded = Player.load(filepath)
        assert loaded is not None
        assert loaded.wrong_commands == ["kubectl get pods"]
        assert loaded.wrong_question_ids == ["pod_001", "svc_002"]
        assert loaded.wrong_review_progress == {"pod_001": 1}

    def test_load_old_save_without_wrong_fields(self, tmp_path):
        """测试兼容缺少新字段的旧版存档"""
        filepath = str(tmp_path / "old_save.json")
        old_data = {
            "name": "老玩家",
            "sect": "青云宗",
            "level": 2,
            "experience": 100,
        }
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(old_data, f, ensure_ascii=False)

        loaded = Player.load(filepath)
        assert loaded is not None
        assert loaded.wrong_commands == []
        assert loaded.wrong_question_ids == []
        assert loaded.wrong_review_progress == {}
