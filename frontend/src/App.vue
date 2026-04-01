<script setup>
import { RouterLink, RouterView } from 'vue-router'
import headerComp from './components/headerComp.vue'
import footerComp from './components/footerComp.vue'
import mHeaderComp from './components/mobile/mHeaderComp.vue'
import mFooterComp from './components/mobile/mFooterComp.vue'
import { useUiStore } from './stores/uiStore'
const uiStore = useUiStore()
</script>

<template>
  <div>
    <headerComp v-if="!uiStore.isMobile" />
    <mHeaderComp v-else />
    <section>
      <RouterView />
    </section>
    <footerComp v-if="!uiStore.isMobile" />
    <mFooterComp v-else />
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
