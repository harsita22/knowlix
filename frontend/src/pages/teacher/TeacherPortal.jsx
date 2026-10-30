import React, { useState, useEffect } from 'react';
import {
  LayoutDashboard, Users, BookOpen, AlertTriangle, Lightbulb,
  UploadCloud, FileText, CheckCircle2, Award, Sparkles, AlertCircle
} from 'lucide-react';
import MetricCard from '../../components/MetricCard';
import { api } from '../../api/client';

export default function TeacherPortal() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [dashboardData, setDashboardData] = useState(null);
  const [classes, setClasses] = useState([]);
  const [selectedClassId, setSelectedClassId] = useState(null);
  const [classStudents, setClassStudents] = useState([]);
  const [interventions, setInterventions] = useState([]);
  const [uploadTitle, setUploadTitle] = useState('');
  const [uploadSubject, setUploadSubject] = useState('CS');
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploadMessage, setUploadMessage] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    setLoading(true);
    try {
      const [dash, clsList, alerts] = await Promise.all([
        api.getTeacherDashboard(),
        api.getTeacherClasses(),
        api.getInterventions(),
      ]);
      setDashboardData(dash);
      setClasses(clsList);
      setInterventions(alerts);
      if (clsList.length > 0) {
        setSelectedClassId(clsList[0].id);
        const students = await api.getClassStudents(clsList[0].id);
        setClassStudents(students);
      }
    } catch (err) {
      console.error('Failed to load teacher portal data', err);
    } finally {
      setLoading(false);
    }
  };

  const handleSelectClass = async (classId) => {
    setSelectedClassId(classId);
    try {
      const students = await api.getClassStudents(classId);
      setClassStudents(students);
    } catch (err) {
      console.error('Load class students error', err);
    }
  };

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!selectedFile || !uploadTitle.trim()) return;

    const formData = new FormData();
    formData.append('title', uploadTitle);
    formData.append('subject_code', uploadSubject);
    formData.append('file', selectedFile);

    try {
      setUploadMessage('Processing document and generating semantic embeddings...');
      const res = await api.uploadCurriculum(formData);
      setUploadMessage(`Success! ${res.title} indexed.`);
      setUploadTitle('');
      setSelectedFile(null);
    } catch (err) {
      setUploadMessage(`Upload error: ${err.message}`);
    }
  };

  const navItems = [
    { id: 'dashboard', label: 'Teacher Dashboard', icon: LayoutDashboard },
    { id: 'classes', label: 'Class Management', icon: Users },
    { id: 'performance', label: 'Student Performance', icon: Award },
    { id: 'gaps', label: 'Learning Gaps', icon: AlertCircle },
    { id: 'misconceptions', label: 'Misconception Insights', icon: Lightbulb },
    { id: 'interventions', label: 'Interventions', icon: AlertTriangle },
    { id: 'assessments', label: 'Assessments', icon: BookOpen },
    { id: 'curriculum', label: 'Curriculum Upload', icon: UploadCloud },
    { id: 'reports', label: 'Reports', icon: FileText },
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
          Loading classroom analytics & pedagogical signals...
        </div>
      ) : (
        <>
          {/* TAB 1: TEACHER DASHBOARD */}
          {activeTab === 'dashboard' && dashboardData && (
            <div className="space-y-8">
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
                <MetricCard
                  title="Class Average"
                  value={`${dashboardData.class_average_mastery}%`}
                  subtitle="Across all assigned cohorts"
                  icon={Award}
                  color="emerald"
                />
                <MetricCard
                  title="Assigned Classes"
                  value={dashboardData.total_classes}
                  subtitle="Grade 10 & 11 cohorts"
                  icon={Users}
                  color="brand"
                />
                <MetricCard
                  title="Enrolled Students"
                  value={dashboardData.total_enrolled_students}
                  subtitle="Active learners tracked"
                  icon={BookOpen}
                  color="brand"
                />
                <MetricCard
                  title="Interventions Recommended"
                  value={dashboardData.pending_interventions_count}
                  subtitle="Evidence-based learning alerts"
                  icon={AlertTriangle}
                  color="amber"
                />
              </div>

              {/* Active Intervention Alert Banner */}
              {interventions.length > 0 && (
                <div className="bg-amber-50 border border-amber-200 rounded-xl p-6">
                  <div className="flex items-center justify-between mb-3">
                    <span className="text-xs uppercase font-bold text-amber-800 bg-amber-100 px-2.5 py-0.5 rounded flex items-center gap-1.5">
                      <AlertTriangle className="w-3.5 h-3.5 text-amber-700" />
                      Priority Pedagogical Intervention Recommended
                    </span>
                    <button
                      onClick={() => setActiveTab('interventions')}
                      className="text-xs font-semibold text-amber-800 hover:underline"
                    >
                      View All Alerts →
                    </button>
                  </div>
                  <h3 className="text-base font-bold text-slate-900">
                    Student {interventions[0].student_name} — {interventions[0].topic}
                  </h3>
                  <p className="text-xs text-slate-600 mt-1">
                    <strong>Trigger:</strong> {interventions[0].trigger_reason}
                  </p>
                  <p className="text-xs text-slate-700 mt-1">
                    <strong>Suggested Action:</strong> {interventions[0].recommendation}
                  </p>
                </div>
              )}

              {/* Class Overview Cards */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="bg-white p-6 rounded-xl border border-slate-200">
                  <h3 className="text-sm font-bold text-slate-900 uppercase tracking-wider mb-4">
                    Assigned Class Roster
                  </h3>
                  <div className="space-y-3">
                    {classes.map((c) => (
                      <div
                        key={c.id}
                        onClick={() => {
                          handleSelectClass(c.id);
                          setActiveTab('performance');
                        }}
                        className="p-4 rounded-lg border border-slate-200 hover:border-brand-500 hover:bg-slate-50 transition cursor-pointer flex items-center justify-between"
                      >
                        <div>
                          <div className="font-bold text-sm text-slate-900">{c.name}</div>
                          <div className="text-xs text-slate-500">{c.subject} • {c.grade_level}</div>
                        </div>
                        <span className="text-xs font-semibold px-2 py-1 bg-slate-100 rounded text-slate-700">
                          {c.student_count} Enrolled
                        </span>
                      </div>
                    ))}
                  </div>
                </div>

                <div className="bg-white p-6 rounded-xl border border-slate-200">
                  <h3 className="text-sm font-bold text-slate-900 uppercase tracking-wider mb-4">
                    Common Misconception Heatmap
                  </h3>
                  <div className="space-y-3">
                    {[
                      { topic: 'Recursion', count: '1 student', issue: 'Base-case return unwinding confused with loops' },
                      { topic: 'Quadratic Equations', count: '1 student', issue: 'Square-root distribution over linear terms' },
                    ].map((m, i) => (
                      <div key={i} className="p-3 bg-slate-50 rounded-lg text-xs space-y-1">
                        <div className="flex justify-between font-bold text-slate-800">
                          <span>{m.topic}</span>
                          <span className="text-rose-600">{m.count} affected</span>
                        </div>
                        <p className="text-slate-500">{m.issue}</p>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* TAB 2: CLASS MANAGEMENT */}
          {activeTab === 'classes' && (
            <div className="space-y-6">
              <div>
                <h2 className="text-lg font-bold text-slate-900">Class Management</h2>
                <p className="text-xs text-slate-500">Manage cohorts, curriculum mapping, and student rosters</p>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {classes.map((c) => (
                  <div key={c.id} className="bg-white p-6 rounded-xl border border-slate-200 space-y-4">
                    <div className="flex justify-between items-start">
                      <div>
                        <span className="text-xs uppercase font-bold text-brand-700 bg-brand-50 px-2 py-0.5 rounded">{c.subject}</span>
                        <h3 className="text-lg font-bold text-slate-900 mt-2">{c.name}</h3>
                      </div>
                      <span className="text-xs text-slate-500">{c.grade_level}</span>
                    </div>
                    <p className="text-xs text-slate-500">Currently enrolled: {c.student_count} student(s).</p>
                    <button
                      onClick={() => {
                        handleSelectClass(c.id);
                        setActiveTab('performance');
                      }}
                      className="w-full py-2 bg-slate-900 hover:bg-slate-800 text-white rounded-lg text-xs font-semibold transition"
                    >
                      View Student Roster & Performance
                    </button>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* TAB 3: STUDENT PERFORMANCE */}
          {activeTab === 'performance' && (
            <div className="space-y-6">
              <div className="flex items-center justify-between">
                <div>
                  <h2 className="text-lg font-bold text-slate-900">Student Performance Breakdown</h2>
                  <p className="text-xs text-slate-500">Individual student mastery scores, accuracy rates, and struggling areas</p>
                </div>
                <select
                  value={selectedClassId || ''}
                  onChange={(e) => handleSelectClass(Number(e.target.value))}
                  className="text-xs px-3 py-1.5 rounded-lg border border-slate-300 bg-white"
                >
                  {classes.map((c) => (
                    <option key={c.id} value={c.id}>{c.name}</option>
                  ))}
                </select>
              </div>

              <div className="bg-white rounded-xl border border-slate-200 overflow-hidden">
                <table className="w-full text-left text-xs">
                  <thead className="bg-slate-50 border-b border-slate-200 text-slate-500 uppercase font-semibold">
                    <tr>
                      <th className="px-6 py-3">Student Name</th>
                      <th className="px-6 py-3">Email</th>
                      <th className="px-6 py-3">Average Mastery</th>
                      <th className="px-6 py-3">Struggling Topics</th>
                      <th className="px-6 py-3">Intervention Status</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100">
                    {classStudents.map((s) => (
                      <tr key={s.id} className="hover:bg-slate-50/50">
                        <td className="px-6 py-4 font-bold text-slate-900">{s.name}</td>
                        <td className="px-6 py-4 text-slate-500">{s.email}</td>
                        <td className="px-6 py-4 font-semibold text-slate-800">{s.average_score}%</td>
                        <td className="px-6 py-4">
                          {s.struggling_topics.length > 0 ? (
                            <span className="text-rose-700 bg-rose-50 px-2 py-0.5 rounded font-semibold">
                              {s.struggling_topics.join(', ')}
                            </span>
                          ) : (
                            <span className="text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded font-semibold">
                              All on track
                            </span>
                          )}
                        </td>
                        <td className="px-6 py-4">
                          <span className={`px-2 py-0.5 rounded text-[11px] font-bold ${
                            s.status === 'Needs Attention' ? 'bg-amber-100 text-amber-800' : 'bg-emerald-100 text-emerald-800'
                          }`}>
                            {s.status}
                          </span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          {/* TAB 4: LEARNING GAPS */}
          {activeTab === 'gaps' && (
            <div className="space-y-6">
              <div>
                <h2 className="text-lg font-bold text-slate-900">Curriculum Learning Gaps</h2>
                <p className="text-xs text-slate-500">Prerequisite bottlenecks detected across the cohort</p>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="bg-white p-6 rounded-xl border border-slate-200 space-y-3">
                  <div className="flex justify-between items-center">
                    <span className="text-xs font-bold uppercase text-brand-700 bg-brand-50 px-2 py-0.5 rounded">Computer Science</span>
                    <span className="text-xs text-rose-600 font-bold">1 Student Struggling</span>
                  </div>
                  <h4 className="font-bold text-base text-slate-900">Recursion (Call Stack Unwinding)</h4>
                  <p className="text-xs text-slate-600">
                    Root cause: Student did not master Functions & Scope return frames before attempting recursive call tracing.
                  </p>
                  <div className="p-3 bg-slate-50 rounded text-xs text-slate-700">
                    <strong>Recommended Action:</strong> Assign Day 1 Prerequisite Review task in recovery planner.
                  </div>
                </div>

                <div className="bg-white p-6 rounded-xl border border-slate-200 space-y-3">
                  <div className="flex justify-between items-center">
                    <span className="text-xs font-bold uppercase text-brand-700 bg-brand-50 px-2 py-0.5 rounded">Mathematics</span>
                    <span className="text-xs text-rose-600 font-bold">1 Student Struggling</span>
                  </div>
                  <h4 className="font-bold text-base text-slate-900">Quadratic Equations (Factoring Trinomials)</h4>
                  <p className="text-xs text-slate-600">
                    Root cause: Direct square-root application attempted prior to completing linear term expansion.
                  </p>
                  <div className="p-3 bg-slate-50 rounded text-xs text-slate-700">
                    <strong>Recommended Action:</strong> Scaffold factoring steps with polynomial difference-of-squares drill.
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* TAB 5: MISCONCEPTION INSIGHTS */}
          {activeTab === 'misconceptions' && (
            <div className="space-y-6">
              <div>
                <h2 className="text-lg font-bold text-slate-900">Cognitive Misconception Analysis</h2>
                <p className="text-xs text-slate-500">Evidence vs. hypothesis classification for recurring error patterns</p>
              </div>

              <div className="space-y-4">
                {[
                  {
                    topic: 'Recursion',
                    misconception: 'Conflating recursive stack unwinding with iterative while-loop repetition.',
                    evidence: 'Quiz answers consistently omit return value accumulation; student wrote "it restarts from n=0".',
                    certainty: 'Confirmed (92% Confidence)',
                    strategy: 'Interactive call-stack diagram illustrating activation records popped in LIFO order.',
                  },
                  {
                    topic: 'Quadratic Equations',
                    misconception: 'Distributing square root over summation terms (sqrt(a + b) = sqrt(a) + sqrt(b)).',
                    evidence: 'Solved x^2 + 6x + 9 = 25 by taking sqrt(x^2) + sqrt(6x) + 3.',
                    certainty: 'Confirmed (88% Confidence)',
                    strategy: 'Review algebraic identities with geometric area tile representations.',
                  },
                ].map((item, idx) => (
                  <div key={idx} className="bg-white p-6 rounded-xl border border-slate-200 space-y-3">
                    <div className="flex justify-between items-center">
                      <span className="text-xs font-bold text-slate-400 uppercase">{item.topic}</span>
                      <span className="text-xs font-bold px-2 py-0.5 rounded bg-emerald-50 text-emerald-700">{item.certainty}</span>
                    </div>
                    <h4 className="font-bold text-base text-slate-900">{item.misconception}</h4>
                    <p className="text-xs text-slate-600"><strong>Evidence:</strong> {item.evidence}</p>
                    <div className="p-3 bg-brand-50/50 border border-brand-100 rounded text-xs text-brand-900">
                      <strong>Pedagogical Strategy:</strong> {item.strategy}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* TAB 6: INTERVENTION RECOMMENDATIONS */}
          {activeTab === 'interventions' && (
            <div className="space-y-6">
              <div>
                <h2 className="text-lg font-bold text-slate-900">Teacher Intervention Recommendations</h2>
                <p className="text-xs text-slate-500">
                  Respectful, evidence-based alerts with actionable scaffolding actions (avoids negative labeling)
                </p>
              </div>

              <div className="space-y-4">
                {interventions.map((ih) => (
                  <div key={ih.id} className="bg-white p-6 rounded-xl border border-slate-200 space-y-3">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-2">
                        <span className="w-2.5 h-2.5 rounded-full bg-amber-500"></span>
                        <h4 className="font-bold text-base text-slate-900">
                          {ih.student_name} — {ih.topic}
                        </h4>
                      </div>
                      <span className="text-xs uppercase font-bold text-amber-700 bg-amber-50 px-2 py-0.5 rounded">
                        {ih.severity} Alert
                      </span>
                    </div>

                    <div className="p-3 bg-slate-50 rounded text-xs space-y-1">
                      <strong className="text-slate-700">Identified Friction:</strong>
                      <p className="text-slate-600">{ih.trigger_reason}</p>
                    </div>

                    <div className="p-3 bg-emerald-50 rounded text-xs space-y-1 border border-emerald-100">
                      <strong className="text-emerald-800">Actionable Teacher Recommendation:</strong>
                      <p className="text-emerald-700">{ih.recommendation}</p>
                    </div>

                    <div className="flex justify-between items-center pt-2 text-xs text-slate-500">
                      <span>Status: <strong>{ih.action_taken}</strong></span>
                      <span className="text-[11px] text-slate-400">Logged: {ih.created_at}</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* TAB 7: ASSESSMENTS */}
          {activeTab === 'assessments' && (
            <div className="space-y-6">
              <div>
                <h2 className="text-lg font-bold text-slate-900">Assessment Management</h2>
                <p className="text-xs text-slate-500">Review class diagnostic assessments and question banks</p>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {[
                  { title: 'Recursion Diagnostic Assessment', subject: 'Computer Science', class: 'AP CS A', attempts: 5, passRate: '40%' },
                  { title: 'Quadratic Equations Mid-Module Test', subject: 'Mathematics', class: 'Grade 10 Math', attempts: 3, passRate: '67%' },
                ].map((a, i) => (
                  <div key={i} className="bg-white p-6 rounded-xl border border-slate-200 space-y-3">
                    <span className="text-xs uppercase font-bold text-brand-700 bg-brand-50 px-2 py-0.5 rounded">{a.subject}</span>
                    <h4 className="font-bold text-base text-slate-900 mt-1">{a.title}</h4>
                    <div className="text-xs text-slate-500 flex justify-between">
                      <span>Class: <strong>{a.class}</strong></span>
                      <span>Pass Rate: <strong>{a.passRate}</strong></span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* TAB 8: CURRICULUM UPLOAD */}
          {activeTab === 'curriculum' && (
            <div className="space-y-6 max-w-2xl">
              <div>
                <h2 className="text-lg font-bold text-slate-900">Curriculum Upload & RAG Grounding</h2>
                <p className="text-xs text-slate-500">
                  Upload PDF, DOCX, TXT, or CSV files to ground AI Tutor answers directly in official course materials
                </p>
              </div>

              <form onSubmit={handleUpload} className="bg-white p-6 rounded-xl border border-slate-200 space-y-4">
                <div>
                  <label className="block text-xs font-bold text-slate-700 uppercase mb-1">Document Title</label>
                  <input
                    type="text"
                    required
                    value={uploadTitle}
                    onChange={(e) => setUploadTitle(e.target.value)}
                    placeholder="e.g. AP Biology Chapter 8 Photosynthesis Standard"
                    className="w-full px-3 py-2 rounded-lg border border-slate-300 text-xs focus:ring-2 focus:ring-brand-500"
                  />
                </div>

                <div>
                  <label className="block text-xs font-bold text-slate-700 uppercase mb-1">Subject Code</label>
                  <select
                    value={uploadSubject}
                    onChange={(e) => setUploadSubject(e.target.value)}
                    className="w-full px-3 py-2 rounded-lg border border-slate-300 text-xs bg-white"
                  >
                    <option value="CS">CS — Computer Science</option>
                    <option value="MATH">MATH — Mathematics</option>
                    <option value="BIO">BIO — Biology</option>
                  </select>
                </div>

                <div>
                  <label className="block text-xs font-bold text-slate-700 uppercase mb-1">Select Document (PDF, TXT, CSV)</label>
                  <input
                    type="file"
                    required
                    onChange={(e) => setSelectedFile(e.target.files[0])}
                    className="w-full text-xs text-slate-500 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-xs file:font-semibold file:bg-brand-50 file:text-brand-700 hover:file:bg-brand-100 cursor-pointer"
                  />
                </div>

                {uploadMessage && (
                  <div className="p-3 bg-brand-50 text-brand-900 border border-brand-200 rounded-lg text-xs">
                    {uploadMessage}
                  </div>
                )}

                <button
                  type="submit"
                  disabled={!selectedFile || !uploadTitle.trim()}
                  className="w-full py-2.5 bg-brand-600 hover:bg-brand-700 disabled:opacity-50 text-white rounded-lg text-xs font-semibold transition"
                >
                  Upload & Index Curriculum
                </button>
              </form>
            </div>
          )}

          {/* TAB 9: REPORTS */}
          {activeTab === 'reports' && (
            <div className="space-y-6">
              <div>
                <h2 className="text-lg font-bold text-slate-900">Pedagogical Reports</h2>
                <p className="text-xs text-slate-500">Synthesized class summaries ready for parent-teacher conferences or interventions</p>
              </div>

              <div className="bg-white p-6 rounded-xl border border-slate-200 space-y-4">
                <div className="flex justify-between items-center pb-4 border-b border-slate-100">
                  <div>
                    <h4 className="font-bold text-sm text-slate-900">Mid-Term Diagnostic Cohort Summary</h4>
                    <p className="text-xs text-slate-500">AP Computer Science A & Grade 10 Mathematics</p>
                  </div>
                  <button
                    onClick={() => window.print()}
                    className="px-3 py-1.5 bg-slate-900 text-white text-xs font-semibold rounded-lg hover:bg-slate-800 transition"
                  >
                    Print / Save PDF
                  </button>
                </div>
                <div className="text-xs space-y-2 text-slate-700 leading-relaxed">
                  <p>• <strong>Cohort Average:</strong> 74.2% across 2 core subjects.</p>
                  <p>• <strong>Active Bottlenecks:</strong> Recursion Call Stack Frame Mechanics (1 student); Factoring quadratic trinomials before taking roots (1 student).</p>
                  <p>• <strong>Intervention Efficacy:</strong> 3-day recovery roadmaps currently assigned with prerequisite verification checkpoints.</p>
                </div>
              </div>
            </div>
          )}
        </>
      )}
    </div>
  );
}
