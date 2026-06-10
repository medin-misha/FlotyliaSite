<script setup>
import { onBeforeUnmount, ref, watch } from 'vue'
import APIPosts from '@/api/posts'
import api from '@/api/api'
import { useAuthStore } from '@/stores/auth'
import { openBlobInNewTab } from '@/utils/openBlobInNewTab'

const props = defineProps({
  document: Object,
  field: Object,
})

const emit = defineEmits(['updated', 'deleted'])
const fileInput = ref(null)
const description = ref(props.document.description || '')
const loading = ref(false)
const currentFileId = ref(props.document.file_id || null)
const previewUrl = ref(null)
const isImagePreview = ref(false)

const revokePreviewUrl = () => {
  if (previewUrl.value) {
    URL.revokeObjectURL(previewUrl.value)
    previewUrl.value = null
  }
}

const fetchFileBlob = async (fileId) => {
  return await api.get(`/files/${fileId}`, {
    responseType: 'blob',
    timeout: 0,
  })
}

const loadPreview = async (fileId = currentFileId.value) => {
  revokePreviewUrl()
  isImagePreview.value = false

  if (!fileId) return

  try {
    const response = await fetchFileBlob(fileId)
    const mimeType = response.data.type || ''

    if (!mimeType.startsWith('image/')) return

    previewUrl.value = URL.createObjectURL(response.data)
    isImagePreview.value = true
  } catch (error) {
    console.error('Failed to load preview:', error)
  }
}

const openFile = async () => {
  if (loading.value || !currentFileId.value) return

  try {
    await openBlobInNewTab(async () => {
      const response = await fetchFileBlob(currentFileId.value)
      return response.data
    }, description.value || props.field?.label || 'Document')
  } catch (error) {
    console.error('Failed to open file:', error)
  }
}

const downloadFile = () => {
  if (!currentFileId.value) return

  const token = useAuthStore().getToken
  const baseUrl = import.meta.env.VITE_API_URL
  const downloadUrl = `${baseUrl}/files/${currentFileId.value}?token=${token}`
  window.open(downloadUrl, '_blank')
}

const triggerFileInput = () => {
  if (loading.value) return
  fileInput.value?.click()
}

const onFileChange = async (event) => {
  const file = event.target.files[0]
  if (!file) return

  loading.value = true
  try {
    const createFile = await APIPosts.createFile(file)
    const fileId = createFile.data.id

    const newDoc = {
      ...props.document,
      file_id: fileId,
      description: description.value,
    }

    currentFileId.value = fileId
    await loadPreview(fileId)
    emit('updated', newDoc)
  } catch (error) {
    console.error('Failed to upload file:', error)
  } finally {
    loading.value = false
  }
}

const updateDescription = (event) => {
  const newDoc = {
    ...props.document,
    description: event.target.value,
  }
  emit('updated', newDoc)
}

const deleteDocument = () => {
  const confirmed = window.confirm('Удалить этот документ?')
  if (!confirmed) return
  emit('deleted')
}

watch(
  () => props.document.file_id,
  async (newFileId) => {
    currentFileId.value = newFileId || null
    await loadPreview(newFileId)
  },
  { immediate: true },
)

watch(
  () => props.document.description,
  (newDescription) => {
    description.value = newDescription || ''
  },
)

onBeforeUnmount(() => {
  revokePreviewUrl()
})
</script>

<template>
  <div 
    :class="[
      'group relative aspect-[3/4] rounded-2xl overflow-hidden border border-outline-variant/30 dark:border-white/10 shadow-sm hover:shadow-md transition-all duration-300 flex flex-col justify-end bg-surface-container-low dark:bg-white/5',
      loading ? 'opacity-60 pointer-events-none' : ''
    ]"
  >
    <!-- File Input Hidden -->
    <input
      ref="fileInput"
      type="file"
      class="hidden"
      @change="onFileChange"
      :disabled="loading"
    />

    <!-- Image Preview or Placeholder Background -->
    <div class="absolute inset-0 w-full h-full flex items-center justify-center overflow-hidden">
      <img
        v-if="isImagePreview && previewUrl"
        :src="previewUrl"
        class="w-full h-full object-cover grayscale group-hover:grayscale-0 transition-all duration-500"
        alt="Document Preview"
      />
      <div v-else class="flex flex-col items-center gap-2 text-secondary/40 dark:text-white/20 p-4 text-center">
        <span class="material-symbols-outlined text-[48px]" style="font-variation-settings: 'FILL' 1;">description</span>
        <span class="text-xs font-semibold select-none">{{ currentFileId ? 'Документ загружен' : 'Нет файла' }}</span>
      </div>
    </div>

    <!-- Details Overlay -->
    <div class="absolute inset-0 bg-gradient-to-t from-black/80 via-black/20 to-transparent flex flex-col justify-end p-4 z-10">
      <!-- Document Label / Description -->
      <div class="space-y-1 mb-2">
        <p class="text-white font-label-md text-label-md font-bold truncate">
          {{ description || field?.label || 'Документ' }}
        </p>
        <input 
          v-if="!currentFileId"
          type="text" 
          :value="description"
          @input="updateDescription"
          placeholder="Название..."
          class="w-full h-8 px-2 rounded-lg bg-white/10 backdrop-blur-sm border-none text-white text-xs placeholder-white/50 focus:ring-1 focus:ring-primary focus:outline-none"
        />
      </div>

      <!-- Action buttons -->
      <div class="flex gap-2">
        <!-- Main dynamic file action -->
        <button
          v-if="currentFileId"
          type="button"
          @click="openFile"
          class="flex-grow py-2 bg-white/20 hover:bg-white/30 backdrop-blur-md text-white rounded-xl flex items-center justify-center gap-1.5 text-xs font-bold transition-all active:scale-[0.98]"
        >
          <span class="material-symbols-outlined text-sm">open_in_new</span>
          Открыть
        </button>
        <button
          v-else
          type="button"
          @click="triggerFileInput"
          class="flex-grow py-2 bg-primary text-white rounded-xl flex items-center justify-center gap-1.5 text-xs font-bold hover:brightness-110 transition-all active:scale-[0.98]"
        >
          <span class="material-symbols-outlined text-sm">upload</span>
          Загрузить
        </button>

        <!-- Downloader -->
        <button
          v-if="currentFileId"
          type="button"
          @click="downloadFile"
          class="p-2 bg-white/15 hover:bg-white/25 backdrop-blur-md text-white rounded-xl flex items-center justify-center transition-all active:scale-[0.98]"
          title="Скачать"
        >
          <span class="material-symbols-outlined text-sm">download</span>
        </button>

        <!-- Delete button -->
        <button
          type="button"
          @click="deleteDocument"
          class="p-2 bg-red-600/20 hover:bg-red-650 backdrop-blur-md text-red-400 hover:text-white rounded-xl flex items-center justify-center transition-all active:scale-[0.98]"
          title="Удалить"
        >
          <span class="material-symbols-outlined text-sm">delete</span>
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
</style>
