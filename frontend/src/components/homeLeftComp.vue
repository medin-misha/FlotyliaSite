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

    <h3>{{ $t("transport-subheader") }}</h3>

    <div class="transport-list">
      <div class="transport-item">
        <p class="transport-title">{{ $t("transport.bike.title") }}</p>
        <ul>
          <li>{{ $t("transport.bike.price") }}</li>
          <li>{{ $t("transport.bike.service") }}</li>
          <li>{{ $t("transport.bike.included") }}</li>
        </ul>
      </div>

      <div class="transport-item">
        <p class="transport-title">
          {{ $t("transport.ebike.title") }}<br />{{ $t("transport.ebike.model1") }}
        </p>
        <ul>
          <li>{{ $t("transport.ebike.price1") }}</li>
          <li>{{ $t("transport.ebike.price_month1") }}</li>
          <li>
            {{ $t("transport.ebike.included") }}
          </li>
          <li>{{ $t("transport.ebike.service") }}</li>
        </ul>
      </div>

      <div class="transport-item">
        <p class="transport-title">
          {{ $t("transport.ebike.title") }}<br />{{ $t("transport.ebike.model2") }}
        </p>
        <ul>
          <li>{{ $t("transport.ebike.amenities") }}</li>
          <li>{{ $t("transport.ebike.price2") }}</li>
          <li>{{ $t("transport.ebike.price_month2") }}</li>
          <li>
            {{ $t("transport.ebike.included") }}
          </li>
          <li>{{ $t("transport.ebike.service") }}</li>
        </ul>
      </div>

      <div class="transport-item">
        <p class="transport-title">{{ $t("transport.escooter.title") }}</p>
        <ul>
          <li>{{ $t("transport.escooter.price") }}</li>
          <li>{{ $t("transport.escooter.included") }}</li>
          <li>{{ $t("transport.escooter.service") }}</li>
        </ul>
      </div>

      <div class="transport-item">
        <p class="transport-title">{{ $t("transport.scooter.title") }}</p>
        <ul>
          <li>{{ $t("transport.scooter.price") }}</li>
          <li>{{ $t("transport.scooter.deposit") }}</li>
          <li>{{ $t("transport.scooter.service") }}</li>
        </ul>
      </div>

      <div class="transport-item">
        <p class="transport-title">{{ $t("transport.car.title") }}</p>
        <ul>
          <li>{{ $t("transport.car.categories") }}</li>
          <li>{{ $t("transport.car.price") }}</li>
          <li>{{ $t("transport.car.deposit") }}</li>
          <li>{{ $t("transport.car.discount") }}</li>
        </ul>
      </div>
    </div>
  </div>
</template>

<style scoped>
.home-left {
  color: var(--color-text);
}

h1 {
  font-family: 'Montserrat', sans-serif;
  font-weight: 600;
  font-size: 45px;
  line-height: 100%;
  letter-spacing: 0%;
  color: var(--color-text);
  margin-bottom: 24px;
}

h2 {
  font-family: 'Montserrat', sans-serif;
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

h3 {
  font-family: 'Montserrat', sans-serif;
  font-weight: 600;
  font-size: 32px;
  line-height: 100%;
  letter-spacing: 0%;
  color: var(--color-text);
  margin-bottom: 24px;
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
  font-family: 'Montserrat', sans-serif;
  font-weight: 500;
  font-size: 20px;
  line-height: 100%;
  letter-spacing: 0%;
  color: var(--color-text);
}

.transport-item ul {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.transport-item li {
  font-family: 'Montserrat', sans-serif;
  font-weight: 400;
  font-size: 18px;
  line-height: 100%;
  letter-spacing: 0%;
  color: var(--color-text);
}

.transport-item li::before {
  content: '• ';
}
</style>
