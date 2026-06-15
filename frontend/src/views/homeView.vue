<script setup>
import { onMounted, onUnmounted } from 'vue'
import { RouterLink } from 'vue-router'
import { useI18n } from 'vue-i18n'

const { t } = useI18n({ useScope: 'global' })

let io = null
onMounted(() => {
  io = new IntersectionObserver((entries) => {
    entries.forEach(en => {
      if (en.isIntersecting) {
        en.target.classList.add('in')
        io.unobserve(en.target)
      }
    })
  }, { threshold: 0.08, rootMargin: '0px 0px -40px 0px' })
  document.querySelectorAll('.reveal').forEach(el => io.observe(el))
})
onUnmounted(() => { if (io) io.disconnect() })
</script>

<template>

<!-- ========================= HERO ========================= -->
<section class="hero" id="top">
  <div class="container hero-inner">
    <div class="hero-copy">
      <span class="eyebrow">{{ t('landing.hero.eyebrow') }}</span>
      <h1 class="h-display reveal">
        {{ t('landing.hero.title-line1') }} <br />
        <span class="hl">{{ t('landing.hero.title-line2') }}</span>
      </h1>
      <p class="lead reveal" style="max-width:520px">
        {{ t('landing.hero.lead') }}
      </p>
      <div class="hero-actions reveal">
        <RouterLink to="/form" class="btn btn-primary btn-lg">
          {{ t('landing.cta.apply') }}
          <svg class="arrow" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 5l7 7-7 7"/></svg>
        </RouterLink>
        <a href="#vehicles" class="btn btn-ghost btn-lg">{{ t('landing.hero.vehicle-link') }}</a>
      </div>
      <div class="hero-meta reveal">
        <div><span class="dot">●</span> <b>4×</b>&nbsp;{{ t('landing.hero.meta.payouts') }}</div>
        <div><span class="dot">●</span> <b>0&nbsp;Kč</b>&nbsp;{{ t('landing.hero.meta.deposit') }}</div>
        <div><span class="dot">●</span> <b>5&nbsp;{{ t('landing.units.minutes-short') }}</b>&nbsp;{{ t('landing.hero.meta.application') }}</div>
      </div>
    </div>

    <div class="hero-visual reveal">
      <div class="hv-grid"></div>
      <div class="hv-blob"></div>
      <div class="hv-mark">
        <span class="glyph-lg">
          <svg fill="currentColor" aria-hidden="true" viewBox="0 19 78 31" style="width:115px;height:auto">
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
        <div class="hero-tag">
          <span class="pulse"></span>
          {{ t('landing.hero.open') }}
        </div>
      </div>
      <div class="hv-stats">
        <div class="hv-stat">
          <div class="num">2–3 <span class="unit">{{ t('landing.units.days') }}</span></div>
          <div class="lbl">{{ t('landing.hero.stats.first-order') }}</div>
        </div>
        <div class="hv-stat">
          <div class="num">4<span class="unit">{{ t('landing.units.per-month-times') }}</span></div>
          <div class="lbl">{{ t('landing.hero.stats.weekly-payouts') }}</div>
        </div>
        <div class="hv-stat">
          <div class="num">0 <span class="unit">Kč</span></div>
          <div class="lbl">{{ t('landing.hero.stats.deposit') }}</div>
        </div>
        <div class="hv-stat">
          <div class="num">24/7</div>
          <div class="lbl">{{ t('landing.hero.stats.support') }}</div>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- ========================= PARTNERS ========================= -->
<section class="partners">
  <div class="container partners-inner">
    <span class="partners-label">{{ t('landing.partners.label') }}</span>
    <div class="partners-list">
      <span class="partner-logo partner-bolt"><span class="pdot"></span>Bolt Food</span>
      <span class="partner-logo partner-foodora"><span class="pdot"></span>Foodora</span>
    </div>
  </div>
</section>

