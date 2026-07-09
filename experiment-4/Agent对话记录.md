# 实验四 — Agent 对话记录

## 对话 1：制定编码计划

**用户：**
这是我项目的需求文档和设计文档。MVP 范围定义：
1. 注册/登录
2. 题目录入（管理员）和分类
3. 顺序练习 + 错题重练
4. SM-2 间隔复习调度 + 每日复习计划
5. 正确率统计 + 薄弱知识点识别

技术栈已确定为：后端 FastAPI + SQLAlchemy + SQLite。

请帮我制定编码计划，梳理模块清单和依赖关系。

**Agent：**
根据你的需求，MVP 编码分为 12 个子任务：
1. 项目脚手架（FastAPI 项目初始化）
2. 数据模型定义（4 张核心表）
3. SM-2 算法实现
4. 种子数据填充
5. 知识点 API
6. 题目 API
7. 答题 API（核心业务逻辑）
8. 复习调度 API
9. 错题本 API
10. 仪表盘 API
11. 薄弱点分析 API
12. 正确率趋势 API

推荐编码顺序如上，遵循"数据模型→工具函数→API 端点"的依赖顺序。

---

## 对话 2：搭建项目脚手架

**用户：**
请帮我搭建项目脚手架。后端用 FastAPI + SQLAlchemy + SQLite。

**Agent：**
已创建项目结构：
- `database.py` — SQLite 连接配置
- `models.py` — SQLAlchemy 模型（KnowledgePoint, Question, AnswerRecord, ReviewSchedule）
- `schemas.py` — Pydantic 模型
- `requirements.txt` — 依赖清单
- 使用 `uvicorn` 作为服务器

---

## 对话 3：实现 SM-2 算法

**用户：**
请实现 SM-2 间隔重复算法。核心公式：
- 质量评分 0-5
- quality < 3: 重置间隔为 1 天
- quality >= 3: interval 按公式递增
- 易度因子 EF 更新公式

**Agent：**
已实现 `sm2.py`，包含：
- `calculate_quality()` — 根据正确性和耗时计算质量分
- `sm2_update()` — 核心算法，返回新的 EF、间隔、下次复习日期
- 附演示脚本验证算法正确性

---

## 对话 4：实现核心 API

**用户：**
请实现答题 API。POST /api/answer 接收 question_id, user_answer, time_spent。
业务逻辑：
1. 查找题目
2. 比对答案
3. 保存答题记录
4. 创建或更新 SM-2 复习调度
5. 返回正误结果和解析

**Agent：**
已实现。同时实现了知识点 API、题目 API、复习调度 API、仪表盘 API 等全部端点。

---

## 对话 5：Bug 修复

**用户：**
POST /api/answer 报错：`TypeError: unsupported operand type(s) for +: 'NoneType' and 'float'`

**Agent：**
问题根因：新建 ReviewSchedule 对象时未传递 easiness_factor 等默认值，SQLAlchemy 的 default 参数在 flush 前不生效。
修复：在构造函数中显式传递默认值 `easiness_factor=2.5, interval=0, repetitions=0`。

---

## 对话 6：种子数据

**用户：**
请填充示例数据，包含考研数学三大科目（高数、线代、概率）的知识点和题目。

**Agent：**
已创建 `seed.py`，包含：
- 9 个知识点（极限与连续、导数与微分、积分学、多元微分、行列式、矩阵、线性方程组、概率论、随机变量）
- 15 道示例题目（填空题 + 选择题）
- 覆盖各难度等级的知识点练习
