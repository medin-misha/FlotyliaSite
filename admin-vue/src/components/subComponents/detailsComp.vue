<script setup>
import APIGetters from '../../api/getters'
import APIPosts from '../../api/posts'
import { useStatesStore } from '../../stores/states'
import { computed, onMounted, onUnmounted, reactive, ref } from 'vue'

const props = defineProps({
  id: {
    type: Number,
    required: true,
  },
  adres: {
    type: String,
    required: true,
  },
  form: {
    type: Object,
    required: true,
  },
})

const statesStore = useStatesStore()

const objectData = reactive({})
const originalDocuments = []
const errors = reactive({})

const isVisible = ref(false)
const isLoading = ref(true)
const isSaving = ref(false)
const saveDone = ref(false)
const loadError = ref(null)
const saveError = ref(null)
const isDeleting = ref(false)
const showDeleteConfirm = ref(false)
const deleteError = ref(null)

const fields = computed(() => props.form?.fields || [])
const detailTitle = computed(() =>
  props.adres === '/users' ? 'Карточка пользователя' : 'Карточка администратора',
)
const groupedFields = computed(() => {
  const groups = {
    personal: [],
    contacts: [],
    logistics: [],
    documents: [],
    system: [],
    other: [],
  }

  for (const field of fields.value) {
    const group = field.group && groups[field.group] ? field.group : 'other'
    groups[group].push(field)
  }

  return groups
})

const sections = computed(() => {
  if (props.adres === '/users') {
    return [
      {
        key: 'personal',
        title: 'Основная информация',
        icon: 'person',
        fields: groupedFields.value.personal,
      },
      {
        key: 'contacts',
        title: 'Контактная информация',
        icon: 'contact_support',
        fields: groupedFields.value.contacts,
      },
      {
        key: 'logistics',
        title: 'Логистика и бухгалтерия',
        icon: 'inventory_2',
        fields: groupedFields.value.logistics,
      },
      {
        key: 'documents',
        title: 'Документы',
        icon: 'folder_open',
        fields: groupedFields.value.documents,
      },
      {
        key: 'other',
        title: 'Дополнительно',
        icon: 'more_horiz',
        fields: groupedFields.value.other,
      },
    ].filter((section) => section.fields.length > 0)
  }

  return [
    { key: 'personal', title: 'Профиль', icon: 'person', fields: groupedFields.value.personal },
    {
      key: 'system',
      title: 'Системные настройки',
      icon: 'shield_person',
      fields: groupedFields.value.system,
    },
    { key: 'other', title: 'Дополнительно', icon: 'more_horiz', fields: groupedFields.value.other },
  ].filter((section) => section.fields.length > 0)
})

const getSection = (key) => sections.value.find((section) => section.key === key)

const resetObjectData = (data) => {
  for (const key of Object.keys(objectData)) {
    delete objectData[key]
  }
  Object.assign(objectData, data || {})

  originalDocuments.splice(
    0,
    originalDocuments.length,
    ...JSON.parse(JSON.stringify(objectData.documents || [])),
  )
}

const loadDetails = async () => {
  if (!Number.isFinite(Number(props.id))) {
    isLoading.value = false
    loadError.value = 'Некорректный ID карточки.'
    return
  }

  isLoading.value = true
  loadError.value = null
  saveError.value = null

  try {
    const response = await APIGetters.getDetail(props.adres, props.id)
    resetObjectData(response.data)
  } catch (err) {
    console.error('Failed to load details:', err)
    loadError.value =
      'Не удалось загрузить карточку. Проверьте соединение или попробуйте открыть ее еще раз.'
  } finally {
    isLoading.value = false
  }
}

const syncDocuments = async () => {
  if (props.adres !== '/users') return

  const finalDocs = objectData.documents || []
  const deletedDocs = originalDocuments.filter(
    (originalDoc) => originalDoc.id && !finalDocs.some((doc) => doc.id === originalDoc.id),
  )

  for (const doc of deletedDocs) {
    await APIPosts.deletePost('/documents', doc.id)
  }

  for (const doc of finalDocs) {
    if (!doc.file_id) continue

    if (!doc.id) {
      await APIPosts.createPost('/documents', {
        file_id: doc.file_id,
        description: doc.description,
        user_id: props.id,
      })
      continue
    }

    const originalDoc = originalDocuments.find((item) => item.id === doc.id)
    if (
      originalDoc &&
      (originalDoc.file_id !== doc.file_id || originalDoc.description !== doc.description)
    ) {
      await APIPosts.updatePost('/documents', doc.id, {
        file_id: doc.file_id,
        description: doc.description,
      })
    }
  }
}

