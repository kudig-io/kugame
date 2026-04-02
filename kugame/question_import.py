"""题库导入系统

支持ZIP包导入和Markdown文件解析。
"""
# -*- coding: utf-8 -*-

import zipfile
import os
import re
import yaml
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime

from .question_bank import Question, QuestionType, QuestionDifficulty, K8sCategory


class MarkdownParser:
    """Markdown题目解析器"""
    
    # 题型识别标记
    TYPE_MARKERS = {
        "[单选]": QuestionType.单选题,
        "[多选]": QuestionType.多选题,
        "[填空]": QuestionType.填空题,
        "[判断]": QuestionType.判断题,
        "[简答]": QuestionType.简答题,
        "[命令]": QuestionType.命令补全,
    }
    
    # 难度识别
    DIFFICULTY_MARKERS = {
        "[入门]": QuestionDifficulty.入门,
        "[简单]": QuestionDifficulty.简单,
        "[中等]": QuestionDifficulty.中等,
        "[困难]": QuestionDifficulty.困难,
        "[专家]": QuestionDifficulty.专家,
    }
    
    @classmethod
    def parse_file(cls, filepath: str) -> Optional[Question]:
        """解析单个Markdown文件
        
        Args:
            filepath: MD文件路径
            
        Returns:
            Optional[Question]: 解析出的题目
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            return cls.parse_content(content, Path(filepath).stem)
        except Exception as e:
            print(f"解析文件失败 {filepath}: {e}")
            return None
    
    @classmethod
    def parse_content(cls, content: str, default_id: str = None) -> Optional[Question]:
        """解析Markdown内容
        
        支持的格式：
        1. YAML Frontmatter格式
        2. 标记格式
        
        Args:
            content: Markdown内容
            default_id: 默认题目ID
            
        Returns:
            Optional[Question]: 解析出的题目
        """
        # 尝试解析YAML Frontmatter
        if content.startswith('---'):
            question = cls._parse_yaml_format(content, default_id)
            if question:
                return question
        
        # 使用标记格式解析
        return cls._parse_marker_format(content, default_id)
    
    @classmethod
    def _parse_yaml_format(cls, content: str, default_id: str = None) -> Optional[Question]:
        """解析YAML Frontmatter格式"""
        try:
            # 提取YAML部分
            match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)$', content, re.DOTALL)
            if not match:
                return None
            
            yaml_content = match.group(1)
            body_content = match.group(2).strip()
            
            # 解析YAML
            metadata = yaml.safe_load(yaml_content)
            if not isinstance(metadata, dict):
                return None
            
            # 构建题目
            question_id = metadata.get('id', default_id or f"imported_{datetime.now().strftime('%Y%m%d%H%M%S')}")
            
            # 解析题型
            q_type_str = metadata.get('type', 'single_choice')
            q_type = QuestionType(q_type_str) if q_type_str in [t.value for t in QuestionType] else QuestionType.单选题
            
            # 解析难度
            diff_level = metadata.get('difficulty', 3)
            difficulty = QuestionDifficulty.中等
            if isinstance(diff_level, int):
                for diff in QuestionDifficulty:
                    if diff.level == diff_level:
                        difficulty = diff
                        break
            
            # 解析分类
            cat_str = metadata.get('category', 'concepts')
            category = K8sCategory(cat_str) if cat_str in [c.value for c in K8sCategory] else K8sCategory.基础概念
            
            # 获取题目内容
            question_text = metadata.get('question', body_content.split('\n')[0] if body_content else '')
            
            # 解析选项（如果有）
            options = metadata.get('options')
            if options is None and body_content:
                options = cls._extract_options_from_body(body_content)
            
            # 获取答案
            correct_answer = metadata.get('answer')
            if correct_answer is None:
                correct_answer = metadata.get('correct_answer')
            
            # 获取解析
            explanation = metadata.get('explanation', metadata.get('解析', ''))
            if not explanation and body_content:
                explanation = cls._extract_explanation_from_body(body_content)
            
            # 获取标签
            tags = metadata.get('tags', [])
            
            # 获取相关命令
            related_commands = metadata.get('related_commands', [])
            
            return Question(
                id=question_id,
                type=q_type,
                difficulty=difficulty,
                category=category,
                question=question_text,
                options=options,
                correct_answer=correct_answer,
                explanation=explanation,
                tags=tags,
                related_commands=related_commands,
                source="导入",
            )
            
        except Exception as e:
            print(f"YAML解析失败: {e}")
            return None
    
    @classmethod
    def _parse_marker_format(cls, content: str, default_id: str = None) -> Optional[Question]:
        """解析标记格式
        
        格式示例：
        [单选][中等][Pod]
        
        Kubernetes中Pod是什么？
        
        A. 一个容器
        B. 最小的部署单元
        C. 一个节点
        D. 一个服务
        
        答案：B
        
        解析：Pod是Kubernetes中最小的部署单元，可以包含一个或多个容器。
        """
        lines = content.strip().split('\n')
        if not lines:
            return None
        
        # 解析第一行的标记
        first_line = lines[0]
        
        q_type = QuestionType.单选题  # 默认单选
        difficulty = QuestionDifficulty.中等  # 默认中等
        category = K8sCategory.基础概念  # 默认基础概念
        
        for marker, q_t in cls.TYPE_MARKERS.items():
            if marker in first_line:
                q_type = q_t
                break
        
        for marker, diff in cls.DIFFICULTY_MARKERS.items():
            if marker in first_line:
                difficulty = diff
                break
        
        for cat in K8sCategory:
            if f"[{cat.value}]" in first_line or f"[{cat.name}]" in first_line:
                category = cat
                break
        
        # 查找题目内容、选项、答案和解析
        question_text = ""
        options = []
        correct_answer = ""
        explanation = ""
        
        # 找到第一个非标记行作为题目开始
        start_idx = 1 if '[' in first_line else 0
        
        # 查找答案行和解析行（从后往前找更可靠）
        answer_pattern = re.compile(r'^[\[\s]*(?:答案|answer)[\]\s]*[:：]?\s*(.+)$', re.IGNORECASE)
        explanation_pattern = re.compile(r'^[\[\s]*(?:解析|explanation)[\]\s]*[:：]?\s*(.+)$', re.IGNORECASE)
        
        # 先扫描一遍找到答案和解析的位置
        answer_idx = -1
        explanation_idx = -1
        
        for i, line in enumerate(lines[start_idx:], start=start_idx):
            if answer_pattern.match(line.strip()):
                answer_idx = i
                correct_answer = answer_pattern.match(line.strip()).group(1).strip()
            elif explanation_pattern.match(line.strip()):
                explanation_idx = i
                explanation = explanation_pattern.match(line.strip()).group(1).strip()
        
        # 确定题目和选项的范围
        content_end = len(lines)
        if explanation_idx > 0:
            content_end = explanation_idx
        elif answer_idx > 0:
            content_end = answer_idx
        
        # 解析选项（在内容区域内）
        in_options = False
        options_letters = ['A', 'B', 'C', 'D', 'E', 'F']
        option_pattern = re.compile(r'^([A-F])[\.\、\s]\s*(.+)$')
        
        for i in range(start_idx, content_end):
            line = lines[i].strip()
            if not line:
                continue
            
            # 跳过答案行
            if i == answer_idx:
                continue
            
            # 检查是否是选项
            option_match = option_pattern.match(line)
            if option_match:
                in_options = True
                options.append(line)
                continue
            
            # 如果已经在选项区域，但当前行不是新选项，可能是选项描述换行
            if in_options and line and line[0] not in options_letters:
                if options:
                    options[-1] += ' ' + line
                continue
            
            # 否则是题目内容
            if not question_text:
                question_text = line
            elif not in_options:  # 只有在还没有遇到选项时才追加题目
                question_text += '\n' + line
        
        # 如果还没找到答案，再扫描一次（可能在后面）
        if not correct_answer and answer_idx >= 0:
            correct_answer = answer_pattern.match(lines[answer_idx].strip()).group(1).strip()
        
        # 收集解析的多行内容
        if explanation_idx >= 0:
            explanation_lines = [explanation]
            for j in range(explanation_idx + 1, len(lines)):
                next_line = lines[j].strip()
                if next_line and not any(re.match(p, next_line) for p in [r'^[\[\s]*(?:答案|answer)', r'^[\[\s]*(?:标签|tags)']):
                    explanation_lines.append(next_line)
                else:
                    break
            explanation = '\n'.join(explanation_lines)
        
        # 处理多选题答案
        if q_type == QuestionType.多选题 and correct_answer:
            # 支持 "A,B,C" 或 "ABC" 格式
            if ',' in correct_answer or '，' in correct_answer:
                correct_answer = [a.strip().upper() for a in re.split(r'[,，]', correct_answer)]
            else:
                correct_answer = list(correct_answer.upper())
        
        # 如果没有找到题目内容，使用第一行
        if not question_text:
            question_text = lines[0] if lines else "未命名题目"
        
        question_id = default_id or f"imported_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        return Question(
            id=question_id,
            type=q_type,
            difficulty=difficulty,
            category=category,
            question=question_text,
            options=options if options else None,
            correct_answer=correct_answer,
            explanation=explanation,
            source="导入",
        )
    
    @classmethod
    def _extract_options_from_body(cls, body: str) -> List[str]:
        """从正文中提取选项"""
        options = []
        option_pattern = re.compile(r'^([A-F])\s*[\.\、]\s*(.+)$', re.MULTILINE)
        matches = option_pattern.findall(body)
        for letter, text in matches:
            options.append(f"{letter}. {text}")
        return options if options else None
    
    @classmethod
    def _extract_explanation_from_body(cls, body: str) -> str:
        """从正文中提取解析"""
        lines = body.split('\n')
        explanation_pattern = re.compile(r'^[解析|explanation]\s*[:：]?\s*(.+)$', re.IGNORECASE)
        
        for i, line in enumerate(lines):
            match = explanation_pattern.match(line.strip())
            if match:
                explanation = match.group(1)
                # 收集后续行
                for j in range(i+1, len(lines)):
                    next_line = lines[j].strip()
                    if next_line and not next_line.startswith('#'):
                        explanation += '\n' + next_line
                    else:
                        break
                return explanation
        
        return ""


class ZipImporter:
    """ZIP包导入器"""
    
    SUPPORTED_EXTENSIONS = ['.md', '.markdown', '.txt']
    
    def __init__(self, question_bank):
        """
        Args:
            question_bank: QuestionBank实例
        """
        self.question_bank = question_bank
        self.parser = MarkdownParser()
    
    def import_from_zip(self, zip_path: str, temp_dir: str = None) -> Dict[str, Any]:
        """从ZIP文件导入题目
        
        Args:
            zip_path: ZIP文件路径
            temp_dir: 临时解压目录
            
        Returns:
            Dict: 导入结果统计
        """
        if not os.path.exists(zip_path):
            return {"success": False, "error": "文件不存在"}
        
        if temp_dir is None:
            temp_dir = os.path.join(os.path.dirname(zip_path), 'temp_import')
        
        results = {
            "success": True,
            "total_files": 0,
            "parsed_files": 0,
            "imported": 0,
            "skipped": 0,
            "errors": [],
            "imported_ids": [],
        }
        
        try:
            # 解压ZIP
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                # 检查文件列表
                file_list = zip_ref.namelist()
                md_files = [f for f in file_list if any(f.endswith(ext) for ext in self.SUPPORTED_EXTENSIONS)]
                
                results["total_files"] = len(md_files)
                
                if not md_files:
                    return {"success": False, "error": "ZIP包中没有找到Markdown文件"}
                
                # 解压
                zip_ref.extractall(temp_dir)
            
            # 解析所有MD文件
            for md_file in md_files:
                filepath = os.path.join(temp_dir, md_file)
                try:
                    question = self.parser.parse_file(filepath)
                    if question:
                        results["parsed_files"] += 1
                        
                        # 生成唯一ID
                        base_id = Path(md_file).stem
                        question.id = self._generate_unique_id(base_id)
                        
                        # 添加到题库
                        if self.question_bank.add_question(question):
                            results["imported"] += 1
                            results["imported_ids"].append(question.id)
                        else:
                            results["skipped"] += 1
                    else:
                        results["errors"].append(f"无法解析: {md_file}")
                except Exception as e:
                    results["errors"].append(f"{md_file}: {str(e)}")
            
            return results
            
        except zipfile.BadZipFile:
            return {"success": False, "error": "无效的ZIP文件"}
        except Exception as e:
            return {"success": False, "error": str(e)}
        finally:
            # 清理临时目录
            self._cleanup_temp_dir(temp_dir)
    
    def _generate_unique_id(self, base_id: str) -> str:
        """生成唯一的题目ID"""
        if base_id not in self.question_bank.questions:
            return base_id
        
        # 添加后缀
        counter = 1
        while f"{base_id}_{counter}" in self.question_bank.questions:
            counter += 1
        return f"{base_id}_{counter}"
    
    def _cleanup_temp_dir(self, temp_dir: str):
        """清理临时目录"""
        try:
            import shutil
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
        except Exception as e:
            print(f"清理临时目录失败: {e}")
    
    def preview_zip(self, zip_path: str) -> Dict[str, Any]:
        """预览ZIP包内容（不解压）
        
        Args:
            zip_path: ZIP文件路径
            
        Returns:
            Dict: 包内文件列表和预览
        """
        if not os.path.exists(zip_path):
            return {"success": False, "error": "文件不存在"}
        
        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                file_list = zip_ref.namelist()
                md_files = [f for f in file_list if any(f.endswith(ext) for ext in self.SUPPORTED_EXTENSIONS)]
                
                # 预览前3个文件
                previews = []
                for md_file in md_files[:3]:
                    try:
                        content = zip_ref.read(md_file).decode('utf-8')
                        preview = self._get_preview(content)
                        previews.append({
                            "filename": md_file,
                            "preview": preview,
                        })
                    except Exception as e:
                        previews.append({
                            "filename": md_file,
                            "preview": f"预览失败: {e}",
                        })
                
                return {
                    "success": True,
                    "total_files": len(file_list),
                    "md_files": len(md_files),
                    "file_list": md_files,
                    "previews": previews,
                }
                
        except zipfile.BadZipFile:
            return {"success": False, "error": "无效的ZIP文件"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _get_preview(self, content: str, max_length: int = 200) -> str:
        """获取内容预览"""
        lines = content.strip().split('\n')
        preview = []
        
        for line in lines:
            line = line.strip()
            if line and not line.startswith('---'):
                preview.append(line)
                if len('\n'.join(preview)) >= max_length:
                    break
        
        result = '\n'.join(preview)
        if len(result) > max_length:
            result = result[:max_length] + "..."
        return result


# 便捷函数
def import_questions_from_zip(question_bank, zip_path: str) -> Dict[str, Any]:
    """便捷函数：从ZIP导入题目
    
    Args:
        question_bank: QuestionBank实例
        zip_path: ZIP文件路径
        
    Returns:
        Dict: 导入结果
    """
    importer = ZipImporter(question_bank)
    return importer.import_from_zip(zip_path)


def preview_zip_contents(zip_path: str) -> Dict[str, Any]:
    """便捷函数：预览ZIP内容
    
    Args:
        zip_path: ZIP文件路径
        
    Returns:
        Dict: 预览信息
    """
    importer = ZipImporter(None)
    return importer.preview_zip(zip_path)
