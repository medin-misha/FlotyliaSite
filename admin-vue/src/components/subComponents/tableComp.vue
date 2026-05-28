<script setup>
import { usePageStore } from '../../stores/page'
import { useRequestStates } from '../../stores/requestStates'
import { useStatesStore } from '../../stores/states'
import APIGetters from '../../api/getters'
import { onUnmounted, ref, watch, computed } from 'vue'

const pageStore = usePageStore()
const requestStatesStore = useRequestStates()
const statesStore = useStatesStore()

const props = defineProps({
  adres: String,
  page: Number,
  limit: Number,
  search: String,
  filter: String,
  form: Object,
})

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
  } catch {
    requestStatesStore.setState('networkError')
  }
  retryTimeout = setTimeout(fetchWithRetry, 10000)
}

const objectsList = ref([])

const fetchAndSet = async () => {
  const res = await fetchWithRetry()
  if (res?.data) {
    objectsList.value = res.data
  }
}

fetchAndSet()

watch(
  () => [props.page, props.limit, props.search, props.filter],
  () => {
    fetchAndSet()
  }
)

onUnmounted(() => clearTimeout(retryTimeout))

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

const getStatusClasses = (status) => {
  const norm = String(status).toLowerCase()
  if (norm === 'active') {
    return 'bg-green-50 dark:bg-green-950/30 text-green-700 dark:text-green-400 border border-green-200 dark:border-green-800'
  } else if (norm === 'pending') {
    return 'bg-blue-50 dark:bg-blue-950/30 text-blue-700 dark:text-blue-400 border border-blue-200 dark:border-blue-800'
  } else if (norm === 'inoperative') {
    return 'bg-red-50 dark:bg-red-950/30 text-red-700 dark:text-red-400 border border-red-200 dark:border-red-800'
  } else if (norm === 'processing') {
    return 'bg-amber-50 dark:bg-amber-950/30 text-amber-700 dark:text-amber-400 border border-amber-200 dark:border-amber-800'
  } else {
    return 'bg-surface-container-high dark:bg-white/10 text-secondary dark:text-secondary-fixed-dim border border-outline-variant/40 dark:border-white/10'
  }
}

const getInitials = (name) => {
  if (!name) return 'U'
  return name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2)
}

const isLastPage = computed(() => objectsList.value.length < props.limit)

const openCreate = () => {
  statesStore.setCreateState()
}

const openDetails = (id) => {
  statesStore.setDetailState(Number(id))
}

const changePage = (page) => {
  pageStore.paginationData.page = page
}

let searchDebounceTimeout = null
const updateSearch = (val) => {
  clearTimeout(searchDebounceTimeout)
  searchDebounceTimeout = setTimeout(() => {
    pageStore.paginationData.search = val
    pageStore.paginationData.page = 1
  }, 300)
}

const updateFilter = (val) => {
  pageStore.filter = val
  pageStore.paginationData.page = 1
}
</script>

