<script setup>
import { defineModel } from 'vue'
const props = defineProps({
  field: Object,
})
const value = defineModel('value', { required: true })
</script>

<template>
  <section class="create-field-section">
    <label for="">{{ field.label }}</label>
    <select v-model="value">
      <option disabled value="">{{ field.label }}</option>
      <option v-for="option in field.options" :key="option.value" :value="option.value">
        {{ option.label }}
      </option>
    </select>
  </section>
</template>

<style scoped>
select {
  width: 50%;
}
</style>
