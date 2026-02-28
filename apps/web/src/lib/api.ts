import axios from 'axios'

const API_URL = process.env.API_URL || 'http://localhost:8001'

const api = axios.create({
  baseURL: `${API_URL}/api/v1`,
  headers: {
    'Content-Type': 'application/json',
  },
})

// 学习路径 API
export const pathsApi = {
  generate: (data: any) => api.post('/paths/generate', data),
  list: () => api.get('/paths'),
  get: (id: number) => api.get(`/paths/${id}`),
}

// 进度 API
export const progressApi = {
  track: (data: any) => api.post('/progress/track', data),
  getStats: (userId: number) => api.get(`/progress/user/${userId}`),
  getStreak: (userId: number) => api.get(`/progress/streak/${userId}`),
  checkIn: (userId: number, minutes: number) => api.post('/progress/check-in', { userId, minutes_studied: minutes }),
}

// AI 对话 API
export const chatApi = {
  send: (data: any) => api.post('/chat/message', data),
  getConversation: (id: string) => api.get(`/chat/conversation/${id}`),
  list: (userId: number) => api.get(`/chat/user/${userId}/conversations`),
}

// 推荐 API
export const recommendationsApi = {
  get: (data: any) => api.post('/recommendations/', data),
  trending: () => api.get('/recommendations/trending'),
}

// 工作流 API
export const workflowsApi = {
  create: (data: any) => api.post('/workflows/', data),
  list: () => api.get('/workflows'),
  get: (id: number) => api.get(`/workflows/${id}`),
  execute: (id: number, data?: any) => api.post(`/workflows/${id}/execute`, data),
  delete: (id: number) => api.delete(`/workflows/${id}`),
}

export default api
