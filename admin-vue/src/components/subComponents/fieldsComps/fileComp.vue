<script setup>
import { onBeforeUnmount, ref, watch } from 'vue'
import APIPosts from '@/api/posts'
import api from '@/api/api'
import { openBlobInNewTab } from '@/utils/openBlobInNewTab'

const props = defineProps({
  field: Object,
})

const value = defineModel('value', { type: [Number, String, Object] })

if (typeof value.value === 'object' && value.value !== null) {
  value.value = value.value.file_id
}

const fileInput = ref(null)
const uploading = ref(false)
const previewUrl = ref(null)
const isImagePreview = ref(false)

const revokePreviewUrl = () => {
  if (previewUrl.value) {
    URL.revokeObjectURL(previewUrl.value)
    previewUrl.value = null
  }
}

const fetchFileBlob = async (fileId) => {
  return await api.get(`/files/${fileId}`, { responseType: 'blob', timeout: 0 })
}

const loadPreview = async (fileId) => {
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
  if (uploading.value || !value.value) return

  try {
    await openBlobInNewTab(async () => {
      return (await fetchFileBlob(value.value)).data
    }, props.field?.label || 'File')
  } catch (error) {
    console.error('Failed to open file:', error)
  }
}

const selectFile = () => {
  if (uploading.value) return
  fileInput.value?.click()
}

const onFileChange = async (event) => {
  const file = event.target.files[0]
  if (!file) return

  uploading.value = true
  try {
    const res = await APIPosts.createFile(file)
    const fileId = res.data.id

    value.value = fileId
    await loadPreview(fileId)
  } catch (err) {
    console.error('File upload failed', err)
  } finally {
    uploading.value = false
  }
}

watch(
  () => value.value,
  async (newFileId) => {
    await loadPreview(newFileId)
  },
  { immediate: true },
)

onBeforeUnmount(() => {
  revokePreviewUrl()
})
</script>

<template>
  <div class="details-field">
    <button type="button" class="file-link-button" @click="openFile" :disabled="!value">
      <label class="details-input-label"> {{ props.field.label }}: {{ value || '' }} </label>
    </button>

    <div class="details-file-wrapper" :class="{ uploading }" @click="selectFile">
      <input ref="fileInput" type="file" class="hidden-input" @change="onFileChange" :disabled="uploading" />

      <img
        v-if="isImagePreview && previewUrl"
        :src="previewUrl"
        class="details-file-preview"
        alt="Preview"
      />
      <span v-else-if="value" class="details-file-placeholder">Открыть файл</span>
      <span v-else class="details-file-placeholder">
        {{ uploading ? 'Загрузка...' : 'Выбрать файл' }}
      </span>
    </div>
  </div>
</template>

<style scoped>
.details-field {
  width: 100%;
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

.details-file-preview {
  max-width: 100%;
  max-height: 80px;
  object-fit: contain;
}

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
</style>
