<script setup>
import documentComp from './documentComp.vue'
const props = defineProps({
  field: Object,
  object: Object,
})
const value = defineModel('value', { default: [] })
const addDocument = () => {
  value.value.push({ file_id: '', description: '', user_id: props.object.id })
}
const onDocumentUpdated = (index, newDoc) => {
  value.value[index] = newDoc
}
const onDocumentDeleted = (index) => {
  value.value.splice(index, 1)
}
</script>

<template>
  <section>
    <div class="document-list-header">
      <h2>Documents</h2>
    </div>
    <documentComp
      v-for="(document, index) in value"
      :key="index"
      :document="document"
      :field="field"
      @updated="(newDoc) => onDocumentUpdated(index, newDoc)"
      @deleted="onDocumentDeleted(index)"
    />
    <button @click="addDocument">+</button>
  </section>
</template>

<style scoped>
section {
  width: 100%;
}
.document-list-header {
  width: 100%;
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
}
button {
  width: 100%;
  cursor: pointer;
  background-color: var(--slidebar-item-hover-bg);
  margin: 0;
}
button:hover {
  background-color: var(--button-hover-bg);
}
</style>
