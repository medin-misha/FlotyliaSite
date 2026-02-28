<script setup>
import { RouterLink, RouterView } from 'vue-router'
import headerComp from './components/headerComp.vue'
import footerComp from './components/footerComp.vue'
</script>

<template>
  <div>
    <headerComp />
    <section>
      <RouterView />
    </section>
    <footerComp />
  </div>
</template>

<style scoped>
div {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

section {
  flex: 1;
}
</style>
