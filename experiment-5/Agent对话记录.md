# 实验五 — Agent 对话记录

## 对话 1：制定测试策略

**用户：**
这是我在实验四完成的 MVP 项目（考研数学刷题系统），后端用 FastAPI + SQLAlchemy + SQLite。
主要模块：
1. SM-2 算法模块（sm2.py）
2. 知识点 API
3. 题目 API
4. 答题 API（核心）
5. 复习调度 API
6. 仪表盘 API
7. 错题本 API
8. 薄弱点分析 API
9. 正确率趋势 API

请帮我分析代码结构，并制定测试策略。

**Agent：**
代码分析：
- `sm2.py` 是纯函数，无外部依赖，非常适合单元测试
- 其他模块都通过 main.py 的路由暴露为 HTTP API，适合集成测试
- 核心业务逻辑在答题 API（submit_answer），涉及判对错 + SM-2 联动

测试策略建议：
1. SM-2 算法 → 单元测试（19 个用例，覆盖正常/边界/异常）
2. 所有 API → 集成测试（14 个用例，覆盖成功/失败场景）
3. 测试框架：pytest + requests

---

## 对话 2：编写 SM-2 单元测试

**用户：**
请为 sm2.py 编写单元测试，覆盖以下场景：
1. 正常场景：各种正确/错误组合下的质量评分
2. 边界条件：时间等于临界值
3. 异常场景：EF 下限保护
4. 每个测试函数要有清晰描述

**Agent：**
已创建 `tests/test_sm2.py`，包含 19 个测试用例：
- TestCalculateQuality 类（8 个用例）：测试 quality 评分
- TestSm2Update 类（11 个用例）：测试间隔更新逻辑
- 覆盖了 EF 下限保护、repetitions 归零、默认参数等

---

## 对话 3：编写 API 集成测试

**用户：**
请为 API 端点编写集成测试。使用 requests 库直接测试实际 HTTP 接口。

**Agent：**
已创建 `tests/test_api_integration.py`，包含 14 个测试用例：
- 知识点 API：列表、分类筛选（2 用例）
- 题目 API：列表、筛选、详情、不存在返回 404（4 用例）
- 答题 API：正确/错误/不存在题目（3 用例）
- 仪表盘 API：数据完整性（1 用例）
- 复习调度 API：数据结构（1 用例）
- 错题本 API：数据结构（1 用例）
- 薄弱点分析 API：数据结构（1 用例）
- 正确率趋势 API：数据完整（1 用例）

---

## 对话 4：Bug 分析和修复

**用户：**
测试发现 `POST /api/answer` 首次提交时返回 500 错误：
```
TypeError: unsupported operand type(s) for +: 'NoneType' and 'float'
```
请分析根因并修复。

**Agent：**
根因定位：`main.py` 中创建 `ReviewSchedule` 对象时未传递 SM-2 参数默认值。

SQLAlchemy 的 `default` 参数在 flush 前不生效，导致 `easiness_factor`、`interval`、`repetitions` 属性为 None。

修复方案：在构造函数中显式传递默认值：
```python
schedule = ReviewSchedule(
    question_id=...,
    easiness_factor=2.5,
    interval=0,
    repetitions=0,
)
```

修复后所有测试通过。

---

## 对话 5：运行全部测试

**用户：**
请运行全部测试，验证修复效果。

**Agent：**
运行结果：
```
tests/test_sm2.py ................... 19 passed
tests/test_api_integration.py .............. 14 passed
================================== 33 passed in 0.30s ==================================
```

全部 33 个测试用例通过，通过率 100%。Bug 修复验证成功。
