"""KuGame Web Backend - FastAPI Application"""
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from api import (
    player_router,
    game_router,
    combat_router,
    shop_router,
    inventory_router,
    k8s_router,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    print("🚀 KuGame server starting...")
    yield
    # Shutdown
    print("👋 KuGame server shutting down...")


app = FastAPI(
    title="KuGame API",
    description="Backend API for KuGame - Learn Kubernetes through Xianxia gaming",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应该限制具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(player_router)
app.include_router(game_router)
app.include_router(combat_router)
app.include_router(shop_router)
app.include_router(inventory_router)
app.include_router(k8s_router)

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            await connection.send_json(message)


manager = ConnectionManager()


@app.websocket("/ws/player")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time player updates"""
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            # 处理收到的消息
            if data.get("type") == "ping":
                await websocket.send_json({"type": "pong"})
            else:
                # 广播给其他连接
                await manager.broadcast({
                    "type": "player_update",
                    "data": data,
                })
    except WebSocketDisconnect:
        manager.disconnect(websocket)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to KuGame API",
        "version": "1.0.0",
        "docs": "/docs",
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
