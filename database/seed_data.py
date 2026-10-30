"""Seed realistic demo and benchmark data for Knowlix."""
import os
import sys
from server.auth import hash_password

from database.connection import init_db, SessionLocal
from database.models import (
    User, TeacherClass, StudentEnrollment, Subject, Topic, TopicPrerequisite,
    TopicMastery, Misconception, StudentAssessment, StudentAnswer, StudyPlan,
    StudyPlanTask, CurriculumDocument, CurriculumChunk, InterventionHistory
)


def seed_all():
    init_db()
    db = SessionLocal()
    try:
        if db.query(User).filter_by(email="teacher@knowlix.edu").first():
            return "Database already seeded."

        # 1. Users
        teacher = User(
            email="teacher@knowlix.edu",
            hashed_password=hash_password("teacher123"),
            full_name="Dr. Alan Turing",
            role="teacher"
        )
        teacher_demo = User(
            email="teacher@knowlix.demo",
            hashed_password=hash_password("teacher123"),
            full_name="Demo Teacher",
            role="teacher"
        )
        student1 = User(
            email="student1@knowlix.edu",
            hashed_password=hash_password("student123"),
            full_name="Sami (Student S1)",
            role="student"
        )
        student_demo = User(
            email="student@knowlix.demo",
            hashed_password=hash_password("student123"),
            full_name="Demo Student",
            role="student"
        )
        student2 = User(
            email="student2@knowlix.edu",
            hashed_password=hash_password("student123"),
            full_name="Maya Lin (Student S2)",
            role="student"
        )
        db.add_all([teacher, teacher_demo, student1, student_demo, student2])
        db.commit()

        # 2. Classes
        class_math = TeacherClass(name="Grade 10 Mathematics", teacher_id=teacher.id, subject="Mathematics", grade_level="Grade 10")
        class_cs = TeacherClass(name="AP Computer Science A", teacher_id=teacher.id, subject="Computer Science", grade_level="Grade 11")
        db.add_all([class_math, class_cs])
        db.commit()

        # 3. Enrollments
        db.add_all([
            StudentEnrollment(student_id=student1.id, class_id=class_cs.id),
            StudentEnrollment(student_id=student1.id, class_id=class_math.id),
            StudentEnrollment(student_id=student_demo.id, class_id=class_cs.id),
            StudentEnrollment(student_id=student_demo.id, class_id=class_math.id),
            StudentEnrollment(student_id=student2.id, class_id=class_cs.id),
        ])
        db.commit()

        # 4. Subjects
        sub_cs = Subject(code="CS", name="Computer Science", description="Core computing principles, algorithms, and data structures.")
        sub_math = Subject(code="MATH", name="Mathematics", description="Algebra, geometry, polynomials, and calculus foundations.")
        sub_bio = Subject(code="BIO", name="Biology", description="Cellular biology, genetics, ecology, and plant systems.")
        db.add_all([sub_cs, sub_math, sub_bio])
        db.commit()

        # 5. Topics
        # CS topics
        t_vars = Topic(subject_id=sub_cs.id, chapter="Basics", name="Variables & Data Types", difficulty="beginner", description="Data representation, primitives, and memory.")
        t_control = Topic(subject_id=sub_cs.id, chapter="Control Flow", name="Conditionals & Loops", difficulty="beginner", description="If-else branches, while, and for loops.")
        t_arrays = Topic(subject_id=sub_cs.id, chapter="Data Structures", name="Arrays & Lists", difficulty="intermediate", description="Contiguous memory indexing, iteration, and searching.")
        t_funcs = Topic(subject_id=sub_cs.id, chapter="Modular Code", name="Functions & Scope", difficulty="intermediate", description="Call stack, parameters, return values, and variable scope.")
        t_rec = Topic(subject_id=sub_cs.id, chapter="Algorithms", name="Recursion", difficulty="advanced", description="Recursive base cases, call stack unwinding, and divide-and-conquer.")
        t_sort = Topic(subject_id=sub_cs.id, chapter="Algorithms", name="Sorting Algorithms", difficulty="intermediate", description="Bubble sort, merge sort, and algorithmic efficiency.")

        # Math topics
        t_m_vars = Topic(subject_id=sub_math.id, chapter="Algebra", name="Algebraic Expressions", difficulty="beginner", description="Symbols, coefficients, and linear terms.")
        t_m_linear = Topic(subject_id=sub_math.id, chapter="Algebra", name="Linear Equations", difficulty="beginner", description="Solving single variable and systems of linear equations.")
        t_m_factor = Topic(subject_id=sub_math.id, chapter="Algebra", name="Factoring Polynomials", difficulty="intermediate", description="Factoring quadratic trinomials and difference of squares.")
        t_m_quad = Topic(subject_id=sub_math.id, chapter="Algebra", name="Quadratic Equations", difficulty="advanced", description="Quadratic formula, vertex form, and roots.")

        # Bio topics
        t_b_cell = Topic(subject_id=sub_bio.id, chapter="Cell Biology", name="Cell Structure", difficulty="beginner", description="Organelles, membrane, chloroplasts, and mitochondria.")
        t_b_photo = Topic(subject_id=sub_bio.id, chapter="Bioenergetics", name="Photosynthesis", difficulty="intermediate", description="Light-dependent reactions and Calvin cycle synthesizing glucose using sunlight and CO2.")

        topics = [t_vars, t_control, t_arrays, t_funcs, t_rec, t_sort, t_m_vars, t_m_linear, t_m_factor, t_m_quad, t_b_cell, t_b_photo]
        db.add_all(topics)
        db.commit()

        # 6. Prerequisites
        prereqs = [
            TopicPrerequisite(topic_id=t_control.id, prerequisite_topic_id=t_vars.id, strength="required"),
            TopicPrerequisite(topic_id=t_arrays.id, prerequisite_topic_id=t_control.id, strength="required"),
            TopicPrerequisite(topic_id=t_funcs.id, prerequisite_topic_id=t_control.id, strength="required"),
            TopicPrerequisite(topic_id=t_rec.id, prerequisite_topic_id=t_funcs.id, strength="required"),
            TopicPrerequisite(topic_id=t_sort.id, prerequisite_topic_id=t_arrays.id, strength="required"),
            TopicPrerequisite(topic_id=t_sort.id, prerequisite_topic_id=t_rec.id, strength="recommended"),
            TopicPrerequisite(topic_id=t_m_linear.id, prerequisite_topic_id=t_m_vars.id, strength="required"),
            TopicPrerequisite(topic_id=t_m_factor.id, prerequisite_topic_id=t_m_vars.id, strength="required"),
            TopicPrerequisite(topic_id=t_m_quad.id, prerequisite_topic_id=t_m_linear.id, strength="required"),
            TopicPrerequisite(topic_id=t_m_quad.id, prerequisite_topic_id=t_m_factor.id, strength="required"),
            TopicPrerequisite(topic_id=t_b_photo.id, prerequisite_topic_id=t_b_cell.id, strength="required"),
        ]
        db.add_all(prereqs)
        db.commit()

        # 7. Topic Mastery for Student S1 & Demo Student
        for s_user in [student1, student_demo]:
            db.add_all([
                TopicMastery(student_id=s_user.id, topic_id=t_arrays.id, mastery_score=82.0, attempts=3, accuracy=0.85, status="mastered"),
                TopicMastery(student_id=s_user.id, topic_id=t_sort.id, mastery_score=64.0, attempts=4, accuracy=0.62, status="in_progress"),
                TopicMastery(student_id=s_user.id, topic_id=t_rec.id, mastery_score=31.0, attempts=5, accuracy=0.28, status="struggling"),
                TopicMastery(student_id=s_user.id, topic_id=t_funcs.id, mastery_score=78.0, attempts=2, accuracy=0.80, status="mastered"),
                TopicMastery(student_id=s_user.id, topic_id=t_m_linear.id, mastery_score=88.0, attempts=3, accuracy=0.90, status="mastered"),
                TopicMastery(student_id=s_user.id, topic_id=t_m_quad.id, mastery_score=45.0, attempts=3, accuracy=0.45, status="struggling"),
            ])
        db.commit()

        # 8. Misconceptions for Student S1 & Demo Student
        for s_user in [student1, student_demo]:
            db.add_all([
                Misconception(
                    student_id=s_user.id,
                    topic_id=t_rec.id,
                    description="Confuses recursive stack unwinding with iterative loops, omitting base-case return values.",
                    evidence="Repeatedly fails recursive return step in factorial and Fibonacci quiz; wrote return f(n-1) without accumulating return value.",
                    confidence_score=0.92,
                    suggested_correction="Illustrate execution tree with visual activation frames showing value propagation backward.",
                    resolution_status="detected"
                ),
                Misconception(
                    student_id=s_user.id,
                    topic_id=t_m_quad.id,
                    description="Attempts to apply square root directly to both sides of quadratic equation before isolating the square term.",
                    evidence="Solved x^2 + 6x + 9 = 25 by taking sqrt(x^2) + sqrt(6x) + 3.",
                    confidence_score=0.88,
                    suggested_correction="Review distributive properties and difference of squares before taking radicals.",
                    resolution_status="detected"
                )
            ])
        db.commit()

        # 9. Assessments & Answers
        ass1 = StudentAssessment(
            student_id=student1.id,
            topic_id=t_rec.id,
            title="Recursion Diagnostic Assessment",
            score=31.0,
            total_points=100.0,
            passed=False
        )
        db.add(ass1)
        db.commit()

        db.add_all([
            StudentAnswer(
                assessment_id=ass1.id,
                question_text="What happens when a recursive function reaches its base case?",
                student_answer="It restarts the loop from n = 0.",
                correct_answer="It returns a value and begins unwinding the call stack.",
                is_correct=False,
                mistake_pattern="Base-case return misunderstood as loop reset"
            ),
            StudentAnswer(
                assessment_id=ass1.id,
                question_text="Identify the error in: def fact(n): return n * fact(n-1)",
                student_answer="Missing return type in function definition.",
                correct_answer="Missing base case (causes infinite recursion / stack overflow).",
                is_correct=False,
                mistake_pattern="Ignored missing termination condition"
            )
        ])
        db.commit()

        # 10. Study Plan for S1
        plan = StudyPlan(
            student_id=student1.id,
            subject_id=sub_cs.id,
            title="Recursion & Prerequisite Mastery Recovery Plan",
            total_estimated_hours=4.5,
            status="active"
        )
        db.add(plan)
        db.commit()

        db.add_all([
            StudyPlanTask(study_plan_id=plan.id, topic_id=t_funcs.id, day_number=1, order_index=1, task_type="concept_review", description="Review Call Stack & Frame Lifecycles in Functions", duration_minutes=30),
            StudyPlanTask(study_plan_id=plan.id, topic_id=t_rec.id, day_number=1, order_index=2, task_type="practice_drill", description="Trace 3 simple recursive tree diagrams (Factorial, Countdown)", duration_minutes=45),
            StudyPlanTask(study_plan_id=plan.id, topic_id=t_rec.id, day_number=2, order_index=1, task_type="concept_review", description="Mastering Base Cases: When and What to Return", duration_minutes=40),
            StudyPlanTask(study_plan_id=plan.id, topic_id=t_rec.id, day_number=2, order_index=2, task_type="practice_drill", description="Write and debug recursive string reversal and array sum", duration_minutes=45),
            StudyPlanTask(study_plan_id=plan.id, topic_id=t_rec.id, day_number=3, order_index=1, task_type="quiz", description="Complete Recursion Mastery Re-Assessment", duration_minutes=30),
        ])
        db.commit()

        # 11. Teacher Intervention
        db.add(InterventionHistory(
            student_id=student1.id,
            teacher_id=teacher.id,
            topic_id=t_rec.id,
            trigger_reason="Persistent low score (31%) and 2 consecutive failed attempts on recursion base cases.",
            recommendation="Schedule a 10-minute 1-on-1 Socratic call-stack walkthrough or assign visual tracing interactive module.",
            severity="warning",
            action_taken="Assigned visual recovery plan"
        ))
        db.commit()

        # 12. Curriculum Documents & Chunks
        doc_bio = CurriculumDocument(
            uploader_id=teacher.id,
            subject_id=sub_bio.id,
            title="Cellular Biology & Photosynthesis Standard Curriculum",
            file_type="txt",
            file_path="data/sample_curriculum/biology_photosynthesis.txt"
        )
        doc_cs = CurriculumDocument(
            uploader_id=teacher.id,
            subject_id=sub_cs.id,
            title="AP Computer Science Algorithms & Recursion Guide",
            file_type="txt",
            file_path="data/sample_curriculum/cs_recursion.txt"
        )
        db.add_all([doc_bio, doc_cs])
        db.commit()

        db.add_all([
            CurriculumChunk(
                document_id=doc_bio.id,
                topic_id=t_b_photo.id,
                chunk_index=1,
                content="Photosynthesis is the process by which autotrophic organisms convert light energy into chemical energy stored in glucose bonds. Equation: 6CO2 + 6H2O + light -> C6H12O6 + 6O2. It takes place in plant chloroplasts across two stages: light-dependent reactions in thylakoid membranes (generating ATP and NADPH), and light-independent Calvin cycle in the stroma (fixing CO2 into sugars).",
                metadata_json={"source": "AP Biology Chapter 8", "section": "8.1 Overview of Photosynthesis"}
            ),
            CurriculumChunk(
                document_id=doc_cs.id,
                topic_id=t_rec.id,
                chunk_index=1,
                content="A recursive algorithm solves a problem by breaking it down into smaller subproblems of the exact same type. Every valid recursive function requires: 1) A base case that stops execution and returns a direct answer without further recursion, and 2) A recursive step that moves toward the base case. Without a proper base case, stack overflow error occurs.",
                metadata_json={"source": "Computer Science Principles", "section": "Algorithms: Recursion and the Call Stack"}
            ),
        ])
        db.commit()

        return "Successfully seeded Knowlix database with users, subjects, topics, prerequisites, assessments, and curriculum."
    finally:
        db.close()


if __name__ == "__main__":
    msg = seed_all()
    print(msg)
