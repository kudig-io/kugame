import { api } from "../lib/api.js";
import { gameStore } from "../lib/store.js";
import { toast } from "../components/ui/Toast.js";

export class LoginPage {
  constructor() {
    this.selectedSect = null;
    this.sects = [
      { id: "qingyun", name: "青云宗", icon: "fa-cloud", color: "text-blue-400", 
        desc: "以天元术为根基，擅长群攻与范围伤害" },
      { id: "jianxin", name: "剑心阁", icon: "fa-khanda", color: "text-red-400",
        desc: "专注单体爆发输出，暴击率高" },
      { id: "lingyao", name: "灵药谷", icon: "fa-leaf", color: "text-green-400",
        desc: "以符箓辅助和治疗为主" },
      { id: "tianji", name: "天机阁", icon: "fa-yin-yang", color: "text-purple-400",
        desc: "精通阵法防御和控制技能" },
    ];
  }

  render() {
    return `
      <div class="min-h-screen flex items-center justify-center relative overflow-hidden bg-gradient-to-br from-slate-900 via-indigo-950 to-slate-900">
        <!-- 背景动画 -->
        <div class="absolute inset-0 overflow-hidden">
          <div class="absolute -inset-[100%] animate-[spin_60s_linear_infinite] opacity-20">
            <div class="absolute top-1/4 left-1/4 w-96 h-96 bg-primary/30 rounded-full blur-3xl"></div>
            <div class="absolute bottom-1/4 right-1/4 w-96 h-96 bg-secondary/30 rounded-full blur-3xl"></div>
          </div>
        </div>

        <!-- 登录卡片 -->
        <div class="relative z-10 w-full max-w-4xl p-8">
          <div class="text-center mb-12">
            <h1 class="text-6xl font-bold mb-4 text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 via-blue-500 to-purple-600">
              KuGame 修仙
            </h1>
            <p class="text-xl text-muted-foreground">在修仙世界掌握 Kubernetes</p>
          </div>

          <div class="glass rounded-2xl p-8 space-y-8">
            <!-- 角色名称 -->
            <div class="space-y-2">
              <label class="text-sm font-medium">道号</label>
              <input 
                type="text" 
                id="player-name" 
                placeholder="请输入您的道号..."
                class="w-full px-4 py-3 rounded-lg bg-background/50 border border-border focus:border-primary focus:ring-1 focus:ring-primary outline-none transition-all"
                maxlength="12"
              >
            </div>

            <!-- 门派选择 -->
            <div class="space-y-4">
              <label class="text-sm font-medium">选择门派</label>
              <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
                ${this.sects.map(sect => this.renderSectCard(sect)).join("")}
              </div>
            </div>

            <!-- 创建按钮 -->
            <button 
              id="btn-create"
              class="w-full py-4 rounded-lg bg-gradient-to-r from-primary to-secondary text-primary-foreground font-semibold text-lg hover:opacity-90 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
              disabled
            >
              踏上修仙之路
            </button>
          </div>

          <!-- 特性展示 -->
          <div class="mt-12 grid grid-cols-3 gap-6 text-center">
            <div class="glass rounded-xl p-4">
              <i class="fas fa-code text-3xl text-primary mb-2"></i>
              <p class="text-sm text-muted-foreground">边玩边学 K8s</p>
            </div>
            <div class="glass rounded-xl p-4">
              <i class="fas fa-users text-3xl text-secondary mb-2"></i>
              <p class="text-sm text-muted-foreground">多人在线修仙</p>
            </div>
            <div class="glass rounded-xl p-4">
              <i class="fas fa-chart-line text-3xl text-accent mb-2"></i>
              <p class="text-sm text-muted-foreground">实时进度追踪</p>
            </div>
          </div>
        </div>
      </div>
    `;
  }

  renderSectCard(sect) {
    const isSelected = this.selectedSect === sect.id;
    return `
      <div 
        class="sect-card cursor-pointer rounded-xl p-4 border-2 transition-all hover:scale-105 ${
          isSelected ? "border-primary bg-primary/10" : "border-border hover:border-primary/50"
        }"
        data-sect="${sect.id}"
      >
        <div class="text-center space-y-2">
          <i class="fas ${sect.icon} text-3xl ${sect.color}"></i>
          <h3 class="font-semibold">${sect.name}</h3>
          <p class="text-xs text-muted-foreground">${sect.desc}</p>
        </div>
      </div>
    `;
  }

  mount(container) {
    container.innerHTML = this.render();
    this.bindEvents();
  }

  bindEvents() {
    // 门派选择
    document.querySelectorAll(".sect-card").forEach(card => {
      card.addEventListener("click", () => {
        this.selectedSect = card.dataset.sect;
        this.updateUI();
      });
    });

    // 名称输入
    const nameInput = document.getElementById("player-name");
    nameInput?.addEventListener("input", () => {
      this.updateUI();
    });

    // 创建角色
    document.getElementById("btn-create")?.addEventListener("click", () => {
      this.handleCreatePlayer();
    });
  }

  updateUI() {
    // 更新门派卡片样式
    document.querySelectorAll(".sect-card").forEach(card => {
      const isSelected = this.selectedSect === card.dataset.sect;
      card.className = `sect-card cursor-pointer rounded-xl p-4 border-2 transition-all hover:scale-105 ${
        isSelected ? "border-primary bg-primary/10" : "border-border hover:border-primary/50"
      }`;
    });

    // 更新按钮状态
    const name = document.getElementById("player-name")?.value?.trim();
    const btnCreate = document.getElementById("btn-create");
    btnCreate.disabled = !(name && this.selectedSect);
  }

  async handleCreatePlayer() {
    const name = document.getElementById("player-name").value.trim();
    
    if (!name || !this.selectedSect) {
      toast.error("请填写完整信息", "道号和门派都是必填项");
      return;
    }

    const btnCreate = document.getElementById("btn-create");
    btnCreate.disabled = true;
    btnCreate.innerHTML = '<i class="fas fa-spinner fa-spin"></i> 创建中...';

    try {
      const response = await api.createPlayer({
        name,
        sect: this.selectedSect,
      });

      gameStore.setState({ player: response.data });
      toast.success("角色创建成功", `欢迎来到 KuGame，${name}！`);
      
      // 触发路由切换到游戏主界面
      window.dispatchEvent(new CustomEvent("game:login", { detail: response.data }));
    } catch (error) {
      toast.error("创建失败", error.message);
      btnCreate.disabled = false;
      btnCreate.innerHTML = "踏上修仙之路";
    }
  }
}
