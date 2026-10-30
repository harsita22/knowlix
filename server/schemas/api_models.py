"""Pydantic API schemas for Knowlix REST endpoints."""
from pydantic import BaseModel
from typing import List, Optional, Any, Dict
import datetime


class UserRegister(BaseModel):
    email: str
    password: str
    full_name: str
    role: str = "student"  # 'student' or 'teacher'


class UserLogin(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: Dict[str, Any]


class UserProfile(BaseModel):
    id: int
    email: str
    full_name: str
    role: str


class StudentDashboardData(BaseModel):
    student_id: int
    student_name: str
    overall_mastery: float
    total_study_hours: float
    topics_in_progress: int
    weak_topics: List[Dict[str, Any]]
    strong_topics: List[Dict[str, Any]]
    recent_assessments: List[Dict[str, Any]]
    active_recovery_plan: Optional[Dict[str, Any]] = None


class KnowledgeGraphData(BaseModel):
    nodes: List[Dict[str, Any]]
    edges: List[Dict[str, Any]]
    subject: str


class TutorChatRequest(BaseModel):
    topic: str
    message: str
    teaching_style: str = "step_by_step"  # analogy, step_by_step, simple, example_based, practice


class TutorChatResponse(BaseModel):
    reply: str
    pedagogical_style: str
    comprehension_check: Optional[str] = None
    citations: List[str] = []


class AgentQueryRequest(BaseModel):
    query: str


class AgentQueryResponse(BaseModel):
    answer: str
    trace: List[Dict[str, Any]]


class RecoveryPlanCreateRequest(BaseModel):
    weak_topic: str
    available_days: int = 3


class TeacherClassItem(BaseModel):
    id: int
    name: str
    subject: str
    grade_level: str
    enrolled_students_count: int


class TeacherInterventionAlert(BaseModel):
    student_id: int
    student_name: str
    topic: str
    severity: str
    trigger_reason: str
    recommendation: str
