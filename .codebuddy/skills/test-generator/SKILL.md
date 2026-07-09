# Test Generator Skill

## 用途

为考研数学刷题系统的后端 API 自动生成 pytest 测试用例。

---

## 测试框架与约定

- 测试框架: pytest
- 数据库: 每个测试使用独立的 SQLite 临时数据库（`conftest.py` 中的 fixture）
- API 测试: 使用 FastAPI `TestClient`
- 测试文件位置: `backend/tests/`

## 测试数据库 Fixture

`conftest.py` 中已提供：
- `test_db` fixture: 创建独立 SQLite 内存数据库，自动建表 + 填充种子数据
- `client` fixture: 基于 test_db 的 FastAPI TestClient，覆盖 `get_db` 依赖

## 测试模式

### 1. 知识点 API 测试
```python
def test_list_knowledge_points(client):
    resp = client.get("/api/knowledge-points")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) > 0
    assert "name" in data[0]
    assert "category" in data[0]

def test_filter_by_category(client):
    resp = client.get("/api/knowledge-points?category=高等数学")
    assert resp.status_code == 200
    for kp in resp.json():
        assert kp["category"] == "高等数学"
```

### 2. 题目 API 测试
```python
def test_list_questions(client):
    resp = client.get("/api/questions")
    assert resp.status_code == 200
    assert len(resp.json()) <= 10  # 默认 limit

def test_get_question_detail(client):
    resp = client.get("/api/questions/1")
    assert resp.status_code == 200
    assert "explanation" in resp.json()

def test_question_not_found(client):
    resp = client.get("/api/questions/99999")
    assert resp.status_code == 404
```

### 3. 答题 API 测试（SM-2 核心）
```python
def test_submit_correct_answer(client):
    resp = client.post("/api/answer", json={
        "question_id": 1,
        "user_answer": "3",
        "time_spent": 30
    })
    assert resp.status_code == 200
    data = resp.json()
    assert data["is_correct"] == True
    assert "review_info" in data

def test_submit_wrong_answer(client):
    resp = client.post("/api/answer", json={
        "question_id": 1,
        "user_answer": "999",
        "time_spent": 60
    })
    assert resp.status_code == 200
    data = resp.json()
    assert data["is_correct"] == False
```

### 4. 仪表盘 API 测试
```python
def test_dashboard(client):
    resp = client.get("/api/dashboard")
    assert resp.status_code == 200
    data = resp.json()
    assert "total_questions" in data
    assert "overall_accuracy" in data
    assert "daily_stats" in data
    assert "knowledge_stats" in data
```

### 5. 错误处理测试
```python
def test_missing_question_id(client):
    resp = client.post("/api/answer", json={
        "user_answer": "3",
        "time_spent": 30
    })
    assert resp.status_code == 422  # Pydantic 验证错误
```

## 生成测试时的注意事项

1. **种子数据已知**: 题目1 的答案是 `"3"`（极限题），题目91 的答案是 `"B"`（选择题）
2. **填空题答案归一化**: 后端使用 `_normalize_answer` 函数，会去除空白/LaTeX符号/统一大小写
3. **SM-2 状态**: 首次答题会**自动创建** ReviewSchedule，无需手动准备
4. **测试隔离**: 每个测试函数独立运行，不依赖其他测试的状态
5. **覆盖目标**: 每个 API 端点至少 1 个正常路径 + 1 个边界/错误路径
