import React from 'react';
import {
  GraduationCap, Network, Bot, AlertOctagon, Calendar,
  ShieldCheck, ArrowRight, BookOpen, CheckCircle2, Award
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';

export default function LandingPage({ onExplore }) {
  const { quickLogin } = useAuth();

  const handleDemo = async (role) => {
    await quickLogin(role);
    if (onExplore) onExplore();
  };

  const capabilities = [
    {
      title: 'Performance Analyst',
      desc: 'Tracks topic-wise mastery, historical accuracy, learning progress, and consistency signals across assessments.',
      icon: Award,
    },
    {
      title: 'Knowledge Graph Detective',
      desc: 'Maps prerequisite hierarchies to diagnose foundational gaps whenever a student struggles with advanced concepts.',
      icon: Network,
    },
    {
      title: 'Misconception Detective',
      desc: 'Isolates cognitive error patterns and provides confidence-rated hypotheses with verified evidence.',
      icon: AlertOctagon,
    },
    {
      title: 'Curriculum-Grounded RAG',
      desc: 'Retrieves verified textbook standards and official syllabi with exact source citations, preventing hallucinations.',
      icon: BookOpen,
    },
    {
      title: 'Adaptive Pedagogical Tutor',
      desc: 'Calibrates explanations to student needs through analogies, step-by-step logic, Socratic questioning, or practice drills.',
      icon: Bot,
    },
    {
      title: 'Personalized Recovery Planner',
      desc: 'Synthesizes prerequisite-ordered study roadmaps with estimated hours, daily tasks, and milestone checkpoints.',
      icon: Calendar,
    },
  ];

  return (
    <div className="bg-slate-50 min-h-screen text-slate-800">
      {/* Hero Section */}
      <section className="py-20 border-b border-slate-200 bg-white">
        <div className="max-w-5xl mx-auto px-6 text-center space-y-6">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-slate-100 border border-slate-200 text-xs font-semibold text-slate-700">
            <ShieldCheck className="w-4 h-4 text-brand-600" />
            <span>AgentX 2026 Core Foundation • Coordinated Multi-Agent ReAct Engine</span>
          </div>

          <h1 className="text-4xl sm:text-5xl lg:text-6xl font-extrabold text-slate-900 tracking-tight">
            AI-Powered Adaptive Learning & Personalized Pedagogy
          </h1>

          <p className="text-lg text-slate-600 max-w-2xl mx-auto" style={{ lineHeight: 1.55 }}>
            Knowlix moves beyond conversational chatbots into an autonomous pedagogical intelligence.
            It diagnoses underlying concept gaps, detects cognitive misconceptions, and builds actionable recovery roadmaps.
          </p>

          <div className="pt-4 flex flex-wrap items-center justify-center gap-4">
            <button
              onClick={() => handleDemo('student')}
              className="px-6 py-3 bg-brand-600 hover:bg-brand-700 text-white rounded-lg text-sm font-bold flex items-center gap-2 shadow-xs transition"
            >
              <span>Launch Student Portal</span>
              <ArrowRight className="w-4 h-4" />
            </button>
            <button
              onClick={() => handleDemo('teacher')}
              className="px-6 py-3 bg-slate-900 hover:bg-slate-800 text-white rounded-lg text-sm font-bold flex items-center gap-2 transition"
            >
              <span>Launch Teacher Portal</span>
              <ArrowRight className="w-4 h-4" />
            </button>
          </div>

          <div className="pt-6 flex items-center justify-center gap-6 text-xs text-slate-500">
            <span className="flex items-center gap-1.5">
              <CheckCircle2 className="w-4 h-4 text-emerald-600" /> PostgreSQL & SQLAlchemy
            </span>
            <span className="flex items-center gap-1.5">
              <CheckCircle2 className="w-4 h-4 text-emerald-600" /> Google Gemini Sole AI
            </span>
            <span className="flex items-center gap-1.5">
              <CheckCircle2 className="w-4 h-4 text-emerald-600" /> Judges' CLI Preserved
            </span>
          </div>
        </div>
      </section>

      {/* Core Architectural Capabilities */}
      <section className="py-20 max-w-6xl mx-auto px-6">
        <div className="text-center space-y-2 mb-12">
          <span className="text-xs uppercase font-bold text-brand-600 tracking-wider">Modular Architecture</span>
          <h2 className="text-3xl font-bold text-slate-900">Coordinated Agentic Capabilities</h2>
          <p className="text-sm text-slate-600 max-w-xl mx-auto" style={{ lineHeight: 1.55 }}>
            Coordinated through a central ReAct reasoning loop with structured tools, bounded iteration caps, and repeat guards.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {capabilities.map((cap, i) => {
            const Icon = cap.icon;
            return (
              <div key={i} className="bg-white p-6 rounded-xl border border-slate-200 shadow-xs flex flex-col justify-between">
                <div>
                  <div className="w-10 h-10 rounded-lg bg-brand-50 border border-brand-200 text-brand-600 flex items-center justify-center mb-4">
                    <Icon className="w-5 h-5" />
                  </div>
                  <h3 className="text-base font-bold text-slate-900">{cap.title}</h3>
                  <p className="text-xs text-slate-600 mt-2" style={{ lineHeight: 1.55 }}>
                    {cap.desc}
                  </p>
                </div>
              </div>
            );
          })}
        </div>
      </section>

      {/* Judging Contract Verification Callout */}
      <section className="py-16 bg-white border-t border-slate-200">
        <div className="max-w-4xl mx-auto px-6 space-y-4">
          <div className="text-xs font-bold text-slate-400 uppercase tracking-wider">Standardized Judging Harness</div>
          <h3 className="text-2xl font-bold text-slate-900">100% Contract Compliance</h3>
          <p className="text-sm text-slate-600" style={{ lineHeight: 1.55 }}>
            Automated test harnesses run <code className="bg-slate-100 text-slate-800 px-1.5 py-0.5 rounded font-mono text-xs">python main.py --json "&lt;query&gt;"</code>.
            Knowlix preserves stdout purity, emits valid single-line JSON with <code className="text-xs font-mono font-bold">answer</code> and <code className="text-xs font-mono font-bold">trace</code>, and routes all diagnostics to stderr.
          </p>
          <div className="p-4 bg-slate-900 text-slate-200 rounded-lg font-mono text-xs overflow-x-auto">
            $ python main.py --json "Which topics is student S1 weak in?"<br />
            {`{"answer": "Student S1 is weak in Recursion (31%) and Quadratic Equations (45%)...", "trace": [...]}`}
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-8 border-t border-slate-200 text-center text-xs text-slate-500">
        <div className="max-w-7xl mx-auto px-6 flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-2">
            <GraduationCap className="w-4 h-4 text-brand-600" />
            <span className="font-bold text-slate-800">Knowlix</span>
            <span>— AI-Powered Adaptive Learning & Personalized Pedagogy</span>
          </div>
          <div>Built for AgentX Challenge 2026 • Local Development Verified</div>
        </div>
      </footer>
    </div>
  );
}
