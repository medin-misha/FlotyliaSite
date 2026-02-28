<script setup>
import { reactive, ref, computed, markRaw } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useI18n } from "vue-i18n"
import APIPosts from '../api/posts'

const route = useRoute()
const router = useRouter()
const { t } = useI18n({ useScope: "global" })
// Reactive form data
const formData = reactive({
  name: '',
  phone: '',
  email: '',
  city: '',
  birth_date: '',
  address: '',
  desired_transport: '',
  how_found_it: '',
  invoice: '',
  stay_type: '',
  contactPlatform: '',
  contactValue: '',
  work_in: route.params.company + "?",
  consent: false,
})

// Files storage
const files = ref([])
const fileInputRef = ref(null)

// Platform selection logic
const contactPlaceholder = computed(() => {
  if (formData.contactPlatform === 'telegram') return '@username'
  if (formData.contactPlatform === 'whatsapp') return '+420...'
  return ''
})

const isContactDisabled = computed(() => !formData.contactPlatform)

function selectPlatform(platform) {
  if (formData.contactPlatform === platform) {
    formData.contactPlatform = ''
    formData.contactValue = ''
  } else {
    formData.contactPlatform = platform
    formData.contactValue = ''
  }
}

// File upload
function triggerFileUpload() {
  fileInputRef.value?.click()
}

function handleFileChange(event) {
  const selected = Array.from(event.target.files)
  files.value.push(...selected)
  event.target.value = ''
}

// Submit
async function submitForm() {
  if (!formData.consent) {
    alert(t('form.alert.consent'))
    return
  }
  if (formData.contactPlatform === 'telegram') {
    formData.telegram = formData.contactValue
  }
  if (formData.contactPlatform === 'whatsapp') {
    formData.whatsapp = formData.contactValue
  }
  delete formData.consent
  delete formData.contactPlatform
  delete formData.contactValue
  console.log('Form Data:', { ...formData })
  console.log('Files:', files.value)
  const user = await APIPosts.createPost(formData, "/users")
  for (const file of files.value) {
    const file_instance = await APIPosts.createFile(file)
    const file_id = file_instance.data.id
    const user_id = user.data.id
    await APIPosts.createPost({ file_id, user_id, description: "Document" }, "/documents")
  }
  router.push(`/success/${route.params.company}`)
}
</script>

