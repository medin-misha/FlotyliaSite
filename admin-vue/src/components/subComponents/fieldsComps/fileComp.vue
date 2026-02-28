<script setup>
import { ref, watch } from 'vue'
import APIPosts from '@/api/posts'

const props = defineProps({
  field: Object,
})

const value = defineModel('value', { type: [Number, String, Object] })

if (typeof value.value === 'object') {
  value.value = value.value.file_id
  value['updated'] = value.value.id
}

const serverUrl = import.meta.env.VITE_API_URL
const fileUrl = ref(value.value ? `${serverUrl}/files/${value.value}` : '')
const uploading = ref(false)
const fileInput = ref(null)

watch(value, (v) => {
  fileUrl.value = v ? `${serverUrl}/files/${v}` : ''
})

const patch = (fileId) => {
  console.log('Patch:', fileId)
}

const onFileChange = async (event) => {
  const file = event.target.files[0]
  if (!file) return

  uploading.value = true
  try {
    const res = await APIPosts.createFile(file)
    const fileId = res.data.id

    value.value = fileId
    patch({ [props.field.key]: fileId })

    fileUrl.value = URL.createObjectURL(file)
  } catch (err) {
    console.error('File upload failed', err)
  } finally {
    uploading.value = false
  }
}

const selectFile = () => {
  fileInput.value.click()
}
</script>

<template>
  <div class="details-field">
    <a :href="fileUrl" target="_blank">
      <label class="details-input-label"> {{ field.label }}: {{ value || '' }} </label>
    </a>

    <div class="details-file-wrapper" :class="{ uploading }" @click="selectFile">
      <input ref="fileInput" type="file" class="hidden-input" @change="onFileChange" />

      <img v-if="fileUrl" :src="fileUrl" class="details-file-preview" alt="Preview" />

      <span v-else class="details-file-placeholder">
        {{ uploading ? 'Uploading...' : 'Select file' }}
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
a {
  text-decoration: none;
  color: var(--button-bg);
}
a:hover {
  color: var(--button-hover-bg);
}
</style>
