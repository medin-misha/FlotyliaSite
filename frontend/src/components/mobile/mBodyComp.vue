<script setup>
import { useI18n } from 'vue-i18n'

const { tm } = useI18n({ useScope: 'global' })

const whyUsItems = [
  {
    titleKey: 'why-us.item1.title',
    lines: ['why-us.item1.line1', 'why-us.item1.line2', 'why-us.item1.line3'],
  },
  {
    titleKey: 'why-us.item2.title',
    lines: ['why-us.item2.line1', 'why-us.item2.line2'],
  },
  {
    titleKey: 'why-us.item3.title',
    lines: ['why-us.item3.line1', 'why-us.item3.line2'],
  },
]

const transportCards = [
  { src: '/transports/car.png', altKey: 'transport-section.alts.car' },
  { src: '/transports/bike2.png', altKey: 'transport-section.alts.bike2' },
  { src: '/transports/scooter.png', altKey: 'transport-section.alts.scooter' },
  { src: '/transports/motorcycle.png', altKey: 'transport-section.alts.motorcycle' },
  { src: '/transports/bike.png', altKey: 'transport-section.alts.bike' },
]

const transportTypes = [
  {
    titleKey: 'transport.bike.title',
    line1Key: 'transport.bike.line1',
    line2Key: 'transport.bike.line2',
  },
  {
    titleKey: 'transport.ebike.title',
    line1Key: 'transport.ebike.line1',
    line2Key: 'transport.ebike.line2',
  },
  {
    titleKey: 'transport.escooter.title',
    line1Key: 'transport.escooter.line1',
    line2Key: 'transport.escooter.line2',
  },
  {
    titleKey: 'transport.car.title',
    line1Key: 'transport.car.line1',
    line2Key: 'transport.car.line2',
  },
]
</script>

