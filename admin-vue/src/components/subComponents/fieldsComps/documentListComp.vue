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
  <div
    class="col-span-1 md:col-span-2 pt-6 border-t border-outline-variant/20 dark:border-white/10 w-full"
  >
    <div class="flex items-center justify-between mb-4">
      <div class="flex items-center gap-3">
        <span
          class="material-symbols-outlined text-primary"
          style="font-variation-settings: 'FILL' 1"
          >folder_shared</span
        >
        <h4 class="font-headline-sm text-headline-sm font-bold text-on-surface dark:text-white">
          Документы
        </h4>
      </div>
      <button
        @click="addDocument"
        class="flex items-center gap-1.5 px-3 py-1.5 bg-primary/10 hover:bg-primary/20 text-primary dark:text-inverse-primary rounded-xl font-label-md text-label-md transition-all active:scale-[0.98]"
      >
        <span class="material-symbols-outlined text-sm">add</span>
        Добавить
      </button>
    </div>

    <!-- Documents Bento Grid -->
    <div class="grid grid-cols-[repeat(auto-fill,minmax(240px,1fr))] gap-4 w-full">
      <documentComp
        v-for="(document, index) in value"
        :key="index"
        :document="document"
        :field="field"
        @updated="(newDoc) => onDocumentUpdated(index, newDoc)"
        @deleted="onDocumentDeleted(index)"
      />
    </div>
  </div>
</template>

<style scoped></style>
