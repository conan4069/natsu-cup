<template>
  <v-form ref="formRef" v-model="valid">
    <!-- Nombre del jugador -->
    <v-text-field
      v-model="form.display_name"
      label="Nombre del jugador"
      placeholder="Ej: Eliezer Hijo Mio"
      variant="outlined"
      :rules="nameRules"
      required
      prepend-inner-icon="mdi-account"
      class="mb-4"
      :readonly="readonly || mode === 'view'"
    />

    <!-- Avatar actual (solo en modo edición) -->
  
    <!-- Subida de avatar -->
    <div
      v-if="!readonly && mode !== 'view'"
      class="mb-6 dropzone"
      @dragover.prevent
      @drop.prevent="onDrop"
      @click="triggerFileInput"
    >
      <div class="dropzone-content">
        <v-icon size="40" color="grey">mdi-cloud-upload</v-icon>
        <span>Arrastra y suelta la imagen aquí</span>
        <input
          type="file"
          accept="image/*"
          style="display: none"
          @change="onFileChange"
          ref="fileInput"
        />
      </div>
    </div>

    <div v-if="avatarPreview" class="mb-4" style="display: flex; flex-direction: column; align-items: center;">
      <p class="text-body-2 text-grey-darken-1 mb-2" style="text-align: center;">Avatar actual</p>
      <v-avatar size="80">
        <v-img :src="avatarPreview" alt="Preview del avatar" />
      </v-avatar>
    </div>

    <div v-if="mode === 'edit' && player?.avatar" class="mb-4 avatar-centrado">
      <p class="text-body-2 text-grey-darken-1 mb-2">Avatar actual:</p>
      <v-avatar class="mb-3" size="80">
        <v-img alt="Avatar actual" :src="player.avatar" />
      </v-avatar>
    </div>
    
    <!-- Información adicional -->
  </v-form>
</template>

<script setup>
import { ref, watch, computed, onMounted } from 'vue'

// Props
const props = defineProps({
  player: {
    type: Object,
    default: null
  },
  mode: {
    type: String,
    default: 'create', // 'create' | 'edit' | 'view'
    validator: value => ['create', 'edit', 'view'].includes(value)
  },
  readonly: {
    type: Boolean,
    default: false
  }
})

// Emits
const emit = defineEmits(['update:form', 'submit', 'valid-change'])

// Referencias
const formRef = ref(null)
const valid = ref(false)
const avatarPreview = ref(null)
const fileInput = ref(null)

// Formulario reactivo
const form = ref({
  display_name: '',
  avatar: null,
  nickname: ''
})

// Reglas de validación
const nameRules = [
  v => !!v || 'El nombre es requerido',
  v => v.length >= 2 || 'El nombre debe tener al menos 2 caracteres',
  v => v.length <= 100 || 'El nombre no puede exceder 100 caracteres'
]

const avatarRules = [
  v => !v || v.size <= 5 * 1024 * 1024 || 'El archivo no puede exceder 5MB'
]

// Computed para determinar si el formulario está en modo solo lectura
const isReadOnly = computed(() => props.mode === 'view')

// Preview del avatar
watch(() => form.value.avatar, file => {
  if (file && file instanceof File) {
    const reader = new FileReader()
    reader.addEventListener('load', e => {
      avatarPreview.value = e.target.result
    })
    reader.readAsDataURL(file)
  } else {
    avatarPreview.value = null
  }
})

// Emitir cambios del formulario
watch(form, (newForm) => {
  emit('update:form', newForm)
}, { deep: true })

// Emitir cambios de validación
watch(valid, (newValid) => {
  emit('valid-change', newValid)
})

// Cargar datos del jugador si está en modo edición
onMounted(() => {
  if (props.player && props.mode === 'edit') {
    form.value = {
      display_name: props.player.display_name || '',
      avatar: null,
      nickname: props.player.nickname || ''
    }
  }
})

// Métodos expuestos
const validate = () => {
  return formRef.value?.validate()
}

const reset = () => {
  formRef.value?.reset()
  form.value = {
    display_name: '',
    avatar: null,
    nickname: ''
  }
  avatarPreview.value = null
}

const getFormData = () => {
  const formData = new FormData()
  formData.append('display_name', form.value.display_name)

  if (form.value.avatar) {
    formData.append('avatar', form.value.avatar)
  }

  if (form.value.nickname) {
    formData.append('nickname', form.value.nickname)
  }

  return formData
}

const triggerFileInput = () => {
  fileInput.value && fileInput.value.click()
}

const onFileChange = (event) => {
  const file = event.target.files[0]
  if (file) {
    form.value.avatar = file
    const reader = new FileReader()
    reader.onload = (e) => {
      avatarPreview.value = e.target.result
    }
    reader.readAsDataURL(file)
  }
}

const onDrop = (event) => {
  const file = event.dataTransfer.files[0]
  if (file) {
    form.value.avatar = file
    const reader = new FileReader()
    reader.onload = (e) => {
      avatarPreview.value = e.target.result
    }
    reader.readAsDataURL(file)
  }
}

// Exponer métodos
defineExpose({
  validate,
  reset,
  getFormData,
  form: form.value,
  valid
})
</script>

<style scoped>
/* Estilos específicos si son necesarios */
.dropzone {
  border: 2px dashed #ccc;
  border-radius: 8px;
  padding: 32px;
  text-align: center;
  cursor: pointer;
  background: #fafafa;
  transition: border-color 0.2s;
}
.dropzone:hover {
  border-color: #1976d2;
}
.dropzone-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}
.avatar-centrado {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}
</style>