<template>
  <main class="mobile-body">
    <section class="mobile-hero">
      <h1 id="about">{{ $t('main-header') }}</h1>
      <p class="mobile-hero-copy">{{ $t('main-subheader') }}</p>

      <div class="mobile-platform-logos" aria-label="Platforms">
        <img src="/bolt.png" alt="Bolt Food" class="mobile-platform-logo mobile-platform-logo--bolt" />
        <img src="/foodora.png" alt="Foodora" class="mobile-platform-logo mobile-platform-logo--foodora" />
      </div>
    </section>

    <section class="mobile-start">
      <div class="mobile-start-head">
        <h2 class="app-section-heading">{{ $t('how-to-start.title') }}</h2>
        <button
          type="button"
          class="mobile-start-button app-pill-button app-fade-transition app-alt-button-text"
          @click="$router.push('/select-platform')"
        >
          {{ $t('how-to-start.button') }}
        </button>
      </div>

      <ol class="mobile-steps-list">
        <li>
          <span class="mobile-step-index">1.</span>
          <span class="mobile-step-text">
            {{ $t('how-to-start.steps.0') }}
            <a class="app-fade-transition" @click="$router.push('/select-platform')">
              {{ $t('how-to-start.steps.1') }}
            </a>
          </span>
        </li>
        <li>
          <span class="mobile-step-index">2.</span>
          <span class="mobile-step-text">{{ $t('how-to-start.steps.2') }}</span>
        </li>
        <li>
          <span class="mobile-step-index">3.</span>
          <span class="mobile-step-text">{{ $t('how-to-start.steps.3') }}</span>
        </li>
      </ol>

      <div class="mobile-support">
        <a
          href="https://t.me/MFS_support"
          target="_blank"
          rel="noreferrer"
          class="mobile-support-link app-fade-transition"
          :aria-label="$t('why-us.support-link-aria')"
        >
          <img src="/MSGButton.svg" alt="" />
        </a>
      </div>
      <img id="work" src="/deliver.png" alt="Courier" class="mobile-deliver-image" />
    </section>

    <section class="mobile-why-us">
      <h2 class="app-section-heading">{{ $t('why-us.title') }}</h2>

      <div class="mobile-why-us-list">
        <article
          v-for="item in whyUsItems"
          :key="item.titleKey"
          class="mobile-why-us-item"
        >
          <p class="mobile-why-us-title">{{ $t(item.titleKey) }}</p>
          <p
            v-for="lineKey in item.lines"
            :key="lineKey"
            class="mobile-why-us-line"
          >
            {{ $t(lineKey) }}
          </p>
        </article>
      </div>
    </section>
    
    <section class="mobile-transport" id="transport">
      <h2 class="app-section-heading">{{ $t('transport-section.title') }}</h2>

      <div class="mobile-transport-grid">
        <img
          v-for="card in transportCards"
          :key="card.src"
          :src="card.src"
          :alt="$t(card.altKey)"
        />
      </div>
    </section>

    <section class="mobile-no-transport">
      <h2 class="app-section-heading">{{ $t('no-transport.title') }}</h2>

      <p class="app-body-copy mobile-body-copy">{{ $t('no-transport.text1') }}</p>

      <div class="mobile-included-block">
        <p class="app-body-copy mobile-body-copy mobile-included-heading">
          {{ $t('no-transport.text2-title') }}
        </p>

        <p
          v-for="(item, index) in tm('no-transport.text2-list')"
          :key="index"
          class="app-body-copy mobile-body-copy mobile-included-line"
        >
          • {{ item }}
        </p>
      </div>
    </section>

    <section class="mobile-transport-types">
      <h2 class="app-section-heading">{{ $t('transport-subheader') }}</h2>

      <div class="mobile-transport-intro">
        <p>{{ $t('transport-intro.line1') }}</p>
        <p>{{ $t('transport-intro.line2') }}</p>
        <p>{{ $t('transport-intro.line3') }}</p>
      </div>

      <div class="mobile-transport-type-list">
        <div
          v-for="item in transportTypes"
          :key="item.titleKey"
          class="mobile-transport-type"
        >
          <p class="mobile-transport-type-title">{{ $t(item.titleKey) }}</p>
          <p class="mobile-transport-type-line">{{ $t(item.line1Key) }}</p>
          <p class="mobile-transport-type-line">{{ $t(item.line2Key) }}</p>
        </div>
      </div>

      <p class="mobile-transport-footnote">{{ $t('transport-footnote') }}</p>
    </section>

    <section class="mobile-contacts" id="contacts">
      <h2 class="app-section-heading">{{ $t('contacts.title') }}</h2>
      <p class="mobile-contacts-copy">
        {{ $t('contacts.text1-line1') }}<br />
        {{ $t('contacts.text1-line2') }}
      </p>
      <p class="mobile-contacts-copy mobile-contacts-copy--strong">
        {{ $t('contacts.text2') }}
      </p>
    </section>
  </main>
</template>

<style scoped>
.mobile-body {
  width: 100%;
  box-sizing: border-box;
  background-color: #fff;
}

.mobile-body section {
  padding: 0 12px;
}

.mobile-hero {
  padding-top: 10px;
}

.mobile-hero h1 {
  font-weight: 600;
  font-size: clamp(20px, 11vw, 35px);
  line-height: 1.04;
  color: var(--color-text);
}

.mobile-hero-copy {
  margin-top: 14px;
  font-weight: 400;
  font-size: clamp(16px, 5.6vw, 24px);
  line-height: 1.15;
  color: #404040;
}

.mobile-platform-logos {
  margin-top: 18px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 6px;
  flex-wrap: wrap;
}

.mobile-platform-logo {
  height: auto;
}

.mobile-platform-logo--bolt {
  width: min(42vw, 160px);
}

.mobile-platform-logo--foodora {
  width: min(48vw, 185px);
  margin-top: -10px;
}

.mobile-start {
  margin-top: 26px;
}

.mobile-start-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.mobile-start-head h2,
.mobile-why-us h2,
.mobile-transport h2,
.mobile-no-transport h2,
.mobile-transport-types h2,
.mobile-contacts h2 {
  font-size: clamp(18px, 7vw, 32px);
  line-height: 1.08;
}

.mobile-start-button {
  flex-shrink: 0;
  padding: 12px 16px;
  background-color: var(--brand-color);
  color: var(--brand-text-color);
  font-size: clamp(13px, 4.1vw, 18px);
}

.mobile-start-button:hover {
  opacity: 0.9;
}

