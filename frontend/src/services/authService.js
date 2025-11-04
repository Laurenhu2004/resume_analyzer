import api from './api'

export const authService = {
  async register(email, password) {
    const response = await api.post('/auth/register', { email, password })
    return response.data
  },

  async login(email, password) {
    const params = new URLSearchParams()
    params.append('username', email)
    params.append('password', password)
    
    const response = await api.post('/auth/login', params.toString(), {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    })
    
    if (response.data.access_token) {
      localStorage.setItem('token', response.data.access_token)
    }
    
    return response.data
  },

  async getCurrentUser() {
    const response = await api.get('/auth/me')
    return response.data
  },

  logout() {
    localStorage.removeItem('token')
    window.location.href = '/login'
  },

  isAuthenticated() {
    return !!localStorage.getItem('token')
  },
}
