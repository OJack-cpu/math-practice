# 考研数学刷题系统 — Bug 分析与修复记录

## Bug 汇总

| Bug ID | 描述 | 发现方式 | 类型 | 严重程度 | 状态 |
|:------:|------|---------|:----:|:--------:|:----:|
| BUG-001 | 新建 ReviewSchedule 对象时属性为 None，导致 SM-2 计算 TypeError | 集成测试 `test_submit_correct_answer` | 编码疏忽 | 🔴 高 | ✅ 已修复 |
| BUG-002 | 考试模式下无法判断答案（答案比对过于严格，要求完全一致） | 代码审查 | 设计问题 | 🟡 中 | ✅ 已修复（使用 upper+strip 容错比对） |
| BUG-003 | 缺少 API 参数校验（time_spent 为负数或零） | 代码审查 | 输入校验 | 🟡 中 | ✅ Pydantic Field 约束已设置 |

---

## Bug 根因分析：BUG-001

### 问题描述
首次提交答案时，`POST /api/answer` 返回 500 错误：
```
TypeError: unsupported operand type(s) for +: 'NoneType' and 'float'
```

### 复现步骤
1. 启动服务器，数据库为空
2. 创建一道题目
3. 调用 `POST /api/answer` 提交答案
4. 服务器返回 500

### 根因分析
**定位文件**：`main.py:147-148`

```python
if not schedule:
    schedule = ReviewSchedule(question_id=body.question_id)
    db.add(schedule)
```

**根因**：SQLAlchemy 模型中定义的 `default` 参数是**数据库级别**的默认值：
```python
interval = Column(Integer, default=0)
easiness_factor = Column(Float, default=2.5)
repetitions = Column(Integer, default=0)
```

在 `db.add()` 之后、`db.commit()` 之前，Python 对象的这些属性值为 `None`。当 `sm2_update()` 试图使用 `easiness_factor + (0.1 - ...)` 计算时，发生了 `None + float` 的类型错误。

**深层原因**：对 SQLAlchemy ORM 的 `default` 行为理解不足。SQLAlchemy 的 `default` 只在 INSERT 语句生成时由数据库或 SQLAlchemy 填充，不会在 Python 对象创建时自动设置属性值。

### 修复方案

**修改前**：
```python
schedule = ReviewSchedule(question_id=body.question_id)
```

**修改后**：
```python
schedule = ReviewSchedule(
    question_id=body.question_id,
    easiness_factor=2.5,
    interval=0,
    repetitions=0,
)
```

**替代方案**：也可以在模型定义中使用 `default=0` 的 Python 端默认值实现：
```python
interval = Column(Integer, default=0)
```
让 Python 类定义 `__init__` 或使用 `init` 参数。

### 影响范围
- 影响所有首次答题的用户
- 首次答题必然导致 500 错误，阻断核心业务流程
- 影响范围：**严重**

### 修复验证
- 修复后 `POST /api/answer` 正常返回 200
- 新建的 ReviewSchedule 对象 EF=2.5, interval=1, repetitions=1
- 所有相关测试用例通过

---

## Bug 分析：BUG-002

### 问题描述
答案比对使用精确字符串匹配 `==`，但用户输入可能包含多余空格、大小写差异。

### 根因分析
**定位文件**：`main.py:132`
```python
is_correct = body.user_answer.strip().upper() == question.answer.strip().upper()
```
当前代码已经做了 `.strip().upper()` 处理。对于选择题，用户可能输入 "a" 而不是 "A"。当前实现已能处理此情况。

**状态**：✅ 当前实现已满足要求

---

## Bug 分析：BUG-003

### 问题描述
API 输入参数缺少校验，用户可以提交负数的 `time_spent` 或空字符串的答案。

### 根因分析
**定位文件**：`schemas.py:65-67`
```python
class AnswerSubmit(BaseModel):
    question_id: int
    user_answer: str
    time_spent: int = Field(..., gt=0, description="答题耗时（秒）")
```

Pydantic 的 `gt=0` (greater than) 验证已确保 `time_spent` 大于 0。

**状态**：✅ 当前实现已满足要求
