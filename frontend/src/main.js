import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import './style.css'

const sanitizeToken = (key) => {
	const raw = localStorage.getItem(key)
	if (!raw) return
	const normalized = raw.trim().startsWith('Bearer ') ? raw.trim().slice(7) : raw.trim()
	if (!normalized || normalized === 'null' || normalized === 'undefined' || normalized.split('.').length !== 3) {
		localStorage.removeItem(key)
	}
}

sanitizeToken('access_token')
sanitizeToken('refresh_token')

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.mount('#app')

document.documentElement.classList.add('dark')
