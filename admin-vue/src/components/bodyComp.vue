<script setup>
import tableComp from './subComponents/tableComp.vue'
import createComp from './subComponents/createComp.vue'
import detailsComp from './subComponents/detailsComp.vue'
import { usePageStore } from '../stores/page'
import { useRequestStates } from '../stores/requestStates'
import { useStatesStore } from '../stores/states'

const statesStore = useStatesStore()
const pageStore = usePageStore()
const requestStatesStore = useRequestStates()
</script>
<template>
  <section>
    <Suspense>
      <template #default>
        <tableComp
          v-if="statesStore.state === statesStore.states.table"
          :adres="pageStore.pageData.adres"
          :page="pageStore.paginationData.page"
          :limit="pageStore.paginationData.limit"
          :search="pageStore.paginationData.search"
          :filter="pageStore.filter"
          :key="`${pageStore.pageData.adres}
        -${pageStore.paginationData.page}
        -${pageStore.paginationData.limit}
        -${pageStore.paginationData.search}
        -${pageStore.filter}`"
        />
        <createComp v-else-if="statesStore.state === statesStore.states.create" />
        <detailsComp
          v-else-if="statesStore.state === statesStore.states.detail"
          :id="statesStore.instance_id"
          :adres="pageStore.pageData.adres"
          :form="pageStore.pageData.schema"
        />
      </template>
      <template #fallback>
        <div>{{ requestStatesStore.state.msg }}</div>
      </template>
    </Suspense>
  </section>
</template>

<style scoped>
div {
  font-weight: bold;
  font-size: 2rem;
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}

section {
  overflow-y: auto;
}
</style>
