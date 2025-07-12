<template>
  <v-container fluid>
    <!-- Loading state -->
    <div v-if="loading" class="d-flex justify-center align-center" style="min-height: 400px;">
      <v-progress-circular color="primary" indeterminate size="64" />
    </div>

    <!-- Error state -->
    <div v-else-if="error" class="text-center py-8">
      <v-icon class="mb-4" color="error" size="64">mdi-alert-circle</v-icon>
      <h3 class="text-h6 text-grey-darken-1 mb-2">Error al crear torneo</h3>
      <p class="text-body-2 text-grey-darken-1 mb-4">{{ error }}</p>
      <v-btn color="primary" rounded="xl" @click="createTournament">Reintentar</v-btn>
    </div>

    <!-- Form -->
    <div v-else>
      <!-- Header -->
      <v-row>
        <v-col cols="12">
          <div class="d-flex align-center mb-4">
            <v-btn
              icon
              variant="text"
              @click="goBack"
            >
              <v-icon>mdi-arrow-left</v-icon>
            </v-btn>
            <div>
              <h1 class="text-h4 font-weight-bold mb-2 page-title">Crear Nuevo Torneo</h1>
              <p class="text-body-1 page-subtitle">
                Configura los detalles de tu torneo
              </p>
            </div>
          </div>
        </v-col>
      </v-row>

      <!-- Tournament form -->
      <v-row>
        <v-col cols="12" md="8">
          <v-card>
            <v-card-title class="text-h6">
              <v-icon start>mdi-trophy</v-icon>
              Información del Torneo
            </v-card-title>
            <v-card-text>
              <v-form ref="form" v-model="valid">
                <v-row>
                  <v-col cols="12" md="6">
                    <v-text-field
                      v-model="tournament.name"
                      color="primary"
                      label="Nombre del Torneo"
                      required
                      rounded-xl
                      :rules="[v => !!v || 'El nombre es requerido']"
                      variant="outlined"
                    />
                  </v-col>

                  <v-col cols="12" md="6">
                    <v-select
                      v-model="tournament.format"
                      color="primary"
                      :items="formatOptions"
                      label="Formato"
                      required
                      rounded-xl
                      variant="outlined"
                    />
                  </v-col>

                  <v-col cols="12" md="6">
                    <v-select
                      v-model="tournament.competition_type"
                      color="primary"
                      item-title="text"
                      item-value="value"
                      :items="competitionTypes"
                      label="Tipo de Competición"
                      required
                      rounded-xl
                      variant="outlined"
                      @update:model-value="onCompetitionTypeChange"
                    />
                  </v-col>

                  <v-col cols="12" md="6">
                    <v-text-field
                      v-model.number="tournament.total_teams"
                      color="primary"
                      label="Número de Equipos"
                      max="32"
                      min="2"
                      required
                      rounded-xl
                      :rules="[v => v >= 2 || 'Mínimo 2 equipos']"
                      type="number"
                      variant="outlined"
                    />
                  </v-col>

                  <!-- Campos específicos para liga -->
                  <v-col v-if="showLeagueFields" cols="12" md="6">
                    <v-text-field
                      v-model.number="tournament.league_rounds"
                      color="primary"
                      label="Número de Vueltas"
                      max="3"
                      min="1"
                      rounded-xl
                      type="number"
                      variant="outlined"
                    />
                  </v-col>

                  <v-col v-if="showLeagueFields" cols="12" md="6">
                    <v-text-field
                      v-model.number="tournament.playoff_teams"
                      color="primary"
                      label="Equipos para Playoffs"
                      max="8"
                      min="2"
                      rounded-xl
                      type="number"
                      variant="outlined"
                    />
                  </v-col>

                  <!-- Campos específicos para grupos -->
                  <v-col v-if="showGroupFields" cols="12" md="6">
                    <v-text-field
                      v-model.number="tournament.teams_per_group"
                      color="primary"
                      label="Equipos por Grupo"
                      max="6"
                      min="2"
                      rounded-xl
                      type="number"
                      variant="outlined"
                    />
                  </v-col>

                  <v-col cols="12">
                    <v-textarea
                      v-model="tournament.rules"
                      auto-grow
                      color="primary"
                      label="Reglas del Torneo (Opcional)"
                      rounded-xl
                      rows="4"
                      variant="outlined"
                    />
                  </v-col>
                </v-row>
              </v-form>
            </v-card-text>
          </v-card>
        </v-col>

        <v-col cols="12" md="4">
          <v-card>
            <v-card-title class="text-h6">
              <v-icon start>mdi-information</v-icon>
              Resumen
            </v-card-title>
            <v-card-text>
              <div class="mb-3">
                <span class="text-body-2 text-grey-darken-1">Tipo:</span>
                <div class="font-weight-medium">{{ getCompetitionTypeText(tournament.competition_type) }}</div>
              </div>
              <div class="mb-3">
                <span class="text-body-2 text-grey-darken-1">Formato:</span>
                <div class="font-weight-medium">{{ tournament.format }}</div>
              </div>
              <div class="mb-3">
                <span class="text-body-2 text-grey-darken-1">Equipos:</span>
                <div class="font-weight-medium">{{ tournament.total_teams }}</div>
              </div>
              <div v-if="showLeagueFields" class="mb-3">
                <span class="text-body-2 text-grey-darken-1">Vueltas:</span>
                <div class="font-weight-medium">{{ tournament.league_rounds }}</div>
              </div>
              <div v-if="showLeagueFields" class="mb-3">
                <span class="text-body-2 text-grey-darken-1">Playoffs:</span>
                <div class="font-weight-medium">{{ tournament.playoff_teams }} equipos</div>
              </div>
              <div v-if="showGroupFields" class="mb-3">
                <span class="text-body-2 text-grey-darken-1">Por Grupo:</span>
                <div class="font-weight-medium">{{ tournament.teams_per_group }} equipos</div>
              </div>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>

      <!-- Actions -->
      <v-row class="mt-6">
        <v-col cols="12">
          <div class="d-flex gap-3">
            <v-btn
              color="secondary"
              variant="outlined"
              @click="goBack"
            >
              Cancelar
            </v-btn>
            <v-btn
              color="primary"
              :disabled="!valid"
              :loading="creating"
              @click="createTournament"
            >
              Crear Torneo
            </v-btn>
          </div>
        </v-col>
      </v-row>
    </div>
  </v-container>