<!-- ========================= FEATURES ========================= -->
<section class="section" id="features">
  <div class="container">
    <div class="section-head reveal">
      <span class="eyebrow">{{ t('landing.features.eyebrow') }}</span>
      <h2 class="h-section">{{ t('landing.features.title-prefix') }} <span class="accent">{{ t('landing.features.title-accent') }}</span>, {{ t('landing.features.title-suffix') }}</h2>
      <p class="lead">{{ t('landing.features.lead') }}</p>
    </div>

    <div class="features">
      <div class="feature reveal">
        <div class="feature-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M3 7a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v2"/><path d="M3 7v10a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7H7a2 2 0 0 0 0 4h14"/><circle cx="17" cy="14" r="1.2" fill="currentColor" stroke="none"/></svg>
        </div>
        <span class="pill">{{ t('landing.features.pills.payouts') }}</span>
        <h3>{{ t('why-us.item1.title') }}</h3>
        <p>{{ t('why-us.item1.line1') }} {{ t('why-us.item1.line2') }} {{ t('why-us.item1.line3') }}</p>
      </div>

      <div class="feature reveal">
        <div class="feature-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M14 3H6a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z"/><path d="M14 3v6h6"/><path d="M9 15l2 2 4-4"/></svg>
        </div>
        <span class="pill">{{ t('landing.features.pills.paperwork') }}</span>
        <h3>{{ t('why-us.item2.title') }}</h3>
        <p>{{ t('why-us.item2.line1') }} {{ t('why-us.item2.line2') }}</p>
      </div>

      <div class="feature reveal">
        <div class="feature-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M13 2L4.5 14h6.5l-1 8L18.5 10H12z" fill="currentColor" stroke="none" opacity=".18"/><path d="M13 2L4.5 14h6.5l-1 8L18.5 10H12z"/></svg>
        </div>
        <span class="pill">{{ t('landing.features.pills.deposit') }}</span>
        <h3>{{ t('why-us.item3.title') }}</h3>
        <p>{{ t('why-us.item3.line1') }} {{ t('why-us.item3.line2') }}</p>
      </div>
    </div>
  </div>
</section>

<!-- ========================= HOW TO START ========================= -->
<section class="section section-tight" id="how">
  <div class="container">
    <div class="section-head reveal">
      <span class="eyebrow">{{ t('landing.steps.eyebrow') }}</span>
      <h2 class="h-section">{{ t('landing.steps.title-prefix') }} <span class="accent">{{ t('landing.steps.title-accent') }}</span></h2>
      <p class="lead">{{ t('landing.steps.lead') }}</p>
    </div>

    <div class="steps">
      <div class="step reveal">
        <span class="step-num">01</span>
        <span class="step-tag"><span class="sn">1</span>{{ t('landing.steps.step-label') }}</span>
        <h3>{{ t('landing.steps.items.0.title') }}</h3>
        <p>{{ t('landing.steps.items.0.text') }}</p>
      </div>
      <div class="step reveal">
        <span class="step-num">02</span>
        <span class="step-tag"><span class="sn">2</span>{{ t('landing.steps.step-label') }}</span>
        <h3>{{ t('landing.steps.items.1.title') }}</h3>
        <p>{{ t('landing.steps.items.1.text') }}</p>
      </div>
      <div class="step reveal">
        <span class="step-num">03</span>
        <span class="step-tag"><span class="sn">3</span>{{ t('landing.steps.step-label') }}</span>
        <h3>{{ t('landing.steps.items.2.title') }}</h3>
        <p>{{ t('landing.steps.items.2.text') }}</p>
      </div>
    </div>
  </div>
</section>

