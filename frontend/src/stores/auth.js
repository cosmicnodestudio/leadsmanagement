import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authService } from '../services/auth'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const token = ref(null)
  const isAuthenticated = computed(() => !!token.value)
  const loading = ref(false)
  const error = ref(null)

  const register = async (email, name, password) => {
    loading.value = true
    error.value = null

    try {
      const response = await authService.register(email, name, password)
      return response.data
    } catch (err) {
      error.value = err.response?.data?.error || 'Registration failed'
      throw error.value
    } finally {
      loading.value = false
    }
  }

  const login = async (email, password) => {
    loading.value = true
    error.value = null

    try {
      const response = await authService.login(email, password)
      token.value = response.data.access_token
      user.value = response.data.user
      authService.setToken(response.data.access_token, response.data.refresh_token)
      localStorage.setItem('user', JSON.stringify(response.data.user))
      return response.data
    } catch (err) {
      error.value = err.response?.data?.error || 'Login failed'
      throw error.value
    } finally {
      loading.value = false
    }
  }

  const logout = () => {
    authService.logout()
    token.value = null
    user.value = null
    error.value = null
    localStorage.removeItem('user')
  }

  const checkAuth = () => {
    const storedToken = authService.getToken()
    if (storedToken) {
      token.value = storedToken
      const storedUser = localStorage.getItem('user')
      if (storedUser) {
        try {
          user.value = JSON.parse(storedUser)
        } catch {
          user.value = null
        }
      }
    } else {
      token.value = null
      user.value = null
      authService.logout()
    }
  }

  const changePassword = async (oldPassword, newPassword) => {
    loading.value = true
    error.value = null

    try {
      const response = await authService.changePassword(oldPassword, newPassword)
      return response.data
    } catch (err) {
      error.value = err.response?.data?.error || 'Password change failed'
      throw error.value
    } finally {
      loading.value = false
    }
  }

  return {
    user,
    token,
    isAuthenticated,
    loading,
    error,
    register,
    login,
    logout,
    checkAuth,
    changePassword
  }
})
