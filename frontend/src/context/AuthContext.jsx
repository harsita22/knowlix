import React, { createContext, useContext, useState, useEffect } from 'react';
import { api } from '../api/client';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('knowlix_token'));
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function checkAuth() {
      if (token) {
        try {
          const profile = await api.getMe();
          setUser(profile);
        } catch (err) {
          console.warn('Session expired or invalid token', err);
          logout();
        }
      }
      setLoading(false);
    }
    checkAuth();
  }, [token]);

  const login = async (email, password) => {
    const data = await api.login(email, password);
    localStorage.setItem('knowlix_token', data.access_token);
    setToken(data.access_token);
    setUser(data.user);
    return data.user;
  };

  const logout = () => {
    localStorage.removeItem('knowlix_token');
    setToken(null);
    setUser(null);
  };

  // Quick 1-click login for evaluation and testing
  const quickLogin = async (role = 'student') => {
    if (role === 'teacher') {
      return login('teacher@knowlix.edu', 'teacher123');
    } else {
      return login('student1@knowlix.edu', 'student123');
    }
  };

  return (
    <AuthContext.Provider value={{ user, token, role: user?.role, login, logout, quickLogin, loading }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => useContext(AuthContext);

