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

// OpenClaw API
export const openclawApi = {
  process: (data: any) => api.post('/openclaw/process', data),
  executeSkill: (data: any) => api.post('/openclaw/execute-skill', data),
  getSkills: () => api.get('/openclaw/skills'),
  chat: (data: any) => api.post('/openclaw/chat', data),
  health: () => api.get('/openclaw/health'),
}

// 多媒体AI API
export const multimediaApi = {
  textToImage: (data: any) => api.post('/multimedia/text-to-image', data),
  imageToImage: (data: any) => api.post('/multimedia/image-to-image', data),
  generateVideo: (data: any) => api.post('/multimedia/generate-video', data),
  editImage: (data: any) => api.post('/multimedia/edit-image', data),
  removeWatermark: (data: any) => api.post('/multimedia/remove-watermark', data),
  getWatermarkRemovalResult: (jobId: string) => api.get(`/multimedia/watermark-removal/${jobId}`),
  getWatermarkRemovalTechniques: () => api.get('/multimedia/watermark-removal/techniques'),
  getStyles: () => api.get('/multimedia/styles'),
  getJobStatus: (jobId: string) => api.get(`/multimedia/job-status/${jobId}`),
  uploadImage: (formData: FormData) => api.post('/multimedia/upload-image', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  }),
  health: () => api.get('/multimedia/health'),
}

// ComfyUI API
export const comfyuiApi = {
  getHealth: () => api.get('/comfyui/health'),
  getQueueStatus: () => api.get('/comfyui/queue-status'),
  getModels: () => api.get('/comfyui/models'),
  getSystemStats: () => api.get('/comfyui/system-stats'),
  generateFromWorkflow: (data: any) => api.post('/comfyui/generate', data),
  quickTextToImage: (data: any) => api.post('/comfyui/quick/text-to-image', data),
  quickImageToImage: (data: any) => api.post('/comfyui/quick/image-to-image', data),
  quickInpainting: (data: any) => api.post('/comfyui/quick/inpainting', data),
  getWorkflowTemplates: () => api.get('/comfyui/workflow-templates'),
  getWorkflowTemplate: (name: string) => api.get(`/comfyui/workflow-templates/${name}`),
  uploadImage: (formData: FormData) => api.post('/comfyui/upload-image', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  }),
  interrupt: () => api.post('/comfyui/interrupt'),
}

// 高级去水印API
export const watermarkRemovalApi = {
  removeByCoordinates: (data: any) => api.post('/advanced-watermark-removal/by-coordinates', data),
  removeByColorRange: (data: any) => api.post('/advanced-watermark-removal/by-color-range', data),
  removeByEdgeDetection: (formData: FormData) => api.post('/advanced-watermark-removal/by-edge-detection', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  }),
  detectAreas: (formData: FormData) => api.post('/advanced-watermark-removal/detect-areas', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  }),
  removeByClicks: (data: any) => api.post('/advanced-watermark-removal/by-clicks', data),
  removeBySegmentation: (formData: FormData) => api.post('/advanced-watermark-removal/by-segmentation', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  }),
  health: () => api.get('/advanced-watermark-removal/health'),
}

export default api
