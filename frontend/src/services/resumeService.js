import api from './api'

export const resumeService = {
  async uploadAndAnalyze(file, targetRole = null) {
    const formData = new FormData()
    formData.append('file', file)
    if (targetRole) {
      formData.append('target_role', targetRole)
    }
    
    // Don't set Content-Type manually - axios will set it automatically with the correct boundary
    // This ensures the Authorization header from the interceptor is preserved
    const response = await api.post('/analyze/upload', formData)
    
    return response.data
  },

  async exportImprovedResume(content) {
    const response = await api.post(
      '/analyze/improve',
      { content },
      {
        responseType: 'blob',
      }
    )
    
    // Create download link
    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', 'improved_resume.pdf')
    document.body.appendChild(link)
    link.click()
    link.remove()
    window.URL.revokeObjectURL(url)
    
    return true
  },
}
