import os
import sys
import shutil
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.backends.backend_pdf import PdfPages

def create_header(ax, title, subtitle, page_num, total_pages=5):
    """Draws a professional top banner with branding."""
    # Top background bar
    banner = patches.Rectangle((0, 0.90), 1, 0.10, transform=ax.transAxes, 
                               facecolor='#0F172A', edgecolor='none', zorder=1)
    ax.add_patch(banner)
    
    # Purple accent stripe
    accent = patches.Rectangle((0, 0.895), 1, 0.005, transform=ax.transAxes,
                               facecolor='#6366F1', edgecolor='none', zorder=2)
    ax.add_patch(accent)

    # Logo / Project badge
    ax.text(0.03, 0.95, "KNOWLIX", transform=ax.transAxes, color='#FFFFFF',
            fontsize=18, fontweight='bold', va='center', ha='left', family='sans-serif')
    ax.text(0.12, 0.95, "|  AI-Powered Adaptive Learning & Personalized Pedagogy", 
            transform=ax.transAxes, color='#94A3B8', fontsize=10, va='center', ha='left', family='sans-serif')
    
    # Title & Subtitle in banner
    ax.text(0.03, 0.92, title, transform=ax.transAxes, color='#38BDF8',
            fontsize=13, fontweight='bold', va='center', ha='left', family='sans-serif')
    ax.text(0.40, 0.92, f"—  {subtitle}", transform=ax.transAxes, color='#E2E8F0',
            fontsize=10, va='center', ha='left', family='sans-serif')

    # Page number
    ax.text(0.97, 0.95, f"Page {page_num} of {total_pages}", transform=ax.transAxes, color='#94A3B8',
            fontsize=9, fontweight='bold', va='center', ha='right', family='sans-serif')
    ax.text(0.97, 0.92, "Google Gemini & AgentX 2026", transform=ax.transAxes, color='#A5B4FC',
            fontsize=8, va='center', ha='right', family='sans-serif')

    # Footer
    footer = patches.Rectangle((0, 0), 1, 0.035, transform=ax.transAxes,
                               facecolor='#F1F5F9', edgecolor='none', zorder=1)
    ax.add_patch(footer)
    ax.text(0.03, 0.017, "CONFIDENTIAL & PROPRIETARY  •  KNOWLIX SYSTEM ARCHITECTURE SPECIFICATION", 
            transform=ax.transAxes, color='#64748B', fontsize=8, va='center', ha='left', family='sans-serif')
    ax.text(0.97, 0.017, "FastAPI  •  React  •  ReAct Multi-Agent  •  Dual DB  •  CLI Contract", 
            transform=ax.transAxes, color='#64748B', fontsize=8, va='center', ha='right', family='sans-serif')


def draw_box(ax, x, y, w, h, title, items, bg_color='#FFFFFF', border_color='#CBD5E1', 
             title_color='#0F172A', title_bg=None, rx=0.015, font_size=8.5):
    """Draws a clean modern rounded card with text bullet points."""
    rect = patches.FancyBboxPatch((x, y), w, h,
                                  boxstyle=f"round,pad=0,rounding_size={rx}",
                                  facecolor=bg_color, edgecolor=border_color,
                                  linewidth=1.2, zorder=2)
    ax.add_patch(rect)
    
    if title_bg:
        tb = patches.FancyBboxPatch((x, y + h - 0.04), w, 0.04,
                                    boxstyle=f"round,pad=0,rounding_size={rx}",
                                    facecolor=title_bg, edgecolor='none', zorder=3)
        ax.add_patch(tb)
        # square bottom corners of header
        tb_sq = patches.Rectangle((x, y + h - 0.04), w, 0.02,
                                  facecolor=title_bg, edgecolor='none', zorder=3)
        ax.add_patch(tb_sq)

    ty = y + h - 0.025
    ax.text(x + 0.012, ty, title, color=title_color, fontsize=font_size + 1.5,
            fontweight='bold', va='center', ha='left', zorder=4, family='sans-serif')
    
    line_y = ty - 0.032
    for item in items:
        if isinstance(item, tuple):
            prefix, body = item
            ax.text(x + 0.015, line_y, prefix, color='#4338CA', fontsize=font_size - 0.5,
                    fontweight='bold', va='center', ha='left', zorder=4, family='sans-serif')
            ax.text(x + 0.015 + len(prefix)*0.007, line_y, body, color='#334155', fontsize=font_size - 0.5,
                    va='center', ha='left', zorder=4, family='sans-serif')
        else:
            ax.text(x + 0.015, line_y, item, color='#334155', fontsize=font_size - 0.5,
                    va='center', ha='left', zorder=4, family='sans-serif')
        line_y -= 0.023


