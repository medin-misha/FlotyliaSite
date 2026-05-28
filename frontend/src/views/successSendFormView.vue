<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { useI18n } from "vue-i18n"

const route = useRoute()
const { t } = useI18n({ useScope: "global" })

const company = computed(() => String(route.params.company || '').toLowerCase())
const isBolt = computed(() => company.value === 'bolt')
const isFoodora = computed(() => company.value === 'foodora')
const files = computed(() => isBolt.value
  ? [
      '/BoltGuide.zip',
    ]
  : [
      '/FoodoraGuide.zip'
    ])

const accentColor = computed(() => {
  if (isBolt.value) return 'var(--bolt-color)'
  if (isFoodora.value) return 'var(--foodora-color)'
  return 'var(--brand-color)'
})

const downloadAll = () => {
  files.value.forEach((url) => {
    const a = document.createElement('a')
    a.href = url
    a.download = ''          // пусть браузер возьмёт имя из URL; можно задать своё
    a.style.display = 'none'
    document.body.appendChild(a)
    a.click()
    a.remove()
  })
}


const instructionHeading = computed(() => t('success.instructions.heading'))
</script>

<template>
  <div class="success-page" :style="{ '--accent-color': accentColor }">
    <div class="success-container">

      <div class="check-big" aria-hidden="true">
        <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5"/></svg>
      </div>

      <h2 class="success-title">
        {{ $t("success.title") }}
      </h2>

      <div class="step-block">
        <p class="step-heading">
          <strong>{{ $t("success.step.label") }}</strong>
          {{ $t("success.step.description") }}
        </p>
        <p class="step-subtitle">
          {{ $t("success.step.subtitle") }}
        </p>
      </div>

      <button type="button" class="cta-button" @click="downloadAll()">
        {{ $t("success.cta") }}
      </button>

      <div class="instructions">
        <p class="instructions-heading">{{ instructionHeading }}</p>
      </div>

    </div>
  </div>
</template>

<style scoped>
.success-page {
  width: 100%;
  display: flex;
  justify-content: center;
  padding: clamp(40px, 7vw, 80px) var(--gutter) clamp(56px, 9vw, 100px);
  box-sizing: border-box;
}

.success-container {
  width: 100%;
  max-width: 640px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--r-lg);
  padding: clamp(32px, 5vw, 56px) clamp(24px, 4vw, 48px);
  box-shadow: var(--ring);
  text-align: center;
}

.check-big {
  width: 64px; height: 64px;
  border-radius: 50%;
  background: var(--accent-color);
  color: var(--on-accent, #fff);
  display: grid; place-items: center;
  margin-bottom: 24px;
  flex: 0 0 auto;
}

.success-title {
  margin: 0;
  font-family: var(--font-alt);
  font-weight: 800;
  font-size: clamp(24px, 3vw, 36px);
  line-height: 1.1;
  letter-spacing: -.01em;
  color: var(--text);
}

.step-block {
  margin-top: 16px;
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.step-heading {
  margin: 0;
  font-size: 15px;
  line-height: 1.55;
  color: var(--text-2);
}

.step-subtitle {
  margin: 0;
  font-size: 14.5px;
  line-height: 1.55;
  color: var(--text-3);
}

.cta-button {
  font-family: var(--font-alt);
  font-weight: 700;
  font-size: 16px;
  line-height: 1;
  color: #fff;
  background: var(--accent-color);
  border: none;
  border-radius: var(--r-pill);
  padding: 16px 32px;
  cursor: pointer;
  transition: filter var(--t-fast), transform 100ms ease;
  margin-top: 28px;
  width: 100%;
  max-width: 420px;
  display: inline-flex; align-items: center; justify-content: center;
  box-shadow: 0 8px 24px -8px rgba(0,0,0,.3);
}
.cta-button:hover  { filter: brightness(1.08); }
.cta-button:active { transform: scale(.97); }

.instructions {
  margin-top: 20px;
  width: 100%;
  padding: 16px 18px;
  background: var(--surface-2);
  border: 1px solid var(--border);
  border-radius: var(--r-md);
  text-align: left;
}

.instructions-heading {
  margin: 0;
  font-size: 14px;
  font-weight: 600;
  line-height: 1.55;
  color: var(--text-2);
}
</style>
