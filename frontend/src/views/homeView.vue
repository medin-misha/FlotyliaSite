<script setup>
import homeLeftComp from '../components/homeLeftComp.vue'
import homeRightComp from '../components/homeRightComp.vue'
</script>

<template>
  <div class="home">
    <div class="home-content">
      <homeLeftComp />
      <homeRightComp />
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
</style>