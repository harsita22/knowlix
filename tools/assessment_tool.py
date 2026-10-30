"""Assessment Agent tool for Knowlix. Generates diagnostic quizzes and verifies student understanding."""
import json
from tools import Tool


class AssessmentGeneratorTool(Tool):
    name = "assessment_generator"
    description = (
        "Generate diagnostic assessment questions, multiple-choice options, rubric, "
        "and explanation keys for a target topic."
    )
    args_doc = '{"topic": "Recursion", "difficulty": "intermediate", "num_questions": 2}'

    def execute(self, topic, difficulty="intermediate", num_questions=2):
        t_clean = topic.strip().title()
        count = max(1, min(int(num_questions), 5))

        # Domain questions library for reliable curriculum assessment
        items = []
        if "recur" in t_clean.lower():
            items.append({
                "id": 1,
                "question": "What is the primary function of a base case in a recursive algorithm?",
                "options": [
                    "A) To speed up execution using multithreading",
                    "B) To terminate recursion and prevent stack overflow",
                    "C) To initialize local variables in the caller frame",
                    "D) To print intermediate variables to the console"
                ],
                "correct_option": "B",
                "explanation": "A base case specifies the terminating condition where the function returns directly without making further recursive calls."
            })
            items.append({
                "id": 2,
                "question": "When a recursive function executes, where are intermediate return states and local variables stored?",
                "options": [
                    "A) Heap memory",
                    "B) CPU registers exclusively",
                    "C) Call stack frames",
                    "D) Disk swap cache"
                ],
                "correct_option": "C",
                "explanation": "Each recursive call allocates a stack frame on the call stack, which is unwound in LIFO order upon reaching the base case."
            })
        elif "photo" in t_clean.lower():
            items.append({
                "id": 1,
                "question": "During which phase of photosynthesis is atmospheric carbon dioxide fixed into carbohydrates?",
                "options": [
                    "A) Light-dependent reactions in thylakoid membrane",
                    "B) Calvin cycle (light-independent reactions) in stroma",
                    "C) Citric acid cycle in mitochondrial matrix",
                    "D) Oxidative phosphorylation"
                ],
                "correct_option": "B",
                "explanation": "The Calvin cycle in the stroma uses ATP and NADPH produced by the light reactions to convert CO2 into glucose."
            })
            items.append({
                "id": 2,
                "question": "What is the primary source of the oxygen gas (O2) released as a byproduct during photosynthesis?",
                "options": [
                    "A) Splitting of water molecules (photolysis) in light reactions",
                    "B) Breakdown of carbon dioxide in the Calvin cycle",
                    "C) Decomposition of cellular glucose",
                    "D) Photorespiration in peroxisomes"
                ],
                "correct_option": "A",
                "explanation": "Light energy in photosystem II splits H2O molecules (photolysis), releasing oxygen gas and protons."
            })
        else:
            items.append({
                "id": 1,
                "question": f"Which of the following best defines the core principle of {t_clean}?",
                "options": [
                    f"A) A foundational rule in {t_clean} applied under standard conditions",
                    f"B) An obsolete hypothesis superseded by modern methods",
                    f"C) An exception that occurs only during error recovery",
                    f"D) A random variation dependent on hardware execution"
                ],
                "correct_option": "A",
                "explanation": f"The core principle of {t_clean} governs its fundamental behavior and prerequisite relationships."
            })

        return json.dumps({
            "topic": t_clean,
            "difficulty": difficulty,
            "questions": items[:count],
            "total_questions": len(items[:count])
        }, indent=2)
