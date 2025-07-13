<template>
  <v-form ref="formRef" v-model="valid">
    <v-row>
      <v-col cols="12" md="6">
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
      </v-col>

      <v-col cols="12" md="6">
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
      </v-col>

      <v-col cols="12" md="6">
        <v-select
          v-model="form.competition_type"
          class="mb-4"
          color="primary"
          item-title="text"
          item-value="value"
          :items="competitionTypes"
          label="Tipo de Competición"
          prepend-inner-icon="mdi-flag"
          :readonly="readonly || mode === 'view'"
          required
          rounded="xl"
          :rules="competitionTypeRules"
          variant="outlined"
          @update:model-value="onCompetitionTypeChange"
        />
      </v-col>

      <v-col cols="12" md="6">
        <v-text-field
          v-model.number="form.total_teams"
          class="mb-4"
          color="primary"
          label="Número de equipos"
          placeholder="Ej: 8, 16, 32"
          prepend-inner-icon="mdi-numeric"
          :readonly="readonly || mode === 'view'"
          required
          rounded="xl"
          :rules="totalTeamsRules"
          type="number"
          variant="outlined"
        />
      </v-col>

      <!-- Campos específicos para liga -->
      <v-col v-if="showLeagueFields" cols="12" md="6">
        <v-text-field
          v-model.number="form.league_rounds"
          class="mb-4"
          color="primary"
          label="Número de vueltas"
          placeholder="Ej: 1, 2"
          prepend-inner-icon="mdi-repeat"
          :readonly="readonly || mode === 'view'"
          rounded="xl"
          :rules="leagueRoundsRules"
          type="number"
          variant="outlined"
        />
      </v-col>

      <v-col v-if="showLeagueFields" cols="12" md="6">
        <v-text-field
          v-model.number="form.playoff_teams"
          class="mb-4"
          color="primary"
          label="Equipos para playoffs"
          placeholder="Ej: 4, 8"
          prepend-inner-icon="mdi-trophy"
          :readonly="readonly || mode === 'view'"
          rounded="xl"
          :rules="playoffTeamsRules"
          type="number"
          variant="outlined"
        />
      </v-col>

      <!-- Campos específicos para grupos -->
      <v-col v-if="showGroupFields" cols="12" md="6">
        <v-text-field
          v-model.number="form.teams_per_group"
          class="mb-4"
          color="primary"
          label="Equipos por grupo"
          placeholder="Ej: 4"
          prepend-inner-icon="mdi-group"
          :readonly="readonly || mode === 'view'"
          rounded="xl"
          :rules="teamsPerGroupRules"
          type="number"
          variant="outlined"
        />
      </v-col>

      <v-col cols="12">
        <v-textarea
          v-model="form.rules"
          class="mb-4"
          color="primary"
          label="Reglas del torneo (opcional)"
          placeholder="Describe las reglas específicas del torneo..."
          prepend-inner-icon="mdi-file-document"
          :readonly="mode === 'view'"
          rounded="xl"
          rows="4"
          variant="outlined"
        />
      </v-col>
    </v-row>
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
    competition_type: 'cup',
    total_teams: 8,
    has_group_stage: false,
    has_knockout: true,
    teams_per_group: 4,
    league_rounds: 1,
    playoff_teams: 4,
    rules: '',
  })

  // Opciones de formato
  const formatOptions = [
    { title: '1 vs 1', value: '1v1' },
    { title: '2 vs 2', value: '2v2' },
  ]

  const competitionTypes = [
    { text: 'Copa (Eliminatoria directa)', value: 'cup' },
    { text: 'Liga (Todos contra todos)', value: 'league' },
    { text: 'Liga + Playoffs', value: 'hybrid' },
    { text: 'Fase de grupos + Eliminatoria', value: 'groups' },
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

  const competitionTypeRules = [
    v => !!v || 'El tipo de competición es requerido',
  ]

  const totalTeamsRules = [
    v => !!v || 'El número de equipos es requerido',
    v => v >= 2 || 'Debe haber al menos 2 equipos',
    v => v <= 64 || 'No puede haber más de 64 equipos',
    v => Number.isInteger(v) || 'Debe ser un número entero',
  ]

  const leagueRoundsRules = [
    v => !showLeagueFields.value || !!v || 'Número de vueltas es requerido para liga',
    v => !showLeagueFields.value || v >= 1 || 'Debe haber al menos 1 vuelta',
    v => !showLeagueFields.value || v <= 3 || 'No puede haber más de 3 vueltas',
    v => !showLeagueFields.value || Number.isInteger(v) || 'Debe ser un número entero',
  ]

  const playoffTeamsRules = [
    v => !showLeagueFields.value || !!v || 'Equipos para playoffs es requerido',
    v => !showLeagueFields.value || v >= 2 || 'Debe haber al menos 2 equipos para playoffs',
    v => !showLeagueFields.value || v <= 8 || 'No puede haber más de 8 equipos para playoffs',
    v => !showLeagueFields.value || Number.isInteger(v) || 'Debe ser un número entero',
  ]

  const teamsPerGroupRules = [
    v => !showGroupFields.value || !!v || 'Equipos por grupo es requerido cuando hay fase de grupos',
    v => !showGroupFields.value || v >= 2 || 'Debe haber al menos 2 equipos por grupo',
    v => !showGroupFields.value || v <= 8 || 'No puede haber más de 8 equipos por grupo',
    v => !showGroupFields.value || Number.isInteger(v) || 'Debe ser un número entero',
  ]

  // Computed
  const isReadOnly = computed(() => props.mode === 'view')

  const showLeagueFields = computed(() => {
    return form.value.competition_type === 'league' || form.value.competition_type === 'hybrid'
  })

  const showGroupFields = computed(() => {
    return form.value.competition_type === 'groups'
  })

  // Métodos
  const onCompetitionTypeChange = value => {
    // Actualizar campos automáticamente según el tipo
    switch (value) {
      case 'league':
      case 'hybrid': {
        form.value.has_group_stage = false
        form.value.has_knockout = value === 'hybrid'
        break
      }
      case 'groups': {
        form.value.has_group_stage = true
        form.value.has_knockout = true
        break
      }
      case 'cup': {
        form.value.has_group_stage = false
        form.value.has_knockout = true
        break
      }
    }
  }

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
        competition_type: props.tournament.competition_type || 'cup',
        total_teams: props.tournament.total_teams || 8,
        has_group_stage: props.tournament.has_group_stage || false,
        has_knockout: props.tournament.has_knockout === undefined ? true : props.tournament.has_knockout,
        teams_per_group: props.tournament.teams_per_group || 4,
        league_rounds: props.tournament.league_rounds || 1,
        playoff_teams: props.tournament.playoff_teams || 4,
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
      competition_type: 'cup',
      total_teams: 8,
      has_group_stage: false,
      has_knockout: true,
      teams_per_group: 4,
      league_rounds: 1,
      playoff_teams: 4,
      rules: '',
    }
  }

  const getFormData = () => {
    return {
      name: form.value.name,
      format: form.value.format,
      competition_type: form.value.competition_type,
      total_teams: form.value.total_teams,
      has_group_stage: form.value.has_group_stage,
      has_knockout: form.value.has_knockout,
      teams_per_group: form.value.teams_per_group,
      league_rounds: form.value.league_rounds,
      playoff_teams: form.value.playoff_teams,
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
