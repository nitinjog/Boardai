// In production (Netlify), set VITE_API_BASE_URL to your Render backend URL
// e.g. https://boardai-backend.onrender.com/api/v1
export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api/v1'
export const MAX_FILE_SIZE_MB = 10
export const ALLOWED_UPLOAD_TYPES = ['image/jpeg', 'image/png', 'image/webp', 'application/pdf']
export const AUTOSAVE_INTERVAL_MS = 10000  // 10 seconds
