<script setup>
import { usePageStore } from '../../stores/page'
import { useRequestStates } from '../../stores/requestStates'
import { useStatesStore } from '../../stores/states'
import { useAuthStore } from '../../stores/auth'
import APIGetters from '../../api/getters'
import APIPosts from '../../api/posts'
import api from '../../api/api'
import { openBlobInNewTab } from '../../utils/openBlobInNewTab'
import { onUnmounted, ref, watch, computed } from 'vue'

const pageStore = usePageStore()
const requestStatesStore = useRequestStates()
const statesStore = useStatesStore()
const authStore = useAuthStore()

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

const selectedIds = ref(new Set())
const pendingBulkStatus = ref('')
const showDeleteConfirm = ref(false)
const bulkLoading = ref(false)

const USER_STATUSES = ['pending', 'processing', 'in activation', 'active', 'inoperative']

const isAllSelected = computed(
  () =>
    objectsList.value.length > 0 &&
    objectsList.value.every((o) => selectedIds.value.has(o.id)),
)

const toggleRow = (id) => {
  const next = new Set(selectedIds.value)
  if (next.has(id)) next.delete(id)
  else next.add(id)
  selectedIds.value = next
}

const toggleAll = () => {
  if (isAllSelected.value) {
    selectedIds.value = new Set()
  } else {
    selectedIds.value = new Set(objectsList.value.map((o) => o.id))
  }
}

const clearSelection = () => {
  selectedIds.value = new Set()
  pendingBulkStatus.value = ''
}

const applyBulkStatus = async () => {
  if (!pendingBulkStatus.value || selectedIds.value.size === 0) return
  bulkLoading.value = true
  try {
    await APIPosts.bulkUpdateStatus(props.adres, [...selectedIds.value], pendingBulkStatus.value)
    clearSelection()
    await fetchAndSet()
  } finally {
    bulkLoading.value = false
  }
}

const confirmBulkDelete = () => {
  showDeleteConfirm.value = true
}

const executeBulkDelete = async () => {
  bulkLoading.value = true
  showDeleteConfirm.value = false
  try {
    await APIPosts.bulkDelete(props.adres, [...selectedIds.value])
    clearSelection()
    await fetchAndSet()
  } finally {
    bulkLoading.value = false
  }
}

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
    clearSelection()
    fetchAndSet()
  },
)

watch(
  () => statesStore.state,
  (newState) => {
    if (newState === 'table') {
      fetchAndSet()
    }
  },
)

onUnmounted(() => clearTimeout(retryTimeout))

const handleExport = () => {
  const token = authStore.getToken
  const baseUrl = import.meta.env.VITE_API_URL
  const downloadUrl = `${baseUrl}/users/export?token=${token}`
  window.open(downloadUrl, '_blank')
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
  } else if (norm === 'in activation') {
    return 'bg-purple-50 dark:bg-purple-950/30 text-purple-700 dark:text-purple-400 border border-purple-200 dark:border-purple-800'
  } else {
    return 'bg-surface-container-high dark:bg-white/10 text-secondary dark:text-secondary-fixed-dim border border-outline-variant/40 dark:border-white/10'
  }
}

