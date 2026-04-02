"""增强版Kubernetes题库系统

支持多种题型、难度分级、标签系统和ZIP导入功能。
"""
# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Tuple
from enum import Enum
import random
import re


class QuestionType(Enum):
    """题目类型"""
    单选题 = "single_choice"
    多选题 = "multiple_choice"
    填空题 = "fill_blank"
    判断题 = "true_false"
    简答题 = "short_answer"
    命令补全 = "command_complete"


class QuestionDifficulty(Enum):
    """题目难度"""
    入门 = (1, "⭐", "适合初学者")
    简单 = (2, "⭐⭐", "基础知识")
    中等 = (3, "⭐⭐⭐", "需要理解")
    困难 = (4, "⭐⭐⭐⭐", "深入掌握")
    专家 = (5, "⭐⭐⭐⭐⭐", "高级应用")
    
    def __init__(self, level, stars, description):
        self.level = level
        self.stars = stars
        self.description = description


class K8sCategory(Enum):
    """Kubernetes知识分类"""
    基础概念 = "concepts"
    Pod = "pod"
    Deployment = "deployment"
    Service = "service"
    ConfigMap = "configmap"
    Secret = "secret"
    存储 = "storage"
    网络 = "network"
    安全 = "security"
    调度 = "scheduling"
    监控 = "monitoring"
    故障排查 = "troubleshooting"
    Helm = "helm"
    集群管理 = "cluster"


@dataclass
class Question:
    """题目数据类
    
    Attributes:
        id: 题目唯一ID
        type: 题目类型
        difficulty: 难度
        category: 知识分类
        tags: 标签列表
        question: 题目内容
        options: 选项（选择题）
        correct_answer: 正确答案
        explanation: 解析
        related_commands: 相关命令
        source: 来源
        created_at: 创建时间
    """
    id: str
    type: QuestionType
    difficulty: QuestionDifficulty
    category: K8sCategory
    question: str
    correct_answer: Any
    options: Optional[List[str]] = None
    explanation: str = ""
    tags: List[str] = field(default_factory=list)
    related_commands: List[str] = field(default_factory=list)
    source: str = "内置"
    created_at: Optional[str] = None
    
    def __post_init__(self):
        if self.created_at is None:
            from datetime import datetime
            self.created_at = datetime.now().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "id": self.id,
            "type": self.type.value,
            "difficulty": self.difficulty.level,
            "category": self.category.value,
            "question": self.question,
            "options": self.options,
            "correct_answer": self.correct_answer,
            "explanation": self.explanation,
            "tags": self.tags,
            "related_commands": self.related_commands,
            "source": self.source,
            "created_at": self.created_at,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Question":
        """从字典创建"""
        # 解析难度
        diff_level = data.get("difficulty", 3)
        difficulty = QuestionDifficulty.中等
        if isinstance(diff_level, int):
            for diff in QuestionDifficulty:
                if diff.level == diff_level:
                    difficulty = diff
                    break
        
        # 解析分类
        cat_value = data.get("category", "concepts")
        category = K8sCategory.基础概念
        for cat in K8sCategory:
            if cat.value == cat_value:
                category = cat
                break
        
        return cls(
            id=data["id"],
            type=QuestionType(data["type"]),
            difficulty=difficulty,
            category=category,
            question=data["question"],
            options=data.get("options"),
            correct_answer=data["correct_answer"],
            explanation=data.get("explanation", ""),
            tags=data.get("tags", []),
            related_commands=data.get("related_commands", []),
            source=data.get("source", "导入"),
            created_at=data.get("created_at"),
        )
    
    def check_answer(self, answer: Any) -> Tuple[bool, str]:
        """检查答案
        
        Returns:
            Tuple[bool, str]: (是否正确, 反馈信息)
        """
        if self.type == QuestionType.单选题:
            is_correct = str(answer).upper() == str(self.correct_answer).upper()
        elif self.type == QuestionType.多选题:
            user_answers = set(str(a).upper() for a in answer) if isinstance(answer, list) else {str(answer).upper()}
            correct_answers = set(str(a).upper() for a in self.correct_answer) if isinstance(self.correct_answer, list) else {str(self.correct_answer).upper()}
            is_correct = user_answers == correct_answers
        elif self.type == QuestionType.判断题:
            is_correct = str(answer).lower() == str(self.correct_answer).lower()
        elif self.type == QuestionType.填空题:
            if isinstance(self.correct_answer, list):
                is_correct = str(answer).strip().lower() in [a.strip().lower() for a in self.correct_answer]
            else:
                is_correct = str(answer).strip().lower() == str(self.correct_answer).strip().lower()
        else:
            # 简答题和命令补全由人工或模糊匹配判断
            is_correct = str(answer).strip().lower() == str(self.correct_answer).strip().lower()
        
        if is_correct:
            return True, "回答正确！" + (f"\n解析：{self.explanation}" if self.explanation else "")
        else:
            return False, f"回答错误。正确答案是：{self.correct_answer}" + (f"\n解析：{self.explanation}" if self.explanation else "")


