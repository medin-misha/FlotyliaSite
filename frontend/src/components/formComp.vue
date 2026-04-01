<script setup>
import { reactive, ref, computed, watch } from 'vue'
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
  citizenship: '',
  invoice: '',
  contactPlatform: '',
  contactValue: '',
  work_in: route.params.company + "?",
  consent: false,
})

// Citizenship check
const isCzech = computed(() => formData.citizenship === 'cz')

// Files are required before submit
const hasRequiredFiles = computed(() => {
  if (!formData.citizenship) return false
  if (isCzech.value) return filesPassport.value.length > 0 && filesOP.value.length > 0
  return filesPassport.value.length > 0 && filesResidence.value.length > 0
})

// Files per zone
const filesOP = ref([])
const filesPassport = ref([])
const filesResidence = ref([])

// Clear files when citizenship changes
watch(() => formData.citizenship, () => {
  filesOP.value = []
  filesPassport.value = []
  filesResidence.value = []
})

// Drag state per zone
const dragging = reactive({ op: false, passport: false, residence: false })

// Hidden input refs
const inputOP = ref(null)
const inputPassport = ref(null)
const inputResidence = ref(null)

const isSubmitting = ref(false)

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
    formData.contactValue = platform === 'whatsapp' ? '+420' : ''
  }
}

watch(() => formData.contactValue, (val) => {
  if (formData.contactPlatform !== 'whatsapp') return
  if (!val.startsWith('+420')) {
    formData.contactValue = '+420'
  }
})

// Drop zone handlers
function addFiles(zone, newFiles) {
  if (zone === 'op') filesOP.value.push(...newFiles)
  else if (zone === 'passport') filesPassport.value.push(...newFiles)
  else if (zone === 'residence') filesResidence.value.push(...newFiles)
}

function onDrop(zone, event) {
  dragging[zone] = false
  addFiles(zone, Array.from(event.dataTransfer.files))
}

function onFileInput(zone, event) {
  addFiles(zone, Array.from(event.target.files))
  event.target.value = ''
}

function removeFile(zone, index) {
  if (zone === 'op') filesOP.value.splice(index, 1)
  else if (zone === 'passport') filesPassport.value.splice(index, 1)
  else if (zone === 'residence') filesResidence.value.splice(index, 1)
}

function triggerInput(zone) {
  if (zone === 'op') inputOP.value?.click()
  else if (zone === 'passport') inputPassport.value?.click()
  else if (zone === 'residence') inputResidence.value?.click()
}

function buildSubmitPayload() {
  const payload = { ...formData }

  if (payload.contactPlatform === 'telegram') {
    payload.telegram = payload.contactValue
  }
  if (payload.contactPlatform === 'whatsapp') {
    payload.whatsapp = payload.contactValue
  }

  delete payload.contactPlatform
  delete payload.contactValue

  return payload
}

