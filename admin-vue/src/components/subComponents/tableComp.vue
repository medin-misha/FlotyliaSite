<script setup>
import { usePageStore } from '../../stores/page'
import { useRequestStates } from '../../stores/requestStates'
import { useStatesStore } from '../../stores/states'
import APIGetters from '../../api/getters'
import { onUnmounted } from 'vue'

const statesStore = useStatesStore()
const props = defineProps({
  adres: String,
  page: Number,
  limit: Number,
  search: String,
  filter: String,
})

const pageStore = usePageStore()
const requestStatesStore = useRequestStates()
let retryTimeout = null

const fetchWithRetry = async () => {
  try {
    requestStatesStore.setState('waiting')
    return await APIGetters.getUniversal(
      props.adres,
      props.page,
      props.limit,
      props.search,
      props.filter,
    )
  } catch (error) {
    requestStatesStore.setState('networkError')
  }
  retryTimeout = setTimeout(fetchWithRetry, 10000)
}
const objectsList = (await fetchWithRetry()).data
console.log(objectsList)
onUnmounted(() => clearTimeout(retryTimeout))
</script>

<template>
  <section>
    <div class="table-wrapper" v-if="Array.isArray(objectsList) && objectsList.length > 0">
      <table>
        <thead>
          <tr>
            <th v-for="obj in Object.keys(objectsList[0])">{{ obj }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="obj in objectsList" @click="statesStore.setDetailState(obj.id)">
            <td v-for="key in Object.keys(obj)">{{ obj[key] }}</td>
          </tr>
        </tbody>
      </table>
    </div>
    <div v-else>
      <h2>{{ requestStatesStore.states.emptyList.msg }}</h2>
    </div>
    <nav>
      <button
        @click="pageStore.prevPage()"
        :disabled="pageStore.paginationData.page - 1 < 1"
        aria-label="previous page"
        class="page-minus"
      >
        {{ pageStore.paginationData.page - 1 }}
      </button>
      {{ pageStore.paginationData.page }}
      <button
        @click="pageStore.nextPage()"
        :disabled="false"
        aria-label="next page"
        class="page-plus"
      >
        {{ pageStore.paginationData.page + 1 }}
      </button>
    </nav>
  </section>
</template>

<style scoped>
section {
  display: flex;
  align-items: center;
  flex-direction: column;
  width: 100%;
  padding: 1rem;
}
.table-wrapper {
  display: block;
  max-width: 80vw;
  overflow-x: auto;
  padding-bottom: 1rem;
}
table {
  min-width: 1000px;
  border-collapse: collapse;
  margin-bottom: 1rem;
}

td,
th {
  min-width: 150px;
}
th {
  font-size: 1.5rem;
  padding: 0.6rem;
}
td {
  font-size: 1rem;
  padding: 0.3rem;
}
nav {
  margin-top: 1rem;
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
}

tbody tr:hover {
  background-color: var(--slidebar-item-hover-bg);
}
button {
  width: 50px;
  height: 30px;
  border-radius: 0.4rem;
  transition: border-radius 0.3s ease;
}
button:hover {
  background-color: var(--button-hover-bg);
}

.page-minus {
  border-radius: 0.4rem 2rem 2rem 0.4rem;
}
.page-plus {
  border-radius: 2rem 0.4rem 0.4rem 2rem;
}
.page-plus:hover {
  border-radius: 0.4rem 2rem 2rem 0.4rem;
}
.page-minus:hover {
  border-radius: 2rem 0.4rem 0.4rem 2rem;
}

.table,
th,
td {
  border: 1px solid var(--slidebar-item-hover-bg);
}
</style>
