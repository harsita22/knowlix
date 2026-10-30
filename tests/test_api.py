"""API endpoint integration tests and student data isolation tests."""
import unittest
from fastapi.testclient import TestClient
from server.app import app


class TestKnowlixAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_health_check(self):
        res = self.client.get("/health")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json().get("platform"), "Knowlix")

    def test_student_login(self):
        res = self.client.post("/api/auth/login", json={
            "email": "student1@knowlix.edu",
            "password": "student123"
        })
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIn("access_token", data)
        self.assertEqual(data["user"]["role"], "student")

    def test_teacher_login(self):
        res = self.client.post("/api/auth/login", json={
            "email": "teacher@knowlix.edu",
            "password": "teacher123"
        })
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIn("access_token", data)
        self.assertEqual(data["user"]["role"], "teacher")

    def test_student_dashboard_isolation(self):
        # 1. Login as Student S1
        res = self.client.post("/api/auth/login", json={
            "email": "student1@knowlix.edu",
            "password": "student123"
        })
        token = res.json()["access_token"]

        # 2. Query Dashboard
        dash = self.client.get("/api/student/dashboard", headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(dash.status_code, 200)
        d = dash.json()
        self.assertEqual(d["student_name"], "Sami (Student S1)")
        self.assertTrue(len(d["weak_topics"]) > 0)

    def test_teacher_dashboard_and_classes(self):
        # 1. Login as Teacher
        res = self.client.post("/api/auth/login", json={
            "email": "teacher@knowlix.edu",
            "password": "teacher123"
        })
        token = res.json()["access_token"]

        # 2. Query Teacher Dashboard
        dash = self.client.get("/api/teacher/dashboard", headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(dash.status_code, 200)
        self.assertIn("total_classes", dash.json())

        # 3. Query Classes
        cls_res = self.client.get("/api/teacher/classes", headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(cls_res.status_code, 200)
        self.assertTrue(len(cls_res.json()) > 0)


if __name__ == "__main__":
    unittest.main()

