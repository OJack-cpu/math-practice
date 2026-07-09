# MVP 编码实现报告 —— 考研数学刷题系统

## 一、项目概述

本项目是一个面向考研数学备考学生的**智能刷题系统**，核心功能包括：

- **智能错题本**：自动收集错题，按知识点分类
- **间隔复习**：SM-2 算法动态调度，根据答题质量自动计算下次复习时间
- **薄弱点分析**：按知识点聚合正确率，自动生成薄弱报告
- **数据可视化**：ECharts 驱动的学习仪表盘

| 维度 | 说明 |
|------|------|
| **后端框架** | Python FastAPI 0.104.1 |
| **前端框架** | React 19 + Vite 8 |
| **UI 框架** | Ant Design 6.5 |
| **数据库** | SQLite + SQLAlchemy 2.0 |
| **算法** | SM-2 间隔重复 |
| **公式渲染** | KaTeX |
| **图表库** | ECharts 6 |
| **测试框架** | pytest + httpx |

## 二、模块清单

### 后端模块（/backend/）

| 文件 | 行数 | 功能说明 |
|------|------|----------|
| `main.py` | 430 | FastAPI 主应用，15 个 API 路由 |
| `models.py` | 82 | SQLAlchemy 数据模型（4 张表，含外键和关系映射） |
| `schemas.py` | 103 | Pydantic 请求/响应模型（前后端通信契约） |
| `database.py` | 27 | 数据库连接配置、会话管理、初始化 |
| `sm2.py` | 98 | SM-2 间隔重复算法（含演示脚本） |
| `seed.py` | 278 | 种子数据生成（20 个知识点，57 道考研真题风格题目） |
| `tests/test_sm2.py` | 140 | SM-2 算法单元测试（20 个用例） |
| `tests/test_api_integration.py` | 220 | API 集成测试（13 个用例） |

### 前端模块（/frontend/src/）

| 文件 | 功能说明 |
|------|----------|
| `App.jsx` | 路由配置 + Ant Design 主题（暗色 + 紫色主色调） |
| `components/AppLayout.jsx` | 全局布局（侧边导航 + 内容区） |
| `components/MathText.jsx` | LaTeX 数学公式渲染组件 |
| `components/AccuracyChart.jsx` | ECharts 正确率趋势折线图 |
| `components/KpRadar.jsx` | ECharts 知识点掌握度雷达图 |
| `pages/Dashboard.jsx` | 学习仪表盘总览 |
| `pages/Practice.jsx` | 刷题练习页（卡片翻转动效） |
| `pages/Review.jsx` | 间隔复习（SM-2 自评打分） |
| `pages/ErrorBook.jsx` | 错题本 |
| `pages/WeakPoints.jsx` | 薄弱点分析表格 |
| `services/api.js` | Axios API 客户端（9 个 API 函数） |

## 三、数据库设计

### ER 图（四表关系）

```
knowledge_points (1) ──→ (N) questions (1) ──→ (N) answer_records
                                          │
                                          └──→ (1) review_schedules
```

### 表结构

**knowledge_points（知识点标签表）**
| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer (PK) | 主键 |
| name | String(50) | 知识点名称 |
| category | String(20) | 分类（高等数学/线性代数/概率论） |
| description | String(200) | 描述 |

**questions（题目表）**
| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer (PK) | 主键 |
| content | Text | 题干（支持 LaTeX） |
| question_type | String(20) | 题型（single_choice/fill_blank） |
| options | JSON | 选项列表 |
| answer | String(50) | 正确答案 |
| explanation | Text | 解析 |
| difficulty | Integer | 难度 1~5 |
| knowledge_point_id | Integer (FK) | 外键关联知识点 |

**answer_records（答题记录表）**
| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer (PK) | 主键 |
| question_id | Integer (FK) | 题目 ID |
| user_answer | String(50) | 用户答案 |
| is_correct | Boolean | 是否正确 |
| time_spent | Integer | 耗时（秒） |
| created_at | DateTime | 答题时间 |

**review_schedules（复习调度表）**
| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer (PK) | 主键 |
| question_id | Integer (FK, UNIQUE) | 题目 ID（一对一） |
| easiness_factor | Float | 难易度因子 EF（≥1.3） |
| interval | Integer | 复习间隔（天） |
| repetitions | Integer | 连续正确次数 |
| next_review_date | DateTime | 下次复习日期 |

## 四、核心算法实现

### SM-2 间隔重复算法

```
输入：quality (0~5)、当前 EF、interval、repetitions
输出：新 EF、新 interval、新 repetitions、next_review_date

if quality < 3:
    repetitions = 0, interval = 1
else:
    repetitions += 1
    if repetitions == 1: interval = 1
    elif repetitions == 2: interval = 6
    else: interval = round(interval * EF)

EF' = EF + (0.1 - (5-q)*(0.08 + (5-q)*0.02))
EF' = max(EF', 1.3)
```

### 质量评分策略

| 正确 | 速度 | 质量分 | 含义 |
|------|------|--------|------|
| ✓ | 快（< 30s） | 5 | 完美回忆 |
| ✓ | 正常（30~90s） | 4 | 良好 |
| ✓ | 慢（> 90s） | 3 | 费力 |
| ✗ | 快 | 2 | 粗心错误 |
| ✗ | 正常 | 1 | 不熟悉 |
| ✗ | 慢 | 0 | 完全不会 |

## 五、API 接口清单

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/knowledge-points` | 知识点列表 |
| GET | `/api/questions` | 题目列表（筛选） |
| GET | `/api/questions/{id}` | 题目详情 |
| POST | `/api/answer` | 提交答案 |
| GET | `/api/review/due` | 待复习题目 |
| GET | `/api/error-book` | 错题本 |
| GET | `/api/dashboard` | 仪表盘数据 |
| GET | `/api/analysis/weak-points` | 薄弱点分析 |
| GET | `/api/stats/correct-rate-trend` | 正确率趋势 |

## 六、测试覆盖

| 测试类别 | 用例数 | 覆盖模块 |
|----------|--------|----------|
| SM-2 算法单元测试 | 20 | 质量计算 + 调度更新 |
| API 集成测试 | 13 | 全部 9 个接口 |
| **总计** | **33** | **100% 通过** |

## 七、代码量统计

| 类型 | 数量 |
|------|------|
| 后端 Python 代码 | ~1,300 行 |
| 前端 React/JSX 代码 | ~1,000 行 |
| 测试代码 | ~360 行 |
| 种子数据 | ~280 行（57 题） |
| **总计** | **~2,940 行** |
