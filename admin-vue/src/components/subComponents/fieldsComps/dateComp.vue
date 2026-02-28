<script setup>
import { computed } from 'vue'

const props = defineProps({
  field: Object,
})

const value = defineModel('value', { type: [String, null], default: '' })

const inputType = computed(() => (props.field?.type === 'datetime' ? 'datetime-local' : 'date'))
</script>

<template>
  <div class="details-field">
    <label class="details-input-label"> {{ field.label }}: {{ value || '' }} </label>

    <input
      class="details-input"
      :type="inputType"
      v-if="!field.readonly"
      :placeholder="field.label"
      v-model="value"
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
