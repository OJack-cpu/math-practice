"""API 集成测试"""
import pytest
import requests


@pytest.fixture(scope="module")
def base(server_url):
    return server_url


class TestAPI:
    def test_knowledge_points_list(self, base):
        res = requests.get(f"{base}/api/knowledge-points")
        assert res.status_code == 200
        data = res.json()
        assert isinstance(data, list) and len(data) > 0
        assert "name" in data[0]

    def test_knowledge_points_filter(self, base):
        res = requests.get(f"{base}/api/knowledge-points?category=高等数学")
        assert res.status_code == 200
        for kp in res.json():
            assert kp["category"] == "高等数学"

    def test_questions_list(self, base):
        res = requests.get(f"{base}/api/questions?limit=5")
        assert res.status_code == 200
        assert len(res.json()) <= 5

    def test_questions_filter_by_kp(self, base):
        kps = requests.get(f"{base}/api/knowledge-points").json()
        if kps:
            kp_id = kps[0]["id"]
            res = requests.get(f"{base}/api/questions?knowledge_point_id={kp_id}")
            assert res.status_code == 200
            for q in res.json():
                assert q["knowledge_point"]["id"] == kp_id

    def test_get_question_by_id(self, base):
        questions = requests.get(f"{base}/api/questions?limit=1").json()
        if questions:
            qid = questions[0]["id"]
            res = requests.get(f"{base}/api/questions/{qid}")
            assert res.status_code == 200
            assert res.json()["id"] == qid

    def test_get_nonexistent_question(self, base):
        res = requests.get(f"{base}/api/questions/99999")
        assert res.status_code == 404

    def test_submit_correct_answer(self, base):
        questions = requests.get(f"{base}/api/questions?limit=1").json()
        if questions:
            q = questions[0]
            res = requests.post(f"{base}/api/answer", json={
                "question_id": q["id"], "user_answer": "3", "time_spent": 15,
            })
            assert res.status_code == 200
            assert "is_correct" in res.json()

    def test_submit_wrong_answer(self, base):
        questions = requests.get(f"{base}/api/questions?limit=1").json()
        if questions:
            q = questions[0]
            res = requests.post(f"{base}/api/answer", json={
                "question_id": q["id"], "user_answer": "WRONG", "time_spent": 30,
            })
            assert res.status_code == 200
            assert res.json()["is_correct"] is False

    def test_submit_nonexistent_question(self, base):
        res = requests.post(f"{base}/api/answer", json={
            "question_id": 99999, "user_answer": "test", "time_spent": 10,
        })
        assert res.status_code == 404

    def test_dashboard(self, base):
        res = requests.get(f"{base}/api/dashboard")
        assert res.status_code == 200
        data = res.json()
        for k in ["total_questions", "total_answers", "overall_accuracy", "daily_stats", "knowledge_stats"]:
            assert k in data

    def test_review_due(self, base):
        res = requests.get(f"{base}/api/review/due")
        assert res.status_code == 200
        assert isinstance(res.json(), list)

    def test_error_book(self, base):
        res = requests.get(f"{base}/api/error-book")
        assert res.status_code == 200
        assert isinstance(res.json(), list)

    def test_weak_points(self, base):
        res = requests.get(f"{base}/api/analysis/weak-points")
        assert res.status_code == 200
        assert isinstance(res.json(), list)

    def test_correct_rate_trend(self, base):
        res = requests.get(f"{base}/api/stats/correct-rate-trend?days=7")
        assert res.status_code == 200
        data = res.json()
        assert len(data) == 7
        for d in data:
            assert "date" in d and "accuracy" in d
