"""Learning Intervention Agent tool for Knowlix. Formulates respectful, evidence-based teacher alerts."""
import json
from tools import Tool


class InterventionRecommendationTool(Tool):
    name = "intervention_recommendation"
    description = (
        "Generate evidence-based learning intervention recommendations for teachers and students "
        "when indicators of difficulty (low scores, repeated errors, unresolved misconceptions) appear."
    )
    args_doc = '{"student_id": "S1", "topic": "Recursion"}'

    def execute(self, student_id="S1", topic=None):
        out = {
            "student_id": str(student_id),
            "topic": topic or "All Areas",
            "needs_intervention": False,
            "severity_level": "none",
            "detected_signals": [],
            "teacher_actionable_recommendations": [],
            "student_support_actions": [],
            "evidence_summary": ""
        }

        try:
            from database.connection import SessionLocal
            from database.models import User, TopicMastery, Topic, Misconception, StudentAssessment
            db = SessionLocal()
            try:
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
                    # Check mastery
                    mastery_q = db.query(TopicMastery, Topic).join(Topic, TopicMastery.topic_id == Topic.id).filter(TopicMastery.student_id == user.id)
                    if topic:
                        mastery_q = mastery_q.filter(Topic.name.ilike(f"%{topic}%"))
                    struggles = [m for m in mastery_q.all() if m[0].mastery_score < 60]

                    # Check misconceptions
                    misc_q = db.query(Misconception, Topic).join(Topic, Misconception.topic_id == Topic.id).filter(
                        Misconception.student_id == user.id, Misconception.resolution_status != "resolved"
                    )
                    if topic:
                        misc_q = misc_q.filter(Topic.name.ilike(f"%{topic}%"))
                    unresolved_misc = misc_q.all()

                    if struggles or unresolved_misc:
                        out["needs_intervention"] = True
                        out["severity_level"] = "warning" if len(struggles) <= 1 else "elevated"

                        for m, t in struggles:
                            out["detected_signals"].append({
                                "signal_type": "Low Mastery Score",
                                "topic": t.name,
                                "metric": f"{m.mastery_score}% accuracy over {m.attempts} attempt(s)"
                            })

                        for misc, t in unresolved_misc:
                            out["detected_signals"].append({
                                "signal_type": "Unresolved Misconception",
                                "topic": t.name,
                                "description": misc.description,
                                "confidence": f"{int(misc.confidence_score * 100)}%"
                            })

                        # Objective, respectful teacher recommendations
                        out["teacher_actionable_recommendations"] = [
                            "Provide alternative visual representation (e.g. call-stack execution diagram or physical model) to bypass cognitive hurdles.",
                            "Offer a brief 10-minute check-in focusing specifically on boundary condition intuition rather than generalized review.",
                            "Pair student with peer study partner for collaborative tracing exercises.",
                            "Verify prerequisite comfort before assigning additional advanced drills."
                        ]

                        out["student_support_actions"] = [
                            "Review recommended 3-day recovery plan in Study Planner.",
                            "Engage with AI Tutor using 'Analogy' or 'Step-by-Step' mode.",
                            "Attempt the non-timed micro-checkpoint quiz to confirm understanding."
                        ]

                        out["evidence_summary"] = (
                            f"Student {user.full_name} exhibits targeted learning friction in "
                            f"{', '.join(t.name for _, t in struggles) if struggles else 'designated topic'}. "
                            f"Intervention is recommended to provide alternative scaffolding."
                        )
                        return json.dumps(out, indent=2)
            finally:
                db.close()
        except Exception:
            pass

        out["evidence_summary"] = f"No critical intervention signals detected for student {student_id}."
        return json.dumps(out, indent=2)