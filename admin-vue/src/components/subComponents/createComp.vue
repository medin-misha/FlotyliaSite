<script setup>
import { reactive } from 'vue'
import { usePageStore } from '../../stores/page'
import { useStatesStore } from '../../stores/states'
import APIPosts from '../../api/posts'
const pageStore = usePageStore()
const states = useStatesStore()
const form = pageStore.pageData.createSchema
const modelData = reactive({})

for (const x of form.fields) {
  modelData[x.key] = ''
}

const create = async () => {
  for (const item of form.fields) {
    if (item.type === 'file' && modelData[item.key]) {
      try {
        const response = await APIPosts.createFile(modelData[item.key])
        modelData[item.key] = response.data.id
      } catch (error) {
        console.error('File upload failed:', error)
        return // Stop execution if file upload fails
      }
    }
  }

  await APIPosts.createPost(pageStore.pageData.adres, modelData)
  states.setTableState()
}
</script>

<template>
  <section :key="pageStore.pageData.createSchema">
    <component
      v-for="(item, index) in form.fields"
      :key="index"
      :is="item.component"
      :field="item"
      v-model:value="modelData[item.key]"
    />
    <div>
      <button @click="create">Create</button>
    </div>
  </section>
</template>

<style scoped>
div {
  margin-top: 2rem;
  display: flex;
  flex-direction: row;
  gap: 1rem;
  width: 100%;
  justify-content: center;
}
</style>