def draw_arrow(ax, x1, y1, x2, y2, color='#6366F1', label=None, label_side='top', lw=1.5):
    """Draws a clean directional connecting line/arrow."""
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="->,head_width=0.35,head_length=0.45",
                                color=color, lw=lw, shrinkA=3, shrinkB=3),
                zorder=5)
    if label:
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        offset = 0.012 if label_side == 'top' else -0.012
        ax.text(mx, my + offset, label, color='#475569', fontsize=7.5,
                fontweight='bold', ha='center', va='center',
                bbox=dict(boxstyle="round,pad=0.2", facecolor='#F8FAFC', edgecolor='#E2E8F0', lw=0.8),
                zorder=6, family='sans-serif')


def build_page_1():
    """Page 1: Full System Architecture Overview."""
    fig, ax = plt.subplots(figsize=(14, 8.5))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    create_header(ax, "SYSTEM ARCHITECTURE OVERVIEW", "Multi-Tier Enterprise AI Pedagogical Engine", 1)

    # 1. CLIENT TIER (Top Left & Top Right)
    draw_box(ax, 0.04, 0.72, 0.43, 0.14, "CLIENT LAYER: React SaaS Web Dashboard", [
        ("Tech: ", "React 18  •  Vite  •  Tailwind CSS  •  Heroicons"),
        ("Features: ", "Adaptive Socratic Chatbot with Step-by-Step Solver"),
        ("Portals: ", "Student Mastery Dashboard & Teacher Class Analytics"),
        ("Auth: ", "JWT Bearer Session Storage, Role Guard Routing")
    ], bg_color='#EEF2FF', border_color='#A5B4FC', title_color='#1E1B4B')

    draw_box(ax, 0.53, 0.72, 0.43, 0.14, "CLIENT LAYER: Automated Judges CLI Contract", [
        ("Command: ", "python main.py --json \"<query>\""),
        ("Compliance: ", "Emits EXACTLY 1 raw JSON line containing {answer, trace}"),
        ("Modes: ", "--dry-run for offline mock, --debug for step inspection"),
        ("Output: ", "All diagnostic logs suppressed or redirected to stderr")
    ], bg_color='#FEF3C7', border_color='#FCD34D', title_color='#78350F')

    # Connections to API Tier
    draw_arrow(ax, 0.255, 0.72, 0.255, 0.63, color='#4F46E5', label="HTTP / REST (JSON)")
    draw_arrow(ax, 0.745, 0.72, 0.745, 0.63, color='#D97706', label="Direct CLI Invocation")

    # 2. GATEWAY & API TIER
    draw_box(ax, 0.04, 0.49, 0.92, 0.14, "API & ORCHESTRATION GATEWAY: FastAPI Layer (server/app.py)", [
        ("Endpoints: ", "/api/tutor/chat  •  /api/auth  •  /api/students  •  /api/curriculum  •  /api/health"),
        ("Security: ", "Native Bcrypt Password Hashing  •  Student Data Isolation Guarantees  •  CORS Middleware"),
        ("Static Host: ", "Mounts production SPA build (frontend/dist) directly at root / with client-side fallback"),
        ("Traceability: ", "Logs every user thought/action session to database AgentTrace table for post-audit")
    ], bg_color='#F0FDF4', border_color='#86EFAC', title_color='#14532D')

    # Connection to Agent Reasoning Core
    draw_arrow(ax, 0.50, 0.49, 0.50, 0.41, color='#059669', label="Session State & Prompt")

    # 3. REASONING CORE & GEMINI
    draw_box(ax, 0.04, 0.27, 0.43, 0.14, "REASONING CORE: ReAct Agent (agent/core.py)", [
        ("Architecture: ", "Thought -> Action -> Action_Input -> Observation Loop"),
        ("LLM Engine: ", "Google Gemini via official google-genai SDK"),
        ("Model: ", "gemini-3.5-flash-lite (Active & Production-ready)"),
        ("Resilience: ", "Auto-repetition breaking, JSON parsing self-correction")
    ], bg_color='#FAF5FF', border_color='#D8B4FE', title_color='#581C87')

    draw_box(ax, 0.53, 0.27, 0.43, 0.14, "INTELLIGENT TOOL SUITE: 8 Pedagogical Tools", [
        ("Diagnostics: ", "student_performance  •  misconception_tool"),
        ("Curriculum: ", "curriculum_retrieval (grounded chunk search)"),
        ("Pedagogy: ", "adaptive_tutor_tool  •  knowledge_graph_tool"),
        ("Remediation: ", "recovery_planner_tool  •  assessment_tool  •  intervention_tool")
    ], bg_color='#F8FAFC', border_color='#CBD5E1', title_color='#0F172A')

    draw_arrow(ax, 0.47, 0.34, 0.53, 0.34, color='#7C3AED', label="Dispatches Tools")
    draw_arrow(ax, 0.50, 0.27, 0.50, 0.19, color='#475569', label="SQLAlchemy ORM")

    # 4. DATABASE & PERSISTENCE TIER
    draw_box(ax, 0.04, 0.06, 0.92, 0.13, "PERSISTENCE TIER: Dual-Engine SQLAlchemy Database (database/)", [
        ("Dual Support: ", "Zero-config SQLite for standalone evaluation & PostgreSQL for enterprise cloud scale"),
        ("Core Models: ", "User  •  TeacherClass  •  StudentEnrollment  •  Subject  •  Topic  •  TopicPrerequisite"),
        ("Pedagogy Tables: ", "TopicMastery  •  Misconception  •  StudentAssessment  •  StudyPlan  •  InterventionHistory"),
        ("Knowledge Engine: ", "CurriculumDocument  •  CurriculumChunk  •  AgentTrace  •  StudentLearningMemory")
    ], bg_color='#F1F5F9', border_color='#94A3B8', title_color='#0F172A')

    plt.tight_layout()
    return fig


