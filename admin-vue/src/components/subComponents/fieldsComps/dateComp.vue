<script setup>
import { computed, ref, defineModel, nextTick } from 'vue'

const props = defineProps({
  field: Object,
  error: String,
  create: {
    type: Boolean,
    default: false,
  },
})

const value = defineModel('value', { type: [String, null], default: '' })
const copied = ref(false)
const editing = ref(false)
const inputRef = ref(null)
let clickTimer = null
let justStoppedEditing = false

const inputType = computed(() => (props.field?.type === 'datetime' ? 'datetime-local' : 'date'))

const formatDate = (val) => {
  if (!val) return '—'
  if (typeof val === 'string') {
    const tIndex = val.indexOf('T')
    if (tIndex !== -1) {
      return val.substring(0, tIndex)
    }
    const spaceIndex = val.indexOf(' ')
    if (spaceIndex !== -1 && val.includes('-')) {
      return val.substring(0, spaceIndex)
    }
  }
  return val
}

const displayValue = computed({
  get() {
    if (!value.value) return ''
    if (typeof value.value === 'string') {
      const tIndex = value.value.indexOf('T')
      if (tIndex !== -1) {
        return value.value.substring(0, tIndex)
      }
      const spaceIndex = value.value.indexOf(' ')
      if (spaceIndex !== -1 && value.value.includes('-')) {
        return value.value.substring(0, spaceIndex)
      }
    }
    return value.value
  },
  set(val) {
    value.value = val
  },
})

const age = computed(() => {
  if (props.field?.key !== 'birth_date' || !value.value) return null
  const birth = new Date(displayValue.value || value.value)
  if (isNaN(birth)) return null
  const today = new Date()
  let years = today.getFullYear() - birth.getFullYear()
  const m = today.getMonth() - birth.getMonth()
  if (m < 0 || (m === 0 && today.getDate() < birth.getDate())) years--
  return years >= 0 ? years : null
})

const ageLabel = (n) => {
  if (n % 100 >= 11 && n % 100 <= 19) return 'лет'
  const r = n % 10
  if (r === 1) return 'год'
  if (r >= 2 && r <= 4) return 'года'
  return 'лет'
}

const copyValue = async () => {
  const toCopy = displayValue.value || formatDate(value.value)
  if (!toCopy || toCopy === '—') return
  try {
    await navigator.clipboard.writeText(toCopy)
    copied.value = true
    setTimeout(() => {
      copied.value = false
    }, 1200)
  } catch (error) {
    console.error('Не удалось скопировать значение', error)
  }
}

const handleClick = () => {
  if (editing.value || justStoppedEditing || !props.field?.copyable) return
  clearTimeout(clickTimer)
  clickTimer = setTimeout(copyValue, 220)
}

const handleDblClick = () => {
  if (props.field?.readonly) return
  clearTimeout(clickTimer)
  editing.value = true
  nextTick(() => inputRef.value?.focus())
}

const stopEditing = () => {
  editing.value = false
  justStoppedEditing = true
  setTimeout(() => {
    justStoppedEditing = false
  }, 300)
}
</script>

<template>
  <!-- Create mode styling -->
  <div v-if="create" class="flex flex-col w-full gap-1.5 group">
    <label
      :for="field.key"
      class="font-label-sm text-label-sm font-semibold text-secondary dark:text-secondary-fixed-dim ml-1 flex items-center gap-1 select-none"
    >
      <span>{{ field.label }}</span>
      <span
        v-if="field.required"
        class="text-primary dark:text-inverse-primary"
        title="Обязательное поле"
        >*</span
      >
    </label>

    <div class="relative flex items-center">
      <!-- Icon prefix -->
      <span
        class="material-symbols-outlined absolute left-3.5 text-[20px] transition-colors duration-200"
        :class="[
          error
            ? 'text-error'
            : 'text-secondary/50 group-focus-within:text-primary dark:group-focus-within:text-inverse-primary',
        ]"
      >
        calendar_month
      </span>

      <input
        :type="inputType"
        v-model="displayValue"
        :id="field.key"
        class="w-full h-12 pl-11 pr-4 rounded-xl border bg-white dark:bg-[#1f2125] text-on-surface dark:text-white font-body-md text-body-md focus:outline-none transition-all duration-200"
        :class="[
          error
            ? 'border-error ring-1 ring-error/50 bg-error/5 dark:bg-error/10'
            : 'border-outline-variant/30 dark:border-white/10 focus:border-primary focus:ring-1 focus:ring-primary dark:focus:border-inverse-primary dark:focus:ring-inverse-primary hover:border-outline-variant/60 dark:hover:border-white/20',
        ]"
      />
    </div>

    <!-- Error message text block -->
    <transition
      enter-active-class="transition duration-150 ease-out"
      enter-from-class="transform -translate-y-1 opacity-0"
      enter-to-class="transform translate-y-0 opacity-100"
      leave-active-class="transition duration-100 ease-in"
      leave-from-class="transform translate-y-0 opacity-100"
      leave-to-class="transform -translate-y-1 opacity-0"
    >
      <p v-if="error" class="text-xs text-error font-semibold ml-1.5 flex items-center gap-1">
        <span class="material-symbols-outlined text-[14px]">error</span>
        <span>{{ error }}</span>
      </p>
    </transition>
  </div>

  <!-- Detail/Edit mode styling -->
  <div
    v-else
    @click="handleClick"
    @dblclick="handleDblClick"
    :class="[
      'p-3 rounded-xl border bg-surface-container-low dark:bg-white/5 flex flex-col gap-1 relative group transition-all duration-200',
      copied
        ? 'border-primary dark:border-inverse-primary ring-1 ring-primary/30'
        : error
          ? 'border-error ring-1 ring-error/50 bg-error/5 dark:bg-error/10'
          : 'border-outline-variant/30',
      editing ? 'cursor-text' : field.copyable && value ? 'cursor-pointer' : '',
    ]"
  >
    <!-- Label -->
    <div class="flex items-center gap-1.5">
      <label class="font-label-sm text-label-sm text-secondary dark:text-secondary-fixed-dim block select-none">
        {{ field.label }}
      </label>
      <span
        v-if="copied"
        class="material-symbols-outlined text-[14px] text-primary dark:text-inverse-primary"
      >
        check
      </span>
    </div>

    <div class="flex items-center gap-2 mt-0.5">
      <!-- Edit Mode / Input -->
      <input
        v-if="!field.readonly && editing"
        ref="inputRef"
        :type="inputType"
        v-model="displayValue"
        @blur="stopEditing"
        @click.stop
        @dblclick.stop
        class="w-full bg-transparent border-none p-0 focus:ring-0 font-body-lg text-body-lg font-semibold text-on-surface dark:text-white"
        :placeholder="field.label"
      />

      <!-- View Mode (readonly or not editing) -->
      <p
        v-else
        class="font-body-lg text-body-lg font-semibold text-on-surface dark:text-white select-none flex items-baseline gap-2"
      >
        {{ formatDate(value) }}
        <span
          v-if="age !== null"
          class="font-label-sm text-label-sm text-secondary dark:text-secondary-fixed-dim font-normal"
        >{{ age }} {{ ageLabel(age) }}</span>
      </p>
    </div>

    <!-- Error message text block for detail page -->
    <p v-if="error" class="text-xs text-error font-semibold mt-1 flex items-center gap-1">
      <span class="material-symbols-outlined text-[14px]">error</span>
      <span>{{ error }}</span>
    </p>
  </div>
</template>

<style scoped></style>
