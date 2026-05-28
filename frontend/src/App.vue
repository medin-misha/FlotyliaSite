<script setup>
import { onMounted } from 'vue'
import { RouterView } from 'vue-router'
import headerComp from './components/headerComp.vue'
import footerComp from './components/footerComp.vue'
import { useThemeStore } from './stores/themeStore'

const themeStore = useThemeStore()
onMounted(() => {
  document.documentElement.setAttribute('data-theme', themeStore.theme)
})
</script>

<template>
  <div class="app-shell">
    <headerComp />
    <main class="app-main">
      <RouterView />
    </main>
    <footerComp />
  </div>
</template>

<style scoped>
.app-shell {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.app-main {
  flex: 1;
}
</style>
