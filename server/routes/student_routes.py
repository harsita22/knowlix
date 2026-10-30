"""Student endpoints with strict student data isolation."""
import json
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from database.connection import get_db
from database.models import (
    User, Subject, Topic, TopicPrerequisite, TopicMastery, Misconception,
    StudentAssessment, StudentAnswer, StudyPlan, StudyPlanTask, LearningSession
)
from server.auth import get_current_user, require_role
from server.schemas.api_models import (
    StudentDashboardData, KnowledgeGraphData, TutorChatRequest, TutorChatResponse,
    RecoveryPlanCreateRequest
)
from tools import build_tools

router = APIRouter(prefix="/api/student", tags=["Student Portal"])


@router.get("/dashboard", response_model=StudentDashboardData)
def get_student_dashboard(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    student_id = current_user.id
    masteries = db.query(TopicMastery, Topic, Subject).join(
        Topic, TopicMastery.topic_id == Topic.id
    ).join(
        Subject, Topic.subject_id == Subject.id
    ).filter(TopicMastery.student_id == student_id).all()

    weak = []
    strong = []
    total_score = 0.0

    for m, t, s in masteries:
        item = {
            "topic_id": t.id,
            "topic_name": t.name,
            "subject": s.name,
            "chapter": t.chapter,
            "score": m.mastery_score,
            "accuracy": m.accuracy,
            "status": m.status
        }
        total_score += m.mastery_score
        if m.mastery_score < 60:
            weak.append(item)
        elif m.mastery_score >= 75:
            strong.append(item)

    avg_mastery = round(total_score / len(masteries), 1) if masteries else 72.0

    assessments = db.query(StudentAssessment).filter(
        StudentAssessment.student_id == student_id
    ).order_by(StudentAssessment.created_at.desc()).limit(5).all()

    recent_ass = [
        {"id": a.id, "title": a.title, "score": a.score, "passed": a.passed, "date": str(a.created_at.date())}
        for a in assessments
    ]

    active_plan = db.query(StudyPlan).filter(
        StudyPlan.student_id == student_id, StudyPlan.status == "active"
    ).first()

    plan_data = None
    if active_plan:
        plan_data = {
            "id": active_plan.id,
            "title": active_plan.title,
            "total_estimated_hours": active_plan.total_estimated_hours,
            "tasks_count": len(active_plan.tasks),
            "completed_tasks": sum(1 for t in active_plan.tasks if t.is_completed)
        }

    return {
        "student_id": student_id,
        "student_name": current_user.full_name,
        "overall_mastery": avg_mastery,
        "total_study_hours": 14.5,
        "topics_in_progress": len(masteries),
        "weak_topics": weak,
        "strong_topics": strong,
        "recent_assessments": recent_ass,
        "active_recovery_plan": plan_data
    }


@router.get("/knowledge-graph", response_model=KnowledgeGraphData)
def get_knowledge_graph(
    subject: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    student_id = current_user.id
    query = db.query(Topic, Subject).join(Subject, Topic.subject_id == Subject.id)
    if subject:
        query = query.filter((Subject.code.ilike(f"%{subject}%")) | (Subject.name.ilike(f"%{subject}%")))
    topics = query.all()

    nodes = []
    edges = []

    # Get student masteries
    mastery_map = {
        m.topic_id: m for m in db.query(TopicMastery).filter(TopicMastery.student_id == student_id).all()
    }

    for t, s in topics:
        m = mastery_map.get(t.id)
        score = m.mastery_score if m else None
        status_val = m.status if m else "unassessed"

        nodes.append({
            "id": str(t.id),
            "label": t.name,
            "chapter": t.chapter,
            "subject": s.name,
            "difficulty": t.difficulty,
            "score": score,
            "status": status_val
        })

    # Get prerequisite edges
    topic_ids = [t.id for t, _ in topics]
    prereqs = db.query(TopicPrerequisite).filter(TopicPrerequisite.topic_id.in_(topic_ids)).all()
    for p in prereqs:
        edges.append({
            "source": str(p.prerequisite_topic_id),
            "target": str(p.topic_id),
            "strength": p.strength
        })

    return {
        "nodes": nodes,
        "edges": edges,
        "subject": subject or "All Subjects"
    }


@router.get("/misconceptions")
def get_student_misconceptions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    student_id = current_user.id
    records = db.query(Misconception, Topic, Subject).join(
        Topic, Misconception.topic_id == Topic.id
    ).join(
        Subject, Topic.subject_id == Subject.id
    ).filter(Misconception.student_id == student_id).all()

    return [
        {
            "id": m.id,
            "subject": s.name,
            "topic": t.name,
            "description": m.description,
            "evidence": m.evidence,
            "confidence_score": m.confidence_score,
            "suggested_correction": m.suggested_correction,
            "resolution_status": m.resolution_status
        }
        for m, t, s in records
    ]


@router.post("/tutor/chat", response_model=TutorChatResponse)
def tutor_chat(
    req: TutorChatRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    tools = build_tools()
    # 1. Retrieve curriculum grounding
    rag_result = json.loads(tools["curriculum_retrieval"].execute(query=req.message or req.topic))
    citations = rag_result.get("source_citations", [])

    # 2. Get pedagogical strategy
    tutor_guide = json.loads(tools["adaptive_tutor"].execute(
        topic=req.topic, style=req.teaching_style, student_level="intermediate"
    ))

    # 3. Assemble pedagogical response
    grounded_text = ""
    if rag_result.get("matches"):
        grounded_text = rag_result["matches"][0]["content"]

    strategy_desc = tutor_guide.get("pedagogical_strategy", "")
    check_q = tutor_guide.get("comprehension_check_question", "")

    # Clean conversational response grounded in pedagogical strategy
    reply = (
        f"**Exploring {req.topic}** ({req.teaching_style.replace('_', ' ').title()} Mode):\n\n"
        f"{strategy_desc}\n\n"
    )
    if grounded_text:
        reply += f"**Key Curriculum Insight:**\n> {grounded_text}\n\n"
    reply += f"Remember: mastering this concept builds directly into your upcoming learning checkpoints!"

    return {
        "reply": reply,
        "pedagogical_style": req.teaching_style,
        "comprehension_check": check_q,
        "citations": citations
    }


@router.get("/study-plans")
def get_study_plans(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    plans = db.query(StudyPlan).filter(StudyPlan.student_id == current_user.id).all()
    out = []
    for p in plans:
        out.append({
            "id": p.id,
            "title": p.title,
            "total_estimated_hours": p.total_estimated_hours,
            "status": p.status,
            "tasks": [
                {
                    "id": t.id,
                    "day": t.day_number,
                    "order": t.order_index,
                    "type": t.task_type,
                    "description": t.description,
                    "duration_minutes": t.duration_minutes,
                    "is_completed": t.is_completed
                }
                for t in p.tasks
            ]
        })
    return out


@router.patch("/study-plans/task/{task_id}/toggle")
def toggle_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    task = db.query(StudyPlanTask).join(StudyPlan).filter(
        StudyPlanTask.id == task_id, StudyPlan.student_id == current_user.id
    ).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task.is_completed = not task.is_completed
    db.commit()
    return {"id": task.id, "is_completed": task.is_completed}

