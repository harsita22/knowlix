import React from 'react';
import { GraduationCap, LogOut, ArrowLeftRight, User } from 'lucide-react';
import { useAuth } from '../context/AuthContext';

export default function Navbar({ onNavigate, currentTab }) {
  const { user, role, logout, quickLogin } = useAuth();

  return (
    <header className="bg-white border-b border-slate-200 sticky top-0 z-30">
      <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
        <div
          className="flex items-center gap-3 cursor-pointer"
          onClick={() => onNavigate && onNavigate('home')}
        >
          <div className="w-10 h-10 rounded-xl bg-brand-600 flex items-center justify-center text-white shadow-xs">
            <GraduationCap className="w-6 h-6" />
          </div>
          <div>
            <span className="text-lg font-bold text-slate-900 tracking-tight">Knowlix</span>
            <span className="hidden sm:inline-block ml-2 text-xs bg-slate-100 text-slate-600 px-2 py-0.5 rounded font-medium">
              AI Adaptive Learning
            </span>
          </div>
        </div>

        <div className="flex items-center gap-3">
          {user ? (
            <>
              {/* Role Switcher */}
              <button
                onClick={() => quickLogin(role === 'student' ? 'teacher' : 'student')}
                className="text-xs font-semibold px-3 py-1.5 rounded-lg border border-slate-300 hover:bg-slate-50 text-slate-700 flex items-center gap-1.5 transition"
                title={`Switch to ${role === 'student' ? 'Teacher' : 'Student'} profile`}
              >
                <ArrowLeftRight className="w-3.5 h-3.5 text-brand-600" />
                <span>Switch to {role === 'student' ? 'Teacher' : 'Student'}</span>
              </button>

              <div className="h-6 w-px bg-slate-200"></div>

              <div className="flex items-center gap-2 text-xs text-slate-700 font-medium">
                <span className="w-7 h-7 rounded-full bg-slate-200 flex items-center justify-center text-slate-600">
                  <User className="w-4 h-4" />
                </span>
                <span className="hidden md:inline font-semibold">{user.full_name}</span>
                <span className="text-[10px] uppercase font-bold px-1.5 py-0.5 rounded bg-brand-100 text-brand-700">
                  {role}
                </span>
              </div>

              <button
                onClick={logout}
                className="p-1.5 text-slate-400 hover:text-slate-600 rounded-lg hover:bg-slate-100 transition"
                title="Log out"
              >
                <LogOut className="w-4 h-4" />
              </button>
            </>
          ) : (
            <div className="flex items-center gap-2">
              <button
                onClick={() => quickLogin('student')}
                className="text-xs font-semibold px-3 py-1.5 rounded-lg bg-brand-50 hover:bg-brand-100 text-brand-700 transition"
              >
                Demo Student
              </button>
              <button
                onClick={() => quickLogin('teacher')}
                className="text-xs font-semibold px-3 py-1.5 rounded-lg bg-slate-900 hover:bg-slate-800 text-white transition"
              >
                Demo Teacher
              </button>
            </div>
          )}
        </div>
      </div>
    </header>
  );
}
