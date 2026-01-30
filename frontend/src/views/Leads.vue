<template>
  <div class="space-y-6">
    <div class="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
      <h1 class="text-2xl font-semibold">Leads Management</h1>
      <div class="flex w-full flex-col gap-3 sm:flex-row sm:items-center md:w-auto">
        <div class="relative w-full sm:w-64">
          <Search class="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500" size="18" />
          <input
            v-model="searchQuery"
            @keyup="handleSearch"
            type="text"
            placeholder="Search leads..."
            class="w-full rounded-md border border-slate-700 bg-slate-950 pl-9 pr-3 py-2 text-slate-100 placeholder-slate-500 focus:border-indigo-500 focus:outline-none"
          />
        </div>
        <router-link
          to="/leads/new"
          class="inline-flex items-center justify-center gap-2 rounded-md bg-indigo-600 px-4 py-2 text-white hover:bg-indigo-500"
        >
          <Plus size="18" /> New Lead
        </router-link>
      </div>
    </div>

    <div v-if="leadsStore.error" class="rounded-md border border-rose-500/40 bg-rose-500/10 px-4 py-3 text-sm text-rose-200">
      {{ leadsStore.error }}
    </div>

    <div v-if="leadsStore.loading" class="text-center text-slate-400">
      Loading leads...
    </div>

    <div v-else-if="leadsStore.leads.length === 0" class="rounded-lg border border-slate-800 bg-slate-900/60 p-6 text-center text-slate-400">
      <p>
        No leads found.
        <router-link to="/leads/new" class="text-indigo-400 hover:text-indigo-300">Create one</router-link>
      </p>
    </div>

    <div v-else class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
      <div
        v-for="lead in leadsStore.leads"
        :key="lead.id"
        class="cursor-pointer rounded-xl border border-slate-800 bg-slate-900/60 p-5 transition hover:-translate-y-0.5 hover:border-slate-700"
        @click="goToDetail(lead.id)"
      >
        <div class="flex items-start justify-between gap-2">
          <h3 class="text-lg font-semibold text-slate-100">{{ lead.name }}</h3>
          <span
            class="rounded-full px-2 py-1 text-xs uppercase"
            :class="{
              'bg-sky-500/10 text-sky-300': lead.status === 'new',
              'bg-amber-500/10 text-amber-300': lead.status === 'contacted',
              'bg-emerald-500/10 text-emerald-300': lead.status === 'qualified',
              'bg-emerald-500/10 text-emerald-300': lead.status === 'converted',
              'bg-rose-500/10 text-rose-300': lead.status === 'lost'
            }"
          >
            {{ lead.status }}
          </span>
        </div>
        <p class="mt-2 text-sm text-slate-400">{{ lead.email }}</p>
        <p v-if="lead.company" class="mt-1 text-sm text-slate-500">{{ lead.company }}</p>
        <div class="mt-4 flex items-center justify-between border-t border-slate-800 pt-3 text-xs text-slate-500">
          <span>{{ lead.source }}</span>
          <span>{{ formatDate(lead.created_at) }}</span>
        </div>
      </div>
    </div>

    <div v-if="leadsStore.pages > 1" class="flex items-center justify-center gap-3 rounded-lg border border-slate-800 bg-slate-900/60 px-4 py-3">
      <button
        v-if="leadsStore.currentPage > 1"
        @click="previousPage"
        class="inline-flex items-center gap-1 rounded-md border border-slate-700 px-3 py-1 text-sm text-slate-200 hover:border-slate-600"
      >
        <ChevronLeft size="16" /> Previous
      </button>
      <span class="text-sm text-slate-400">Page {{ leadsStore.currentPage }} of {{ leadsStore.pages }}</span>
      <button
        v-if="leadsStore.currentPage < leadsStore.pages"
        @click="nextPage"
        class="inline-flex items-center gap-1 rounded-md border border-slate-700 px-3 py-1 text-sm text-slate-200 hover:border-slate-600"
      >
        Next <ChevronRight size="16" />
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { Search, Plus, ChevronLeft, ChevronRight } from 'lucide-vue-next'
import { useLeadsStore } from '../stores/leads'

const router = useRouter()
const leadsStore = useLeadsStore()

const searchQuery = ref('')
let searchTimeout = null

const formatDate = (date) => {
  return new Date(date).toLocaleDateString()
}

const goToDetail = (id) => {
  router.push(`/leads/${id}`)
}

const handleSearch = () => {
  clearTimeout(searchTimeout)

  if (!searchQuery.value.trim()) {
    leadsStore.listLeads(1)
    return
  }

  searchTimeout = setTimeout(() => {
    leadsStore.searchLeads(searchQuery.value, 1)
  }, 500)
}

const previousPage = () => {
  leadsStore.listLeads(leadsStore.currentPage - 1)
}

const nextPage = () => {
  leadsStore.listLeads(leadsStore.currentPage + 1)
}

onMounted(async () => {
  await leadsStore.listLeads(1)
})
</script>
