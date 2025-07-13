<template>
  <v-form ref="formRef" v-model="valid">
    <!-- Nombre del equipo -->
    <v-text-field
      v-model="form.name"
      class="mb-4"
      color="primary"
      label="Nombre del equipo"
      placeholder="Ej: Real Madrid"
      prepend-inner-icon="mdi-shield"
      :readonly="readonly || mode === 'view'"
      required
      rounded="xl"
      :rules="nameRules"
      variant="outlined"
    />

    <!-- Subida de logo -->
    <div
      v-if="!readonly && mode !== 'view'"
      class="mb-6 dropzone"
      @click="triggerFileInput"
      @dragover.prevent
      @drop.prevent="onDrop"
    >
      <div class="dropzone-content">
        <v-icon color="grey" size="40">mdi-cloud-upload</v-icon>
        <span>Arrastra y suelta el logo aquí</span>
        <input
          ref="fileInput"
          accept="image/*"
          style="display: none"
          type="file"
          @change="onFileChange"
        >
      </div>
    </div>

    <div v-if="logoPreview" class="mb-4" style="display: flex; flex-direction: column; align-items: center;">
      <p class="text-body-2 text-grey-darken-1 mb-2" style="text-align: center;">Logo actual</p>
      <v-avatar size="140">
        <v-img alt="Preview del logo" :src="logoPreview" />
      </v-avatar>
    </div>

    <div v-if="mode === 'edit' && team?.logo" class="mb-4 avatar-centrado">
      <p class="text-body-2 text-grey-darken-1 mb-2">Logo actual:</p>
      <v-avatar class="mb-3" size="80">
        <v-img alt="Logo actual" :src="team.logo" />
      </v-avatar>
    </div>
  </v-form>
</template>

<script setup>
  import { computed, onMounted, ref, watch } from 'vue'

  // Props
  const props = defineProps({
    team: {
      type: Object,
      default: null,
    },
    mode: {
      type: String,
      default: 'create', // 'create' | 'edit' | 'view'
      validator: value => ['create', 'edit', 'view'].includes(value),
    },
    readonly: {
      type: Boolean,
      default: false,
    },
  })

  // Emits
  const emit = defineEmits(['update:form', 'submit', 'valid-change'])

  // Referencias
  const formRef = ref(null)
  const valid = ref(false)
  const logoPreview = ref(null)
  const fileInput = ref(null)

  // Formulario reactivo
  const form = ref({
    name: '',
    logo: null,
  })

  // Reglas de validación
  const nameRules = [
    v => !!v || 'El nombre es requerido',
    v => v.length >= 2 || 'El nombre debe tener al menos 2 caracteres',
    v => v.length <= 100 || 'El nombre no puede exceder 100 caracteres',
  ]

  // Computed para determinar si el formulario está en modo solo lectura
  const isReadOnly = computed(() => props.mode === 'view')

  // Preview del logo
  watch(() => form.value.logo, file => {
    if (file && file instanceof File) {
      const reader = new FileReader()
      reader.addEventListener('load', e => {
        logoPreview.value = e.target.result
      })
      reader.readAsDataURL(file)
    } else {
      logoPreview.value = null
    }
  })

  // Emitir cambios del formulario
  watch(form, newForm => {
    emit('update:form', newForm)
  }, { deep: true })

  // Emitir cambios de validación
  watch(valid, newValid => {
    emit('valid-change', newValid)
  })

  // Cargar datos del equipo si está en modo edición o vista
  onMounted(() => {
    if (props.team && (props.mode === 'edit' || props.mode === 'view')) {
      form.value = {
        name: props.team.name || '',
        logo: null,
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
      name: '',
      logo: null,
    }
    logoPreview.value = null
  }

  const getFormData = () => {
    const formData = new FormData()
    formData.append('name', form.value.name)
    if (form.value.logo) {
      formData.append('logo', form.value.logo)
    }
    return formData
  }

  const triggerFileInput = () => {
    fileInput.value && fileInput.value.click()
  }

  const onFileChange = event => {
    const file = event.target.files[0]
    if (file) {
      form.value.logo = file
      const reader = new FileReader()
      reader.addEventListener('load', e => {
        logoPreview.value = e.target.result
      })
      reader.readAsDataURL(file)
    }
  }

  const onDrop = event => {
    const file = event.dataTransfer.files[0]
    if (file) {
      form.value.logo = file
      const reader = new FileReader()
      reader.addEventListener('load', e => {
        logoPreview.value = e.target.result
      })
      reader.readAsDataURL(file)
    }
  }

  // Exponer métodos
  defineExpose({
    validate,
    reset,
    getFormData,
    form: form.value,
    valid,
  })
</script>

<style scoped>
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