</template>

<script setup>
  import { computed, ref } from 'vue'
  import { useRouter } from 'vue-router'
  import { handleApiError, tournamentAPI } from '@/services/api'

  // Router
  const router = useRouter()

  // Form ref
  const form = ref(null)
  const valid = ref(false)

  // Estado reactivo
  const tournament = ref({
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
  const creating = ref(false)
  const loading = ref(false)
  const error = ref(null)

  // Options
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

  // Computed
  const showLeagueFields = computed(() => {
    return tournament.value.competition_type === 'league' || tournament.value.competition_type === 'hybrid'
  })

  const showGroupFields = computed(() => {
    return tournament.value.competition_type === 'groups'
  })

  // Methods
  const onCompetitionTypeChange = value => {
    // Actualizar campos automáticamente según el tipo
    switch (value) {
      case 'league':
      case 'hybrid': {
        tournament.value.has_group_stage = false
        tournament.value.has_knockout = value === 'hybrid'

        break
      }
      case 'groups': {
        tournament.value.has_group_stage = true
        tournament.value.has_knockout = true

        break
      }
      case 'cup': {
        tournament.value.has_group_stage = false
        tournament.value.has_knockout = true

        break
      }
    // No default
    }
  }

  const getCompetitionTypeText = type => {
    const typeMap = {
      cup: 'Copa (Eliminatoria directa)',
      league: 'Liga (Todos contra todos)',
      hybrid: 'Liga + Playoffs',
      groups: 'Fase de grupos + Eliminatoria',
    }
    return typeMap[type] || 'Desconocido'
  }

  const createTournament = async () => {
    if (!form.value.validate()) return

    creating.value = true
    error.value = null

    try {
      console.log('Creando torneo:', tournament.value)

      const response = await tournamentAPI.createTournament(tournament.value)
      console.log('Torneo creado:', response.data)

      // Redirigir al torneo creado
      router.push(`/tournaments/${response.data.id}`)
    } catch (error_) {
      const errorInfo = handleApiError(error_)
      error.value = errorInfo.message
      console.error('Error al crear torneo:', errorInfo.message)
    } finally {
      creating.value = false
    }
  }

  const goBack = () => {
    router.push('/tournaments')
  }
</script>

<style scoped>
/* Estilos específicos si son necesarios */
</style>
