"""
数据模型定义 - 考研数学刷题系统核心表结构

四张核心表：
  knowledge_points  → 知识点标签表（如：极限、导数、矩阵）
  questions         → 题目表（题干、选项、答案、解析、关联知识点）
  answer_records    → 答题记录表（每次作答的详细记录）
  review_schedules  → 复习调度表（SM-2 算法驱动，控制何时复习）
"""
from sqlalchemy import (
    Column, Integer, String, Float, Text, Boolean,
    DateTime, ForeignKey, JSON
)
from sqlalchemy.orm import relationship
from datetime import datetime

from database import Base


class KnowledgePoint(Base):
    """知识点标签表——考研数学的知识体系"""
    __tablename__ = "knowledge_points"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, comment="知识点名称，如：极限与连续")
    category = Column(
        String(20), nullable=False,
        comment="大类：高等数学 / 线性代数 / 概率论与数理统计"
    )
    description = Column(String(200), comment="知识点描述")

    # 关联题目
    questions = relationship("Question", back_populates="knowledge_point")


class Question(Base):
    """题目表——所有刷题数据"""
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(Text, nullable=False, comment="题干（支持 Markdown 或纯文本）")
    question_type = Column(
        String(20), default="single_choice",
        comment="题型：single_choice / multiple_choice / fill_blank"
    )
    options = Column(JSON, comment="选项列表，JSON 数组，如 ['A. 1', 'B. 2', 'C. 3', 'D. 4']")
    answer = Column(String(50), nullable=False, comment="正确答案，如 'C'")
    explanation = Column(Text, comment="解析")
    difficulty = Column(
        Integer, default=3,
        comment="难度 1~5：1=基础题，3=中等题，5=压轴题"
    )
    source = Column(String(100), comment="来源：如 2023数一真题")

    # 外键关联知识点
    knowledge_point_id = Column(
        Integer, ForeignKey("knowledge_points.id"), nullable=False
    )
    knowledge_point = relationship("KnowledgePoint", back_populates="questions")

    # 关联答题记录和复习调度
    answer_records = relationship("AnswerRecord", back_populates="question")
    review_schedule = relationship("ReviewSchedule", back_populates="question", uselist=False)


class AnswerRecord(Base):
    """答题记录表——每次做题的完整快照，用于薄弱点分析"""
    __tablename__ = "answer_records"

    id = Column(Integer, primary_key=True, autoincrement=True)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    user_answer = Column(String(50), comment="用户提交的答案")
    is_correct = Column(Boolean, nullable=False, comment="是否正确")
    time_spent = Column(Integer, comment="答题耗时（秒）")
    created_at = Column(DateTime, default=datetime.utcnow, comment="答题时间")

    # 关联题目
    question = relationship("Question", back_populates="answer_records")


class ReviewSchedule(Base):
    """
    复习调度表——SM-2 间隔重复算法的核心数据

    SM-2 算法三个关键参数：
      easiness_factor (EF)  → 难易度因子，越大表示题目越容易，默认 2.5
      interval               → 当前复习间隔（天）
      repetitions            → 连续正确次数
    """
    __tablename__ = "review_schedules"

    id = Column(Integer, primary_key=True, autoincrement=True)
    question_id = Column(
        Integer, ForeignKey("questions.id"), unique=True, nullable=False
    )
    easiness_factor = Column(Float, default=2.5, comment="难易度因子 EF，≥1.3")
    interval = Column(Integer, default=0, comment="当前间隔（天）")
    repetitions = Column(Integer, default=0, comment="连续正确次数")
    next_review_date = Column(DateTime, comment="下次复习日期")
    last_review_date = Column(DateTime, comment="上次复习日期")
    created_at = Column(DateTime, default=datetime.utcnow)

    # 关联题目
    question = relationship("Question", back_populates="review_schedule")