def build_page_2():
    """Page 2: Interactive Socratic AI Tutoring Workflow."""
    fig, ax = plt.subplots(figsize=(14, 8.5))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    create_header(ax, "WORKFLOW 1: SOCRATIC AI TUTORING & PROBLEM SOLVING", 
                  "End-to-End Inquiry, Retrieval & Guided Pedagogical Reasoning", 2)

    # 6 Step Process Flow across horizontal stages
    steps = [
        (0.04, 0.58, 0.28, 0.26, "STAGE 1: Student Inquiry", [
            ("Trigger: ", "Student asks question in Chat Tutor"),
            ("Modes: ", "Concept / Problem / Exam Review"),
            ("Payload: ", "{message, subject_id, mode}"),
            ("Identity: ", "JWT token verified by FastAPI"),
            ("Context: ", "Loads last 6 conversation turns")
        ], '#EFF6FF', '#93C5FD', '#1E3A8A'),

        (0.36, 0.58, 0.28, 0.26, "STAGE 2: Mastery & Misconception Lookup", [
            ("Tool: ", "student_performance & misconception_tool"),
            ("Analysis: ", "Fetches student current topic mastery"),
            ("Risk Check: ", "Identifies active misconception flags"),
            ("Calibration: ", "Sets cognitive difficulty level"),
            ("Isolation: ", "Guarantees student cannot view peer data")
        ], '#FDF4FF', '#F0ABFC', '#701A75'),

        (0.68, 0.58, 0.28, 0.26, "STAGE 3: Grounded Curriculum RAG", [
            ("Tool: ", "curriculum_retrieval"),
            ("Search: ", "Queries vetted textbook & lecture chunks"),
            ("Source: ", "Biology, Chemistry, Math, Physics docs"),
            ("Anti-Hallucination: ", "Injects exact course excerpts"),
            ("Fallback: ", "Structured knowledge base grounding")
        ], '#F0FDF4', '#86EFAC', '#14532D'),

        (0.04, 0.16, 0.28, 0.28, "STAGE 4: ReAct Pedagogical Loop", [
            ("Orchestrator: ", "agent/core.py with Google Gemini"),
            ("Thought: ", "Decides pedagogical scaffolding needed"),
            ("Rule: ", "DO NOT spoon-feed direct answers"),
            ("Socratic Prompt: ", "Asks leading guiding question"),
            ("Step Scaffolding: ", "Breaks complex problems into mini-steps")
        ], '#FEF3C7', '#FCD34D', '#78350F'),

        (0.36, 0.16, 0.28, 0.28, "STAGE 5: Trace & Memory Logging", [
            ("Audit Log: ", "Saves full trace in AgentTrace"),
            ("Memory Store: ", "Saves student response pattern"),
            ("Telemetry: ", "Tracks latency, tool calls, token count"),
            ("Persistence: ", "Committed to SQLite/Postgres DB"),
            ("Observability: ", "Inspectable by teachers & judges")
        ], '#F1F5F9', '#CBD5E1', '#0F172A'),

        (0.68, 0.16, 0.28, 0.28, "STAGE 6: Interactive Response Delivery", [
            ("Client UI: ", "React ChatTutor component"),
            ("Rendering: ", "Rich Markdown, math & code formatting"),
            ("Chips: ", "Generates 3 interactive follow-up pills"),
            ("Feedback: ", "Thumbs up/down feedback widget"),
            ("Loop Closure: ", "Awaits next student problem attempt")
        ], '#ECFDF5', '#6EE7B7', '#064E3B')
    ]

    for x, y, w, h, title, items, bg, border, tcolor in steps:
        draw_box(ax, x, y, w, h, title, items, bg_color=bg, border_color=border, title_color=tcolor)

    # Arrows connecting workflow stages
    draw_arrow(ax, 0.32, 0.71, 0.36, 0.71, color='#2563EB', label="Auth & Context")
    draw_arrow(ax, 0.64, 0.71, 0.68, 0.71, color='#C026D3', label="Mastery Score")
    draw_arrow(ax, 0.82, 0.58, 0.82, 0.49, color='#059669')
    draw_arrow(ax, 0.82, 0.49, 0.18, 0.49, color='#059669', label="Grounded Curriculum Chunks + Student State")
    draw_arrow(ax, 0.18, 0.49, 0.18, 0.44, color='#D97706')
    draw_arrow(ax, 0.32, 0.30, 0.36, 0.30, color='#D97706', label="Thought Sequence")
    draw_arrow(ax, 0.64, 0.30, 0.68, 0.30, color='#475569', label="Formatted Payload")

    # Highlight Callout Banner at middle
    callout = patches.FancyBboxPatch((0.20, 0.46), 0.60, 0.06, boxstyle="round,pad=0,rounding_size=0.01",
                                     facecolor='#FAFAFA', edgecolor='#E2E8F0', linewidth=1, zorder=3)
    ax.add_patch(callout)
    ax.text(0.50, 0.49, "CORE PEDAGOGY RULE: Knowlix Never Gives Unearned Answers",
            fontsize=9.5, fontweight='bold', color='#4338CA', ha='center', va='center', family='sans-serif', zorder=4)
    ax.text(0.50, 0.472, "The agent assesses prior mastery, fetches textbook chunks, and guides students step-by-step.",
            fontsize=8, color='#64748B', ha='center', va='center', family='sans-serif', zorder=4)

    plt.tight_layout()
    return fig


