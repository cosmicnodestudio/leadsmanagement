import api from './api'

export const authService = {
  register: (email, name, password) => {
    return api.post('/auth/register', { email, name, password })
  },

  login: (email, password) => {
    return api.post('/auth/login', { email, password })
  },

  logout: () => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    localStorage.removeItem('user')
    return Promise.resolve()
  },

  getProfile: () => {
    return api.get('/auth/profile')
  },

  changePassword: (oldPassword, newPassword) => {
    return api.post('/auth/change-password', { old_password: oldPassword, new_password: newPassword })
  },

  setToken: (accessToken, refreshToken) => {
    if (accessToken && accessToken !== 'null' && accessToken !== 'undefined') {
      const normalized = accessToken.startsWith('Bearer ') ? accessToken.slice(7) : accessToken
      localStorage.setItem('access_token', normalized)
    } else {
      localStorage.removeItem('access_token')
    }

    if (refreshToken && refreshToken !== 'null' && refreshToken !== 'undefined') {
      const normalizedRefresh = refreshToken.startsWith('Bearer ')
        ? refreshToken.slice(7)
        : refreshToken
      localStorage.setItem('refresh_token', normalizedRefresh)
    } else {
      localStorage.removeItem('refresh_token')
    }
  },

  getToken: () => {
    const token = localStorage.getItem('access_token')
    const cleaned = token ? token.trim() : ''
    const normalized = cleaned.startsWith('Bearer ') ? cleaned.slice(7) : cleaned
    if (!normalized || normalized === 'null' || normalized === 'undefined') {
      return null
    }
    const parts = normalized.split('.')
    if (parts.length !== 3) {
      return null
    }
    return normalized
  }
}
