import { reactive } from 'vue'

// ---------------------------------------------------------------------------
// Field length constraints (shared with template via destructuring in caller)
// ---------------------------------------------------------------------------
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

// ---------------------------------------------------------------------------
// Pure helpers (not exported — internal to the composable)
// ---------------------------------------------------------------------------
function hasTextValue(value) {
  return typeof value === 'string' ? value.trim().length > 0 : Boolean(value)
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

// ---------------------------------------------------------------------------
// sanitizeNameValue is exported so formComp.vue can use it in normalizeNameField
// ---------------------------------------------------------------------------
export function sanitizeNameValue(value) {
  if (typeof value !== 'string') return ''
  return value.replace(/\p{Script=Cyrillic}+/gu, '')
}

// ---------------------------------------------------------------------------
// Composable
// ---------------------------------------------------------------------------

/**
 * @param {object} formData - Reactive form data object.
 * @param {{ filesPassport: Ref, filesOP: Ref, filesResidence: Ref, isCzech: ComputedRef }} deps
 */
export function useFormValidation(formData, { filesPassport, filesOP, filesResidence, isCzech }) {
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

  return {
    fieldLengthLimits,
    invalidFields,
    getInvalidVisibleFields,
    applyInvalidFields,
  }
}