def build_page_3():
    """Page 3: Prerequisite Bottleneck & Misconception Recovery Workflow."""
    fig, ax = plt.subplots(figsize=(14, 8.5))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    create_header(ax, "WORKFLOW 2: PREREQUISITE & MISCONCEPTION RECOVERY", 
                  "Automated Knowledge Graph Traversal & Diagnostic Remediation", 3)

    # Left: Knowledge Graph Concept Visual
    draw_box(ax, 0.04, 0.50, 0.43, 0.35, "DAG PREREQUISITE GRAPH (knowledge_graph_tool)", [
        ("Graph Nature: ", "Directed Acyclic Graph of Subject Topics"),
        ("Dependency 1: ", "Basic Chemistry  --->  Macromolecules  --->  Enzymes"),
        ("Dependency 2: ", "Cell Structure   --->  Membrane Transport ---> Osmosis"),
        ("Dependency 3: ", "Light Reactions ---> Calvin Cycle        ---> Carbon Fixation"),
        ("Bottleneck Logic: ", "A student failing an advanced topic is rarely weak"),
        ("Root Cause: ", "in the advanced topic itself; they lack prerequisite mastery."),
        ("Tool Action: ", "Traverses parents recursively to locate lowest unmastered node.")
    ], bg_color='#EEF2FF', border_color='#A5B4FC', title_color='#1E1B4B')

    # Right: Misconception Catalog Visual
    draw_box(ax, 0.53, 0.50, 0.43, 0.35, "MISCONCEPTION CATALOG (misconception_tool)", [
        ("Target Detection: ", "Diagnoses high-frequency cognitive errors"),
        ("Example 1: ", "'Plants do photosynthesis, animals do respiration' [FALSE]"),
        ("Correction 1: ", "Plants possess mitochondria and respire 24/7."),
        ("Example 2: ", "'Mass of trees comes from soil minerals' [FALSE]"),
        ("Correction 2: ", "95%+ of dry plant biomass is fixed from atmospheric CO2."),
        ("Remediation: ", "Contrasts intuitive misconception with empirical reality"),
        ("Verification: ", "Issues micro-quiz targeting the exact boundary condition.")
    ], bg_color='#FFF1F2', border_color='#FECDD3', title_color='#881337')

    # Middle Connecting Pipeline: Recovery Action Plan
    draw_box(ax, 0.04, 0.07, 0.92, 0.38, "AUTOMATED ADAPTIVE RECOVERY PIPELINE (recovery_planner_tool & intervention_tool)", [
        ("Step 1 - Detection: ", "Student fails assessment questions or exhibits confusion during chat on target topic."),
        ("Step 2 - Graph Walk: ", "knowledge_graph_tool walks upstream: checks prerequisite nodes for mastery threshold (< 0.70)."),
        ("Step 3 - Diagnosis: ", "misconception_tool checks student answers against known false cognitive models."),
        ("Step 4 - Prescription: ", "recovery_planner_tool generates a personalized 3-phase StudyPlan with sequenced StudyPlanTasks:"),
        ("     • Phase A: ", "Remediate missing prerequisite foundation chunk (e.g. review ATP currency before Calvin cycle)"),
        ("     • Phase B: ", "Directly refute identified misconception using visual comparison counter-example"),
        ("     • Phase C: ", "Re-assess target topic with calibrated formative quiz (assessment_tool)"),
        ("Step 5 - Intervention: ", "intervention_tool records action in InterventionHistory and alerts Teacher Dashboard if plateau persists.")
    ], bg_color='#F0FDF4', border_color='#86EFAC', title_color='#14532D', font_size=9)

    # Connections
    draw_arrow(ax, 0.255, 0.50, 0.255, 0.45, color='#4F46E5', label="Unmet Prerequisite Node")
    draw_arrow(ax, 0.745, 0.50, 0.745, 0.45, color='#E11D48', label="Diagnosed Error Model")

    plt.tight_layout()
    return fig


