<script setup>
import { defineModel } from 'vue'
const props = defineProps({
  field: Object,
})
const value = defineModel('value', { required: true })

const handleFileChange = (event) => {
  value.value = event.target.files[0]
}
</script>

<template>
  <section class="create-field-section">
    <label for="">{{ field.label }}</label>
    <input type="file" @change="handleFileChange" />
  </section>
</template>

<style scoped>
input {
  width: 50%;
}
</style>