// Submit
async function submitForm() {
  if (!formData.consent) {
    alert(t('form.alert.consent'))
    return
  }

  const allFiles = isCzech.value
    ? [...filesPassport.value, ...filesOP.value]
    : [...filesPassport.value, ...filesResidence.value]

  const payload = buildSubmitPayload()
  isSubmitting.value = true

  try {
    const user = await APIPosts.createPost(payload, "/users")

    for (const file of allFiles) {
      const file_instance = await APIPosts.createFile(file)
      const file_id = file_instance.data.id
      const user_id = user.data.id
      await APIPosts.createPost({ file_id, user_id, description: "Document" }, "/documents")
    }

    router.push(`/success/${route.params.company}`)
  } catch (error) {
    console.error('Failed to submit form', error)
    alert(error?.message || t('form.alert.submit'))
  } finally {
    isSubmitting.value = false
  }
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
        <label>{{ $t("form.fields.city") }}</label>
        <input type="text" v-model="formData.city" />
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
        <label>{{ $t("form.fields.birth_date") }}</label>
        <input type="date" v-model="formData.birth_date" />
      </div>

      <div class="field-group">
        <label>{{ $t("form.fields.address") }}</label>
        <input type="text" v-model="formData.address" />
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

        <p v-if="formData.contactPlatform === 'whatsapp'" class="whatsapp-hint">
          {{ $t("form.whatsapp-hint") }}
        </p>

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

      <div class="field-group">
        <label>{{ $t("form.fields.desired_transport") }}</label>
        <select v-model="formData.desired_transport">
          <option value="" disabled>{{ $t("form.placeholders.transport") }}</option>
          <option value="bike">{{ $t("form.transport-options.bike") }}</option>
          <option value="escooter">{{ $t("form.transport-options.escooter") }}</option>
          <option value="scooter">{{ $t("form.transport-options.scooter") }}</option>
          <option value="car">{{ $t("form.transport-options.car") }}</option>
        </select>
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
        <label>{{ $t("form.fields.citizenship") }}</label>
        <select v-model="formData.citizenship">
          <option value="" disabled>{{ $t("form.placeholders.citizenship") }}</option>
          <option value="cz">Česká republika</option>
          <option value="ua">Ukraine</option>
          <option value="tr">Turkey</option>
          <option value="ind">India</option>
          <option value="sk">Slovakia</option>
          <option value="other">{{ $t("form.citizenship.other") }}</option>
        </select>
      </div>

      <div class="field-group">
        <label>{{ $t("form.fields.how_found_it") }}</label>
        <input type="text" v-model="formData.how_found_it" />
      </div>

      <!-- Section 2: Documents -->
      <div class="section-title">
        <span class="section-number">2.</span>
        <span class="section-text">{{ $t("form.section2.title") }}</span>
      </div>

      <!-- Czech: Občanský průkaz front + back -->
      <template v-if="isCzech">
        <div
          class="drop-zone"
          :class="{ dragging: dragging.passport }"
          @dragover.prevent="dragging.passport = true"
          @dragleave.prevent="dragging.passport = false"
          @drop.prevent="onDrop('passport', $event)"
          @click="triggerInput('passport')"
        >
          <p class="drop-zone-label">{{ $t("form.documents.op_front") }}</p>
          <p class="drop-zone-hint">{{ $t("form.documents.drop_here") }}</p>
          <div v-if="filesPassport.length" class="files-list" @click.stop>
            <div v-for="(file, i) in filesPassport" :key="i" class="file-item">
              <span>{{ file.name }}</span>
              <button type="button" class="remove-file" @click.stop="removeFile('passport', i)">✕</button>
            </div>
          </div>
          <input type="file" ref="inputPassport" multiple class="hidden-file-input" @change="onFileInput('passport', $event)" />
        </div>

        <div
          class="drop-zone"
          :class="{ dragging: dragging.op }"
          @dragover.prevent="dragging.op = true"
          @dragleave.prevent="dragging.op = false"
          @drop.prevent="onDrop('op', $event)"
          @click="triggerInput('op')"
        >
          <p class="drop-zone-label">{{ $t("form.documents.op_back") }}</p>
          <p class="drop-zone-hint">{{ $t("form.documents.drop_here") }}</p>
          <div v-if="filesOP.length" class="files-list" @click.stop>
            <div v-for="(file, i) in filesOP" :key="i" class="file-item">
              <span>{{ file.name }}</span>
              <button type="button" class="remove-file" @click.stop="removeFile('op', i)">✕</button>
            </div>
          </div>
          <input type="file" ref="inputOP" multiple class="hidden-file-input" @change="onFileInput('op', $event)" />
        </div>
      </template>

      <!-- Non-Czech: passport front + visa/residence front -->
      <template v-else>
        <div
          class="drop-zone"
          :class="{ dragging: dragging.passport }"
          @dragover.prevent="dragging.passport = true"
          @dragleave.prevent="dragging.passport = false"
          @drop.prevent="onDrop('passport', $event)"
          @click="triggerInput('passport')"
        >
          <p class="drop-zone-label">{{ $t("form.documents.passport_front") }}</p>
          <p class="drop-zone-hint">{{ $t("form.documents.drop_here") }}</p>
          <div v-if="filesPassport.length" class="files-list" @click.stop>
            <div v-for="(file, i) in filesPassport" :key="i" class="file-item">
              <span>{{ file.name }}</span>
              <button type="button" class="remove-file" @click.stop="removeFile('passport', i)">✕</button>
            </div>
          </div>
          <input type="file" ref="inputPassport" multiple class="hidden-file-input" @change="onFileInput('passport', $event)" />
        </div>

        <div
          class="drop-zone"
          :class="{ dragging: dragging.residence }"
          @dragover.prevent="dragging.residence = true"
          @dragleave.prevent="dragging.residence = false"
          @drop.prevent="onDrop('residence', $event)"
          @click="triggerInput('residence')"
        >
          <p class="drop-zone-label">{{ $t("form.documents.residence_permit_front") }}</p>
          <p class="drop-zone-hint">{{ $t("form.documents.drop_here") }}</p>
          <div v-if="filesResidence.length" class="files-list" @click.stop>
            <div v-for="(file, i) in filesResidence" :key="i" class="file-item">
              <span>{{ file.name }}</span>
              <button type="button" class="remove-file" @click.stop="removeFile('residence', i)">✕</button>
            </div>
          </div>
          <input type="file" ref="inputResidence" multiple class="hidden-file-input" @change="onFileInput('residence', $event)" />
        </div>
      </template>

      <!-- Submit button -->
      <button
        type="submit"
        :disabled="isSubmitting || !hasRequiredFiles"
        :class="(route.params.company === 'bolt' ? 'app-pill-button app-alt-button-text submit-btn bolt' : 'app-pill-button app-alt-button-text submit-btn foodora')"
      >
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
  font-weight: 700;
  font-size: 25px;
  line-height: 100%;
  margin: 0;
  color: var(--color-text);
}

