import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "../components/ui/Card.js";
import { ProgressWithLabel } from "../components/ui/Progress.js";
import { gameStore } from "../lib/store.js";

export class Dashboard {
  constructor() {
    this.unsubscribe = null;
  }

  render() {
    const player = gameStore.getState().player;
    
    if (!player) {
      return `
        <div class="flex items-center justify-center h-full">
          <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
        </div>
      `;
    }

    return `
      <div class="p-6 space-y-6">
        <!-- 欢迎信息 -->
        <div class="flex items-center justify-between">
          <div>
            <h1 class="text-3xl font-bold gradient-text">欢迎回来，${player.name}</h1>
            <p class="text-muted-foreground">${player.sect} · ${player.cultivation_realm}</p>
          </div>
          <div class="text-right">
            <p class="text-sm text-muted-foreground">在线时间</p>
            <p class="text-xl font-mono">${player.online_time || "00:00:00"}</p>
          </div>
        </div>

        <!-- 状态卡片 -->
        <div class="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
          ${this.renderStatCard("境界进度", player.realm_progress, "/100", "text-blue-500")}
          ${this.renderStatCard("K8s 经验", player.k8s_exp || 0, "", "text-purple-500")}
          ${this.renderStatCard("灵石", player.spirit_stones || 0, "", "text-yellow-500")}
          ${this.renderStatCard("完成任务", player.completed_quests || 0, "", "text-green-500")}
        </div>

        <!-- 主要状态条 -->
        <div class="grid gap-4 md:grid-cols-2">
          ${this.renderStatusCard(player)}
          ${this.renderQuickActionsCard()}
        </div>

        <!-- 最新活动 -->
        <Card>
          <CardHeader>
            <CardTitle>最近活动</CardTitle>
            <CardDescription>您的修仙历程</CardDescription>
          </CardHeader>
          <CardContent>
            <div id="activity-list" class="space-y-2">
              ${this.renderActivities(player.recent_activities || [])}
            </div>
          </CardContent>
        </Card>
      </div>
    `;
  }

  renderStatCard(label, value, suffix, colorClass) {
    return `
      <div class="game-card p-4">
        <p class="text-sm text-muted-foreground">${label}</p>
        <p class="text-2xl font-bold ${colorClass}">${value}${suffix}</p>
      </div>
    `;
  }

  renderStatusCard(player) {
    return `
      <div class="game-card">
        <div class="p-6 space-y-4">
          <h3 class="text-lg font-semibold">生命与法力</h3>
          <div class="space-y-3">
            <div>
              <div class="flex justify-between text-sm mb-1">
                <span>生命值</span>
                <span>${player.hp || 100}/${player.max_hp || 100}</span>
              </div>
              <div class="h-2 bg-muted rounded-full overflow-hidden">
                <div class="h-full bg-red-500 transition-all" 
                     style="width: ${((player.hp || 100) / (player.max_hp || 100) * 100)}%"></div>
              </div>
            </div>
            <div>
              <div class="flex justify-between text-sm mb-1">
                <span>法力值</span>
                <span>${player.mp || 50}/${player.max_mp || 50}</span>
              </div>
              <div class="h-2 bg-muted rounded-full overflow-hidden">
                <div class="h-full bg-blue-500 transition-all" 
                     style="width: ${((player.mp || 50) / (player.max_mp || 50) * 100)}%"></div>
              </div>
            </div>
            <div>
              <div class="flex justify-between text-sm mb-1">
                <span>经验值</span>
                <span>${player.exp || 0}/${player.max_exp || 100}</span>
              </div>
              <div class="h-2 bg-muted rounded-full overflow-hidden">
                <div class="h-full bg-yellow-500 transition-all" 
                     style="width: ${((player.exp || 0) / (player.max_exp || 100) * 100)}%"></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    `;
  }

  renderQuickActionsCard() {
    return `
      <div class="game-card">
        <div class="p-6 space-y-4">
          <h3 class="text-lg font-semibold">快捷操作</h3>
          <div class="grid grid-cols-2 gap-3">
            <button id="btn-cultivate" class="flex flex-col items-center gap-2 p-4 rounded-lg bg-primary/10 hover:bg-primary/20 transition-colors">
              <i class="fas fa-meditation text-2xl text-primary"></i>
              <span class="text-sm">修炼</span>
            </button>
            <button id="btn-explore" class="flex flex-col items-center gap-2 p-4 rounded-lg bg-secondary hover:bg-secondary/80 transition-colors">
              <i class="fas fa-compass text-2xl text-secondary-foreground"></i>
              <span class="text-sm">探索</span>
            </button>
            <button id="btn-rest" class="flex flex-col items-center gap-2 p-4 rounded-lg bg-accent hover:bg-accent/80 transition-colors">
              <i class="fas fa-bed text-2xl text-accent-foreground"></i>
              <span class="text-sm">休息</span>
            </button>
            <button id="btn-quest" class="flex flex-col items-center gap-2 p-4 rounded-lg bg-muted hover:bg-muted/80 transition-colors">
              <i class="fas fa-scroll text-2xl text-muted-foreground"></i>
              <span class="text-sm">任务</span>
            </button>
          </div>
        </div>
      </div>
    `;
  }

  renderActivities(activities) {
    if (activities.length === 0) {
      return `<p class="text-muted-foreground text-center py-4">暂无活动记录</p>`;
    }
    
    return activities.map(activity => `
      <div class="flex items-center gap-3 p-3 rounded-lg bg-muted/50">
        <div class="w-2 h-2 rounded-full ${this.getActivityColor(activity.type)}"></div>
        <div class="flex-1">
          <p class="text-sm">${activity.message}</p>
          <p class="text-xs text-muted-foreground">${activity.time}</p>
        </div>
      </div>
    `).join("");
  }

  getActivityColor(type) {
    const colors = {
      combat: "bg-red-500",
      cultivation: "bg-blue-500",
      quest: "bg-green-500",
      shop: "bg-yellow-500",
      default: "bg-gray-500",
    };
    return colors[type] || colors.default;
  }

  mount(container) {
    container.innerHTML = this.render();
    this.bindEvents();
    
    // 订阅状态变化
    this.unsubscribe = gameStore.subscribe(() => {
      container.innerHTML = this.render();
      this.bindEvents();
    });
  }

  bindEvents() {
    document.getElementById("btn-cultivate")?.addEventListener("click", () => {
      this.handleCultivate();
    });
    document.getElementById("btn-explore")?.addEventListener("click", () => {
      this.handleExplore();
    });
    document.getElementById("btn-rest")?.addEventListener("click", () => {
      this.handleRest();
    });
    document.getElementById("btn-quest")?.addEventListener("click", () => {
      this.handleQuest();
    });
  }

  async handleCultivate() {
    // 实现修炼逻辑
    console.log("开始修炼...");
  }

  async handleExplore() {
    // 实现探索逻辑
    console.log("开始探索...");
  }

  async handleRest() {
    // 实现休息逻辑
    console.log("开始休息...");
  }

  async handleQuest() {
    // 实现任务逻辑
    console.log("查看任务...");
  }

  unmount() {
    if (this.unsubscribe) {
      this.unsubscribe();
    }
  }
}
