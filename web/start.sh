#!/bin/bash

# KuGame Web 启动脚本

echo "🎮 Starting KuGame Web..."

# 启动后端
start_backend() {
    echo "📡 Starting backend server..."
    cd backend
    python3 main.py &
    BACKEND_PID=$!
    cd ..
    echo "✅ Backend started (PID: $BACKEND_PID)"
}

# 启动前端
start_frontend() {
    echo "🎨 Starting frontend server..."
    cd frontend
    python3 -m http.server 3000 &
    FRONTEND_PID=$!
    cd ..
    echo "✅ Frontend started (PID: $FRONTEND_PID) on http://localhost:3000"
}

# 清理函数
cleanup() {
    echo ""
    echo "🛑 Shutting down servers..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    echo "👋 KuGame stopped"
    exit 0
}

# 捕获中断信号
trap cleanup INT TERM

# 启动服务
start_backend
start_frontend

echo ""
echo "🚀 KuGame is running!"
echo "   Frontend: http://localhost:3000"
echo "   Backend:  http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop"

# 保持运行
wait
