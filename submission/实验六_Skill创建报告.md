# 实验六 模块一：Skill 创建报告

## 概述

本模块为考研数学刷题系统创建了两个 CodeBuddy Skill，用于提升 AI 辅助开发的效率和质量。

## Skill 1: project-context（项目上下文）

### 文件位置
`.codebuddy/skills/project-context/SKILL.md`

### 功能描述
为 AI 助手提供项目的完整上下文信息，包括：

- **技术栈全景**：FastAPI + React + PostgreSQL + Docker
- **项目结构**：backend/ 和 frontend/ 的目录树
- **核心数据模型**：4 张数据库表的字段、关系和用途
- **SM-2 算法**：间隔重复算法的核心逻辑说明
- **API 路由汇总**：9 个 API 端点的完整列表和方法/路径
- **环境变量**：DATABASE_URL、ALLOWED_ORIGINS、ENV 的说明
- **代码公约**：Python PEP 8、React 函数组件规范

### 使用场景

当开发者需要 AI 帮助以下操作时，加载此 Skill：
- 添加新功能（API 端点、页面组件）
- 修复 Bug（了解现有逻辑）
- 代码重构（了解架构约定）
- 新人上手项目

### 覆盖内容

| 类别 | 内容 |
|------|------|
| 架构 | 三层架构（前端 → Nginx → FastAPI → PostgreSQL） |
| 后端 | main.py、models.py、schemas.py、sm2.py、seed.py |
| 前端 | React 页面路由、组件树、数据流 |
| 基础设施 | Docker 多服务编排、环境变量配置 |

---

## Skill 2: test-generator（测试生成器）

### 文件位置
`.codebuddy/skills/test-generator/SKILL.md`

### 功能描述
自动为后端 API 端点生成 pytest 测试用例，包括：

- **测试框架约定**：pytest + SQLite 内存数据库 + FastAPI TestClient
- **Fixture 说明**：test_db 和 client 的用法
- **5 种测试模式**：
  1. 知识点 API 测试（列表、分类筛选）
  2. 题目 API 测试（列表、详情、404 边界）
  3. 答题 API 测试（正确/错误提交、SM-2 状态验证）
  4. 仪表盘 API 测试（数据结构验证）
  5. 错误处理测试（Pydantic 验证、非法参数）

### 使用场景

当开发者需要：
- 为新 API 端点生成测试
- 补充现有端点的测试覆盖率
- 检查边界条件和错误处理

### 关键约定

- 题目 1 答案是 `"3"`（极限题），可用作正确提交
- 后端 `_normalize_answer` 会做归一化处理（去空白、统一大小写）
- 首次答题会自动创建 ReviewSchedule
- 每个测试独立运行，无状态依赖

---

## 创建过程

1. 分析项目结构，提取关键信息（main.py、models.py、Dockerfile 等）
2. 编写 project-context Skill，覆盖全部技术栈和 API 路由
3. 阅读现有测试文件（conftest.py）理解测试约定
4. 编写 test-generator Skill，提供可复用的测试模板
5. 验证两个 Skill 的准确性和完整性

---

## 结论

两个 Skill 已成功创建，分别覆盖「项目全貌理解」和「自动化测试生成」两个高频场景，可显著提升 AI 辅助开发的效率和准确性。
