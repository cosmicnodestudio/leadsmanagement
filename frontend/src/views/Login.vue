<template>
  <div class="flex min-h-[calc(100vh-72px)] items-center justify-center">
    <div class="w-full max-w-md rounded-xl border border-slate-800 bg-slate-900/70 p-8 shadow-xl">
      <div class="mb-6 flex justify-center">
        <LogIn size="32" class="text-indigo-500" />
      </div>
      <h1 class="mb-6 text-center text-2xl font-semibold">Login</h1>

      <div v-if="error" class="mb-4 rounded-md border border-rose-500/40 bg-rose-500/10 px-4 py-3 text-sm text-rose-200">
        {{ error }}
      </div>

      <form @submit.prevent="handleLogin" class="space-y-4">
        <div>
          <label for="email" class="mb-1 flex items-center gap-2 text-sm text-slate-300">
            <Mail size="16" /> Email
          </label>
          <input
            id="email"
            v-model="form.email"
            type="email"
            required
            :disabled="loading"
            placeholder="your@email.com"
            class="w-full rounded-md border border-slate-700 bg-slate-950 px-3 py-2 text-slate-100 placeholder-slate-500 focus:border-indigo-500 focus:outline-none"
          />
        </div>

        <div>
          <label for="password" class="mb-1 flex items-center gap-2 text-sm text-slate-300">
            <Lock size="16" /> Password
          </label>
          <input
            id="password"
            v-model="form.password"
            type="password"
            required
            :disabled="loading"
            placeholder="••••••••"
            class="w-full rounded-md border border-slate-700 bg-slate-950 px-3 py-2 text-slate-100 placeholder-slate-500 focus:border-indigo-500 focus:outline-none"
          />
        </div>

        <button
          type="submit"
          class="inline-flex w-full items-center justify-center gap-2 rounded-md bg-indigo-600 py-2 text-white hover:bg-indigo-500 disabled:cursor-not-allowed disabled:opacity-60"
          :disabled="loading"
        >
          <LogIn size="18" />
          {{ loading ? 'Logging in...' : 'Login' }}
        </button>
      </form>

      <p class="mt-6 text-center text-sm text-slate-400">
        Don't have an account?
        <router-link to="/register" class="text-indigo-400 hover:text-indigo-300">Register here</router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { LogIn, Mail, Lock } from 'lucide-vue-next'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const form = reactive({
  email: '',
  password: ''
})

const loading = ref(false)
const error = ref(null)

const handleLogin = async () => {
  loading.value = true
  error.value = null

  try {
    await authStore.login(form.email, form.password)
    router.push('/')
  } catch (err) {
    error.value = err
  } finally {
    loading.value = false
  }
}
</script>
