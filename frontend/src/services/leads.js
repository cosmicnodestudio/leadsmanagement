import api from './api'

export const leadsService = {
  list: (page = 1, perPage = 9, status = null) => {
    const params = { page, per_page: perPage }
    if (status) params.status = status
    return api.get('/leads', { params })
  },

  create: (leadData) => {
    return api.post('/leads', leadData)
  },

  get: (id) => {
    return api.get(`/leads/${id}`)
  },

  update: (id, leadData) => {
    return api.put(`/leads/${id}`, leadData)
  },

  delete: (id) => {
    return api.delete(`/leads/${id}`)
  },

  search: (query, page = 1, perPage = 9) => {
    return api.get('/leads/search', {
      params: { q: query, page, per_page: perPage }
    })
  },

  getInteractions: (leadId) => {
    return api.get(`/leads/${leadId}/interactions`)
  },

  addInteraction: (leadId, interactionData) => {
    return api.post(`/leads/${leadId}/interactions`, interactionData)
  },

  deleteInteraction: (interactionId) => {
    return api.delete(`/leads/interactions/${interactionId}`)
  }
}
