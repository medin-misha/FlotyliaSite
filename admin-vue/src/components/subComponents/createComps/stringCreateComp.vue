<script setup>
import { defineModel } from 'vue'
const props = defineProps({
  field: Object,
})
const value = defineModel('value', { required: true, type: String })
</script>

<template>
  <section class="create-field-section">
    <label :for="field.key">{{ field.label }}</label>
    <input type="text" v-model="value" :placeholder="field.label" :name="field.key" />
  </section>
</template>

<style scoped>
input {
  width: 50%;
}
</style>
