// 简单的状态管理 store
export function createStore(initialState = {}) {
  let state = { ...initialState };
  const listeners = new Set();

  return {
    getState() {
      return state;
    },

    setState(newState) {
      state = { ...state, ...newState };
      listeners.forEach(listener => listener(state));
    },

    subscribe(listener) {
      listeners.add(listener);
      return () => listeners.delete(listener);
    },

    // 特定路径的选择器
    select(selector) {
      return selector(state);
    },
  };
}

// 游戏状态 store
export const gameStore = createStore({
  player: null,
  inventory: [],
  quests: [],
  currentLocation: null,
  inCombat: false,
  combatState: null,
  notifications: [],
  loading: false,
  error: null,
});

// 主题 store
export const themeStore = createStore({
  theme: "dark",
  sidebarOpen: true,
  activeTab: "dashboard",
});

// WebSocket 连接管理
export function createWebSocketClient(url) {
  let ws = null;
  const messageHandlers = new Map();

  function connect() {
    ws = new WebSocket(url);

    ws.onopen = () => {
      console.log("WebSocket connected");
      gameStore.setState({ wsConnected: true });
    };

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      const handler = messageHandlers.get(data.type);
      if (handler) {
        handler(data.payload);
      }
    };

    ws.onclose = () => {
      console.log("WebSocket disconnected");
      gameStore.setState({ wsConnected: false });
      // 自动重连
      setTimeout(connect, 3000);
    };

    ws.onerror = (error) => {
      console.error("WebSocket error:", error);
    };
  }

  function send(type, payload) {
    if (ws?.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify({ type, payload }));
    }
  }

  function on(type, handler) {
    messageHandlers.set(type, handler);
  }

  return { connect, send, on };
}
