<script setup>
import { reactive, ref, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useI18n } from "vue-i18n"
import APIPosts from '../api/posts'

const route = useRoute()
const router = useRouter()
const { t } = useI18n({ useScope: "global" })
const supportTelegramUrl = 'https://t.me/MFS_support'
const fieldLengthLimits = {
  name: { min: 2, max: 255 },
  city: { min: 2, max: 255 },
  phone: { min: 2, max: 15 },
  email: { max: 255 },
  address: { min: 2, max: 528 },
  desired_transport: { min: 2, max: 255 },
  how_found_it: { min: 2, max: 255 },
  citizenship: { min: 2, max: 100 },
  invoice: { min: 2, max: 255 },
  telegram: { min: 2, max: 255 },
  whatsapp: { min: 2, max: 15 },
}

// Reactive form data
const formData = reactive({
  name: '',
  phone: '+420',
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

// Files per zone
const filesOP = ref([])
const filesPassport = ref([])
const filesResidence = ref([])

// Clear files when citizenship changes
watch(() => formData.citizenship, () => {
  filesOP.value = []
  filesPassport.value = []
  filesResidence.value = []
  syncFieldValidity('passport')
  syncFieldValidity('op')
  syncFieldValidity('residence')
})

// Drag state per zone
const dragging = reactive({ op: false, passport: false, residence: false })

// Hidden input refs
const inputOP = ref(null)
const inputPassport = ref(null)
const inputResidence = ref(null)

const isSubmitting = ref(false)
const submitError = ref(null)

// Platform selection logic
const contactPlaceholder = computed(() => {
  if (formData.contactPlatform === 'telegram') return '@username'
  if (formData.contactPlatform === 'whatsapp') return '+...'
  return ''
})

const isContactDisabled = computed(() => !formData.contactPlatform)
const invalidFields = reactive({
  name: false,
  city: false,
  phone: false,
  email: false,
  birth_date: false,
  address: false,
  contactPlatform: false,
  contactValue: false,
  desired_transport: false,
  how_found_it: false,
  citizenship: false,
  invoice: false,
  passport: false,
  op: false,
  residence: false,
})

function hasTextValue(value) {
  return typeof value === 'string' ? value.trim().length > 0 : Boolean(value)
}

function sanitizeNameValue(value) {
  if (typeof value !== 'string') return ''
  return value.replace(/\p{Script=Cyrillic}+/gu, '')
}

function isTextWithinLimits(value, limits, emptyPrefix = '') {
  const normalizedValue = typeof value === 'string' ? value.trim() : ''

  if (normalizedValue.length === 0 || normalizedValue === emptyPrefix) {
    return false
  }

  if (typeof limits?.min === 'number' && normalizedValue.length < limits.min) {
    return false
  }

  if (typeof limits?.max === 'number' && normalizedValue.length > limits.max) {
    return false
  }

  return true
}

function getInvalidVisibleFields() {
  const hasContactPlatform = hasTextValue(formData.contactPlatform)
  const hasContactValue = formData.contactPlatform === 'whatsapp'
    ? isTextWithinLimits(formData.contactValue, fieldLengthLimits.whatsapp, '+')
    : isTextWithinLimits(formData.contactValue, fieldLengthLimits.telegram)

  return {
    name: !isTextWithinLimits(formData.name, fieldLengthLimits.name),
    city: !isTextWithinLimits(formData.city, fieldLengthLimits.city),
    phone: !isTextWithinLimits(formData.phone, fieldLengthLimits.phone, '+420'),
    email: !isTextWithinLimits(formData.email, fieldLengthLimits.email),
    birth_date: !hasTextValue(formData.birth_date),
    address: !isTextWithinLimits(formData.address, fieldLengthLimits.address),
    contactPlatform: !hasContactPlatform,
    contactValue: hasContactPlatform ? !hasContactValue : false,
    desired_transport: !isTextWithinLimits(formData.desired_transport, fieldLengthLimits.desired_transport),
    how_found_it: !isTextWithinLimits(formData.how_found_it, fieldLengthLimits.how_found_it),
    citizenship: !isTextWithinLimits(formData.citizenship, fieldLengthLimits.citizenship),
    invoice: !isTextWithinLimits(formData.invoice, fieldLengthLimits.invoice),
    passport: filesPassport.value.length === 0,
    op: isCzech.value ? filesOP.value.length === 0 : false,
    residence: isCzech.value ? false : filesResidence.value.length === 0,
  }
}

function applyInvalidFields(nextInvalidFields) {
  Object.keys(invalidFields).forEach((field) => {
    invalidFields[field] = Boolean(nextInvalidFields[field])
  })
}

function syncFieldValidity(field) {
  invalidFields[field] = getInvalidVisibleFields()[field]
}

function normalizeNameField() {
  formData.name = sanitizeNameValue(formData.name)
  syncFieldValidity('name')
}

function selectPlatform(platform) {
  if (formData.contactPlatform === platform) {
    formData.contactPlatform = ''
    formData.contactValue = ''
  } else {
    formData.contactPlatform = platform
    formData.contactValue = platform === 'whatsapp' ? '+' : ''
  }

  syncFieldValidity('contactPlatform')
  syncFieldValidity('contactValue')
}

watch(() => formData.phone, (val) => {
  if (!val.startsWith('+420')) {
    formData.phone = '+420'
  }

  syncFieldValidity('phone')
})

watch(() => formData.contactValue, (val) => {
  if (formData.contactPlatform !== 'whatsapp') return
  if (!val.startsWith('+')) {
    formData.contactValue = '+'
  }

  syncFieldValidity('contactValue')
})

// Drop zone handlers
function addFiles(zone, newFiles) {
  if (zone === 'op') filesOP.value.push(...newFiles)
  else if (zone === 'passport') filesPassport.value.push(...newFiles)
  else if (zone === 'residence') filesResidence.value.push(...newFiles)

  syncFieldValidity(zone)
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

  syncFieldValidity(zone)
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

const submitErrorContent = computed(() => {
  if (!submitError.value) return null

  if (submitError.value.isPartial) {
    return {
      title: t('form.serverError.title'),
      description: t('form.serverError.partial'),
      showSupport: true,
    }
  }

  const errorTypeMap = {
    network: 'network',
    timeout: 'timeout',
    validation: 'validation',
    upload: 'upload',
    service_unavailable: 'serviceUnavailable',
    server: 'server',
    unknown: 'unknown',
  }

  const descriptionKey = errorTypeMap[submitError.value.type] || 'unknown'
  const showSupport = ['service_unavailable', 'server'].includes(submitError.value.type)

  return {
    title: t('form.serverError.title'),
    description: t(`form.serverError.${descriptionKey}`),
    showSupport,
  }
})

// Submit
async function submitForm() {
  const nextInvalidFields = getInvalidVisibleFields()
  applyInvalidFields(nextInvalidFields)

  if (Object.values(nextInvalidFields).some(Boolean)) {
    alert(t('form.alert.required'))
    return
  }

  if (!formData.consent) {
    alert(t('form.alert.consent'))
    return
  }

  const allFiles = isCzech.value
    ? [...filesPassport.value, ...filesOP.value]
    : [...filesPassport.value, ...filesResidence.value]

  const payload = buildSubmitPayload()
  let hasPartialSubmission = false
  submitError.value = null
  isSubmitting.value = true

  try {
    const user = await APIPosts.createPost(payload, "/users")
    hasPartialSubmission = true

    for (const file of allFiles) {
      const file_instance = await APIPosts.createFile(file)
      const file_id = file_instance.data.id
      const user_id = user.data.id
      await APIPosts.createPost({ file_id, user_id, description: "Document" }, "/documents")
    }

    router.push(`/success/${route.params.company}`)
  } catch (error) {
    console.error('Failed to submit form', error)
    submitError.value = {
      type: error?.type || 'unknown',
      isPartial: hasPartialSubmission,
    }
  } finally {
    isSubmitting.value = false
  }
}
</script>

<template>
  <div class="form-page">
    <form class="form-container" novalidate @submit.prevent="submitForm">
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
        <input
          placeholder="Ivan Ivanush"
          type="text"
          v-model="formData.name"
          :minlength="fieldLengthLimits.name.min"
          :maxlength="fieldLengthLimits.name.max"
          :class="{ 'field-invalid': invalidFields.name }"
          @input="normalizeNameField"
        />
      </div>

      <div class="field-group">
        <label>{{ $t("form.fields.city") }}</label>
        <input
          type="text"
          v-model="formData.city"
          :minlength="fieldLengthLimits.city.min"
          :maxlength="fieldLengthLimits.city.max"
          :class="{ 'field-invalid': invalidFields.city }"
          @input="syncFieldValidity('city')"
        />
      </div>

      <div class="field-group">
        <label>{{ $t("form.fields.phone") }}</label>
        <input
          type="tel"
          v-model="formData.phone"
          :minlength="fieldLengthLimits.phone.min"
          :maxlength="fieldLengthLimits.phone.max"
          :class="{ 'field-invalid': invalidFields.phone }"
        />
      </div>

      <div class="field-group">
        <label>{{ $t("form.fields.email") }}</label>
        <input
          type="email"
          v-model="formData.email"
          :maxlength="fieldLengthLimits.email.max"
          :class="{ 'field-invalid': invalidFields.email }"
          @input="syncFieldValidity('email')"
        />
      </div>

      <div class="field-group">
        <label>{{ $t("form.fields.birth_date") }}</label>
        <input
          type="date"
          v-model="formData.birth_date"
          :class="{ 'field-invalid': invalidFields.birth_date }"
          @input="syncFieldValidity('birth_date')"
          @change="syncFieldValidity('birth_date')"
        />
      </div>

      <div class="field-group">
        <label>{{ $t("form.fields.address") }}</label>
        <input
          type="text"
          v-model="formData.address"
          :minlength="fieldLengthLimits.address.min"
          :maxlength="fieldLengthLimits.address.max"
          :class="{ 'field-invalid': invalidFields.address }"
          @input="syncFieldValidity('address')"
        />
      </div>

      <!-- Platform selection -->
      <div class="platform-section" :class="{ 'platform-invalid': invalidFields.contactPlatform }">
        <p class="platform-label">{{ $t("form.platform.label") }}</p>

        <div class="checkbox-group">
          <label class="checkbox-item" @click.prevent="selectPlatform('telegram')">
            <span
              class="custom-checkbox"
              :class="{ checked: formData.contactPlatform === 'telegram', 'field-invalid': invalidFields.contactPlatform }"
            ></span>
            <span>Telegram</span>
          </label>

          <label class="checkbox-item" @click.prevent="selectPlatform('whatsapp')">
            <span
              class="custom-checkbox"
              :class="{ checked: formData.contactPlatform === 'whatsapp', 'field-invalid': invalidFields.contactPlatform }"
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
            :minlength="formData.contactPlatform === 'whatsapp' ? fieldLengthLimits.whatsapp.min : fieldLengthLimits.telegram.min"
            :maxlength="formData.contactPlatform === 'whatsapp' ? fieldLengthLimits.whatsapp.max : fieldLengthLimits.telegram.max"
            :class="{ 'input-disabled': isContactDisabled, 'field-invalid': invalidFields.contactValue }"
            @input="syncFieldValidity('contactValue')"
          />
        </div>
      </div>

      <div class="field-group">
        <label>{{ $t("form.fields.desired_transport") }}</label>
        <select
          v-model="formData.desired_transport"
          :class="{ 'field-invalid': invalidFields.desired_transport }"
          @change="syncFieldValidity('desired_transport')"
        >
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
          :minlength="fieldLengthLimits.invoice.min"
          :maxlength="fieldLengthLimits.invoice.max"
          :class="{ 'field-invalid': invalidFields.invoice }"
          @input="syncFieldValidity('invoice')"
        />
      </div>

      <div class="field-group">
        <label>{{ $t("form.fields.citizenship") }}</label>
        <select
          v-model="formData.citizenship"
          :class="{ 'field-invalid': invalidFields.citizenship }"
          @change="syncFieldValidity('citizenship')"
        >
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
        <input
          type="text"
          v-model="formData.how_found_it"
          :minlength="fieldLengthLimits.how_found_it.min"
          :maxlength="fieldLengthLimits.how_found_it.max"
          :class="{ 'field-invalid': invalidFields.how_found_it }"
          @input="syncFieldValidity('how_found_it')"
        />
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
          :class="{ dragging: dragging.passport, 'drop-zone-invalid': invalidFields.passport }"
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
          :class="{ dragging: dragging.op, 'drop-zone-invalid': invalidFields.op }"
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
          :class="{ dragging: dragging.passport, 'drop-zone-invalid': invalidFields.passport }"
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
          :class="{ dragging: dragging.residence, 'drop-zone-invalid': invalidFields.residence }"
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
        :disabled="isSubmitting || !formData.consent"
        :class="(route.params.company === 'bolt' ? 'app-pill-button app-alt-button-text submit-btn bolt' : 'app-pill-button app-alt-button-text submit-btn foodora')"
        
      >
        {{ $t("form.submit") }}
      </button>

      <div v-if="submitErrorContent" class="form-error-banner" role="alert" aria-live="polite">
        <p class="form-error-title">{{ submitErrorContent.title }}</p>
        <p class="form-error-text">{{ submitErrorContent.description }}</p>
        <a
          v-if="submitErrorContent.showSupport"
          :href="supportTelegramUrl"
          target="_blank"
          rel="noreferrer"
          class="form-error-link"
          :aria-label="$t('why-us.support-link-aria')"
        >
          @MFS_support
        </a>
      </div>

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

.form-error-banner {
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding: 16px 18px;
  border: 1px solid #e53935;
  border-radius: 18px;
  background: rgba(229, 57, 53, 0.08);
}

.form-error-title {
  margin: 0;
  font-weight: 700;
  font-size: 16px;
  color: #8c1d18;
}

.form-error-text {
  margin: 0;
  font-size: 14px;
  line-height: 1.5;
  color: #8c1d18;
}

.form-error-link {
  width: fit-content;
  font-weight: 700;
  font-size: 14px;
  color: #8c1d18;
  text-decoration: underline;
  text-underline-offset: 3px;
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

.field-group input.field-invalid,
.field-group select.field-invalid {
  border-color: #e53935;
  box-shadow: 0 0 0 3px rgba(229, 57, 53, 0.12);
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

.custom-checkbox.field-invalid {
  border-color: #e53935;
  box-shadow: 0 0 0 3px rgba(229, 57, 53, 0.12);
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

.drop-zone.drop-zone-invalid {
  border-color: #e53935;
  background-color: rgba(229, 57, 53, 0.04);
  box-shadow: 0 0 0 3px rgba(229, 57, 53, 0.12);
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
