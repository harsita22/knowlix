"""Tool registry for Knowlix. Coordinates all ReAct agent capabilities."""


class Tool:
    name = "tool"
    description = ""
    args_doc = "{}"

    def execute(self, **kwargs):
        raise NotImplementedError


def build_tools():
    from tools.calculator import Calculator
    from tools.data_query import ListFiles, ReadFile, SqlQuery
    from tools.web_search import WebSearch
    from tools.student_performance import StudentPerformance
    from tools.knowledge_graph_tool import KnowledgeGraphTool
    from tools.misconception_tool import MisconceptionTool
    from tools.curriculum_retrieval import CurriculumRetrieval
    from tools.adaptive_tutor_tool import AdaptiveTutorTool
    from tools.recovery_planner_tool import RecoveryPlannerTool
    from tools.assessment_tool import AssessmentGeneratorTool
    from tools.intervention_tool import InterventionRecommendationTool

    tools = [
        # Foundation Starter Tools
        ListFiles(),
        ReadFile(),
        SqlQuery(),
        Calculator(),
        WebSearch(),
        # Knowlix Modular Capabilities
        StudentPerformance(),
        KnowledgeGraphTool(),
        MisconceptionTool(),
        CurriculumRetrieval(),
        AdaptiveTutorTool(),
        RecoveryPlannerTool(),
        AssessmentGeneratorTool(),
        InterventionRecommendationTool(),
    ]
    return {t.name: t for t in tools}