<!-- ========================= VEHICLES ========================= -->
<section class="section" id="vehicles">
  <div class="container">
    <div class="section-head reveal">
      <span class="eyebrow">{{ t('transport-section.title') }}</span>
      <h2 class="h-section">{{ t('landing.vehicles.title-prefix') }} <span class="accent">{{ t('landing.vehicles.title-accent') }}</span></h2>
      <p class="lead">{{ t('landing.vehicles.lead') }}</p>
    </div>

    <div class="vehicles">
      <article class="vehicle reveal">
        <div class="v-image">
          <span class="v-no-deposit">{{ t('landing.vehicles.no-deposit') }}</span>
          <div class="v-icon">
            <svg viewBox="0 0 96 64"><circle cx="22" cy="48" r="12"/><circle cx="74" cy="48" r="12"/><circle cx="22" cy="48" r="1.5" fill="currentColor"/><circle cx="74" cy="48" r="1.5" fill="currentColor"/><path d="M22 48 40 22h22l12 26"/><path d="M40 22h16"/><path d="M56 22l6-10h8" stroke-linecap="round"/><path d="M62 22v-4"/></svg>
          </div>
        </div>
        <div class="v-body">
          <h3>{{ t('transport.bike.title') }}</h3>
          <p>{{ t('transport.bike.line1') }} {{ t('transport.bike.line2') }}</p>
          <RouterLink to="/form" class="v-cta">
            {{ t('landing.cta.apply') }}
            <svg class="arrow" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 5l7 7-7 7"/></svg>
          </RouterLink>
        </div>
      </article>

      <article class="vehicle reveal">
        <div class="v-image">
          <span class="v-badge">{{ t('landing.vehicles.ebike-price') }} <small>{{ t('landing.units.per-week') }}</small></span>
          <span class="v-no-deposit">{{ t('landing.vehicles.no-deposit') }}</span>
          <div class="v-icon">
            <svg viewBox="0 0 96 64"><circle cx="22" cy="48" r="12"/><circle cx="74" cy="48" r="12"/><circle cx="22" cy="48" r="1.5" fill="currentColor"/><circle cx="74" cy="48" r="1.5" fill="currentColor"/><path d="M22 48 40 22h22l12 26"/><path d="M40 22h16"/><path d="M56 22l6-10h8"/><path d="M44 38l6-8-4-2 6-8" fill="currentColor" stroke="currentColor" stroke-width="1.2"/></svg>
          </div>
        </div>
        <div class="v-body">
          <h3>{{ t('transport.ebike.title') }}</h3>
          <p>{{ t('transport.ebike.line1') }} {{ t('transport.ebike.line2') }}</p>
          <RouterLink to="/form" class="v-cta">
            {{ t('landing.cta.apply') }}
            <svg class="arrow" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 5l7 7-7 7"/></svg>
          </RouterLink>
        </div>
      </article>

      <article class="vehicle reveal">
        <div class="v-image">
          <span class="v-no-deposit">{{ t('landing.vehicles.no-deposit') }}</span>
          <div class="v-icon">
            <svg viewBox="0 0 96 64"><circle cx="20" cy="50" r="8"/><circle cx="76" cy="50" r="8"/><path d="M20 50h56"/><path d="M76 50 60 18h-8"/><path d="M60 18v-6h-8v6"/><path d="M52 12l6 6" stroke-linecap="round"/><path d="M28 50l8-12" stroke-linecap="round"/></svg>
          </div>
        </div>
        <div class="v-body">
          <h3>{{ t('transport.escooter.title') }}</h3>
          <p>{{ t('transport.escooter.line1') }} {{ t('transport.escooter.line2') }}</p>
          <RouterLink to="/form" class="v-cta">
            {{ t('landing.cta.apply') }}
            <svg class="arrow" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 5l7 7-7 7"/></svg>
          </RouterLink>
        </div>
      </article>

      <article class="vehicle reveal">
        <div class="v-image">
          <span class="v-badge">{{ t('landing.vehicles.car-price') }} <small>{{ t('landing.units.per-week') }}</small></span>
          <div class="v-icon">
            <svg viewBox="0 0 96 64"><path d="M10 44h76v-8l-8-4-6-12c-1.6-3-3.6-4-7-4H35c-3.4 0-5.4 1-7 4l-6 12-8 4z"/><path d="M22 36h52"/><circle cx="26" cy="50" r="6"/><circle cx="70" cy="50" r="6"/><path d="M5 44v6h5M86 44v6h5"/></svg>
          </div>
        </div>
        <div class="v-body">
          <h3>{{ t('transport.car.title') }}</h3>
          <p>{{ t('transport.car.line1') }} {{ t('transport.car.line2') }}</p>
          <RouterLink to="/form" class="v-cta">
            {{ t('landing.cta.apply') }}
            <svg class="arrow" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 5l7 7-7 7"/></svg>
          </RouterLink>
        </div>
      </article>
    </div>

    <div class="vehicles-note">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4M12 8h.01"/></svg>
      <span>{{ t('transport-footnote') }}</span>
    </div>
  </div>
</section>