<template>
  <div class="form-page">
    <form class="form-container" @submit.prevent="submitForm">
      <!-- Header -->
      <div class="form-header">
        <h2>{{ $t("form.header") }}</h2>
        <img :src="route.params.company === 'bolt' ? '/bolt.png' : '/foodora.png'" :alt="$t('form.logo-alt')" class="bolt-logo" />
      </div>

      <!-- Section 1: General info -->
      <div class="section-title">
        <span class="section-number">1.</span>
        <span class="section-text">{{ $t("form.section1.title") }}</span>
      </div>

      <!-- Input Fields -->
      <div class="field-group">
        <label>{{ $t("form.fields.name") }}</label>
        <input type="text" v-model="formData.name" required />
      </div>

      <div class="field-group">
        <label>{{ $t("form.fields.phone") }}</label>
        <input type="tel" v-model="formData.phone" :placeholder="$t('form.placeholders.phone')" required />
      </div>

      <div class="field-group">
        <label>{{ $t("form.fields.email") }}</label>
        <input type="email" v-model="formData.email" required />
      </div>

      <div class="field-group">
        <label>{{ $t("form.fields.city") }}</label>
        <input type="text" v-model="formData.city" />
      </div>

      <div class="field-group">
        <label>{{ $t("form.fields.birth_date") }}</label>
        <input type="date" v-model="formData.birth_date" />
      </div>

      <div class="field-group">
        <label>{{ $t("form.fields.address") }}</label>
        <input type="text" v-model="formData.address" />
      </div>

      <div class="field-group">
        <label>{{ $t("form.fields.desired_transport") }}</label>
        <input
          type="text"
          v-model="formData.desired_transport"
          :placeholder="$t('form.placeholders.transport')"
        />
      </div>

      <div class="field-group">
        <label>{{ $t("form.fields.how_found_it") }}</label>
        <input type="text" v-model="formData.how_found_it" />
      </div>

      <div class="field-group">
        <label>{{ $t("form.fields.invoice") }}</label>
        <input
          type="text"
          v-model="formData.invoice"
          :placeholder="$t('form.placeholders.invoice')"
        />
      </div>

      <div class="field-group">
        <label>{{ $t("form.fields.stay_type") }}</label>
        <input type="text" v-model="formData.stay_type" />
      </div>

      <!-- Platform selection -->
      <div class="platform-section">
        <p class="platform-label">{{ $t("form.platform.label") }}</p>

        <div class="checkbox-group">
          <label class="checkbox-item" @click.prevent="selectPlatform('telegram')">
            <span
              class="custom-checkbox"
              :class="{ checked: formData.contactPlatform === 'telegram' }"
            ></span>
            <span>Telegram</span>
          </label>

          <label class="checkbox-item" @click.prevent="selectPlatform('whatsapp')">
            <span
              class="custom-checkbox"
              :class="{ checked: formData.contactPlatform === 'whatsapp' }"
            ></span>
            <span>WhatsApp</span>
          </label>
        </div>

        <div class="field-group">
          <input
            type="text"
            v-model="formData.contactValue"
            :placeholder="contactPlaceholder"
            :disabled="isContactDisabled"
            :class="{ 'input-disabled': isContactDisabled }"
          />
        </div>
      </div>

      <!-- Section 2: Documents -->
      <div class="section-title section-documents">
        <div class="section-title-left">
          <span class="section-number">2.</span>
          <span class="section-text">{{ $t("form.section2.title") }}</span>
        </div>
        <button type="button" class="upload-btn" @click="triggerFileUpload">{{ $t("form.documents.upload") }}</button>
        <input
          type="file"
          ref="fileInputRef"
          multiple
          @change="handleFileChange"
          class="hidden-file-input"
        />
      </div>

      <!-- Uploaded files list -->
      <div v-if="files.length" class="files-list">
        <div v-for="(file, index) in files" :key="index" class="file-item">
          {{ file.name }}
        </div>
      </div>

      <!-- Document description -->
      <p class="doc-description">
        {{ $t("form.documents.passport") }}<br />
        {{ $t("form.documents.or") }}<br />
        {{ $t("form.documents.residence_permit") }}
      </p>

      <!-- Submit button -->
      <button type="submit" :class="(route.params.company === 'bolt' ? 'submit-btn bolt' : 'submit-btn foodora')">
        {{ $t("form.submit") }}
      </button>

      <!-- Consent checkbox -->
      <div class="consent-row">
        <input
          type="checkbox"
          id="consent"
          v-model="formData.consent"
          class="consent-checkbox"
        />
        <label for="consent" class="consent-label">
          {{ $t("form.consent.label") }}
        </label>
      </div>
    </form>
  </div>
</template>

<style scoped>
.form-page {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 40px 20px 60px;
}

