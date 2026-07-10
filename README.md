# 考研数学刷题系统 (Math Practice)

基于 FastAPI + React + PostgreSQL 的智能刷题系统，集成 **SM-2 间隔重复算法**，帮助高效备考考研数学。

## 功能特性

- 📝 **60+ 考研真题风格题目** — 覆盖高等数学、线性代数、概率论三大类
- 🧠 **SM-2 间隔重复** — 算法驱动智能复习，薄弱题目高频出现
- 📊 **数据可视化仪表盘** — 每日学习折线图、知识点掌握度雷达图
- ❌ **智能错题本** — 自动收集错题，按最后错误时间排序
- 🔍 **薄弱点分析** — 按知识点统计正确率，精准定位弱项
- 📱 **响应式界面** — React + Ant Design + KaTeX 数学公式渲染

## 技术栈

| 层级 | 技术 |
|------|------|
| 后端 | FastAPI + SQLAlchemy + Uvicorn |
| 数据库 | PostgreSQL（生产）/ SQLite（开发） |
| 前端 | React 19 + Vite + Ant Design |
| 图表 | ECharts |
| 公式 | KaTeX |
| 容器化 | Docker + Docker Compose |
| 反向代理 | Nginx |

## 项目结构

```
├── backend/
│   ├── main.py          # API 路由（9 个端点）
│   ├── models.py        # 4 张核心数据表
│   ├── sm2.py           # SM-2 算法实现
│   ├── seed.py          # 种子数据（60+ 题）
│   ├── schemas.py       # Pydantic 模型
│   └── tests/           # pytest 测试
├── frontend/
│   ├── src/pages/       # 仪表盘、刷题、错题本、复习
│   ├── nginx.conf       # Nginx 反向代理
│   └── Dockerfile       # 多阶段构建
├── docker-compose.yml   # 三服务编排
└── submission/          # 实验报告
```

## 快速开始

### 方式一：本地开发（零配置 SQLite）

```bash
# 后端
cd backend
pip install -r requirements.txt
python main.py              # http://localhost:8000/docs

# 前端（新终端）
cd frontend
npm install
npm run dev                 # http://localhost:5173
```

### 方式二：Docker 部署（PostgreSQL）

```bash
docker compose up -d        # 一键启动三服务
# 前端: http://localhost
# API:  http://localhost:8000/docs
```

## API 概览

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/knowledge-points` | 知识点列表 |
| GET | `/api/questions` | 题目列表（支持筛选） |
| GET | `/api/questions/{id}` | 题目详情 |
| POST | `/api/answer` | 提交答案（SM-2 核心） |
| GET | `/api/review/due` | 到期复习题 |
| GET | `/api/error-book` | 错题本 |
| GET | `/api/dashboard` | 仪表盘数据 |
| GET | `/api/analysis/weak-points` | 薄弱点分析 |
| GET | `/api/stats/correct-rate-trend` | 正确率趋势 |

## 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `DATABASE_URL` | 数据库连接串 | `sqlite:///./math_practice.db` |
| `ALLOWED_ORIGINS` | CORS 白名单 | `localhost:5173,localhost:3000` |
| `ENV` | `development` 开启热重载 | （空） |

## 许可证

MIT
