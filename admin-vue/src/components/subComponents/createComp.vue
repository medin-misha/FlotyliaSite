<script setup>
import { reactive, ref, computed } from 'vue'
import { usePageStore } from '../../stores/page'
import { useStatesStore } from '../../stores/states'
import APIPosts from '../../api/posts'

const statesStore = useStatesStore()
const pageStore = usePageStore()
const form = pageStore.pageData.createSchema

const modelData = reactive({})
const errors = reactive({})
const globalError = ref(null)
const isSaving = ref(false)

// Initialize form model values
for (const x of form.fields) {
  modelData[x.key] = x.type === 'boolean' ? false : ''
}

const isUsers = computed(() => pageStore.pageData.name === 'Users')

// Tabs definition for Users creation
const sections = [
  {
    id: 'personal',
    label: 'Личные данные',
    icon: 'person',
    fields: ['name', 'birth_date', 'citizenship'],
  },
  {
    id: 'contacts',
    label: 'Контакты',
    icon: 'alternate_email',
    fields: ['email', 'phone', 'telegram', 'whatsapp', 'city', 'address'],
  },
  {
    id: 'work_finance',
    label: 'Работа и оплата',
    icon: 'payments',
    fields: ['work_in', 'desired_transport', 'invoice', 'how_found_it'],
  },
  {
    id: 'settings',
    label: 'Параметры',
    icon: 'tune',
    fields: ['status', 'consent'],
  },
]

const currentTab = ref('personal')

// Get fields that should be visible on the current tab (or all fields if not Users)
const visibleFields = computed(() => {
  if (!isUsers.value) return form.fields
  const activeSection = sections.find((s) => s.id === currentTab.value)
  if (!activeSection) return form.fields
  return form.fields.filter((f) => activeSection.fields.includes(f.key))
})

// Check if a section has any fields with active errors
const sectionHasError = (sectionId) => {
  const section = sections.find((s) => s.id === sectionId)
  if (!section) return false
  return section.fields.some((fKey) => !!errors[fKey])
}

// Client-side validations
const validateForm = () => {
  let isValid = true

  // Clear previous errors
  globalError.value = null
  for (const key in errors) {
    errors[key] = null
  }

  for (const item of form.fields) {
    // Required fields check
    if (item.required) {
      if (item.type === 'boolean') {
        if (!modelData[item.key]) {
          errors[item.key] = 'Необходимо подтвердить согласие'
          isValid = false
        }
      } else if (!modelData[item.key] || String(modelData[item.key]).trim() === '') {
        errors[item.key] = `Поле «${item.label}» обязательно для заполнения`
        isValid = false
      }
    }

    // E-mail validation format check
    if (item.key === 'email' && modelData[item.key]) {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
      if (!emailRegex.test(modelData[item.key])) {
        errors[item.key] = 'Пожалуйста, введите корректный адрес эл. почты'
        isValid = false
      }
    }

    // Phone length check
    if (item.key === 'phone' && modelData[item.key]) {
      const cleanedPhone = String(modelData[item.key]).replace(/\D/g, '')
      if (cleanedPhone.length < 5 || cleanedPhone.length > 15) {
        errors[item.key] = 'Длина номера телефона должна быть от 5 до 15 цифр'
        isValid = false
      }
    }
  }

  // If there are errors, automatically switch to the first tab that has an error
  if (!isValid && isUsers.value) {
    for (const section of sections) {
      if (sectionHasError(section.id)) {
        currentTab.value = section.id
        break
      }
    }
  }

  return isValid
}

const create = async () => {
  if (!validateForm()) return

  isSaving.value = true

  try {
    // Clean payload: convert all empty string fields ("") to null if they are optional
    const cleanedPayload = {}
    for (const key in modelData) {
      const value = modelData[key]
      const fieldDef = form.fields.find((f) => f.key === key)

      if (value === '' && (!fieldDef || !fieldDef.required)) {
        cleanedPayload[key] = null
      } else {
        cleanedPayload[key] = value
      }
    }

    // Perform standard creation
    await APIPosts.createPost(pageStore.pageData.adres, cleanedPayload)
    statesStore.setTableState()
  } catch (error) {
    console.error('Creation failed:', error)

    const responseData = error.response?.data
    if (responseData && responseData.detail) {
      if (Array.isArray(responseData.detail)) {
        // FastAPI / Pydantic validation error format
        globalError.value = 'Пожалуйста, исправьте ошибки валидации в форме.'
        for (const errItem of responseData.detail) {
          const fieldKey = errItem.loc[errItem.loc.length - 1]
          errors[fieldKey] = errItem.msg
        }

        // Auto switch tab if errors occur in a specific section
        if (isUsers.value) {
          for (const section of sections) {
            if (sectionHasError(section.id)) {
              currentTab.value = section.id
              break
            }
          }
        }
      } else if (typeof responseData.detail === 'string') {
        globalError.value = responseData.detail
      } else {
        globalError.value = 'Ошибка на стороне сервера. Проверьте введенные данные.'
      }
    } else {
      globalError.value = 'Не удалось связаться с сервером. Пожалуйста, попробуйте позже.'
    }
  } finally {
    isSaving.value = false
  }
}
</script>