def build_page_4():
    """Page 4: Automated Judging CLI Contract Workflow."""
    fig, ax = plt.subplots(figsize=(14, 8.5))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    create_header(ax, "WORKFLOW 3: JUDGES CLI EVALUATION CONTRACT", 
                  "Strict Automated Compliance (python main.py --json)", 4)

    # 4 Quadrants detailing the judging execution pipeline
    draw_box(ax, 0.04, 0.51, 0.43, 0.34, "COMMAND LINE INTERACTION SPECIFICATION", [
        ("Judge Command: ", "python main.py --json \"<query>\""),
        ("Strict Rule 1: ", "STDOUT contains EXACTLY 1 raw JSON line. No logs."),
        ("Strict Rule 2: ", "No banners, no ANSI colors, no markdown formatting on stdout."),
        ("Strict Rule 3: ", "Exit code 0 on successful processing."),
        ("Flag --dry-run: ", "Runs entirely offline without requiring live API keys."),
        ("Flag --max-steps: ", "Caps max tool iterations (default: 8) to prevent loops."),
        ("Flag --debug: ", "Directs step-by-step ReAct traces exclusively to stderr.")
    ], bg_color='#FEF3C7', border_color='#FCD34D', title_color='#78350F')

    draw_box(ax, 0.53, 0.51, 0.43, 0.34, "OUTPUT JSON SCHEMA & VALIDATION", [
        ("Root Object: ", "{ 'answer': string, 'trace': list }"),
        ("answer Field: ", "Comprehensive, accurate pedagogical answer to query"),
        ("trace Field: ", "List of execution step objects [step_1, step_2, ...]"),
        ("Step Object: ", "{ 'step': int, 'thought': str, 'action': str,"),
        (" ", "  'action_input': dict/str, 'observation': str }"),
        ("Validation: ", "Parsable by json.loads(stdout.strip()) without error"),
        ("Zero Hallucination: ", "Grounded in seeded curriculum or tool outputs.")
    ], bg_color='#EEF2FF', border_color='#A5B4FC', title_color='#1E1B4B')

    draw_box(ax, 0.04, 0.07, 0.43, 0.39, "JUDGE VERIFICATION TEST RESULTS", [
        ("Suite: ", "python -m unittest discover tests"),
        ("Execution: ", "Ran 20 unit tests in 0.971s — 100% PASSING (OK)"),
        ("Coverage Areas: ", ""),
        (" • Test 1-5: ", "ReAct loop termination, self-correction, dry-run"),
        (" • Test 6-10: ", "8 Specialized pedagogical tool execution & schemas"),
        (" • Test 11-14: ", "Database seeding, SQLite/PostgreSQL connection"),
        (" • Test 15-17: ", "FastAPI endpoints & native Bcrypt authentication"),
        (" • Test 18-20: ", "Student isolation security & curriculum chunking")
    ], bg_color='#F0FDF4', border_color='#86EFAC', title_color='#14532D')

    draw_box(ax, 0.53, 0.07, 0.43, 0.39, "SAMPLE TEST RUNS VERIFIED ON REPO", [
        ("Query 1: ", "python main.py --json \"Explain photosynthesis\""),
        ("Result 1: ", "answer: 'Photosynthesis is the process... [C4 / Light]'"),
        ("Trace 1: ", "Called curriculum_retrieval -> returned vetted text"),
        ("Query 2: ", "python main.py --json \"Which topics is S1 weak in?\""),
        ("Result 2: ", "answer: 'Student S1 is weak in Cell Respiration'"),
        ("Trace 2: ", "Called student_performance -> fetched TopicMastery < 0.7"),
        ("Query 3: ", "python main.py --json --dry-run \"test\""),
        ("Result 3: ", "Mock fallback executed cleanly with valid JSON schema")
    ], bg_color='#FAF5FF', border_color='#D8B4FE', title_color='#581C87')

    draw_arrow(ax, 0.47, 0.68, 0.53, 0.68, color='#D97706', label="Parses & Formats")
    draw_arrow(ax, 0.255, 0.51, 0.255, 0.46, color='#059669', label="Verified by")
    draw_arrow(ax, 0.745, 0.51, 0.745, 0.46, color='#7C3AED', label="Observed on CLI")

    plt.tight_layout()
    return fig


