import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { leadsService } from '../services/leads'

export const useLeadsStore = defineStore('leads', () => {
  const leads = ref([])
  const currentLead = ref(null)
  const loading = ref(false)
  const error = ref(null)
  const total = ref(0)
  const pages = ref(0)
  const currentPage = ref(1)

  const listLeads = async (page = 1, status = null) => {
    loading.value = true
    error.value = null

    try {
      const response = await leadsService.list(page, 9, status)
      leads.value = response.data.leads
      total.value = response.data.total
      pages.value = response.data.pages
      currentPage.value = page
      return response.data
    } catch (err) {
      error.value = err.response?.data?.error || 'Failed to load leads'
      throw error.value
    } finally {
      loading.value = false
    }
  }

  const createLead = async (leadData) => {
    loading.value = true
    error.value = null

    try {
      const response = await leadsService.create(leadData)
      leads.value.unshift(response.data.lead)
      return response.data.lead
    } catch (err) {
      error.value = err.response?.data?.error || 'Failed to create lead'
      throw error.value
    } finally {
      loading.value = false
    }
  }

  const getLead = async (id) => {
    loading.value = true
    error.value = null

    try {
      const response = await leadsService.get(id)
      currentLead.value = response.data.lead
      return response.data.lead
    } catch (err) {
      error.value = err.response?.data?.error || 'Failed to load lead'
      throw error.value
    } finally {
      loading.value = false
    }
  }

  const updateLead = async (id, leadData) => {
    loading.value = true
    error.value = null

    try {
      const response = await leadsService.update(id, leadData)
      const index = leads.value.findIndex(l => l.id === id)
      if (index !== -1) {
        leads.value[index] = response.data.lead
      }
      currentLead.value = response.data.lead
      return response.data.lead
    } catch (err) {
      error.value = err.response?.data?.error || 'Failed to update lead'
      throw error.value
    } finally {
      loading.value = false
    }
  }

  const deleteLead = async (id) => {
    loading.value = true
    error.value = null

    try {
      await leadsService.delete(id)
      leads.value = leads.value.filter(l => l.id !== id)
      if (currentLead.value?.id === id) {
        currentLead.value = null
      }
      return true
    } catch (err) {
      error.value = err.response?.data?.error || 'Failed to delete lead'
      throw error.value
    } finally {
      loading.value = false
    }
  }

  const searchLeads = async (query, page = 1) => {
    loading.value = true
    error.value = null

    try {
      const response = await leadsService.search(query, page)
      leads.value = response.data.leads
      total.value = response.data.total
      pages.value = response.data.pages
      currentPage.value = page
      return response.data
    } catch (err) {
      error.value = err.response?.data?.error || 'Search failed'
      throw error.value
    } finally {
      loading.value = false
    }
  }

  return {
    leads,
    currentLead,
    loading,
    error,
    total,
    pages,
    currentPage,
    listLeads,
    createLead,
    getLead,
    updateLead,
    deleteLead,
    searchLeads
  }
})
