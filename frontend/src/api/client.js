import axios from 'axios'
import { API_BASE_URL } from '../constants/config'

const client = axios.create({
  baseURL: API_BASE_URL,
  timeout: 120000, // 2 min — Gemini can be slow on free tier
  headers: { 'Content-Type': 'application/json' },
})

// Attach student ID header from localStorage
client.interceptors.request.use((config) => {
  const stored = localStorage.getItem('boardai_student')
  if (stored) {
    try {
      const student = JSON.parse(stored)
      if (student?.id) config.headers['X-Student-ID'] = student.id
    } catch { /* ignore */ }
  }
  return config
})

// Normalise error responses
client.interceptors.response.use(
  (res) => res,
  (err) => {
    const msg = err.response?.data?.detail || err.message || 'Something went wrong'
    return Promise.reject(new Error(typeof msg === 'string' ? msg : JSON.stringify(msg)))
  }
)

export default client