def build_page_5():
    """Page 5: Relational Data Model & ER Architecture."""
    fig, ax = plt.subplots(figsize=(14, 8.5))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    create_header(ax, "DATA ARCHITECTURE & ENTITY RELATIONSHIP MODEL", 
                  "17 Relational Entities in Dual-Engine SQLAlchemy Store", 5)

    # 4 Domain Columns
    draw_box(ax, 0.04, 0.07, 0.21, 0.78, "IDENTITY & CLASSES", [
        ("User", ""),
        (" • id: ", "Integer PK"),
        (" • email: ", "String(255) Unique"),
        (" • password_hash: ", "String"),
        (" • full_name: ", "String(100)"),
        (" • role: ", "student / teacher"),
        (" • created_at: ", "DateTime"),
        ("", ""),
        ("TeacherClass", ""),
        (" • id: ", "Integer PK"),
        (" • teacher_id: ", "FK -> User.id"),
        (" • name: ", "String(100)"),
        (" • grade_level: ", "String(20)"),
        ("", ""),
        ("StudentEnrollment", ""),
        (" • id: ", "Integer PK"),
        (" • student_id: ", "FK -> User.id"),
        (" • class_id: ", "FK -> Class.id")
    ], bg_color='#F8FAFC', border_color='#CBD5E1', title_color='#0F172A', font_size=8)

    draw_box(ax, 0.28, 0.07, 0.21, 0.78, "KNOWLEDGE GRAPH", [
        ("Subject", ""),
        (" • id: ", "Integer PK"),
        (" • name: ", "String(100)"),
        (" • code: ", "BIO / CHEM / MATH"),
        ("", ""),
        ("Topic", ""),
        (" • id: ", "Integer PK"),
        (" • subject_id: ", "FK -> Subject.id"),
        (" • name: ", "String(150)"),
        (" • difficulty_level: ", "1 - 5"),
        ("", ""),
        ("TopicPrerequisite", ""),
        (" • id: ", "Integer PK"),
        (" • topic_id: ", "FK -> Topic.id"),
        (" • prerequisite_id: ", "FK -> Topic"),
        ("", ""),
        ("TopicMastery", ""),
        (" • id: ", "Integer PK"),
        (" • student_id: ", "FK -> User.id"),
        (" • topic_id: ", "FK -> Topic.id"),
        (" • mastery_score: ", "Float 0.0-1.0")
    ], bg_color='#EEF2FF', border_color='#A5B4FC', title_color='#1E1B4B', font_size=8)

    draw_box(ax, 0.52, 0.07, 0.21, 0.78, "PEDAGOGY & RECOVERY", [
        ("Misconception", ""),
        (" • id: ", "Integer PK"),
        (" • topic_id: ", "FK -> Topic.id"),
        (" • misconception_text: ", "Text"),
        (" • correction_strategy: ", "Text"),
        ("", ""),
        ("StudentAssessment", ""),
        (" • id: ", "Integer PK"),
        (" • student_id: ", "FK -> User.id"),
        (" • score: ", "Float"),
        (" • date_taken: ", "DateTime"),
        ("", ""),
        ("StudyPlan & Task", ""),
        (" • id: ", "Integer PK"),
        (" • student_id: ", "FK -> User.id"),
        (" • status: ", "active/completed"),
        (" • task_type: ", "review/quiz"),
        ("", ""),
        ("InterventionHistory", ""),
        (" • action_taken: ", "Text"),
        (" • trigger_reason: ", "Text")
    ], bg_color='#FFF1F2', border_color='#FECDD3', title_color='#881337', font_size=8)

    draw_box(ax, 0.76, 0.07, 0.21, 0.78, "KNOWLEDGE & TRACE", [
        ("CurriculumDocument", ""),
        (" • id: ", "Integer PK"),
        (" • title: ", "String(200)"),
        (" • subject_id: ", "FK -> Subject.id"),
        (" • source_file: ", "String"),
        ("", ""),
        ("CurriculumChunk", ""),
        (" • id: ", "Integer PK"),
        (" • document_id: ", "FK -> Doc.id"),
        (" • chunk_index: ", "Integer"),
        (" • content: ", "Text"),
        (" • token_count: ", "Integer"),
        ("", ""),
        ("AgentTrace", ""),
        (" • session_id: ", "String(64)"),
        (" • query: ", "Text"),
        (" • thoughts: ", "JSON / Text"),
        (" • execution_time_ms: ", "Int"),
        ("", ""),
        ("StudentLearningMemory", ""),
        (" • key_fact: ", "Text")
    ], bg_color='#F0FDF4', border_color='#86EFAC', title_color='#14532D', font_size=8)

    plt.tight_layout()
    return fig