<template>
  <main
    class="flex min-h-screen w-full items-start justify-center bg-background px-margin-desktop pb-12 pt-[100px] dark:bg-on-background"
  >
    <div
      class="w-full max-w-4xl bg-surface-container-lowest dark:bg-[#16181c] rounded-xl border border-outline-variant/30 dark:border-white/10 shadow-[0_12px_32px_rgba(175,16,26,0.04)] overflow-hidden flex flex-col transition-all duration-300"
    >
      <!-- Card Header -->
      <div
        class="p-stack-lg border-b border-outline-variant/30 dark:border-white/10 flex justify-between items-center bg-surface-container-lowest dark:bg-[#16181c]"
      >
        <div>
          <h2
            class="font-headline-md text-headline-md font-bold text-on-surface dark:text-white flex items-center gap-2 select-none"
          >
            <span
              class="material-symbols-outlined text-[28px] text-primary dark:text-inverse-primary"
              >person_add</span
            >
            <span>Создать запись</span>
          </h2>
          <p
            class="font-body-md text-body-md text-secondary dark:text-secondary-fixed-dim mt-0.5 select-none"
          >
            Раздел: {{ pageStore.pageData.name === 'Users' ? 'Пользователи' : 'Администраторы' }}
          </p>
        </div>
        <div
          class="px-4 py-1.5 rounded-full bg-primary/10 text-primary dark:text-inverse-primary font-label-md text-label-md font-bold uppercase tracking-wider select-none animate-pulse"
        >
          Новая запись
        </div>
      </div>

      <!-- Global Error Notice -->
      <transition
        enter-active-class="transition duration-200 ease-out"
        enter-from-class="transform -translate-y-2 opacity-0"
        enter-to-class="transform translate-y-0 opacity-100"
        leave-active-class="transition duration-150 ease-in"
        leave-from-class="transform translate-y-0 opacity-100"
        leave-to-class="transform -translate-y-2 opacity-0"
      >
        <div
          v-if="globalError"
          class="mx-6 mt-6 p-4 rounded-xl border border-error/20 bg-error/5 text-error flex items-start gap-3 shadow-sm"
        >
          <span class="material-symbols-outlined text-[22px] shrink-0 mt-0.5">warning</span>
          <div class="flex-1">
            <h4 class="font-semibold text-sm">Ошибка сохранения</h4>
            <p class="text-xs text-error/90 mt-0.5">{{ globalError }}</p>
          </div>
          <button
            @click="globalError = null"
            class="text-error hover:opacity-85 shrink-0 transition-opacity"
          >
            <span class="material-symbols-outlined text-[18px]">close</span>
          </button>
        </div>
      </transition>

      <!-- Users Navigation Section Tabs -->
      <div
        v-if="isUsers"
        class="px-6 pt-5 border-b border-outline-variant/20 dark:border-white/5 bg-surface-container-lowest dark:bg-[#16181c]"
      >
        <nav class="flex flex-wrap gap-2 select-none" aria-label="Tabs">
          <button
            v-for="tab in sections"
            :key="tab.id"
            @click="currentTab = tab.id"
            type="button"
            class="flex items-center gap-2 px-4 py-2.5 rounded-xl text-xs font-semibold tracking-wide uppercase transition-all duration-200"
            :class="[
              currentTab === tab.id
                ? 'bg-primary text-white shadow-md shadow-primary/20 dark:bg-inverse-primary dark:text-primary dark:shadow-none'
                : 'text-secondary/70 dark:text-secondary-fixed-dim/70 hover:text-on-surface dark:hover:text-white hover:bg-surface-container-high/50 dark:hover:bg-white/5',
            ]"
          >
            <span class="material-symbols-outlined text-[18px]">{{ tab.icon }}</span>
            <span>{{ tab.label }}</span>

            <!-- Error indicator badge inside tab -->
            <span
              v-if="sectionHasError(tab.id)"
              class="w-2 h-2 rounded-full bg-error ring-2"
              :class="
                currentTab === tab.id
                  ? 'ring-white dark:ring-primary'
                  : 'ring-background dark:ring-inverse-surface'
              "
            ></span>
          </button>
        </nav>
      </div>

      <!-- Scrollable Card Body -->
      <div
        class="flex-1 p-stack-lg max-h-[calc(100vh-300px)] overflow-y-auto custom-scrollbar bg-surface-container-lowest dark:bg-[#16181c]"
      >
        <form @submit.prevent="create" class="grid grid-cols-1 md:grid-cols-2 gap-stack-lg">
          <component
            v-for="item in visibleFields"
            :key="item.key"
            :is="item.component"
            :field="item"
            :create="true"
            v-model:value="modelData[item.key]"
            :error="errors[item.key]"
          />
        </form>
      </div>

      <!-- Sticky Footer -->
      <div
        class="p-stack-lg border-t border-outline-variant/30 dark:border-white/10 bg-surface-container-lowest dark:bg-[#16181c] flex items-center justify-end gap-stack-md sticky bottom-0 z-10 shadow-[0_-4px_16px_rgba(0,0,0,0.02)]"
      >
        <button
          @click="statesStore.setTableState()"
          type="button"
          :disabled="isSaving"
          class="px-6 py-2.5 font-label-md text-label-md text-secondary dark:text-secondary-fixed-dim hover:text-on-surface dark:hover:text-white disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          Отмена
        </button>

        <button
          @click="create"
          type="button"
          :disabled="isSaving"
          class="px-8 py-2.5 bg-primary text-on-primary rounded-full font-bold flex items-center gap-2 hover:brightness-110 active:scale-[0.98] disabled:opacity-75 disabled:cursor-not-allowed transition-all shadow-lg shadow-primary/20"
        >
          <span
            v-if="isSaving"
            class="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"
          ></span>
          <span>{{ isSaving ? 'Создание...' : 'Создать' }}</span>
          <span v-if="!isSaving" class="material-symbols-outlined text-sm">add</span>
        </button>
      </div>
    </div>
  </main>
</template>

<style scoped></style>
