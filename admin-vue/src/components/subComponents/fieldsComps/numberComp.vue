<script setup>
import { ref } from 'vue'

const props = defineProps({
  field: Object,
})

const value = defineModel('value', { type: [Number, String] })

// Локальный ref для корректной работы input type=number
const inputValue = ref(value ?? '')

const patch = (data) => {
  console.log('Patch called:', data)
}

const onInput = (e) => {
  // Конвертация в число, если не пусто
  const val = e.target.value === '' ? '' : Number(e.target.value)
  inputValue.value = val
  value.value = val
  patch({ [props.field.key]: val })
}
</script>

<template>
  <div class="details-field">
    <label class="details-input-label">{{ field.label }}: {{ value }}</label>
    <input
      class="details-input"
      type="number"
      :value="inputValue"
      v-if="!field.readonly"
      :placeholder="field.label"
      @input="onInput"
    />
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
.details-input {
  width: 30%;
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
</style>