<!-- ========================= CTA BANNER ========================= -->
<section class="section" id="cta">
  <div class="container">
    <div class="cta-banner reveal">
      <div class="cta-copy">
        <span class="eyebrow">{{ t('landing.cta.eyebrow') }}</span>
        <h2 class="h-section">{{ t('landing.cta.title') }}</h2>
        <p class="lead">{{ t('landing.cta.lead') }}</p>
        <ul class="cta-list">
          <li>
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5"/></svg>
            {{ t('landing.cta.items.0') }}
          </li>
          <li>
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5"/></svg>
            {{ t('landing.cta.items.1') }}
          </li>
          <li>
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5"/></svg>
            {{ t('landing.cta.items.2') }}
          </li>
        </ul>
        <div class="cta-actions">
          <RouterLink to="/form" class="btn btn-primary btn-lg">
            {{ t('landing.cta.apply') }}
            <svg class="arrow" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 5l7 7-7 7"/></svg>
          </RouterLink>
          <a href="https://t.me/MFS_support" class="btn btn-ghost btn-lg" target="_blank" rel="noopener">{{ t('landing.cta.telegram') }}</a>
        </div>
      </div>
      <div class="cta-side" aria-hidden="true">
        <div class="cta-meta">
          <div class="cta-metric">
            <div class="v">~1 {{ t('landing.units.hour-short') }}</div>
            <div class="k">{{ t('landing.cta.metrics.response') }}</div>
          </div>
          <div class="cta-metric">
            <div class="v">5 {{ t('landing.units.minutes-short') }}</div>
            <div class="k">{{ t('landing.cta.metrics.form') }}</div>
          </div>
          <div class="cta-metric">
            <div class="v">2–3 {{ t('landing.units.days') }}</div>
            <div class="k">{{ t('landing.cta.metrics.first-order') }}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>

</template>

<style scoped>
/* ─── Reveal ─── */
.reveal { opacity: 0; transform: translateY(16px); transition: opacity 600ms ease, transform 700ms cubic-bezier(.2,.7,.3,1); }
.reveal.in { opacity: 1; transform: none; }

/* ─── Hero ─── */
.hero {
  position: relative;
  padding-top: clamp(40px, 7vw, 80px);
  padding-bottom: clamp(40px, 7vw, 80px);
  overflow: hidden;
}
.hero::before {
  content: '';
  position: absolute;
  inset: -10% -10% auto -10%;
  height: 100%;
  background:
    radial-gradient(60% 70% at 80% 10%, var(--accent-soft), transparent 60%),
    radial-gradient(50% 60% at 0% 90%, var(--accent-soft), transparent 60%);
  opacity: .9;
  pointer-events: none;
  z-index: 0;
}
.hero-inner {
  position: relative;
  display: grid;
  grid-template-columns: 1.05fr 1fr;
  gap: clamp(24px, 4vw, 56px);
  align-items: center;
  z-index: 1;
}
.hero-copy { display: flex; flex-direction: column; gap: 22px; align-items: flex-start; }
.h-display {
  font-family: var(--font-alt);
  font-weight: 800;
  font-size: clamp(36px, 6.4vw, 76px);
  line-height: 1.02;
  letter-spacing: -0.02em;
  color: var(--text);
  text-wrap: balance;
}
.hl {
  background: var(--accent-grad);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}
.h-section {
  font-family: var(--font-alt);
  font-weight: 800;
  font-size: clamp(28px, 4.4vw, 52px);
  line-height: 1.05;
  letter-spacing: -0.018em;
  color: var(--text);
  text-wrap: balance;
}
.lead {
  font-size: clamp(16px, 1.4vw, 19px);
  line-height: 1.55;
  color: var(--text-2);
  text-wrap: pretty;
}
.accent { color: var(--accent); }
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
.hero-actions { display: flex; flex-wrap: wrap; gap: 12px; margin-top: 8px; }
.hero-meta {
  display: flex; flex-wrap: wrap; gap: 20px 28px;
  margin-top: 14px; color: var(--text-2); font-size: 14px;
}
.hero-meta b { color: var(--text); font-weight: 700; }
.hero-meta .dot { color: var(--accent); }

