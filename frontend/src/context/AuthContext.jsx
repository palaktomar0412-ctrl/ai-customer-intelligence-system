/**
 * Authentication Context - Manages user authentication state,
 * JWT tokens, and provides login/logout/register functionality.
 */
import { createContext, useContext, useState, useEffect } from 'react'
import api from '../services/api'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [token, setToken] = useState(localStorage.getItem('token'))
  const [loading, setLoading] = useState(true)

  // Check if user is authenticated on mount
  useEffect(() => {
    if (token) {
      api.defaults.headers.common['Authorization'] = `Bearer ${token}`
      fetchCurrentUser()
    } else {
      setLoading(false)
    }
  }, [])

  const fetchCurrentUser = async () => {
    try {
      const response = await api.get('/auth/me')
      setUser(response.data)
    } catch (error) {
      console.error('Failed to fetch user:', error)
      logout()
    } finally {
      setLoading(false)
    }
  }

  const login = async (email, password) => {
    const response = await api.post('/auth/login', { email, password })
    const { access_token, refresh_token, user: userData } = response.data

    localStorage.setItem('token', access_token)
    localStorage.setItem('refresh_token', refresh_token)
    api.defaults.headers.common['Authorization'] = `Bearer ${access_token}`

    setToken(access_token)
    setUser(userData)
    return userData
  }

  const register = async (userData) => {
    const response = await api.post('/auth/register', userData)
    const { access_token, refresh_token, user: newUser } = response.data

    localStorage.setItem('token', access_token)
    localStorage.setItem('refresh_token', refresh_token)
    api.defaults.headers.common['Authorization'] = `Bearer ${access_token}`

    setToken(access_token)
    setUser(newUser)
    return newUser
  }

  const logout = () => {
    localStorage.removeItem('token')
    localStorage.removeItem('refresh_token')
    delete api.defaults.headers.common['Authorization']
    setToken(null)
    setUser(null)
  }

  const value = {
    user,
    token,
    loading,
    login,
    register,
    logout,
    isAuthenticated: !!token,
  }

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}
