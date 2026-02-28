<script setup>
import { useI18n } from "vue-i18n"

const { t } = useI18n({useScope: "global"})
</script>

<template>
  <div class="select-platform">
    <h2>{{ t("select-platform-title") }}</h2>

    <div class="platforms">
      <div class="platform bolt">
        <img src="/bolt.png" alt="Bolt Food" class="platform-logo" />

        <div class="platform-card">
          <div class="platform-features">
            <p>{{ $t("bolt-select.platform-features.0") }}</p>
            <p>{{ $t("bolt-select.platform-features.1") }}</p>
            <p>{{ $t("bolt-select.platform-features.2") }}</p>
            <p>{{ $t("bolt-select.platform-features.3") }}</p>
          </div>
          <div class="platform-details">
            <p>{{ $t("bolt-select.platform-details.0") }}</p>
            <p class="indent">{{ $t("bolt-select.indent") }}</p>
            <p>{{ $t("bolt-select.platform-details.1") }}</p>
          </div>
        </div>

        <button class="btn-bolt" @click="$router.push('/form/bolt')">{{ $t("bolt-select.button") }}</button>
      </div>

      <div class="platform foodora">
        <img src="/foodora.png" alt="Foodora" class="platform-logo" />

        <div class="platform-card">
          <div class="platform-features">
            <p>{{ $t("foodora-select.platform-features.0") }}</p>
            <p>{{ $t("foodora-select.platform-features.1") }}</p>
            <p>{{ $t("foodora-select.platform-features.2") }}</p>
            <p>{{ $t("foodora-select.platform-features.3") }}</p>
          </div>
          <div class="platform-details">
            <p>{{ $t("foodora-select.platform-details.0") }}</p>
            <p>{{ $t("foodora-select.platform-details.1") }}</p>
          </div>
        </div>

        <button class="btn-foodora" @click="$router.push('/form/foodora')">{{ $t("foodora-select.button") }}</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.select-platform {
  padding: 40px 0;
}

h2 {
  font-family: 'Montserrat', sans-serif;
  font-weight: 600;
  font-size: 32px;
  line-height: 100%;
  letter-spacing: 0%;
  color: var(--color-text);
  text-align: center;
  margin: 0 0 40px 0;
}

.platforms {
  display: flex;
  width: 100%;
  gap: 15%;
  justify-content: center;
}

.platform {
  display: flex;
  flex-direction: column;
  align-items: center;
  flex: 1;
  max-width: 650px;
  min-width: 400px;
}

.platform-logo {
  height: 60px;
  width: auto;
  margin-bottom: 24px;
}

.platform-card {
  width: clamp(400px, 100%, 650px);
  height: 100%;
  border-radius: 16px;
  padding: 24px 28px;
  margin-bottom: 24px;
}

.bolt .platform-card {
  border: 2px solid var(--bolt-color);
}

.foodora .platform-card {
  border: 2px solid var(--foodora-color);
}

.platform-features {
  margin-bottom: 20px;
}

.platform-features p {
  font-family: 'Montserrat', sans-serif;
  font-weight: 400;
  font-size: 20px;
  line-height: 160%;
  letter-spacing: 0%;
  color: var(--color-text);
  margin: 0;
}

.platform-details p {
  font-family: 'Montserrat', sans-serif;
  font-weight: 400;
  font-size: 18px;
  line-height: 160%;
  letter-spacing: 0%;
  color: var(--color-text);
  margin: 0;
}

.platform-details .indent {
  padding-left: 24px;
}

button {
  width: clamp(400px, 100%, 650px);
  font-family: 'Montserrat Alternates', sans-serif;
  font-weight: 600;
  font-size: 20px;
  line-height: 100%;
  letter-spacing: 0%;
  color: var(--brand-text-color);
  border: none;
  border-radius: 30px;
  padding: 16px 32px;
  cursor: pointer;
  transition: opacity 0.2s ease;
}

button:hover {
  opacity: 0.9;
}

.btn-bolt {
  background-color: var(--bolt-color);
}

.btn-foodora {
  background-color: var(--foodora-color);
}
</style>