const updatePost = async () => {
  if (isLoading.value || isSaving.value || loadError.value) return

  isSaving.value = true
  saveError.value = null
  saveDone.value = false
  for (const key of Object.keys(errors)) {
    delete errors[key]
  }

  try {
    await APIPosts.updatePost(props.adres, props.id, objectData)
    await syncDocuments()
    originalDocuments.splice(
      0,
      originalDocuments.length,
      ...JSON.parse(JSON.stringify(objectData.documents || [])),
    )
    saveDone.value = true
  } catch (err) {
    console.error('Update failed:', err)
    const detail = err.response?.data?.detail

    if (Array.isArray(detail)) {
      saveError.value = 'Пожалуйста, исправьте ошибки валидации в форме.'
      for (const item of detail) {
        const fieldKey = item.loc?.[item.loc.length - 1]
        if (fieldKey) errors[fieldKey] = item.msg
      }
    } else if (typeof detail === 'string') {
      saveError.value = detail
    } else {
      saveError.value = 'Не удалось сохранить изменения. Проверьте соединение или попробуйте позже.'
    }
  } finally {
    isSaving.value = false
  }
}

const deletePost = async () => {
  if (isLoading.value || isSaving.value || isDeleting.value || loadError.value) return

  isDeleting.value = true
  deleteError.value = null

  try {
    await APIPosts.deletePost(props.adres, props.id)
    showDeleteConfirm.value = false
    closeDrawer()
  } catch (err) {
    console.error('Delete failed:', err)
    const detail = err.response?.data?.detail
    if (typeof detail === 'string') {
      deleteError.value = detail
    } else {
      deleteError.value = 'Не удалось удалить запись. Возможно, она связана с другими объектами.'
    }
  } finally {
    isDeleting.value = false
  }
}

const closeDrawer = () => {
  isVisible.value = false
  setTimeout(() => {
    statesStore.setTableState()
  }, 220)
}

const isMobileOrTablet = ref(false)

const checkMobile = () => {
  isMobileOrTablet.value = window.innerWidth < 1024
}

onMounted(() => {
  checkMobile()
  window.addEventListener('resize', checkMobile)
  requestAnimationFrame(() => {
    isVisible.value = true
  })
  loadDetails()
})

onUnmounted(() => {
  window.removeEventListener('resize', checkMobile)
})
</script>

