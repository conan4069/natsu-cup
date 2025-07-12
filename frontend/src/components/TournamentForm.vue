<template>
  <v-form ref="formRef" v-model="valid">
    <!-- Nombre del torneo -->
    <v-text-field
      v-model="form.name"
      class="mb-4"
      color="primary"
      label="Nombre del torneo"
      placeholder="Ej: Natsu Cup 2024"
      prepend-inner-icon="mdi-trophy"
      :readonly="readonly || mode === 'view'"
      required
      rounded="xl"
      :rules="nameRules"
      variant="outlined"
    />

    <!-- Formato del torneo -->
    <v-select
      v-model="form.format"
      class="mb-4"
      color="primary"
      :items="formatOptions"
      label="Formato"
      prepend-inner-icon="mdi-account-group"
      :readonly="readonly || mode === 'view'"
      required
      rounded="xl"
      :rules="formatRules"
      variant="outlined"
    />

    <!-- Número total de equipos -->
    <v-text-field
      v-model.number="form.total_teams"
      class="mb-4"
      color="primary"
      label="Número total de equipos"
      prepend-inner-icon="mdi-numeric"
      :readonly="readonly || mode === 'view'"
      required
      rounded="xl"
      :rules="totalTeamsRules"
      type="number"
      variant="outlined"
    />

    <!-- Equipos por grupo -->
    <v-text-field
      v-model.number="form.teams_per_group"
      class="mb-4"
      color="primary"
      label="Equipos por grupo"
      prepend-inner-icon="mdi-group"
      :readonly="readonly || mode === 'view'"
      required
      rounded="xl"
      :rules="teamsPerGroupRules"
      type="number"
      variant="outlined"
    />

    <!-- Configuración de fases -->
    <v-row class="mb-4">
      <v-col cols="12" md="6">
        <v-switch
          v-model="form.has_group_stage"
          color="primary"
          label="Fase de grupos"
          :readonly="readonly || mode === 'view'"
        />
      </v-col>
      <v-col cols="12" md="6">
        <v-switch
          v-model="form.has_knockout"
          color="primary"
          label="Fase eliminatoria"
          :readonly="readonly || mode === 'view'"
        />
      </v-col>
    </v-row>

    <!-- Reglas del torneo -->
    <v-textarea
      v-model="form.rules"
      class="mb-4"
      color="primary"
      label="Reglas del torneo"
      placeholder="Describe las reglas específicas del torneo..."
      prepend-inner-icon="mdi-file-document"
      :readonly="readonly || mode === 'view'"
      rounded="xl"
      rows="4"
      variant="outlined"
    />
  </v-form>
</template>

<script setup>
  import { computed, onMounted, ref, watch } from 'vue'

  // Props
  const props = defineProps({
    tournament: {
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

  // Formulario reactivo
  const form = ref({
    name: '',
    format: '1v1',
    total_teams: 8,
    teams_per_group: 4,
    has_group_stage: false,
    has_knockout: true,
    rules: '',
  })

  // Opciones de formato
  const formatOptions = [
    { title: '1 vs 1', value: '1v1' },
    { title: '2 vs 2', value: '2v2' },
  ]

  // Reglas de validación
  const nameRules = [
    v => !!v || 'El nombre es requerido',
    v => v.length >= 3 || 'El nombre debe tener al menos 3 caracteres',
    v => v.length <= 100 || 'El nombre no puede exceder 100 caracteres',
  ]

  const formatRules = [
    v => !!v || 'El formato es requerido',
  ]

  const totalTeamsRules = [
    v => !!v || 'El número de equipos es requerido',
    v => v >= 2 || 'Debe haber al menos 2 equipos',
    v => v <= 64 || 'No puede haber más de 64 equipos',
  ]

  const teamsPerGroupRules = [
    v => !!v || 'El número de equipos por grupo es requerido',
    v => v >= 2 || 'Debe haber al menos 2 equipos por grupo',
    v => v <= 8 || 'No puede haber más de 8 equipos por grupo',
  ]

  // Computed para determinar si el formulario está en modo solo lectura
  const isReadOnly = computed(() => props.mode === 'view')

  // Emitir cambios del formulario
  watch(form, newForm => {
    emit('update:form', newForm)
  }, { deep: true })

  // Emitir cambios de validación
  watch(valid, newValid => {
    emit('valid-change', newValid)
  })

  // Cargar datos del torneo si está en modo edición
  onMounted(() => {
    if (props.tournament && props.mode === 'edit') {
      form.value = {
        name: props.tournament.name || '',
        format: props.tournament.format || '1v1',
        total_teams: props.tournament.total_teams || 8,
        teams_per_group: props.tournament.teams_per_group || 4,
        has_group_stage: props.tournament.has_group_stage || false,
        has_knockout: props.tournament.has_knockout === undefined ? true : props.tournament.has_knockout,
        rules: props.tournament.rules || '',
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
      format: '1v1',
      total_teams: 8,
      teams_per_group: 4,
      has_group_stage: false,
      has_knockout: true,
      rules: '',
    }
  }

  const getFormData = () => {
    return {
      name: form.value.name,
      format: form.value.format,
      total_teams: form.value.total_teams,
      teams_per_group: form.value.teams_per_group,
      has_group_stage: form.value.has_group_stage,
      has_knockout: form.value.has_knockout,
      rules: form.value.rules,
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
/* Estilos específicos si son necesarios */
</style>
