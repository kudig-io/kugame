// KuGame Web Frontend - Main Entry Point
import { LoginPage } from "./pages/Login.js";
import { GameLayout } from "./pages/Layout.js";
import { Dashboard } from "./pages/Dashboard.js";
import { gameStore, createWebSocketClient } from "./lib/store.js";
import { api } from "./lib/api.js";
import { toast } from "./components/ui/Toast.js";

class KuGameApp {
  constructor() {
    this.currentPage = null;
    this.layout = null;
    this.wsClient = null;
    
    this.init();
  }

  async init() {
    console.log("🎮 KuGame initializing...");
    
    // 检查登录状态
    await this.checkAuth();
    
    // 绑定全局事件
    this.bindGlobalEvents();
    
    // 初始化 WebSocket
    this.initWebSocket();
  }

  async checkAuth() {
    try {
      // 尝试获取玩家信息
      const response = await api.getPlayer();
      if (response.data && response.data.id) {
        gameStore.setState({ player: response.data });
        this.showGame();
      } else {
        this.showLogin();
      }
    } catch (error) {
      console.log("Not authenticated, showing login");
      this.showLogin();
    }
  }

  showLogin() {
    const app = document.getElementById("app");
    this.currentPage = new LoginPage();
    this.currentPage.mount(app);
  }

  showGame() {
    const app = document.getElementById("app");
    this.layout = new GameLayout();
    this.layout.mount(app);
    
    // 默认显示 Dashboard
    const dashboard = new Dashboard();
    dashboard.mount(document.getElementById("main-content"));
  }

  bindGlobalEvents() {
    // 登录成功事件
    window.addEventListener("game:login", (e) => {
      gameStore.setState({ player: e.detail });
      this.showGame();
      toast.success("登录成功", `欢迎回来，${e.detail.name}！`);
    });

    // Tab 切换事件
    window.addEventListener("game:tab-change", (e) => {
      this.handleTabChange(e.detail.tab);
    });

    // 错误处理
    window.addEventListener("error", (e) => {
      console.error("Global error:", e.error);
      toast.error("发生错误", e.error?.message || "未知错误");
    });

    // 未处理的 Promise 错误
    window.addEventListener("unhandledrejection", (e) => {
      console.error("Unhandled rejection:", e.reason);
      toast.error("请求失败", e.reason?.message || "网络错误");
    });
  }

  handleTabChange(tab) {
    const mainContent = document.getElementById("main-content");
    if (!mainContent) return;

    // 清除当前内容
    mainContent.innerHTML = "";

    // 根据 tab 渲染对应页面
    switch (tab) {
      case "dashboard":
        const dashboard = new Dashboard();
        dashboard.mount(mainContent);
        break;
      case "combat":
        mainContent.innerHTML = `
          <div class="p-6">
            <h2 class="text-2xl font-bold mb-4">战斗系统</h2>
            <p class="text-muted-foreground">战斗功能开发中...</p>
          </div>
        `;
        break;
      case "cultivation":
        mainContent.innerHTML = `
          <div class="p-6">
            <h2 class="text-2xl font-bold mb-4">修炼系统</h2>
            <p class="text-muted-foreground">修炼功能开发中...</p>
          </div>
        `;
        break;
      case "inventory":
        mainContent.innerHTML = `
          <div class="p-6">
            <h2 class="text-2xl font-bold mb-4">背包</h2>
            <p class="text-muted-foreground">背包功能开发中...</p>
          </div>
        `;
        break;
      case "shop":
        mainContent.innerHTML = `
          <div class="p-6">
            <h2 class="text-2xl font-bold mb-4">商店</h2>
            <p class="text-muted-foreground">商店功能开发中...</p>
          </div>
        `;
        break;
      case "quests":
        mainContent.innerHTML = `
          <div class="p-6">
            <h2 class="text-2xl font-bold mb-4">任务系统</h2>
            <p class="text-muted-foreground">任务功能开发中...</p>
          </div>
        `;
        break;
      case "k8s":
        mainContent.innerHTML = `
          <div class="p-6">
            <h2 class="text-2xl font-bold mb-4">K8s 秘境</h2>
            <p class="text-muted-foreground">K8s 学习功能开发中...</p>
          </div>
        `;
        break;
      default:
        mainContent.innerHTML = `
          <div class="p-6">
            <h2 class="text-2xl font-bold mb-4">${tab}</h2>
            <p class="text-muted-foreground">功能开发中...</p>
          </div>
        `;
    }
  }

  initWebSocket() {
    this.wsClient = createWebSocketClient("ws://localhost:8000/ws/player");
    
    this.wsClient.on("player_update", (data) => {
      gameStore.setState({ player: data });
    });

    this.wsClient.on("notification", (data) => {
      toast.info(data.title, data.message);
    });

    this.wsClient.on("combat_update", (data) => {
      gameStore.setState({ combatState: data });
    });

    this.wsClient.connect();
  }
}

// 初始化应用
document.addEventListener("DOMContentLoaded", () => {
  window.kugame = new KuGameApp();
});

// 热更新支持
if (import.meta.hot) {
  import.meta.hot.accept();
}
