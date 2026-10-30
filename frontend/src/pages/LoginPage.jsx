import React, { useState } from 'react';
import { GraduationCap, Mail, Lock, Eye, EyeOff, FileText, Check } from 'lucide-react';
import { useAuth } from '../context/AuthContext';

export default function LoginPage() {
  const { login } = useAuth();
  const [role, setRole] = useState('student'); // 'student' or 'teacher'
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [rememberMe, setRememberMe] = useState(true);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!email.trim() || !password.trim()) return;
    setLoading(true);
    setError('');
    try {
      await login(email.trim(), password.trim());
    } catch (err) {
      setError(err.message || 'Invalid email or password');
    } finally {
      setLoading(false);
    }
  };

  const handleFillDemo = (targetRole) => {
    setRole(targetRole);
    if (targetRole === 'student') {
      setEmail('student@knowlix.demo');
      setPassword('student123');
    } else {
      setEmail('teacher@knowlix.demo');
      setPassword('teacher123');
    }
    setError('');
  };

  return (
    <div className="min-h-screen bg-[#faf8fd] flex flex-col justify-center items-center px-4 py-12">
      {/* Brand Header */}
      <div className="text-center mb-8">
        <div className="w-12 h-12 rounded-2xl bg-[#342767] flex items-center justify-center text-white shadow-md mx-auto mb-3">
          <GraduationCap className="w-7 h-7" />
        </div>
        <h1 className="text-2xl font-bold text-slate-900 tracking-tight">Knowlix</h1>
        <p className="text-xs text-slate-500 font-medium mt-1">Learn Smarter. Grow Better.</p>
      </div>

      {/* Main Login Card */}
      <div className="max-w-[440px] w-full bg-white rounded-3xl p-8 shadow-sm border border-slate-100">
        {/* Role Segmented Tabs */}
        <div className="mb-6">
          <label className="block text-[11px] font-bold text-slate-400 uppercase tracking-wider mb-2">
            I AM SIGNING IN AS
          </label>
          <div className="bg-[#f2f2f7] p-1.5 rounded-2xl flex gap-1">
            <button
              type="button"
              onClick={() => handleFillDemo('student')}
              className={`flex-1 text-left px-4 py-2.5 rounded-xl transition ${
                role === 'student'
                  ? 'bg-white shadow-xs border border-slate-200/50 text-slate-900'
                  : 'text-slate-500 hover:text-slate-800'
              }`}
            >
              <div className="font-bold text-xs sm:text-sm">Student Login</div>
              <div className="text-[11px] text-slate-400">Learning & courses</div>
            </button>

            <button
              type="button"
              onClick={() => handleFillDemo('teacher')}
              className={`flex-1 text-left px-4 py-2.5 rounded-xl transition ${
                role === 'teacher'
                  ? 'bg-white shadow-xs border border-slate-200/50 text-slate-900'
                  : 'text-slate-500 hover:text-slate-800'
              }`}
            >
              <div className="font-bold text-xs sm:text-sm">Teacher Login</div>
              <div className="text-[11px] text-slate-400">Classes & grading</div>
            </button>
          </div>
        </div>

        {error && (
          <div className="mb-4 p-3 rounded-xl bg-rose-50 border border-rose-200 text-rose-700 text-xs">
            {error}
          </div>
        )}

        {/* Credentials Form */}
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1.5">
              Email address
            </label>
            <div className="relative">
              <Mail className="w-4 h-4 text-slate-400 absolute left-3.5 top-3" />
              <input
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="you@example.com"
                className="w-full pl-10 pr-4 py-2.5 rounded-xl border border-slate-200 text-sm focus:outline-none focus:ring-2 focus:ring-[#4c35b5] focus:border-[#4c35b5] text-slate-800 placeholder-slate-400"
              />
            </div>
          </div>

          <div>
            <div className="flex items-center justify-between mb-1.5">
              <label className="block text-xs font-semibold text-slate-700">
                Password
              </label>
              <button
                type="button"
                className="text-xs font-semibold text-[#6e46e6] hover:underline"
              >
                Forgot password?
              </button>
            </div>
            <div className="relative">
              <Lock className="w-4 h-4 text-slate-400 absolute left-3.5 top-3" />
              <input
                type={showPassword ? 'text' : 'password'}
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Enter your password"
                className="w-full pl-10 pr-10 py-2.5 rounded-xl border border-slate-200 text-sm focus:outline-none focus:ring-2 focus:ring-[#4c35b5] focus:border-[#4c35b5] text-slate-800 placeholder-slate-400"
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="absolute right-3 top-3 text-slate-400 hover:text-slate-600"
              >
                {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
              </button>
            </div>
          </div>

          <div className="flex items-center gap-2 pt-1">
            <input
              type="checkbox"
              id="rememberMe"
              checked={rememberMe}
              onChange={(e) => setRememberMe(e.target.checked)}
              className="w-4 h-4 rounded text-[#4c35b5] focus:ring-[#4c35b5] border-slate-300 cursor-pointer"
            />
            <label htmlFor="rememberMe" className="text-xs text-slate-600 font-medium cursor-pointer">
              Remember me
            </label>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full py-3 bg-[#342767] hover:bg-[#281d52] disabled:opacity-50 text-white rounded-xl text-sm font-semibold shadow-xs transition duration-150"
          >
            {loading ? 'Signing in...' : 'Log in'}
          </button>
        </form>

        {/* Demo Accounts Callout (Matching Lovable Screenshot 1) */}
        <div className="mt-6 border border-dashed border-[#cbb8f7] bg-[#fbf9fe] rounded-2xl p-4">
          <div className="flex items-center gap-1.5 text-[#6e46e6] font-bold text-xs uppercase tracking-wider mb-1">
            <FileText className="w-3.5 h-3.5" />
            <span>DEMO ACCOUNTS</span>
          </div>
          <p className="text-[11px] text-slate-500 mb-3">
            For evaluation only — not production accounts. One click fills the form above.
          </p>
          <div className="grid grid-cols-2 gap-2">
            <button
              type="button"
              onClick={() => handleFillDemo('student')}
              className={`p-2.5 rounded-xl border text-left transition ${
                role === 'student' && email === 'student@knowlix.demo'
                  ? 'border-[#6e46e6] bg-white ring-1 ring-[#6e46e6]'
                  : 'border-slate-200 bg-white hover:border-slate-300'
              }`}
            >
              <div className="font-bold text-xs text-slate-900">Fill Student Demo</div>
              <div className="text-[10px] text-slate-400 font-mono truncate">student@knowlix.demo</div>
            </button>

            <button
              type="button"
              onClick={() => handleFillDemo('teacher')}
              className={`p-2.5 rounded-xl border text-left transition ${
                role === 'teacher' && email === 'teacher@knowlix.demo'
                  ? 'border-[#6e46e6] bg-white ring-1 ring-[#6e46e6]'
                  : 'border-slate-200 bg-white hover:border-slate-300'
              }`}
            >
              <div className="font-bold text-xs text-slate-900">Fill Teacher Demo</div>
              <div className="text-[10px] text-slate-400 font-mono truncate">teacher@knowlix.demo</div>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