.bolt-logo {
  height: 35px;
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
  font-weight: 500;
  font-size: 15px;
  line-height: 100%;
  color: var(--color-text);
}

.field-group input,
.field-group select {
  font-size: 15px;
  padding: 12px 16px;
  border: 1.5px solid #ccc;
  border-radius: 50px;
  outline: none;
  transition: border-color 0.2s ease;
  width: 100%;
  box-sizing: border-box;
  appearance: none;
  background-color: #fff;
}

.field-group input:focus,
.field-group select:focus {
  border-color: var(--brand-color);
}

.field-group input::placeholder {
  color: #aaa;
}

.field-group select option[value=""] {
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

/* ---- WhatsApp hint ---- */
.whatsapp-hint {
  margin: 0;
  font-size: 13px;
  color: #888;
  line-height: 1.4;
}

/* ---- Drop zones ---- */
.hidden-file-input {
  display: none;
}

.drop-zone {
  border: 1.5px dashed #ccc;
  border-radius: 16px;
  padding: 20px 16px 16px;
  cursor: pointer;
  transition: border-color 0.2s ease, background-color 0.2s ease;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
}

.drop-zone:hover,
.drop-zone.dragging {
  border-color: var(--brand-color);
  background-color: rgba(0, 0, 0, 0.02);
}

.drop-zone-label {
  font-weight: 500;
  font-size: 15px;
  color: var(--color-text);
  margin: 0;
  text-align: center;
}

.drop-zone-hint {
  font-size: 13px;
  color: #aaa;
  margin: 0;
  text-align: center;
}

.files-list {
  display: flex;
  flex-direction: column;
  gap: 4px;
  width: 100%;
  margin-top: 12px;
}

.file-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 14px;
  color: #555;
  padding: 6px 12px;
  background: #f9f9f9;
  border-radius: 6px;
}

.remove-file {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 13px;
  color: #aaa;
  padding: 0 0 0 8px;
  line-height: 1;
  transition: color 0.15s ease;
}

.remove-file:hover {
  color: #e53935;
}

/* ---- Submit button ---- */
.submit-btn {
  font-size: 20px;
  text-align: center;
  color: #fff;
  padding: 18px;
  width: 100%;
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