.hero-visual {
  position: relative;
  aspect-ratio: 5 / 4;
  border-radius: var(--r-lg);
  background:
    radial-gradient(120% 90% at 100% 0%, var(--accent-soft) 0%, transparent 55%),
    radial-gradient(110% 100% at 0% 100%, color-mix(in srgb, var(--accent) 12%, transparent) 0%, transparent 60%),
    var(--surface);
  border: 1px solid var(--border);
  box-shadow: var(--ring);
  overflow: hidden;
  isolation: isolate;
  padding: clamp(24px, 3vw, 36px);
  display: flex; flex-direction: column;
  justify-content: space-between; gap: 18px; min-height: 360px;
}
.hv-mark {
  display: flex; align-items: center; justify-content: space-between; z-index: 2;
}
.glyph-lg {
  height: 72px; border-radius: 18px;
  background: var(--accent); color: #fff;
  display: inline-flex; align-items: center; justify-content: center;
  padding: 14px 22px;
  box-shadow: 0 14px 30px -10px var(--accent-ring);
}
.hero-tag {
  display: inline-flex; align-items: center; gap: 8px;
  padding: 7px 12px 7px 9px;
  border-radius: var(--r-pill);
  background: color-mix(in srgb, var(--surface) 85%, transparent);
  border: 1px solid var(--border-2);
  backdrop-filter: blur(8px);
  font-size: 12px; font-weight: 600; color: var(--text);
}
.pulse {
  width: 8px; height: 8px; border-radius: 50%;
  background: var(--accent);
  animation: pulse 1.8s ease-out infinite;
}
@keyframes pulse {
  0%   { box-shadow: 0 0 0 0 var(--accent-ring); }
  70%  { box-shadow: 0 0 0 10px transparent; }
  100% { box-shadow: 0 0 0 0 transparent; }
}
.hv-stats {
  display: grid; grid-template-columns: 1fr 1fr; gap: 10px; z-index: 2;
}
.hv-stat {
  background: color-mix(in srgb, var(--bg) 70%, transparent);
  border: 1px solid var(--border);
  border-radius: var(--r-md);
  padding: 16px 16px 14px;
  backdrop-filter: blur(6px);
}
.hv-stat .num {
  font-family: var(--font-alt); font-weight: 800;
  font-size: clamp(28px, 3.4vw, 40px);
  line-height: 1; letter-spacing: -.02em; color: var(--text);
  display: flex; align-items: baseline; gap: 4px;
}
.unit { font-size: .5em; color: var(--accent); font-weight: 700; }
.hv-stat .lbl { margin-top: 6px; font-size: 12.5px; color: var(--text-2); line-height: 1.3; }
.hv-grid {
  position: absolute; inset: 0;
  background-image:
    linear-gradient(to right, color-mix(in srgb, var(--text) 6%, transparent) 1px, transparent 1px),
    linear-gradient(to bottom, color-mix(in srgb, var(--text) 6%, transparent) 1px, transparent 1px);
  background-size: 40px 40px;
  mask-image: radial-gradient(120% 90% at 70% 30%, #000 30%, transparent 75%);
  pointer-events: none; z-index: 0;
}
.hv-blob {
  position: absolute; right: -60px; bottom: -80px;
  width: 320px; height: 320px; border-radius: 50%;
  background: radial-gradient(circle at 30% 30%, var(--accent-light), var(--accent) 60%, transparent 70%);
  filter: blur(40px); opacity: .35; z-index: 0;
}
@media (max-width: 860px) {
  .hero-inner { grid-template-columns: 1fr; }
  .hero-visual { order: -1; aspect-ratio: auto; min-height: 280px; }
}

/* ─── Partners ─── */
.partners {
  border-top: 1px solid var(--border);
  border-bottom: 1px solid var(--border);
  padding: 22px 0;
}
.partners-inner {
  display: flex; flex-wrap: wrap;
  align-items: center; justify-content: space-between; gap: 18px 32px;
}
.partners-label {
  font-size: 12px; letter-spacing: .14em;
  text-transform: uppercase; color: var(--text-3); font-weight: 600;
}
.partners-list { display: flex; flex-wrap: wrap; align-items: center; gap: 28px; }
.partner-logo {
  display: inline-flex; align-items: center; gap: 8px;
  font-weight: 700; font-size: 17px; color: var(--text-2); letter-spacing: -.01em;
}
.pdot { width: 10px; height: 10px; border-radius: 50%; }
.partner-bolt .pdot  { background: #34D086; }
.partner-foodora .pdot { background: #DF1068; }

/* ─── Sections ─── */
.section { padding: clamp(56px, 9vw, 112px) 0; }
.section-tight { padding: clamp(40px, 7vw, 80px) 0; }
.section-head {
  display: flex; flex-direction: column; gap: 18px;
  max-width: 720px; margin-bottom: clamp(32px, 4vw, 56px);
}

/* ─── Features ─── */
.features { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; }
@media (max-width: 860px) { .features { grid-template-columns: 1fr; } }

.feature {
  position: relative;
  background: var(--surface); border: 1px solid var(--border);
  border-radius: var(--r-lg); padding: 28px 26px;
  display: flex; flex-direction: column; gap: 16px;
  transition: transform var(--t-base), border-color var(--t-base);
  overflow: hidden; isolation: isolate;
}
.feature::before {
  content:''; position: absolute; inset: 0;
  background: var(--card-glow); opacity: 0;
  transition: opacity var(--t-base); z-index: -1;
}
.feature:hover { transform: translateY(-3px); border-color: var(--border-2); }
.feature:hover::before { opacity: 1; }
.feature-icon {
  width: 48px; height: 48px; border-radius: 14px;
  background: var(--accent-soft); color: var(--accent);
  display: grid; place-items: center;
}
.feature-icon svg { width: 24px; height: 24px; stroke: currentColor; }
.feature h3 { font-weight: 700; font-size: clamp(18px,1.6vw,22px); line-height: 1.2; }
.feature p { color: var(--text-2); font-size: 15px; line-height: 1.55; }
.feature .pill {
  align-self: flex-start; font-size: 12px; font-weight: 700; letter-spacing: .04em;
  padding: 5px 10px; border-radius: var(--r-pill);
  background: var(--surface-2); color: var(--text-2); border: 1px solid var(--border);
}

/* ─── Steps ─── */
.steps { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; }
@media (max-width: 860px) { .steps { grid-template-columns: 1fr; } }

.step {
  position: relative;
  background: var(--surface); border: 1px solid var(--border);
  border-radius: var(--r-lg); padding: 28px 26px 26px;
  display: flex; flex-direction: column; gap: 12px; overflow: hidden;
}
.step-num {
  font-family: var(--font-alt); font-weight: 800; font-size: 80px;
  line-height: .9; letter-spacing: -.04em; color: var(--text); opacity: .08;
  position: absolute; right: 22px; top: 14px; pointer-events: none;
}
.step-tag {
  display: inline-flex; align-items: center; gap: 8px;
  font-size: 12px; font-weight: 700; letter-spacing: .12em;
  text-transform: uppercase; color: var(--accent);
}
.sn {
  width: 22px; height: 22px; border-radius: 50%;
  background: var(--accent); color: var(--on-accent);
  display: grid; place-items: center; font-size: 11px; letter-spacing: 0;
}
.step h3 { font-weight: 700; font-size: 19px; line-height: 1.2; position: relative; z-index: 1; }
.step p { color: var(--text-2); font-size: 14.5px; position: relative; z-index: 1; }

/* ─── Vehicles ─── */
.vehicles { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; }
@media (max-width: 1080px) { .vehicles { grid-template-columns: repeat(2, 1fr); } }
@media (max-width: 520px)  { .vehicles { grid-template-columns: 1fr; } }

.vehicle {
  position: relative; background: var(--surface); border: 1px solid var(--border);
  border-radius: var(--r-lg); overflow: hidden; display: flex; flex-direction: column;
  transition: transform var(--t-base), border-color var(--t-base); isolation: isolate;
}
.vehicle:hover { transform: translateY(-4px); border-color: var(--border-2); }
.vehicle:hover .v-icon { transform: scale(1.06); }

.v-image {
  position: relative; aspect-ratio: 4 / 3;
  background: radial-gradient(120% 90% at 100% 0%, var(--accent-soft) 0%, transparent 55%), var(--surface-2);
  overflow: hidden; isolation: isolate; display: grid; place-items: center;
}
.v-image::before {
  content:''; position: absolute; inset: 0;
  background-image:
    linear-gradient(to right, color-mix(in srgb, var(--text) 5%, transparent) 1px, transparent 1px),
    linear-gradient(to bottom, color-mix(in srgb, var(--text) 5%, transparent) 1px, transparent 1px);
  background-size: 28px 28px;
  mask-image: radial-gradient(80% 60% at 50% 60%, #000 30%, transparent 80%);
  z-index: 0;
}
.v-icon {
  position: relative; z-index: 1; width: 60%; max-width: 180px; color: var(--accent);
  transition: transform 500ms cubic-bezier(.2,.7,.3,1);
}
.v-icon svg {
  width: 100%; height: auto; stroke: currentColor; fill: none;
  stroke-width: 1.6; stroke-linecap: round; stroke-linejoin: round;
}
.v-badge {
  position: absolute; left: 14px; top: 14px; z-index: 3;
  display: inline-flex; align-items: baseline; gap: 4px;
  padding: 6px 12px; border-radius: var(--r-pill);
  background: var(--accent); color: var(--on-accent);
  font-family: var(--font-alt); font-weight: 700; font-size: 13px; line-height: 1;
}
.v-badge small { font-size: 10.5px; font-weight: 600; opacity: .7; }
.v-no-deposit {
  position: absolute; right: 14px; top: 14px; z-index: 3;
  padding: 6px 10px; border-radius: var(--r-pill);
  background: color-mix(in srgb, var(--surface) 85%, transparent);
  border: 1px solid var(--border-2); color: var(--text-2);
  font-size: 11.5px; font-weight: 600; backdrop-filter: blur(6px);
}
.v-body { padding: 20px 22px 24px; display: flex; flex-direction: column; gap: 8px; flex: 1; }
.v-body h3 { font-weight: 700; font-size: 18px; line-height: 1.2; }
.v-body p  { color: var(--text-2); font-size: 14px; line-height: 1.5; flex: 1; }
.v-cta {
  display: inline-flex; align-items: center; gap: 6px; margin-top: 8px;
  font-size: 13.5px; font-weight: 600; color: var(--accent); text-decoration: none;
}
.v-cta .arrow { transition: transform var(--t-fast); }
.vehicle:hover .v-cta .arrow { transform: translateX(3px); }
.vehicles-note {
  margin-top: 24px; padding: 16px 20px;
  background: var(--surface); border: 1px solid var(--border);
  border-radius: var(--r-md); display: flex; gap: 12px;
  font-size: 13px; line-height: 1.5; color: var(--text-2);
}
.vehicles-note svg { flex: 0 0 auto; color: var(--accent); margin-top: 2px; }

/* ─── CTA Banner ─── */
.cta-banner {
  position: relative; background: var(--surface); border: 1px solid var(--border);
  border-radius: var(--r-lg); padding: clamp(28px, 4vw, 56px);
  display: grid; grid-template-columns: 1.4fr 1fr;
  gap: clamp(28px, 4vw, 56px); overflow: hidden; isolation: isolate; align-items: center;
}
.cta-banner::before {
  content:''; position: absolute; inset: 0;
  background:
    radial-gradient(60% 100% at 100% 0%, var(--accent-soft), transparent 60%),
    radial-gradient(50% 100% at 0% 100%, color-mix(in srgb, var(--accent) 10%, transparent), transparent 60%);
  z-index: -1; pointer-events: none;
}
@media (max-width: 860px) { .cta-banner { grid-template-columns: 1fr; } }

.cta-copy { display: flex; flex-direction: column; gap: 16px; align-items: flex-start; }
.cta-list {
  list-style: none; display: flex; flex-direction: column; gap: 10px; margin: 4px 0 8px;
}
.cta-list li {
  display: flex; align-items: center; gap: 10px; color: var(--text-2); font-size: 14.5px;
}
.cta-list li svg { color: var(--accent); flex: 0 0 auto; }
.cta-actions { display: flex; flex-wrap: wrap; gap: 12px; margin-top: 8px; }
.cta-side { align-self: stretch; display: flex; align-items: center; }
.cta-meta { display: grid; gap: 12px; width: 100%; }
.cta-metric {
  background: var(--bg); border: 1px solid var(--border);
  border-radius: var(--r-md); padding: 18px 20px; display: flex; flex-direction: column; gap: 4px;
}
.cta-metric .v {
  font-family: var(--font-alt); font-weight: 800;
  font-size: clamp(22px, 2.6vw, 30px); line-height: 1; letter-spacing: -.02em; color: var(--accent);
}
.cta-metric .k { font-size: 13px; color: var(--text-2); line-height: 1.4; }

/* ─── Button arrow ─── */
.btn .arrow { transition: transform var(--t-fast); }
.btn:hover .arrow { transform: translateX(3px); }
</style>
