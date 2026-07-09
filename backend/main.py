"""
考研数学刷题系统 —— FastAPI 后端服务

启动方式:
    cd backend
    pip install -r requirements.txt
    python main.py

API 文档自动生成: http://localhost:8000/docs
"""
import os
from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, case, and_, desc
from datetime import datetime, timedelta
from typing import List, Optional

import re
from database import get_db, init_db
from models import KnowledgePoint, Question, AnswerRecord, ReviewSchedule
from schemas import (
    KnowledgePointOut, KnowledgePointStats,
    QuestionOut, QuestionWithSchedule,
    AnswerSubmit, AnswerResult, ReviewScheduleOut,
    DashboardData, DailyStats,
)
from sm2 import calculate_quality, sm2_update
import seed


def _normalize_answer(ans: str) -> str:
    """宽松的答案归一化：去空格+去LaTeX符号+统一大小写"""
    ans = ans.strip()
    ans = ans.replace('$', '').replace('\\', '')
    ans = re.sub(r'\s+', '', ans)  # 去所有空白
    # 统一乘法符号
    ans = ans.replace('×', '*').replace('x', '*').replace('X', '*')
    ans = ans.replace('^', '^')
    # 统一括号
    ans = ans.replace('（', '(').replace('）', ')')
    ans = ans.replace('，', ',').replace('；', ';')
    return ans.lower()

app = FastAPI(
    title="考研数学刷题系统",
    description="智能错题本 + 间隔复习 + 薄弱点分析 + 数据可视化",
    version="1.0.0",
)

# CORS：允许前端跨域访问
# 通过环境变量 ALLOWED_ORIGINS 配置允许的域名，逗号分隔；默认允许本地开发地址
_cors_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173,http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in _cors_origins],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── 启动时初始化 ──
@app.on_event("startup")
def startup():
    init_db()
    # 如果数据库为空，自动填充示例数据
    db = next(get_db())
    if db.query(KnowledgePoint).count() == 0:
        seed.seed_all(db)
    db.close()


# ═══════════════════════════════════════════
#  知识点 API
# ═══════════════════════════════════════════

@app.get("/api/knowledge-points", response_model=List[KnowledgePointOut])
def list_knowledge_points(
    category: Optional[str] = Query(None, description="按大类筛选"),
    db: Session = Depends(get_db),
):
    """获取知识点列表，可按大类筛选"""
    q = db.query(KnowledgePoint)
    if category:
        q = q.filter(KnowledgePoint.category == category)
    return q.all()


# ═══════════════════════════════════════════
#  题目 API
# ═══════════════════════════════════════════

@app.get("/api/questions", response_model=List[QuestionOut])
def list_questions(
    knowledge_point_id: Optional[int] = None,
    difficulty: Optional[int] = None,
    category: Optional[str] = None,
    limit: int = Query(default=10, ge=1, le=50),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
):
    """
    获取题目列表，支持多条件筛选
    例: /api/questions?category=高等数学&difficulty=3
    """
    q = db.query(Question).options(joinedload(Question.knowledge_point))

    if knowledge_point_id:
        q = q.filter(Question.knowledge_point_id == knowledge_point_id)
    if difficulty:
        q = q.filter(Question.difficulty == difficulty)
    if category:
        q = q.join(KnowledgePoint).filter(KnowledgePoint.category == category)

    return q.offset(offset).limit(limit).all()


@app.get("/api/questions/{question_id}", response_model=QuestionOut)
def get_question(question_id: int, db: Session = Depends(get_db)):
    """获取单个题目详情"""
    q = db.query(Question)\
        .options(joinedload(Question.knowledge_point))\
        .filter(Question.id == question_id)\
        .first()
    if not q:
        raise HTTPException(status_code=404, detail="题目不存在")
    return q


# ═══════════════════════════════════════════
#  答题 API（核心：SM-2 算法集成点）
# ═══════════════════════════════════════════

