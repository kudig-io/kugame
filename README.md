# KuGame - 游戏化学习Kubernetes

<div align="center">

![KuGame Logo](https://img.shields.io/badge/KuGame-v2.0.0-blue?style=for-the-badge)
![Python Version](https://img.shields.io/badge/Python-3.8+-green?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)
![Tests](https://img.shields.io/badge/Tests-179%20Passed-brightgreen?style=for-the-badge)
![Web Version](https://img.shields.io/badge/Web%20Version-Available-purple?style=for-the-badge)

**🎮 CLI + 🌐 Web 双版本支持**

</div>

## 📖 项目简介

KuGame是一款创新的游戏化学习工具，通过武侠故事的方式帮助开发者和运维工程师学习和掌握Kubernetes命令行工具（kubectl）。在这个独特的修仙世界中，您将扮演一位初入青云宗的侠客，通过完成各种挑战和任务，逐步掌握Kubernetes的核心命令，最终飞升大成，成为一代宗师。

传统的Kubernetes学习往往枯燥乏味，命令繁多且难以记忆。KuGame将复杂的命令行操作融入精彩的武侠叙事中，让学习过程变得生动有趣。每一位使用者都可以在熟悉的江湖故事背景下，轻松愉快地掌握kubectl的各种命令，实现从「凡人」到「金仙」的修炼之路。

### 🌐 Web 版本全新上线

KuGame 现在提供 **Web 版本**！无需安装，打开浏览器即可开始您的 Kubernetes 修仙之旅：

- **现代 UI/UX**：基于 Tailwind CSS 的精美界面，支持暗黑主题
- **实时同步**：WebSocket 实时同步游戏状态
- **响应式设计**：支持桌面和移动设备
- **零安装**：直接在浏览器中运行

👉 [查看 Web 版本详情](#-web-版本)

## 📚 文档

- [玩家指南](docs/player-guide.md) - 新玩家入门教程
- [系统架构](docs/architecture.md) - 技术架构设计
- [开发指南](docs/development.md) - 开发规范与扩展指南
- [系统文档](docs/README.md) - 各系统详细文档
- [Web 版本文档](web/README.md) - Web 版本开发指南

## 🎮 项目特色

### 双版本支持
| 特性 | CLI 版本 | Web 版本 |
|-----|---------|---------|
| 界面类型 | 终端 ASCII 艺术 | 现代 Web UI |
| 安装方式 | pip 安装 | 浏览器直接访问 |
| 实时同步 | ❌ | ✅ WebSocket |
| 响应式设计 | ❌ | ✅ 支持移动端 |
| 主题切换 | ❌ | ✅ 暗黑/明亮模式 |
| 离线支持 | ✅ | ❌ |

### 故事驱动的学习体验
KuGame不再是将命令简单地罗列展示，而是将其编织成一个完整的武侠故事。从踏入青云宗山门开始，您将经历各种冒险和挑战，在解决实际问题的过程中自然而然地掌握命令。每个章节都有精心设计的故事背景和对应的ASCII艺术图片，将命令的功能与故事情节、视觉元素紧密结合。

### 完整的修炼体系
游戏内置了完整的修炼境界系统，从「凡人」到「金仙」共十个境界。玩家通过学习和实践获得经验值，提升等级，解锁新的修炼境界。这种gamification的设计让学习过程充满动力和成就感。

### 丰富的命令覆盖
KuGame涵盖了**90+个**常用的Kubernetes命令，涵盖**12个功能分类**：基础操作、部署管理、服务发现、配置管理、存储管理、资源管理、故障排查、进阶操作、集群管理、网络管理、安全管理、工具命令。每个命令都有详细的说明、语法示例和实际应用场景。

### 多样化的练习模式
- **故事模式**：跟随武侠剧情学习新命令
- **挑战模式**：完成各种挑战任务，检验学习成果，支持连击系统让收益倍增
- **测验模式**：进行知识测验，测试对Kubernetes命令的掌握程度
- **纯粹答题模式**：专注于命令练习，支持「全部命令」和「错题集」两种学习方式

### 装备与道具系统
- **装备类型**：武器（攻击）、护甲（防御）、饰品（特殊效果）
- **品质等级**：普通(白) → 精良(绿) → 稀有(蓝) → 史诗(紫) → 传说(橙)
- **获取途径**：战斗掉落、挑战奖励、商店购买、装备强化

### 门派技能与天赋系统
- **门派技能**：每个门派拥有3个独特技能，战斗中可使用
  - 青云宗：稳如泰山、道法自然、以柔克刚
  - 炼狱门：狂暴、嗜血、不屈
  - 玄天宗：变化莫测、天机洞察、乾坤挪移
  - 逍遥派：逍遥游、因材施教、随性而为
- **天赋树**：每个门派独立的天赋树，升级获得天赋点，自由分配

### 副本与挑战塔系统
- **无尽挑战塔**：100层挑战塔，每层难度递增，奖励丰厚
- **每日副本**：每日刷新，包括经验副本、装备副本、极限挑战
- **体力系统**：合理分配体力，挑战不同副本

### 每日签到系统
- **连续签到奖励**：连续签到天数越多，奖励越丰厚
- **周/月额外奖励**：7天、14天、30天里程碑奖励
- **奖励内容**：经验值、体力、装备等
- **断签重置**：断签后连续天数重置，鼓励每日学习

### 任务系统
- **每日任务**：每天3个随机任务，完成获得经验、体力等奖励
- **每周任务**：每周2个高难度任务，奖励更丰厚
- **主线任务**：7个章节任务，推进剧情发展
- **支线任务**：5个特色任务，探索游戏深度

### 装备套装系统
- **8大套装**：新手、青云、炼狱、玄天、逍遥、龙鳞、凤羽、混元
- **套装加成**：2/3/4/5件套激活不同属性加成
- **收集进度**：查看套装收集进度和缺失部件

### 宝石系统
- **6种宝石**：攻击、防御、生命、经验、连击、暴击
- **5级品质**：普通、精良、稀有、史诗、传说
- **宝石合成**：相同宝石可合成升级
- **镶嵌系统**：装备镶嵌宝石获得属性提升

### 排行榜系统
- **多维度排名**：经验、等级、成就、挑战塔、战斗胜率
- **实时更新**：数据实时同步，公平竞争
- **个人排名**：查看自己的全服排名

### PVP竞技场
- **异步对战**：与玩家镜像或AI对手战斗
- **段位系统**：青铜→白银→黄金→铂金→钻石→大师→王者
- **赛季制**：每月一个赛季，赛季结束结算奖励
- **积分系统**：ELO算法，连胜有额外加成
- **排名榜**：查看竞技场排名和战斗历史

### 事件链系统
- **事件链**：炼丹奇遇、古墓探险、仙人指点等连续事件
- **多分支选择**：不同选择导致不同结果
- **稀有事件**：根据玩家等级触发不同稀有度事件

### 宠物系统
- **5种宠物**：灵狐、烈焰虎、玄铁龟、雷霆雕、碧玉龙
- **6种稀有度**：普通→稀有→精良→史诗→传说→神话
- **4种类型**：攻击型、防御型、辅助型、平衡型
- **培养系统**：喂食、玩耍、训练提升属性
- **进化系统**：20/40/60级可进化，大幅提升能力
- **宠物技能**：每只宠物拥有独特技能，战斗中可使用

### 题库系统
- **6种题型**：单选、多选、填空、判断、简答、命令补全
- **5级难度**：入门、简单、中等、困难、专家
- **14个分类**：基础概念、Pod、Deployment、Service、ConfigMap等
- **题目导入**：支持ZIP包导入，自动解析Markdown文件
- **智能练习**：根据难度和分类生成练习卷
- **答案解析**：每道题都有详细解析和相关命令

### 战斗系统
创新性地将命令学习融入回合制战斗，玩家需要回答Kubernetes命令题来攻击怪物，增强学习趣味性和挑战性。

### 存档管理系统
完整的存档管理功能，包括自定义存档名称、存档列表查看、加载指定存档、删除存档、重命名存档。

### 成就系统
内置**26个成就**，涵盖10个维度，激励玩家持续学习和探索：

| 成就类型 | 数量 | 说明 |
|---------|------|------|
| 📚 命令掌握 | 4个 | 掌握10/30/50/全部命令 |
| 📖 故事进度 | 3个 | 完成第3/6/9章 |
| 🏆 挑战完成 | 2个 | 完成10/50个挑战 |
| 🔥 连续成功 | 3个 | 连续答对5/10/20次 |
| 🎒 收集成就 | 3个 | 收集10/50件装备、获得传说装备 |
| ⬆️ 等级成就 | 4个 | 达到10/30/50/100级 |
| 🏰 挑战塔成就 | 3个 | 达到10/50/100层 |
| ⚔️ 战斗成就 | 2个 | 参加100场/获胜50场战斗 |
| ⭐ 特殊成就 | 2个 | 首次登录、完美答题10道 |

每个成就都有独特的称号奖励和经验值奖励，完成全部成就可获得超过**50,000经验值**！

## 🚀 快速开始

### CLI 版本

#### 环境要求

- Python 3.8或更高版本
- pip包管理器
- 建议4GB以上内存
- 100MB以上磁盘空间

#### 安装方法

**方式一：使用pip安装（推荐）**

```bash
pip install kugame
```

**方式二：从源码安装**

```bash
# 克隆项目仓库
git clone https://github.com/yourusername/kugame.git
cd kugame

# 安装项目
pip install -e .
```

**方式三：使用pipx安装**

```bash
pipx install kugame
```

#### 启动游戏

```bash
kugame
```

或者，如果您从源码安装：

```bash
python -m kugame.cli
```

---

## 🌐 Web 版本

KuGame Web 版本使用 **FastAPI** 后端 + **Vanilla JavaScript** 前端构建，提供现代化的游戏体验。

### 技术栈

| 层级 | 技术 | 说明 |
|-----|-----|-----|
| 后端 | FastAPI | 高性能 Python Web 框架 |
| 后端 | WebSocket | 实时双向通信 |
| 后端 | Uvicorn | ASGI 服务器 |
| 前端 | Vanilla JS | 原生 JavaScript (ES6+) |
| 前端 | Tailwind CSS | 实用优先的 CSS 框架 |
| 前端 | Font Awesome | 图标库 |

### 项目结构

```
web/
├── backend/              # FastAPI 后端
│   ├── api/             # API 路由
│   │   ├── player.py       # 玩家 API
│   │   ├── game.py         # 游戏逻辑 API
│   │   ├── combat.py       # 战斗系统 API
│   │   ├── shop.py         # 商店 API
│   │   ├── inventory.py    # 背包 API
│   │   └── k8s.py          # K8s 学习 API
│   ├── main.py          # 应用入口
│   └── requirements.txt # 依赖列表
│
└── frontend/            # 前端应用
    ├── index.html       # 主页面
    ├── src/
    │   ├── main.js          # 应用入口
    │   ├── components/ui/   # UI 组件
    │   │   ├── Button.js
    │   │   ├── Card.js
    │   │   ├── Progress.js
    │   │   └── Toast.js
    │   ├── pages/          # 页面组件
    │   │   ├── Login.js    # 登录/创建角色
    │   │   ├── Layout.js   # 主布局
    │   │   └── Dashboard.js # 概览页
    │   ├── lib/            # 工具库
    │   │   ├── api.js      # API 客户端
    │   │   ├── store.js    # 状态管理
    │   │   └── utils.js    # 通用工具
    │   └── styles/         # 样式文件
    │       ├── variables.css
    │       ├── globals.css
    │       └── animations.css
    └── package.json
```

### API 端点

#### 玩家 (Player)
- `GET /api/player` - 获取玩家信息
- `POST /api/player/create` - 创建角色
- `GET /api/player/stats` - 获取统计数据

#### 游戏 (Game)
- `POST /api/game/explore` - 探索世界
- `POST /api/game/cultivate` - 修炼
- `POST /api/game/rest` - 休息恢复
- `GET /api/game/locations` - 获取地点列表

#### 战斗 (Combat)
- `POST /api/combat/start` - 开始战斗
- `POST /api/combat/action` - 执行战斗动作
- `GET /api/combat/enemies` - 获取敌人列表
- `GET /api/combat/skills` - 获取技能列表

#### 商店 (Shop)
- `GET /api/shop/items` - 获取商品列表
- `POST /api/shop/buy` - 购买物品
- `POST /api/shop/sell` - 出售物品

#### K8s 学习
- `GET /api/k8s/levels` - 获取学习关卡
- `POST /api/k8s/execute` - 执行 K8s 命令（模拟）
- `GET /api/k8s/cluster` - 获取集群状态

#### WebSocket
- `WS /ws/player` - 实时玩家更新

### 启动 Web 版本

**一键启动（推荐）**

```bash
cd web
./start.sh
```

**分别启动**

```bash
# 终端 1：启动后端
cd web/backend
pip install -r requirements.txt
python main.py
# 后端运行在 http://localhost:8000

# 终端 2：启动前端
cd web/frontend
python -m http.server 3000
# 前端运行在 http://localhost:3000
```

### 设计特色

- **🎨 修仙主题 UI**：暗黑模式 + 霓虹发光效果 + 渐变文字
- **✨ 动画效果**：淡入、滑动、浮动、脉冲等多种动画
- **🃏 玻璃态效果**：半透明面板 + 模糊背景
- **📱 响应式布局**：适配桌面和移动设备
- **🔔 实时通知**：Toast 通知系统

---

## 📚 使用指南

### 创建角色

首次启动游戏时，您需要创建一个角色。您可以选择自己的侠名和所属门派。KuGame提供了四个独特的门派供您选择：

| 门派 | 特色 | 加成 |
|-----|------|------|
| **青云宗** | 正道第一大宗，擅长创建和管理稳定的应用部署 | 经验+10% |
| **玄天宗** | 以玄妙变化著称，擅长服务发现和网络配置 | 基础平衡 |
| **炼狱门** | 以实战著称，专注于故障排查和性能优化 | 经验+20% |
| **逍遥派** | 以逍遥自在为理念，擅长配置管理和存储管理 | 经验+15% |

选择完毕后，您将踏入修仙之旅，开始学习Kubernetes之道。

### 主菜单功能

| 选项 | 功能描述 |
|-----|------|
| 📖 开始故事 | 继续阅读故事章节，学习新的Kubernetes命令 |
| ⚔️ 修炼场 | 在已学命令中进行自由练习，巩固所学知识 |
| 🏆 挑战关卡 | 完成各种挑战任务，检验学习成果，有连击系统让收益倍增 |
| 📝 知识问答 | 进行知识测验，测试您对Kubernetes命令的掌握程度 |
| 📊 修炼进度 | 查看当前的学习进度，包括等级、境界、命令掌握情况等 |
| 📚 命令手册 | 查看所有kubectl命令的详细说明和示例，随时查阅 |
| 🎒 装备管理 | 查看、装备、卸下装备，强化装备属性 |
| 🏪 仙缘商店 | 购买装备、道具，强化装备 |
| ⚡ 门派技能 | 查看技能、使用技能、管理天赋树 |
| 🏰 副本挑战 | 进入每日副本、挑战无尽之塔 |
| 💾 保存进度 | 手动保存当前游戏进度，确保学习成果不会丢失 |
| 📁 档案管理 | 管理游戏存档，包括创建、加载、删除和重命名存档 |
| 🚪 退出游戏 | 安全退出游戏，您的进度会自动保存 |

### 修炼境界系统

| 境界 | 等级范围 | 描述 | 解锁功能 |
|-----|---------|------|---------|
| 凡人 | 1-10 | 凡人之躯，初入仙门 | 基础功能 |
| 练气期 | 11-20 | 初步入门，感知灵气 | 技能系统 |
| 筑基期 | 21-30 | 根基稳固，道法初成 | 天赋树开启 |
| 金丹期 | 31-40 | 金丹大道，修为精进 | 装备强化 |
| 元婴期 | 41-50 | 元婴初成，神识通明 | 高级副本 |
| 化神期 | 51-60 | 化神飞升，神通广大 | 精英副本 |
| 大乘期 | 61-70 | 大乘圆满，道法自然 | 传说装备 |
| 渡劫期 | 71-80 | 渡劫飞升，历经磨难 | 极限挑战 |
| 散仙 | 81-90 | 逍遥天地，无拘无束 | 全副本解锁 |
| 金仙 | 91-100 | 金仙不朽，万古长存 | 无尽之塔顶层 |

## 🏔️ 故事章节

| 章节 | 标题 | 核心内容 | 解锁命令 |
|-----|------|---------|---------|
| 序章 | 踏入仙门 | 容器基础 | kubectl run、get pods |
| 第一章 | 容器之道 | Deployment管理 | create deployment、scale |
| 第二章 | 服务之门 | Service服务发现 | expose、get services |
| 第三章 | 配置之密 | ConfigMap和Secret | create configmap/secret |
| 第四章 | 存储之道 | PersistentVolume | get pv/pvc、apply |
| 第五章 | 调度之学 | 资源配额、节点管理 | top、label node |
| 第六章 | 故障排查 | 日志查看、容器调试 | logs、exec、port-forward |
| 第七章 | 进阶之道 | YAML配置、版本回滚 | patch、rollout undo |
| 第八章 | 网络与安全 | 网络策略、RBAC权限 | networkpolicies、roles |
| 第九章 | 集群管理 | 集群信息查看、API资源 | cluster-info、api-resources |
| 第十章 | 云厂商管理 | 阿里云、腾讯云等管理命令 | aliyun、tke、cce |
| 第十一章 | 云厂商高级特性 | 云厂商特有扩展功能 | 高级管理命令 |
| 终章 | 飞升大成 | 最终考验 | 全部命令综合运用 |

## 📋 命令覆盖

KuGame涵盖了以下12个分类的Kubernetes命令：

### 1. 基础操作命令 ⭐
| 命令 | 功能描述 |
|-----|---------|
| `kubectl run` | 创建并运行一个Pod |
| `kubectl get pods` | 列出所有Pod |
| `kubectl describe pod` | 显示Pod的详细信息 |
| `kubectl delete pod` | 删除Pod |
| `kubectl get all` | 列出所有资源 |
| `kubectl delete all` | 删除所有资源 |

### 2. 部署管理命令 ⭐⭐
| 命令 | 功能描述 |
|-----|---------|
| `kubectl create deployment` | 创建一个Deployment |
| `kubectl scale` | 扩缩容Deployment副本数 |
| `kubectl get deployments` | 列出所有Deployment |
| `kubectl rollout status` | 查看滚动更新状态 |
| `kubectl describe deployment` | 显示Deployment的详细信息 |
| `kubectl delete deployment` | 删除Deployment |

### 3. 服务发现命令 ⭐⭐
| 命令 | 功能描述 |
|-----|---------|
| `kubectl expose` | 为Pod或Deployment创建Service |
| `kubectl get services` | 列出所有Service |
| `kubectl describe service` | 显示Service的详细信息 |
| `kubectl delete service` | 删除Service |
| `kubectl get endpoints` | 列出所有Endpoints |

### 4. 配置管理命令 ⭐⭐
| 命令 | 功能描述 |
|-----|---------|
| `kubectl create configmap` | 创建ConfigMap |
| `kubectl create secret` | 创建Secret |
| `kubectl get configmaps` | 列出所有ConfigMap |
| `kubectl get secrets` | 列出所有Secret |
| `kubectl describe configmap` | 显示ConfigMap详情 |
| `kubectl delete configmap` | 删除ConfigMap |
| `kubectl delete secret` | 删除Secret |

### 5. 存储管理命令 ⭐⭐⭐
| 命令 | 功能描述 |
|-----|---------|
| `kubectl get pv` | 列出所有PersistentVolume |
| `kubectl get pvc` | 列出所有PersistentVolumeClaim |
| `kubectl apply` | 从YAML文件创建或更新资源 |
| `kubectl delete pvc` | 删除PersistentVolumeClaim |
| `kubectl get storageclasses` | 列出所有StorageClass |
| `kubectl delete pv` | 删除PersistentVolume |

### 6. 资源管理命令 ⭐⭐⭐
| 命令 | 功能描述 |
|-----|---------|
| `kubectl top` | 查看资源使用情况 |
| `kubectl top node` | 查看节点资源使用情况 |
| `kubectl describe node` | 显示Node的详细信息 |
| `kubectl label node` | 为Node添加标签 |
| `kubectl taint node` | 为Node添加污点 |
| `kubectl untaint node` | 移除Node的污点 |
| `kubectl get nodes` | 列出所有Node |
| `kubectl cordon node` | 标记节点为不可调度 |
| `kubectl uncordon node` | 标记节点为可调度 |
| `kubectl drain node` | 驱逐节点上的所有Pod |
| `kubectl cp` | 在本地和Pod之间复制文件 |
| `kubectl annotate` | 为资源添加注解 |

### 7. 故障排查命令 ⭐⭐⭐
| 命令 | 功能描述 |
|-----|---------|
| `kubectl logs` | 查看Pod的日志 |
| `kubectl logs -f` | 实时查看Pod日志 |
| `kubectl exec` | 在Pod中执行命令 |
| `kubectl port-forward` | 本地端口转发到Pod |
| `kubectl events` | 查看集群事件 |
| `kubectl get events` | 列出所有事件 |
| `kubectl debug` | 调试Pod |

### 8. 进阶操作命令 ⭐⭐⭐⭐
| 命令 | 功能描述 |
|-----|---------|
| `kubectl patch` | 更新资源的字段 |
| `kubectl set image` | 更新容器镜像 |
| `kubectl rollout undo` | 回滚Deployment到上一版本 |
| `kubectl rollout history` | 查看Deployment版本历史 |
| `kubectl replace` | 替换资源 |
| `kubectl edit` | 编辑资源 |

### 9. 集群管理命令 ⭐⭐⭐⭐
| 命令 | 功能描述 |
|-----|---------|
| `kubectl auth can-i` | 检查当前用户的权限 |
| `kubectl config view` | 显示kubeconfig配置 |
| `kubectl cluster-info` | 显示集群信息 |
| `kubectl api-resources` | 列出所有可用的API资源 |

### 10. 网络管理命令 ⭐⭐⭐⭐
| 命令 | 功能描述 |
|-----|---------|
| `kubectl get networkpolicies` | 列出所有网络策略 |
| `kubectl describe networkpolicy` | 显示网络策略的详细信息 |
| `kubectl create networkpolicy` | 创建网络策略 |
| `kubectl delete networkpolicy` | 删除网络策略 |
| `kubectl get ingress` | 列出所有Ingress资源 |
| `kubectl describe ingress` | 显示Ingress的详细信息 |
| `kubectl delete ingress` | 删除Ingress资源 |

### 11. 安全管理命令 ⭐⭐⭐⭐⭐
| 命令 | 功能描述 |
|-----|---------|
| `kubectl get roles` | 列出所有Role |
| `kubectl get rolebindings` | 列出所有RoleBinding |
| `kubectl get clusterroles` | 列出所有ClusterRole |
| `kubectl get clusterrolebindings` | 列出所有ClusterRoleBinding |
| `kubectl create role` | 创建Role |
| `kubectl create rolebinding` | 创建RoleBinding |
| `kubectl create secret generic` | 从文件或字面量创建Secret |
| `kubectl create secret docker-registry` | 创建Docker Registry认证Secret |
| `kubectl describe secret` | 显示Secret的详细信息 |
| `kubectl get serviceaccounts` | 列出所有ServiceAccount |
| `kubectl describe serviceaccount` | 显示ServiceAccount的详细信息 |

### 12. 工具命令 ⭐⭐
| 命令 | 功能描述 |
|-----|---------|
| `kubectl completion` | 生成shell补全脚本 |
| `kubectl version` | 显示kubectl版本信息 |
| `kubectl plugin list` | 列出所有kubectl插件 |

## 📊 项目统计

| 指标 | CLI 版本 | Web 版本 | 总计 |
|-----|---------|---------|-----|
| **代码行数** | 20,000+ | 3,000+ | 23,000+ |
| **测试数量** | 179+ | - | 179+ |
| **测试覆盖率** | 85%+ | - | 85%+ |
| **API 端点** | - | 35+ | 35+ |
| **WebSocket 路由** | - | 1 | 1 |
| **UI 组件** | - | 4+ | 4+ |
| **页面数量** | - | 3+ | 3+ |
| **成就数量** | 26 | 26 | 26 |
| **任务数量** | 20+ | 20+ | 20+ |
| **装备套装** | 8 | 8 | 8 |
| **宝石类型** | 6 | 6 | 6 |
| **事件链** | 3 | 3 | 3 |
| **竞技场段位** | 7 | 7 | 7 |
| **宠物种类** | 5 | 5 | 5 |
| **题库题型** | 6 | 6 | 6 |
| **题目数量** | 200+ | 200+ | 200+ |
| **命令覆盖** | 90+ | 90+ | 90+ |
| **故事章节** | 13 | 13 | 13 |
| **装备品质** | 5 | 5 | 5 |
| **门派数量** | 4 | 4 | 4 |
| **技能数量** | 12 | 12 | 12 |
| **挑战塔层数** | 100 | 100 | 100 |
| **随机事件** | 15+ | 15+ | 15+ |

## 🛠️ 开发指南

### 项目结构

```
kugame/
├── kugame/                    # CLI 主包目录
│   ├── __init__.py           # 包初始化
│   ├── cli.py                # 命令行界面（1700+行）
│   ├── player.py             # 玩家角色系统（1600+行）
│   ├── story.py              # 故事管理器（450+行）
│   ├── kubernetes_commands.py # 命令管理器（1000+行）
│   ├── game_engine.py        # 游戏引擎（1200+行）
│   ├── equipment.py          # 装备系统
│   ├── skills.py             # 技能系统
│   ├── talent_tree.py        # 天赋系统
│   ├── dungeon.py            # 副本系统
│   ├── tower.py              # 挑战塔系统
│   ├── daily_checkin.py      # 每日签到系统
│   └── save_manager.py       # 存档管理系统
│
├── web/                       # 🌐 Web 版本
│   ├── backend/              # FastAPI 后端
│   │   ├── api/              # API 路由
│   │   ├── main.py           # 后端入口
│   │   └── requirements.txt  # 后端依赖
│   ├── frontend/             # 前端应用
│   │   ├── index.html        # 主页面
│   │   ├── src/              # 源代码
│   │   │   ├── components/ui/ # UI 组件
│   │   │   ├── pages/        # 页面组件
│   │   │   ├── lib/          # 工具库
│   │   │   └── styles/       # 样式文件
│   │   └── package.json
│   ├── README.md             # Web 版本文档
│   └── start.sh              # 一键启动脚本
│
├── tests/                    # 测试目录
│   ├── test_player.py        # 玩家系统测试
│   ├── test_story.py         # 故事管理器测试
│   ├── test_kubernetes_commands.py
│   ├── test_game_engine.py
│   ├── test_equipment.py
│   ├── test_skills.py
│   ├── test_dungeon.py
│   ├── test_checkin.py       # 签到系统测试
│   └── test_achievements_extended.py # 成就系统测试
│
├── docs/                     # 文档目录
│   ├── systems/              # 系统详细文档
│   │   ├── achievement-system.md
│   │   ├── equipment.md
│   │   ├── skills.md
│   │   ├── talent_tree.md
│   │   ├── dungeon.md
│   │   └── tower.md
│   ├── architecture.md
│   ├── player-guide.md
│   └── development.md
│
├── pyproject.toml
└── README.md                 # 本文档
```

### 运行测试

KuGame项目包含完整的测试套件，使用pytest框架编写。

**方法一：使用一键测试脚本（Windows）**

```bash
.\test.bat
```

**方法二：手动运行测试命令**

```bash
# 运行所有测试
pytest tests/ -v

# 运行并生成覆盖率报告
pytest tests/ --cov=kugame --cov-report=html

# 运行指定测试文件
pytest tests/test_player.py -v

# 运行指定测试用例
pytest tests/test_player.py::TestPlayer::test_level_up -v

# 运行mypy类型检查
python -m mypy kugame/
```

### 代码规范

KuGame项目遵循以下代码规范：

- 使用Python 3.8+的新特性
- 遵循PEP 8代码风格指南
- 使用类型提示（Type Hints）增强代码可读性
- 所有公共函数和类都有docstring文档
- 使用black进行代码格式化（行长度100）
- 使用mypy进行类型检查

### 添加新命令

如果您想为KuGame添加新的kubectl命令，请按照以下步骤操作：

1. 在`kubernetes_commands.py`中的`_initialize_commands`方法里添加新的`KubectlCommand`实例
2. 在`story.py`中找到对应的章节，在`commands_to_learn`列表中添加命令名
3. 编写对应的测试用例
4. 更新README文档中的命令速查表

### Web 版本开发

**添加新 API 端点**

```python
# web/backend/api/your_module.py
from fastapi import APIRouter

router = APIRouter(prefix="/api/your-module", tags=["your-module"])

@router.get("/items")
async def get_items():
    return {"status": "success", "data": []}
```

然后在 `web/backend/main.py` 中注册路由。

**添加新页面**

```javascript
// web/frontend/src/pages/YourPage.js
export class YourPage {
  render() {
    return `<div>Your Page Content</div>`;
  }
  
  mount(container) {
    container.innerHTML = this.render();
  }
}
```

## 🤝 贡献指南

我们欢迎并感谢您对KuGame项目的贡献！无论是报告bug、提出新功能建议，还是直接贡献代码，我们都十分欢迎。

### 贡献方式

**报告bug**：如果您发现任何bug或问题，请通过GitHub Issues页面提交报告。

**提出建议**：如果您有好的想法或改进建议，请通过GitHub Discussions页面与我们分享。

**贡献代码**：

1. Fork本项目到您的GitHub账户
2. 创建一个新的分支进行您的修改
3. 确保您的代码符合项目的代码规范
4. 添加适当的测试用例
5. 提交Pull Request，等待代码审查

### 开发环境设置

```bash
# 克隆您的fork仓库
git clone https://github.com/YOUR_USERNAME/kugame.git
cd kugame

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/macOS
# 或
.\venv\Scripts\activate  # Windows

# 安装开发依赖
pip install -e ".[dev]"

# 运行代码检查
black kugame/
mypy kugame/

# 运行测试
pytest tests/ -v
```

## 📄 许可证

KuGame项目采用MIT许可证开源。

```
MIT License

Copyright (c) 2026 KuGame Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## 🙏 致谢

KuGame项目的诞生离不开以下开源项目和社区的支持：

- **Rich库**：为KuGame提供了美观且功能强大的终端输出能力
- **PyYAML**：用于处理YAML格式的Kubernetes配置文件
- **pytest**：为KuGame提供了完善的测试框架
- **FastAPI**：为Web版本提供了高性能的后端框架
- **Tailwind CSS**：为Web版本提供了精美的UI组件
- **Kubernetes社区**：创造了如此优秀的容器编排平台，让KuGame有了学习的目标

同时，也要感谢所有为KuGame项目贡献代码、报告bug和提出建议的开发者们。

## 📞 联系方式

如果您有任何问题或建议，欢迎通过以下方式联系我们：

- **GitHub Issues**：用于报告bug和提出功能建议
- **GitHub Discussions**：用于一般性讨论和问题解答
- **电子邮件**：kugame@example.com

## 🔮 未来规划

KuGame项目还在不断发展中，以下是未来版本的一些规划功能：

- [x] **Web界面版本**：✅ 已完成 - 提供基于浏览器的图形界面版本
- [ ] **更多故事章节**：增加更多有趣的故事章节，覆盖更多Kubernetes高级主题
- [ ] **多人模式**：支持多人协作学习，增加排行榜和竞技场功能
- [ ] **移动端适配**：开发移动应用程序
- [ ] **插件系统**：支持用户自定义故事和命令
- [ ] **AI辅助学习**：集成AI助手，提供个性化学习建议
- [ ] **云端存档**：Web 版本支持云端存档同步
- [ ] **社交功能**：好友系统、公会系统

---

<div align="center">

**愿你在Kubernetes之道上一帆风顺！**

*凡人之躯，终可问道苍穹。*

**[⬆ 回到顶部](#kugame---游戏化学习kubernetes)**

</div>
