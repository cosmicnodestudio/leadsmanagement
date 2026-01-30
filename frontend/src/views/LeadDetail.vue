<template>
  <div class="space-y-6">
    <div v-if="leadsStore.loading" class="text-center text-slate-400">
      Loading lead details...
    </div>

    <div v-else-if="leadsStore.currentLead" class="space-y-6">
      <div>
        <router-link to="/leads" class="inline-flex items-center gap-1 text-sm text-indigo-400 hover:text-indigo-300">
          <ArrowLeft size="16" /> Back to Leads
        </router-link>
        <h1 class="mt-2 flex items-center gap-2 text-2xl font-semibold"><UserCheck size="28" /> {{ leadsStore.currentLead.name }}</h1>
      </div>

      <div v-if="leadsStore.error" class="rounded-md border border-rose-500/40 bg-rose-500/10 px-4 py-3 text-sm text-rose-200">
        {{ leadsStore.error }}
      </div>

      <div class="grid gap-6 lg:grid-cols-[2fr_1fr]">
        <div class="space-y-6">
          <div class="rounded-xl border border-slate-800 bg-slate-900/60 p-6">
            <h3 class="mb-4 flex items-center gap-2 text-lg font-semibold"><FileText size="20" /> Contact Information</h3>
            <div class="grid gap-4 sm:grid-cols-2">
              <div>
                <label class="text-xs uppercase text-slate-500">Email</label>
                <p class="mt-1 text-slate-200">{{ leadsStore.currentLead.email }}</p>
              </div>
              <div>
                <label class="text-xs uppercase text-slate-500">Phone</label>
                <p class="mt-1 text-slate-200">{{ leadsStore.currentLead.phone || 'Not provided' }}</p>
              </div>
              <div>
                <label class="text-xs uppercase text-slate-500">Company</label>
                <p class="mt-1 text-slate-200">{{ leadsStore.currentLead.company || 'Not provided' }}</p>
              </div>
              <div>
                <label class="text-xs uppercase text-slate-500">Source</label>
                <p class="mt-1 text-slate-200">{{ leadsStore.currentLead.source }}</p>
              </div>
            </div>
          </div>

          <div class="rounded-xl border border-slate-800 bg-slate-900/60 p-6">
            <h3 class="mb-4 flex items-center gap-2 text-lg font-semibold"><Edit size="20" /> Lead Details</h3>
            <div class="grid gap-4 sm:grid-cols-2">
              <div>
                <label class="text-xs uppercase text-slate-500">Status</label>
                <select
                  v-model="editForm.status"
                  class="mt-1 w-full rounded-md border border-slate-700 bg-slate-950 px-3 py-2 text-slate-100 focus:border-indigo-500 focus:outline-none"
                >
                  <option value="new">New</option>
                  <option value="contacted">Contacted</option>
                  <option value="qualified">Qualified</option>
                  <option value="converted">Converted</option>
                  <option value="lost">Lost</option>
                </select>
              </div>
              <div>
                <label class="text-xs uppercase text-slate-500">Created</label>
                <p class="mt-2 text-slate-200">{{ formatDate(leadsStore.currentLead.created_at) }}</p>
              </div>
            </div>
          </div>

          <div class="rounded-xl border border-slate-800 bg-slate-900/60 p-6">
            <h3 class="mb-4 text-lg font-semibold">Notes</h3>
            <textarea
              v-model="editForm.notes"
              placeholder="Add notes about this lead..."
              rows="4"
              class="w-full rounded-md border border-slate-700 bg-slate-950 px-3 py-2 text-slate-100 placeholder-slate-500 focus:border-indigo-500 focus:outline-none"
            ></textarea>
          </div>

          <div class="flex flex-wrap gap-3">
            <button @click="updateLead" class="inline-flex items-center gap-2 rounded-md bg-emerald-600 px-4 py-2 text-white hover:bg-emerald-500">
              <Save size="18" /> Save Changes
            </button>
            <button @click="deleteLead" class="inline-flex items-center gap-2 rounded-md bg-rose-600 px-4 py-2 text-white hover:bg-rose-500">
              <Trash2 size="18" /> Delete Lead
            </button>
          </div>
        </div>

        <div class="rounded-xl border border-slate-800 bg-slate-900/60 p-6">
          <h3 class="mb-4 flex items-center gap-2 text-lg font-semibold"><MessageCircle size="20" /> Interactions</h3>

          <div class="mb-4 space-y-3 rounded-lg border border-slate-800 bg-slate-950/60 p-4">
            <select
              v-model="newInteraction.type"
              class="w-full rounded-md border border-slate-700 bg-slate-950 px-3 py-2 text-slate-100 focus:border-indigo-500 focus:outline-none"
            >
              <option value="">Select interaction type</option>
              <option value="email">Email</option>
              <option value="call">Call</option>
              <option value="meeting">Meeting</option>
              <option value="note">Note</option>
            </select>
            <textarea
              v-model="newInteraction.description"
              placeholder="Interaction details..."
              rows="2"
              class="w-full rounded-md border border-slate-700 bg-slate-950 px-3 py-2 text-slate-100 placeholder-slate-500 focus:border-indigo-500 focus:outline-none"
            ></textarea>
            <button @click="addInteraction" class="inline-flex w-full items-center justify-center gap-2 rounded-md bg-indigo-600 py-2 text-white hover:bg-indigo-500">
              <Plus size="18" /> Add Interaction
            </button>
          </div>

          <div v-if="interactions.length === 0" class="text-center text-sm text-slate-500">
            No interactions yet
          </div>

          <div v-else class="space-y-3">
            <div v-for="interaction in interactions" :key="interaction.id" class="rounded-lg border border-slate-800 bg-slate-950/60 p-4">
              <div class="flex items-center justify-between text-xs text-slate-500">
                <span class="capitalize text-indigo-300">{{ interaction.interaction_type }}</span>
                <span>{{ formatDate(interaction.created_at) }}</span>
              </div>
              <p class="mt-2 text-sm text-slate-200">{{ interaction.description }}</p>
              <button
                @click="deleteInteraction(interaction.id)"
                class="inline-flex items-center gap-1 text-xs text-rose-300 hover:text-rose-200"
              >
                <Trash size="14" /> Delete
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ArrowLeft, UserCheck, FileText, Edit, Save, Trash2, MessageCircle, Plus, Trash } from 'lucide-vue-next'
import { useLeadsStore } from '../stores/leads'
import { useToastStore } from '../stores/toast'

