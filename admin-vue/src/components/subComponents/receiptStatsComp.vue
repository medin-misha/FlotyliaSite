<script setup>
import { computed, onMounted, ref } from 'vue'
import api from '../../api/api'

const MONTHS_RU = [
  'Январь',
  'Февраль',
  'Март',
  'Апрель',
  'Май',
  'Июнь',
  'Июль',
  'Август',
  'Сентябрь',
  'Октябрь',
  'Ноябрь',
  'Декабрь',
]

const rawStats = ref([]) // [{ year, month, total_amount }]
const isLoading = ref(true)
const loadError = ref(null)
const selectedYear = ref(null)

const fetchStats = async () => {
  isLoading.value = true
  loadError.value = null
  try {
    const response = await api.get('/receipts/statistics/monthly')
    rawStats.value = Array.isArray(response.data) ? response.data : []
    if (availableYears.value.length > 0) {
      selectedYear.value = availableYears.value[availableYears.value.length - 1]
    }
  } catch (error) {
    console.error('Failed to load receipt statistics:', error)
    loadError.value = 'Не удалось загрузить статистику. Попробуйте обновить страницу.'
  } finally {
    isLoading.value = false
  }
}

const availableYears = computed(() => {
  const years = [...new Set(rawStats.value.map((row) => row.year))]
  return years.sort((a, b) => a - b)
})

// Массив из 12 месяцев с суммами для выбранного года (0, если данных нет)
const monthlyRows = computed(() => {
  const totalsByMonth = {}
  for (const row of rawStats.value) {
    if (row.year === selectedYear.value) {
      totalsByMonth[row.month] = (totalsByMonth[row.month] || 0) + Number(row.total_amount)
    }
  }
  return MONTHS_RU.map((label, index) => ({
    label,
    month: index + 1,
    total: totalsByMonth[index + 1] || 0,
  }))
})

const maxTotal = computed(() => {
  const totals = monthlyRows.value.map((row) => row.total)
  const max = Math.max(...totals, 0)
  return max > 0 ? max : 1
})

const yearTotal = computed(() => monthlyRows.value.reduce((sum, row) => sum + row.total, 0))

const formatAmount = (val) =>
  Number(val || 0).toLocaleString('cs-CZ', { minimumFractionDigits: 2, maximumFractionDigits: 2 })

onMounted(fetchStats)
</script>

<template>
  <main class="min-h-screen w-full px-margin-desktop pb-12 pt-[100px]">
    <div class="mx-auto max-w-[1280px] space-y-gutter">
      <!-- Header -->
      <section class="flex flex-col md:flex-row md:items-end justify-between gap-4">
        <div>
          <div class="flex items-center gap-3 mb-2">
            <h2
              class="font-headline-md text-headline-md font-bold text-on-background dark:text-white"
            >
              Статистика расходов
            </h2>
          </div>
          <p class="font-body-md text-body-md text-secondary dark:text-secondary-fixed-dim">
            Сумма расходов по чекам в разрезе месяцев.
          </p>
        </div>

        <div v-if="availableYears.length" class="relative w-full md:w-48">
          <select
            v-model="selectedYear"
            class="w-full h-[52px] px-4 bg-surface-container-lowest dark:bg-white/5 border border-outline-variant/30 dark:border-white/10 rounded-full text-body-md text-on-surface dark:text-white focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary transition-all appearance-none"
          >
            <option
              v-for="year in availableYears"
              :key="year"
              :value="year"
              class="bg-surface-container-lowest dark:bg-inverse-surface text-on-surface dark:text-white"
            >
              {{ year }}
            </option>
          </select>
        </div>
      </section>

      <!-- Loading -->
      <div
        v-if="isLoading"
        class="flex min-h-[280px] items-center justify-center rounded-xl border border-outline-variant/20 bg-surface-container-low text-secondary dark:border-white/10 dark:bg-white/5 dark:text-secondary-fixed-dim"
      >
        Загрузка статистики...
      </div>

      <!-- Error -->
      <div
        v-else-if="loadError"
        class="rounded-xl border border-error/20 bg-error/5 p-5 text-error"
      >
        <div class="flex items-start gap-3">
          <span class="material-symbols-outlined mt-0.5 text-[22px]">warning</span>
          <div>
            <h4 class="font-label-md text-label-md font-bold">Ошибка загрузки</h4>
            <p class="mt-1 font-body-sm text-body-sm">{{ loadError }}</p>
          </div>
        </div>
      </div>

      <!-- Empty -->
      <div
        v-else-if="!availableYears.length"
        class="flex min-h-[280px] flex-col items-center justify-center gap-3 rounded-xl border border-outline-variant/20 bg-surface-container-low text-secondary dark:border-white/10 dark:bg-white/5 dark:text-secondary-fixed-dim"
      >
        <span class="material-symbols-outlined text-[40px] opacity-60">bar_chart</span>
        <p class="font-body-md text-body-md">Пока нет чеков для отображения статистики.</p>
      </div>

      <!-- Bars -->
      <section
        v-else
        class="bg-surface-container-lowest dark:bg-white/5 rounded-xl border border-outline-variant/30 dark:border-white/10 shadow-[0_8px_24px_rgba(175,16,26,0.02)] overflow-hidden p-6"
      >
        <div class="space-y-3">
          <div
            v-for="row in monthlyRows"
            :key="row.month"
            class="flex items-center gap-4"
          >
            <span
              class="w-24 shrink-0 font-label-md text-label-md text-secondary dark:text-secondary-fixed-dim"
            >
              {{ row.label }}
            </span>
            <div class="flex-grow h-7 rounded-lg bg-surface-container-high dark:bg-white/10 overflow-hidden">
              <div
                class="h-full rounded-lg bg-primary transition-all duration-500 ease-out"
                :style="{ width: `${(row.total / maxTotal) * 100}%` }"
              ></div>
            </div>
            <span
              class="w-40 shrink-0 text-right font-body-md text-body-md font-bold text-on-surface dark:text-white whitespace-nowrap"
            >
              {{ formatAmount(row.total) }} CZK
            </span>
          </div>
        </div>

        <!-- Yearly total -->
        <div
          class="mt-6 pt-4 border-t border-outline-variant/30 dark:border-white/10 flex items-center justify-between"
        >
          <span class="font-label-md text-label-md font-bold text-on-surface dark:text-white">
            Итого за {{ selectedYear }} год
          </span>
          <span class="font-headline-sm text-headline-sm font-bold text-primary dark:text-inverse-primary whitespace-nowrap">
            {{ formatAmount(yearTotal) }} CZK
          </span>
        </div>
      </section>
    </div>
  </main>
</template>

<style scoped></style>
