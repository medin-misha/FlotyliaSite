import { defineStore } from 'pinia'

export const useThemeStore = defineStore('theme', {
  state: () => ({
    theme: localStorage.getItem('theme') || 'light',
  }),
  actions: {
    toggleTheme() {
      const next = this.theme === 'dark' ? 'light' : 'dark'
      this.theme = next
      localStorage.setItem('theme', next)
      document.documentElement.setAttribute('data-theme', next)
    },
  },
})