const router = useRouter()
const route = useRoute()
const leadsStore = useLeadsStore()
const toastStore = useToastStore()

const editForm = ref({
  status: '',
  notes: ''
})

const newInteraction = ref({
  type: '',
  description: ''
})

const interactions = ref([])

const formatDate = (date) => {
  return new Date(date).toLocaleDateString()
}

const updateLead = async () => {
  try {
    await leadsStore.updateLead(route.params.id, {
      status: editForm.value.status,
      notes: editForm.value.notes
    })
    toastStore.addToast('Lead updated successfully', 'success')
  } catch (error) {
    toastStore.addToast('Failed to update lead', 'error')
  }
}

const deleteLead = async () => {
  if (confirm('Are you sure you want to delete this lead?')) {
    try {
      await leadsStore.deleteLead(route.params.id)
      router.push('/leads')
    } catch (error) {
      alert('Failed to delete lead')
    }
  }
}

const addInteraction = async () => {
  if (!newInteraction.value.type || !newInteraction.value.description) {
    alert('Please fill in all fields')
    return
  }

  try {
    await leadsStore.currentLead.interactions?.push({
      interaction_type: newInteraction.value.type,
      description: newInteraction.value.description
    })

    await loadInteractions()
    newInteraction.value = { type: '', description: '' }
  } catch (error) {
    alert('Failed to add interaction')
  }
}

const deleteInteraction = async (id) => {
  if (confirm('Delete this interaction?')) {
    try {
      await leadsStore.leadsService?.deleteInteraction(id)
      await loadInteractions()
    } catch (error) {
      alert('Failed to delete interaction')
    }
  }
}

const loadInteractions = async () => {
  try {
    const response = await leadsStore.leadsService?.getInteractions(route.params.id)
    if (response?.data?.interactions) {
      interactions.value = response.data.interactions
    }
  } catch (error) {
    console.error('Failed to load interactions')
  }
}

onMounted(async () => {
  const leadId = route.params.id
  await leadsStore.getLead(leadId)

  if (leadsStore.currentLead) {
    editForm.value.status = leadsStore.currentLead.status
    editForm.value.notes = leadsStore.currentLead.notes || ''
  }

  await loadInteractions()
})
</script>
