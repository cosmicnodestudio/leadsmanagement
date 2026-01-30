<template>
  <div class="min-h-screen bg-slate-950 text-slate-100">
    <nav class="sticky top-0 z-50 border-b border-slate-800 bg-slate-950/90 backdrop-blur">
      <div class="mx-auto flex max-w-6xl items-center justify-between px-6 py-4">
        <router-link to="/" class="flex items-center gap-2 text-lg font-semibold text-slate-100">
          <Briefcase size="28" class="text-indigo-500" /> Leads Manager
        </router-link>
        <div class="flex items-center gap-4 text-sm">
          <router-link
            v-if="authStore.isAuthenticated"
            to="/leads"
            class="inline-flex items-center gap-1 text-slate-300 hover:text-white"
          >
            <ListChecks size="16" /> Leads
          </router-link>
          <router-link
            v-if="authStore.isAuthenticated"
            to="/profile"
            class="inline-flex items-center gap-1 text-slate-300 hover:text-white"
          >
            <User size="16" /> Profile
          </router-link>
          <button
            v-if="authStore.isAuthenticated"
            @click="handleLogout"
            class="inline-flex items-center gap-2 rounded-md bg-rose-600 px-3 py-1.5 text-white hover:bg-rose-500"
          >
            <LogOut size="16" /> Logout
          </button>
          <router-link
            v-if="!authStore.isAuthenticated"
            to="/login"
            class="rounded-md bg-indigo-600 px-3 py-1.5 text-white hover:bg-indigo-500"
          >
            Login
          </router-link>
        </div>
      </div>
    </nav>

    <main class="mx-auto w-full max-w-6xl px-6 py-8">
      <router-view />
    </main>

    <ToastContainer />
  </div>
</template>

<script setup>
import { useAuthStore } from './stores/auth'
import { useRouter } from 'vue-router'
import { Briefcase, LogOut, ListChecks, User } from 'lucide-vue-next'
import ToastContainer from './components/ToastContainer.vue'

const authStore = useAuthStore()
const router = useRouter()

authStore.checkAuth()

const handleLogout = () => {
  authStore.logout()
  router.push('/login')
}
</script>
