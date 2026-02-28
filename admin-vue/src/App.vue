<script setup>
import sideBarComp from './components/sideBarComp.vue'
import headerComp from './components/headerComp.vue'
import bodyComp from './components/bodyComp.vue'
import loginComp from './components/loginComp.vue'
import { useAuthStore } from './stores/auth'
import { usePageStore } from './stores/page'

const isLogin = useAuthStore().isLogin()
const pageStore = usePageStore()
</script>

<template>
  <loginComp v-if="!isLogin" />
  <div v-else class="container">
    <sideBarComp />
    <main>
      <headerComp :key="pageStore.pageData.adres" />
      <bodyComp />
    </main>
  </div>
</template>

<style scoped>
.container {
  height: 100dvh;
  display: flex;
  flex-direction: row;
}
main {
  display: flex;
  flex-direction: column;
  width: 100%;
}
</style>
