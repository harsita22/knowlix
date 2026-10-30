"""SQLAlchemy database models for Knowlix platform."""
import datetime
from sqlalchemy import (
    Column, Integer, String, Text, Float, Boolean, DateTime, ForeignKey, Index, JSON
)
from sqlalchemy.orm import relationship
from database.connection import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False, default="student")  # 'student', 'teacher', 'admin'
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    enrollments = relationship("StudentEnrollment", back_populates="student", cascade="all, delete-orphan")
    masteries = relationship("TopicMastery", back_populates="student", cascade="all, delete-orphan")
    misconceptions = relationship("Misconception", back_populates="student", cascade="all, delete-orphan")
    study_plans = relationship("StudyPlan", back_populates="student", cascade="all, delete-orphan")
    assessments = relationship("StudentAssessment", back_populates="student", cascade="all, delete-orphan")


class TeacherClass(Base):
    __tablename__ = "teacher_classes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    teacher_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    subject = Column(String(100), nullable=False)
    grade_level = Column(String(50), default="Grade 10")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    enrollments = relationship("StudentEnrollment", back_populates="klass", cascade="all, delete-orphan")


class StudentEnrollment(Base):
    __tablename__ = "student_enrollments"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    class_id = Column(Integer, ForeignKey("teacher_classes.id", ondelete="CASCADE"), nullable=False, index=True)
    enrolled_at = Column(DateTime, default=datetime.datetime.utcnow)

    student = relationship("User", back_populates="enrollments")
    klass = relationship("TeacherClass", back_populates="enrollments")


class Subject(Base):
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(50), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, default="")

    topics = relationship("Topic", back_populates="subject", cascade="all, delete-orphan")


class Topic(Base):
    __tablename__ = "topics"

    id = Column(Integer, primary_key=True, index=True)
    subject_id = Column(Integer, ForeignKey("subjects.id", ondelete="CASCADE"), nullable=False, index=True)
    chapter = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False, index=True)
    difficulty = Column(String(50), default="intermediate")  # beginner, intermediate, advanced
    description = Column(Text, default="")

    subject = relationship("Subject", back_populates="topics")
    prerequisites = relationship("TopicPrerequisite", foreign_keys="TopicPrerequisite.topic_id", back_populates="topic")


class TopicPrerequisite(Base):
    __tablename__ = "topic_prerequisites"

    id = Column(Integer, primary_key=True, index=True)
    topic_id = Column(Integer, ForeignKey("topics.id", ondelete="CASCADE"), nullable=False, index=True)
    prerequisite_topic_id = Column(Integer, ForeignKey("topics.id", ondelete="CASCADE"), nullable=False, index=True)
    strength = Column(String(50), default="required")  # 'required', 'recommended'

    topic = relationship("Topic", foreign_keys=[topic_id], back_populates="prerequisites")
    prerequisite_topic = relationship("Topic", foreign_keys=[prerequisite_topic_id])


class TopicMastery(Base):
    __tablename__ = "topic_mastery"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    topic_id = Column(Integer, ForeignKey("topics.id", ondelete="CASCADE"), nullable=False, index=True)
    mastery_score = Column(Float, default=0.0)  # 0 to 100
    attempts = Column(Integer, default=0)
    accuracy = Column(Float, default=0.0)       # 0.0 to 1.0
    status = Column(String(50), default="in_progress")  # 'struggling', 'in_progress', 'mastered'
    last_assessed = Column(DateTime, default=datetime.datetime.utcnow)

    student = relationship("User", back_populates="masteries")
    topic = relationship("Topic")


class Misconception(Base):
    __tablename__ = "misconceptions"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    topic_id = Column(Integer, ForeignKey("topics.id", ondelete="CASCADE"), nullable=False, index=True)
    description = Column(Text, nullable=False)
    evidence = Column(Text, default="")
    confidence_score = Column(Float, default=0.75)  # 0.0 to 1.0
    suggested_correction = Column(Text, default="")
    resolution_status = Column(String(50), default="detected")  # 'detected', 'reviewing', 'resolved'
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    student = relationship("User", back_populates="misconceptions")
    topic = relationship("Topic")