const getInitials = (name) => {
  if (!name) return 'U'
  return name
    .split(' ')
    .map((n) => n[0])
    .join('')
    .toUpperCase()
    .slice(0, 2)
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

const updateSearch = (val) => {
  pageStore.paginationData.search = val
  pageStore.paginationData.page = 1
}

const updateFilter = (val) => {
  pageStore.filter = val
  pageStore.paginationData.page = 1
}

const formatDate = (val) => {
  if (!val) return '—'
  if (typeof val === 'string') {
    const tIndex = val.indexOf('T')
    if (tIndex !== -1) {
      return val.substring(0, tIndex)
    }
    const spaceIndex = val.indexOf(' ')
    if (spaceIndex !== -1 && val.includes('-')) {
      return val.substring(0, spaceIndex)
    }
  }
  return val
}

const formatAmount = (val) => {
  if (val === null || val === undefined || val === '') return '—'
  const num = Number(val)
  if (Number.isNaN(num)) return val
  return num.toLocaleString('cs-CZ', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
}

const openReceiptFile = async (fileId) => {
  if (!fileId) return
  try {
    await openBlobInNewTab(
      async () => (await api.get(`/files/${fileId}`, { responseType: 'blob', timeout: 0 })).data,
      'Чек',
    )
  } catch (error) {
    console.error('Failed to open receipt file:', error)
  }
}

const selectChip = (val) => {
  if (pageStore.paginationData.search === val) {
    pageStore.paginationData.search = ''
  } else {
    pageStore.paginationData.search = val
  }
  pageStore.paginationData.page = 1
}

const getChipClasses = (chip) => {
  const norm = String(chip).toLowerCase()
  if (norm === 'pending') {
    return 'bg-blue-50/50 dark:bg-blue-950/10 text-blue-600 dark:text-blue-400 border-blue-200 dark:border-blue-900/50 hover:bg-blue-50 dark:hover:bg-blue-950/20'
  } else if (norm === 'processing') {
    return 'bg-amber-50/50 dark:bg-amber-950/10 text-amber-600 dark:text-amber-400 border-amber-200 dark:border-amber-900/50 hover:bg-amber-50 dark:hover:bg-amber-950/20'
  } else if (norm === 'in activation') {
    return 'bg-purple-50/50 dark:bg-purple-950/10 text-purple-600 dark:text-purple-400 border-purple-200 dark:border-purple-900/50 hover:bg-purple-50 dark:hover:bg-purple-950/20'
  } else if (norm === 'inoperative') {
    return 'bg-red-50/50 dark:bg-red-950/10 text-red-600 dark:text-red-400 border-red-200 dark:border-red-900/50 hover:bg-red-50 dark:hover:bg-red-950/20'
  }
  return 'bg-surface-container-high dark:bg-white/10 text-secondary dark:text-secondary-fixed-dim border border-outline-variant/40 dark:border-white/10 hover:bg-surface-container'
}

const getChipActiveClasses = (chip) => {
  const norm = String(chip).toLowerCase()
  if (norm === 'pending') {
    return 'bg-blue-100 dark:bg-blue-900/50 text-blue-800 dark:text-blue-200 border-blue-400 dark:border-blue-700 shadow-sm ring-2 ring-blue-500/20'
  } else if (norm === 'processing') {
    return 'bg-amber-100 dark:bg-amber-900/50 text-amber-800 dark:text-amber-200 border-amber-400 dark:border-amber-700 shadow-sm ring-2 ring-amber-500/20'
  } else if (norm === 'in activation') {
    return 'bg-purple-100 dark:bg-purple-900/50 text-purple-800 dark:text-purple-200 border-purple-400 dark:border-purple-700 shadow-sm ring-2 ring-purple-500/20'
  } else if (norm === 'inoperative') {
    return 'bg-red-100 dark:bg-red-900/50 text-red-800 dark:text-red-200 border-red-400 dark:border-red-700 shadow-sm ring-2 ring-red-500/20'
  }
  return 'bg-primary text-on-primary border-primary shadow-sm ring-2 ring-primary/20'
}
</script>

<template>
  <main class="min-h-screen w-full px-margin-desktop pb-12 pt-[100px]">
    <div class="mx-auto max-w-[1280px] space-y-gutter">
      <!-- Section Header -->
      <section class="flex flex-col md:flex-row md:items-end justify-between gap-4">
        <div>
          <div class="flex items-center gap-3 mb-2">
            <h2
              class="font-headline-md text-headline-md font-bold text-on-background dark:text-white"
            >
              {{
                adres === '/users'
                  ? 'Пользователи'
                  : adres === '/receipts'
                    ? 'Чеки'
                    : 'Администраторы'
              }}
            </h2>
            <span
              class="px-2.5 py-0.5 bg-primary/10 dark:bg-primary/20 text-primary dark:text-inverse-primary rounded-full font-label-md text-label-md"
            >
              {{ objectsList.length }}
            </span>
          </div>
          <p class="font-body-md text-body-md text-secondary dark:text-secondary-fixed-dim">
            {{
              adres === '/users'
                ? 'Управление доступом и статусами сотрудников организации.'
                : adres === '/receipts'
                  ? 'Учёт расходов и хранение чеков.'
                  : 'Системные администраторы панели управления.'
            }}
          </p>
        </div>

        <div class="flex items-center gap-3">
          <button
            v-if="adres === '/users'"
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
            <span
              class="material-symbols-outlined absolute left-4 top-1/2 -translate-y-1/2 text-secondary group-focus-within:text-primary transition-colors"
              >search</span
            >
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
              <option
                value=""
                class="bg-surface-container-lowest dark:bg-inverse-surface text-on-surface dark:text-white"
              >
                По всем полям
              </option>
              <option
                :value="field.key"
                v-for="field in form?.fields"
                :key="field.key"
                class="bg-surface-container-lowest dark:bg-inverse-surface text-on-surface dark:text-white"
              >
                {{ field.label }}
              </option>
            </select>
          </div>
        </div>

        <!-- Chips Section -->
        <div v-if="adres === '/users'" class="flex flex-wrap gap-2.5 items-center pl-1">
          <span
            class="text-xs text-secondary dark:text-secondary-fixed-dim font-medium mr-1 select-none"
            >Быстрый поиск по статусу:</span
          >

          <button
            v-for="chip in ['pending', 'processing', 'in activation', 'inoperative']"
            :key="chip"
            @click="selectChip(chip)"
            :class="[
              'px-3.5 py-1 rounded-full text-[12px] font-semibold tracking-wide border cursor-pointer select-none transition-all duration-200 active:scale-[0.96]',
              pageStore.paginationData.search === chip
                ? getChipActiveClasses(chip)
                : getChipClasses(chip),
            ]"
          >
            {{ chip }}
          </button>

          <button
            v-if="pageStore.paginationData.search"
            @click="selectChip('')"
            class="px-2.5 py-1 rounded-full text-[12px] font-medium text-secondary hover:text-primary dark:text-secondary-fixed-dim dark:hover:text-white flex items-center gap-1 cursor-pointer transition-colors"
          >
            <span class="material-symbols-outlined text-[14px]">close</span>
            Сбросить
          </button>
        </div>
      </section>

      <!-- Bulk Action Bar -->
      <section
        v-if="adres === '/users' && selectedIds.size > 0"
        class="flex flex-wrap items-center gap-3 px-5 py-3 bg-primary/5 dark:bg-primary/10 border border-primary/20 dark:border-primary/30 rounded-xl"
      >
        <span class="font-label-md text-label-md font-semibold text-primary dark:text-inverse-primary flex items-center gap-2">
          <span class="material-symbols-outlined text-[18px]">check_box</span>
          {{ selectedIds.size }} выбрано
        </span>

        <div class="flex items-center gap-2 ml-auto flex-wrap">
          <select
            v-model="pendingBulkStatus"
            class="h-9 px-3 bg-surface-container-lowest dark:bg-white/5 border border-outline-variant/30 dark:border-white/10 rounded-lg text-body-sm text-on-surface dark:text-white focus:outline-none focus:ring-2 focus:ring-primary/20"
          >
            <option value="" disabled>Status</option>
            <option v-for="s in USER_STATUSES" :key="s" :value="s">{{ s }}</option>
          </select>
          <button
            @click="applyBulkStatus"
            :disabled="!pendingBulkStatus || bulkLoading"
            class="h-9 px-4 bg-primary text-on-primary rounded-lg font-label-sm text-label-sm hover:brightness-110 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
          >
            Применить
          </button>
          <button
            @click="confirmBulkDelete"
            :disabled="bulkLoading"
            class="h-9 px-4 bg-error/10 dark:bg-error/20 text-error dark:text-red-400 border border-error/30 rounded-lg font-label-sm text-label-sm hover:bg-error/20 dark:hover:bg-error/30 disabled:opacity-50 disabled:cursor-not-allowed transition-all flex items-center gap-1.5"
          >
            <span class="material-symbols-outlined text-[16px]">delete</span>
            Удалить ({{ selectedIds.size }})
          </button>
          <button
            @click="clearSelection"
            class="h-9 px-3 text-secondary dark:text-secondary-fixed-dim hover:text-primary rounded-lg font-label-sm text-label-sm transition-colors"
          >
            Сбросить
          </button>
        </div>
      </section>

      <!-- Delete Confirmation Modal -->
      <Teleport to="body">
        <div
          v-if="showDeleteConfirm"
          class="fixed inset-0 z-50 flex items-center justify-center bg-black/40 dark:bg-black/60 backdrop-blur-sm"
          @click.self="showDeleteConfirm = false"
        >
          <div class="bg-surface dark:bg-surface-container-high rounded-2xl shadow-xl border border-outline-variant/30 dark:border-white/10 p-6 max-w-sm w-full mx-4">
            <div class="flex items-center gap-3 mb-3">
              <span class="material-symbols-outlined text-error text-[28px]">warning</span>
              <h3 class="font-headline-sm text-headline-sm font-bold text-on-surface dark:text-white">
                Подтвердите удаление
              </h3>
            </div>
            <p class="font-body-md text-body-md text-secondary dark:text-secondary-fixed-dim mb-6">
              Будет удалено <strong class="text-error">{{ selectedIds.size }}</strong> пользователей вместе с их документами и договорами. Это действие необратимо.
            </p>
            <div class="flex gap-3 justify-end">
              <button
                @click="showDeleteConfirm = false"
                class="px-5 py-2 rounded-xl border border-outline-variant/40 dark:border-white/10 text-secondary dark:text-secondary-fixed-dim font-label-md text-label-md hover:bg-surface-container dark:hover:bg-white/5 transition-all"
              >
                Отмена
              </button>
              <button
                @click="executeBulkDelete"
                class="px-5 py-2 rounded-xl bg-error text-on-error font-label-md text-label-md hover:brightness-110 active:scale-[0.98] transition-all"
              >
                Удалить
              </button>
            </div>
          </div>
        </div>
      </Teleport>

      <!-- Data Table Wrapper -->
      <section
        class="bg-surface-container-lowest dark:bg-white/5 rounded-xl border border-outline-variant/30 dark:border-white/10 shadow-[0_8px_24px_rgba(175,16,26,0.02)] overflow-hidden"
      >
        <div class="overflow-x-auto custom-scrollbar">
          <table class="w-full text-left border-collapse">
            <!-- Table Header -->
            <thead
              class="bg-surface-container-high/30 dark:bg-white/5 border-b border-outline-variant/20 dark:border-white/10 text-secondary dark:text-secondary-fixed-dim font-label-sm text-label-sm uppercase tracking-wider"
            >
              <tr v-if="adres === '/users'">
                <th class="px-4 py-4 w-10">
                  <input
                    type="checkbox"
                    :checked="isAllSelected"
                    @change="toggleAll"
                    class="w-4 h-4 rounded border-outline-variant/50 text-primary focus:ring-primary/20 cursor-pointer"
                  />
                </th>
                <th class="px-6 py-4">Пользователь</th>
                <th class="px-6 py-4">Телефон</th>
                <th class="px-6 py-4">Город</th>
                <th class="px-6 py-4">Работает в</th>
                <th class="px-6 py-4">Статус</th>
              </tr>
              <tr v-else-if="adres === '/receipts'">
                <th class="px-6 py-4">Дата чека</th>
                <th class="px-6 py-4">Сумма</th>
                <th class="px-6 py-4">Описание</th>
                <th class="px-6 py-4">Файл</th>
                <th class="px-6 py-4">Дата создания</th>
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
                  :class="[
                    'hover:bg-surface-container-low dark:hover:bg-white/5 transition-colors cursor-pointer',
                    selectedIds.has(obj.id) ? 'bg-primary/5 dark:bg-primary/10' : '',
                  ]"
                >
                  <td class="px-4 py-4 w-10" @click.stop>
                    <input
                      type="checkbox"
                      :checked="selectedIds.has(obj.id)"
                      @change="toggleRow(obj.id)"
                      class="w-4 h-4 rounded border-outline-variant/50 text-primary focus:ring-primary/20 cursor-pointer"
                    />
                  </td>
                  <td class="px-6 py-4 flex items-center gap-4">
                    <div
                      class="w-10 h-10 rounded-full bg-primary/10 text-primary dark:text-inverse-primary flex items-center justify-center font-bold text-sm"
                    >
                      {{ getInitials(obj.name) }}
                    </div>
                    <div class="flex flex-col">
                      <span
                        class="font-label-md text-label-md font-bold text-on-surface dark:text-white"
                        >{{ obj.name || 'Без имени' }}</span
                      >
                      <span class="text-xs text-secondary dark:text-secondary-fixed-dim">{{
                        obj.email || '—'
                      }}</span>
                    </div>
                  </td>
                  <td
                    class="px-6 py-4 font-body-md text-body-md text-on-surface dark:text-secondary-fixed-dim"
                  >
                    {{ obj.phone || '—' }}
                  </td>
                  <td
                    class="px-6 py-4 font-body-md text-body-md text-on-surface dark:text-secondary-fixed-dim"
                  >
                    {{ obj.city || '—' }}
                  </td>
                  <td
                    class="px-6 py-4 font-body-md text-body-md text-on-surface dark:text-secondary-fixed-dim"
                  >
                    {{ obj.work_in || '—' }}
                  </td>
                  <td class="px-6 py-4">
                    <span
                      :class="[
                        'px-3 py-1 rounded-full text-[11px] font-bold uppercase tracking-wider',
                        getStatusClasses(obj.status),
                      ]"
                    >
                      {{ obj.status || '—' }}
                    </span>
                  </td>
                </tr>
              </template>

              <!-- Receipts view custom row styling -->
              <template v-else-if="adres === '/receipts'">
                <tr
                  v-for="obj in objectsList"
                  :key="obj.id"
                  @click="openDetails(obj.id)"
                  class="hover:bg-surface-container-low dark:hover:bg-white/5 transition-colors cursor-pointer"
                >
                  <td
                    class="px-6 py-4 font-body-md text-body-md text-on-surface dark:text-white font-semibold"
                  >
                    {{ formatDate(obj.receipt_date) }}
                  </td>
                  <td
                    class="px-6 py-4 font-body-md text-body-md text-on-surface dark:text-white font-bold whitespace-nowrap"
                  >
                    {{ formatAmount(obj.amount) }} CZK
                  </td>
                  <td
                    class="px-6 py-4 font-body-md text-body-md text-secondary dark:text-secondary-fixed-dim max-w-xs truncate"
                  >
                    {{ obj.description || '—' }}
                  </td>
                  <td class="px-6 py-4" @click.stop>
                    <button
                      v-if="obj.file_id"
                      @click="openReceiptFile(obj.file_id)"
                      class="inline-flex items-center gap-1.5 text-primary dark:text-inverse-primary hover:underline font-label-md text-label-md"
                    >
                      <span class="material-symbols-outlined text-[18px]">attach_file</span>
                      Открыть
                    </button>
                    <span v-else class="text-secondary dark:text-secondary-fixed-dim">—</span>
                  </td>
                  <td
                    class="px-6 py-4 font-body-md text-body-md text-secondary dark:text-secondary-fixed-dim"
                  >
                    {{ formatDate(obj.created_date) }}
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
                    <div
                      class="w-10 h-10 rounded-full bg-primary-container/10 dark:bg-primary-container/20 text-primary dark:text-inverse-primary flex items-center justify-center font-bold text-sm"
                    >
                      <span class="material-symbols-outlined text-[20px]">shield_person</span>
                    </div>
                    <div class="flex flex-col">
                      <span
                        class="font-label-md text-label-md font-bold text-on-surface dark:text-white"
                        >{{ obj.username || 'Админ' }}</span
                      >
                      <span class="text-xs text-secondary dark:text-secondary-fixed-dim"
                        >ID: {{ obj.id }}</span
                      >
                    </div>
                  </td>
                  <td
                    class="px-6 py-4 font-body-md text-body-md text-on-surface dark:text-secondary-fixed-dim"
                  >
                    {{ formatDate(obj.last_login_at) }}
                  </td>
                  <td
                    class="px-6 py-4 font-body-md text-body-md text-on-surface dark:text-secondary-fixed-dim"
                  >
                    {{ formatDate(obj.created_at) }}
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
