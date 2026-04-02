# Kubernetes题库导入示例

这个目录包含示例题目文件，展示如何创建符合规范的Kubernetes题目。

## 文件格式

支持两种格式：

### 1. YAML Frontmatter 格式（推荐）

```markdown
---
id: q001
type: single_choice
difficulty: 1
category: pod
question: 题目内容
options:
  - A. 选项1
  - B. 选项2
  - C. 选项3
  - D. 选项4
answer: B
explanation: 解析内容
tags:
  - 标签1
  - 标签2
related_commands:
  - kubectl get pods
---

# 正文（可选）
更多说明内容...
```

### 2. 标记格式

```markdown
[单选][中等][Pod]

题目内容？

A. 选项A
B. 选项B
C. 选项C
D. 选项D

答案：B

解析：这是解析内容。

标签：标签1, 标签2
```

## 字段说明

### 必填字段

- `id`: 题目唯一标识
- `type`: 题目类型
  - `single_choice` - 单选题
  - `multiple_choice` - 多选题
  - `fill_blank` - 填空题
  - `true_false` - 判断题
  - `short_answer` - 简答题
  - `command_complete` - 命令补全
- `question`: 题目内容
- `answer`: 正确答案

### 可选字段

- `difficulty`: 难度 (1-5)
  - 1: 入门
  - 2: 简单
  - 3: 中等
  - 4: 困难
  - 5: 专家
- `category`: 分类
  - concepts, pod, deployment, service
  - configmap, secret, storage, network
  - security, scheduling, monitoring
  - troubleshooting, helm, cluster
- `options`: 选项列表（选择题）
- `explanation`: 解析
- `tags`: 标签列表
- `related_commands`: 相关命令列表

## 创建ZIP包

将多个MD文件打包成ZIP：

```bash
# Linux/Mac
zip -r my_questions.zip *.md

# Windows
# 选中文件 -> 右键 -> 发送到 -> 压缩文件夹
```

## 导入题库

在KuGame中使用命令导入：

```
主菜单 -> 题库管理 -> 导入题库 -> 选择ZIP文件
```

## 示例文件说明

| 文件 | 题型 | 说明 |
|------|------|------|
| q001_pod_basics.md | 单选题 | YAML格式，基础概念 |
| q002_deployment.md | 多选题 | 标记格式，功能考察 |
| q003_command_fill.md | 填空题 | YAML格式，命令补全 |
| q004_configmap.md | 判断题 | 标记格式，安全配置 |
| q005_logs.md | 命令补全 | YAML格式，日志排查 |
| q006_interview.md | 简答题 | YAML格式，面试题 |

## 注意事项

1. ID必须唯一，建议使用 `qXXX` 格式
2. 文件编码必须是UTF-8
3. 图片暂时不支持，请使用文字描述
4. 代码块使用 ```bash 标记
5. 多选题答案可以是 "A,B,C" 或 "ABC" 格式
