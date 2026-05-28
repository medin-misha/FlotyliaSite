<script setup>
import { ref, markRaw, onMounted } from 'vue'
import { useAuthStore } from '../stores/auth.js'
import { usePageStore } from '../stores/page.js'
import { useStatesStore } from '../stores/states.js'

import { userSchema, userCreateSchema } from '../forms/userFrom.js'
import { adminSchema, adminCreateSchema } from '../forms/adminForm.js'

const authStore = useAuthStore()
const pageStore = usePageStore()
const statesStore = useStatesStore()

const menu = [
  {
    url: userSchema.endpoint,
    name: 'Users',
    icon: 'group',
    schema: markRaw(userSchema),
    createSchema: markRaw(userCreateSchema),
  },
  {
    url: adminSchema.endpoint,
    name: 'Admins',
    icon: 'shield_person',
    schema: markRaw(adminSchema),
    createSchema: markRaw(adminCreateSchema),
  },
]

const activeIndex = ref(pageStore.pageData.name === 'Admins' ? 1 : 0)

const setPage = (index) => {
  activeIndex.value = index
  const item = menu[index]
  pageStore.setPage(item.url, item.name, item.createSchema, item.schema)
  statesStore.setTableState()
}

// Dark Mode Toggle
const isDark = ref(false)
const toggleDarkMode = () => {
  isDark.value = !isDark.value
  const html = document.documentElement
  if (isDark.value) {
    html.classList.add('dark')
    html.classList.remove('light')
    localStorage.setItem('theme', 'dark')
  } else {
    html.classList.remove('dark')
    html.classList.add('light')
    localStorage.setItem('theme', 'light')
  }
}

onMounted(() => {
  isDark.value = document.documentElement.classList.contains('dark')
})
</script>

<template>
  <aside class="fixed left-0 top-0 z-50 flex h-full w-sidebar-width flex-col overflow-y-auto border-r border-outline-variant/30 bg-surface-container-lowest p-stack-md shadow-sm transition-colors duration-300 dark:border-white/10 dark:bg-inverse-surface/95 dark:shadow-none">
    <!-- Logo Section -->
    <div class="mb-10 flex items-center gap-3 px-2">
      <div class="w-10 h-10 rounded-xl bg-primary flex items-center justify-center text-on-primary">
        <span class="material-symbols-outlined" style="font-variation-settings: 'FILL' 1;">admin_panel_settings</span>
      </div>
      <div class="flex flex-col">
        <span class="font-headline-sm text-headline-sm font-bold text-primary dark:text-primary-fixed-dim">Flotylia</span>
        <span class="font-label-sm text-label-sm text-secondary">Admin Suite</span>
      </div>
    </div>

    <!-- Navigation Links -->
    <nav class="flex-grow space-y-2">
      <button
        v-for="(item, index) in menu"
        :key="index + item.name"
        @click="setPage(index)"
        :class="[
          'w-full flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-150 text-left',
          activeIndex === index
            ? 'bg-primary/10 text-primary font-bold dark:bg-primary-container/20 dark:text-inverse-primary'
            : 'text-secondary hover:bg-surface-container-high dark:text-secondary-fixed-dim dark:hover:bg-white/5'
        ]"
      >
        <span class="material-symbols-outlined">{{ item.icon }}</span>
        <span class="font-label-md text-label-md">{{ item.name }}</span>
      </button>
    </nav>

    <!-- Footer Area with Actions and Profile -->
    <div class="mt-auto space-y-2 pt-6 border-t border-outline-variant/30 dark:border-white/10">
      <!-- Dark mode switch -->
      <button
        @click="toggleDarkMode"
        class="w-full flex items-center gap-3 px-4 py-3 text-secondary dark:text-secondary-fixed-dim hover:bg-surface-container-high dark:hover:bg-white/5 rounded-xl transition-colors text-left"
      >
        <span class="material-symbols-outlined">{{ isDark ? 'light_mode' : 'dark_mode' }}</span>
        <span class="font-label-md text-label-md">{{ isDark ? 'Светлая тема' : 'Темная тема' }}</span>
      </button>

      <!-- Logout Button -->
      <button
        @click="authStore.logout()"
        class="w-full flex items-center gap-3 px-4 py-3 text-error dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-950/20 rounded-xl transition-colors text-left font-semibold"
      >
        <span class="material-symbols-outlined">logout</span>
        <span class="font-label-md text-label-md">Выйти</span>
      </button>

      <!-- Admin Profile Card -->
      <div class="flex items-center gap-3 p-3 mt-4 bg-surface-container-high dark:bg-white/5 rounded-2xl">
        <div class="overflow-hidden">
          <p class="truncate font-label-md text-label-md font-bold">{{ authStore.user || 'Admin' }}</p>
          <p class="text-[10px] uppercase tracking-wider opacity-60">Администратор</p>
        </div>
      </div>
    </div>
  </aside>
</template>

<style scoped>
/* Scoped overrides if any, but Tailwind handles most */
</style>
