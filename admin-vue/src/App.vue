<script setup>
import { computed } from 'vue'
import sideBarComp from './components/sideBarComp.vue'
import headerComp from './components/headerComp.vue'
import bodyComp from './components/bodyComp.vue'
import loginComp from './components/loginComp.vue'
import { usePageStore } from './stores/page'
import { useAuthStore } from './stores/auth'

const pageStore = usePageStore()
const authStore = useAuthStore()

const isLoginPage = computed(() => !authStore.isLogin())
</script>

<template>
  <loginComp v-if="isLoginPage" />
  <div
    v-else
    class="min-h-screen w-full bg-background text-on-surface transition-colors duration-300 dark:bg-on-background dark:text-white"
  >
    <sideBarComp />

    <div class="min-h-screen min-w-0 pl-sidebar-width">
      <headerComp :key="pageStore.pageData.adres" />
      <bodyComp />
    </div>
  </div>
</template>

<style scoped></style>
