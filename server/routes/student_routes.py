"""Student endpoints with strict student data isolation and live Socratic AI Tutor."""
import json
import os
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
from agent.llm import LLM, DryRunLLM

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
    
    # 1. Fetch student's real mastery and misconceptions from DB
    mastery = db.query(TopicMastery).join(Topic).filter(
        TopicMastery.student_id == current_user.id,
        Topic.name.ilike(f"%{req.topic}%")
    ).first()

    misconceptions = db.query(Misconception).join(Topic).filter(
        Misconception.student_id == current_user.id,
        Topic.name.ilike(f"%{req.topic}%")
    ).all()

    # 2. Retrieve curriculum grounding
    rag_result = json.loads(tools["curriculum_retrieval"].execute(query=req.message or req.topic))
    citations = rag_result.get("source_citations", [])
    grounded_context = ""
    if rag_result.get("matches"):
        grounded_context = "\n".join(m["content"] for m in rag_result["matches"][:2])

    score_info = f"Current mastery score: {mastery.mastery_score}% ({mastery.status})" if mastery else "First time exploring this topic."
    misc_info = ""
    if misconceptions:
        misc_info = "Known cognitive misconceptions: " + "; ".join(f"{m.description} (Evidence: {m.evidence})" for m in misconceptions)

    # 3. Construct lively, Socratic system prompt
    style_label = req.teaching_style.replace('_', ' ').title()
    system_prompt = f"""You are Knowlix, an encouraging, lively, and highly capable Socratic AI learning partner.
You are directly helping student {current_user.full_name} solve their questions, homework doubts, or coding problems.
Current Area/Topic: {req.topic}
Student Diagnostic Profile: {score_info}
{misc_info}

Mode: {style_label}
- 'Step By Step': Walk through the problem or concept one clear step at a time, guiding the student collaboratively.
- 'Analogy': Connect technical ideas to vivid, tangible everyday experiences.
- 'Practice': Give an immediate micro-challenge or problem for the student to attempt.
- 'Simple': Explain with intuitive, plain English without heavy jargon.
- 'Example Based': Walk through a small concrete working example showing inputs transforming into outputs.

Pedagogical Directives for Interactive Problem Solving:
1. Be lively, conversational, enthusiastic, and supportive. Use clean formatting (bold key terms, bullet points, and code fences).
2. When the student shares THEIR OWN problem, code, or question:
   - If they ask how to solve something: Scaffold the solution! Walk them through step 1, give a gentle hint, and ask them what they think the next step or result should be.
   - If they paste their attempt or code with an error: Pinpoint the exact line or concept where the mistake occurs, explain why it happened, and ask them how they might adjust it.
   - If they say 'give me the full answer' or have tried repeatedly: Provide the complete, beautifully formatted step-by-step solution, then ask a follow-up check question to confirm they understand the mechanism.
3. Ground your explanation in verified curriculum material when relevant:
{grounded_context}
4. Always end your turn with an engaging checkpoint question, hint, or invitation for the student's next step.
"""

    messages = []
    if req.history:
        for h in req.history:
            messages.append({"role": h.get("role", "user"), "content": h.get("content", "")})
    messages.append({"role": "user", "content": req.message})

    # 4. Generate with live Gemini LLM
    try:
        if os.environ.get("GEMINI_API_KEY") and not os.environ.get("AGENTX_DRY_RUN"):
            llm = LLM()
            reply = llm.generate(system_prompt, messages)
        else:
            raise RuntimeError("Dry run or offline mode")
    except Exception as e:
        # Fallback to adaptive tutor tool if offline
        tutor_guide = json.loads(tools["adaptive_tutor"].execute(
            topic=req.topic, style=req.teaching_style, student_level="intermediate"
        ))
        strategy_desc = tutor_guide.get("pedagogical_strategy", "")
        reply = (
            f"**Exploring {req.topic}** ({style_label} Mode):\n\n"
            f"{strategy_desc}\n\n"
        )
        if grounded_context:
            reply += f"**Key Curriculum Insight:**\n> {grounded_context}\n\n"
        reply += f"Let's solve this step by step. What part of {req.topic} would you like to start with?"

    # Extract or generate check question
    check_q = f"What do you think is our next step for {req.topic}?"
    if "?" in reply:
        questions = [line for line in reply.split("\n") if "?" in line]
        if questions:
            check_q = questions[-1].strip("*# ")

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
