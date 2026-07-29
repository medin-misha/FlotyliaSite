<script setup>
import tableComp from './subComponents/tableComp.vue'
import createComp from './subComponents/createComp.vue'
import detailsComp from './subComponents/detailsComp.vue'
import receiptStatsComp from './subComponents/receiptStatsComp.vue'
import { usePageStore } from '../stores/page'
import { useStatesStore } from '../stores/states'
import { computed } from 'vue'

const statesStore = useStatesStore()
const pageStore = usePageStore()

const detailId = computed(() => {
  const id = Number(statesStore.instance_id)
  return Number.isFinite(id) ? id : null
})
const isDetailState = computed(
  () => statesStore.state === statesStore.states.detail && detailId.value !== null,
)
const isStatsView = computed(() => pageStore.pageData.view === 'stats')
</script>

<template>
  <section class="h-screen relative flex flex-col lg:flex-row overflow-y-auto custom-scrollbar">
    <receiptStatsComp v-if="isStatsView" />
    <div
      v-else
      class="flex-grow min-w-0 transition-all duration-300 ease-in-out"
      :class="isDetailState ? 'lg:mr-[50vw]' : ''"
    >
      <tableComp
        v-if="statesStore.state === statesStore.states.table || isDetailState"
        :adres="pageStore.pageData.adres"
        :page="pageStore.paginationData.page"
        :limit="pageStore.paginationData.limit"
        :search="pageStore.paginationData.search"
        :filter="pageStore.filter"
        :form="pageStore.pageData.schema"
        :key="pageStore.pageData.adres"
      />
      <createComp v-else-if="statesStore.state === statesStore.states.create" />
    </div>

    <detailsComp
      v-if="isDetailState && !isStatsView"
      :key="pageStore.pageData.adres + '-' + detailId"
      :id="detailId"
      :adres="pageStore.pageData.adres"
      :form="pageStore.pageData.schema"
    />
  </section>
</template>

<style scoped></style>
