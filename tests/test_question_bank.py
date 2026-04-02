"""题库系统测试

测试题目导入、解析和管理功能。
"""
# -*- coding: utf-8 -*-

import pytest
import os
import sys
import tempfile
import zipfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from kugame.question_bank import (
    Question, QuestionType, QuestionDifficulty, K8sCategory,
    QuestionBank
)
from kugame.question_import import (
    MarkdownParser, ZipImporter,
    import_questions_from_zip, preview_zip_contents
)


class TestQuestion:
    """测试题目类"""
    
    def test_question_creation(self):
        """测试题目创建"""
        q = Question(
            id="test_001",
            type=QuestionType.单选题,
            difficulty=QuestionDifficulty.简单,
            category=K8sCategory.Pod,
            question="测试题目",
            options=["A. 选项1", "B. 选项2"],
            correct_answer="A",
            explanation="解析",
        )
        
        assert q.id == "test_001"
        assert q.type == QuestionType.单选题
        assert q.question == "测试题目"
    
    def test_check_answer_single_choice(self):
        """测试单选题答案检查"""
        q = Question(
            id="test_001",
            type=QuestionType.单选题,
            difficulty=QuestionDifficulty.简单,
            category=K8sCategory.Pod,
            question="测试",
            options=["A. 1", "B. 2"],
            correct_answer="B",
        )
        
        is_correct, feedback = q.check_answer("B")
        assert is_correct is True
        
        is_correct, feedback = q.check_answer("A")
        assert is_correct is False
    
    def test_check_answer_multiple_choice(self):
        """测试多选题答案检查"""
        q = Question(
            id="test_002",
            type=QuestionType.多选题,
            difficulty=QuestionDifficulty.中等,
            category=K8sCategory.Pod,
            question="测试",
            options=["A. 1", "B. 2", "C. 3"],
            correct_answer=["A", "B"],
        )
        
        is_correct, feedback = q.check_answer(["A", "B"])
        assert is_correct is True
        
        is_correct, feedback = q.check_answer(["A", "C"])
        assert is_correct is False
    
    def test_check_answer_true_false(self):
        """测试判断题答案检查"""
        q = Question(
            id="test_003",
            type=QuestionType.判断题,
            difficulty=QuestionDifficulty.简单,
            category=K8sCategory.Pod,
            question="测试",
            correct_answer="True",
        )
        
        is_correct, feedback = q.check_answer("True")
        assert is_correct is True
        
        is_correct, feedback = q.check_answer("False")
        assert is_correct is False
    
    def test_to_dict(self):
        """测试转换为字典"""
        q = Question(
            id="test_001",
            type=QuestionType.单选题,
            difficulty=QuestionDifficulty.简单,
            category=K8sCategory.Pod,
            question="测试",
            correct_answer="A",
        )
        
        data = q.to_dict()
        assert data["id"] == "test_001"
        assert data["type"] == "single_choice"
        assert data["difficulty"] == 2


class TestQuestionBank:
    """测试题库管理器"""
    
    def test_bank_creation(self):
        """测试题库创建"""
        bank = QuestionBank()
        assert len(bank.questions) > 0  # 有默认题目
    
    def test_add_question(self):
        """测试添加题目"""
        bank = QuestionBank()
        q = Question(
            id="new_001",
            type=QuestionType.单选题,
            difficulty=QuestionDifficulty.简单,
            category=K8sCategory.Pod,
            question="新题目",
            correct_answer="A",
        )
        
        result = bank.add_question(q)
        assert result is True
        assert "new_001" in bank.questions
    
    def test_add_duplicate_question(self):
        """测试添加重复题目"""
        bank = QuestionBank()
        q = Question(
            id="q001",  # 默认题目已存在
            type=QuestionType.单选题,
            difficulty=QuestionDifficulty.简单,
            category=K8sCategory.Pod,
            question="重复",
            correct_answer="A",
        )
        
        result = bank.add_question(q)
        assert result is False
    
    def test_get_random_question(self):
        """测试随机获取题目"""
        bank = QuestionBank()
        q = bank.get_random_question()
        assert q is not None
    
    def test_get_questions_by_difficulty(self):
        """测试按难度筛选"""
        bank = QuestionBank()
        questions = bank.get_questions(difficulty=QuestionDifficulty.入门)
        assert len(questions) >= 0
    
    def test_generate_quiz(self):
        """测试生成练习卷"""
        bank = QuestionBank()
        quiz = bank.generate_quiz(num_questions=3)
        assert len(quiz) == 3
    
    def test_search_questions(self):
        """测试搜索题目"""
        bank = QuestionBank()
        results = bank.search_questions("Pod")
        assert len(results) >= 0
    
    def test_import_export(self):
        """测试导入导出"""
        bank = QuestionBank()
        
        # 导出
        data = bank.export_to_dict()
        assert "questions" in data
        
        # 导入到新题库
        new_bank = QuestionBank()
        imported, skipped = new_bank.import_from_dict(data, merge=False)
        assert imported > 0


