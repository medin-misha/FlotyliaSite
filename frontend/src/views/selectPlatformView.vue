<script setup>
import selectPlatformComp from '../components/selectPlatformComp.vue'
import mSelectPlatform from '../components/mobile/mSelectPlatform.vue'
import { useUiStore } from '../stores/uiStore'

const uiStore = useUiStore()
</script>

<template>
  <div
    class="select-platform-view"
    :class="{ 'select-platform-view--mobile': uiStore.isMobile }"
  >
    <selectPlatformComp v-if="!uiStore.isMobile" />
    <mSelectPlatform v-else />
  </div>
</template>

<style scoped>
.select-platform-view {
  width: 100%;
  padding: 0 40px;
  box-sizing: border-box;
}

.select-platform-view--mobile {
  padding: 0;
}
</style>
