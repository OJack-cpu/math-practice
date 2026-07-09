#!/bin/bash
# ══════════════════════════════════════════
#  考研数学刷题系统 - 一键启动脚本
#  用法: bash start.sh
# ══════════════════════════════════════════

echo "🚀 启动考研数学刷题系统..."

# 后端
echo -n "  [1/2] 后端 FastAPI (端口 8000)... "
cd /workspace/backend
nohup python -m uvicorn main:app --host 0.0.0.0 --port 8000 > /tmp/be.log 2>&1 &
sleep 2
curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/docs | grep -q 200 && echo "✅ OK" || echo "❌ 失败"

# 前端
echo -n "  [2/2] 前端 Vite (端口 35181)... "
cd /workspace/frontend
nohup npx vite --host 0.0.0.0 --port 35181 > /tmp/fe.log 2>&1 &
sleep 3
curl -s -o /dev/null -w "%{http_code}" http://localhost:35181/ | grep -q 200 && echo "✅ OK" || echo "❌ 失败"

echo ""
echo "══════════════════════════════════"
echo "  ✅ 启动完成！"
echo "  去端口面板 → 35181 → 查看预览"
echo "══════════════════════════════════"
