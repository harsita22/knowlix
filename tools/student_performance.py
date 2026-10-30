"""Performance Analyst tool for Knowlix. Analyzes topic mastery, trends, and weak/strong concepts."""
import csv
import json
import os
from tools import Tool
import config


class StudentPerformance(Tool):
    name = "student_performance"
    description = (
        "Analyze a student's academic performance, topic-wise mastery scores, accuracy, "
        "weak and strong concepts, and learning consistency."
    )
    args_doc = '{"student_id": "S1", "subject": "CS"}'

    def execute(self, student_id="S1", subject=None):
        student_key = str(student_id).strip()
        results = {
            "student_id": student_key,
            "subject": subject or "All Subjects",
            "topics": [],
            "weak_topics": [],
            "strong_topics": [],
            "average_score": 0.0,
            "accuracy_rate": 0.0,
            "learning_consistency": "Consistent",
            "summary": ""
        }

        # Try database first
        try:
            from database.connection import SessionLocal
            from database.models import User, TopicMastery, Topic, Subject
            db = SessionLocal()
            try:
                # Find user matching student key (id or email or name)
                user = None
                if student_key.isdigit():
                    user = db.query(User).filter(User.id == int(student_key), User.role == "student").first()
                if not user and student_key.upper().startswith("S") and student_key[1:].isdigit():
                    num = student_key[1:]
                    user = db.query(User).filter(
                        (User.email.ilike(f"%student{num}%")) | (User.full_name.ilike(f"%S{num}%")),
                        User.role == "student"
                    ).first()
                if not user:
                    user = db.query(User).filter(
                        (User.email.ilike(f"%{student_key}%")) | (User.full_name.ilike(f"%{student_key}%")),
                        User.role == "student"
                    ).first()
                if not user:
                    user = db.query(User).filter(User.role == "student").first()

                if user:
                    query = db.query(TopicMastery, Topic, Subject).join(Topic, TopicMastery.topic_id == Topic.id).join(Subject, Topic.subject_id == Subject.id).filter(TopicMastery.student_id == user.id)
                    if subject:
                        query = query.filter((Subject.code.ilike(f"%{subject}%")) | (Subject.name.ilike(f"%{subject}%")))
                    records = query.all()
                    if records:
                        total_score = 0.0
                        total_acc = 0.0
                        for mastery, topic, subj in records:
                            item = {
                                "topic": topic.name,
                                "subject": subj.name,
                                "chapter": topic.chapter,
                                "score": mastery.mastery_score,
                                "accuracy": mastery.accuracy,
                                "attempts": mastery.attempts,
                                "status": mastery.status
                            }
                            results["topics"].append(item)
                            total_score += mastery.mastery_score
                            total_acc += mastery.accuracy
                            if mastery.mastery_score < 60:
                                results["weak_topics"].append({"topic": topic.name, "score": mastery.mastery_score, "status": mastery.status})
                            elif mastery.mastery_score >= 75:
                                results["strong_topics"].append({"topic": topic.name, "score": mastery.mastery_score, "status": mastery.status})

                        count = len(records)
                        results["average_score"] = round(total_score / count, 1)
                        results["accuracy_rate"] = round((total_acc / count) * 100, 1)
                        results["summary"] = (
                            f"Student {user.full_name} has an average score of {results['average_score']}% "
                            f"with {len(results['weak_topics'])} weak topic(s) and {len(results['strong_topics'])} strong topic(s)."
                        )
                        return json.dumps(results, indent=2)
            finally:
                db.close()
        except Exception:
            pass  # Fall through to CSV fallback

        # Fallback to CSV datasets in DATA_DIR
        csv_path = os.path.join(config.DATA_DIR, "scores.csv")
        if os.path.exists(csv_path):
            with open(csv_path, mode="r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                matched_rows = [r for r in reader if r.get("student", "").strip().lower() == student_key.lower()]
                if not matched_rows:
                    f.seek(0)
                    reader = csv.DictReader(f)
                    matched_rows = list(reader)

            if matched_rows:
                total_score = 0.0
                for r in matched_rows:
                    try:
                        score = float(r.get("score", 0))
                    except ValueError:
                        score = 0.0
                    topic_name = r.get("topic", "Unknown")
                    item = {"topic": topic_name, "score": score, "attempts": 1}
                    results["topics"].append(item)
                    total_score += score
                    if score < 50:
                        results["weak_topics"].append(item)
                    elif score >= 70:
                        results["strong_topics"].append(item)

                count = len(matched_rows)
                results["average_score"] = round(total_score / count, 1) if count else 0
                results["summary"] = (
                    f"Student {student_key} scored an average of {results['average_score']}%. "
                    f"Weakest topic: {min(matched_rows, key=lambda x: float(x.get('score', 0)))['topic']}."
                )
                return json.dumps(results, indent=2)

        return json.dumps({"student_id": student_key, "error": "No performance records found.", "topics": []})