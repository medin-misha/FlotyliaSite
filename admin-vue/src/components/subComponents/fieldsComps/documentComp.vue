<script setup>
import { onBeforeUnmount, ref, watch } from 'vue'
import APIPosts from '@/api/posts'
import api from '@/api/api'

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

  const openedWindow = window.open('', '_blank', 'noopener,noreferrer')

  try {
    const response = await fetchFileBlob(currentFileId.value)
    const blobUrl = URL.createObjectURL(response.data)

    if (openedWindow) {
      openedWindow.location.href = blobUrl
    } else {
      window.open(blobUrl, '_blank', 'noopener,noreferrer')
    }

    setTimeout(() => URL.revokeObjectURL(blobUrl), 60000)
  } catch (error) {
    if (openedWindow) openedWindow.close()
    console.error('Failed to open file:', error)
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
    <button class="delete-btn" @click="deleteDocument" :disabled="loading">✕</button>
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

.delete-btn {
  background: var(--slidebar-item-hover-bg);
  border: none;
  color: var(--slidebar-item-text-color);
  opacity: 0.3;
  cursor: pointer;
  font-size: 1rem;
  padding: 0.2rem 0.5rem;
  transition:
    opacity 0.2s ease,
    color 0.2s ease;
}
.delete-btn:hover {
  opacity: 1;
  color: #e74c3c;
}
</style>