.form-container {
  width: 100%;
  max-width: 660px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

/* ---- Header ---- */
.form-header {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 8px;
}

.form-header h2 {
  font-family: 'Montserrat', sans-serif;
  font-weight: 700;
  font-size: 28px;
  line-height: 100%;
  margin: 0;
  color: var(--color-text);
}

.bolt-logo {
  height: 40px;
  width: auto;
  object-fit: contain;
}

/* ---- Section titles ---- */
.section-title {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-top: 16px;
  margin-bottom: 4px;
}

.section-number {
  font-family: 'Mulish', sans-serif;
  font-weight: 500;
  font-size: 40px;
  line-height: 100%;
  color: var(--brand-color);
}

.section-text {
  font-family: 'Montserrat', sans-serif;
  font-weight: 500;
  font-size: 24px;
  line-height: 100%;
  color: var(--color-text);
}

/* ---- Fields ---- */
.field-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.field-group label {
  font-family: 'Montserrat', sans-serif;
  font-weight: 500;
  font-size: 15px;
  line-height: 100%;
  color: var(--color-text);
}

.field-group input {
  font-family: 'Montserrat', sans-serif;
  font-size: 15px;
  padding: 12px 16px;
  border: 1.5px solid #ccc;
  border-radius: 50px;
  outline: none;
  transition: border-color 0.2s ease;
  width: 100%;
  box-sizing: border-box;
}

.field-group input:focus {
  border-color: var(--brand-color);
}

.field-group input::placeholder {
  color: #aaa;
}

.input-disabled {
  background-color: #f5f5f5;
  cursor: not-allowed;
  opacity: 0.6;
}

/* ---- Platform section ---- */
.platform-section {
  margin-top: 8px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.platform-label {
  font-family: 'Montserrat', sans-serif;
  font-weight: 500;
  font-size: 15px;
  margin: 0;
  color: var(--color-text);
}

.checkbox-group {
  display: flex;
  gap: 24px;
}

.checkbox-item {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  font-family: 'Montserrat', sans-serif;
  font-weight: 400;
  font-size: 15px;
  color: var(--color-text);
  user-select: none;
}

.custom-checkbox {
  width: 20px;
  height: 20px;
  border: 2px solid #ccc;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
  flex-shrink: 0;
}

.custom-checkbox.checked {
  background-color: var(--brand-color);
  border-color: var(--brand-color);
}

.custom-checkbox.checked::after {
  content: '✓';
  color: #fff;
  font-size: 14px;
  font-weight: 700;
}

/* ---- Documents section ---- */
.section-documents {
  justify-content: space-between;
  flex-wrap: wrap;
}

.section-title-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.upload-btn {
  font-family: 'Montserrat', sans-serif;
  font-weight: 600;
  font-size: 16px;
  color: #fff;
  background-color: var(--brand-color);
  border: none;
  border-radius: 30px;
  padding: 12px 40px;
  cursor: pointer;
  transition: opacity 0.2s ease, transform 0.15s ease;
}

.upload-btn:hover {
  opacity: 0.85;
  transform: translateY(-1px);
}

.hidden-file-input {
  display: none;
}

.files-list {
  display: flex;
  flex-direction: column;
  gap: 4px;
  padding: 8px 0;
}

.file-item {
  font-family: 'Montserrat', sans-serif;
  font-size: 14px;
  color: #555;
  padding: 6px 12px;
  background: #f9f9f9;
  border-radius: 6px;
}

/* ---- Doc description ---- */
.doc-description {
  font-family: 'Montserrat', sans-serif;
  font-weight: 400;
  font-size: 18px;
  line-height: 140%;
  color: var(--color-text);
  margin: 4px 0 16px;
}

/* ---- Submit button ---- */
.submit-btn {
  font-family: 'Montserrat Alternates', sans-serif;
  font-weight: 600;
  font-size: 20px;
  text-align: center;
  color: #fff;
  border: none;
  border-radius: 30px;
  padding: 18px;
  width: 100%;
  cursor: pointer;
  transition: opacity 0.2s ease, transform 0.15s ease, box-shadow 0.2s ease;
  margin-top: 8px;
}

.bolt {
  background: var(--bolt-color);
}

.foodora {
  background: var(--foodora-color);
}

.submit-btn:hover {
  opacity: 0.9;
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(52, 208, 134, 0.35);
}

/* ---- Consent ---- */
.consent-row {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-top: 8px;
}

.consent-checkbox {
  width: 18px;
  height: 18px;
  accent-color: var(--brand-color);
  cursor: pointer;
  flex-shrink: 0;
}

.consent-label {
  font-family: 'Actor', sans-serif;
  font-weight: 400;
  font-size: 16px;
  line-height: 100%;
  color: var(--color-text);
  cursor: pointer;
}
</style>
