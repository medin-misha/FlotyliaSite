<script setup>
import { defineProps, defineModel } from 'vue'

const props = defineProps({
  field: Object,
  error: String,
  create: {
    type: Boolean,
    default: false,
  },
})

const value = defineModel('value')

const selectedOptionLabel = () => {
  const selectedOption = props.field?.options?.find((option) => option.value === value.value)
  return selectedOption?.label ?? value.value
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
        rule
      </span>

      <select
        v-model="value"
        :id="field.key"
        class="w-full h-12 pl-11 pr-10 rounded-xl border bg-white dark:bg-[#1f2125] text-on-surface dark:text-white font-body-md text-body-md focus:outline-none transition-all duration-200 appearance-none cursor-pointer"
        :class="[
          error
            ? 'border-error ring-1 ring-error/50 bg-error/5 dark:bg-error/10'
            : 'border-outline-variant/30 dark:border-white/10 focus:border-primary focus:ring-1 focus:ring-primary dark:focus:border-inverse-primary dark:focus:ring-inverse-primary hover:border-outline-variant/60 dark:hover:border-white/20',
        ]"
      >
        <option
          disabled
          value=""
          class="bg-white dark:bg-[#1f2125] text-on-surface dark:text-white"
        >
          Выбрать {{ field.label.toLowerCase() }}...
        </option>
        <option
          v-for="option in field.options"
          :key="option.value"
          :value="option.value"
          class="bg-white dark:bg-[#1f2125] text-on-surface dark:text-white"
        >
          {{ option.label }}
        </option>
      </select>

      <!-- Custom dropdown arrow -->
      <span
        class="material-symbols-outlined absolute right-3 text-secondary/50 pointer-events-none"
      >
        keyboard_arrow_down
      </span>
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
    :class="[
      'p-4 rounded-xl border bg-surface-container-low dark:bg-white/5 flex flex-col gap-1 relative group hover:scale-[1.01] hover:shadow-sm transition-all duration-200',
      error
        ? 'border-error ring-1 ring-error/50 bg-error/5 dark:bg-error/10'
        : 'border-outline-variant/30',
    ]"
  >
    <!-- Label -->
    <label class="font-label-sm text-label-sm text-secondary dark:text-secondary-fixed-dim block">
      {{ field.label }}
    </label>

    <div class="flex items-center justify-between gap-2 mt-0.5">
      <!-- Edit Mode / Dropdown -->
      <select
        v-if="!field.readonly"
        v-model="value"
        class="w-full bg-transparent border-none p-0 focus:ring-0 font-body-lg text-body-lg font-semibold text-on-surface dark:text-white appearance-none cursor-pointer"
      >
        <option
          v-for="option in field.options"
          :key="option.value"
          :value="option.value"
          class="bg-surface-container-lowest dark:bg-inverse-surface text-on-surface dark:text-white"
        >
          {{ option.label }}
        </option>
      </select>

      <!-- Readonly View -->
      <p v-else class="font-body-lg text-body-lg font-semibold text-on-surface dark:text-white">
        {{ selectedOptionLabel() || '—' }}
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
