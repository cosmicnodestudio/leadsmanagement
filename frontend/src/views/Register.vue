<template>
  <div class="flex min-h-[calc(100vh-72px)] items-center justify-center">
    <div class="w-full max-w-md rounded-xl border border-slate-800 bg-slate-900/70 p-8 shadow-xl">
      <div class="mb-6 flex justify-center">
        <UserPlus size="32" class="text-emerald-500" />
      </div>
      <h1 class="mb-6 text-center text-2xl font-semibold">Create Account</h1>

      <div v-if="error" class="mb-4 rounded-md border border-rose-500/40 bg-rose-500/10 px-4 py-3 text-sm text-rose-200">
        {{ error }}
      </div>

      <form @submit.prevent="handleRegister" class="space-y-4">
        <div>
          <label for="name" class="mb-1 flex items-center gap-2 text-sm text-slate-300">
            <User size="16" /> Full Name
          </label>
          <input
            id="name"
            v-model="form.name"
            type="text"
            required
            :disabled="loading"
            placeholder="John Doe"
            class="w-full rounded-md border border-slate-700 bg-slate-950 px-3 py-2 text-slate-100 placeholder-slate-500 focus:border-indigo-500 focus:outline-none"
          />
        </div>

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
          class="inline-flex w-full items-center justify-center gap-2 rounded-md bg-emerald-600 py-2 text-white hover:bg-emerald-500 disabled:cursor-not-allowed disabled:opacity-60"
          :disabled="loading"
        >
          <UserPlus size="18" />
          {{ loading ? 'Creating account...' : 'Register' }}
        </button>
      </form>

      <p class="mt-6 text-center text-sm text-slate-400">
        Already have an account?
        <router-link to="/login" class="text-indigo-400 hover:text-indigo-300">Login here</router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { UserPlus, User, Mail, Lock } from 'lucide-vue-next'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const form = reactive({
  name: '',
  email: '',
  password: ''
})

const loading = ref(false)
const error = ref(null)

const handleRegister = async () => {
  loading.value = true
  error.value = null

  try {
    await authStore.register(form.email, form.name, form.password)
    router.push('/login')
  } catch (err) {
    error.value = err
  } finally {
    loading.value = false
  }
}
</script>
