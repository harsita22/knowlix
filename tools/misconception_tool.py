"""Misconception Detective tool for Knowlix. Analyzes cognitive error patterns and pedagogical evidence."""
import json
from tools import Tool


class MisconceptionTool(Tool):
    name = "misconception_analysis"
    description = (
        "Detect and review student learning misconceptions, cognitive error patterns, "
        "evidence from assessment history, confidence scores, and suggested pedagogical corrections."
    )
    args_doc = '{"student_id": "S1", "topic": "Recursion"}'

    def execute(self, student_id="S1", topic=None):
        results = {
            "student_id": str(student_id),
            "topic_filter": topic or "All",
            "detected_misconceptions": [],
            "recent_error_patterns": [],
            "hypotheses_vs_evidence": []
        }

        try:
            from database.connection import SessionLocal
            from database.models import User, Misconception, Topic, Subject, StudentAssessment, StudentAnswer
            db = SessionLocal()
            try:
                # Find student user
                s_key = str(student_id).strip()
                user = None
                if s_key.isdigit():
                    user = db.query(User).filter(User.id == int(s_key), User.role == "student").first()
                if not user and s_key.upper().startswith("S") and s_key[1:].isdigit():
                    num = s_key[1:]
                    user = db.query(User).filter(
                        (User.email.ilike(f"%student{num}%")) | (User.full_name.ilike(f"%S{num}%")),
                        User.role == "student"
                    ).first()
                if not user:
                    user = db.query(User).filter(
                        (User.email.ilike(f"%{s_key}%")) | (User.full_name.ilike(f"%{s_key}%")),
                        User.role == "student"
                    ).first()
                if not user:
                    user = db.query(User).filter(User.role == "student").first()

                if user:
                    query = db.query(Misconception, Topic, Subject).join(
                        Topic, Misconception.topic_id == Topic.id
                    ).join(Subject, Topic.subject_id == Subject.id).filter(
                        Misconception.student_id == user.id
                    )
                    if topic:
                        query = query.filter(Topic.name.ilike(f"%{topic}%"))
                    records = query.all()

                    for m, t, s in records:
                        item = {
                            "id": m.id,
                            "subject": s.name,
                            "topic": t.name,
                            "description": m.description,
                            "evidence": m.evidence,
                            "confidence_score": m.confidence_score,
                            "suggested_correction": m.suggested_correction,
                            "resolution_status": m.resolution_status,
                            "certainty_level": "Confirmed Evidence" if m.confidence_score >= 0.85 else "Working Hypothesis"
                        }
                        results["detected_misconceptions"].append(item)

                    # Look at recent wrong answers for evidence
                    ans_query = db.query(StudentAnswer, StudentAssessment, Topic).join(
                        StudentAssessment, StudentAnswer.assessment_id == StudentAssessment.id
                    ).join(
                        Topic, StudentAssessment.topic_id == Topic.id
                    ).filter(
                        StudentAssessment.student_id == user.id,
                        StudentAnswer.is_correct.is_(False)
                    )
                    if topic:
                        ans_query = ans_query.filter(Topic.name.ilike(f"%{topic}%"))
                    wrong_answers = ans_query.limit(5).all()

                    for ans, ass, t in wrong_answers:
                        results["recent_error_patterns"].append({
                            "topic": t.name,
                            "question": ans.question_text,
                            "student_answer": ans.student_answer,
                            "correct_answer": ans.correct_answer,
                            "mistake_pattern": ans.mistake_pattern
                        })

                    results["summary"] = (
                        f"Found {len(results['detected_misconceptions'])} registered misconception(s) for student {user.full_name}. "
                        f"{len(results['recent_error_patterns'])} diagnostic error pattern(s) logged."
                    )
                    return json.dumps(results, indent=2)
            finally:
                db.close()
        except Exception as e:
            return json.dumps({"error": f"Misconception analysis error: {e}", "detected_misconceptions": []})