@app.post("/api/answer", response_model=AnswerResult)
def submit_answer(body: AnswerSubmit, db: Session = Depends(get_db)):
    """
    提交答案 → 判对错 → 记录 → 更新 SM-2 复习计划

    这是系统的核心接口，每次答题都会：
      1. 判断正误
      2. 保存答题记录
      3. 用 SM-2 算法计算下次复习时间
      4. 返回解析和复习信息
    """
    question = db.query(Question).filter(Question.id == body.question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="题目不存在")

    #  智能判题：对填空题做宽松匹配
    user_ans = _normalize_answer(body.user_answer)
    correct_ans = _normalize_answer(question.answer)
    is_correct = user_ans == correct_ans

    #  ① 保存答题记录
    record = AnswerRecord(
        question_id=body.question_id,
        user_answer=body.user_answer,
        is_correct=is_correct,
        time_spent=body.time_spent,
    )
    db.add(record)

    # ② 获取或创建复习调度
    schedule = db.query(ReviewSchedule)\
        .filter(ReviewSchedule.question_id == body.question_id)\
        .first()
    if not schedule:
        schedule = ReviewSchedule(
            question_id=body.question_id,
            easiness_factor=2.5, interval=0, repetitions=0,
        )
        db.add(schedule)

    # ③ SM-2 算法：计算质量 & 更新调度
    quality = calculate_quality(is_correct, body.time_spent)
    updated = sm2_update(
        quality=quality,
        easiness_factor=schedule.easiness_factor,
        interval=schedule.interval,
        repetitions=schedule.repetitions,
    )

    schedule.easiness_factor = updated["easiness_factor"]
    schedule.interval = updated["interval"]
    schedule.repetitions = updated["repetitions"]
    schedule.next_review_date = datetime.fromisoformat(updated["next_review_date"])
    schedule.last_review_date = datetime.utcnow()

    db.commit()
    db.refresh(schedule)

    return AnswerResult(
        is_correct=is_correct,
        correct_answer=question.answer,
        explanation=question.explanation,
        review_info=ReviewScheduleOut.model_validate(schedule),
    )


# ═══════════════════════════════════════════
#  复习调度 API
# ═══════════════════════════════════════════

@app.get("/api/review/due", response_model=List[QuestionWithSchedule])
def get_due_reviews(
    limit: int = Query(default=20, ge=1, le=50),
    db: Session = Depends(get_db),
):
    """
    获取今天需要复习的题目列表
    条件：next_review_date <= 现在
    """
    now = datetime.utcnow()
    schedules = db.query(ReviewSchedule)\
        .filter(ReviewSchedule.next_review_date <= now)\
        .limit(limit)\
        .all()

    result = []
    for s in schedules:
        q = db.query(Question)\
            .options(joinedload(Question.knowledge_point))\
            .filter(Question.id == s.question_id)\
            .first()
        if q:
            q_out = QuestionWithSchedule.model_validate(q)
            q_out.review_schedule = ReviewScheduleOut.model_validate(s)
            result.append(q_out)
    return result


# ═══════════════════════════════════════════
#  错题本 API
# ═══════════════════════════════════════════

@app.get("/api/error-book", response_model=List[QuestionOut])
def get_error_book(
    limit: int = Query(default=20, ge=1, le=50),
    db: Session = Depends(get_db),
):
    """
    获取错题本：所有答错过的题目（去重）
    按最近错误时间排序
    """
    # 找出所有答错过的 question_id
    subq = db.query(
        AnswerRecord.question_id,
        func.max(AnswerRecord.created_at).label("last_error")
    ).filter(
        AnswerRecord.is_correct == False
    ).group_by(AnswerRecord.question_id).subquery()

    questions = db.query(Question)\
        .options(joinedload(Question.knowledge_point))\
        .join(subq, Question.id == subq.c.question_id)\
        .order_by(subq.c.last_error.desc())\
        .limit(limit)\
        .all()

    return questions


# ═══════════════════════════════════════════
#  仪表盘 / 数据可视化 API
# ═══════════════════════════════════════════

@app.get("/api/dashboard", response_model=DashboardData)
def get_dashboard(db: Session = Depends(get_db)):
    """
    仪表盘数据，一次请求返回前端需要展示的所有统计信息：
      - 总览数字
      - 每日学习折线图数据
      - 知识点掌握度雷达图数据
    """
    now = datetime.utcnow()
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)

    # 总览数据
    total_questions = db.query(Question).count()
    total_answers = db.query(AnswerRecord).count()
    overall_accuracy = db.query(
        func.avg(case((AnswerRecord.is_correct == True, 1), else_=0))
    ).scalar() or 0

    today_records = db.query(AnswerRecord)\
        .filter(AnswerRecord.created_at >= today_start)
    today_questions = today_records.count()
    today_accuracy = db.query(
        func.avg(case((AnswerRecord.is_correct == True, 1), else_=0))
    ).filter(AnswerRecord.created_at >= today_start).scalar() or 0

    review_due = db.query(ReviewSchedule)\
        .filter(ReviewSchedule.next_review_date <= now)\
        .count()

    # 每日统计（最近14天）
    daily_stats = []
    for i in range(13, -1, -1):
        day_start = (now - timedelta(days=i)).replace(hour=0, minute=0, second=0, microsecond=0)
        day_end = day_start + timedelta(days=1)
        day_records = db.query(AnswerRecord)\
            .filter(AnswerRecord.created_at >= day_start, AnswerRecord.created_at < day_end)
        total = day_records.count()
        correct = day_records.filter(AnswerRecord.is_correct == True).count()
        daily_stats.append(DailyStats(
            date=day_start.strftime("%m-%d"),
            total_questions=total,
            correct_count=correct,
            accuracy=correct / total if total > 0 else 0,
        ))

    # 知识点统计（薄弱点分析数据源）—— 单次 SQL 聚合，避免 N+1
    kp_stats = []
    stats_rows = db.query(
        KnowledgePoint.id,
        KnowledgePoint.name,
        KnowledgePoint.category,
        func.count(AnswerRecord.id).label("total_attempts"),
        func.sum(case((AnswerRecord.is_correct == True, 1), else_=0)).label("correct_count"),
        func.avg(AnswerRecord.time_spent).label("avg_time"),
    ).outerjoin(Question, Question.knowledge_point_id == KnowledgePoint.id)\
     .outerjoin(AnswerRecord, AnswerRecord.question_id == Question.id)\
     .group_by(KnowledgePoint.id, KnowledgePoint.name, KnowledgePoint.category)\
     .all()

    for row in stats_rows:
        total = row.total_attempts or 0
        correct = row.correct_count or 0
        avg_time = round(row.avg_time or 0, 1)
        accuracy = correct / total if total > 0 else 0

        if accuracy >= 0.9:
            level = "优秀"
        elif accuracy >= 0.75:
            level = "良好"
        elif accuracy >= 0.6:
            level = "一般"
        elif accuracy >= 0.4:
            level = "薄弱"
        else:
            level = "危险"

        kp_stats.append(KnowledgePointStats(
            id=row.id,
            name=row.name,
            category=row.category,
            total_attempts=total,
            correct_count=correct,
            accuracy=round(accuracy, 2),
            avg_time_spent=avg_time,
            level=level,
        ))

    return DashboardData(
        total_questions=total_questions,
        total_answers=total_answers,
        overall_accuracy=round(overall_accuracy, 2),
        today_questions=today_questions,
        today_accuracy=round(today_accuracy, 2),
        review_due_count=review_due,
        daily_stats=daily_stats,
        knowledge_stats=kp_stats,
    )


