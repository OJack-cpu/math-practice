"""
Pydantic 模型 —— 定义 API 的请求和响应格式

这是前后端通信的"契约"：
  - 前端按这个格式发请求
  - 后端按这个格式返回数据
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


# ═══════════════════════════════════════════
#  知识点
# ═══════════════════════════════════════════

class KnowledgePointOut(BaseModel):
    """知识点输出"""
    id: int
    name: str
    category: str
    description: Optional[str] = None

    class Config:
        from_attributes = True


class KnowledgePointStats(BaseModel):
    """知识点统计（用于薄弱点分析）"""
    id: int
    name: str
    category: str
    total_attempts: int      # 总答题次数
    correct_count: int       # 正确次数
    accuracy: float          # 正确率 0~1
    avg_time_spent: float    # 平均耗时（秒）
    level: str               # 掌握等级：优秀/良好/一般/薄弱/危险


# ═══════════════════════════════════════════
#  题目
# ═══════════════════════════════════════════

class QuestionOut(BaseModel):
    """题目输出（不含答案，用于前端展示）"""
    id: int
    content: str
    question_type: str
    options: Optional[list] = None
    difficulty: int
    source: Optional[str] = None
    knowledge_point: Optional[KnowledgePointOut] = None

    class Config:
        from_attributes = True


class QuestionWithSchedule(QuestionOut):
    """带复习调度信息的题目"""
    review_schedule: Optional["ReviewScheduleOut"] = None


class AnswerSubmit(BaseModel):
    """提交答案的请求体"""
    question_id: int
    user_answer: str
    time_spent: int = Field(..., gt=0, description="答题耗时（秒）")


class AnswerResult(BaseModel):
    """提交答案后的响应"""
    is_correct: bool
    correct_answer: str
    explanation: Optional[str] = None
    review_info: "ReviewScheduleOut"


# ═══════════════════════════════════════════
#  复习调度
# ═══════════════════════════════════════════

class ReviewScheduleOut(BaseModel):
    """复习调度输出"""
    id: int
    question_id: int
    easiness_factor: float
    interval: int
    repetitions: int
    next_review_date: Optional[datetime] = None
    last_review_date: Optional[datetime] = None

    class Config:
        from_attributes = True


# ═══════════════════════════════════════════
#  仪表盘 / 统计数据
# ═══════════════════════════════════════════

class DailyStats(BaseModel):
    """每日学习统计（用于折线图）"""
    date: str
    total_questions: int
    correct_count: int
    accuracy: float


class DashboardData(BaseModel):
    """仪表盘总览数据"""
    total_questions: int               # 题库总数
    total_answers: int                 # 总答题次数
    overall_accuracy: float            # 总正确率
    today_questions: int               # 今日答题数
    today_accuracy: float              # 今日正确率
    review_due_count: int              # 待复习数量
    daily_stats: List[DailyStats]      # 每日统计
    knowledge_stats: List[KnowledgePointStats]  # 知识点统计


class QuestionListParams(BaseModel):
    """题目列表筛选参数"""
    knowledge_point_id: Optional[int] = None
    difficulty: Optional[int] = None
    category: Optional[str] = None
    limit: int = Field(default=10, ge=1, le=50)


# 解决循环引用
QuestionWithSchedule.model_rebuild()
AnswerResult.model_rebuild()
