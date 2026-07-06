import { ref, reactive } from 'vue'

/**
 * Encapsulates drag-and-drop file upload logic for the three document zones
 * (op, passport, residence).
 *
 * @param {Function} onZoneChange - Called with the zone name after files are
 *   added or removed. Typically syncFieldValidity from useFormValidation.
 */
export function useFileUpload(onZoneChange) {
  // File lists per zone
  const filesOP = ref([])
  const filesPassport = ref([])
  const filesResidence = ref([])

  // Drag state per zone
  const dragging = reactive({ op: false, passport: false, residence: false })

  // Hidden <input type="file"> refs per zone
  const inputOP = ref(null)
  const inputPassport = ref(null)
  const inputResidence = ref(null)

  function addFiles(zone, newFiles) {
    if (zone === 'op') filesOP.value.push(...newFiles)
    else if (zone === 'passport') filesPassport.value.push(...newFiles)
    else if (zone === 'residence') filesResidence.value.push(...newFiles)
    onZoneChange?.(zone)
  }

  function onDrop(zone, event) {
    dragging[zone] = false
    addFiles(zone, Array.from(event.dataTransfer.files))
  }

  function onFileInput(zone, event) {
    addFiles(zone, Array.from(event.target.files))
    event.target.value = ''
  }

  function removeFile(zone, index) {
    if (zone === 'op') filesOP.value.splice(index, 1)
    else if (zone === 'passport') filesPassport.value.splice(index, 1)
    else if (zone === 'residence') filesResidence.value.splice(index, 1)
    onZoneChange?.(zone)
  }

  function triggerInput(zone) {
    if (zone === 'op') inputOP.value?.click()
    else if (zone === 'passport') inputPassport.value?.click()
    else if (zone === 'residence') inputResidence.value?.click()
  }

  function clearAllFiles() {
    filesOP.value = []
    filesPassport.value = []
    filesResidence.value = []
  }

  return {
    filesOP, filesPassport, filesResidence,
    inputOP, inputPassport, inputResidence,
    dragging,
    onDrop, onFileInput, removeFile, triggerInput,
    clearAllFiles,
  }
}
