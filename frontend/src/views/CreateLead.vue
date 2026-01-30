<template>
  <div class="space-y-6">
    <div>
      <router-link to="/leads" class="inline-flex items-center gap-1 text-sm text-indigo-400 hover:text-indigo-300">
        <ArrowLeft size="16" /> Back to Leads
      </router-link>
      <h1 class="mt-2 flex items-center gap-2 text-2xl font-semibold"><FileText size="28" /> Create New Lead</h1>
    </div>

    <div v-if="leadsStore.error" class="rounded-md border border-rose-500/40 bg-rose-500/10 px-4 py-3 text-sm text-rose-200">
      {{ leadsStore.error }}
    </div>

    <div class="rounded-xl border border-slate-800 bg-slate-900/60 p-6">
      <form @submit.prevent="createLead" class="space-y-6">
        <div class="grid gap-6 sm:grid-cols-2">
          <div>
            <label for="name" class="block text-sm font-medium text-slate-300">Name *</label>
            <input
              id="name"
              v-model="form.name"
              type="text"
              required
              placeholder="Lead name"
              class="mt-2 w-full rounded-md border border-slate-700 bg-slate-950 px-3 py-2 text-slate-100 placeholder-slate-500 focus:border-indigo-500 focus:outline-none"
            />
          </div>
          <div>
            <label for="email" class="block text-sm font-medium text-slate-300">Email *</label>
            <input
              id="email"
              v-model="form.email"
              type="email"
              required
              placeholder="email@example.com"
              class="mt-2 w-full rounded-md border border-slate-700 bg-slate-950 px-3 py-2 text-slate-100 placeholder-slate-500 focus:border-indigo-500 focus:outline-none"
            />
          </div>
        </div>

        <div class="grid gap-6 sm:grid-cols-2">
          <div>
            <label for="phone" class="block text-sm font-medium text-slate-300">Phone</label>
            <input
              id="phone"
              v-model="form.phone"
              type="tel"
              placeholder="+1 (555) 000-0000"
              class="mt-2 w-full rounded-md border border-slate-700 bg-slate-950 px-3 py-2 text-slate-100 placeholder-slate-500 focus:border-indigo-500 focus:outline-none"
            />
          </div>
          <div>
            <label for="company" class="block text-sm font-medium text-slate-300">Company</label>
            <input
              id="company"
              v-model="form.company"
              type="text"
              placeholder="Company name"
              class="mt-2 w-full rounded-md border border-slate-700 bg-slate-950 px-3 py-2 text-slate-100 placeholder-slate-500 focus:border-indigo-500 focus:outline-none"
            />
          </div>
        </div>

        <div class="grid gap-6 sm:grid-cols-2">
          <div>
            <label for="source" class="block text-sm font-medium text-slate-300">Source *</label>
            <select
              id="source"
              v-model="form.source"
              required
              class="mt-2 w-full rounded-md border border-slate-700 bg-slate-950 px-3 py-2 text-slate-100 focus:border-indigo-500 focus:outline-none"
            >
              <option value="">Select source...</option>
              <option value="website">Website</option>
              <option value="referral">Referral</option>
              <option value="social_media">Social Media</option>
              <option value="email">Email</option>
              <option value="other">Other</option>
            </select>
          </div>
          <div>
            <label for="status" class="block text-sm font-medium text-slate-300">Status</label>
            <select
              id="status"
              v-model="form.status"
              class="mt-2 w-full rounded-md border border-slate-700 bg-slate-950 px-3 py-2 text-slate-100 focus:border-indigo-500 focus:outline-none"
            >
              <option value="new">New</option>
              <option value="contacted">Contacted</option>
              <option value="qualified">Qualified</option>
              <option value="converted">Converted</option>
              <option value="lost">Lost</option>
            </select>
          </div>
        </div>

        <div>
          <label for="notes" class="block text-sm font-medium text-slate-300">Notes</label>
          <textarea
            id="notes"
            v-model="form.notes"
            placeholder="Add notes about this lead..."
            rows="4"
            class="mt-2 w-full rounded-md border border-slate-700 bg-slate-950 px-3 py-2 text-slate-100 placeholder-slate-500 focus:border-indigo-500 focus:outline-none"
          ></textarea>
        </div>

        <div class="flex gap-3">
          <button
            type="submit"
            :disabled="loading"
            class="inline-flex items-center gap-2 rounded-md bg-indigo-600 px-6 py-2 text-white hover:bg-indigo-500 disabled:opacity-50"
          >
            <Check size="18" /> {{ loading ? 'Creating...' : 'Create Lead' }}
          </button>
          <router-link to="/leads" class="inline-flex items-center gap-2 rounded-md border border-slate-700 px-6 py-2 text-slate-300 hover:bg-slate-800">
            <X size="18" /> Cancel
          </router-link>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ArrowLeft, FileText, Check, X } from 'lucide-vue-next'
import { useLeadsStore } from '../stores/leads'
import { useToastStore } from '../stores/toast'

const router = useRouter()
const leadsStore = useLeadsStore()
const toastStore = useToastStore()

const loading = ref(false)
const form = ref({
  name: '',
  email: '',
  phone: '',
  company: '',
  source: '',
  status: 'new',
  notes: ''
})

const createLead = async () => {
  if (!form.value.name || !form.value.email || !form.value.source) {
    toastStore.addToast('Please fill in required fields', 'warning')
    return
  }

  loading.value = true
  try {
    await leadsStore.createLead(form.value)
    toastStore.addToast('Lead created successfully', 'success')
    router.push('/leads')
  } catch (error) {
    toastStore.addToast('Failed to create lead', 'error')
  } finally {
    loading.value = false
  }
}
</script>
