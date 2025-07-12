<template>
  <v-container fluid>
    <!-- Loading state -->
    <div v-if="loading" class="d-flex justify-center align-center" style="min-height: 400px;">
      <v-progress-circular color="primary" indeterminate size="64" />
    </div>

    <!-- Error state -->
    <div v-else-if="error" class="text-center py-8">
      <v-icon class="mb-4" color="error" size="64">mdi-alert-circle</v-icon>
      <h3 class="text-h6 text-grey-darken-1 mb-2">Error al cargar torneo</h3>
      <p class="text-body-2 text-grey-darken-1 mb-4">{{ error }}</p>
      <v-btn color="primary" @click="loadTournament">Reintentar</v-btn>
    </div>

    <!-- Tournament bracket -->
    <div v-else-if="tournament">
      <!-- Header -->
      <v-row class="mb-6">
        <v-col cols="12">
          <div class="d-flex align-center mb-4">
            <v-btn
              class="mr-4"
              icon="mdi-arrow-left"
              variant="text"
              @click="goBack"
            />
            <div>
              <h1 class="text-h4 font-weight-bold mb-2">{{ tournament.name }}</h1>
              <p class="text-body-1 text-grey-darken-1">
                Fase Eliminatoria - {{ tournament.format }}
              </p>
            </div>
          </div>
        </v-col>
      </v-row>

      <!-- Tournament info card -->
      <v-row class="mb-6">
        <v-col cols="12" md="4">
          <v-card>
            <v-card-title class="text-h6">
              <v-icon start>mdi-information</v-icon>
              Información del Torneo
            </v-card-title>
            <v-card-text>
              <div class="d-flex justify-space-between mb-2">
                <span class="text-body-2 text-grey-darken-1">Formato:</span>
                <span class="font-weight-medium">{{ tournament.format }}</span>
              </div>
              <div class="d-flex justify-space-between mb-2">
                <span class="text-body-2 text-grey-darken-1">Equipos:</span>
                <span class="font-weight-medium">{{ tournament.team_count || 0 }}</span>
              </div>
              <div class="d-flex justify-space-between mb-2">
                <span class="text-body-2 text-grey-darken-1">Estado:</span>
                <v-chip
                  :color="tournament.status === 'completed' ? 'success' : 'warning'"
                  size="small"
                  variant="outlined"
                >
                  {{ tournament.status === 'completed' ? 'Completado' : 'En progreso' }}
                </v-chip>
              </div>
              <div class="d-flex justify-space-between">
                <span class="text-body-2 text-grey-darken-1">Partidos jugados:</span>
                <span class="font-weight-medium">{{ playedMatches }}/{{ totalMatches }}</span>
              </div>
            </v-card-text>
          </v-card>
        </v-col>

        <v-col cols="12" md="8">
          <v-card>
            <v-card-title class="text-h6">
              <v-icon start>mdi-trophy</v-icon>
              Progreso del Torneo
            </v-card-title>
            <v-card-text>
              <div class="d-flex align-center mb-4">
                <div class="flex-grow-1 mr-4">
                  <v-progress-linear
                    color="primary"
                    height="8"
                    :model-value="progressPercentage"
                    rounded
                  />
                </div>
                <span class="text-body-2 font-weight-medium">
                  {{ Math.round(progressPercentage) }}%
                </span>
              </div>

              <div class="d-flex justify-space-between text-caption text-grey-darken-1">
                <span>Cuartos de Final</span>
                <span>Semifinales</span>
                <span>Final</span>
              </div>

              <div class="d-flex justify-space-between mt-2">
                <v-chip
                  :color="quarterfinalsCompleted ? 'success' : 'grey'"
                  size="small"
                  variant="outlined"
                >
                  {{ quarterfinalMatches.length }}/4
                </v-chip>
                <v-chip
                  :color="semifinalsCompleted ? 'success' : 'grey'"
                  size="small"
                  variant="outlined"
                >
                  {{ semifinalMatches.length }}/2
                </v-chip>
                <v-chip
                  :color="finalCompleted ? 'success' : 'grey'"
                  size="small"
                  variant="outlined"
                >
                  {{ finalMatches.length }}/1
                </v-chip>
              </div>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>

      <!-- Bracket component -->
      <TournamentBracket
        :generating="generating"
        :matches="matches"
        :tournament="tournament"
        @edit-match="editMatch"
        @generate-stage="generateStage"
        @view-match="viewMatch"
      />

      <!-- Match result dialog -->
      <MatchResultForm
        v-model="showMatchDialog"
        :match="selectedMatch"
        @save-result="saveMatchResult"
      />
    </div>
  </v-container>
</template>