<template>
  <main class="min-h-screen w-full px-margin-desktop pb-12 pt-[100px]">
    <div class="mx-auto max-w-[1280px] space-y-gutter">
      <!-- Section Header -->
      <section class="flex flex-col md:flex-row md:items-end justify-between gap-4">
        <div>
          <div class="flex items-center gap-3 mb-2">
            <h2 class="font-headline-md text-headline-md font-bold text-on-background dark:text-white">
              {{ adres === '/users' ? 'Пользователи' : 'Администраторы' }}
            </h2>
            <span class="px-2.5 py-0.5 bg-primary/10 dark:bg-primary/20 text-primary dark:text-inverse-primary rounded-full font-label-md text-label-md">
              {{ objectsList.length }}
            </span>
          </div>
          <p class="font-body-md text-body-md text-secondary dark:text-secondary-fixed-dim">
            {{ adres === '/users' ? 'Управление доступом и статусами сотрудников организации.' : 'Системные администраторы панели управления.' }}
          </p>
        </div>

        <div class="flex items-center gap-3">
          <button
            @click="handleExport"
            class="flex items-center gap-2 px-5 py-2.5 bg-surface-container-lowest dark:bg-white/5 border border-outline-variant/50 dark:border-white/10 text-on-surface dark:text-secondary-fixed-dim rounded-xl font-label-md text-label-md hover:bg-surface-container dark:hover:bg-white/10 active:scale-[0.98] transition-all"
          >
            <span class="material-symbols-outlined text-[18px]">file_download</span>
            Экспорт в Excel
          </button>
          <button
            @click="openCreate"
            class="flex items-center gap-2 px-5 py-2.5 bg-primary text-on-primary rounded-xl font-label-md text-label-md shadow-md hover:brightness-110 active:scale-[0.98] transition-all"
          >
            <span class="material-symbols-outlined text-[18px]">person_add</span>
            Добавить
          </button>
        </div>
      </section>

      <!-- Search and Filters Section -->
      <section class="space-y-4">
        <div class="flex flex-col md:flex-row gap-4">
          <!-- Search Input -->
          <div class="relative flex-grow max-w-2xl group">
            <span class="material-symbols-outlined absolute left-4 top-1/2 -translate-y-1/2 text-secondary group-focus-within:text-primary transition-colors">search</span>
            <input
              :value="pageStore.paginationData.search"
              @input="updateSearch($event.target.value)"
              class="w-full pl-12 pr-4 py-3.5 bg-surface-container-lowest dark:bg-white/5 border border-outline-variant/30 dark:border-white/10 rounded-full font-body-md text-body-md focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary dark:focus:border-primary-fixed-dim text-on-surface dark:text-white transition-all shadow-sm"
              placeholder="Поиск по имени, e-mail или телефону..."
              type="text"
            />
          </div>

          <!-- Select Filter Type -->
          <div class="relative w-full md:w-60">
            <select
              :value="pageStore.filter"
              @change="updateFilter($event.target.value)"
              class="w-full h-[52px] px-4 bg-surface-container-lowest dark:bg-white/5 border border-outline-variant/30 dark:border-white/10 rounded-full text-body-md text-secondary dark:text-secondary-fixed-dim focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary dark:focus:border-primary-fixed-dim transition-all appearance-none"
            >
              <option value="" class="bg-surface-container-lowest dark:bg-inverse-surface text-on-surface dark:text-white">По всем полям</option>
              <option :value="field.key" v-for="field in form?.fields" :key="field.key" class="bg-surface-container-lowest dark:bg-inverse-surface text-on-surface dark:text-white">
                {{ field.label }}
              </option>
            </select>
          </div>
        </div>
      </section>

      <!-- Data Table Wrapper -->
      <section class="bg-surface-container-lowest dark:bg-white/5 rounded-xl border border-outline-variant/30 dark:border-white/10 shadow-[0_8px_24px_rgba(175,16,26,0.02)] overflow-hidden">
        <div class="overflow-x-auto custom-scrollbar">
          <table class="w-full text-left border-collapse">
            <!-- Table Header -->
            <thead class="bg-surface-container-high/30 dark:bg-white/5 border-b border-outline-variant/20 dark:border-white/10 text-secondary dark:text-secondary-fixed-dim font-label-sm text-label-sm uppercase tracking-wider">
              <tr v-if="adres === '/users'">
                <th class="px-6 py-4">Пользователь</th>
                <th class="px-6 py-4">Телефон</th>
                <th class="px-6 py-4">Город</th>
                <th class="px-6 py-4">Работает в</th>
                <th class="px-6 py-4">Статус</th>
              </tr>
              <tr v-else>
                <th class="px-6 py-4">Администратор</th>
                <th class="px-6 py-4">Последняя сессия</th>
                <th class="px-6 py-4">Дата создания</th>
              </tr>
            </thead>

            <!-- Table Body -->
            <tbody class="divide-y divide-outline-variant/10 dark:divide-white/5">
              <!-- Users view custom row styling -->
              <template v-if="adres === '/users'">
                <tr
                  v-for="obj in objectsList"
                  :key="obj.id"
                  @click="openDetails(obj.id)"
                  class="hover:bg-surface-container-low dark:hover:bg-white/5 transition-colors cursor-pointer"
                >
                  <td class="px-6 py-4 flex items-center gap-4">
                    <div class="w-10 h-10 rounded-full bg-primary/10 text-primary dark:text-inverse-primary flex items-center justify-center font-bold text-sm">
                      {{ getInitials(obj.name) }}
                    </div>
                    <div class="flex flex-col">
                      <span class="font-label-md text-label-md font-bold text-on-surface dark:text-white">{{ obj.name || 'Без имени' }}</span>
                      <span class="text-xs text-secondary dark:text-secondary-fixed-dim">{{ obj.email || '—' }}</span>
                    </div>
                  </td>
                  <td class="px-6 py-4 font-body-md text-body-md text-on-surface dark:text-secondary-fixed-dim">
                    {{ obj.phone || '—' }}
                  </td>
                  <td class="px-6 py-4 font-body-md text-body-md text-on-surface dark:text-secondary-fixed-dim">
                    {{ obj.city || '—' }}
                  </td>
                  <td class="px-6 py-4 font-body-md text-body-md text-on-surface dark:text-secondary-fixed-dim">
                    {{ obj.work_in || '—' }}
                  </td>
                  <td class="px-6 py-4">
                    <span :class="['px-3 py-1 rounded-full text-[11px] font-bold uppercase tracking-wider', getStatusClasses(obj.status)]">
                      {{ obj.status || '—' }}
                    </span>
                  </td>
                </tr>
              </template>

              <!-- Admins view custom row styling -->
              <template v-else>
                <tr
                  v-for="obj in objectsList"
                  :key="obj.id"
                  @click="openDetails(obj.id)"
                  class="hover:bg-surface-container-low dark:hover:bg-white/5 transition-colors cursor-pointer"
                >
                  <td class="px-6 py-4 flex items-center gap-4">
                    <div class="w-10 h-10 rounded-full bg-primary-container/10 dark:bg-primary-container/20 text-primary dark:text-inverse-primary flex items-center justify-center font-bold text-sm">
                      <span class="material-symbols-outlined text-[20px]">shield_person</span>
                    </div>
                    <div class="flex flex-col">
                      <span class="font-label-md text-label-md font-bold text-on-surface dark:text-white">{{ obj.username || 'Админ' }}</span>
                      <span class="text-xs text-secondary dark:text-secondary-fixed-dim">ID: {{ obj.id }}</span>
                    </div>
                  </td>
                  <td class="px-6 py-4 font-body-md text-body-md text-on-surface dark:text-secondary-fixed-dim">
                    {{ obj.last_login_at || '—' }}
                  </td>
                  <td class="px-6 py-4 font-body-md text-body-md text-on-surface dark:text-secondary-fixed-dim">
                    {{ obj.created_at || '—' }}
                  </td>
                </tr>
              </template>
            </tbody>
          </table>
        </div>
      </section>

      <!-- Pagination Footer -->
      <footer class="flex items-center justify-center gap-4 mt-6">
        <button
          @click="changePage(pageStore.paginationData.page - 1)"
          :disabled="pageStore.paginationData.page - 1 < 1"
          class="w-10 h-10 rounded-xl bg-surface-container-lowest dark:bg-white/5 border border-outline-variant/30 dark:border-white/10 flex items-center justify-center text-secondary dark:text-secondary-fixed-dim hover:bg-surface-container dark:hover:bg-white/10 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
        >
          <span class="material-symbols-outlined text-[18px]">chevron_left</span>
        </button>
        <span class="font-label-md text-label-md font-bold text-on-surface dark:text-white px-2">
          Страница {{ pageStore.paginationData.page }}
        </span>
        <button
          @click="changePage(pageStore.paginationData.page + 1)"
          :disabled="isLastPage"
          class="w-10 h-10 rounded-xl bg-surface-container-lowest dark:bg-white/5 border border-outline-variant/30 dark:border-white/10 flex items-center justify-center text-secondary dark:text-secondary-fixed-dim hover:bg-surface-container dark:hover:bg-white/10 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
        >
          <span class="material-symbols-outlined text-[18px]">chevron_right</span>
        </button>
      </footer>
    </div>
  </main>
</template>

<style scoped>
/* Scrollbar optimizations */
</style>