# ═══════════════════════════════════════════
#  薄弱点分析 API
# ═══════════════════════════════════════════

@app.get("/api/analysis/weak-points", response_model=List[KnowledgePointStats])
def get_weak_points(
    min_attempts: int = Query(default=3, description="最少答题次数才纳入分析"),
    db: Session = Depends(get_db),
):
    """
    薄弱点分析：返回所有知识点的掌握情况
    可按正确率升序排列，最薄弱的排最前
    """
    # 单次 SQL 聚合：按知识点统计，HAVING 过滤答题不足的知识点，避免 N+1
    stats_rows = db.query(
        KnowledgePoint.id,
        KnowledgePoint.name,
        KnowledgePoint.category,
        func.count(AnswerRecord.id).label("total_attempts"),
        func.sum(case((AnswerRecord.is_correct == True, 1), else_=0)).label("correct_count"),
        func.avg(AnswerRecord.time_spent).label("avg_time"),
    ).outerjoin(Question, Question.knowledge_point_id == KnowledgePoint.id)\
     .outerjoin(AnswerRecord, AnswerRecord.question_id == Question.id)\
     .group_by(KnowledgePoint.id, KnowledgePoint.name, KnowledgePoint.category)\
     .having(func.count(AnswerRecord.id) >= min_attempts)\
     .all()

    stats = []
    for row in stats_rows:
        total = row.total_attempts or 0
        correct = row.correct_count or 0
        avg_time = round(row.avg_time or 0, 1)
        accuracy = correct / total if total > 0 else 0

        if accuracy >= 0.9:
            level = "优秀"
        elif accuracy >= 0.75:
            level = "良好"
        elif accuracy >= 0.6:
            level = "一般"
        elif accuracy >= 0.4:
            level = "薄弱"
        else:
            level = "危险"

        stats.append(KnowledgePointStats(
            id=row.id,
            name=row.name,
            category=row.category,
            total_attempts=total,
            correct_count=correct,
            accuracy=round(accuracy, 2),
            avg_time_spent=avg_time,
            level=level,
        ))

    # 按正确率升序 → 薄弱排前面
    stats.sort(key=lambda x: x.accuracy)
    return stats


# ═══════════════════════════════════════════
#  复习统计 API
# ═══════════════════════════════════════════

@app.get("/api/stats/correct-rate-trend")
def get_correct_rate_trend(
    days: int = Query(default=14, ge=1, le=60),
    db: Session = Depends(get_db),
):
    """正确率趋势图数据"""
    now = datetime.utcnow()
    trend = []
    for i in range(days - 1, -1, -1):
        day_start = (now - timedelta(days=i)).replace(hour=0, minute=0, second=0, microsecond=0)
        day_end = day_start + timedelta(days=1)
        records = db.query(AnswerRecord)\
            .filter(AnswerRecord.created_at >= day_start, AnswerRecord.created_at < day_end)
        total = records.count()
        correct = records.filter(AnswerRecord.is_correct == True).count()
        trend.append({
            "date": day_start.strftime("%m-%d"),
            "accuracy": round(correct / total, 2) if total > 0 else 0,
            "total": total,
        })
    return trend


if __name__ == "__main__":
    import uvicorn
    _reload = os.getenv("ENV", "").lower() == "development"
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=_reload)
