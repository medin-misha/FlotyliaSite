<script setup>
import APIGetters from '../../api/getters'
import { usePageStore } from '../../stores/page'
import { useStatesStore } from '../../stores/states'
import APIPosts from '../../api/posts'
import { ref, reactive } from 'vue'
const props = defineProps({
  id: Number,
  adres: String,
  form: Object,
})
const pageStore = usePageStore()
const statesStore = useStatesStore()
const schema = pageStore.pageData.schema
const objectData = reactive((await APIGetters.getDetail(props.adres, props.id)).data)

const deletePost = () => {
  APIPosts.deletePost(props.adres, props.id)
}

// Кастыль!!!!!!

const documents = JSON.parse(JSON.stringify(objectData.documents || []))
const updatePost = () => {
  APIPosts.updatePost(props.adres, props.id, objectData)
  console.log('Оригинал', objectData.documents)
  console.log('Копия', documents)
  if (objectData.documents && objectData.documents.length > 0) {
    for (var i = 0; i < objectData.documents.length; i++) {
      if (objectData.documents[i] !== documents[i]) {
        APIPosts.deletePost('/documents', objectData.documents[i].id)
        APIPosts.createPost('/documents', objectData.documents[i])
      }
    }
  }
}
</script>

<template>
  <section>
    <component
      v-for="field in schema.fields"
      :is="field.component"
      :key="field.key"
      :field="field"
      v-model:value="objectData[field.key]"
      :object="objectData"
    />
    <div class="buttons">
      <button @click="(updatePost(), statesStore.setTableState())">Update</button>
    </div>
  </section>
</template>

<style scoped>
section {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 1rem;
}

.buttons {
  display: flex;
  gap: 3rem;
}
</style>
