# 考研数学刷题系统 — MVP 编码实现报告

## 1. 项目概述

| 项目 | 内容 |
|------|------|
| 项目名称 | 考研数学刷题系统 |
| 技术栈 | 后端：Python FastAPI + SQLAlchemy + SQLite |
| MVP 目标 | 核心刷题闭环：答题→判对错→SM-2 复习调度→数据分析 |
| 开发工具 | OpenCode (AI Agent) |
| 代码仓库 | `./backend/` |

## 2. MVP 范围覆盖

### 2.1 核心功能完成清单

| 功能模块 | 状态 | 说明 |
|---------|:----:|------|
| 知识点管理 | ✅ 已完成 | 9 个知识点，覆盖高数/线代/概率，支持分类筛选 |
| 题库管理 | ✅ 已完成 | 15 道示例题（填空+选择题），支持多条件筛选 |
| 顺序/随机练习 | ✅ 已完成 | 通过 `GET /api/practice/next` 获取题目 |
| 答题判对错 | ✅ 已完成 | POST /api/answer 即时反馈正误+解析 |
| SM-2 间隔复习 | ✅ 已完成 | 完整 SM-2 算法实现，动态计算复习间隔 |
| 每日复习计划 | ✅ 已完成 | GET /api/review/due 获取今日待复习题 |
| 错题本 | ✅ 已完成 | GET /api/error-book 获取所有答错题目 |
| 正确率统计 | ✅ 已完成 | 仪表盘 + 趋势图数据 |
| 薄弱知识点分析 | ✅ 已完成 | 按知识点聚合正确率，5 级掌握度判定 |

### 2.2 未实现（非 MVP）

| 功能 | 计划 |
|------|------|
| 用户注册/登录 (JWT) | 第二期 |
| 前端 React 界面 | 第二期 |
| 模拟考试模式 | 第二期 |
| 复习提醒通知 | 第三期 |
| 题目批量导入/导出 | 第三期 |

## 3. 项目结构

```
backend/
├── main.py          # FastAPI 应用入口，所有 API 路由
├── models.py        # SQLAlchemy 数据模型
├── schemas.py       # Pydantic 请求/响应模型
├── database.py      # SQLite 数据库配置
├── sm2.py           # SM-2 间隔重复算法
├── seed.py          # 种子数据填充
└── requirements.txt # 项目依赖
```

## 4. 核心 API 清单

| 方法 | 路径 | 说明 |
|:----:|------|------|
| GET | `/api/knowledge-points` | 知识点列表 |
| GET | `/api/questions` | 题目列表（支持筛选） |
| GET | `/api/questions/{id}` | 题目详情 |
| POST | `/api/answer` | 提交答案 → 判对错 → SM-2 更新 |
| GET | `/api/review/due` | 今日待复习题目 |
| GET | `/api/error-book` | 错题本 |
| GET | `/api/dashboard` | 仪表盘总览 |
| GET | `/api/analysis/weak-points` | 薄弱点分析 |
| GET | `/api/stats/correct-rate-trend` | 正确率趋势 |

## 5. 关键技术实现

### SM-2 间隔重复算法

- 质量评分：根据正确性和答题时间计算 0-5 分
- 间隔计算：正确→递增间隔，错误→重置为1天
- 易度因子更新：EF' = EF + (0.1 - (5-q) * (0.08 + (5-q) * 0.02))

### 薄弱点分析

- 按知识点聚合答题记录
- 正确率 >= 90%: 优秀, >= 75%: 良好, >= 60%: 一般, >= 40%: 薄弱, < 40%: 危险
- 答题不足 3 次的知识点不纳入分析

## 6. 运行方式

```bash
cd backend
pip install -r requirements.txt
python main.py
# API 文档自动生成在 http://localhost:8000/docs
```

## 7. 已知问题

1. 无用户认证，所有操作视为同一用户
2. 前端尚未实现，需通过 API 工具或 curl 调试
3. 种子数据量较少（15 题），仅作演示