class QuestionBank:
    """题库管理器
    
    管理所有题目，支持导入、查询、练习等功能。
    """
    
    def __init__(self):
        self.questions: Dict[str, Question] = {}
        self._init_default_questions()
    
    def _init_default_questions(self):
        """初始化默认题目"""
        default_questions = [
            # 单选题示例
            Question(
                id="q001",
                type=QuestionType.单选题,
                difficulty=QuestionDifficulty.入门,
                category=K8sCategory.基础概念,
                question="Kubernetes中，最小的部署单元是什么？",
                options=["A. Node", "B. Pod", "C. Container", "D. Cluster"],
                correct_answer="B",
                explanation="Pod是Kubernetes中最小的部署单元，一个Pod可以包含一个或多个容器。",
                tags=["基础", "概念"],
                related_commands=["kubectl get pods"],
            ),
            Question(
                id="q002",
                type=QuestionType.单选题,
                difficulty=QuestionDifficulty.简单,
                category=K8sCategory.Pod,
                question="查看所有Pod的命令是什么？",
                options=[
                    "A. kubectl get nodes",
                    "B. kubectl get pods",
                    "C. kubectl list pods",
                    "D. kubectl show pods"
                ],
                correct_answer="B",
                explanation="kubectl get pods 是查看所有Pod的标准命令。",
                tags=["命令", "查询"],
                related_commands=["kubectl get pods", "kubectl get pods -o wide"],
            ),
            # 多选题示例
            Question(
                id="q003",
                type=QuestionType.多选题,
                difficulty=QuestionDifficulty.中等,
                category=K8sCategory.Deployment,
                question="Deployment可以实现哪些功能？（多选）",
                options=[
                    "A. 应用部署",
                    "B. 滚动更新",
                    "C. 自动扩缩容",
                    "D. 服务发现"
                ],
                correct_answer=["A", "B", "C"],
                explanation="Deployment主要负责应用部署、滚动更新和自动扩缩容，服务发现是Service的功能。",
                tags=["Deployment", "功能"],
                related_commands=["kubectl create deployment", "kubectl rollout"],
            ),
            # 判断题示例
            Question(
                id="q004",
                type=QuestionType.判断题,
                difficulty=QuestionDifficulty.简单,
                category=K8sCategory.Service,
                question="Service可以直接访问容器内部的端口。",
                correct_answer="False",
                explanation="Service访问的是Pod的端口，而不是直接访问容器内部端口。",
                tags=["Service", "网络"],
                related_commands=["kubectl expose", "kubectl get svc"],
            ),
            # 填空题示例
            Question(
                id="q005",
                type=QuestionType.填空题,
                difficulty=QuestionDifficulty.中等,
                category=K8sCategory.ConfigMap,
                question="创建ConfigMap的命令是：kubectl ______ configmap",
                correct_answer=["create", "apply"],
                explanation="可以使用 kubectl create configmap 或 kubectl apply -f configmap.yaml 创建ConfigMap。",
                tags=["ConfigMap", "命令"],
                related_commands=["kubectl create configmap"],
            ),
            # 命令补全示例
            Question(
                id="q006",
                type=QuestionType.命令补全,
                difficulty=QuestionDifficulty.困难,
                category=K8sCategory.故障排查,
                question="查看Pod日志并实时跟踪的命令：kubectl logs ______",
                correct_answer="-f",
                explanation="-f 参数表示follow，实时跟踪日志输出。",
                tags=["日志", "排查"],
                related_commands=["kubectl logs", "kubectl logs -f"],
            ),
        ]
        
        for q in default_questions:
            self.questions[q.id] = q
    
    def add_question(self, question: Question) -> bool:
        """添加题目"""
        if question.id in self.questions:
            return False
        self.questions[question.id] = question
        return True
    
    def update_question(self, question_id: str, updates: Dict[str, Any]) -> bool:
        """更新题目"""
        if question_id not in self.questions:
            return False
        
        q = self.questions[question_id]
        for key, value in updates.items():
            if hasattr(q, key):
                setattr(q, key, value)
        return True
    
    def delete_question(self, question_id: str) -> bool:
        """删除题目"""
        if question_id in self.questions:
            del self.questions[question_id]
            return True
        return False
    
    def get_question(self, question_id: str) -> Optional[Question]:
        """获取指定题目"""
        return self.questions.get(question_id)
    
    def get_random_question(self, 
                           difficulty: Optional[QuestionDifficulty] = None,
                           category: Optional[K8sCategory] = None,
                           question_type: Optional[QuestionType] = None) -> Optional[Question]:
        """随机获取题目"""
        filtered = list(self.questions.values())
        
        if difficulty:
            filtered = [q for q in filtered if q.difficulty == difficulty]
        if category:
            filtered = [q for q in filtered if q.category == category]
        if question_type:
            filtered = [q for q in filtered if q.type == question_type]
        
        if not filtered:
            return None
        
        return random.choice(filtered)
    
    def get_questions(self,
                     difficulty: Optional[QuestionDifficulty] = None,
                     category: Optional[K8sCategory] = None,
                     question_type: Optional[QuestionType] = None,
                     tag: Optional[str] = None,
                     limit: int = 50) -> List[Question]:
        """获取题目列表"""
        filtered = list(self.questions.values())
        
        if difficulty:
            filtered = [q for q in filtered if q.difficulty == difficulty]
        if category:
            filtered = [q for q in filtered if q.category == category]
        if question_type:
            filtered = [q for q in filtered if q.type == question_type]
        if tag:
            filtered = [q for q in filtered if tag in q.tags]
        
        return filtered[:limit]
    
    def generate_quiz(self, 
                      num_questions: int = 10,
                      difficulties: Optional[List[QuestionDifficulty]] = None) -> List[Question]:
        """生成练习卷"""
        if difficulties is None:
            difficulties = [QuestionDifficulty.入门, QuestionDifficulty.简单, QuestionDifficulty.中等]
        
        # 按难度分布选题
        questions_per_difficulty = num_questions // len(difficulties)
        result = []
        
        for diff in difficulties:
            available = self.get_questions(difficulty=diff)
            selected = random.sample(available, min(questions_per_difficulty, len(available)))
            result.extend(selected)
        
        # 如果数量不足，随机补充
        while len(result) < num_questions:
            q = self.get_random_question()
            if q and q not in result:
                result.append(q)
        
        random.shuffle(result)
        return result[:num_questions]
    
    def search_questions(self, keyword: str) -> List[Question]:
        """搜索题目"""
        keyword = keyword.lower()
        results = []
        
        for q in self.questions.values():
            if (keyword in q.question.lower() or
                keyword in q.explanation.lower() or
                any(keyword in tag.lower() for tag in q.tags)):
                results.append(q)
        
        return results
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取题库统计"""
        total = len(self.questions)
        
        by_type = {}
        for q in self.questions.values():
            by_type[q.type.value] = by_type.get(q.type.value, 0) + 1
        
        by_difficulty = {}
        for q in self.questions.values():
            by_difficulty[q.difficulty.name] = by_difficulty.get(q.difficulty.name, 0) + 1
        
        by_category = {}
        for q in self.questions.values():
            by_category[q.category.value] = by_category.get(q.category.value, 0) + 1
        
        return {
            "total_questions": total,
            "by_type": by_type,
            "by_difficulty": by_difficulty,
            "by_category": by_category,
        }
    
    def export_to_dict(self) -> Dict[str, Any]:
        """导出为字典"""
        return {
            "version": "1.0",
            "total": len(self.questions),
            "questions": [q.to_dict() for q in self.questions.values()],
        }
    
    def import_from_dict(self, data: Dict[str, Any], merge: bool = False) -> Tuple[int, int]:
        """从字典导入
        
        Args:
            data: 题目数据
            merge: 是否合并（True则保留现有题目，False则替换）
            
        Returns:
            Tuple[int, int]: (成功导入数, 跳过的重复数)
        """
        if not merge:
            self.questions.clear()
        
        imported = 0
        skipped = 0
        
        for q_data in data.get("questions", []):
            try:
                question = Question.from_dict(q_data)
                if question.id in self.questions:
                    skipped += 1
                    continue
                self.questions[question.id] = question
                imported += 1
            except Exception as e:
                print(f"导入题目失败: {e}")
                skipped += 1
        
        return imported, skipped