<template>
  <teleport to="body" :disabled="!isMobileOrTablet">
    <div :class="isMobileOrTablet ? 'fixed inset-0 z-[60]' : ''">
      <button
        v-if="isMobileOrTablet"
        type="button"
        class="absolute inset-0 h-full w-full bg-black/30 transition-opacity duration-200 dark:bg-black/50"
        :class="isVisible ? 'opacity-100' : 'opacity-0'"
        aria-label="Закрыть карточку"
        @click="closeDrawer"
      ></button>

      <aside
        class="flex flex-col bg-surface-container-lowest dark:bg-inverse-surface border-l border-outline-variant/30 dark:border-white/10 shadow-2xl transition-transform duration-300 ease-out"
        :class="[
          isMobileOrTablet
            ? 'absolute right-0 top-0 z-[70] h-full w-full sm:w-[480px]'
            : 'fixed right-0 top-[70px] bottom-0 w-[50vw] z-30',
          isVisible ? 'translate-x-0' : 'translate-x-full',
        ]"
        :style="isMobileOrTablet ? {} : { height: 'calc(100vh - 70px)' }"
      >
        <header
          class="sticky top-0 z-10 flex items-center justify-between border-b border-outline-variant/20 bg-surface-container-lowest/90 px-stack-lg py-5 backdrop-blur-md dark:border-white/10 dark:bg-inverse-surface/90"
        >
          <div class="flex min-w-0 items-center gap-4">
            <button
              type="button"
              class="flex h-10 w-10 shrink-0 items-center justify-center rounded-full transition-colors hover:bg-surface-container-high dark:hover:bg-white/5"
              @click="closeDrawer"
            >
              <span class="material-symbols-outlined text-primary dark:text-inverse-primary"
                >arrow_back</span
              >
            </button>
            <div class="min-w-0">
              <h3
                class="truncate font-headline-sm text-headline-sm font-bold text-on-surface dark:text-white"
              >
                {{ detailTitle }}
              </h3>
              <p class="font-label-sm text-label-sm text-secondary dark:text-secondary-fixed-dim">
                ID: {{ id }}
              </p>
            </div>
          </div>

          <div class="flex items-center gap-2 shrink-0">
            <button
              v-if="!loadError"
              type="button"
              class="flex items-center gap-2 rounded-full px-4 py-2 font-label-sm text-label-sm bg-error/15 text-error hover:bg-error/25 hover:text-error transition-all active:scale-95 disabled:cursor-not-allowed disabled:opacity-60"
              :disabled="isLoading || isSaving || isDeleting"
              @click="showDeleteConfirm = true"
            >
              <span class="material-symbols-outlined text-sm">delete</span>
              <span class="hidden sm:inline">Удалить</span>
            </button>

            <button
              type="button"
              class="flex items-center gap-2 rounded-full px-4 py-2 font-label-sm text-label-sm shadow-md transition-all disabled:cursor-not-allowed disabled:opacity-60"
              :class="
                saveDone
                  ? 'bg-green-600 text-white shadow-green-600/20'
                  : 'bg-primary text-on-primary shadow-primary/20 hover:brightness-110 active:scale-95'
              "
              :disabled="isLoading || isSaving || Boolean(loadError) || isDeleting"
              @click="updatePost"
            >
              <span class="material-symbols-outlined text-sm">{{
                saveDone ? 'done' : 'save'
              }}</span>
              <span>{{ isSaving ? 'Сохранение...' : saveDone ? 'Готово' : 'Сохранить' }}</span>
            </button>
          </div>
        </header>

        <div class="flex-1 overflow-y-auto p-3 custom-scrollbar">
          <div
            v-if="isLoading"
            class="flex min-h-[280px] items-center justify-center rounded-xl border border-outline-variant/20 bg-surface-container-low text-secondary dark:border-white/10 dark:bg-white/5 dark:text-secondary-fixed-dim"
          >
            Загрузка карточки...
          </div>

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

          <div v-else class="space-y-3 pb-4">
            <div
              v-if="saveError"
              class="rounded-xl border border-error/20 bg-error/5 p-4 text-error"
            >
              <div class="flex items-start gap-3">
                <span class="material-symbols-outlined mt-0.5 text-[22px]">warning</span>
                <div>
                  <h4 class="font-label-md text-label-md font-bold">Ошибка сохранения</h4>
                  <p class="mt-1 font-body-sm text-body-sm">{{ saveError }}</p>
                </div>
              </div>
            </div>

            <!-- Users layout -->
            <template v-if="adres === '/users'">
              <!-- Row 1: Basic info & Documents side by side -->
              <div class="grid grid-cols-1 lg:grid-cols-2 gap-3 items-start">
                <!-- Personal / Basic Info -->
                <section v-if="getSection('personal')" class="space-y-2">
                  <div class="flex items-center gap-2">
                    <span
                      class="material-symbols-outlined text-[18px] text-primary dark:text-inverse-primary"
                      >{{ getSection('personal').icon }}</span
                    >
                    <h4
                      class="font-label-md text-label-md text-on-surface dark:text-white font-bold"
                    >
                      {{ getSection('personal').title }}
                    </h4>
                  </div>
                  <div class="grid grid-cols-1 gap-2">
                    <component
                      v-for="field in getSection('personal').fields"
                      :is="field.component"
                      :key="field.key"
                      :field="field"
                      v-model:value="objectData[field.key]"
                      :error="errors[field.key]"
                      :object="objectData"
                    />
                  </div>
                </section>

                <!-- Documents -->
                <section v-if="getSection('documents')" class="space-y-2">
                  <div class="grid grid-cols-1 gap-2">
                    <component
                      v-for="field in getSection('documents').fields"
                      :is="field.component"
                      :key="field.key"
                      :field="field"
                      v-model:value="objectData[field.key]"
                      :error="errors[field.key]"
                      :object="objectData"
                    />
                  </div>
                </section>
              </div>

              <!-- Row 2: Contacts & Logistics side by side -->
              <div class="grid grid-cols-1 lg:grid-cols-2 gap-3 items-start">
                <!-- Contacts -->
                <section v-if="getSection('contacts')" class="space-y-2">
                  <div class="flex items-center gap-2">
                    <span
                      class="material-symbols-outlined text-[18px] text-primary dark:text-inverse-primary"
                      >{{ getSection('contacts').icon }}</span
                    >
                    <h4
                      class="font-label-md text-label-md text-on-surface dark:text-white font-bold"
                    >
                      {{ getSection('contacts').title }}
                    </h4>
                  </div>
                  <div class="grid grid-cols-1 gap-2">
                    <component
                      v-for="field in getSection('contacts').fields"
                      :is="field.component"
                      :key="field.key"
                      :field="field"
                      v-model:value="objectData[field.key]"
                      :error="errors[field.key]"
                      :object="objectData"
                    />
                  </div>
                </section>

                <!-- Logistics -->
                <section v-if="getSection('logistics')" class="space-y-2">
                  <div class="flex items-center gap-2">
                    <span
                      class="material-symbols-outlined text-[18px] text-primary dark:text-inverse-primary"
                      >{{ getSection('logistics').icon }}</span
                    >
                    <h4
                      class="font-label-md text-label-md text-on-surface dark:text-white font-bold"
                    >
                      {{ getSection('logistics').title }}
                    </h4>
                  </div>
                  <div class="grid grid-cols-1 gap-2">
                    <component
                      v-for="field in getSection('logistics').fields"
                      :is="field.component"
                      :key="field.key"
                      :field="field"
                      v-model:value="objectData[field.key]"
                      :error="errors[field.key]"
                      :object="objectData"
                    />
                  </div>
                </section>
              </div>

              <!-- Row 3: Other -->
              <section v-if="getSection('other')" class="space-y-2">
                <div class="flex items-center gap-2">
                  <span class="material-symbols-outlined text-[18px] text-primary dark:text-inverse-primary">{{
                    getSection('other').icon
                  }}</span>
                  <h4
                    class="font-label-md text-label-md text-on-surface dark:text-white font-bold"
                  >
                    {{ getSection('other').title }}
                  </h4>
                </div>
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-2">
                  <component
                    v-for="field in getSection('other').fields"
                    :is="field.component"
                    :key="field.key"
                    :field="field"
                    v-model:value="objectData[field.key]"
                    :error="errors[field.key]"
                    :object="objectData"
                  />
                </div>
              </section>
            </template>

            <!-- Admins and other layout -->
            <template v-else>
              <section v-for="section in sections" :key="section.key" class="space-y-2">
                <div class="flex items-center gap-2">
                  <span class="material-symbols-outlined text-[18px] text-primary dark:text-inverse-primary">{{
                    section.icon
                  }}</span>
                  <h4 class="font-label-md text-label-md text-on-surface dark:text-white font-bold">
                    {{ section.title }}
                  </h4>
                </div>

                <div
                  class="grid grid-cols-1 gap-2 md:grid-cols-2"
                  :class="section.key === 'documents' ? 'md:grid-cols-1' : ''"
                >
                  <component
                    v-for="field in section.fields"
                    :is="field.component"
                    :key="field.key"
                    :field="field"
                    v-model:value="objectData[field.key]"
                    :error="errors[field.key]"
                    :object="objectData"
                  />
                </div>
              </section>
            </template>
          </div>
        </div>
      </aside>
    </div>
  </teleport>

  <!-- Delete Confirmation Modal -->
  <teleport to="body" v-if="showDeleteConfirm">
    <div class="fixed inset-0 z-[100] flex items-center justify-center p-4">
      <!-- Backdrop -->
      <div
        class="absolute inset-0 bg-black/60 backdrop-blur-sm transition-opacity"
        @click="showDeleteConfirm = false"
      ></div>

      <!-- Modal Card -->
      <div
        class="relative bg-surface-container-lowest dark:bg-[#1e2025] border border-outline-variant/30 dark:border-white/10 w-full max-w-md rounded-2xl p-6 shadow-2xl transition-all scale-100 flex flex-col gap-4 animate-in fade-in zoom-in-95 duration-200"
      >
        <div class="flex items-start gap-4">
          <div
            class="flex h-12 w-12 shrink-0 items-center justify-center rounded-full bg-error/10 text-error"
          >
            <span class="material-symbols-outlined text-2xl">warning</span>
          </div>
          <div class="flex-1 min-w-0">
            <h3 class="font-headline-sm text-headline-sm font-bold text-on-surface dark:text-white">
              Подтвердите удаление
            </h3>
            <p class="mt-2 text-body-md text-secondary dark:text-secondary-fixed-dim">
              Вы действительно хотите удалить эту запись (ID: {{ id }})? Это действие нельзя
              отменить.
            </p>
          </div>
        </div>

        <div
          v-if="deleteError"
          class="rounded-xl border border-error/20 bg-error/5 p-3 text-error text-body-sm font-medium"
        >
          {{ deleteError }}
        </div>

        <div class="flex items-center justify-end gap-3 mt-2">
          <button
            type="button"
            class="px-5 py-2.5 rounded-xl font-label-md text-label-md text-secondary dark:text-secondary-fixed-dim hover:bg-surface-container dark:hover:bg-white/5 transition-all"
            @click="showDeleteConfirm = false"
            :disabled="isDeleting"
          >
            Отмена
          </button>
          <button
            type="button"
            class="px-6 py-2.5 bg-error text-white font-bold rounded-xl flex items-center gap-2 hover:brightness-110 active:scale-[0.98] disabled:opacity-50 transition-all shadow-md shadow-error/20"
            @click="deletePost"
            :disabled="isDeleting"
          >
            <span
              v-if="isDeleting"
              class="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"
            ></span>
            <span>{{ isDeleting ? 'Удаление...' : 'Да, удалить' }}</span>
          </button>
        </div>
      </div>
    </div>
  </teleport>
</template>

<style scoped></style>
