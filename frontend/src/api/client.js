/**
 * REST API client for Knowlix backend.
 */
const BASE_URL = '/api';

export function getAuthHeaders() {
  const token = localStorage.getItem('knowlix_token');
  return {
    'Content-Type': 'application/json',
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
  };
}

export async function apiRequest(endpoint, options = {}) {
  const res = await fetch(`${BASE_URL}${endpoint}`, {
    ...options,
    headers: {
      ...getAuthHeaders(),
      ...(options.headers || {}),
    },
  });

  if (!res.ok) {
    const errorData = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(errorData.detail || 'An unexpected API error occurred');
  }

  return res.json();
}

export const api = {
  // Auth
  login: (email, password) =>
    apiRequest('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    }),
  register: (fullName, email, password, role) =>
    apiRequest('/auth/register', {
      method: 'POST',
      body: JSON.stringify({ full_name: fullName, email, password, role }),
    }),
  getMe: () => apiRequest('/auth/me'),

  // Student
  getStudentDashboard: () => apiRequest('/student/dashboard'),
  getKnowledgeGraph: (subject) =>
    apiRequest(`/student/knowledge-graph${subject ? `?subject=${encodeURIComponent(subject)}` : ''}`),
  getStudentMisconceptions: () => apiRequest('/student/misconceptions'),
  tutorChat: (topic, message, teachingStyle) =>
    apiRequest('/student/tutor/chat', {
      method: 'POST',
      body: JSON.stringify({ topic, message, teaching_style: teachingStyle }),
    }),
  getStudyPlans: () => apiRequest('/student/study-plans'),
  toggleStudyTask: (taskId) =>
    apiRequest(`/student/study-plans/task/${taskId}/toggle`, { method: 'PATCH' }),

  // Teacher
  getTeacherDashboard: () => apiRequest('/teacher/dashboard'),
  getTeacherClasses: () => apiRequest('/teacher/classes'),
  getClassStudents: (classId) => apiRequest(`/teacher/classes/${classId}/students`),
  getInterventions: () => apiRequest('/teacher/interventions'),
  uploadCurriculum: async (formData) => {
    const token = localStorage.getItem('knowlix_token');
    const res = await fetch(`${BASE_URL}/teacher/curriculum/upload`, {
      method: 'POST',
      headers: {
        ...(token ? { Authorization: `Bearer ${token}` } : {}),
      },
      body: formData,
    });
    if (!res.ok) throw new Error('Upload failed');
    return res.json();
  },

  // Central ReAct Agent execution
  queryAgent: (query) =>
    apiRequest('/agent/query', {
      method: 'POST',
      body: JSON.stringify({ query }),
    }),
};

