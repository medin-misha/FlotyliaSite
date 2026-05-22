<script setup>
import { ref } from 'vue'

const props = defineProps({
  field: Object,
  value: String, // это значение от v-model
})

const emit = defineEmits(['update:value'])
const copied = ref(false)

const onInput = (e) => {
  emit('update:value', e.target.value)
}

const copyValue = async () => {
  if (!props.value) return

  try {
    await navigator.clipboard.writeText(props.value)
    copied.value = true
    setTimeout(() => {
      copied.value = false
    }, 1200)
  } catch (error) {
    console.error('Не удалось скопировать значение', error)
  }
}
</script>

<template>
  <div class="details-field">
    <label class="details-input-label"> {{ field.label }}: {{ value }} </label>

    <div class="details-actions">
      <button
        v-if="field.copyable"
        class="copy-button"
        type="button"
        :disabled="!value"
        @click="copyValue"
      >
        {{ copied ? 'Скопировано' : 'Копировать' }}
      </button>

      <textarea
        class="details-input"
        :value="value"
        v-if="!field.readonly"
        :placeholder="field.label"
        @input="onInput"
      />
    </div>
  </div>
</template>

<style scoped>
.details-field {
  width: 100%;
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  border-bottom: 1px solid var(--slidebar-item-hover-bg);
  margin-bottom: 1rem;
}
.details-input-label {
  font-weight: bold;
}
.details-actions {
  width: 45%;
  display: flex;
  justify-content: flex-end;
  align-items: center;
  gap: 0.75rem;
}
.details-input {
  width: 67%;
  background-color: transparent;
  color: var(--slidebar-item-text-color);
  font-weight: bold;
  border: none;
  padding: 0.5rem;
}
.details-input:focus {
  outline: none;
  color: var(--button-bg);
}
.copy-button {
  width: auto;
  min-width: 110px;
  height: 32px;
  padding: 0.35rem 0.75rem;
  font-size: 0.85rem;
}
.copy-button:disabled {
  cursor: not-allowed;
  opacity: 0.5;
}
</style>
