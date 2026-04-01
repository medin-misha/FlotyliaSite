<script setup>
import MBodyComp from '@/components/mobile/mBodyComp.vue'
import homeLeftComp from '../components/homeLeftComp.vue'
import homeRightComp from '../components/homeRightComp.vue'
import { useUiStore } from '../stores/uiStore'

const uiStore = useUiStore()
</script>

<template>
  <div class="home" :class="{ 'home--mobile': uiStore.isMobile }">
    <div class="home-content" :class="{ 'home-content--mobile': uiStore.isMobile }">
      <template v-if="!uiStore.isMobile">
        <homeLeftComp />
        <homeRightComp />
      </template>
      <template v-else>
        <MBodyComp />
      </template>
    </div>
  </div>
</template>

<style scoped>
.home {
  width: 100%;
  padding: 0 40px;
  box-sizing: border-box;
}

.home-content {
  max-width: 1400px;
  margin: 0 auto;
  display: flex;
  gap: 60px;
  justify-content: space-between;
  padding: 40px 0;
}

.home--mobile {
  padding: 0;
}

.home-content--mobile {
  max-width: none;
  display: block;
  padding: 0;
}
</style>