class StudentAssessment(Base):
    __tablename__ = "student_assessments"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    topic_id = Column(Integer, ForeignKey("topics.id", ondelete="CASCADE"), nullable=True)
    title = Column(String(255), nullable=False)
    score = Column(Float, nullable=False)
    total_points = Column(Float, default=100.0)
    passed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    student = relationship("User", back_populates="assessments")
    answers = relationship("StudentAnswer", back_populates="assessment", cascade="all, delete-orphan")


class StudentAnswer(Base):
    __tablename__ = "student_answers"

    id = Column(Integer, primary_key=True, index=True)
    assessment_id = Column(Integer, ForeignKey("student_assessments.id", ondelete="CASCADE"), nullable=False, index=True)
    question_text = Column(Text, nullable=False)
    student_answer = Column(Text, nullable=False)
    correct_answer = Column(Text, nullable=False)
    is_correct = Column(Boolean, default=False)
    mistake_pattern = Column(String(255), default="")

    assessment = relationship("StudentAssessment", back_populates="answers")


class StudyPlan(Base):
    __tablename__ = "study_plans"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    subject_id = Column(Integer, ForeignKey("subjects.id", ondelete="SET NULL"), nullable=True)
    title = Column(String(255), nullable=False)
    total_estimated_hours = Column(Float, default=5.0)
    status = Column(String(50), default="active")  # 'active', 'completed', 'archived'
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    student = relationship("User", back_populates="study_plans")
    tasks = relationship("StudyPlanTask", back_populates="plan", cascade="all, delete-orphan")


class StudyPlanTask(Base):
    __tablename__ = "study_plan_tasks"

    id = Column(Integer, primary_key=True, index=True)
    study_plan_id = Column(Integer, ForeignKey("study_plans.id", ondelete="CASCADE"), nullable=False, index=True)
    topic_id = Column(Integer, ForeignKey("topics.id", ondelete="SET NULL"), nullable=True)
    day_number = Column(Integer, default=1)
    order_index = Column(Integer, default=1)
    task_type = Column(String(50), default="concept_review")  # concept_review, practice_drill, quiz
    description = Column(Text, nullable=False)
    duration_minutes = Column(Integer, default=30)
    is_completed = Column(Boolean, default=False)

    plan = relationship("StudyPlan", back_populates="tasks")


class CurriculumDocument(Base):
    __tablename__ = "curriculum_documents"

    id = Column(Integer, primary_key=True, index=True)
    uploader_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    subject_id = Column(Integer, ForeignKey("subjects.id", ondelete="SET NULL"), nullable=True)
    title = Column(String(255), nullable=False)
    file_type = Column(String(50), default="txt")  # pdf, docx, txt, csv
    file_path = Column(String(500), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    chunks = relationship("CurriculumChunk", back_populates="document", cascade="all, delete-orphan")


class CurriculumChunk(Base):
    __tablename__ = "curriculum_chunks"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("curriculum_documents.id", ondelete="CASCADE"), nullable=False, index=True)
    topic_id = Column(Integer, ForeignKey("topics.id", ondelete="SET NULL"), nullable=True, index=True)
    chunk_index = Column(Integer, nullable=False)
    content = Column(Text, nullable=False)
    embedding_json = Column(JSON, nullable=True)  # Store vector embedding list for SQLite / PG vector compatibility
    metadata_json = Column(JSON, nullable=True)

    document = relationship("CurriculumDocument", back_populates="chunks")


class InterventionHistory(Base):
    __tablename__ = "intervention_history"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    teacher_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    topic_id = Column(Integer, ForeignKey("topics.id", ondelete="SET NULL"), nullable=True)
    trigger_reason = Column(Text, nullable=False)
    recommendation = Column(Text, nullable=False)
    severity = Column(String(50), default="warning")  # info, warning, critical
    action_taken = Column(String(255), default="Pending review")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class LearningSession(Base):
    __tablename__ = "learning_sessions"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    topic_id = Column(Integer, ForeignKey("topics.id", ondelete="SET NULL"), nullable=True)
    teaching_style = Column(String(50), default="socratic")
    session_title = Column(String(255), default="Tutoring Session")
    messages_json = Column(JSON, default=list)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class AgentTrace(Base):
    __tablename__ = "agent_traces"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    query = Column(Text, nullable=False)
    final_answer = Column(Text, nullable=False)
    trace_json = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class StudentLearningMemory(Base):
    __tablename__ = "student_learning_memory"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    memory_key = Column(String(100), nullable=False)
    memory_value = Column(Text, nullable=False)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

