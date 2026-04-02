// 游戏主布局
export class GameLayout {
  constructor() {
    this.sidebarOpen = true;
    this.activeTab = "dashboard";
    this.tabs = [
      { id: "dashboard", name: "概览", icon: "fa-home" },
      { id: "combat", name: "战斗", icon: "fa-sword" },
      { id: "cultivation", name: "修炼", icon: "fa-meditation" },
      { id: "inventory", name: "背包", icon: "fa-backpack" },
      { id: "shop", name: "商店", icon: "fa-store" },
      { id: "quests", name: "任务", icon: "fa-scroll" },
      { id: "k8s", name: "K8s", icon: "fa-dharmachakra" },
    ];
  }

  render() {
    return `
      <div class="flex h-screen bg-background">
        <!-- 侧边栏 -->
        <aside class="${
          this.sidebarOpen ? "w-64" : "w-16"
        } transition-all duration-300 border-r border-border bg-card flex flex-col">
          <!-- Logo -->
          <div class="h-16 flex items-center justify-center border-b border-border">
            ${this.sidebarOpen 
              ? `<span class="text-xl font-bold gradient-text">KuGame</span>`
              : `<i class="fas fa-gamepad text-xl text-primary"></i>`
            }
          </div>

          <!-- 导航 -->
          <nav class="flex-1 py-4 space-y-1">
            ${this.tabs.map(tab => this.renderNavItem(tab)).join("")}
          </nav>

          <!-- 底部 -->
          <div class="p-4 border-t border-border">
            <button id="toggle-sidebar" class="w-full flex items-center justify-center p-2 rounded-lg hover:bg-accent transition-colors">
              <i class="fas ${this.sidebarOpen ? "fa-chevron-left" : "fa-chevron-right"}"></i>
            </button>
          </div>
        </aside>

        <!-- 主内容区 -->
        <div class="flex-1 flex flex-col overflow-hidden">
          <!-- 顶部栏 -->
          <header class="h-16 border-b border-border bg-card flex items-center justify-between px-6">
            <div class="flex items-center gap-4">
              <span class="text-muted-foreground">当前位置:</span>
              <span class="font-medium">${this.getCurrentLocation()}</span>
            </div>
            <div class="flex items-center gap-4">
              <button class="p-2 rounded-lg hover:bg-accent transition-colors relative">
                <i class="fas fa-bell"></i>
                <span class="absolute top-1 right-1 w-2 h-2 bg-red-500 rounded-full"></span>
              </button>
              <div class="flex items-center gap-2">
                <div class="w-8 h-8 rounded-full bg-primary/20 flex items-center justify-center">
                  <i class="fas fa-user text-primary"></i>
                </div>
                <span class="text-sm font-medium hidden sm:block">玩家名称</span>
              </div>
            </div>
          </header>

          <!-- 内容区 -->
          <main id="main-content" class="flex-1 overflow-auto">
            <!-- 动态内容将在这里渲染 -->
          </main>
        </div>
      </div>
    `;
  }

  renderNavItem(tab) {
    const isActive = this.activeTab === tab.id;
    return `
      <button 
        class="w-full flex items-center ${
          this.sidebarOpen ? "px-4" : "justify-center px-2"
        } py-3 transition-all ${
          isActive 
            ? "bg-primary/10 text-primary border-r-2 border-primary" 
            : "text-muted-foreground hover:bg-accent hover:text-foreground"
        }"
        data-tab="${tab.id}"
      >
        <i class="fas ${tab.icon} ${this.sidebarOpen ? "mr-3" : ""}"></i>
        ${this.sidebarOpen ? `<span>${tab.name}</span>` : ""}
      </button>
    `;
  }

  getCurrentLocation() {
    const locations = {
      dashboard: "青云宗 · 主峰",
      combat: "战斗训练场",
      cultivation: "修炼洞府",
      inventory: "储物袋",
      shop: "坊市",
      quests: "任务堂",
      k8s: "天机阁 · K8s 秘境",
    };
    return locations[this.activeTab] || "未知区域";
  }

  mount(container) {
    container.innerHTML = this.render();
    this.bindEvents();
  }

  bindEvents() {
    // 切换侧边栏
    document.getElementById("toggle-sidebar")?.addEventListener("click", () => {
      this.sidebarOpen = !this.sidebarOpen;
      this.mount(document.getElementById("app"));
    });

    // 导航切换
    document.querySelectorAll("[data-tab]").forEach(btn => {
      btn.addEventListener("click", () => {
        this.activeTab = btn.dataset.tab;
        this.mount(document.getElementById("app"));
        // 触发 tab 切换事件
        window.dispatchEvent(new CustomEvent("game:tab-change", { 
          detail: { tab: this.activeTab } 
        }));
      });
    });
  }

  // 渲染特定标签的内容
  renderContent(content) {
    const mainContent = document.getElementById("main-content");
    if (mainContent) {
      mainContent.innerHTML = content;
    }
  }
}
