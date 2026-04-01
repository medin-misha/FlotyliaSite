<script setup>
import { useI18n } from "vue-i18n"

const { t } = useI18n({useScope: "global"})
</script>

<template>
  <div class="home-left">
    <h1 id="about">
      {{ $t("main-header") }}
    </h1>

    <h2>{{ $t("main-subheader") }}</h2>

    <img class="deliver-img" src="/deliver.png" alt="Курьер на велосипеде" />

    <h3 class="app-section-heading transport-heading">{{ $t("transport-subheader") }}</h3>

    <div class="transport-intro">
      <p>{{ $t("transport-intro.line1") }}</p>
      <p>{{ $t("transport-intro.line2") }}</p>
      <p>{{ $t("transport-intro.line3") }}</p>
    </div>

    <div class="transport-list">
      <div class="transport-item">
        <h3 class="transport-title">{{ $t("transport.bike.title") }}</h3>
        <p>{{ $t("transport.bike.line1") }}</p>
        <p>{{ $t("transport.bike.line2") }}</p>
      </div>

      <div class="transport-item">
        <h3 class="transport-title">{{ $t("transport.ebike.title") }}</h3>
        <p>{{ $t("transport.ebike.line1") }}</p>
        <p>{{ $t("transport.ebike.line2") }}</p>
      </div>

      <div class="transport-item">
        <h3 class="transport-title">{{ $t("transport.escooter.title") }}</h3>
        <p>{{ $t("transport.escooter.line1") }}</p>
        <p>{{ $t("transport.escooter.line2") }}</p>
      </div>

      <div class="transport-item">
        <h3 class="transport-title">{{ $t("transport.car.title") }}</h3>
        <p>{{ $t("transport.car.line1") }}</p>
        <p>{{ $t("transport.car.line2") }}</p>
      </div>
    </div>

    <p class="transport-footnote">{{ $t("transport-footnote") }}</p>
  </div>
</template>

<style scoped>
.home-left {
  color: var(--color-text);
}

h1 {
  font-weight: 600;
  font-size: 45px;
  line-height: 100%;
  letter-spacing: 0%;
  color: var(--color-text);
  margin-bottom: 24px;
}

h2 {
  font-weight: 400;
  font-size: 32px;
  line-height: 100%;
  letter-spacing: 0%;
  color: var(--color-text);
  margin-bottom: 32px;
}

.deliver-img {
  width: 100%;
  max-width: 480px;
  border-radius: 12px;
  margin-bottom: 40px;
}

.transport-heading {
  margin-bottom: 16px;
}

.transport-intro {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 24px;
  font-weight: 400;
  font-size: 18px;
  line-height: 140%;
  color: var(--color-text);
}

.transport-footnote {
  margin-top: 16px;
  font-weight: 400;
  font-size: 15px;
  line-height: 140%;
  color: var(--color-text);
  opacity: 0.75;
}

.transport-list {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.transport-item {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.transport-title {
  font-weight: 500;
  font-size: 20px;
  line-height: 100%;
  letter-spacing: 0%;
  color: var(--color-text);
}

.transport-item p {
  font-weight: 400;
  font-size: 18px;
  line-height: 140%;
  letter-spacing: 0%;
  color: var(--color-text);
}
</style>
