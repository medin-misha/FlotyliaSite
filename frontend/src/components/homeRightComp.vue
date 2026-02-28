<script setup>
import { useI18n } from "vue-i18n"

const { tm } = useI18n({ useScope: "global" })
</script>

<template>
  <div class="home-right">
    <div class="logos">
      <img src="/bolt.png" alt="Bolt Food" class="logo-bolt" />
      <img src="/foodora.png" alt="Foodora" class="logo-foodora" />
    </div>

    <div class="how-to-start">
      <div class="how-to-start-header">
        <h2>{{ $t("how-to-start.title") }}</h2>
        <button @click="$router.push('/select-platform')">{{ $t("how-to-start.button") }}</button>
      </div>

      <ol class="steps-list">
        <li>
          <span class="step-number">1.</span>
          <span class="step-text">{{ $t("how-to-start.steps.0") }}<a @click="$router.push('/select-platform')">{{ $t("how-to-start.steps.1") }}</a></span>
        </li>
        <li>
          <span class="step-number">2.</span>
          <span class="step-text">{{ $t("how-to-start.steps.2") }}</span>
        </li>
        <li>
          <span class="step-number">3.</span>
          <span class="step-text">{{ $t("how-to-start.steps.3") }}</span>
        </li>
      </ol>
    </div>

    <div class="why-us">
      <div class="why-us-header" id="work">
        <h2>{{ $t("why-us.title") }}</h2>
        <a
          href="https://t.me/MFS_support"
          target="_blank"
          :aria-label="$t('why-us.support-link-aria')"
        >
          <img src="/MSGButton.svg" alt="" class="msg-icon" />
        </a>
      </div>

      <div class="why-us-list">
        <div class="why-us-item">
          <p>
            <strong>{{ $t("why-us.item1.title") }}</strong><br />
            {{ $t("why-us.item1.line1") }}<br />
            {{ $t("why-us.item1.line2") }}<br />
            {{ $t("why-us.item1.line3") }}
          </p>
        </div>

        <div class="why-us-item">
          <p>
            <strong>{{ $t("why-us.item2.title") }}</strong>
            {{ $t("why-us.item2.line1") }}<br />
            {{ $t("why-us.item2.line2") }}
          </p>
        </div>

        <div class="why-us-item">
          <p>
            <strong>{{ $t("why-us.item3.title") }}</strong>
            {{ $t("why-us.item3.line1") }}<br />
            {{ $t("why-us.item3.line2") }}
          </p>
        </div>
      </div>
    </div>

    <div class="transport" id="transport">
      <h2>{{ $t("transport-section.title") }}</h2>
      <div class="transport-grid">
        <img src="/transports/car.png" :alt="$t('transport-section.alts.car')" class="transport-car" />
        <img src="/transports/bike2.png" :alt="$t('transport-section.alts.bike2')" class="transport-bike2" />
        <img src="/transports/scooter.png" :alt="$t('transport-section.alts.scooter')" class="transport-scooter" />
        <img src="/transports/bike.png" :alt="$t('transport-section.alts.bike')" class="transport-bike" />
        <img src="/transports/motorcycle.png" :alt="$t('transport-section.alts.motorcycle')" class="transport-motorcycle" />
      </div>
    </div>

    <div class="no-transport">
      <h2>{{ $t("no-transport.title") }}</h2>
      <p>
        {{ $t("no-transport.text1") }}
      </p>
      <p>
        <strong>{{ $t("no-transport.text2-title") }}</strong><br />
        <template v-for="(item, idx) in tm('no-transport.text2-list')" :key="idx">
          • {{ item }}<br />
        </template>
      </p>
    </div>

    <div class="contacts">
      <h2>{{ $t("contacts.title") }}</h2>
      <p>
        {{ $t("contacts.text1-line1") }}<br />
        {{ $t("contacts.text1-line2") }}
      </p>
      <p>{{ $t("contacts.text2") }}</p>
    </div>
  </div>
</template>

<style scoped>
.home-right {
    max-width: 50%;
  color: var(--color-text);
  flex-shrink: 0;
}

.logos {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 40px;
  margin-bottom: 32px;
}

.logo-bolt {
  height: 40px;
  width: auto;
}

.logo-foodora {
  height: 40px;
  width: auto;
  margin-top: -15px;
}

.how-to-start {
  background-color: #fff;
  border-radius: 16px;
  padding: 0;
  /* box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08); */
}

.how-to-start-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 24px;
}

