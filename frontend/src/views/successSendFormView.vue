<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { useI18n } from "vue-i18n"

const route = useRoute()
const { t, tm } = useI18n({ useScope: "global" })

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

const instructionLines = computed(() => {
  if (isBolt.value) {
    return tm('success.instructions.bolt')
  }
  return tm('success.instructions.foodora')
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
const passwordNote = computed(() => t('success.password-note'))
</script>

<template>
  <div class="success-page" :style="{ '--accent-color': accentColor }">
    <div class="success-container">
      <h2 class="success-title">
        {{ $t("success.title") }}
      </h2>

      <div class="step-block">
        <span class="step-number">3.</span>
        <div class="step-text">
          <p class="step-heading">
            <span class="step-label">{{ $t("success.step.label") }}</span>
            <span class="step-description">
              {{ $t("success.step.description") }}
            </span>
          </p>
          <p class="step-subtitle">
            {{ $t("success.step.subtitle") }}
          </p>
        </div>
      </div>

      <button type="button" class="cta-button" @click="downloadAll()">
        {{ $t("success.cta") }}
      </button>

      <div class="instructions">
        <p class="instructions-heading">{{ instructionHeading }}</p>
        <div class="instructions-body">
          <p v-for="line in instructionLines" :key="line">{{ line }}</p>
          <p v-if="isFoodora" class="instructions-note">{{ passwordNote }}</p>
        </div>
      </div>

      <p class="store-note">
        {{ $t("success.store-note") }}
      </p>
    </div>
  </div>
</template>

<style scoped>
.success-page {
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
  box-sizing: border-box;
}

.success-container {
  width: 100%;
  max-width: 1100px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 28px;
}

.success-title {
  margin: 0;
  font-family: 'Montserrat', sans-serif;
  font-weight: 500;
  font-size: 32px;
  line-height: 100%;
  letter-spacing: 0%;
  text-align: center;
  color: var(--color-text);
  padding: 0 16px;
}

.step-block {
  width: 100%;
  max-width: 940px;
  display: flex;
  gap: 16px;
  align-items: flex-start;
  justify-content: center;
  margin-top: 4px;
}

.step-number {
  font-family: 'Mulish', sans-serif;
  font-weight: 500;
  font-size: 40px;
  line-height: 100%;
  letter-spacing: 0%;
  color: var(--brand-color);
  flex-shrink: 0;
}

.step-text {
  display: flex;
  flex-direction: column;
  gap: 6px;
  color: var(--color-text);
}

.step-heading {
  margin: 0;
  font-family: 'Montserrat', sans-serif;
  font-weight: 500;
  font-size: 18px;
  line-height: 100%;
  letter-spacing: 0%;
}

.step-subtitle {
  margin: 0;
  font-family: 'Montserrat', sans-serif;
  font-weight: 500;
  font-size: 18px;
  line-height: 100%;
  letter-spacing: 0%;
}

.step-label {
  font-family: 'Montserrat', sans-serif;
  font-weight: 500;
}

.step-description {
  font-family: 'Montserrat', sans-serif;
  font-weight: 500;
}

.cta-button {
  font-family: 'Montserrat Alternates', sans-serif;
  font-weight: 600;
  font-size: 20px;
  line-height: 100%;
  letter-spacing: 0%;
  color: #fff;
  background-color: var(--accent-color);
  border: none;
  border-radius: 32px;
  padding: 12px 18px;
  cursor: pointer;
  transition: transform 0.15s ease, box-shadow 0.2s ease, opacity 0.2s ease;
  /* width: 600px; */
  width: clamp(480px, 55vw, 700px);
}

.cta-button:hover {
  opacity: 0.92;
  transform: translateY(-1px);
  box-shadow: 0 8px 22px rgba(0, 0, 0, 0.12);
}

.cta-button:active {
  transform: translateY(0);
  box-shadow: 0 5px 14px rgba(0, 0, 0, 0.12);
}

.instructions {
  width: 100%;
  max-width: 940px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  color: var(--color-text);
}

.instructions-heading {
  margin: 0;
  font-family: Montserrat;
  font-weight: 500;
  font-style: Medium;
  font-size: 18px;
  line-height: 100%;
  letter-spacing: 0%;
}

.instructions-body {
  display: flex;
  flex-direction: column;
}

.instructions-body p {
  margin: 0;
  font-family: Montserrat;
  font-weight: 400;
  font-style: Regular;
  font-size: 18px;
  line-height: 120%;
  letter-spacing: 0%;
}


.store-note {
  margin: 4px 0 0;
  font-family: 'Montserrat', sans-serif;
  font-weight: 300;
  font-size: 18px;
  line-height: 100%;
  letter-spacing: 0%;
  color: var(--color-text);
  width: 100%;
  max-width: 940px;
}

@media (max-width: 900px) {
  .success-page {
    padding: 40px 18px 64px;
  }

  .success-title {
    font-size: 28px;
  }

  .step-block {
    max-width: 100%;
  }

  .cta-button {
    width: 100%;
    max-width: 420px;
  }
}

@media (max-width: 640px) {
  .success-page {
    padding: 32px 16px 54px;
  }

  .success-container {
    gap: 22px;
  }

  .success-title {
    font-size: 24px;
  }

  .step-block {
    flex-direction: column;
    align-items: flex-start;
  }

  .step-number {
    font-size: 32px;
  }

  .step-heading,
  .step-subtitle,
  .instructions-heading,
  .instructions-body p,
  .store-note {
    font-size: 16px;
    line-height: 100%;
  }

  .cta-button {
    font-size: 18px;
  }
}
</style>
