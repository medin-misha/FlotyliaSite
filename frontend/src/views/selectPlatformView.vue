<script setup>
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'

const router = useRouter()
const { t } = useI18n({ useScope: 'global' })
</script>

<template>
  <section class="select-page">
    <div class="container">

      <div class="page-head">
        <span class="eyebrow">{{ t('landing.cta.eyebrow') }}</span>
        <h1 class="h-display">{{ t('select-platform-title') }}</h1>
        <p class="lead">{{ t('landing.hero.lead') }}</p>
      </div>

      <div class="platform-picker">

        <!-- Bolt -->
        <div class="platform bolt" @click="router.push('/form/bolt')">
          <div class="p-header">
            <div class="p-icon">
              <span class="swatch bolt-swatch">B</span>
              <div class="p-info">
                <span class="p-name">Bolt Food</span>
                <span class="p-tag">{{ t('bolt-select.platform-features.1') }}</span>
              </div>
            </div>
            <span class="p-arrow">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 5l7 7-7 7"/></svg>
            </span>
          </div>
          <ul class="p-features">
            <li v-for="i in 4" :key="i">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5"/></svg>
              {{ t(`bolt-select.platform-features.${i - 1}`) }}
            </li>
          </ul>
          <div class="p-details">
            <span>{{ t('bolt-select.platform-details.0') }}</span>
            <span class="indent">{{ t('bolt-select.indent') }}</span>
            <span>{{ t('bolt-select.platform-details.1') }}</span>
          </div>
          <button class="platform-btn bolt-btn" type="button">
            {{ t('bolt-select.button') }}
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 5l7 7-7 7"/></svg>
          </button>
        </div>

        <!-- Foodora -->
        <div class="platform foodora" @click="router.push('/form/foodora')">
          <div class="p-header">
            <div class="p-icon">
              <span class="swatch foodora-swatch">F</span>
              <div class="p-info">
                <span class="p-name">Foodora</span>
                <span class="p-tag">{{ t('foodora-select.platform-features.0') }}</span>
              </div>
            </div>
            <span class="p-arrow">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 5l7 7-7 7"/></svg>
            </span>
          </div>
          <ul class="p-features">
            <li v-for="i in 4" :key="i">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5"/></svg>
              {{ t(`foodora-select.platform-features.${i - 1}`) }}
            </li>
          </ul>
          <div class="p-details">
            <span>{{ t('foodora-select.platform-details.0') }}</span>
            <span>{{ t('foodora-select.platform-details.1') }}</span>
          </div>
          <button class="platform-btn foodora-btn" type="button">
            {{ t('foodora-select.button') }}
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 5l7 7-7 7"/></svg>
          </button>
        </div>

      </div>
    </div>
  </section>
</template>

<style scoped>
.select-page {
  padding: clamp(40px, 7vw, 80px) 0 clamp(56px, 9vw, 96px);
}

.page-head {
  display: flex;
  flex-direction: column;
  gap: 18px;
  max-width: 640px;
  margin-bottom: clamp(32px, 5vw, 56px);
}

.eyebrow {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: .18em;
  text-transform: uppercase;
  color: var(--accent);
  background: var(--accent-soft);
  padding: 7px 12px;
  border-radius: var(--r-pill);
}
.eyebrow::before {
  content: '';
  width: 6px; height: 6px; border-radius: 50%;
  background: var(--accent);
  box-shadow: 0 0 0 4px var(--accent-soft);
}

.h-display {
  font-family: var(--font-alt);
  font-weight: 800;
  font-size: clamp(32px, 5vw, 56px);
  line-height: 1.04;
  letter-spacing: -0.02em;
  color: var(--text);
}

.lead {
  font-size: clamp(15px, 1.3vw, 17px);
  color: var(--text-2);
  line-height: 1.55;
}

.platform-picker {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}
@media (max-width: 720px) { .platform-picker { grid-template-columns: 1fr; } }

.platform {
  position: relative;
  background: var(--surface);
  border: 1.5px solid var(--border-2);
  border-radius: var(--r-lg);
  padding: 28px;
  display: flex;
  flex-direction: column;
  gap: 20px;
  cursor: pointer;
  transition: transform var(--t-base), border-color var(--t-base);
  overflow: hidden;
  isolation: isolate;
}
.platform::before {
  content: '';
  position: absolute; inset: 0;
  background: var(--card-glow);
  opacity: 0;
  transition: opacity var(--t-base);
  z-index: -1;
}
.platform:hover { transform: translateY(-3px); }
.platform:hover::before { opacity: 1; }
.platform:active { transform: scale(.99); }
.bolt:hover    { border-color: rgba(52,208,134,.5); }
.foodora:hover { border-color: rgba(223,16,104,.5); }

.p-header { display: flex; align-items: center; justify-content: space-between; }
.p-icon   { display: flex; align-items: center; gap: 14px; }

.swatch {
  width: 52px; height: 52px;
  border-radius: 14px;
  display: grid; place-items: center;
  font-family: var(--font-alt);
  font-weight: 800;
  font-size: 22px;
  letter-spacing: -.04em;
  flex: 0 0 auto;
}
.bolt-swatch    { background: #34D086; color: #07150E; }
.foodora-swatch { background: #DF1068; color: #fff; }

.p-info { display: flex; flex-direction: column; gap: 4px; }
.p-name {
  font-family: var(--font-alt);
  font-weight: 700;
  font-size: 20px;
  color: var(--text);
  letter-spacing: -.01em;
}
.p-tag  { font-size: 13px; color: var(--text-3); }

.p-arrow {
  color: var(--text-3);
  transition: transform var(--t-fast), color var(--t-fast);
}
.bolt:hover .p-arrow    { transform: translateX(4px); color: #34D086; }
.foodora:hover .p-arrow { transform: translateX(4px); color: #DF1068; }

.p-features {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.p-features li {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14.5px;
  color: var(--text-2);
}
.bolt    .p-features svg { color: #34D086; }
.foodora .p-features svg { color: #DF1068; }

.p-details {
  display: flex;
  flex-direction: column;
  gap: 4px;
  font-size: 13.5px;
  color: var(--text-3);
  padding: 14px 16px;
  background: var(--surface-2);
  border-radius: var(--r-md);
  border: 1px solid var(--border);
}
.p-details .indent { padding-left: 16px; }

.platform-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 16px 28px;
  border-radius: var(--r-pill);
  border: none;
  font-family: var(--font-alt);
  font-weight: 700;
  font-size: 16px;
  cursor: pointer;
  transition: filter var(--t-fast), transform 100ms ease, box-shadow var(--t-fast);
}
.platform-btn:active { transform: scale(.97); }

.bolt-btn {
  background: #34D086;
  color: #07150E;
  box-shadow: 0 8px 24px -8px rgba(52,208,134,.4);
}
.bolt-btn:hover { filter: brightness(1.08); }

.foodora-btn {
  background: #DF1068;
  color: #fff;
  box-shadow: 0 8px 24px -8px rgba(223,16,104,.4);
}
.foodora-btn:hover { filter: brightness(1.08); }
</style>
