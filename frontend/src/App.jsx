import React, { useState } from 'react';
import { AuthProvider, useAuth } from './context/AuthContext';
import Navbar from './components/Navbar';
import LandingPage from './pages/LandingPage';
import StudentPortal from './pages/student/StudentPortal';
import TeacherPortal from './pages/teacher/TeacherPortal';

function AppContent() {
  const { user, role } = useAuth();
  const [view, setView] = useState('home');

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col font-sans">
      <Navbar onNavigate={setView} currentTab={view} />
      <main className="flex-1">
        {!user ? (
          <LandingPage onExplore={() => setView('portal')} />
        ) : role === 'teacher' ? (
          <TeacherPortal />
        ) : (
          <StudentPortal />
        )}
      </main>
    </div>
  );
}

export default function App() {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  );
}
