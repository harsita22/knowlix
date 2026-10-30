"""Adaptive Tutor tool for Knowlix. Calibrates pedagogical guidance, analogies, and differentiated explanations."""
import json
from tools import Tool


class AdaptiveTutorTool(Tool):
    name = "adaptive_tutor"
    description = (
        "Generate pedagogical explanations tailored to a student's learning style "
        "(e.g., 'analogy', 'step_by_step', 'simple', 'example_based', 'practice'). "
        "Provides scaffolding, analogies, and comprehension check questions."
    )
    args_doc = '{"topic": "Recursion", "style": "analogy", "student_level": "beginner"}'

    def execute(self, topic, style="step_by_step", student_level="intermediate", known_misconceptions=None):
        style = style.lower()
        topic_clean = topic.strip().title()

        # Pedagogical templates & strategies based on educational research
        scaffolding = {
            "analogy": (
                f"Analogy approach for {topic_clean}: Connect the abstract concept to an everyday tangible experience. "
                f"For recursion: like a stack of Russian nesting dolls (matryoshka), where each doll opens to reveal a smaller one until the solid inner doll (the base case) is reached; then you assemble them back. "
                f"For photosynthesis: like a solar-powered bakery where sunlight is electricity, carbon dioxide and water are raw flour and sugar, and glucose is the baked bread."
            ),
            "step_by_step": (
                f"Step-by-step breakdown for {topic_clean}: "
                f"1. Establish foundational definition and prerequisite grounding. "
                f"2. Deconstruct the primary mechanism into sequential phases. "
                f"3. Highlight the critical decision boundary or boundary condition. "
                f"4. Trace one concrete walkthrough showing inputs transforming into outputs."
            ),
            "example_based": (
                f"Example-first approach for {topic_clean}: Start with a minimal working scenario before generalizing rules. "
                f"Show input -> intermediate steps -> final outcome."
            ),
            "simple": (
                f"Intuitive, plain-language explanation for {topic_clean}: Avoid heavy technical jargon. "
                f"Focus on the core 'why' and 'how' in two conversational paragraphs."
            ),
            "practice": (
                f"Active recall challenge for {topic_clean}: Present an interactive micro-drill with 1 diagnostic check question."
            )
        }

        strategy = scaffolding.get(style, scaffolding["step_by_step"])

        check_question = (
            f"Comprehension Check: In your own words, what role does the boundary condition or base case play in {topic_clean}, "
            f"and what happens if it is omitted?"
        )

        response = {
            "topic": topic_clean,
            "selected_style": style,
            "target_student_level": student_level,
            "pedagogical_strategy": strategy,
            "recommended_tone": "Warm, encouraging, intellectually respectful, and growth-mindset focused.",
            "comprehension_check_question": check_question
        }

        if known_misconceptions:
            response["caution_flag"] = f"Address this known misconception proactively: {known_misconceptions}"

        return json.dumps(response, indent=2)