.how-to-start-header h2 {
  font-family: 'Montserrat', sans-serif;
  font-weight: 600;
  font-size: 32px;
  line-height: 100%;
  letter-spacing: 0%;
  color: var(--color-text);
  margin: 0;
}

.how-to-start-header button {
  font-family: 'Montserrat Alternates', sans-serif;
  font-weight: 600;
  font-size: 14px;
  line-height: 100%;
  letter-spacing: 0%;
  color: var(--brand-text-color);
  background-color: var(--brand-color);
  border: none;
  border-radius: 30px;
  padding: 12px 28px;
  cursor: pointer;
  white-space: nowrap;
  transition: opacity 0.2s ease;
}

.how-to-start-header button:hover {
  opacity: 0.9;
}

.steps-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.steps-list li {
  display: flex;
  align-items: baseline;
  gap: 12px;
}

.step-number {
  font-family: 'Mulish', sans-serif;
  font-weight: 500;
  font-size: 40px;
  line-height: 100%;
  letter-spacing: 0%;
  color: var(--brand-color);
}

.step-text {
  font-family: 'Montserrat', sans-serif;
  font-weight: 400;
  font-size: 18px;
  line-height: 100%;
  letter-spacing: 0%;
  color: var(--color-text);
}

.step-text a {
  color: var(--color-text);
  text-decoration: underline;
}

.step-text a:hover {
  opacity: 0.7;
}

.why-us {
  margin-top: 32px;
}

.why-us-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
}

.why-us-header h2 {
  font-family: 'Montserrat', sans-serif;
  font-weight: 600;
  font-size: 32px;
  line-height: 100%;
  letter-spacing: 0%;
  color: var(--color-text);
  margin: 0;
}

.msg-icon {
  width: 48px;
  height: 48px;
}

.why-us-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.why-us-item p {
  font-family: 'Montserrat', sans-serif;
  font-weight: 500;
  font-size: 18px;
  line-height: 140%;
  letter-spacing: 0%;
  color: var(--color-text);
  margin: 0;
  word-wrap: break-word;
  overflow-wrap: break-word;
}

.why-us-item strong {
  font-weight: 700;
}

.transport {
  margin-top: 40px;
  height: 500px;
}

.transport h2 {
  font-family: 'Montserrat', sans-serif;
  font-weight: 600;
  font-size: 32px;
  line-height: 100%;
  letter-spacing: 0%;
  color: var(--color-text);
  margin: 0 0 24px 0;
}

.transport-grid {
  display: grid;
  grid-template-columns: 1fr 1.4fr 1fr;
  grid-template-rows: 1fr 1fr;
  gap: 12px;
  transform: scale(0.8);
  transform-origin: top left;
}

.transport-grid img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 12px;
}

.transport-car {
  grid-column: 1;
  grid-row: 1;
  object-fit: contain !important;
  transform: scale(1.1);
}

.transport-bike2 {
  grid-column: 2;
  grid-row: 1 / 3;
}

.transport-scooter {
  grid-column: 3;
  grid-row: 1;
}

.transport-bike {
  grid-column: 1;
  grid-row: 2;
}

.transport-motorcycle {
  grid-column: 3;
  grid-row: 2;
  object-fit: contain !important;
  transform: scale(1.2);
}

.no-transport {
  margin-top: 40px;
}

.no-transport h2 {
  font-family: 'Montserrat', sans-serif;
  font-weight: 600;
  font-size: 32px;
  line-height: 100%;
  letter-spacing: 0%;
  color: var(--color-text);
  margin: 0 0 24px 0;
}

.no-transport p {
  font-family: 'Montserrat', sans-serif;
  font-weight: 400;
  font-size: 18px;
  line-height: 140%;
  letter-spacing: 0%;
  color: var(--color-text);
  margin: 0 0 16px 0;
}

.no-transport p strong {
  font-weight: 600;
}

.contacts {
  margin-top: 40px;
}

.contacts h2 {
  font-family: 'Montserrat', sans-serif;
  font-weight: 600;
  font-size: 32px;
  line-height: 100%;
  letter-spacing: 0%;
  color: var(--color-text);
  margin: 0 0 24px 0;
}

.contacts p {
  font-family: 'Montserrat', sans-serif;
  font-weight: 600;
  font-size: 24px;
  line-height: 140%;
  letter-spacing: 0%;
  color: var(--color-text);
  margin: 0 0 20px 0;
}
</style>
