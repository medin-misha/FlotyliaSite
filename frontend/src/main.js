import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { createI18n, useI18n } from "vue-i18n"
import { defaultLocale, locales } from "./i18n"
import { useLocaleStore } from "./stores/localeStore"

import App from './App.vue'
import router from './router'
const pinia = createPinia()
const localeStore = useLocaleStore(pinia)
const i18n = createI18n({
    legacy: false, // для работы с компонентами на Vue 3 Composition API
    fallbackLocale: defaultLocale, // Если передали что то непонятное, то используем русский язык
    locale: localeStore.locale, // Язык по умолчанию
    messages: Object.assign(locales)
})
const app = createApp(App, {
    setup() {
        const { t } = useI18n()
        return { t }
    }
})

app.use(pinia)
app.use(router)
app.use(i18n)

app.mount('#app')
