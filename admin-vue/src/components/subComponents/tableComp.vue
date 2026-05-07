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
  form: Object,
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

const statusClass = (obj) => {
  const status = obj.status
  if (status === 'pending') return 'row-pending'
  if (status === 'active') return 'row-active'
  if (status === 'inoperative') return 'row-inoperative'
  if (status === 'processing') return 'row-processing'
  if (status === 'in activation') return 'row-in-activation'
  return ''
}

const getOptionLabel = (field, value) => {
  if (!field?.options) {
    return value
  }

  const selectedOption = field.options.find((option) => option.value === value)
  return selectedOption?.label ?? value
}
</script>

<template>
  <section>
    <div class="table-wrapper" v-if="Array.isArray(objectsList) && objectsList.length > 0">
      <table>
        <thead>
          <tr>
            <template v-if="form?.fields">
              <th v-for="field in form.fields" :key="field.key">{{ field.label }}</th>
            </template>
            <template v-else>
              <th v-for="key in Object.keys(objectsList[0])" :key="key">{{ key }}</th>
            </template>
          </tr>
        </thead>
        <tbody>
          <tr v-for="obj in objectsList" :key="obj.id" :class="statusClass(obj)" @click="statesStore.setDetailState(obj.id)">
            <template v-if="form?.fields">
              <td v-for="field in form.fields" :key="field.key">
                <template v-if="typeof obj[field.key] === 'object'">
                  {{ obj[field.key] !== null && (Array.isArray(obj[field.key]) ? obj[field.key].length > 0 : Object.keys(obj[field.key]).length > 0) ? 'True' : 'False' }}
                </template>
                <template v-else-if="typeof obj[field.key] === 'boolean'">
                  {{ obj[field.key] ? 'True' : 'False' }}
                </template>
                <template v-else>{{ getOptionLabel(field, obj[field.key]) }}</template>
              </td>
            </template>
            <template v-else>
              <td v-for="key in Object.keys(obj)" :key="key">
                <template v-if="typeof obj[key] === 'object'">
                  {{ obj[key] !== null && (Array.isArray(obj[key]) ? obj[key].length > 0 : Object.keys(obj[key]).length > 0) ? 'True' : 'False' }}
                </template>
                <template v-else-if="typeof obj[key] === 'boolean'">
                  {{ obj[key] ? 'True' : 'False' }}
                </template>
                <template v-else>{{ obj[key] }}</template>
              </td>
            </template>
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
}
.table-wrapper {
  display: block;
  max-width: 91vw;
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
.row-pending {
  background-color: #fffbeb;
}
.row-active {
  background-color: #f0fdf4;
}
.row-inoperative {
  background-color: #fff1f2;
}
.row-processing {
  background-color: #eff6ff;
}
.row-in-activation {
  background-color: #f5f3ff;
}
.row-pending:hover {
  background-color: #fef3c7;
}
.row-active:hover {
  background-color: #dcfce7;
}
.row-inoperative:hover {
  background-color: #ffe4e6;
}
.row-processing:hover {
  background-color: #dbeafe;
}
.row-in-activation:hover {
  background-color: #ede9fe;
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