<script setup>
  import { computed, onMounted, ref } from 'vue'
  import { useRoute, useRouter } from 'vue-router'
  import MatchResultForm from '@/components/MatchResultForm.vue'
  import TournamentBracket from '@/components/TournamentBracket.vue'
  import { handleApiError, matchAPI, tournamentAPI } from '@/services/api'

  // Router y Route
  const router = useRouter()
  const route = useRoute()

  // Estado reactivo
  const tournament = ref(null)
  const matches = ref([])
  const loading = ref(true)
  const error = ref(null)
  const generating = ref(false)
  const showMatchDialog = ref(false)
  const selectedMatch = ref(null)

  // Computed
  const quarterfinalMatches = computed(() => {
    return matches.value.filter(match => match.stage === 'quarterfinal')
  })

  const semifinalMatches = computed(() => {
    return matches.value.filter(match => match.stage === 'semifinal')
  })

  const finalMatches = computed(() => {
    return matches.value.filter(match => match.stage === 'final')
  })

  const totalMatches = computed(() => {
    return quarterfinalMatches.value.length + semifinalMatches.value.length + finalMatches.value.length
  })

  const playedMatches = computed(() => {
    return matches.value.filter(match => match.played).length
  })

  const progressPercentage = computed(() => {
    if (totalMatches.value === 0) return 0
    return (playedMatches.value / totalMatches.value) * 100
  })

  const quarterfinalsCompleted = computed(() => {
    return quarterfinalMatches.value.length === 4
      && quarterfinalMatches.value.every(match => match.played)
  })

  const semifinalsCompleted = computed(() => {
    return semifinalMatches.value.length === 2
      && semifinalMatches.value.every(match => match.played)
  })

  const finalCompleted = computed(() => {
    return finalMatches.value.length === 1
      && finalMatches.value.every(match => match.played)
  })

  // Cargar torneo
  const loadTournament = async () => {
    const tournamentId = route.params.id

    loading.value = true
    error.value = null

    try {
      console.log('Cargando torneo con ID:', tournamentId)

      // Cargar datos del torneo
      const tournamentResponse = await tournamentAPI.getTournament(tournamentId)
      tournament.value = tournamentResponse.data
      console.log('Datos del torneo cargados:', tournament.value)

      // Cargar partidos del torneo
      await loadMatches(tournamentId)
    } catch (error_) {
      const errorInfo = handleApiError(error_)
      error.value = errorInfo.message
      console.error('Error al cargar torneo:', errorInfo.message)
    } finally {
      loading.value = false
    }
  }

  // Cargar partidos
  const loadMatches = async tournamentId => {
    try {
      const matchesResponse = await matchAPI.getTournamentMatches(tournamentId)
      // Asegurar que matches sea siempre un array
      matches.value = matchesResponse.data?.matches || matchesResponse.data || []
      console.log('Partidos del torneo cargados:', matches.value)
    } catch (error_) {
      console.error('Error al cargar partidos:', error_)
      matches.value = []
    }
  }

  // Generar etapa
  const generateStage = async stageData => {
    const tournamentId = route.params.id

    generating.value = true
    try {
      console.log('Generando etapa:', stageData)

      const response = await tournamentAPI.completeKnockoutStage(tournamentId, stageData)
      console.log('Etapa generada:', response.data)

      // Recargar partidos
      await loadMatches(tournamentId)

      // Mostrar mensaje de éxito
      // Aquí podrías usar un sistema de notificaciones
      console.log('Etapa generada exitosamente')
    } catch (error_) {
      const errorInfo = handleApiError(error_)
      console.error('Error al generar etapa:', errorInfo.message)
    // Aquí podrías mostrar un mensaje de error
    } finally {
      generating.value = false
    }
  }

  // Editar partido
  const editMatch = match => {
    selectedMatch.value = match
    showMatchDialog.value = true
  }

  // Ver partido
  const viewMatch = match => {
    // Aquí podrías navegar a una página de detalle del partido
    console.log('Ver partido:', match)
  }

  // Guardar resultado del partido
  const saveMatchResult = async result => {
    try {
      console.log('Guardando resultado:', result)

      const matchId = result.matchId
      const matchData = {
        played: true,
        goals: {
          // Aquí necesitarías mapear los IDs de los equipos correctamente
          // Por ahora usamos valores de ejemplo
          [result.team1Id || 1]: result.team1Score,
          [result.team2Id || 2]: result.team2Score,
        },
      }

      await matchAPI.markMatchAsPlayed(matchId, matchData)

      // Recargar partidos
      await loadMatches(route.params.id)

      console.log('Resultado guardado exitosamente')
    } catch (error_) {
      const errorInfo = handleApiError(error_)
      console.error('Error al guardar resultado:', errorInfo.message)
    }
  }

  // Navegación
  const goBack = () => {
    router.push(`/tournaments/${route.params.id}`)
  }

  // Cargar datos al montar el componente
  onMounted(() => {
    loadTournament()
  })
</script>

<style scoped>
/* Estilos específicos si son necesarios */
</style>
