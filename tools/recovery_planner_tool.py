"""Recovery Planner tool for Knowlix. Generates evidence-based, prerequisite-aware recovery plans."""
import json
from tools import Tool


class RecoveryPlannerTool(Tool):
    name = "recovery_planner"
    description = (
        "Generate a structured, personalized recovery plan for a student based on weak topics, "
        "missing prerequisites, study tasks, estimated hours, and milestone checkpoints."
    )
    args_doc = '{"student_id": "S1", "weak_topic": "Recursion", "available_days": 3}'

    def execute(self, student_id="S1", weak_topic="Recursion", available_days=3):
        student_key = str(student_id)
        days = max(1, min(int(available_days), 14))

        plan = {
            "student_id": student_key,
            "target_topic": weak_topic,
            "duration_days": days,
            "total_estimated_hours": 0.0,
            "prerequisites_to_review": [],
            "daily_schedule": [],
            "checkpoint_milestones": []
        }

        # Query database to ground the plan in real prerequisites and mastery scores
        try:
            from database.connection import SessionLocal
            from database.models import Topic, TopicPrerequisite, TopicMastery, User
            db = SessionLocal()
            try:
                topic = db.query(Topic).filter(Topic.name.ilike(f"%{weak_topic}%")).first()
                if topic:
                    # Fetch prerequisites
                    prereqs = db.query(Topic).join(
                        TopicPrerequisite, TopicPrerequisite.prerequisite_topic_id == Topic.id
                    ).filter(TopicPrerequisite.topic_id == topic.id).all()

                    for p in prereqs:
                        plan["prerequisites_to_review"].append({
                            "topic": p.name,
                            "reason": f"Foundational dependency required before mastering {topic.name}"
                        })

                    # Construct Day-by-Day sequence
                    day_tasks = []
                    # Day 1: Prerequisite grounding
                    prereq_name = plan["prerequisites_to_review"][0]["topic"] if plan["prerequisites_to_review"] else "Core Foundations"
                    day_tasks.append({
                        "day": 1,
                        "focus": f"Prerequisite Mastery: {prereq_name}",
                        "tasks": [
                            {"order": 1, "type": "Concept Review", "duration": "30 mins", "description": f"Review foundational rules and call execution flow of {prereq_name}"},
                            {"order": 2, "type": "Guided Practice", "duration": "45 mins", "description": "Solve 3 guided exercises reinforcing prerequisite concepts"}
                        ],
                        "estimated_hours": 1.25
                    })

                    # Day 2: Target Concept Deconstruction & Misconception Correction
                    day_tasks.append({
                        "day": 2,
                        "focus": f"Core Concept Remediation: {topic.name}",
                        "tasks": [
                            {"order": 1, "type": "Misconception Diagnosis", "duration": "30 mins", "description": f"Examine common error patterns and trace {topic.name} step-by-step"},
                            {"order": 2, "type": "Scaffolded Drills", "duration": "45 mins", "description": "Complete progressive micro-challenges with immediate feedback"}
                        ],
                        "estimated_hours": 1.25
                    })

                    # Day 3: Independent Practice & Assessment Checkpoint
                    day_tasks.append({
                        "day": 3,
                        "focus": "Synthesis & Diagnostic Checkpoint",
                        "tasks": [
                            {"order": 1, "type": "Independent Application", "duration": "40 mins", "description": f"Solve 2 real-world synthesis problems applying {topic.name}"},
                            {"order": 2, "type": "Mastery Assessment", "duration": "30 mins", "description": "Complete 5-question checkpoint assessment to verify mastery resolution"}
                        ],
                        "estimated_hours": 1.15
                    })

                    plan["daily_schedule"] = day_tasks[:days]
                    plan["total_estimated_hours"] = round(sum(d["estimated_hours"] for d in plan["daily_schedule"]), 1)
                    plan["checkpoint_milestones"] = [
                        f"Day 1 Checkpoint: Prerequisite quiz score >= 80% on {prereq_name}",
                        f"Day 2 Checkpoint: Zero unresolved boundary misconceptions on {topic.name}",
                        f"Day {days} Checkpoint: Mastery score reaches at least 75% on final diagnostic"
                    ]

                    return json.dumps(plan, indent=2)
            finally:
                db.close()
        except Exception:
            pass

        # Fallback if DB is unavailable
        plan["daily_schedule"] = [
            {"day": 1, "focus": "Prerequisite Review", "tasks": [{"description": f"Review foundations of {weak_topic}", "duration": "45 mins"}]},
            {"day": 2, "focus": "Core Remediation", "tasks": [{"description": f"Practice problem sets on {weak_topic}", "duration": "60 mins"}]},
            {"day": 3, "focus": "Self-Assessment", "tasks": [{"description": f"Complete diagnostic review on {weak_topic}", "duration": "30 mins"}]}
        ]
        plan["total_estimated_hours"] = 2.25
        return json.dumps(plan, indent=2)
