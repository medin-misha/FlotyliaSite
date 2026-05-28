<script setup>
import { useI18n } from 'vue-i18n'
import { useRouter } from 'vue-router'

const { t, tm } = useI18n({ useScope: 'global' })
const router = useRouter()
</script>

<template>
  <div class="select-page">
    <div class="container">
      <div class="select-head">
        <span class="eyebrow">Выбор платформы</span>
        <h1 class="h-display">{{ t('select-platform-title') }}</h1>
        <p class="lead">Выбери платформу — от этого зависит менеджер и условия. Можно поменять позже.</p>
      </div>

      <div class="platforms">

        <!-- Bolt -->
        <div class="platform-card bolt">
          <div class="platform-head">
            <span class="platform-swatch bolt-swatch">B</span>
            <div>
              <div class="platform-name">Bolt Food</div>
              <div class="platform-tag">Самый популярный выбор</div>
            </div>
          </div>
          <ul class="platform-features">
            <li v-for="(feat, i) in tm('bolt-select.platform-features')" :key="i">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5"/></svg>
              {{ feat }}
            </li>
          </ul>
          <div class="platform-details">
            <p v-for="(detail, i) in tm('bolt-select.platform-details')" :key="i">{{ detail }}</p>
            <p class="indent">{{ t('bolt-select.indent') }}</p>
          </div>
          <button class="btn btn-bolt btn-lg" @click="router.push('/form/bolt')">
            {{ t('bolt-select.button') }}
            <svg class="arrow" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 5l7 7-7 7"/></svg>
          </button>
        </div>

        <!-- Foodora -->
        <div class="platform-card foodora">
          <div class="platform-head">
            <span class="platform-swatch foodora-swatch">F</span>
            <div>
              <div class="platform-name">Foodora</div>
              <div class="platform-tag">Больше ресторанов в Праге</div>
            </div>
          </div>
          <ul class="platform-features">
            <li v-for="(feat, i) in tm('foodora-select.platform-features')" :key="i">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5"/></svg>
              {{ feat }}
            </li>
          </ul>
          <div class="platform-details">
            <p v-for="(detail, i) in tm('foodora-select.platform-details')" :key="i">{{ detail }}</p>
          </div>
          <button class="btn btn-foodora btn-lg" @click="router.push('/form/foodora')">
            {{ t('foodora-select.button') }}
            <svg class="arrow" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 5l7 7-7 7"/></svg>
          </button>
        </div>

      </div>
    </div>
  </div>
</template>

<style scoped>
.select-page {
  padding: clamp(40px, 7vw, 80px) 0 clamp(56px, 9vw, 112px);
}

.select-head {
  display: flex;
  flex-direction: column;
  gap: 16px;
  max-width: 640px;
  margin-bottom: clamp(32px, 4vw, 56px);
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
.lead { font-size: clamp(15px, 1.3vw, 17px); color: var(--text-2); line-height: 1.55; }

.platforms {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  max-width: 900px;
}
@media (max-width: 720px) { .platforms { grid-template-columns: 1fr; } }

.platform-card {
  position: relative;
  background: var(--surface);
  border: 1.5px solid var(--border);
  border-radius: var(--r-lg);
  padding: clamp(24px, 3vw, 36px);
  display: flex;
  flex-direction: column;
  gap: 20px;
  transition: border-color var(--t-base), transform var(--t-base);
  overflow: hidden;
  isolation: isolate;
}
.platform-card::before {
  content: '';
  position: absolute; inset: 0;
  background: var(--card-glow);
  opacity: 0;
  transition: opacity var(--t-base);
  z-index: -1;
}
.bolt:hover   { border-color: #34D086; }
.foodora:hover { border-color: #DF1068; }
.platform-card:hover { transform: translateY(-3px); }
.platform-card:hover::before { opacity: 1; }

.platform-head { display: flex; align-items: center; gap: 14px; }

.platform-swatch {
  width: 52px; height: 52px; border-radius: 14px;
  display: grid; place-items: center;
  font-family: var(--font-alt); font-weight: 800; font-size: 22px;
  letter-spacing: -.04em; color: #fff; flex: 0 0 auto;
}
.bolt-swatch    { background: #34D086; color: #07150E; }
.foodora-swatch { background: #DF1068; }

.platform-name {
  font-family: var(--font-alt); font-weight: 700; font-size: 20px;
  letter-spacing: -.01em; color: var(--text); line-height: 1.1;
}
.platform-tag { margin-top: 4px; font-size: 13px; color: var(--text-3); }

.platform-features {
  list-style: none;
  display: flex; flex-direction: column; gap: 10px;
}
.platform-features li {
  display: flex; align-items: center; gap: 10px;
  font-size: 15px; color: var(--text-2); line-height: 1.4;
}
.platform-features svg { flex: 0 0 auto; color: var(--accent); }

.platform-details {
  display: flex; flex-direction: column; gap: 4px;
  padding: 14px 16px;
  background: var(--surface-2);
  border-radius: var(--r-md);
  border: 1px solid var(--border);
}
.platform-details p { font-size: 14px; color: var(--text-2); margin: 0; line-height: 1.5; }
.indent { padding-left: 16px; }

.btn-bolt {
  display: inline-flex; align-items: center; justify-content: center; gap: 10px;
  padding: 18px 32px; border-radius: var(--r-pill);
  font-family: var(--font-alt); font-weight: 700; font-size: 17px; line-height: 1;
  background: #34D086; color: #07150E;
  box-shadow: 0 8px 24px -8px rgba(52,208,134,.4), inset 0 1px 0 rgba(255,255,255,.3);
  transition: filter var(--t-fast), transform 100ms ease, box-shadow var(--t-fast);
  border: none; cursor: pointer; user-select: none; width: 100%;
}
.btn-bolt:hover  { filter: brightness(1.08); }
.btn-bolt:active { transform: scale(.97); }

.btn-foodora {
  display: inline-flex; align-items: center; justify-content: center; gap: 10px;
  padding: 18px 32px; border-radius: var(--r-pill);
  font-family: var(--font-alt); font-weight: 700; font-size: 17px; line-height: 1;
  background: #DF1068; color: #fff;
  box-shadow: 0 8px 24px -8px rgba(223,16,104,.4), inset 0 1px 0 rgba(255,255,255,.2);
  transition: filter var(--t-fast), transform 100ms ease, box-shadow var(--t-fast);
  border: none; cursor: pointer; user-select: none; width: 100%;
}
.btn-foodora:hover  { filter: brightness(1.08); }
.btn-foodora:active { transform: scale(.97); }

.arrow { transition: transform var(--t-fast); }
.btn-bolt:hover .arrow,
.btn-foodora:hover .arrow { transform: translateX(3px); }
</style>
