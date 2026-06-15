<script setup>
import { reactive, ref, computed, watch, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from "vue-i18n"
import APIPosts from '../api/posts'

const router = useRouter()
const { t } = useI18n({ useScope: "global" })

// Cookie Helpers
function setCookie(name, value, maxAgeSeconds) {
  document.cookie = `${name}=${value}; max-age=${maxAgeSeconds}; path=/; SameSite=Lax`
}

function getCookie(name) {
  const matches = document.cookie.match(new RegExp(
    "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
  ))
  return matches ? decodeURIComponent(matches[1]) : undefined
}

function applyPlatform(val) {
  if (val === 'bolt' || val === 'foodora') {
    document.documentElement.setAttribute('data-platform', val)
    try { localStorage.setItem('mfs_platform', val) } catch (_) {}
  } else {
    document.documentElement.removeAttribute('data-platform')
  }
}

onMounted(() => {
  if (getCookie('is_regi') === 'true') {
    const company = localStorage.getItem('mfs_platform') || 'bolt'
    router.replace(`/success/${company}`)
    return
  }
  // Restore previously selected platform
  try {
    const stored = localStorage.getItem('mfs_platform')
    if (stored === 'bolt' || stored === 'foodora') {
      formData.work_in = stored
      applyPlatform(stored)
    }
  } catch (_) {}
})

onUnmounted(() => {
  document.documentElement.removeAttribute('data-platform')
})
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
  work_in: '',
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
  work_in: false,
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
    work_in: !hasTextValue(formData.work_in),
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

function selectWorkPlatform(platform) {
  formData.work_in = platform
  applyPlatform(platform)
  syncFieldValidity('work_in')
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
  if (getCookie('is_send') === 'true') {
    return
  }

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

  const file1 = filesPassport.value[0]
  const file2 = isCzech.value ? filesOP.value[0] : filesResidence.value[0]

  const file1_desc = isCzech.value ? t('form.documents.op_front') : t('form.documents.passport_front')
  const file2_desc = isCzech.value ? t('form.documents.op_back') : t('form.documents.residence_permit_front')

  const payload = buildSubmitPayload()
  
  // Set is_send cookie for 1 minute as we start form sending
  setCookie('is_send', 'true', 60)

  submitError.value = null
  isSubmitting.value = true

  try {
    await APIPosts.registerUser(payload, file1, file2, file1_desc, file2_desc)
    
    // Set is_regi and extend cookies to 1 year on successful 2xx response
    setCookie('is_send', 'true', 31536000)
    setCookie('is_regi', 'true', 31536000)
    
    router.push(`/success/${formData.work_in}`)
  } catch (error) {
    console.error('Failed to submit form', error)
    submitError.value = {
      type: error?.type || 'unknown',
      isPartial: false,
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
        <img
          v-if="formData.work_in"
          :src="formData.work_in === 'bolt' ? '/bolt.png' : '/foodora.png'"
          :alt="$t('form.logo-alt')"
          class="bolt-logo"
        />
      </div>

      <!-- Platform picker -->
      <div class="field-group" :class="{ 'field-group--invalid': invalidFields.work_in }">
        <label>{{ $t("form.work_in.label") }}</label>
        <p class="field-hint">{{ $t("form.work_in.hint") }}</p>
        <div class="platform-picker">
          <div
            class="platform-card bolt"
            :class="{ selected: formData.work_in === 'bolt' }"
            @click="selectWorkPlatform('bolt')"
          >
            <span class="platform-swatch bolt-swatch">B</span>
            <span class="platform-info">
              <span class="platform-name">Bolt Food</span>
              <span class="platform-tag">{{ $t("form.work_in.bolt_tag") }}</span>
            </span>
            <span class="platform-check">
              <svg v-if="formData.work_in === 'bolt'" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5"/></svg>
            </span>
          </div>
          <!-- <div
            class="platform-card foodora"
            :class="{ selected: formData.work_in === 'foodora' }"
            @click="selectWorkPlatform('foodora')"
          >
            <span class="platform-swatch foodora-swatch">F</span>
            <span class="platform-info">
              <span class="platform-name">Foodora</span>
              <span class="platform-tag">foodora_tag</span>
            </span>
            <span class="platform-check"></span>
          </div> -->
        </div>
        <span v-if="invalidFields.work_in" class="field-error-msg">{{ $t("form.work_in.error") }}</span>
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
        :class="[
          'submit-btn',
          formData.work_in === 'bolt' ? 'bolt' : formData.work_in === 'foodora' ? 'foodora' : 'default',
          { 'submitting': isSubmitting }
        ]"
      >
        <span v-if="!isSubmitting">{{ $t("form.submit") }}</span>
        <span v-else class="loader-container">
          <span class="spinner-icon"></span>
          <span>{{ $t("form.submit") }}...</span>
        </span>
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
  padding: clamp(24px, 4vw, 48px) var(--gutter) clamp(48px, 7vw, 80px);
}

.form-container {
  width: 100%;
  max-width: 680px;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--r-lg);
  padding: clamp(24px, 4vw, 40px);
  display: flex;
  flex-direction: column;
  gap: 20px;
  box-shadow: var(--ring);
}

/* ---- Header ---- */
.form-header {
  display: flex;
  align-items: center;
  gap: 16px;
  padding-bottom: 20px;
  border-bottom: 1px solid var(--border);
}

.form-header h2 {
  font-family: var(--font-alt);
  font-weight: 800;
  font-size: clamp(22px, 2.6vw, 28px);
  line-height: 1.1;
  margin: 0;
  color: var(--text);
  letter-spacing: -.01em;
}

.bolt-logo {
  height: 32px;
  width: auto;
  object-fit: contain;
}

/* ---- Error banner ---- */
.form-error-banner {
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding: 16px 18px;
  border: 1px solid var(--accent);
  border-radius: var(--r-md);
  background: var(--accent-soft);
}
.form-error-title {
  margin: 0; font-weight: 700; font-size: 15px; color: var(--accent-light);
}
.form-error-text {
  margin: 0; font-size: 13.5px; line-height: 1.5; color: var(--text-2);
}
.form-error-link {
  width: fit-content; font-weight: 700; font-size: 13.5px;
  color: var(--accent-light); text-decoration: underline; text-underline-offset: 3px;
}

/* ---- Section titles ---- */
.section-title {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-top: 8px;
  padding-top: 20px;
  border-top: 1px solid var(--border);
}

.section-number {
  width: 28px; height: 28px;
  border-radius: 50%;
  background: var(--accent-soft);
  color: var(--accent);
  display: grid; place-items: center;
  font-family: var(--font-alt); font-weight: 700; font-size: 13px;
  flex: 0 0 auto;
}

.section-text {
  font-family: var(--font-alt);
  font-weight: 700;
  font-size: clamp(17px, 1.8vw, 20px);
  line-height: 1.2;
  color: var(--text);
  letter-spacing: -.01em;
}

/* ---- Fields ---- */
.field-group {
  display: flex;
  flex-direction: column;
  gap: 7px;
}

.field-group label {
  font-size: 13px;
  font-weight: 600;
  color: var(--text);
  letter-spacing: 0;
}

.field-group input,
.field-group select {
  width: 100%;
  padding: 14px 18px;
  border-radius: var(--r-pill);
  background: var(--field-bg);
  border: 1px solid var(--border-2);
  color: var(--text);
  font-size: 15px;
  font-family: var(--font-sans);
  transition: border-color var(--t-fast), box-shadow var(--t-fast), background-color var(--t-fast);
  outline: none;
  -webkit-appearance: none;
  appearance: none;
  box-sizing: border-box;
}
.field-group input::placeholder { color: var(--text-3); }
.field-group input:focus,
.field-group select:focus {
  border-color: var(--accent);
  box-shadow: 0 0 0 4px var(--accent-ring);
}
.field-group input.field-invalid,
.field-group select.field-invalid {
  border-color: #c8423a;
  box-shadow: 0 0 0 3px rgba(200,66,58,.18);
}
.field-group select {
  background-image:
    linear-gradient(45deg, transparent 50%, var(--text-2) 50%),
    linear-gradient(135deg, var(--text-2) 50%, transparent 50%);
  background-position: calc(100% - 22px) center, calc(100% - 16px) center;
  background-size: 6px 6px;
  background-repeat: no-repeat;
  padding-right: 44px;
}
.field-group select option[value=""] { color: var(--text-3); }

.input-disabled {
  opacity: 0.45;
  cursor: not-allowed;
}

/* ---- Platform section ---- */
.platform-section {
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.platform-invalid .custom-checkbox { border-color: #c8423a; }

.platform-label {
  font-size: 13px; font-weight: 600; margin: 0; color: var(--text);
}

.checkbox-group { display: flex; gap: 12px; flex-wrap: wrap; }

.checkbox-item {
  display: flex; align-items: center; gap: 10px;
  padding: 10px 14px;
  border-radius: var(--r-pill);
  background: var(--field-bg);
  border: 1px solid var(--border-2);
  cursor: pointer; font-size: 14px; font-weight: 600;
  color: var(--text-2); user-select: none;
  transition: border-color var(--t-fast), background-color var(--t-fast);
}
.checkbox-item:hover { border-color: var(--text-3); }

.custom-checkbox {
  width: 18px; height: 18px;
  border: 1.5px solid var(--border-2);
  border-radius: 5px;
  display: grid; place-items: center;
  transition: all var(--t-fast); flex-shrink: 0;
}
.custom-checkbox.field-invalid {
  border-color: #c8423a;
  box-shadow: 0 0 0 3px rgba(200,66,58,.18);
}
.custom-checkbox.checked {
  background: var(--accent); border-color: var(--accent);
}
.custom-checkbox.checked::after {
  content: '';
  display: block;
  width: 10px; height: 10px;
  background: url("data:image/svg+xml,%3csvg viewBox='0 0 24 24' fill='none' stroke='%23fff' stroke-width='3.2' stroke-linecap='round' stroke-linejoin='round' xmlns='http://www.w3.org/2000/svg'%3e%3cpath d='M20 6 9 17l-5-5'/%3e%3c/svg%3e") center/contain no-repeat;
}

/* ---- WhatsApp hint ---- */
.whatsapp-hint {
  margin: 0; font-size: 12.5px; color: var(--text-3); line-height: 1.4;
}

/* ---- Drop zones ---- */
.hidden-file-input { display: none; }

.drop-zone {
  border: 1.5px dashed var(--border-2);
  border-radius: var(--r-md);
  padding: 24px 16px 20px;
  cursor: pointer;
  transition: border-color var(--t-fast), background-color var(--t-fast);
  display: flex; flex-direction: column; align-items: center; gap: 6px;
  background: var(--field-bg);
}
.drop-zone:hover,
.drop-zone.dragging {
  border-color: var(--accent);
  background: var(--accent-soft);
}
.drop-zone.drop-zone-invalid {
  border-color: #c8423a;
  background: rgba(200,66,58,.06);
  box-shadow: 0 0 0 3px rgba(200,66,58,.18);
}
.drop-zone-label {
  font-weight: 600; font-size: 14.5px; color: var(--text); margin: 0; text-align: center;
}
.drop-zone-hint {
  font-size: 12.5px; color: var(--text-3); margin: 0; text-align: center;
}
.files-list {
  display: flex; flex-direction: column; gap: 4px; width: 100%; margin-top: 12px;
}
.file-item {
  display: flex; align-items: center; justify-content: space-between;
  font-size: 13.5px; color: var(--text-2);
  padding: 7px 12px;
  background: var(--surface-2);
  border: 1px solid var(--border);
  border-radius: var(--r-sm);
}
.remove-file {
  background: none; border: none; cursor: pointer;
  font-size: 13px; color: var(--text-3); padding: 0 0 0 8px; line-height: 1;
  transition: color var(--t-fast);
}
.remove-file:hover { color: var(--accent); }

/* ---- Platform picker ---- */
.field-hint {
  font-size: 12.5px;
  color: var(--text-3);
  margin: -2px 0 0;
  line-height: 1.4;
}

.field-group--invalid > label {
  color: #c8423a;
}

.field-error-msg {
  font-size: 12.5px;
  color: #ff7a6f;
  margin-top: 2px;
}

.platform-picker {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}
@media (max-width: 460px) { .platform-picker { grid-template-columns: 1fr; } }

.platform-card {
  position: relative;
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 18px;
  border-radius: var(--r-md);
  background: var(--field-bg);
  border: 1.5px solid var(--border-2);
  cursor: pointer;
  transition: border-color var(--t-fast), background-color var(--t-fast), transform 100ms ease;
  user-select: none;
  overflow: hidden;
}
.platform-card:hover { border-color: var(--text-3); }
.platform-card:active { transform: scale(.99); }
.platform-card.selected {
  border-color: var(--accent);
  background: var(--accent-soft);
}

.platform-swatch {
  width: 44px; height: 44px;
  border-radius: 12px;
  display: grid; place-items: center;
  font-family: var(--font-alt);
  font-weight: 800;
  font-size: 18px;
  letter-spacing: -.04em;
  flex: 0 0 auto;
}
.bolt-swatch    { background: #34D086; color: #07150E; }
.foodora-swatch { background: #DF1068; color: #fff; }

.platform-info {
  display: flex;
  flex-direction: column;
  gap: 3px;
  flex: 1;
  min-width: 0;
}
.platform-name {
  font-family: var(--font-alt);
  font-weight: 700;
  font-size: 16px;
  color: var(--text);
  letter-spacing: -.01em;
  line-height: 1.1;
}
.platform-tag {
  font-size: 12px;
  color: var(--text-3);
}

.platform-check {
  position: absolute;
  top: 10px; right: 10px;
  width: 22px; height: 22px;
  border-radius: 50%;
  background: var(--surface-2);
  border: 1.5px solid var(--border-2);
  display: grid; place-items: center;
  flex: 0 0 auto;
  transition: background-color var(--t-fast), border-color var(--t-fast);
  color: var(--on-accent);
}
.platform-card.selected .platform-check {
  background: var(--accent);
  border-color: var(--accent);
}

/* ---- Submit button ---- */
.submit-btn {
  font-family: var(--font-alt);
  font-weight: 700; font-size: 17px; line-height: 1;
  text-align: center;
  padding: 18px; width: 100%;
  border-radius: var(--r-pill);
  border: none; cursor: pointer;
  transition: filter var(--t-fast), transform 100ms ease, box-shadow var(--t-fast);
  margin-top: 8px;
  display: inline-flex; align-items: center; justify-content: center; gap: 10px;
}
.submit-btn.default {
  background: var(--accent); color: var(--on-accent);
  box-shadow: 0 8px 24px -8px var(--accent-ring), inset 0 1px 0 rgba(255,255,255,.18);
}
.submit-btn.bolt {
  background: #34D086; color: #07150E;
  box-shadow: 0 8px 24px -8px rgba(52,208,134,.4), inset 0 1px 0 rgba(255,255,255,.3);
}
.submit-btn.foodora {
  background: #DF1068; color: #fff;
  box-shadow: 0 8px 24px -8px rgba(223,16,104,.4), inset 0 1px 0 rgba(255,255,255,.2);
}
.submit-btn:hover  { filter: brightness(1.08); }
.submit-btn:active { transform: scale(.97); }
.submit-btn:disabled {
  opacity: .45; cursor: not-allowed;
  transform: none !important; filter: none !important; box-shadow: none !important;
}

.loader-container {
  display: flex; align-items: center; justify-content: center; gap: 10px;
}
.spinner-icon {
  width: 20px; height: 20px;
  border: 3px solid rgba(255,255,255,.3);
  border-radius: 50%; border-top-color: #fff;
  animation: spin 1s ease-in-out infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }

/* ---- Consent ---- */
.consent-row {
  display: flex; align-items: flex-start; gap: 10px; margin-top: 4px;
}
.consent-checkbox {
  width: 20px; height: 20px;
  accent-color: var(--accent); cursor: pointer; flex-shrink: 0; margin-top: 2px;
}
.consent-label {
  font-size: 13px; font-weight: 500; line-height: 1.45; color: var(--text-2); cursor: pointer;
}
</style>
