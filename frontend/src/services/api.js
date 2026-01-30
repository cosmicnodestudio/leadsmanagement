import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000'

const api = axios.create({
  baseURL: `${API_URL}/api`,
  headers: {
    'Content-Type': 'application/json'
  }
})

const normalizeToken = (token) => {
  if (!token) return null
  const trimmed = token.trim()
  const normalized = trimmed.startsWith('Bearer ') ? trimmed.slice(7) : trimmed
  if (!normalized || normalized === 'null' || normalized === 'undefined') return null
  return normalized.split('.').length === 3 ? normalized : null
}

// Add token to requests
api.interceptors.request.use(config => {
  const token = normalizeToken(localStorage.getItem('access_token'))
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  } else {
    delete config.headers.Authorization
    delete api.defaults.headers.common.Authorization
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
  }
  return config
}, error => Promise.reject(error))

// Handle token refresh
api.interceptors.response.use(
  response => response,
  async error => {
    const originalRequest = error.config

    if (error.response?.status === 422) {
      const message = error.response?.data?.msg || ''
      if (message.toLowerCase().includes('not enough segments')) {
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        delete api.defaults.headers.common.Authorization
        window.location.href = '/login'
        return Promise.reject(error)
      }
    }

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true

      try {
        const refreshToken = normalizeToken(localStorage.getItem('refresh_token'))
        if (refreshToken) {
          const response = await axios.post(`${API_URL}/api/auth/refresh`, {}, {
            headers: { Authorization: `Bearer ${refreshToken}` }
          })

          if (response.data?.access_token) {
            localStorage.setItem('access_token', response.data.access_token)
            api.defaults.headers.common.Authorization = `Bearer ${response.data.access_token}`
          }

          return api(originalRequest)
        }
      } catch (refreshError) {
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        window.location.href = '/login'
      }
    }

    return Promise.reject(error)
  }
)

export default api
