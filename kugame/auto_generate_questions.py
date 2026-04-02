"""自动题目生成器

基于Kubernetes命令自动生成基础题库。
"""
# -*- coding: utf-8 -*-

from typing import List, Dict, Any
import random

from .question_bank import (
    Question, QuestionType, QuestionDifficulty, K8sCategory, QuestionBank
)
from .kubernetes_commands import KubernetesCommandManager, CommandCategory


class QuestionGenerator:
    """题目生成器"""
    
    def __init__(self):
        self.cmd_mgr = KubernetesCommandManager()
        self.question_bank = QuestionBank()
    
    def generate_all(self, target_count: int = 500) -> int:
        """生成所有题目
        
        Args:
            target_count: 目标题目数量
            
        Returns:
            int: 实际生成数量
        """
        generated = 0
        
        # 1. 为每个命令生成题目
        for cmd_name, cmd in self.cmd_mgr.commands.items():
            # 每道命令生成3-5题
            num_questions = random.randint(3, 5)
            for i in range(num_questions):
                questions = self._generate_for_command(cmd, i)
                for q in questions:
                    if self.question_bank.add_question(q):
                        generated += 1
                        if generated >= target_count:
                            return generated
        
        # 2. 生成概念理解题
        concept_questions = self._generate_concept_questions()
        for q in concept_questions:
            if self.question_bank.add_question(q):
                generated += 1
                if generated >= target_count:
                    return generated
        
        # 3. 生成场景应用题
        scenario_questions = self._generate_scenario_questions()
        for q in scenario_questions:
            if self.question_bank.add_question(q):
                generated += 1
                if generated >= target_count:
                    return generated
        
        return generated
    
    def _generate_for_command(self, cmd, variant: int = 0) -> List[Question]:
        """为单个命令生成题目"""
        questions = []
        
        # 映射命令分类到题目分类
        category_map = {
            CommandCategory.基础操作: K8sCategory.基础概念,
            CommandCategory.部署管理: K8sCategory.Deployment,
            CommandCategory.服务发现: K8sCategory.Service,
            CommandCategory.配置管理: K8sCategory.ConfigMap,
            CommandCategory.存储管理: K8sCategory.存储,
            CommandCategory.资源管理: K8sCategory.调度,
            CommandCategory.故障排查: K8sCategory.故障排查,
            CommandCategory.进阶操作: K8sCategory.调度,
            CommandCategory.集群管理: K8sCategory.集群管理,
            CommandCategory.网络管理: K8sCategory.网络,
            CommandCategory.安全管理: K8sCategory.安全,
            CommandCategory.工具命令: K8sCategory.基础概念,
        }
        
        category = category_map.get(cmd.category, K8sCategory.基础概念)
        
        # 根据命令生成不同类型的题目
        if variant == 0:
            # 命令功能题
            q = self._create_command_function_question(cmd, category)
            if q:
                questions.append(q)
        elif variant == 1:
            # 语法补全题
            q = self._create_syntax_question(cmd, category)
            if q:
                questions.append(q)
        elif variant == 2:
            # 使用场景题
            q = self._create_scenario_question(cmd, category)
            if q:
                questions.append(q)
        elif variant == 3:
            # 相关命令题
            q = self._create_related_command_question(cmd, category)
            if q:
                questions.append(q)
        else:
            # 概念判断题
            q = self._create_concept_question(cmd, category)
            if q:
                questions.append(q)
        
        return questions
    
    def _create_command_function_question(self, cmd, category) -> Question:
        """创建命令功能题"""
        question_id = f"auto_{cmd.name.replace(' ', '_').replace('-', '_')}_{random.randint(1000, 9999)}"
        
        # 从命令描述生成题目
        desc = cmd.description
        
        # 获取同分类的其他命令作为干扰项
        same_category_cmds = [
            c for c in self.cmd_mgr.commands.values()
            if c.category == cmd.category and c.name != cmd.name
        ]
        
        if len(same_category_cmds) < 3:
            return None
        
        distractors = random.sample(same_category_cmds, 3)
        
        options = [
            f"A. {cmd.name}",
            f"B. {distractors[0].name}",
            f"C. {distractors[1].name}",
            f"D. {distractors[2].name}",
        ]
        
        random.shuffle(options)
        
        # 找到正确答案的选项
        correct_letter = None
        for i, opt in enumerate(options):
            if cmd.name in opt:
                correct_letter = chr(ord('A') + i)
                break
        
        if not correct_letter:
            correct_letter = 'A'
        
        # 确定难度
        difficulty = QuestionDifficulty.简单 if cmd.difficulty <= 2 else (
            QuestionDifficulty.中等 if cmd.difficulty <= 4 else QuestionDifficulty.困难
        )
        
        return Question(
            id=question_id,
            type=QuestionType.单选题,
            difficulty=difficulty,
            category=category,
            question=f"以下哪个命令可以{desc}？",
            options=options,
            correct_answer=correct_letter,
            explanation=f"{cmd.name} 命令用于{desc}。\n语法: {cmd.syntax}\n示例: {cmd.example}",
            related_commands=[cmd.name],
            tags=["命令识别", cmd.category.value],
            source="自动生成",
        )
    
    def _create_syntax_question(self, cmd, category) -> Question:
        """创建语法补全题"""
        question_id = f"auto_syntax_{cmd.name.replace(' ', '_').replace('-', '_')}_{random.randint(1000, 9999)}"
        
        # 从语法中提取关键部分
        syntax = cmd.syntax
        
        # 找到关键参数进行挖空
        common_flags = ['--namespace', '-n', '--all', '-o', '--watch', '-w', '--force', '--grace-period']
        
        # 简化为填空题
        if 'create' in cmd.name:
            blank_part = 'create'
        elif 'get' in cmd.name:
            blank_part = 'get'
        elif 'delete' in cmd.name:
            blank_part = 'delete'
        elif 'apply' in cmd.name:
            blank_part = 'apply'
        else:
            parts = cmd.name.split()
            blank_part = parts[-1] if len(parts) > 1 else parts[0]
        
        question_text = syntax.replace(blank_part, '______', 1)
        
        # 生成干扰项
        all_verbs = ['create', 'get', 'delete', 'apply', 'describe', 'edit', 'patch', 'replace', 'rollout', 'scale', 'expose', 'run']
        if blank_part in all_verbs:
            all_verbs.remove(blank_part)
        
        distractors = random.sample(all_verbs, min(3, len(all_verbs)))
        options = [blank_part] + distractors
        random.shuffle(options)
        
        options_str = [f"{chr(ord('A')+i)}. {opt}" for i, opt in enumerate(options)]
        correct_letter = chr(ord('A') + options.index(blank_part))
        
        return Question(
            id=question_id,
            type=QuestionType.单选题,
            difficulty=QuestionDifficulty.中等,
            category=category,
            question=f"补全命令: {question_text}",
            options=options_str,
            correct_answer=correct_letter,
            explanation=f"正确答案是 '{blank_part}'。\n完整命令: {syntax}\n说明: {cmd.description}",
            related_commands=[cmd.name],
            tags=["命令语法", "填空"],
            source="自动生成",
        )
    
    def _create_scenario_question(self, cmd, category) -> Question:
        """创建场景应用题"""
        question_id = f"auto_scenario_{cmd.name.replace(' ', '_').replace('-', '_')}_{random.randint(1000, 9999)}"
        
        # 构建场景描述
        scenarios = {
            CommandCategory.基础操作: [
                f"你需要快速查看集群中运行的Pod状态",
                f"你想创建一个新的Nginx服务进行测试",
            ],
            CommandCategory.部署管理: [
                f"你需要将Deployment的副本数扩展到5个",
                f"你想查看Deployment的滚动更新状态",
            ],
            CommandCategory.故障排查: [
                f"应用出现问题，你需要查看容器日志",
                f"Pod无法启动，你想进入容器调试",
            ],
            CommandCategory.存储管理: [
                f"你需要查看集群中的持久卷",
                f"想查看某个PVC的绑定状态",
            ],
        }
        
        scenario_list = scenarios.get(cmd.category, [f"你需要{cmd.description}"])
        scenario = random.choice(scenario_list)
        
        # 干扰项 - 其他分类的命令
        other_cmds = [c for c in self.cmd_mgr.commands.values() if c.category != cmd.category]
        if len(other_cmds) < 3:
            return None
        
        distractors = random.sample(other_cmds, 3)
        
        options = [
            f"A. {cmd.name}",
            f"B. {distractors[0].name}",
            f"C. {distractors[1].name}",
            f"D. {distractors[2].name}",
        ]
        random.shuffle(options)
        
        correct_letter = None
        for i, opt in enumerate(options):
            if cmd.name in opt:
                correct_letter = chr(ord('A') + i)
                break
        
        if not correct_letter:
            correct_letter = 'A'
        
        return Question(
            id=question_id,
            type=QuestionType.单选题,
            difficulty=QuestionDifficulty.中等,
            category=category,
            question=f"场景: {scenario}，应该使用哪个命令？",
            options=options,
            correct_answer=correct_letter,
            explanation=f"正确答案是 {cmd.name}。\n{cmd.description}\n用法: {cmd.example}",
            related_commands=[cmd.name],
            tags=["场景应用", cmd.category.value],
            source="自动生成",
        )
    
    def _create_related_command_question(self, cmd, category) -> Question:
        """创建相关命令题"""
        if not cmd.related_commands:
            return None
        
        question_id = f"auto_related_{cmd.name.replace(' ', '_').replace('-', '_')}_{random.randint(1000, 9999)}"
        
        related = cmd.related_commands[:]
        if len(related) < 2:
            return None
        
        # 随机选择是否询问相关命令
        if random.choice([True, False]):
            # 问"与X相关的命令是"
            target_cmd = random.choice(related)
            question = f"与 '{cmd.name}' 经常配合使用的命令是？"
            correct = target_cmd
        else:
            # 问"X命令的作用"
            question = f"'{random.choice(related)}' 命令的作用是？"
            # 找到这个命令
            target = random.choice(related)
            target_cmd_obj = self.cmd_mgr.commands.get(target)
            if target_cmd_obj:
                correct = target_cmd_obj.description
            else:
                return None
        
        return Question(
            id=question_id,
            type=QuestionType.填空题,
            difficulty=QuestionDifficulty.中等,
            category=category,
            question=question,
            correct_answer=correct,
            explanation=f"{cmd.name} 的相关命令包括: {', '.join(cmd.related_commands)}",
            related_commands=[cmd.name] + cmd.related_commands,
            tags=["相关命令"],
            source="自动生成",
        )
    
    def _create_concept_question(self, cmd, category) -> Question:
        """创建概念判断题"""
        question_id = f"auto_concept_{cmd.name.replace(' ', '_').replace('-', '_')}_{random.randint(1000, 9999)}"
        
        # 生成判断题
        statements = [
            (f"'{cmd.name}' 命令可以用于{cmd.description}", True),
            (f"'{cmd.name}' 命令只能在default命名空间使用", False),
            (f"使用 '{cmd.name}' 需要cluster-admin权限", cmd.category in [CommandCategory.集群管理, CommandCategory.安全管理]),
        ]
        
        statement, is_true = random.choice(statements)
        
        return Question(
            id=question_id,
            type=QuestionType.判断题,
            difficulty=QuestionDifficulty.简单,
            category=category,
            question=statement,
            correct_answer="True" if is_true else "False",
            explanation=f"{cmd.description}\n语法: {cmd.syntax}",
            related_commands=[cmd.name],
            tags=["概念判断"],
            source="自动生成",
        )
    
    def _generate_concept_questions(self) -> List[Question]:
        """生成概念理解题"""
        questions = []
        
        concept_questions = [
            {
                "id": "auto_concept_001",
                "question": "Kubernetes中，Pod和Container的关系是什么？",
                "options": ["A. 一对一", "B. 一对多", "C. 多对一", "D. 没有关系"],
                "correct": "B",
                "category": K8sCategory.基础概念,
                "explanation": "一个Pod可以包含一个或多个Container，它们共享网络和存储。"
            },
            {
                "id": "auto_concept_002",
                "question": "Deployment和ReplicaSet的关系是？",
                "options": ["A. Deployment管理ReplicaSet", "B. ReplicaSet管理Deployment", "C. 同级关系", "D. 没有关系"],
                "correct": "A",
                "category": K8sCategory.Deployment,
                "explanation": "Deployment通过管理ReplicaSet来实现Pod的滚动更新和回滚。"
            },
            {
                "id": "auto_concept_003",
                "question": "Service的作用是什么？",
                "options": ["A. 部署应用", "B. 服务发现和负载均衡", "C. 存储数据", "D. 监控告警"],
                "correct": "B",
                "category": K8sCategory.Service,
                "explanation": "Service为一组Pod提供稳定的访问入口，实现服务发现和负载均衡。"
            },
        ]
        
        for q_data in concept_questions:
            q = Question(
                id=q_data["id"],
                type=QuestionType.单选题,
                difficulty=QuestionDifficulty.简单,
                category=q_data["category"],
                question=q_data["question"],
                options=q_data["options"],
                correct_answer=q_data["correct"],
                explanation=q_data["explanation"],
                source="自动生成",
            )
            questions.append(q)
        
        return questions
    
    def _generate_scenario_questions(self) -> List[Question]:
        """生成场景应用题"""
        questions = []
        
        scenarios = [
            {
                "id": "auto_scenario_001",
                "question": "应用发布新版本后出现问题，需要回滚到上一版本，应该怎么做？",
                "options": [
                    "A. kubectl delete deployment 重新创建",
                    "B. kubectl rollout undo deployment/xxx",
                    "C. 修改镜像标签重新部署",
                    "D. 重启所有Pod"
                ],
                "correct": "B",
                "category": K8sCategory.Deployment,
                "difficulty": QuestionDifficulty.中等,
                "explanation": "kubectl rollout undo 是标准的回滚命令，可以快速回到上一版本。"
            },
            {
                "id": "auto_scenario_002",
                "question": "需要查看Pod的实时日志，应该使用什么命令？",
                "options": [
                    "A. kubectl logs pod-name",
                    "B. kubectl logs pod-name -f",
                    "C. kubectl get logs pod-name",
                    "D. kubectl describe pod pod-name"
                ],
                "correct": "B",
                "category": K8sCategory.故障排查,
                "difficulty": QuestionDifficulty.简单,
                "explanation": "-f 参数表示follow，会持续跟踪日志输出。"
            },
        ]
        
        for q_data in scenarios:
            q = Question(
                id=q_data["id"],
                type=QuestionType.单选题,
                difficulty=q_data.get("difficulty", QuestionDifficulty.中等),
                category=q_data["category"],
                question=q_data["question"],
                options=q_data["options"],
                correct_answer=q_data["correct"],
                explanation=q_data["explanation"],
                source="自动生成",
            )
            questions.append(q)
        
        return questions


def generate_and_save(target_count: int = 500) -> Dict[str, Any]:
    """生成题目并返回结果
    
    Args:
        target_count: 目标题目数量
        
    Returns:
        Dict: 生成结果统计
    """
    generator = QuestionGenerator()
    count = generator.generate_all(target_count)
    
    stats = generator.question_bank.get_statistics()
    
    return {
        "generated": count,
        "total": stats["total_questions"],
        "by_type": stats["by_type"],
        "by_difficulty": stats["by_difficulty"],
        "by_category": stats["by_category"],
        "bank": generator.question_bank,
    }


# 便捷函数
def quick_generate(min_questions: int = 500) -> QuestionBank:
    """快速生成题目的便捷函数
    
    Args:
        min_questions: 最少题目数量
        
    Returns:
        QuestionBank: 包含生成题目的题库
    """
    result = generate_and_save(min_questions)
    return result["bank"]
