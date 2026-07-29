<script setup>
import { ref, markRaw, onMounted, inject } from 'vue'
import { useAuthStore } from '../stores/auth.js'
import { usePageStore } from '../stores/page.js'
import { useStatesStore } from '../stores/states.js'

import { userSchema, userCreateSchema } from '../forms/userFrom.js'
import { adminSchema, adminCreateSchema } from '../forms/adminForm.js'
import { receiptSchema, receiptCreateSchema } from '../forms/receiptForm.js'
import { receiptStatsSchema } from '../forms/receiptStatsForm.js'

const authStore = useAuthStore()
const pageStore = usePageStore()
const statesStore = useStatesStore()

const sidebarCollapsed = inject('sidebarCollapsed')

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
  {
    url: receiptSchema.endpoint,
    name: 'Чеки',
    icon: 'receipt_long',
    schema: markRaw(receiptSchema),
    createSchema: markRaw(receiptCreateSchema),
  },
  {
    url: receiptStatsSchema.endpoint,
    name: 'Статистика',
    icon: 'bar_chart',
    schema: markRaw(receiptStatsSchema),
    createSchema: null,
    view: 'stats',
  },
]

const activeIndex = ref(pageStore.pageData.name === 'Admins' ? 1 : 0)

const setPage = (index) => {
  activeIndex.value = index
  const item = menu[index]
  pageStore.setPage(item.url, item.name, item.createSchema, item.schema, item.view || 'crud')
  statesStore.setTableState()
}

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
  <aside
    class="fixed left-0 top-0 z-50 flex h-full flex-col overflow-y-auto overflow-x-hidden border-r border-outline-variant/30 bg-surface-container-lowest shadow-sm transition-all duration-300 dark:border-white/10 dark:bg-inverse-surface/95 dark:shadow-none"
    :class="sidebarCollapsed ? 'w-16 p-2' : 'w-[260px] p-stack-md'"
  >
    <!-- Logo + Toggle -->
    <div
      class="mb-6 flex items-center"
      :class="sidebarCollapsed ? 'justify-center' : 'justify-between px-2'"
    >
      <div v-if="!sidebarCollapsed" class="flex items-center gap-3">
        <div class="w-10 h-10 rounded-xl bg-primary flex items-center justify-center text-on-primary shrink-0">
          <span class="material-symbols-outlined" style="font-variation-settings: 'FILL' 1">admin_panel_settings</span>
        </div>
        <div class="flex flex-col">
          <span class="font-headline-sm text-headline-sm font-bold text-primary dark:text-primary-fixed-dim">Flotylia</span>
          <span class="font-label-sm text-label-sm text-secondary">Admin Suite</span>
        </div>
      </div>

      <button
        @click="sidebarCollapsed = !sidebarCollapsed"
        class="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl transition-colors hover:bg-surface-container-high dark:hover:bg-white/5 text-secondary dark:text-secondary-fixed-dim"
        :title="sidebarCollapsed ? 'Развернуть меню' : 'Свернуть меню'"
      >
        <span class="material-symbols-outlined text-[20px] transition-transform duration-300" :class="sidebarCollapsed ? 'rotate-180' : ''">
          chevron_left
        </span>
      </button>
    </div>

    <!-- Navigation Links -->
    <nav class="flex-grow space-y-1">
      <button
        v-for="(item, index) in menu"
        :key="index + item.name"
        @click="setPage(index)"
        :title="sidebarCollapsed ? item.name : ''"
        :class="[
          'w-full flex items-center gap-3 py-3 rounded-xl transition-all duration-150 text-left',
          sidebarCollapsed ? 'justify-center px-2' : 'px-4',
          activeIndex === index
            ? 'bg-primary/10 text-primary font-bold dark:bg-primary-container/20 dark:text-inverse-primary'
            : 'text-secondary hover:bg-surface-container-high dark:text-secondary-fixed-dim dark:hover:bg-white/5',
        ]"
      >
        <span class="material-symbols-outlined shrink-0">{{ item.icon }}</span>
        <span v-if="!sidebarCollapsed" class="font-label-md text-label-md">{{ item.name }}</span>
      </button>
    </nav>

    <!-- Footer -->
    <div
      class="mt-auto space-y-1 pt-4 border-t border-outline-variant/30 dark:border-white/10"
    >
      <!-- Dark mode -->
      <button
        @click="toggleDarkMode"
        :title="sidebarCollapsed ? (isDark ? 'Светлая тема' : 'Тёмная тема') : ''"
        :class="[
          'w-full flex items-center gap-3 py-3 text-secondary dark:text-secondary-fixed-dim hover:bg-surface-container-high dark:hover:bg-white/5 rounded-xl transition-colors text-left',
          sidebarCollapsed ? 'justify-center px-2' : 'px-4',
        ]"
      >
        <span class="material-symbols-outlined shrink-0">{{ isDark ? 'light_mode' : 'dark_mode' }}</span>
        <span v-if="!sidebarCollapsed" class="font-label-md text-label-md">{{ isDark ? 'Светлая тема' : 'Темная тема' }}</span>
      </button>

      <!-- Logout -->
      <button
        @click="authStore.logout()"
        :title="sidebarCollapsed ? 'Выйти' : ''"
        :class="[
          'w-full flex items-center gap-3 py-3 text-error dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-950/20 rounded-xl transition-colors text-left font-semibold',
          sidebarCollapsed ? 'justify-center px-2' : 'px-4',
        ]"
      >
        <span class="material-symbols-outlined shrink-0">logout</span>
        <span v-if="!sidebarCollapsed" class="font-label-md text-label-md">Выйти</span>
      </button>

      <!-- Profile card -->
      <div
        v-if="!sidebarCollapsed"
        class="flex items-center gap-3 p-3 mt-2 bg-surface-container-high dark:bg-white/5 rounded-2xl"
      >
        <div class="overflow-hidden">
          <p class="truncate font-label-md text-label-md font-bold">{{ authStore.user || 'Admin' }}</p>
          <p class="text-[10px] uppercase tracking-wider opacity-60">Администратор</p>
        </div>
      </div>
      <div
        v-else
        class="flex justify-center mt-2"
        :title="authStore.user || 'Admin'"
      >
        <div class="w-9 h-9 rounded-xl bg-surface-container-high dark:bg-white/5 flex items-center justify-center">
          <span class="material-symbols-outlined text-[18px] text-secondary dark:text-secondary-fixed-dim">account_circle</span>
        </div>
      </div>
    </div>
  </aside>
</template>

<style scoped></style>
