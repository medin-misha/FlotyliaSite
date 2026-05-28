<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { RouterLink } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { useLocaleStore } from '@/stores/localeStore'
import { useThemeStore } from '@/stores/themeStore'

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
          <svg fill="currentColor" aria-hidden="true" viewBox="0 19 78 31" style="width:70px;height:auto">
            <path d="M36.917 35.4791L37.782 30.2397H49.535L48.67 35.4791H36.917Z"/>
            <path d="M53.8181 29.4093H53.6709L53.6919 29.2729L53.8181 29.4093Z"/>
            <path d="M70.7841 39.9395L70.7809 39.9679L70.7554 39.9395H70.7841Z"/>
            <path d="M70.8437 40.0365H70.7673L70.7795 39.9668L70.8437 40.0365Z"/>
            <path d="M54.5569 19.3517H38.8032L38.8092 19.3184H34.9646L29.438 24.5426L25.23 50.0002H33.7391L37.9381 24.5911H53.6919L54.5569 19.3517Z"/>
            <path d="M60.9367 29.2728L61.7476 24.3637H69.2686L70.0976 19.3516H55.332L53.692 29.2728L53.8182 29.4091L63.6189 39.9394H63.5378L62.7028 44.9879H54.7072L55.5392 39.9394H48.2946L46.6306 50H69.1184L70.7794 39.9667L70.7554 39.9394L60.9367 29.2728Z"/>
            <path d="M70.9145 19.3516L69.2505 29.4091H76.3389L77.9999 19.3516H70.9145Z"/>
            <path d="M19.319 34.1184L9.15792 19.3184H5.07004L0 50.0002H8.6413L11.4316 33.0487L16.772 40.0881H20.3372L27.2245 33.0002L28.4709 25.4608L19.319 34.1184Z"/>
          </svg>
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

        <RouterLink to="/select-platform" class="btn btn-primary btn-sm">
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
  width: 34px;
  height: 34px;
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

@media (max-width: 480px) {
  .sub { display: none; }
  .lang-btn { padding: 4px 7px; }
}
</style>
