"""Knowledge Graph Detective tool for Knowlix. Maps subjects, topics, prerequisites, and mastery dependencies."""
import json
from tools import Tool


class KnowledgeGraphTool(Tool):
    name = "knowledge_graph"
    description = (
        "Inspect the concept hierarchy and prerequisite dependency graph for a subject or topic. "
        "Can check if prerequisite concepts are understood when a student struggles with a topic."
    )
    args_doc = '{"subject": "Computer Science", "target_topic": "Recursion", "student_id": "S1"}'

    def execute(self, subject=None, target_topic=None, student_id=None):
        out = {
            "subject": subject or "All",
            "target_topic": target_topic,
            "prerequisites": [],
            "dependents": [],
            "graph_nodes": [],
            "gap_analysis": ""
        }

        try:
            from database.connection import SessionLocal
            from database.models import Subject, Topic, TopicPrerequisite, TopicMastery, User
            db = SessionLocal()
            try:
                # 1. If target_topic is specified, find it and its prerequisite chain
                if target_topic:
                    topic = db.query(Topic).filter(Topic.name.ilike(f"%{target_topic}%")).first()
                    if topic:
                        out["topic_id"] = topic.id
                        out["topic_name"] = topic.name
                        out["chapter"] = topic.chapter
                        out["difficulty"] = topic.difficulty

                        # Get prerequisites
                        prereq_links = db.query(TopicPrerequisite, Topic).join(
                            Topic, TopicPrerequisite.prerequisite_topic_id == Topic.id
                        ).filter(TopicPrerequisite.topic_id == topic.id).all()

                        prereq_ids = []
                        for link, p_topic in prereq_links:
                            prereq_ids.append(p_topic.id)
                            out["prerequisites"].append({
                                "id": p_topic.id,
                                "name": p_topic.name,
                                "chapter": p_topic.chapter,
                                "strength": link.strength
                            })

                        # If student_id provided, check mastery of target and prerequisites
                        if student_id:
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
                                target_mastery = db.query(TopicMastery).filter(
                                    TopicMastery.student_id == user.id, TopicMastery.topic_id == topic.id
                                ).first()
                                target_score = target_mastery.mastery_score if target_mastery else None

                                prereq_gaps = []
                                for p in out["prerequisites"]:
                                    pm = db.query(TopicMastery).filter(
                                        TopicMastery.student_id == user.id, TopicMastery.topic_id == p["id"]
                                    ).first()
                                    p["student_score"] = pm.mastery_score if pm else "Not yet assessed"
                                    p["student_status"] = pm.status if pm else "unknown"
                                    if pm and pm.mastery_score < 60:
                                        prereq_gaps.append(p["name"])

                                if prereq_gaps:
                                    out["gap_analysis"] = (
                                        f"Student struggles with {topic.name} (score: {target_score}%). "
                                        f"ROOT CAUSE IDENTIFIED: Missing prerequisite mastery in: {', '.join(prereq_gaps)}."
                                    )
                                else:
                                    out["gap_analysis"] = (
                                        f"Target topic {topic.name} has score {target_score}%. "
                                        f"Immediate prerequisites appear satisfied; struggle may be isolated to concept-specific misconceptions."
                                    )

                        return json.dumps(out, indent=2)

                # 2. Otherwise return full graph for subject
                query = db.query(Topic, Subject).join(Subject, Topic.subject_id == Subject.id)
                if subject:
                    query = query.filter((Subject.name.ilike(f"%{subject}%")) | (Subject.code.ilike(f"%{subject}%")))
                topics = query.all()

                for t, s in topics:
                    prereqs = [
                        p.prerequisite_topic.name for p in t.prerequisites if p.prerequisite_topic
                    ]
                    out["graph_nodes"].append({
                        "id": t.id,
                        "subject": s.name,
                        "chapter": t.chapter,
                        "name": t.name,
                        "difficulty": t.difficulty,
                        "prerequisites": prereqs
                    })

                out["total_concepts"] = len(out["graph_nodes"])
                return json.dumps(out, indent=2)
            finally:
                db.close()
        except Exception as e:
            return json.dumps({"error": f"Knowledge graph lookup error: {e}", "nodes": []})
