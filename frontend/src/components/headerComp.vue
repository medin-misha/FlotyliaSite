<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { RouterLink } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { useLocaleStore } from '@/stores/localeStore'
import { useThemeStore } from '@/stores/themeStore'
import LogoComp from '@/components/LogoComp.vue'

const scrolled = ref(false)

function onScroll() {
  scrolled.value = window.scrollY > 6
}

onMounted(() => {
  window.addEventListener('scroll', onScroll, { passive: true })
  onScroll()
})
onUnmounted(() => {
  window.removeEventListener('scroll', onScroll)
})

const { locale } = useI18n({ useScope: 'global' })
const localeStore = useLocaleStore()

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

const themeStore = useThemeStore()
const isDark = computed(() => themeStore.theme === 'dark')
</script>

<template>
  <header class="header" :class="{ scrolled }">
    <div class="container header-inner">
      <RouterLink to="/" class="brandmark" aria-label="MFS Fleet">
        <span class="glyph">
          <LogoComp style="width:70px;height:auto" />
        </span>
        <span class="brand-text">
          Fleet <span class="sub">· {{ $t('brand.country') }}</span>
        </span>
      </RouterLink>

      <div class="header-actions">
        <div class="lang-switcher" role="group" :aria-label="$t('nav-bar.language')">
          <button
            v-for="lang in languages"
            :key="lang.value"
            type="button"
            class="lang-btn"
            :class="{ active: selectedLang === lang.value }"
            @click="selectedLang = lang.value"
          >
            {{ lang.label }}
          </button>
        </div>

        <button type="button" class="theme-btn" :aria-label="isDark ? 'Switch to light theme' : 'Switch to dark theme'" @click="themeStore.toggleTheme()">
          <!-- sun -->
          <svg v-if="isDark" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M4.93 19.07l1.41-1.41M17.66 6.34l1.41-1.41"/></svg>
          <!-- moon -->
          <svg v-else width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>
        </button>

        <RouterLink to="/form" class="btn btn-primary btn-sm">
          {{ $t('buttons.connect-button') }}
        </RouterLink>
      </div>
    </div>
  </header>
</template>

<style scoped>
.header {
  position: sticky;
  top: 0;
  z-index: 50;
  background: color-mix(in srgb, var(--bg) 78%, transparent);
  backdrop-filter: blur(14px) saturate(160%);
  -webkit-backdrop-filter: blur(14px) saturate(160%);
  border-bottom: 1px solid transparent;
  transition: border-color var(--t-base), background-color var(--t-base);
}
.header.scrolled {
  border-bottom-color: var(--border);
}

.header-inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  height: 64px;
}

.brandmark {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  font-family: var(--font-alt);
  font-weight: 800;
  font-size: 17px;
  letter-spacing: -.01em;
  color: var(--text);
  text-decoration: none;
}

.glyph {
  height: 38px;
  border-radius: 8px;
  background: var(--accent);
  color: #fff;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 6px 4px;
  transition: background-color var(--t-fast);
}

.sub {
  color: var(--text-3);
  font-weight: 500;
  font-family: var(--font-sans);
  font-size: 13px;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-shrink: 0;
}

.lang-switcher {
  display: flex;
  align-items: center;
  gap: 2px;
  background: var(--surface-2, rgba(0,0,0,.06));
  border-radius: 8px;
  padding: 3px;
}

.lang-btn {
  border: none;
  background: transparent;
  padding: 4px 9px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 600;
  letter-spacing: .03em;
  color: var(--text-3);
  cursor: pointer;
  transition: background-color var(--t-fast), color var(--t-fast);
  line-height: 1.6;
}

.lang-btn:hover:not(.active) {
  color: var(--text);
}

.lang-btn.active {
  background: var(--bg);
  color: var(--text);
  box-shadow: 0 1px 3px rgba(0,0,0,.12);
}

.theme-btn {
  width: 40px;
  height: 40px;
  border-radius: 8px;
  background: var(--surface-2);
  border: 1px solid var(--border);
  display: grid;
  place-items: center;
  color: var(--text-2);
  cursor: pointer;
  transition: background-color var(--t-fast), color var(--t-fast), border-color var(--t-fast);
  flex-shrink: 0;
}
.theme-btn:hover {
  background: var(--surface-3);
  color: var(--text);
}

@media (max-width: 560px) {
  .header-actions .btn { display: none; }
}

@media (max-width: 480px) {
  .sub { display: none; }
  .lang-btn { padding: 5px 8px; }
}
</style>
