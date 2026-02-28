<script setup>
import { usePageStore } from '../stores/page.js'
import { useStatesStore } from '../stores/states'
import APIGetters from '../api/getters.js'
const statesStore = useStatesStore()
const pageStore = usePageStore()

const handleExport = async () => {
  try {
    const response = await APIGetters.getExport()
    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', 'database_export.xlsx')
    document.body.appendChild(link)
    link.click()
    link.remove()
    window.URL.revokeObjectURL(url)
  } catch (error) {
    console.error('Export failed:', error)
  }
}
</script>

<template>
  <header>
    <aside>
      <h2>{{ pageStore.pageData.name }} {{ statesStore.state }}</h2>
      <div>
        <button @click="handleExport" class="export-button">Export</button>
        <button
          @click="statesStore.setCreateState"
          v-if="statesStore.state === statesStore.states.table"
        >
          Create New
        </button>
        <button @click="statesStore.setTableState" v-else>Back to table</button>
      </div>
    </aside>
    <div class="filters">
      {{ (pageStore.filter, pageStore.search) }}
      <input
        @input="pageStore.setSearchParams($event.target.value)"
        type="text"
        placeholder="Search"
      />
      <select name="filter" v-model="pageStore.filter">
        <option disabled value="">filter</option>
        <option value="">string params</option>
        <option :value="field.key" v-for="field in pageStore.pageData.schema.fields">
          {{ field.label }}
        </option>
      </select>
    </div>
  </header>
</template>

<style scoped>
header {
  width: 100%;
  height: clamp(150px, 15%, 200px);
  background-color: var(--slidebar-bg);
  display: flex;
  flex-direction: column;
  gap: 2rem;
  padding: 1rem;
}
aside {
  display: flex;
  justify-content: space-between;
}

input {
  background-color: var(--slidebar-item-hover-bg);
  height: 3rem;
  border-radius: 1rem;
}
.filters {
  display: flex;
  gap: 1rem;
  flex-direction: row;
}
select {
  background-color: var(--slidebar-item-hover-bg);
  height: 3rem;
  width: 20%;
  border-radius: 1rem;
  color: var(--slidebar-item-hover-text-color);
}

button {
  margin-left: 1rem;
}

.export-button {
  background-color: var(--slidebar-itemr-bg);
  color: var(--slidebar-item-hover-text-color);
}
.export-button:hover {
  background-color: var(--slidebar-item-hover-bg);
  color: var(--slidebar-item-text-color);
}
</style>
