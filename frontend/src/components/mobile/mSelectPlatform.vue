<script setup>
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'

const router = useRouter()
const { t } = useI18n({ useScope: 'global' })

const platforms = [
  {
    key: 'bolt', swatchClass: 'bolt-swatch', letter: 'B',
    name: 'Bolt Food', tag: 'Самый популярный выбор',
    buttonKey: 'bolt-select.button', route: '/form/bolt',
    featureKeys: ['bolt-select.platform-features.0','bolt-select.platform-features.1','bolt-select.platform-features.2','bolt-select.platform-features.3'],
    detailKeys: ['bolt-select.platform-details.0','bolt-select.indent','bolt-select.platform-details.1'],
    btnClass: 'btn-bolt',
  },
  {
    key: 'foodora', swatchClass: 'foodora-swatch', letter: 'F',
    name: 'Foodora', tag: 'Больше ресторанов в Праге',
    buttonKey: 'foodora-select.button', route: '/form/foodora',
    featureKeys: ['foodora-select.platform-features.0','foodora-select.platform-features.1','foodora-select.platform-features.2','foodora-select.platform-features.3'],
    detailKeys: ['foodora-select.platform-details.0','foodora-select.platform-details.1'],
    btnClass: 'btn-foodora',
  },
]
</script>

<template>
  <div class="m-select">
    <div class="m-select-head">
      <span class="eyebrow">Выбор платформы</span>
      <h1 class="h-display">{{ t('select-platform-title') }}</h1>
      <p class="lead">Выбери платформу — от этого зависит менеджер и условия.</p>
    </div>

    <div class="m-platform-list">
      <div v-for="p in platforms" :key="p.key" class="m-platform-card" :class="p.key">
        <div class="m-platform-head">
          <span class="m-swatch" :class="p.swatchClass">{{ p.letter }}</span>
          <div>
            <div class="m-platform-name">{{ p.name }}</div>
            <div class="m-platform-tag">{{ p.tag }}</div>
          </div>
        </div>

        <ul class="m-features">
          <li v-for="fk in p.featureKeys" :key="fk">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5"/></svg>
            {{ t(fk) }}
          </li>
        </ul>

        <div class="m-details">
          <p v-for="dk in p.detailKeys" :key="dk" :class="{ indent: dk.includes('indent') }">{{ t(dk) }}</p>
        </div>

        <button type="button" class="m-btn" :class="p.btnClass" @click="router.push(p.route)">
          {{ t(p.buttonKey) }}
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 5l7 7-7 7"/></svg>
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.m-select {
  padding: clamp(24px, 5vw, 40px) var(--gutter) clamp(40px, 7vw, 64px);
}

.m-select-head {
  display: flex; flex-direction: column; gap: 14px; margin-bottom: 28px;
}

.eyebrow {
  display: inline-flex; align-items: center; gap: 8px;
  font-size: 11px; font-weight: 700; letter-spacing: .18em;
  text-transform: uppercase; color: var(--accent);
  background: var(--accent-soft); padding: 7px 12px; border-radius: var(--r-pill);
}
.eyebrow::before {
  content: ''; width: 6px; height: 6px; border-radius: 50%;
  background: var(--accent); box-shadow: 0 0 0 4px var(--accent-soft);
}

.h-display {
  font-family: var(--font-alt); font-weight: 800;
  font-size: clamp(28px, 8vw, 42px);
  line-height: 1.04; letter-spacing: -0.02em; color: var(--text);
}
.lead { font-size: clamp(14px, 4vw, 16px); color: var(--text-2); line-height: 1.55; }

.m-platform-list { display: flex; flex-direction: column; gap: 16px; }

.m-platform-card {
  background: var(--surface); border: 1.5px solid var(--border);
  border-radius: var(--r-lg); padding: 22px 20px;
  display: flex; flex-direction: column; gap: 18px;
}
.m-platform-card.bolt  { border-color: rgba(52,208,134,.3); }
.m-platform-card.foodora { border-color: rgba(223,16,104,.3); }

.m-platform-head { display: flex; align-items: center; gap: 14px; }
.m-swatch {
  width: 48px; height: 48px; border-radius: 13px;
  display: grid; place-items: center;
  font-family: var(--font-alt); font-weight: 800; font-size: 20px;
  flex: 0 0 auto;
}
.bolt-swatch    { background: #34D086; color: #07150E; }
.foodora-swatch { background: #DF1068; color: #fff; }
.m-platform-name {
  font-family: var(--font-alt); font-weight: 700;
  font-size: 18px; letter-spacing: -.01em; color: var(--text);
}
.m-platform-tag { font-size: 12.5px; color: var(--text-3); margin-top: 2px; }

.m-features {
  list-style: none; display: flex; flex-direction: column; gap: 8px;
}
.m-features li {
  display: flex; align-items: center; gap: 9px;
  font-size: 14px; color: var(--text-2); line-height: 1.4;
}
.m-features svg { flex: 0 0 auto; color: var(--accent); }

.m-details {
  padding: 12px 14px; background: var(--surface-2);
  border: 1px solid var(--border); border-radius: var(--r-md);
}
.m-details p { font-size: 13.5px; color: var(--text-2); margin: 0; line-height: 1.5; }
.m-details p + p { margin-top: 3px; }
.indent { padding-left: 14px; }

.m-btn {
  display: inline-flex; align-items: center; justify-content: center; gap: 8px;
  width: 100%; padding: 15px 24px; border-radius: var(--r-pill);
  font-family: var(--font-alt); font-weight: 700; font-size: 16px; line-height: 1;
  border: none; cursor: pointer;
  transition: filter var(--t-fast), transform 100ms ease;
}
.m-btn:active { transform: scale(.97); }
.m-btn:hover  { filter: brightness(1.08); }

.btn-bolt    { background: #34D086; color: #07150E; box-shadow: 0 6px 20px -6px rgba(52,208,134,.5); }
.btn-foodora { background: #DF1068; color: #fff;    box-shadow: 0 6px 20px -6px rgba(223,16,104,.4); }
</style>
