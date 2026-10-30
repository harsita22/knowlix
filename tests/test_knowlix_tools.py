"""Offline unit tests for all Knowlix modular tools."""
import json
import unittest
from tools import build_tools


class TestKnowlixTools(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tools = build_tools()

    def test_all_tools_registered(self):
        expected_tools = [
            "list_files", "read_file", "sql_query", "calculator", "web_search",
            "student_performance", "knowledge_graph", "misconception_analysis",
            "curriculum_retrieval", "adaptive_tutor", "recovery_planner",
            "assessment_generator", "intervention_recommendation"
        ]
        for name in expected_tools:
            self.assertIn(name, self.tools, f"Missing tool: {name}")

    def test_student_performance_analysis(self):
        res = json.loads(self.tools["student_performance"].execute(student_id="S1"))
        self.assertIn("topics", res)
        self.assertIn("weak_topics", res)
        self.assertTrue(len(res["topics"]) > 0 or len(res.get("weak_topics", [])) >= 0)

    def test_knowledge_graph_prerequisite_lookup(self):
        res = json.loads(self.tools["knowledge_graph"].execute(target_topic="Recursion", student_id="S1"))
        self.assertIn("prerequisites", res)
        self.assertTrue(any("Function" in p.get("name", "") for p in res["prerequisites"]))

    def test_misconception_detection(self):
        res = json.loads(self.tools["misconception_analysis"].execute(student_id="S1", topic="Recursion"))
        self.assertIn("detected_misconceptions", res)
        self.assertTrue(len(res["detected_misconceptions"]) > 0)
        self.assertIn("confidence_score", res["detected_misconceptions"][0])

    def test_curriculum_retrieval(self):
        res = json.loads(self.tools["curriculum_retrieval"].execute(query="photosynthesis light reaction"))
        self.assertIn("matches", res)
        self.assertTrue(len(res["matches"]) > 0)
        self.assertIn("source", res["matches"][0])

    def test_adaptive_tutor_scaffolding(self):
        res = json.loads(self.tools["adaptive_tutor"].execute(topic="Recursion", style="analogy"))
        self.assertIn("pedagogical_strategy", res)
        self.assertIn("comprehension_check_question", res)
        self.assertIn("nesting dolls", res["pedagogical_strategy"].lower())

    def test_recovery_planner(self):
        res = json.loads(self.tools["recovery_planner"].execute(student_id="S1", weak_topic="Recursion", available_days=3))
        self.assertIn("daily_schedule", res)
        self.assertEqual(len(res["daily_schedule"]), 3)
        self.assertTrue(res["total_estimated_hours"] > 0)

    def test_assessment_generator(self):
        res = json.loads(self.tools["assessment_generator"].execute(topic="Photosynthesis", num_questions=2))
        self.assertIn("questions", res)
        self.assertEqual(len(res["questions"]), 2)
        self.assertIn("correct_option", res["questions"][0])

    def test_intervention_recommendation(self):
        res = json.loads(self.tools["intervention_recommendation"].execute(student_id="S1", topic="Recursion"))
        self.assertIn("teacher_actionable_recommendations", res)
        self.assertTrue(res["needs_intervention"])


if __name__ == "__main__":
    unittest.main()

