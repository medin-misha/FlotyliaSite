<script setup>
import { ref, computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { useLocaleStore } from '../../stores/localeStore'
import { useThemeStore } from '../../stores/themeStore'
import MobileNavBar from './mobileNavBar.vue'

const isMenuOpen = ref(false)
const openMenu = () => { isMenuOpen.value = true }
const closeMenu = () => { isMenuOpen.value = false }

const { locale } = useI18n({ useScope: 'global' })
const localeStore = useLocaleStore()
const themeStore = useThemeStore()

const languages = [
  { value: 'ru', label: 'RU' },
  { value: 'cz', label: 'CZ' },
  { value: 'en', label: 'EN' },
]

const selectedLang = computed({
  get: () => localeStore.locale,
  set: (value) => {
    localeStore.setLocale(value)
    locale.value = value
  },
})

const isDark = computed(() => themeStore.theme === 'dark')
</script>

<template>
  <div>
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
      @click="$router.push('/form')"
    >
      {{ $t('buttons.connect-button') }}
    </button>

    <div class="mobile-header-controls">
      <div class="mobile-lang-switcher" role="group" :aria-label="$t('nav-bar.language')">
        <button
          v-for="lang in languages"
          :key="lang.value"
          type="button"
          class="mobile-lang-btn app-fade-transition"
          :class="{ active: selectedLang === lang.value }"
          @click="selectedLang = lang.value"
        >
          {{ lang.label }}
        </button>
      </div>

      <button
        type="button"
        class="mobile-theme-btn app-fade-transition"
        :aria-label="isDark ? 'Switch to light mode' : 'Switch to dark mode'"
        @click="themeStore.toggleTheme()"
      >
        <svg v-if="isDark" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
          <circle cx="12" cy="12" r="5"/>
          <line x1="12" y1="1" x2="12" y2="3"/>
          <line x1="12" y1="21" x2="12" y2="23"/>
          <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/>
          <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/>
          <line x1="1" y1="12" x2="3" y2="12"/>
          <line x1="21" y1="12" x2="23" y2="12"/>
          <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/>
          <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/>
        </svg>
        <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
          <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>
        </svg>
      </button>

      <img src="/fullRedLogo.svg" alt="MFS Logo" class="mobile-header-logo" />
    </div>
  </header>

  <MobileNavBar v-if="isMenuOpen" @close="closeMenu" />
  </div>
</template>

<style scoped>
.mobile-header {
  position: sticky;
  top: 0;
  z-index: 20;
  width: 100%;
  padding: 12px 16px;
  display: grid;
  grid-template-columns: auto 1fr auto;
  align-items: center;
  gap: 10px;
  background-color: var(--bg);
  border-bottom: 1px solid var(--border);
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
  background-color: var(--text);
}

.mobile-connect-button {
  justify-self: center;
  width: 80%;
  max-width: 100%;
  padding: 12px 0;
  background-color: var(--accent);
  color: var(--on-accent);
  font-size: clamp(14px, 4vw, 22px);
}

.mobile-connect-button:hover {
  opacity: 0.9;
}

.mobile-header-controls {
  display: flex;
  align-items: center;
  gap: 6px;
}

.mobile-lang-switcher {
  display: flex;
  align-items: center;
  gap: 1px;
  background: var(--surface-2);
  border-radius: 6px;
  padding: 2px;
}

.mobile-lang-btn {
  border: none;
  background: transparent;
  padding: 4px 6px;
  border-radius: 5px;
  font-size: 10px;
  font-weight: 700;
  letter-spacing: .04em;
  color: var(--text-3);
  cursor: pointer;
  line-height: 1.6;
}

.mobile-lang-btn:hover:not(.active) {
  color: var(--text);
}

.mobile-lang-btn.active {
  background: var(--bg);
  color: var(--text);
  box-shadow: 0 1px 3px rgba(0, 0, 0, .12);
}

.mobile-theme-btn {
  width: 32px;
  height: 32px;
  border: none;
  background: transparent;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: var(--text-3);
  padding: 0;
  border-radius: 6px;
}

.mobile-theme-btn:hover {
  color: var(--text);
  background: var(--surface-2);
}

.mobile-theme-btn svg {
  width: 17px;
  height: 17px;
}

.mobile-header-logo {
  width: clamp(28px, 12vw, 40px);
  height: auto;
}
</style>
