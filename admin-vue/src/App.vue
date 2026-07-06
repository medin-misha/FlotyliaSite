<script setup>
import { computed, ref, provide, watch } from 'vue'
import sideBarComp from './components/sideBarComp.vue'
import headerComp from './components/headerComp.vue'
import bodyComp from './components/bodyComp.vue'
import loginComp from './components/loginComp.vue'
import { usePageStore } from './stores/page'
import { useAuthStore } from './stores/auth'

const pageStore = usePageStore()
const authStore = useAuthStore()

const isLoginPage = computed(() => !authStore.isLogin())

const sidebarCollapsed = ref(localStorage.getItem('sidebar-collapsed') === '1')
watch(sidebarCollapsed, (v) => localStorage.setItem('sidebar-collapsed', v ? '1' : '0'))
provide('sidebarCollapsed', sidebarCollapsed)
</script>

<template>
  <loginComp v-if="isLoginPage" />
  <div
    v-else
    class="min-h-screen w-full bg-background text-on-surface transition-colors duration-300 dark:bg-on-background dark:text-white"
  >
    <sideBarComp />

    <div
      class="min-h-screen min-w-0 transition-all duration-300"
      :class="sidebarCollapsed ? 'pl-16' : 'pl-[260px]'"
    >
      <headerComp :key="pageStore.pageData.adres" />
      <bodyComp />
    </div>
  </div>
</template>

<style scoped></style>
