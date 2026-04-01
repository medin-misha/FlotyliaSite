<script setup>
import { ref } from 'vue'
import MobileNavBar from './mobileNavBar.vue'

const isMenuOpen = ref(false)

const openMenu = () => {
  isMenuOpen.value = true
}

const closeMenu = () => {
  isMenuOpen.value = false
}
</script>

<template>
  <header class="mobile-header">
    <button
      type="button"
      class="mobile-menu-button app-fade-transition"
      aria-label="Open navigation"
      @click="openMenu"
    >
      <span />
      <span />
      <span />
    </button>

    <button
      type="button"
      class="mobile-connect-button app-pill-button app-fade-transition app-alt-button-text"
      @click="$router.push('/select-platform')"
    >
      {{ $t('buttons.connect-button') }}
    </button>

    <img src="/fullRedLogo.svg" alt="MFS Logo" class="mobile-header-logo" />
  </header>

  <MobileNavBar v-if="isMenuOpen" @close="closeMenu" />
</template>

<style scoped>
.mobile-header {
  position: sticky;
  top: 0;
  z-index: 20;
  width: 100%;
  padding: 16px;
  display: grid;
  grid-template-columns: auto 1fr auto;
  align-items: center;
  gap: 12px;
  background-color: #fff;
}

.mobile-menu-button {
  width: 42px;
  height: 42px;
  border: none;
  background: transparent;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 5px;
  cursor: pointer;
}

.mobile-menu-button:hover {
  opacity: 0.65;
}

.mobile-menu-button span {
  width: 28px;
  height: 2px;
  border-radius: 999px;
  background-color: var(--color-text);
}

.mobile-connect-button {
  justify-self: center;
  width: 80%;
  max-width: 100%;
  padding: 14px 0px;
  background-color: var(--brand-color);
  color: var(--brand-text-color);
  font-size: clamp(16px, 4.6vw, 26px);
}

.mobile-connect-button:hover {
  opacity: 0.9;
}

.mobile-header-logo {
  width: clamp(32px, 16vw, 48px);
  height: auto;
}
</style>
