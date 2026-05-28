<script setup>
import { computed } from 'vue'

const props = defineProps({
  field: Object,
  error: String,
  create: {
    type: Boolean,
    default: false,
  },
  value: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits(['update:value'])

const model = computed({
  get: () => props.value,
  set: (val) => emit('update:value', val),
})
</script>

<template>
  <!-- Create mode styling -->
  <div v-if="create" :class="['p-4 rounded-xl border flex items-center justify-between relative group hover:shadow-sm transition-all duration-200 bg-white dark:bg-[#1f2125]', error ? 'border-error ring-1 ring-error/50 bg-error/5 dark:bg-error/10' : 'border-outline-variant/30 dark:border-white/10']">
    <div class="pr-4 select-none flex-1">
      <label :for="field.key" class="font-label-sm text-label-sm font-semibold text-secondary dark:text-secondary-fixed-dim block cursor-pointer">
        {{ field.label }}
        <span v-if="field.required" class="text-primary dark:text-inverse-primary" title="Обязательное поле">*</span>
      </label>
      <p class="text-xs text-secondary/60 dark:text-secondary-fixed-dim/70 mt-1">
        {{ model ? 'Да / Согласен' : 'Нет / Не согласен' }}
      </p>
      
      <!-- Error message text block -->
      <p v-if="error" class="text-xs text-error font-semibold mt-1 flex items-center gap-1">
        <span class="material-symbols-outlined text-[14px]">error</span>
        <span>{{ error }}</span>
      </p>
    </div>

    <!-- Premium Switch Toggle -->
    <label class="relative inline-flex items-center cursor-pointer select-none shrink-0">
      <input 
        type="checkbox" 
        class="sr-only peer" 
        v-model="model" 
        :id="field.key"
      />
      <div class="w-11 h-6 bg-surface-container-highest dark:bg-white/10 rounded-full peer peer-checked:after:translate-x-5 after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary"></div>
    </label>
  </div>

  <!-- Detail/Edit mode styling -->
  <div v-else :class="['p-4 rounded-xl border flex items-center justify-between relative group hover:scale-[1.01] hover:shadow-sm transition-all duration-200 bg-surface-container-low dark:bg-white/5', error ? 'border-error ring-1 ring-error/50 bg-error/5 dark:bg-error/10' : 'border-outline-variant/30']">
    <div class="flex-1 pr-4">
      <label class="font-label-sm text-label-sm text-secondary dark:text-secondary-fixed-dim block">
        {{ field.label }}
      </label>
      <p class="font-body-lg text-body-lg font-semibold text-on-surface dark:text-white mt-0.5">
        {{ model ? 'Да / Согласен' : 'Нет / Не согласен' }}
      </p>
      
      <!-- Error message text block for detail page -->
      <p v-if="error" class="text-xs text-error font-semibold mt-1 flex items-center gap-1">
        <span class="material-symbols-outlined text-[14px]">error</span>
        <span>{{ error }}</span>
      </p>
    </div>

    <!-- Premium Switch Toggle -->
    <label 
      class="relative inline-flex items-center shrink-0" 
      :class="{ 'cursor-pointer': !field.readonly, 'opacity-65 pointer-events-none': field.readonly }"
    >
      <input 
        type="checkbox" 
        class="sr-only peer" 
        :disabled="field.readonly" 
        v-model="model" 
      />
      <div class="w-11 h-6 bg-surface-container-highest dark:bg-white/10 rounded-full peer peer-checked:after:translate-x-5 after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary"></div>
    </label>
  </div>
</template>

<style scoped>
</style>
