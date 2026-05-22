<script setup>
import { onBeforeUnmount, ref, watch } from 'vue'
import APIPosts from '@/api/posts'
import api from '@/api/api'
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
    }, description.value || field?.label || 'Document')
  } catch (error) {
    console.error('Failed to open file:', error)
  }
}

const downloadFile = async () => {
  if (loading.value || !currentFileId.value) return

  loading.value = true
  try {
    const response = await fetchFileBlob(currentFileId.value)
    const fileUrl = URL.createObjectURL(response.data)
    const link = document.createElement('a')

    link.href = fileUrl
    link.download = description.value || `document-${props.document.id || currentFileId.value}`
    document.body.appendChild(link)
    link.click()
    link.remove()
    URL.revokeObjectURL(fileUrl)
  } catch (error) {
    console.error('Failed to download file:', error)
  } finally {
    loading.value = false
  }
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
    console.log('Selected file:', file.name)
    const createFile = await APIPosts.createFile(file)
    const fileId = createFile.data.id

    let newDoc
    if (props.document.id) {
      // Обновляем существующий документ вместо удаления и создания
      const updateRes = await APIPosts.updatePost('/documents', props.document.id, {
        file_id: fileId,
        description: description.value,
      })
      newDoc = updateRes.data
    } else {
      // Создаем новый, если ID нет (хотя в этом компоненте он обычно есть)
      const uploadRes = await APIPosts.createPost('/documents', {
        file_id: fileId,
        description: description.value,
        user_id: props.document.user_id,
      })
      newDoc = uploadRes.data
    }

    currentFileId.value = newDoc.file_id
    await loadPreview(newDoc.file_id)
    emit('updated', newDoc)
  } catch (error) {
    console.error('Failed to upload file:', error)
  } finally {
    loading.value = false
  }
}

const deleteDocument = async () => {
  if (loading.value) return

  const confirmed = window.confirm('Удалить этот документ?')
  if (!confirmed) return

  if (props.document.id) {
    loading.value = true
    try {
      await APIPosts.deletePost('/documents', props.document.id)
      emit('deleted')
    } catch (error) {
      console.error('Failed to delete document:', error)
    } finally {
      loading.value = false
    }
  } else {
    emit('deleted')
  }
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
  <section :class="{ 'component-loading': loading }">
    <button type="button" class="file-link-button" @click="openFile" :disabled="!currentFileId">
      <label class="details-input-label"> {{ field.label }} </label>
    </button>
    <input
      type="text"
      v-model="description"
      class="description-input"
      placeholder="description"
      :disabled="loading"
    />
    <div class="document-actions">
      <button
        type="button"
        class="action-btn download-btn"
        aria-label="Скачать документ"
        title="Скачать документ"
        @click="downloadFile"
        :disabled="loading || !currentFileId"
      >
        ↓
      </button>
      <button
        type="button"
        class="action-btn delete-btn"
        aria-label="Удалить документ"
        title="Удалить документ"
        @click="deleteDocument"
        :disabled="loading"
      >
        ✕
      </button>
    </div>
    <div class="details-file-wrapper" @click="triggerFileInput" :class="{ uploading: loading }">
      <input
        ref="fileInput"
        type="file"
        class="hidden-input"
        @change="onFileChange"
        :disabled="loading"
      />

      <img
        v-if="isImagePreview && previewUrl"
        :src="previewUrl"
        class="details-file-preview"
        alt="Preview"
      />
      <span v-else-if="currentFileId" class="details-file-placeholder">Открыть файл</span>
      <span v-else class="details-file-placeholder">{{
        loading ? 'Загрузка...' : 'Выбрать файл'
      }}</span>
    </div>
  </section>
</template>

<style scoped>
section {
  width: 100vh;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid var(--slidebar-item-hover-bg);
  margin-bottom: 1rem;
  padding-bottom: 0.3rem;
}

.details-input-label {
  font-weight: bold;
}

.component-loading {
  opacity: 0.6;
  pointer-events: none;
}

.description-input {
  width: 30%;
}

/* Область выбора файла — как input справа */
.details-file-wrapper {
  width: 30%;
  min-height: 48px;
  border-radius: 0.5rem;
  border: 1px dashed var(--slidebar-item-hover-bg);
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  transition: 0.2s ease;
  overflow: hidden;
  position: relative;
}

.details-file-wrapper:hover {
  border-color: var(--button-bg);
}

.details-file-wrapper.uploading {
  opacity: 0.6;
  pointer-events: none;
}

/* Превью */
.details-file-preview {
  max-width: 100%;
  max-height: 80px;
  object-fit: contain;
}

/* Заглушка */
.details-file-placeholder {
  font-size: 0.9rem;
  font-weight: bold;
  color: var(--slidebar-item-text-color);
  opacity: 0.7;
}

.hidden-input {
  display: none;
}

.file-link-button {
  background: transparent;
  border: none;
  padding: 0;
  color: var(--button-bg);
  cursor: pointer;
}

.file-link-button:hover {
  color: var(--button-hover-bg);
}

.file-link-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.document-actions {
  display: flex;
  align-items: center;
  gap: 0.35rem;
}

.action-btn {
  background: var(--slidebar-item-hover-bg);
  border: none;
  color: var(--slidebar-item-text-color);
  opacity: 0.3;
  cursor: pointer;
  width: 1.4rem;
  height: 1.4rem;
  padding: 0;
  border-radius: 0.25rem;
  font-size: 0.75rem;
  line-height: 1;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  transition:
    opacity 0.2s ease,
    color 0.2s ease;
}

.action-btn:hover:not(:disabled) {
  opacity: 1;
}

.action-btn:disabled {
  cursor: not-allowed;
}

.download-btn:hover:not(:disabled) {
  color: var(--button-bg);
}

.download-btn {
  width: 2.6rem;
  height: 1.8rem;
  font-size: 1rem;
}

.delete-btn:hover {
  opacity: 1;
  color: #e74c3c;
}
</style>
