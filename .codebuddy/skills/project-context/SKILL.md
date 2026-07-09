# Project Context Skill

## 用途

为 AI 助手提供考研数学刷题系统的完整项目上下文，包括架构、技术栈、数据库模型和代码公约。

---

## 项目概述

**考研数学刷题系统** 是一个基于 FastAPI + React + PostgreSQL 的 Web 应用，使用 SM-2 间隔重复算法帮助用户高效复习考研数学题目。

## 技术栈

| 层级 | 技术 |
|------|------|
| 后端框架 | FastAPI (Python 3.11+) |
| ORM | SQLAlchemy 2.0 |
| 数据库 | PostgreSQL 16（生产）/ SQLite（开发） |
| 前端框架 | React 19 + Vite |
| UI 库 | Ant Design 5 |
| 数学公式渲染 | KaTeX |
| 图表库 | ECharts (via echarts-for-react) |
| 容器化 | Docker + docker-compose |
| 反向代理 | Nginx |

## 项目结构

```
/workspace/
├── backend/
│   ├── main.py           # FastAPI 应用入口，全部 API 路由
│   ├── database.py       # SQLAlchemy 引擎 & 会话管理
│   ├── models.py         # ORM 模型定义（4 张核心表）
│   ├── schemas.py        # Pydantic 请求/响应模型
│   ├── sm2.py            # SM-2 间隔重复算法实现
│   ├── seed.py           # 种子数据（60+ 道考研真题风格题目）
│   ├── tests/            # pytest 测试
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── pages/        # 页面组件
│   │   │   ├── Dashboard.jsx   # 仪表盘 / 数据可视化
│   │   │   ├── Practice.jsx    # 刷题页面
│   │   │   ├── ErrorBook.jsx   # 错题本
│   │   │   └── Review.jsx      # 复习调度
│   │   ├── App.jsx       # 路由配置
│   │   └── main.jsx      # 入口
│   ├── nginx.conf
│   ├── vite.config.js
│   └── Dockerfile
└── docker-compose.yml
```

## 核心数据模型

### knowledge_points（知识点表）
- `id`, `name`, `category`（高等数学/线性代数/概率论）, `description`
- 关联: 一对多 → questions

### questions（题目表）
- `id`, `content`（题干）, `question_type`（single_choice/multiple_choice/fill_blank）
- `options`（JSON 数组）, `answer`, `explanation`, `difficulty`（1~5）
- `knowledge_point_id`（外键）

### answer_records（答题记录表）
- `id`, `question_id`, `user_answer`, `is_correct`, `time_spent`, `created_at`

### review_schedules（SM-2 复习调度表）
- `question_id`（unique）, `easiness_factor`, `interval`, `repetitions`
- `next_review_date`, `last_review_date`

## SM-2 算法

位于 `backend/sm2.py`，核心逻辑：
- `calculate_quality(is_correct, time_spent)` → 返回 0~5 的质量评分
- `sm2_update(quality, easiness_factor, interval, repetitions)` → 返回更新后的参数和下次复习日期

## API 路由汇总

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
| `ALLOWED_ORIGINS` | CORS 白名单（逗号分隔） | `http://localhost:5173,http://localhost:3000` |
| `ENV` | 运行环境（`development` 开启热重载） | （空） |

## 代码公约

- Python 遵循 PEP 8，使用 4 空格缩进
- API 路由定义在 `main.py` 中，按功能分区，使用 `═══` 注释分隔
- 数据库操作使用 SQLAlchemy ORM，通过 `Depends(get_db)` 注入会话
- 前端使用函数组件 + Hooks，Ant Design 组件
- 数据获取使用 axios，API 调用集中在各页面组件中
