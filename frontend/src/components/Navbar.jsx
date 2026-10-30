import React from 'react';
import { GraduationCap } from 'lucide-react';
import { useAuth } from '../context/AuthContext';

export default function Navbar() {
  const { user, role, logout } = useAuth();

  const getRoleDisplayName = () => {
    if (role === 'teacher') {
      return `${user?.full_name || 'Demo Teacher'} · Teacher`;
    }
    return `${user?.full_name || 'Demo Student'} · Student`;
  };

  return (
    <header className="bg-white border-b border-slate-100 sticky top-0 z-30">
      <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
        {/* Logo */}
        <div className="flex items-center gap-2.5">
          <div className="w-8 h-8 rounded-xl bg-[#342767] flex items-center justify-center text-white shadow-xs">
            <GraduationCap className="w-5 h-5" />
          </div>
          <span className="text-xl font-bold text-slate-900 tracking-tight">Knowlix</span>
        </div>

        {/* User Badge & Sign out */}
        {user && (
          <div className="flex items-center gap-4">
            <span className="text-sm font-medium text-slate-600 hidden sm:inline-block">
              {getRoleDisplayName()}
            </span>
            <button
              onClick={logout}
              className="border border-slate-200 px-4 py-1.5 rounded-xl text-xs sm:text-sm font-semibold hover:bg-slate-50 text-slate-800 transition"
            >
              Sign out
            </button>
          </div>
        )}
      </div>
    </header>
  );
}
