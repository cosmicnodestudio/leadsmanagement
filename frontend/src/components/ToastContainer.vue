<template>
  <div class="pointer-events-none fixed right-6 top-6 z-[60] flex flex-col gap-3">
    <div
      v-for="toast in toastStore.toasts"
      :key="toast.id"
      class="pointer-events-auto flex items-start gap-3 rounded-lg border px-4 py-3 text-sm shadow-lg"
      :class="toastClasses(toast.type)"
    >
      <span class="font-medium">{{ labelFor(toast.type) }}</span>
      <span class="text-slate-200">{{ toast.message }}</span>
      <button
        class="ml-auto text-slate-300 hover:text-white"
        @click="toastStore.removeToast(toast.id)"
      >
        ✕
      </button>
    </div>
  </div>
</template>

<script setup>
import { useToastStore } from '../stores/toast'

const toastStore = useToastStore()

const toastClasses = (type) => {
  switch (type) {
    case 'success':
      return 'border-emerald-500/40 bg-emerald-500/10 text-emerald-100'
    case 'error':
      return 'border-rose-500/40 bg-rose-500/10 text-rose-100'
    case 'warning':
      return 'border-amber-500/40 bg-amber-500/10 text-amber-100'
    default:
      return 'border-slate-700 bg-slate-900/80 text-slate-100'
  }
}

const labelFor = (type) => {
  switch (type) {
    case 'success':
      return 'Success'
    case 'error':
      return 'Error'
    case 'warning':
      return 'Warning'
    default:
      return 'Info'
  }
}
</script>
