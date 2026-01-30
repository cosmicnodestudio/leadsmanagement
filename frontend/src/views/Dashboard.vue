<template>
  <div class="space-y-6">
    <div class="rounded-2xl border border-slate-800 bg-gradient-to-br from-slate-900 to-slate-950 p-8">
      <h1 class="flex items-center gap-2 text-2xl font-semibold"><UserCircle size="32" /> Welcome, {{ authStore.user?.name }}!</h1>
      <p class="mt-2 text-slate-400">Manage your leads efficiently</p>
    </div>

    <div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
      <div class="rounded-xl border border-slate-800 bg-slate-900/60 p-5">
        <div class="flex items-center gap-2">
          <Users size="20" class="text-indigo-400" />
          <h3 class="text-sm text-slate-400">Total Leads</h3>
        </div>
        <p class="mt-2 text-3xl font-semibold text-indigo-400">{{ leadsStore.total }}</p>
      </div>

      <div class="rounded-xl border border-slate-800 bg-slate-900/60 p-5">
        <div class="flex items-center gap-2">
          <Zap size="20" class="text-yellow-400" />
          <h3 class="text-sm text-slate-400">New Leads</h3>
        </div>
        <p class="mt-2 text-3xl font-semibold text-indigo-400">{{ newLeadsCount }}</p>
      </div>

      <div class="rounded-xl border border-slate-800 bg-slate-900/60 p-5">
        <div class="flex items-center gap-2">
          <CheckCircle size="20" class="text-emerald-400" />
          <h3 class="text-sm text-slate-400">Converted</h3>
        </div>
        <p class="mt-2 text-3xl font-semibold text-emerald-400">{{ convertedLeadsCount }}</p>
      </div>

      <div class="rounded-xl border border-slate-800 bg-slate-900/60 p-5">
        <div class="flex items-center gap-2">
          <Clock size="20" class="text-amber-400" />
          <h3 class="text-sm text-slate-400">In Progress</h3>
        </div>
        <p class="mt-2 text-3xl font-semibold text-amber-400">{{ inProgressCount }}</p>
      </div>
    </div>

    <router-link
      to="/leads"
      class="inline-flex items-center gap-2 rounded-md bg-indigo-600 px-4 py-2 text-white hover:bg-indigo-500"
    >
      <ListChecks size="18" /> View All Leads
    </router-link>
    <router-link
      to="/leads/new"
      class="ml-3 inline-flex items-center gap-2 rounded-md bg-emerald-600 px-4 py-2 text-white hover:bg-emerald-500"
    >
      <Plus size="18" /> New Lead
    </router-link>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { UserCircle, Users, Zap, CheckCircle, Clock, ListChecks, Plus } from 'lucide-vue-next'
import { useAuthStore } from '../stores/auth'
import { useLeadsStore } from '../stores/leads'

const authStore = useAuthStore()
const leadsStore = useLeadsStore()

const newLeadsCount = computed(() => {
  return leadsStore.leads.filter(l => l.status === 'new').length
})

const convertedLeadsCount = computed(() => {
  return leadsStore.leads.filter(l => l.status === 'converted').length
})

const inProgressCount = computed(() => {
  const statuses = ['contacted', 'qualified']
  return leadsStore.leads.filter(l => statuses.includes(l.status)).length
})

onMounted(async () => {
  if (leadsStore.leads.length === 0) {
    await leadsStore.listLeads()
  }
})
</script>
