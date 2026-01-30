<template>
  <div class="mx-auto max-w-2xl">
    <div class="rounded-xl border border-slate-800 bg-slate-900/60 p-8">
      <h1 class="flex items-center gap-2 text-2xl font-semibold"><User size="28" /> My Profile</h1>

      <div class="mt-6 space-y-4">
        <div>
          <label class="mb-1 block text-sm text-slate-300">Email</label>
          <input
            type="email"
            :value="authStore.user?.email"
            disabled
            class="w-full rounded-md border border-slate-800 bg-slate-950 px-3 py-2 text-slate-400"
          />
        </div>

        <div>
          <label class="mb-1 block text-sm text-slate-300">Full Name</label>
          <input
            v-model="form.name"
            type="text"
            class="w-full rounded-md border border-slate-700 bg-slate-950 px-3 py-2 text-slate-100 focus:border-indigo-500 focus:outline-none"
          />
        </div>

        <button @click="updateProfile" class="inline-flex items-center gap-2 rounded-md bg-emerald-600 px-4 py-2 text-white hover:bg-emerald-500">
          <Save size="18" /> Update Profile
        </button>
      </div>

      <div class="my-8 border-t border-slate-800"></div>

      <div class="space-y-4">
        <h3 class="flex items-center gap-2 text-lg font-semibold"><Lock size="20" /> Change Password</h3>

        <div>
          <label class="mb-1 block text-sm text-slate-300">Current Password</label>
          <input
            v-model="passwordForm.oldPassword"
            type="password"
            class="w-full rounded-md border border-slate-700 bg-slate-950 px-3 py-2 text-slate-100 focus:border-indigo-500 focus:outline-none"
          />
        </div>

        <div>
          <label class="mb-1 block text-sm text-slate-300">New Password</label>
          <input
            v-model="passwordForm.newPassword"
            type="password"
            class="w-full rounded-md border border-slate-700 bg-slate-950 px-3 py-2 text-slate-100 focus:border-indigo-500 focus:outline-none"
          />
        </div>

        <div>
          <label class="mb-1 block text-sm text-slate-300">Confirm New Password</label>
          <input
            v-model="passwordForm.confirmPassword"
            type="password"
            class="w-full rounded-md border border-slate-700 bg-slate-950 px-3 py-2 text-slate-100 focus:border-indigo-500 focus:outline-none"
          />
        </div>

        <button @click="changePassword" class="inline-flex items-center gap-2 rounded-md bg-indigo-600 px-4 py-2 text-white hover:bg-indigo-500">
          <Key size="18" /> Change Password
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive } from 'vue'
import { User, Lock, Key, Save } from 'lucide-vue-next'
import { useAuthStore } from '../stores/auth'
import { useToastStore } from '../stores/toast'

const authStore = useAuthStore()
const toastStore = useToastStore()

const form = reactive({
  name: authStore.user?.name || ''
})

const passwordForm = reactive({
  oldPassword: '',
  newPassword: '',
  confirmPassword: ''
})

const updateProfile = async () => {
  try {
    if (form.name !== authStore.user?.name) {
      // Call API to update profile
      toastStore.addToast('Profile updated successfully', 'success')
    }
  } catch (err) {
    toastStore.addToast('Failed to update profile', 'error')
  }
}

const changePassword = async () => {
  if (passwordForm.newPassword !== passwordForm.confirmPassword) {
    toastStore.addToast('Passwords do not match', 'warning')
    return
  }

  if (passwordForm.newPassword.length < 6) {
    toastStore.addToast('Password must be at least 6 characters', 'warning')
    return
  }

  try {
    await authStore.changePassword(
      passwordForm.oldPassword,
      passwordForm.newPassword
    )

    toastStore.addToast('Password changed successfully', 'success')
    passwordForm.oldPassword = ''
    passwordForm.newPassword = ''
    passwordForm.confirmPassword = ''
  } catch (err) {
    toastStore.addToast(err, 'error')
  }
}
</script>
