<script setup>
import { defineModel } from 'vue'
const props = defineProps({
  field: Object,
})
const value = defineModel('value', { required: true, type: String })
</script>

<template>
  <section class="create-field-section">
    <label for="">{{ field.label }}</label>
    <input type="date" v-model="value" />
  </section>
</template>

<style scoped>
input {
  width: 50%;
}
</style>