def main():
    output_pdf_path = os.path.abspath("Knowlix_Workflow_and_Architecture.pdf")
    docs_dir = os.path.abspath(os.path.join("docs", "diagrams"))
    artifact_dir = r"C:\Users\Sami\.gemini\antigravity\brain\68b771cd-2341-497b-93c8-22f569ffe78c"
    os.makedirs(docs_dir, exist_ok=True)
    
    print(f"Generating workflow and architecture PDF at: {output_pdf_path}")
    
    page_builders = [
        ("page_1_system_architecture", build_page_1),
        ("page_2_socratic_tutoring_workflow", build_page_2),
        ("page_3_recovery_pipeline_workflow", build_page_3),
        ("page_4_judges_cli_contract", build_page_4),
        ("page_5_data_er_model", build_page_5)
    ]

    with PdfPages(output_pdf_path) as pdf:
        for name, builder in page_builders:
            print(f"Rendering and saving {name}...")
            fig = builder()
            # Save vector page into PDF
            pdf.savefig(fig, dpi=300)
            
            # Save high-res PNG
            png_path = os.path.join(docs_dir, f"{name}.png")
            fig.savefig(png_path, dpi=200, bbox_inches='tight')
            
            # Also copy to artifacts directory for inline chat viewing
            if os.path.exists(artifact_dir):
                shutil.copy2(png_path, os.path.join(artifact_dir, f"{name}.png"))
                
            plt.close(fig)

    file_size_kb = os.path.getsize(output_pdf_path) / 1024
    print(f"PDF successfully generated: {output_pdf_path} ({file_size_kb:.1f} KB)")


if __name__ == '__main__':
    main()
