<script setup>
import { ref } from 'vue'
import { useI18n } from "vue-i18n"
import { defaultLocale } from "../i18n"
import { useLocaleStore } from "../stores/localeStore"
const { t, locale } = useI18n({useScope: "global"})
const localeStore = useLocaleStore()

const selectedLang = ref(localeStore.locale)
const languages = [
  { value: 'ru', label: 'Рус.' },
  { value: 'cz', label: 'Čes.' },
  { value: 'en', label: 'Eng.' },
]
const loadLanguageAsync = (lang) => {
  localeStore.setLocale(lang)
  locale.value = localeStore.locale
 console.log(lang)
}
</script>

<template>
  <header>
    <div>
      <nav>
        <a href="#about" @click="$router.push('/')">{{ $t("nav-bar.about") }}</a>
        <a href="#work" @click="$router.push('/')">{{ $t("nav-bar.work-with-us") }}</a>
        <a href="#transport" @click="$router.push('/')">{{ $t("nav-bar.transport") }}</a>
        <a href="#footer" @click="$router.push('/')">{{ $t("nav-bar.contacts") }}</a>
      </nav>

      <div>
        <button @click="$router.push('/select-platform')">{{ $t("buttons.connect-button") }}</button>
        <img src="/MiniLogo.svg" alt="MFS Logo" />
      </div>
      <select v-model="selectedLang" @change="loadLanguageAsync(selectedLang)" >
          <option
            v-for="lang in languages"
            :key="lang.value"
            :value="lang.value"
          >
            {{ lang.label }}
          </option>
        </select>
    </div>
  </header>
</template>

<style scoped>
header {
  background-color: var(--brand-color);
  width: 100%;
  min-width: 700px;
  padding: 0 40px;
  box-sizing: border-box;
}

header > div {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 40px;
  height: 60px;
  max-width: 1400px;
  margin: 0 auto;
}

nav {
  display: flex;
  align-items: center;
  gap: 32px;
}

nav a {
  font-family: 'Montserrat', sans-serif;
  font-weight: 600;
  font-size: 17px;
  line-height: 100%;
  letter-spacing: 0%;
  color: var(--brand-text-color);
  text-decoration: none;
  white-space: nowrap;
  transition: opacity 0.2s ease;
}

nav a:hover {
  opacity: 0.8;
}

nav + div {
  display: flex;
  align-items: center;
  gap: 24px;
}

button {
  font-family: 'Montserrat Alternates', sans-serif;
  font-weight: 600;
  font-size: 20px;
  line-height: 100%;
  letter-spacing: 0%;
  color: var(--brand-color);
  background-color: var(--brand-text-color);
  border: none;
  border-radius: 30px;
  padding: 12px 36px;
  cursor: pointer;
  white-space: nowrap;
  transition: opacity 0.2s ease;
}

button:hover {
  opacity: 0.9;
}

img {
  height: 36px;
  margin-top: -15px;
  width: auto;
}

select {
  font-family: 'Montserrat', sans-serif;
  font-weight: 600;
  font-size: 17px;
  line-height: 100%;
  color: var(--brand-color);
  background-color: var(--brand-text-color);
  border: none;
  border-radius: 30px;
  padding: 8px 16px;
  cursor: pointer;
  appearance: none;
  -webkit-appearance: none;
  -moz-appearance: none;
  outline: none;
  text-align: center;
  min-width: 70px;
}
</style>
