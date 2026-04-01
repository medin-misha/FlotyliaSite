<script setup>
const platforms = [
  {
    key: 'bolt',
    logo: '/bolt.png',
    alt: 'Bolt Food',
    buttonKey: 'bolt-select.button',
    buttonClass: 'mobile-platform-button--bolt',
    cardClass: 'mobile-platform-card--bolt',
    route: '/form/bolt',
    featureKeys: [
      'bolt-select.platform-features.0',
      'bolt-select.platform-features.1',
      'bolt-select.platform-features.2',
      'bolt-select.platform-features.3',
    ],
    detailKeys: [
      'bolt-select.platform-details.0',
      'bolt-select.indent',
      'bolt-select.platform-details.1',
    ],
  },
  {
    key: 'foodora',
    logo: '/foodora.png',
    alt: 'Foodora',
    buttonKey: 'foodora-select.button',
    buttonClass: 'mobile-platform-button--foodora',
    cardClass: 'mobile-platform-card--foodora',
    route: '/form/foodora',
    featureKeys: [
      'foodora-select.platform-features.0',
      'foodora-select.platform-features.1',
      'foodora-select.platform-features.2',
      'foodora-select.platform-features.3',
    ],
    detailKeys: [
      'foodora-select.platform-details.0',
      'foodora-select.platform-details.1',
    ],
  },
]
</script>

<template>
  <div class="mobile-select-platform">
    <h1 class="app-section-heading mobile-select-platform-title">
      {{ $t('select-platform-title') }}
    </h1>

    <div class="mobile-platform-list">
      <section
        v-for="platform in platforms"
        :key="platform.key"
        class="mobile-platform"
      >
        <img
          :src="platform.logo"
          :alt="platform.alt"
          class="mobile-platform-logo"
        />

        <div class="mobile-platform-card" :class="platform.cardClass">
          <div class="mobile-platform-features">
            <p
              v-for="featureKey in platform.featureKeys"
              :key="featureKey"
            >
              {{ $t(featureKey) }}
            </p>
          </div>

          <div class="mobile-platform-details">
            <p
              v-for="detailKey in platform.detailKeys"
              :key="detailKey"
              :class="{ 'mobile-platform-details-indent': detailKey.includes('indent') }"
            >
              {{ $t(detailKey) }}
            </p>
          </div>
        </div>

        <button
          type="button"
          class="mobile-platform-button app-pill-button app-fade-transition app-alt-button-text"
          @click="$router.push(platform.route)"
          :class="platform.buttonClass"
        >
          {{ $t(platform.buttonKey) }}
        </button>
      </section>
    </div>
  </div>
</template>

<style scoped>
.mobile-select-platform {
  width: 100%;
  padding: 16px 12px 32px;
}

.mobile-select-platform-title {
  margin: 0;
  text-align: center;
  font-size: clamp(26px, 8.5vw, 40px);
  line-height: 1.08;
}

.mobile-platform-list {
  margin-top: 22px;
  display: flex;
  flex-direction: column;
  gap: 26px;
}

.mobile-platform {
  display: flex;
  flex-direction: column;
  align-items: stretch;
}

.mobile-platform-logo {
  align-self: center;
  height: 44px;
  width: auto;
  margin-bottom: 14px;
}

.mobile-platform-card {
  width: 100%;
  border-radius: 18px;
  padding: 16px 16px 18px;
  background-color: #fff;
}

.mobile-platform-card--bolt {
  border: 2px solid var(--bolt-color);
}

.mobile-platform-card--foodora {
  border: 2px solid var(--foodora-color);
}

.mobile-platform-features {
  display: flex;
  flex-direction: column;
  gap: 4px;
  margin-bottom: 12px;
}

.mobile-platform-features p,
.mobile-platform-details p {
  margin: 0;
  color: var(--color-text);
}

.mobile-platform-features p {
  font-weight: 400;
  font-size: clamp(15px, 4.8vw, 19px);
  line-height: 1.28;
}

.mobile-platform-details {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.mobile-platform-details p {
  font-weight: 400;
  font-size: clamp(14px, 4.4vw, 17px);
  line-height: 1.26;
}

.mobile-platform-details-indent {
  padding-left: 18px;
}

.mobile-platform-button {
  width: 100%;
  margin-top: 14px;
  padding: 14px 18px;
  color: var(--brand-text-color);
  font-size: clamp(15px, 4.8vw, 20px);
}

.mobile-platform-button:hover {
  opacity: 0.9;
}

.mobile-platform-button--bolt {
  background-color: var(--bolt-color);
}

.mobile-platform-button--foodora {
  background-color: var(--foodora-color);
}
</style>
