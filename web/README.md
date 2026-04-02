# KuGame Web Version

<div align="center">

![KuGame Web](https://img.shields.io/badge/KuGame-Web-purple?style=for-the-badge)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)

**在浏览器中体验 Kubernetes 修仙之旅**

</div>

## ✨ 特性

- 🎮 **完整的修仙主题 UI** - 暗黑模式 + 霓虹发光效果 + 渐变文字
- 📡 **实时同步** - WebSocket 实时同步游戏状态
- 🎨 **现代设计** - Tailwind CSS 构建，玻璃态效果
- 📱 **响应式布局** - 支持桌面和移动设备
- 🔔 **实时通知** - Toast 通知系统
- ⚡ **高性能** - FastAPI 后端，异步处理

## 🏗️ 技术栈

### 后端
| 技术 | 版本 | 说明 |
|-----|-----|-----|
| FastAPI | 0.109+ | 高性能 Python Web 框架 |
| Uvicorn | 0.27+ | ASGI 服务器 |
| WebSocket | - | 实时双向通信 |
| Pydantic | 2.5+ | 数据验证 |

### 前端
| 技术 | 版本 | 说明 |
|-----|-----|-----|
| Vanilla JS | ES6+ | 原生 JavaScript |
| Tailwind CSS | 3.x | 实用优先的 CSS 框架 |
| Font Awesome | 6.4+ | 图标库 |
| Google Fonts | - | Noto Sans SC 中文字体 |

## 📁 项目结构

```
web/
├── backend/                  # FastAPI 后端
│   ├── api/                 # API 路由模块
│   │   ├── __init__.py
│   │   ├── player.py           # 玩家 API (创建、获取、更新)
│   │   ├── game.py             # 游戏逻辑 API (探索、修炼、休息)
│   │   ├── combat.py           # 战斗系统 API (开始战斗、执行动作)
│   │   ├── shop.py             # 商店 API (商品列表、购买、出售)
│   │   ├── inventory.py        # 背包 API (查看、使用、装备)
│   │   └── k8s.py              # K8s 学习 API (关卡、执行命令)
│   ├── core/                # 核心逻辑
│   ├── main.py              # FastAPI 应用入口
│   └── requirements.txt     # Python 依赖
│
├── frontend/                 # 前端应用
│   ├── index.html           # 主页面入口
│   ├── src/
│   │   ├── main.js              # 应用入口，路由管理
│   │   ├── components/          # UI 组件
│   │   │   └── ui/
│   │   │       ├── Button.js       # 按钮组件
│   │   │       ├── Card.js         # 卡片组件
│   │   │       ├── Progress.js     # 进度条组件
│   │   │       └── Toast.js        # 通知组件
│   │   ├── pages/               # 页面组件
│   │   │   ├── Login.js            # 登录/创建角色页
│   │   │   ├── Layout.js           # 主布局 (侧边栏 + 顶部栏)
│   │   │   └── Dashboard.js        # 概览仪表盘
│   │   ├── lib/                 # 工具库
│   │   │   ├── utils.js            # 通用工具函数
│   │   │   ├── api.js              # API 客户端
│   │   │   └── store.js            # 状态管理 + WebSocket
│   │   └── styles/              # 样式文件
│   │       ├── variables.css       # CSS 变量
│   │       ├── globals.css         # 全局样式
│   │       └── animations.css      # 动画效果
│   └── package.json         # 前端配置
│
├── start.sh                 # 一键启动脚本
└── README.md               # 本文档
```

## 🚀 快速开始

### 环境要求

- Python 3.8+
- pip 包管理器
- 现代浏览器 (Chrome/Firefox/Safari/Edge)

### 一键启动（推荐）

```bash
cd web
./start.sh
```

脚本会自动启动后端 (端口 8000) 和前端 (端口 3000)。

### 手动启动

**1. 安装后端依赖**

```bash
cd web/backend
pip install -r requirements.txt
```

**2. 启动后端服务器**

```bash
# 方式一：直接运行
python main.py

# 方式二：使用 uvicorn（推荐开发）
uvicorn main:app --reload --port 8000
```

后端服务将在 http://localhost:8000 运行

- API 文档: http://localhost:8000/docs
- OpenAPI Schema: http://localhost:8000/openapi.json

**3. 启动前端**

```bash
cd web/frontend

# Python 3
python -m http.server 3000

# 或 Node.js
npx serve .
```

前端将在 http://localhost:3000 运行

## 📡 API 端点

### 玩家 (Player)
```
GET    /api/player              # 获取当前玩家信息
POST   /api/player/create       # 创建新角色
GET    /api/player/stats        # 获取详细统计
POST   /api/player/update       # 更新玩家信息
```

### 游戏 (Game)
```
POST   /api/game/explore        # 探索世界
POST   /api/game/cultivate      # 修炼
POST   /api/game/rest           # 休息恢复
GET    /api/game/locations      # 获取可探索地点
GET    /api/game/events         # 获取随机事件
```

### 战斗 (Combat)
```
POST   /api/combat/start        # 开始战斗
POST   /api/combat/action       # 执行战斗动作
GET    /api/combat/enemies      # 获取敌人列表
GET    /api/combat/skills       # 获取技能列表
```

### 商店 (Shop)
```
GET    /api/shop/items          # 获取商品列表
POST   /api/shop/buy            # 购买物品
POST   /api/shop/sell           # 出售物品
GET    /api/shop/categories     # 获取商品分类
```

### 背包 (Inventory)
```
GET    /api/inventory           # 获取背包内容
POST   /api/inventory/use       # 使用物品
POST   /api/inventory/equip     # 装备物品
GET    /api/inventory/equipment # 获取已装备物品
```

### K8s 学习
```
GET    /api/k8s/levels          # 获取学习关卡
GET    /api/k8s/levels/{id}     # 获取特定关卡
POST   /api/k8s/execute         # 执行 K8s 命令（模拟）
GET    /api/k8s/cluster         # 获取集群状态
GET    /api/k8s/namespaces      # 获取命名空间
GET    /api/k8s/pods            # 获取 Pod 列表
GET    /api/k8s/nodes           # 获取节点列表
```

### WebSocket
```
WS     /ws/player              # 实时玩家更新
```

## 🎨 设计系统

### 颜色主题
```css
/* 主色调 */
--primary: #6366f1;        /* Indigo - 主要操作 */
--secondary: #8b5cf6;      /* Purple - 次要操作 */
--accent: #06b6d4;         /* Cyan - 强调色 */

/* 游戏专用 */
--hp-color: #ef4444;       /* 生命值 - 红色 */
--mp-color: #3b82f6;       /* 法力值 - 蓝色 */
--exp-color: #f59e0b;      /* 经验值 - 黄色 */

/* 境界颜色 */
--realm-qi: #9ca3af;       /* 练气期 */
--realm-foundation: #60a5fa; /* 筑基期 */
--realm-core: #a78bfa;     /* 金丹期 */
--realm-nascent: #f472b6;  /* 元婴期 */
--realm-spirit: #fbbf24;   /* 化神期 */
```

### 组件风格
- **Glassmorphism** - 玻璃态效果：`backdrop-filter: blur(16px)`
- **Neon Glow** - 霓虹发光：`box-shadow: 0 0 20px rgba(99, 102, 241, 0.5)`
- **Gradient Text** - 渐变文字
- **Smooth Animations** - 流畅动画：300ms ease

## 📦 开发计划

### ✅ 已完成
- [x] FastAPI 后端框架
- [x] 6 个 API 模块，35+ 端点
- [x] WebSocket 实时通信
- [x] 前端组件系统
- [x] 登录/创建角色页面
- [x] 主布局 (侧边栏 + 顶部栏)
- [x] Dashboard 概览页
- [x] 暗黑主题 + 动画效果

### 🚧 进行中
- [ ] 战斗系统 UI
- [ ] 修炼系统 UI
- [ ] 背包系统 UI
- [ ] 商店系统 UI

### 📋 待开发
- [ ] K8s 终端模拟器
- [ ] 任务系统 UI
- [ ] 成就系统 UI
- [ ] 社交功能
- [ ] 云端存档
- [ ] PVP 竞技场

## 🔧 开发指南

### 添加新 API 端点

```python
# backend/api/new_module.py
from fastapi import APIRouter

router = APIRouter(prefix="/api/new-module", tags=["new-module"])

@router.get("/items")
async def get_items():
    return {
        "status": "success",
        "data": [...]
    }
```

在 `backend/main.py` 中注册：
```python
from api.new_module import router as new_router
app.include_router(new_router)
```

### 添加新页面

```javascript
// frontend/src/pages/NewPage.js
export class NewPage {
  constructor() {
    this.state = {};
  }

  render() {
    return `
      <div class="p-6">
        <h1 class="text-2xl font-bold">新页面</h1>
      </div>
    `;
  }

  mount(container) {
    container.innerHTML = this.render();
    this.bindEvents();
  }

  bindEvents() {
    // 绑定事件
  }
}
```

在 `main.js` 中添加路由：
```javascript
import { NewPage } from "./pages/NewPage.js";

// 在 handleTabChange 中添加 case
case "new-tab":
  const newPage = new NewPage();
  newPage.mount(mainContent);
  break;
```

### 状态管理

```javascript
// 获取状态
const player = gameStore.getState().player;

// 更新状态
gameStore.setState({ player: newPlayerData });

// 订阅变化
const unsubscribe = gameStore.subscribe((state) => {
  console.log("State updated:", state);
});

// 取消订阅
unsubscribe();
```

## 🐛 调试

### 后端调试
```bash
# 启用热重载
uvicorn main:app --reload --port 8000

# 查看日志
uvicorn main:app --log-level debug
```

### 前端调试
- 打开浏览器开发者工具 (F12)
- 查看 Console 面板
- Network 面板查看 API 请求
- Application 面板查看 LocalStorage

## 🤝 贡献

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](../LICENSE)

## 🙏 致谢

- [FastAPI](https://fastapi.tiangolo.com/) - 高性能 Web 框架
- [Tailwind CSS](https://tailwindcss.com/) - 实用优先 CSS 框架
- [Font Awesome](https://fontawesome.com/) - 精美图标

---

<div align="center">

**在浏览器中开启你的 Kubernetes 修仙之旅！**

</div>
