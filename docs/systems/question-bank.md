# 题库系统文档

## 概述

KuGame题库系统支持多种题型、难度分级和自定义导入，帮助玩家更全面地学习Kubernetes知识。

## 题目类型

| 类型 | 说明 | 示例 |
|------|------|------|
| **单选题** | 四选一 | 选择正确的命令 |
| **多选题** | 多选少选都错 | 选择所有适用场景 |
| **填空题** | 补全命令或概念 | kubectl ___ pods |
| **判断题** | 对/错判断 | ConfigMap可以存储密码 |
| **简答题** | 开放性问题 | 解释Pod的生命周期 |
| **命令补全** | 补全命令参数 | kubectl logs __ |

## 难度分级

| 等级 | 星级 | 说明 |
|------|------|------|
| 入门 | ⭐ | 适合初学者 |
| 简单 | ⭐⭐ | 基础知识 |
| 中等 | ⭐⭐⭐ | 需要理解概念 |
| 困难 | ⭐⭐⭐⭐ | 深入掌握 |
| 专家 | ⭐⭐⭐⭐⭐ | 高级应用 |

## 知识分类

- **基础概念**: Kubernetes核心概念
- **Pod**: Pod相关知识和操作
- **Deployment**: 部署管理
- **Service**: 服务发现
- **ConfigMap**: 配置管理
- **Secret**: 敏感数据管理
- **存储**: PV/PVC/StorageClass
- **网络**: 网络策略、Ingress
- **安全**: RBAC、安全策略
- **调度**: 资源配额、亲和性
- **监控**: 日志、指标、追踪
- **故障排查**: 调试技巧
- **Helm**: 包管理
- **集群管理**: 集群运维

## 题目导入

### ZIP包导入

支持批量导入Markdown格式的题目。

#### 创建题目文件

**YAML Frontmatter 格式（推荐）**：

```markdown
---
id: q001
type: single_choice
difficulty: 1
category: pod
question: Kubernetes中最小的部署单元是什么？
options:
  - A. Node
  - B. Pod
  - C. Container
  - D. Cluster
answer: B
explanation: Pod是Kubernetes中最小的部署单元
tags:
  - 基础
  - 概念
related_commands:
  - kubectl get pods
---
```

**标记格式**：

```markdown
[单选][简单][Pod]

题目内容？

A. 选项1
B. 选项2

答案：B

解析：这是解析内容
```

#### 打包ZIP

```bash
zip -r my_questions.zip *.md
```

#### 导入游戏

```python
from kugame.question_bank import QuestionBank
from kugame.question_import import import_questions_from_zip

bank = QuestionBank()
result = import_questions_from_zip(bank, "my_questions.zip")

print(f"导入成功: {result['imported']} 题")
print(f"跳过重复: {result['skipped']} 题")
```

## API接口

### 获取随机题目

```python
from kugame.question_bank import QuestionBank, QuestionDifficulty

bank = QuestionBank()

# 随机获取一道题
q = bank.get_random_question()

# 按条件筛选
q = bank.get_random_question(
    difficulty=QuestionDifficulty.中等,
    category=K8sCategory.Pod
)
```

### 生成练习卷

```python
# 生成10道题的练习卷
quiz = bank.generate_quiz(num_questions=10)

# 指定难度分布
quiz = bank.generate_quiz(
    num_questions=10,
    difficulties=[QuestionDifficulty.简单, QuestionDifficulty.中等]
)
```

### 检查答案

```python
# 获取题目
q = bank.get_question("q001")

# 检查答案
is_correct, feedback = q.check_answer("B")
print(feedback)  # 包含解析
```

### 搜索题目

```python
# 按关键词搜索
results = bank.search_questions("Pod")

# 按分类获取
questions = bank.get_questions(
    category=K8sCategory.Deployment,
    difficulty=QuestionDifficulty.中等,
    limit=20
)
```

## 题目格式规范

### 字段说明

| 字段 | 必填 | 说明 |
|------|------|------|
| id | ✓ | 唯一标识 |
| type | ✓ | 题目类型 |
| question | ✓ | 题目内容 |
| answer | ✓ | 正确答案 |
| difficulty | | 难度 (1-5) |
| category | | 知识分类 |
| options | | 选项列表（选择题） |
| explanation | | 解析 |
| tags | | 标签列表 |
| related_commands | | 相关命令 |

### 题型特定格式

**多选题答案格式**：
```yaml
answer: ["A", "B", "C"]  # 或 "A,B,C"
```

**填空题多答案**：
```yaml
answer:
  - "get"
  - "list"
```

**判断题答案**：
```yaml
answer: "True"  # 或 "False"
```

## 示例题目

### 单选题
```markdown
---
id: example_001
type: single_choice
difficulty: 1
category: pod
question: 查看所有Pod的命令是什么？
options:
  - A. kubectl get nodes
  - B. kubectl get pods
  - C. kubectl list pods
  - D. kubectl show pods
answer: B
explanation: kubectl get pods 是标准命令
---
```

### 多选题
```markdown
---
id: example_002
type: multiple_choice
difficulty: 3
category: deployment
question: Deployment可以实现哪些功能？
options:
  - A. 滚动更新
  - B. 自动扩缩容
  - C. 服务发现
  - D. 版本回滚
answer: ["A", "B", "D"]
explanation: 服务发现是Service的功能
---
```

### 判断题
```markdown
---
id: example_003
type: true_false
difficulty: 2
category: configmap
question: ConfigMap适合存储密码
answer: "False"
explanation: 敏感数据应该使用Secret
---
```

## 导入预览

在正式导入前可以预览ZIP包内容：

```python
from kugame.question_import import preview_zip_contents

preview = preview_zip_contents("questions.zip")
print(f"包含 {preview['md_files']} 个题目文件")
for p in preview['previews']:
    print(f"- {p['filename']}")
    print(f"  {p['preview'][:100]}...")
```

## 题库统计

```python
stats = bank.get_statistics()
print(f"总题数: {stats['total_questions']}")
print(f"按题型: {stats['by_type']}")
print(f"按难度: {stats['by_difficulty']}")
print(f"按分类: {stats['by_category']}")
```

## 导入示例

参考 `examples/questions/` 目录中的示例文件：

- `q001_pod_basics.md` - YAML格式单选题
- `q002_deployment.md` - 标记格式多选题
- `q003_command_fill.md` - 填空题
- `q004_configmap.md` - 判断题
- `q005_logs.md` - 命令补全
- `q006_interview.md` - 简答题
