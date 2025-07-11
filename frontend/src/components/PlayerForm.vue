<template>
  <v-form ref="formRef" v-model="valid">
    <!-- Nombre del jugador -->
    <v-text-field
      v-model="form.display_name"
      label="Nombre del jugador"
      placeholder="Ej: Lionel Messi"
      variant="outlined"
      :rules="nameRules"
      required
      prepend-inner-icon="mdi-account"
      class="mb-4"
      :readonly="readonly || mode === 'view'"
    />

    <!-- Avatar actual (solo en modo edición) -->
    <div v-if="mode === 'edit' && player?.avatar" class="mb-4">
      <p class="text-body-2 text-grey-darken-1 mb-2">Avatar actual:</p>
      <v-avatar class="mb-3" size="80">
        <v-img alt="Avatar actual" :src="player.avatar" />
      </v-avatar>
    </div>

    <!-- Subida de avatar -->
    <v-file-input
      v-if="!readonly && mode !== 'view'"
      v-model="form.avatar"
      :label="mode === 'edit' ? 'Cambiar avatar (opcional)' : 'Avatar (opcional)'"
      accept="image/*"
      variant="outlined"
      prepend-inner-icon="mdi-image"
      class="mb-6"
      :rules="avatarRules"
      show-size
      counter
    >
      <template #prepend>
        <v-avatar v-if="avatarPreview" class="mr-3" size="40">
          <v-img alt="Preview del avatar" :src="avatarPreview" />
        </v-avatar>
      </template>
    </v-file-input>

    <!-- Información adicional -->
    <v-expansion-panels class="mb-6" variant="accordion">
      <v-expansion-panel>
        <v-expansion-panel-title>
          <v-icon start>mdi-information</v-icon>
          Información adicional
        </v-expansion-panel-title>
        <v-expansion-panel-text>
          <p class="text-body-2 text-grey-darken-1 mb-4">
            Esta información será visible en el perfil del jugador y en los torneos.
          </p>

          <v-text-field
            v-model="form.nickname"
            class="mb-4"
            label="Apodo (opcional)"
            placeholder="Ej: La Pulga"
            prepend-inner-icon="mdi-tag"
            variant="outlined"
            :readonly="readonly || mode === 'view'"
          />
        </v-expansion-panel-text>
      </v-expansion-panel>
    </v-expansion-panels>
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
</style>
