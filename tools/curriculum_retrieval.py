"""Curriculum Retrieval Agent (RAG) for Knowlix. Grounds educational explanations in validated curriculum."""
import json
import os
import re
from tools import Tool
import config


class CurriculumRetrieval(Tool):
    name = "curriculum_retrieval"
    description = (
        "Retrieve grounded educational curriculum excerpts and textbook explanations for a topic or concept. "
        "Provides official learning objectives, definitions, and citations."
    )
    args_doc = '{"query": "photosynthesis light dependent reactions", "subject": "Biology"}'

    def execute(self, query, subject=None):
        results = {
            "query": query,
            "subject": subject or "All",
            "matches": [],
            "grounding_status": "grounded",
            "source_citations": []
        }

        query_terms = set(re.findall(r"\w+", query.lower()))

        # 1. Search Database Curriculum Chunks
        try:
            from database.connection import SessionLocal
            from database.models import CurriculumChunk, CurriculumDocument, Topic, Subject
            db = SessionLocal()
            try:
                q = db.query(CurriculumChunk, CurriculumDocument, Topic, Subject).join(
                    CurriculumDocument, CurriculumChunk.document_id == CurriculumDocument.id
                ).outerjoin(
                    Topic, CurriculumChunk.topic_id == Topic.id
                ).outerjoin(
                    Subject, CurriculumDocument.subject_id == Subject.id
                )

                if subject:
                    q = q.filter((Subject.name.ilike(f"%{subject}%")) | (Subject.code.ilike(f"%{subject}%")))

                chunks = q.all()
                scored_chunks = []
                for chunk, doc, topic, subj in chunks:
                    text = chunk.content.lower()
                    overlap = sum(1 for term in query_terms if term in text)
                    if topic and any(term in topic.name.lower() for term in query_terms):
                        overlap += 3
                    if overlap > 0:
                        scored_chunks.append((overlap, chunk, doc, topic, subj))

                scored_chunks.sort(key=lambda x: x[0], reverse=True)
                for score, chunk, doc, topic, subj in scored_chunks[:3]:
                    source_title = doc.title if doc else "Curriculum Standard"
                    meta = chunk.metadata_json or {}
                    section = meta.get("section", topic.name if topic else "General")
                    results["matches"].append({
                        "content": chunk.content,
                        "topic": topic.name if topic else "General",
                        "subject": subj.name if subj else "General",
                        "source": f"{source_title} - Section: {section}",
                        "relevance_score": score
                    })
                    results["source_citations"].append(f"{source_title} ({section})")
            finally:
                db.close()
        except Exception:
            pass

        # 2. If no DB matches, search local curriculum files in data/
        if not results["matches"]:
            curriculum_dir = os.path.join(config.DATA_DIR, "sample_curriculum")
            if os.path.exists(curriculum_dir):
                for fname in os.listdir(curriculum_dir):
                    fpath = os.path.join(curriculum_dir, fname)
                    if os.path.isfile(fpath) and fname.endswith((".txt", ".md", ".csv")):
                        try:
                            with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                                content = f.read()
                            overlap = sum(1 for term in query_terms if term in content.lower())
                            if overlap > 0:
                                results["matches"].append({
                                    "content": content[:1500],
                                    "topic": fname.replace(".txt", "").replace("_", " ").title(),
                                    "source": f"Local Curriculum File: {fname}",
                                    "relevance_score": overlap
                                })
                                results["source_citations"].append(fname)
                        except Exception:
                            continue

        if not results["matches"]:
            results["grounding_status"] = "no_curriculum_found"
            results["message"] = (
                f"No uploaded curriculum documents matched '{query}'. "
                f"You may use web_search to find authoritative public curriculum or state clearly that official local curriculum was unavailable."
            )
            return json.dumps(results, indent=2)

        results["summary"] = f"Found {len(results['matches'])} relevant curriculum reference(s)."
        return json.dumps(results, indent=2)
