<script setup>
import { computed, onBeforeUnmount, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { useRouter } from 'vue-router'
import { useLocaleStore } from '../../stores/localeStore'

const emit = defineEmits(['close'])

const router = useRouter()
const localeStore = useLocaleStore()
const { locale } = useI18n({ useScope: 'global' })

const navItems = [
  { labelKey: 'nav-bar.about', hash: '#about'},
  { labelKey: 'nav-bar.work-with-us', hash: '#work' },
  { labelKey: 'nav-bar.transport', hash: '#transport' },
  { labelKey: 'nav-bar.contacts', hash: '#contacts' },
]

const languages = [
  { value: 'ru', label: 'Рус.' },
  { value: 'cz', label: 'Čes.' },
  { value: 'en', label: 'Eng.' },
]

const selectedLang = computed({
  get: () => localeStore.locale,
  set: (value) => {
    localeStore.setLocale(value)
    locale.value = value
  },
})

let previousBodyOverflow = ''

const closeMenu = () => emit('close')

const handleKeydown = (event) => {
  if (event.key === 'Escape') {
    closeMenu()
  }
}

const navigateTo = async (hash) => {
  closeMenu()

  if (
    router.currentRoute.value.path !== '/' ||
    router.currentRoute.value.hash !== hash
  ) {
    await router.push({ path: '/', hash })
  }

  window.setTimeout(() => {
    const target = document.querySelector(hash)

    if (target instanceof HTMLElement) {
      target.scrollIntoView({ behavior: 'smooth', block: 'start' })
    }
  }, 120)
}

onMounted(() => {
  previousBodyOverflow = document.body.style.overflow
  document.body.style.overflow = 'hidden'
  window.addEventListener('keydown', handleKeydown)
})

onBeforeUnmount(() => {
  document.body.style.overflow = previousBodyOverflow
  window.removeEventListener('keydown', handleKeydown)
})
</script>

<template>
  <div class="mobile-nav-shell" @click.self="closeMenu">
    <aside class="mobile-nav-panel" aria-label="Mobile navigation">
      <div class="mobile-nav-head">
        <img src="/MiniLogo.svg" alt="MFS Logo" class="mobile-nav-logo" />

        <button
          type="button"
          class="mobile-nav-close app-fade-transition"
          aria-label="Close navigation"
          @click="closeMenu"
        >
          <span />
          <span />
        </button>
      </div>

      <nav class="mobile-nav-links">
        <button
          v-for="item in navItems"
          :key="item.hash"
          type="button"
          class="mobile-nav-link app-fade-transition"
          @click="navigateTo(item.hash)"
        >
          {{ $t(item.labelKey) }}
        </button>
      </nav>

      <div class="mobile-nav-language">
        <span>{{ $t('nav-bar.language') }}</span>

        <div class="mobile-nav-language-pill app-pill-button app-alt-button-text">
          <select v-model="selectedLang" class="mobile-nav-select">
            <option
              v-for="language in languages"
              :key="language.value"
              :value="language.value"
            >
              {{ language.label }}
            </option>
          </select>
        </div>
      </div>
    </aside>
  </div>
</template>

<style scoped>
.mobile-nav-shell {
  position: fixed;
  inset: 0;
  z-index: 50;
  background: color-mix(in srgb, var(--bg) 96%, transparent);
  backdrop-filter: blur(2px);
  animation: shell-fade-in 0.22s ease;
}

.mobile-nav-panel {
  min-height: 100dvh;
  width: 100%;
  background-color: var(--bg);
  padding: 28px 32px 36px;
  display: flex;
  flex-direction: column;
  animation: panel-slide-in 0.28s cubic-bezier(0.22, 1, 0.36, 1);
}

.mobile-nav-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 24px;
}

.mobile-nav-logo {
  width: clamp(92px, 24vw, 120px);
  height: auto;
}

.mobile-nav-close {
  width: 44px;
  height: 44px;
  border: none;
  background: transparent;
  display: grid;
  place-items: center;
  cursor: pointer;
  position: relative;
}

.mobile-nav-close:hover {
  opacity: 0.65;
}

.mobile-nav-close span {
  position: absolute;
  width: 28px;
  height: 2px;
  border-radius: 999px;
  background-color: var(--color-text);
}

.mobile-nav-close span:first-child {
  transform: rotate(45deg);
}

.mobile-nav-close span:last-child {
  transform: rotate(-45deg);
}

.mobile-nav-links {
  display: flex;
  flex-direction: column;
  gap: 26px;
  margin-top: clamp(72px, 14vh, 140px);
}

.mobile-nav-link {
  width: fit-content;
  border: none;
  background: transparent;
  padding: 0;
  text-align: left;
  font-weight: 400;
  font-size: clamp(26px, 8.5vw, 54px);
  line-height: 1.05;
  color: var(--color-text);
  cursor: pointer;
}

.mobile-nav-link:hover {
  opacity: 0.65;
}

.mobile-nav-language {
  margin-top: auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
  padding-top: 40px;
}

.mobile-nav-language span {
  font-weight: 400;
  font-size: clamp(24px, 7vw, 44px);
  line-height: 1;
  color: var(--color-text);
}

.mobile-nav-language-pill {
  min-width: 132px;
  padding: 0 18px;
  border-radius: 999px;
  background-color: var(--brand-color);
}

.mobile-nav-select {
  width: 100%;
  border: none;
  background: transparent;
  padding: 15px 0;
  font-size: clamp(18px, 5vw, 34px);
  color: var(--brand-text-color);
  text-align: center;
  cursor: pointer;
  outline: none;
  appearance: none;
  -webkit-appearance: none;
  -moz-appearance: none;
}

@keyframes shell-fade-in {
  from {
    opacity: 0;
  }

  to {
    opacity: 1;
  }
}

@keyframes panel-slide-in {
  from {
    opacity: 0;
    transform: translateX(-18px);
  }

  to {
    opacity: 1;
    transform: translateX(0);
  }
}
option {
  color: var(--brand-color);
}
</style>