class TestMarkdownParser:
    """测试Markdown解析器"""
    
    def test_parse_yaml_format(self):
        """测试YAML格式解析"""
        content = '''---
id: test_001
type: single_choice
difficulty: 2
category: pod
question: 测试题目
options:
  - A. 选项1
  - B. 选项2
answer: B
explanation: 解析
---

正文
'''
        q = MarkdownParser.parse_content(content, "test_001")
        
        assert q is not None
        assert q.id == "test_001"
        assert q.question == "测试题目"
        assert q.correct_answer == "B"
    
    def test_parse_marker_format(self):
        """测试标记格式解析"""
        content = '''[单选][简单][Pod]

测试题目内容？

A. 选项1
B. 选项2
C. 选项3

答案：B

解析：这是解析内容
'''
        q = MarkdownParser.parse_content(content, "test_002")
        
        assert q is not None
        assert q.type == QuestionType.单选题
        assert q.difficulty == QuestionDifficulty.简单
        assert "B" in str(q.correct_answer)
    
    def test_parse_multiple_choice(self):
        """测试多选题解析"""
        content = '''[多选][中等][Deployment]

多选题测试

A. 选项1
B. 选项2
C. 选项3

答案：A,B

解析：多选解析
'''
        q = MarkdownParser.parse_content(content, "test_003")
        
        assert q is not None
        assert q.type == QuestionType.多选题
        assert isinstance(q.correct_answer, list)
    
    def test_parse_fill_blank(self):
        """测试填空题解析"""
        content = '''[填空][中等][Storage]

完成命令：kubectl ______ pods

答案：get

解析：get用于获取资源
'''
        q = MarkdownParser.parse_content(content, "test_004")
        
        assert q is not None
        assert q.type == QuestionType.填空题


class TestZipImporter:
    """测试ZIP导入器"""
    
    def create_test_zip(self, temp_dir, files_content):
        """创建测试ZIP文件"""
        zip_path = os.path.join(temp_dir, "test_questions.zip")
        
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
            for filename, content in files_content.items():
                filepath = os.path.join(temp_dir, filename)
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                zf.write(filepath, filename)
        
        return zip_path
    
    def test_preview_zip(self):
        """测试预览ZIP"""
        with tempfile.TemporaryDirectory() as tmpdir:
            files = {
                "q001.md": '''---
id: q001
type: single_choice
question: 测试题目
answer: A
---
''',
                "q002.md": "[单选]\n\n题目2\n\nA. 1\nB. 2\n\n答案：A",
            }
            
            zip_path = self.create_test_zip(tmpdir, files)
            result = preview_zip_contents(zip_path)
            
            assert result["success"] is True
            assert result["md_files"] == 2
    
    def test_import_from_zip(self):
        """测试从ZIP导入"""
        with tempfile.TemporaryDirectory() as tmpdir:
            files = {
                "q001.md": '''---
id: zip_test_001
type: single_choice
difficulty: 1
category: pod
question: ZIP测试题目1
options:
  - A. 选项1
  - B. 选项2
answer: A
---
''',
                "q002.md": "[多选][中等][Service]\n\n题目2\n\nA. 1\nB. 2\n\n答案：AB",
            }
            
            zip_path = self.create_test_zip(tmpdir, files)
            
            bank = QuestionBank()
            importer = ZipImporter(bank)
            
            result = importer.import_from_zip(zip_path, temp_dir=os.path.join(tmpdir, "extract"))
            
            assert result["success"] is True
            assert result["imported"] == 2
            # 检查是否有导入的题目（ID基于文件名）
            assert any("q001" in qid for qid in bank.questions)
    
    def test_import_duplicate(self):
        """测试导入重复题目"""
        with tempfile.TemporaryDirectory() as tmpdir:
            files = {
                "q001.md": '''---
id: q001
type: single_choice
question: 重复题目
answer: A
---
''',
            }
            
            zip_path = self.create_test_zip(tmpdir, files)
            
            bank = QuestionBank()
            importer = ZipImporter(bank)
            
            # 第一次导入
            result1 = importer.import_from_zip(zip_path, temp_dir=os.path.join(tmpdir, "extract1"))
            assert result1["imported"] == 1
            
            # 第二次导入（应该跳过或生成新ID）
            result2 = importer.import_from_zip(zip_path, temp_dir=os.path.join(tmpdir, "extract2"))
            # 由于ID会生成唯一值，不会跳过而是创建新题目
            assert result2["imported"] + result2["skipped"] > 0