.mobile-steps-list {
  list-style: none;
  margin: 20px 0 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.mobile-steps-list li {
  display: grid;
  grid-template-columns: 30px 1fr;
  align-items: start;
  gap: 0;
}

.mobile-step-index {
  font-family: 'Mulish', sans-serif;
  font-weight: 500;
  font-size: clamp(24px, 8vw, 40px);
  line-height: 1;
  color: var(--brand-color);
}

.mobile-step-text {
  padding-top: 3px;
  font-weight: 400;
  font-size: clamp(15px, 5.2vw, 22px);
  line-height: 1.15;
  color: var(--color-text);
}

.mobile-step-text a {
  color: inherit;
  text-decoration: underline;
  cursor: pointer;
}

.mobile-step-text a:hover {
  opacity: 0.7;
}

.mobile-support {
  display: flex;
  justify-content: flex-end;
  margin-top: 18px;
}

.mobile-support-link {
  display: inline-flex;
  align-items: center;
}

.mobile-support-link:hover {
  opacity: 0.8;
}

.mobile-support-link img {
  width: 44px;
  height: 44px;
}

.mobile-deliver-image {
  display: block;
  width: 100%;
  margin-top: 8px;
  border-radius: 22px;
  object-fit: cover;
}

.mobile-why-us,
.mobile-transport,
.mobile-no-transport,
.mobile-transport-types,
.mobile-contacts {
  margin-top: 28px;
}

.mobile-why-us-list {
  margin-top: 18px;
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.mobile-why-us-item {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.mobile-why-us-title,
.mobile-why-us-line {
  margin: 0;
  font-size: clamp(15px, 5.1vw, 22px);
  line-height: 1.1;
  color: var(--color-text);
}

.mobile-why-us-title {
  font-weight: 500;
}

.mobile-why-us-line {
  font-weight: 400;
}

.mobile-transport-grid {
  margin-top: 14px;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  grid-template-areas:
    'car bike2 scooter'
    'motorcycle bike2 bike';
  gap: 6px;
}

.mobile-transport-grid img {
  width: 100%;
  height: 94px;
  border-radius: 8px;
  object-fit: cover;
  background-color: #f5f5f5;
}

.mobile-transport-grid img:nth-child(1) {
  grid-area: car;
}

.mobile-transport-grid img:nth-child(2) {
  grid-area: bike2;
  height: 194px;
}

.mobile-transport-grid img:nth-child(3) {
  grid-area: scooter;
}

.mobile-transport-grid img:nth-child(4) {
  grid-area: motorcycle;
}

.mobile-transport-grid img:nth-child(5) {
  grid-area: bike;
}

.mobile-body-copy {
  font-size: clamp(15px, 5vw, 20px);
  line-height: 1.1;
}

.mobile-no-transport > .mobile-body-copy {
  margin-top: 14px;
}

.mobile-included-block {
  margin-top: 16px;
}

.mobile-included-heading {
  font-weight: 500;
  margin-bottom: 6px;
}

.mobile-included-line {
  margin-bottom: 2px;
}

.mobile-transport-type-list {
  margin-top: 18px;
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.mobile-transport-intro {
  margin-top: 14px;
  display: flex;
  flex-direction: column;
  gap: 6px;
  font-weight: 400;
  font-size: clamp(14px, 4.6vw, 18px);
  line-height: 1.4;
  color: var(--color-text);
}

.mobile-transport-type-title {
  margin: 0;
  display: inline-block;
  width: fit-content;
  padding-bottom: 2px;
  border-bottom: 1px solid currentColor;
  font-weight: 500;
  font-size: clamp(18px, 6vw, 24px);
  line-height: 1.1;
  color: var(--color-text);
}

.mobile-transport-type-line {
  margin: 0;
  font-weight: 400;
  font-size: clamp(14px, 4.6vw, 18px);
  line-height: 1.4;
  color: var(--color-text);
}

.mobile-transport-footnote {
  margin-top: 14px;
  font-weight: 400;
  font-size: clamp(13px, 4vw, 16px);
  line-height: 1.4;
  color: var(--color-text);
  opacity: 0.75;
}

.mobile-contacts-copy {
  margin: 18px 0 0;
  font-weight: 600;
  font-size: clamp(17px, 5.4vw, 24px);
  line-height: 1.14;
  color: var(--color-text);
}

.mobile-contacts-copy--strong {
  margin-top: 18px;
}


</style>
