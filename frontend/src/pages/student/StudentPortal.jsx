import React, { useState, useEffect } from 'react';
import {
  LayoutDashboard, BookOpen, Network, Bot, AlertOctagon, Calendar,
  Award, TrendingUp, FolderGit2, CheckCircle2, Clock, Sparkles
} from 'lucide-react';
import MetricCard from '../../components/MetricCard';
import KnowledgeGraphViewer from '../../components/KnowledgeGraphViewer';
import ChatTutor from '../../components/ChatTutor';
import { api } from '../../api/client';

export default function StudentPortal() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [dashboardData, setDashboardData] = useState(null);
  const [graphData, setGraphData] = useState(null);
  const [misconceptions, setMisconceptions] = useState([]);
  const [studyPlans, setStudyPlans] = useState([]);
  const [selectedSubject, setSelectedSubject] = useState('Computer Science');
  const [tutorDefaultTopic, setTutorDefaultTopic] = useState('Recursion');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadData();
  }, [selectedSubject]);

  const loadData = async () => {
    setLoading(true);
    try {
      const [dash, graph, misc, plans] = await Promise.all([
        api.getStudentDashboard(),
        api.getKnowledgeGraph(selectedSubject),
        api.getStudentMisconceptions(),
        api.getStudyPlans(),
      ]);
      setDashboardData(dash);
      setGraphData(graph);
      setMisconceptions(misc);
      setStudyPlans(plans);
    } catch (err) {
      console.error('Failed to load student portal data', err);
    } finally {
      setLoading(false);
    }
  };

  const handleToggleTask = async (taskId) => {
    try {
      await api.toggleStudyTask(taskId);
      const plans = await api.getStudyPlans();
      setStudyPlans(plans);
    } catch (err) {
      console.error('Toggle task error', err);
    }
  };

  const navItems = [
    { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { id: 'subjects', label: 'My Subjects', icon: BookOpen },
    { id: 'knowledge_graph', label: 'Knowledge Graph', icon: Network },
    { id: 'tutor', label: 'AI Tutor', icon: Bot },
    { id: 'mistakes', label: 'My Mistakes', icon: AlertOctagon },
    { id: 'study_planner', label: 'Study Planner', icon: Calendar },
    { id: 'assessments', label: 'Practice & Quizzes', icon: Award },
    { id: 'progress', label: 'Progress Tracking', icon: TrendingUp },
    { id: 'resources', label: 'Learning Resources', icon: FolderGit2 },
  ];

  return (
    <div className="max-w-7xl mx-auto px-6 py-8">
      {/* Navigation Sub-bar */}
      <div className="flex items-center gap-1 overflow-x-auto pb-4 mb-6 border-b border-slate-200">
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = activeTab === item.id;
          return (
            <button
              key={item.id}
              onClick={() => setActiveTab(item.id)}
              className={`flex items-center gap-2 px-4 py-2 rounded-lg text-xs font-semibold whitespace-nowrap transition ${
                isActive
                  ? 'bg-slate-900 text-white shadow-xs'
                  : 'text-slate-600 hover:bg-slate-100'
              }`}
            >
              <Icon className="w-4 h-4" />
              <span>{item.label}</span>
            </button>
          );
        })}
      </div>

      {loading ? (
        <div className="py-20 text-center text-slate-400 text-sm">
          <Sparkles className="w-6 h-6 animate-spin mx-auto text-brand-600 mb-2" />
          Loading student learning records...
        </div>
      ) : (
        <>
          {/* TAB 1: DASHBOARD */}
          {activeTab === 'dashboard' && dashboardData && (
            <div className="space-y-8">
              {/* Top Metrics Row */}
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
                <MetricCard
                  title="Overall Mastery"
                  value={`${dashboardData.overall_mastery}%`}
                  subtitle="Across all enrolled subjects"
                  icon={TrendingUp}
                  color={dashboardData.overall_mastery >= 75 ? 'emerald' : 'amber'}
                />
                <MetricCard
                  title="Concepts in Progress"
                  value={dashboardData.topics_in_progress}
                  subtitle="Active learning modules"
                  icon={BookOpen}
                  color="brand"
                />
                <MetricCard
                  title="Weak Concepts"
                  value={dashboardData.weak_topics.length}
                  subtitle="Requires prerequisite review"
                  icon={AlertOctagon}
                  color="rose"
                />
                <MetricCard
                  title="Study Hours"
                  value={`${dashboardData.total_study_hours} hrs`}
                  subtitle="Consistent weekly effort"
                  icon={Clock}
                  color="emerald"
                />
              </div>

              {/* Recovery Plan Spotlight */}
              {dashboardData.active_recovery_plan && (
                <div className="bg-amber-50 border border-amber-200 rounded-xl p-6 flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
                  <div>
                    <span className="text-xs uppercase font-bold text-amber-800 bg-amber-100 px-2.5 py-0.5 rounded">
                      Active Recovery Roadmap
                    </span>
                    <h3 className="text-lg font-bold text-slate-900 mt-2">
                      {dashboardData.active_recovery_plan.title}
                    </h3>
                    <p className="text-xs text-slate-600 mt-1">
                      {dashboardData.active_recovery_plan.completed_tasks} of {dashboardData.active_recovery_plan.tasks_count} tasks completed ({dashboardData.active_recovery_plan.total_estimated_hours} hrs total).
                    </p>
                  </div>
                  <button
                    onClick={() => setActiveTab('study_planner')}
                    className="px-4 py-2 bg-amber-700 hover:bg-amber-800 text-white rounded-lg text-xs font-semibold whitespace-nowrap transition"
                  >
                    Continue Study Plan
                  </button>
                </div>
              )}

              {/* Weak vs Strong Grid */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {/* Weak Concepts Card */}
                <div className="bg-white rounded-xl border border-slate-200 p-6">
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="text-sm font-bold text-slate-900 uppercase tracking-wider flex items-center gap-2">
                      <span className="w-2.5 h-2.5 rounded-full bg-rose-500"></span>
                      Attention Areas ({dashboardData.weak_topics.length})
                    </h3>
                    <span className="text-xs text-slate-500">&lt;60% Mastery</span>
                  </div>
                  <div className="space-y-3">
                    {dashboardData.weak_topics.map((t) => (
                      <div key={t.topic_id} className="p-3 bg-rose-50/50 border border-rose-100 rounded-lg flex items-center justify-between">
                        <div>
                          <div className="font-bold text-sm text-slate-800">{t.topic_name}</div>
                          <div className="text-xs text-slate-500">{t.subject} • {t.chapter}</div>
                        </div>
                        <div className="flex items-center gap-3">
                          <span className="text-xs font-bold text-rose-700">{t.score}%</span>
                          <button
                            onClick={() => {
                              setTutorDefaultTopic(t.topic_name);
                              setActiveTab('tutor');
                            }}
                            className="text-xs text-brand-600 hover:underline font-semibold"
                          >
                            Review
                          </button>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Strong Concepts Card */}
                <div className="bg-white rounded-xl border border-slate-200 p-6">
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="text-sm font-bold text-slate-900 uppercase tracking-wider flex items-center gap-2">
                      <span className="w-2.5 h-2.5 rounded-full bg-emerald-500"></span>
                      Mastered Concepts ({dashboardData.strong_topics.length})
                    </h3>
                    <span className="text-xs text-slate-500">≥75% Mastery</span>
                  </div>
                  <div className="space-y-3">
                    {dashboardData.strong_topics.map((t) => (
                      <div key={t.topic_id} className="p-3 bg-emerald-50/50 border border-emerald-100 rounded-lg flex items-center justify-between">
                        <div>
                          <div className="font-bold text-sm text-slate-800">{t.topic_name}</div>
                          <div className="text-xs text-slate-500">{t.subject} • {t.chapter}</div>
                        </div>
                        <span className="text-xs font-bold text-emerald-700">{t.score}%</span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* TAB 2: MY SUBJECTS */}
          {activeTab === 'subjects' && (
            <div className="space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                {[
                  { code: 'CS', name: 'Computer Science', count: '6 Topics', desc: 'Call stacks, recursion mechanics, and algorithmic sorting.' },
                  { code: 'MATH', name: 'Mathematics', count: '4 Topics', desc: 'Algebraic factoring, linear systems, and quadratic equations.' },
                  { code: 'BIO', name: 'Biology', count: '2 Topics', desc: 'Cell organelles, bioenergetics, and photosynthetic pathways.' },
                ].map((s) => (
                  <div
                    key={s.code}
                    onClick={() => {
                      setSelectedSubject(s.name);
                      setActiveTab('knowledge_graph');
                    }}
                    className="bg-white p-6 rounded-xl border border-slate-200 hover:border-brand-500 hover:shadow-xs transition cursor-pointer"
                  >
                    <span className="text-xs font-bold px-2 py-0.5 rounded bg-brand-50 text-brand-700 uppercase">{s.code}</span>
                    <h3 className="text-lg font-bold text-slate-900 mt-2">{s.name}</h3>
                    <p className="text-xs text-slate-500 mt-1">{s.desc}</p>
                    <div className="mt-4 pt-4 border-t border-slate-100 flex justify-between text-xs font-semibold text-slate-600">
                      <span>{s.count}</span>
                      <span className="text-brand-600">View Graph →</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* TAB 3: KNOWLEDGE GRAPH */}
          {activeTab === 'knowledge_graph' && (
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <div>
                  <h2 className="text-lg font-bold text-slate-900">Interactive Concept Dependency Graph</h2>
                  <p className="text-xs text-slate-500">Prerequisite relationships and mastery level for each concept</p>
                </div>
                <div className="flex gap-2 text-xs">
                  {['Computer Science', 'Mathematics', 'Biology'].map((subj) => (
                    <button
                      key={subj}
                      onClick={() => setSelectedSubject(subj)}
                      className={`px-3 py-1.5 rounded-lg font-medium transition ${
                        selectedSubject === subj ? 'bg-slate-900 text-white' : 'bg-white border border-slate-200 text-slate-600 hover:bg-slate-50'
                      }`}
                    >
                      {subj}
                    </button>
                  ))}
                </div>
              </div>
              <KnowledgeGraphViewer
                graphData={graphData}
                onSelectTopic={(topicName) => {
                  setTutorDefaultTopic(topicName);
                  setActiveTab('tutor');
                }}
              />
            </div>
          )}

          {/* TAB 4: AI TUTOR */}
          {activeTab === 'tutor' && (
            <div className="space-y-4">
              <div>
                <h2 className="text-lg font-bold text-slate-900">Adaptive AI Tutor</h2>
                <p className="text-xs text-slate-500">
                  Step-by-step Socratic guidance grounded in your official curriculum standards
                </p>
              </div>
              <ChatTutor defaultTopic={tutorDefaultTopic} />
            </div>
          )}

          {/* TAB 5: MY MISTAKES (MISCONCEPTIONS) */}
          {activeTab === 'mistakes' && (
            <div className="space-y-6">
              <div>
                <h2 className="text-lg font-bold text-slate-900">Detected Learning Misconceptions</h2>
                <p className="text-xs text-slate-500">
                  Evidence-based cognitive error patterns analyzed from quizzes and problem-solving attempts
                </p>
              </div>

              <div className="grid grid-cols-1 gap-4">
                {misconceptions.map((m) => (
                  <div key={m.id} className="bg-white rounded-xl border border-slate-200 p-6 space-y-3">
                    <div className="flex items-start justify-between gap-4">
                      <div>
                        <div className="text-xs font-bold text-slate-400 uppercase">{m.subject} • {m.topic}</div>
                        <h4 className="text-base font-bold text-slate-900 mt-1">{m.description}</h4>
                      </div>
                      <span className="text-xs font-semibold px-2.5 py-1 rounded bg-rose-50 text-rose-700 border border-rose-200">
                        {Math.round(m.confidence_score * 100)}% Confidence
                      </span>
                    </div>

                    <div className="p-3 bg-slate-50 rounded-lg text-xs space-y-1">
                      <span className="font-bold text-slate-700">Observed Evidence:</span>
                      <p className="text-slate-600">{m.evidence}</p>
                    </div>

                    <div className="p-3 bg-emerald-50 rounded-lg text-xs space-y-1 border border-emerald-100">
                      <span className="font-bold text-emerald-800">Pedagogical Correction Strategy:</span>
                      <p className="text-emerald-700">{m.suggested_correction}</p>
                    </div>

                    <div className="flex justify-end pt-2">
                      <button
                        onClick={() => {
                          setTutorDefaultTopic(m.topic);
                          setActiveTab('tutor');
                        }}
                        className="text-xs font-semibold text-brand-600 hover:text-brand-700 flex items-center gap-1"
                      >
                        Practice with AI Tutor →
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* TAB 6: STUDY PLANNER */}
          {activeTab === 'study_planner' && (
            <div className="space-y-6">
              <div>
                <h2 className="text-lg font-bold text-slate-900">Personalized Recovery Roadmaps</h2>
                <p className="text-xs text-slate-500">
                  Prerequisite-first daily schedule synthesized from your assessment diagnostic gaps
                </p>
              </div>

              {studyPlans.map((p) => (
                <div key={p.id} className="bg-white rounded-xl border border-slate-200 p-6 space-y-6">
                  <div className="flex items-center justify-between pb-4 border-b border-slate-100">
                    <div>
                      <span className="text-xs uppercase font-bold text-brand-700 bg-brand-50 px-2 py-0.5 rounded">
                        Active Plan
                      </span>
                      <h3 className="text-lg font-bold text-slate-900 mt-1">{p.title}</h3>
                    </div>
                    <div className="text-right">
                      <div className="text-xs text-slate-400">Estimated Effort</div>
                      <div className="text-sm font-bold text-slate-800">{p.total_estimated_hours} Hours</div>
                    </div>
                  </div>

                  <div className="space-y-3">
                    {p.tasks.map((task) => (
                      <div
                        key={task.id}
                        onClick={() => handleToggleTask(task.id)}
                        className={`p-4 rounded-lg border flex items-center justify-between gap-4 cursor-pointer transition ${
                          task.is_completed ? 'bg-slate-50 border-slate-200 opacity-60' : 'bg-white border-slate-200 hover:border-brand-500'
                        }`}
                      >
                        <div className="flex items-center gap-3">
                          <CheckCircle2 className={`w-5 h-5 ${task.is_completed ? 'text-emerald-600' : 'text-slate-300'}`} />
                          <div>
                            <span className="text-[10px] font-bold uppercase tracking-wider text-slate-400">Day {task.day} • {task.type}</span>
                            <div className={`text-sm font-semibold ${task.is_completed ? 'line-through text-slate-500' : 'text-slate-900'}`}>
                              {task.description}
                            </div>
                          </div>
                        </div>
                        <span className="text-xs text-slate-400 font-medium whitespace-nowrap">{task.duration_minutes}m</span>
                      </div>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          )}

          {/* TAB 7: PRACTICE & ASSESSMENTS */}
          {activeTab === 'assessments' && (
            <div className="space-y-6">
              <div>
                <h2 className="text-lg font-bold text-slate-900">Diagnostic Practice Checkpoints</h2>
                <p className="text-xs text-slate-500">Formative micro-quizzes to verify mastery resolution</p>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {[
                  { title: 'Recursion Call Stack Diagnostic', topic: 'Recursion', questions: 5, difficulty: 'Intermediate', lastScore: '31%' },
                  { title: 'Quadratic Factoring Assessment', topic: 'Quadratic Equations', questions: 4, difficulty: 'Intermediate', lastScore: '45%' },
                  { title: 'Photosynthesis Stages Verification', topic: 'Photosynthesis', questions: 5, difficulty: 'Beginner', lastScore: 'Unattempted' },
                ].map((q, idx) => (
                  <div key={idx} className="bg-white p-6 rounded-xl border border-slate-200 space-y-4">
                    <div className="flex items-start justify-between">
                      <div>
                        <span className="text-xs font-semibold text-slate-400 uppercase">{q.topic}</span>
                        <h4 className="font-bold text-slate-900 text-base mt-1">{q.title}</h4>
                      </div>
                      <span className="text-xs font-bold px-2 py-0.5 rounded bg-slate-100 text-slate-700">{q.difficulty}</span>
                    </div>
                    <div className="text-xs text-slate-500 flex justify-between">
                      <span>{q.questions} Questions</span>
                      <span>Prior Score: <strong>{q.lastScore}</strong></span>
                    </div>
                    <button
                      onClick={() => {
                        setTutorDefaultTopic(q.topic);
                        setActiveTab('tutor');
                      }}
                      className="w-full py-2 bg-slate-900 hover:bg-slate-800 text-white rounded-lg text-xs font-semibold transition"
                    >
                      Start Diagnostic Checkpoint
                    </button>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* TAB 8: PROGRESS TRACKING */}
          {activeTab === 'progress' && (
            <div className="space-y-6">
              <div>
                <h2 className="text-lg font-bold text-slate-900">Longitudinal Learning Progress</h2>
                <p className="text-xs text-slate-500">Tracking accuracy, attempt trends, and mastery growth over time</p>
              </div>

              <div className="bg-white p-6 rounded-xl border border-slate-200 space-y-4">
                <h4 className="text-sm font-bold text-slate-800 uppercase tracking-wider">Concept Growth Curve</h4>
                <div className="h-48 flex items-end gap-6 pt-8 pb-2 border-b border-slate-200">
                  {[
                    { label: 'Week 1', score: 42 },
                    { label: 'Week 2', score: 55 },
                    { label: 'Week 3', score: 61 },
                    { label: 'Week 4', score: 68 },
                    { label: 'Current', score: 74 },
                  ].map((bar, i) => (
                    <div key={i} className="flex-1 flex flex-col items-center gap-2">
                      <span className="text-xs font-bold text-brand-600">{bar.score}%</span>
                      <div
                        className="w-full bg-brand-500 rounded-t-md transition-all duration-500"
                        style={{ height: `${bar.score * 1.5}px` }}
                      ></div>
                      <span className="text-xs text-slate-500">{bar.label}</span>
                    </div>
                  ))}
                </div>
                <p className="text-xs text-slate-500">Consistent upward trajectory (+32% mastery over 4 weeks).</p>
              </div>
            </div>
          )}

          {/* TAB 9: LEARNING RESOURCES */}
          {activeTab === 'resources' && (
            <div className="space-y-6">
              <div>
                <h2 className="text-lg font-bold text-slate-900">Curriculum Guides & Reference Sheets</h2>
                <p className="text-xs text-slate-500">Official textbook excerpts and verified learning resources</p>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {[
                  { title: 'AP CS: Call Stack & Recursion Guide', file: 'cs_recursion.txt', size: '1.2 KB', desc: 'Base cases, activation frames, and stack overflow mechanics.' },
                  { title: 'Biology: Cellular Energy & Photosynthesis', file: 'biology_photosynthesis.txt', size: '1.4 KB', desc: 'Thylakoids, Calvin cycle formulas, and ATP/NADPH reactions.' },
                  { title: 'Algebra: Factoring Polynomials Quick Reference', file: 'math_algebra.txt', size: '1.8 KB', desc: 'Trinomial factoring techniques and quadratic formula rules.' },
                ].map((res, i) => (
                  <div key={i} className="bg-white p-5 rounded-xl border border-slate-200 flex items-start justify-between gap-4">
                    <div>
                      <h4 className="font-bold text-sm text-slate-900">{res.title}</h4>
                      <p className="text-xs text-slate-500 mt-1">{res.desc}</p>
                      <span className="text-[11px] text-slate-400 mt-2 block font-mono">{res.file} • {res.size}</span>
                    </div>
                    <button
                      onClick={() => {
                        setTutorDefaultTopic(res.title);
                        setActiveTab('tutor');
                      }}
                      className="text-xs font-semibold text-brand-600 hover:underline whitespace-nowrap"
                    >
                      Read in Tutor
                    </button>
                  </div>
                ))}
              </div>
            </div>
          )}
        </>
      )}
    </div>
  );
}
