<script setup>
import { computed } from 'vue'

const props = defineProps({
  field: Object,
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
  <div class="details-field">
    <label class="details-input-label"> {{ field.label }}: {{ model }} </label>

    <input type="checkbox" class="details-input" v-if="!field.readonly" v-model="model" />
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
