// API 客户端
const API_BASE_URL = "http://localhost:8000";

class ApiClient {
  constructor() {
    this.baseURL = API_BASE_URL;
  }

  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    const config = {
      headers: {
        "Content-Type": "application/json",
        ...options.headers,
      },
      ...options,
    };

    if (config.body && typeof config.body === "object") {
      config.body = JSON.stringify(config.body);
    }

    try {
      const response = await fetch(url, config);
      
      if (!response.ok) {
        const error = await response.json().catch(() => ({ message: "Unknown error" }));
        throw new Error(error.message || `HTTP ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error("API Error:", error);
      throw error;
    }
  }

  // Player API
  getPlayer() {
    return this.request("/api/player");
  }

  createPlayer(data) {
    return this.request("/api/player/create", {
      method: "POST",
      body: data,
    });
  }

  getPlayerStats() {
    return this.request("/api/player/stats");
  }

  // Game API
  explore() {
    return this.request("/api/game/explore", { method: "POST" });
  }

  cultivate() {
    return this.request("/api/game/cultivate", { method: "POST" });
  }

  rest() {
    return this.request("/api/game/rest", { method: "POST" });
  }

  // Combat API
  startCombat(enemyId) {
    return this.request("/api/combat/start", {
      method: "POST",
      body: { enemy_id: enemyId },
    });
  }

  combatAction(action, data = {}) {
    return this.request("/api/combat/action", {
      method: "POST",
      body: { action, ...data },
    });
  }

  // Shop API
  getShopItems() {
    return this.request("/api/shop/items");
  }

  buyItem(itemId, quantity = 1) {
    return this.request("/api/shop/buy", {
      method: "POST",
      body: { item_id: itemId, quantity },
    });
  }

  sellItem(itemId, quantity = 1) {
    return this.request("/api/shop/sell", {
      method: "POST",
      body: { item_id: itemId, quantity },
    });
  }

  // Inventory API
  getInventory() {
    return this.request("/api/inventory");
  }

  useItem(itemId) {
    return this.request("/api/inventory/use", {
      method: "POST",
      body: { item_id: itemId },
    });
  }

  equipItem(itemId) {
    return this.request("/api/inventory/equip", {
      method: "POST",
      body: { item_id: itemId },
    });
  }

  // K8s API
  getClusterStatus() {
    return this.request("/api/k8s/cluster");
  }

  getNamespaces() {
    return this.request("/api/k8s/namespaces");
  }

  getPods(namespace) {
    return this.request(`/api/k8s/pods?namespace=${namespace}`);
  }

  getNodeStatus() {
    return this.request("/api/k8s/nodes");
  }
}

export const api = new ApiClient();
