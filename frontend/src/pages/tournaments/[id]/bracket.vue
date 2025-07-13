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
              color="white"
              icon="mdi-arrow-left"
              variant="text"
              @click="goBack"
            />
            <div>
              <h1 class="text-h4 font-weight-bold mb-2 text-white">{{ tournament.name }}</h1>
              <p class="text-body-1 text-grey-darken-1">
                Fase Eliminatoria - {{ tournament.format }}
              </p>
            </div>
            <!-- Botón para alternar la vista -->
            <v-btn
              class="ml-auto"
              color="primary"
              variant="elevated"
              @click="toggleBracketView"
            >
              {{ showVisualBracket ? 'Vista clásica' : 'Vista visual' }}
            </v-btn>
          </div>
        </v-col>
      </v-row>

      <!-- Estado de las eliminatorias -->
      <v-row class="mb-6">
        <v-col cols="12" md="4">
          <v-card>
            <v-card-title class="text-h6">
              <v-icon start>mdi-trophy</v-icon>
              Estado de las Eliminatorias
            </v-card-title>
            <v-card-text>
              <div class="d-flex justify-space-between mb-2">
                <span class="text-body-2 text-grey-darken-1">Fase actual:</span>
                <span class="font-weight-medium">{{ currentEliminationPhase }}</span>
              </div>
              <div class="d-flex justify-space-between mb-2">
                <span class="text-body-2 text-grey-darken-1">Equipos activos:</span>
                <span class="font-weight-medium">{{ activeTeams }}/{{ totalTeams }}</span>
              </div>
              <div class="d-flex justify-space-between mb-2">
                <span class="text-body-2 text-grey-darken-1">Estado:</span>
                <v-chip
                  :color="eliminationStatus === 'completed' ? 'success' : 'warning'"
                  size="small"
                  variant="outlined"
                >
                  {{ eliminationStatusText }}
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
              Progreso de las Eliminatorias
            </v-card-title>
            <v-card-text>
              <div class="d-flex align-center mb-4">
                <div class="flex-grow-1 mr-4">
                  <v-progress-linear
                    color="primary"
                    height="8"
                    :model-value="eliminationProgress"
                    rounded
                  />
                </div>
                <span class="text-body-2 font-weight-medium">
                  {{ Math.round(eliminationProgress) }}%
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
                  {{ quarterfinalMatches.length }}/{{ quarterfinalMatches.length || 4 }}
                </v-chip>
                <v-chip
                  :color="semifinalsCompleted ? 'success' : 'grey'"
                  size="small"
                  variant="outlined"
                >
                  {{ semifinalMatches.length }}/{{ semifinalMatches.length || 2 }}
                </v-chip>
                <v-chip
                  :color="finalCompleted ? 'success' : 'grey'"
                  size="small"
                  variant="outlined"
                >
                  {{ finalMatches.length }}/{{ finalMatches.length || 1 }}
                </v-chip>
              </div>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>

      <!-- Botón dinámico para generar etapas -->
      <v-row v-if="canGenerateNextStage" class="mb-4">
        <v-col cols="12">
          <v-card>
            <v-card-text class="text-center">
              <v-btn
                color="success"
                :loading="generating"
                prepend-icon="mdi-trophy"
                size="large"
                @click="generateNextStage"
              >
                {{ generateButtonText }}
              </v-btn>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>

      <!-- Renderizado condicional de la vista -->
      <TournamentBracket
        v-if="!showVisualBracket"
        :generating="generating"
        :matches="matches"
        :tournament="tournament"
        @edit-match="editMatch"
        @generate-stage="generateStage"
        @view-match="viewMatch"
      />

      <TournamentBracketVisual
        v-else
        :generating="generating"
        :matches="matches"
        :tournament="tournament"
      />

      <!-- Match result dialog -->
      <MatchResultForm
        v-model="showMatchDialog"
        :match="selectedMatch"
        @save-result="saveMatchResult"
      />
    </div>

    <!-- Snackbar para notificaciones -->
    <v-snackbar
      v-model="appStore.snackbar.show"
      :color="appStore.snackbar.color"
      location="top"
      :timeout="appStore.snackbar.timeout"
    >
      {{ appStore.snackbar.message }}

      <template #actions>
        <v-btn
          color="white"
          text
          @click="appStore.hideSnackbar"
        >
          Cerrar
        </v-btn>
      </template>
    </v-snackbar>
  </v-container>
</template>

<script setup>
  import { computed, onMounted, ref, watch } from 'vue'
  import { useRoute, useRouter } from 'vue-router'
  import MatchResultForm from '@/components/MatchResultForm.vue'
  import TournamentBracket from '@/components/TournamentBracket.vue'
  import TournamentBracketVisual from '@/components/TournamentBracketVisual.vue'
  import { handleApiError, matchAPI, tournamentAPI } from '@/services/api'
  import { useAppStore } from '@/stores/app'

  // Router, Route y Store
  const router = useRouter()
  const route = useRoute()
  const appStore = useAppStore()

  // Estado reactivo
  const tournament = ref(null)
  const matches = ref([])
  const loading = ref(true)
  const error = ref(null)
  const generating = ref(false)
  const showMatchDialog = ref(false)
  const selectedMatch = ref(null)
  const showVisualBracket = ref(false)

  // Agregar estado para equipos clasificados
  const qualifiedTeams = ref([])
  const qualifiedTeamsCount = ref(0)

  // Computed corregidos
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

  const eliminationProgress = computed(() => {
    if (totalMatches.value === 0) return 0
    return Math.min((playedMatches.value / totalMatches.value) * 100, 100)
  })

  const quarterfinalsCompleted = computed(() => {
    return quarterfinalMatches.value.length > 0
      && quarterfinalMatches.value.every(match => match.played)
  })

  const semifinalsCompleted = computed(() => {
    return semifinalMatches.value.length > 0
      && semifinalMatches.value.every(match => match.played)
  })

  const finalCompleted = computed(() => {
    return finalMatches.value.length > 0
      && finalMatches.value.every(match => match.played)
  })

  // Computed para el botón dinámico - CORREGIDO
  const canGenerateNextStage = computed(() => {
    return (
      (quarterfinalsCompleted.value && semifinalMatches.value.length === 0)
      || (semifinalsCompleted.value && finalMatches.value.length === 0)
      || (totalMatches.value === 0)
    )
  })

  // Función para verificar si un equipo es real (no placeholder)
  const isRealTeam = team => {
    return team && team.id && team.name && !team.name.includes('Ganador M')
  }

  // Función para contar equipos reales en partidos
  const countRealTeams = matches => {
    const teams = new Set()
    for (const match of matches) {
      if (isRealTeam(match.team1)) teams.add(match.team1.id)
      if (isRealTeam(match.team2)) teams.add(match.team2.id)
    }
    return teams.size
  }

  // Corregir el computed de totalTeams
  const totalTeams = computed(() => {
    return countRealTeams(matches.value)
  })

  // Corregir el computed de activeTeams
  const activeTeams = computed(() => {
    const activeMatches = matches.value.filter(match => !match.played)
    return countRealTeams(activeMatches)
  })

  // Corregir la lógica del botón dinámico
  const generateButtonText = computed(() => {
    if (totalMatches.value === 0) {
      // Usar equipos clasificados en lugar de totalTeams
      if (qualifiedTeamsCount.value === 2) {
        return 'Generar Final'
      }
      if (qualifiedTeamsCount.value === 4) {
        return 'Generar Semifinales'
      }
      if (qualifiedTeamsCount.value === 8) {
        return 'Generar Cuartos de Final'
      }
      return 'Generar Eliminatorias'
    }
    if (quarterfinalsCompleted.value && semifinalMatches.value.length === 0) return 'Generar Semifinales'
    if (semifinalsCompleted.value && finalMatches.value.length === 0) return 'Generar Final'
    return 'Generar Siguiente Etapa'
  })

  // Estado específico de las eliminatorias
  const eliminationStatus = computed(() => {
    if (finalCompleted.value) return 'completed'
    if (semifinalsCompleted.value) return 'final_stage'
    if (quarterfinalsCompleted.value) return 'semifinal_stage'
    if (totalMatches.value > 0) return 'in_progress'
    return 'not_started'
  })

  const eliminationStatusText = computed(() => {
    const status = eliminationStatus.value
    const statusMap = {
      completed: 'Completada',
      final_stage: 'Final',
      semifinal_stage: 'Semifinales',
      in_progress: 'En progreso',
      not_started: 'No iniciada',
    }
    return statusMap[status] || 'Desconocido'
  })

  const currentEliminationPhase = computed(() => {
    if (finalCompleted.value) return 'Final'
    if (semifinalsCompleted.value) return 'Final'
    if (quarterfinalsCompleted.value) return 'Semifinales'
    if (quarterfinalMatches.value.length > 0) return 'Cuartos de Final'
    return 'No iniciada'
  })

  // Métodos
  const toggleBracketView = () => {
    showVisualBracket.value = !showVisualBracket.value
  }

  // Cargar equipos clasificados
  const loadQualifiedTeams = async tournamentId => {
    try {
      const response = await tournamentAPI.getQualifiedTeams(tournamentId)
      qualifiedTeams.value = response.data
      qualifiedTeamsCount.value = response.data.total_qualified || 0
      console.log('Equipos clasificados cargados:', qualifiedTeamsCount.value)
    } catch (error_) {
      console.error('Error al cargar equipos clasificados:', error_)
      qualifiedTeamsCount.value = 0
    }
  }

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

      // Cargar equipos clasificados
      await loadQualifiedTeams(tournamentId)

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
      // Usar tournamentAPI para obtener partidos del torneo
      const matchesResponse = await tournamentAPI.getTournamentMatches(tournamentId)

      // Procesar los datos correctamente
      const matchesData = matchesResponse.data
      if (Array.isArray(matchesData)) {
        matches.value = matchesData
      } else if (matchesData && Array.isArray(matchesData.matches)) {
        matches.value = matchesData.matches
      } else {
        matches.value = []
      }

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
    error.value = null

    try {
      console.log('Generando etapa:', stageData)

      let response
      if (stageData.stage) {
        // Completar etapa específica
        response = await tournamentAPI.knockoutStage(tournamentId, stageData)
      } else {
        // Generar nueva etapa
        response = await tournamentAPI.knockoutStage(tournamentId, {})
      }

      console.log('Etapa generada:', response.data)

      // Recargar partidos
      await loadMatches(tournamentId)

      console.log('Etapa generada exitosamente')
    } catch (error_) {
      const errorInfo = handleApiError(error_)
      console.error('Error al generar etapa:', errorInfo.message)
      error.value = `Error al generar etapa: ${errorInfo.message}`
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

  // Validar que los datos del backend sean correctos
  const validateBackendResponse = response => {
    if (!response || !response.data) {
      throw new Error('Respuesta del servidor inválida')
    }

    const data = response.data

    // Validar que se generaron partidos
    if (data.matches_created !== undefined && data.matches_created === 0) {
      throw new Error('No se generaron partidos')
    }

    // Validar que hay equipos clasificados
    if (data.qualified_teams !== undefined && data.qualified_teams < 2) {
      throw new Error('No hay suficientes equipos clasificados')
    }

    return data
  }

  // Generar siguiente etapa con validaciones mejoradas - CORREGIDO
  const generateNextStage = async () => {
    const tournamentId = route.params.id

    try {
      generating.value = true

      let response
      let stageName = ''

      if (totalMatches.value === 0) {
        // Determinar qué etapa generar según la cantidad de equipos clasificados
        if (qualifiedTeamsCount.value === 2) {
          // Solo 2 equipos: generar directamente la final
          console.log('Generando final directamente...')
          response = await tournamentAPI.knockoutStage(tournamentId, { stage: 'final' })
          const validatedData = validateBackendResponse(response)
          stageName = 'final'
          appStore.showSuccess(`Final generada: ${validatedData.winners_count || 2} equipos clasificados`)
        } else if (qualifiedTeamsCount.value === 4) {
          // 4 equipos: generar semifinales
          console.log('Generando semifinales...')
          response = await tournamentAPI.knockoutStage(tournamentId, { stage: 'semifinal' })
          const validatedData = validateBackendResponse(response)
          stageName = 'semifinales'
          appStore.showSuccess(`Semifinales generadas: ${validatedData.winners_count || 2} equipos clasificados`)
        } else {
          // Más de 4 equipos: generar eliminatoria inicial
          console.log('Generando eliminatoria inicial...')
          response = await tournamentAPI.knockoutStage(tournamentId, {})
          const validatedData = validateBackendResponse(response)
          stageName = validatedData.stage || 'eliminatorias'
          appStore.showSuccess(`Eliminatorias generadas: ${stageName} con ${validatedData.qualified_teams} equipos`)
        }
      } else if (quarterfinalsCompleted.value && semifinalMatches.value.length === 0) {
        // Generar semifinales
        console.log('Generando semifinales...')
        response = await tournamentAPI.knockoutStage(tournamentId, { stage: 'semifinal' })
        const validatedData = validateBackendResponse(response)
        stageName = 'semifinales'
        appStore.showSuccess(`Semifinales generadas: ${validatedData.winners_count || 2} equipos clasificados`)
      } else if (semifinalsCompleted.value && finalMatches.value.length === 0) {
        // Generar final
        console.log('Generando final...')
        response = await tournamentAPI.knockoutStage(tournamentId, { stage: 'final' })
        const validatedData = validateBackendResponse(response)
        stageName = 'final'
        appStore.showSuccess(`Final generada: ${validatedData.winners_count || 2} equipos clasificados`)
      }

      // Recargar partidos después de generar
      await loadMatches(tournamentId)

      // Mostrar información adicional si está disponible
      if (response?.data?.matches_info) {
        console.log('Partidos generados:', response.data.matches_info)
      }

      // Verificar si se completó el torneo
      if (finalCompleted.value) {
        appStore.showSuccess('¡Torneo completado! Se ha determinado el campeón.')
      }
    } catch (error_) {
      const errorInfo = handleApiError(error_)
      appStore.showError(`Error al generar etapa: ${errorInfo.message}`)
      console.error('Error al generar etapa:', errorInfo.message)
    } finally {
      generating.value = false
    }
  }

  // Guardar resultado del partido con mejoras
  const saveMatchResult = async result => {
    try {
      console.log('Guardando resultado:', result)

      const matchId = result.matchId
      const selectedMatch = matches.value.find(m => m.id === matchId)

      if (!selectedMatch) {
        throw new Error('Partido no encontrado')
      }

      // Validar que el partido tenga equipos válidos
      if (!selectedMatch.team1 || !selectedMatch.team2) {
        throw new Error('Partido sin equipos válidos')
      }

      const team1Id = selectedMatch.team1.id
      const team2Id = selectedMatch.team2.id

      const matchData = {
        goals: {
          [team1Id]: result.team1Score,
          [team2Id]: result.team2Score,
        },
      }

      // Guardar resultado
      await matchAPI.saveMatchResult(matchId, matchData)

      // Recargar partidos para obtener datos actualizados
      await loadMatches(route.params.id)

      // Mostrar notificación de éxito con información del ganador
      const winner = result.team1Score > result.team2Score ? selectedMatch.team1 : selectedMatch.team2
      const winnerName = winner.name || winner.display_name || winner.team?.name || 'Equipo ganador'

      appStore.showSuccess(`Resultado guardado. Ganador: ${winnerName}`)

      // Verificar si se debe generar la siguiente etapa automáticamente
      await checkAndGenerateNextStage()

      console.log('Resultado guardado exitosamente')
    } catch (error_) {
      const errorInfo = handleApiError(error_)
      appStore.showError(`Error al guardar resultado: ${errorInfo.message}`)
      console.error('Error al guardar resultado:', errorInfo.message)
    }
  }

  // Navegación
  const goBack = () => {
    router.push(`/tournaments/${route.params.id}`)
  }

  // Verificar si se debe generar la siguiente etapa automáticamente
  const checkAndGenerateNextStage = async () => {
    const tournamentId = route.params.id

    try {
      // Verificar si se completaron cuartos y no hay semifinales
      if (quarterfinalsCompleted.value && semifinalMatches.value.length === 0) {
        console.log('Generando semifinales automáticamente...')
        await tournamentAPI.knockoutStage(tournamentId, { stage: 'semifinal' })
        await loadMatches(tournamentId)
        appStore.showInfo('Semifinales generadas automáticamente')
      }

      // Verificar si se completaron semifinales y no hay final
      if (semifinalsCompleted.value && finalMatches.value.length === 0) {
        console.log('Generando final automáticamente...')
        await tournamentAPI.knockoutStage(tournamentId, { stage: 'final' })
        await loadMatches(tournamentId)
        appStore.showInfo('Final generada automáticamente')
      }
    } catch (error_) {
      console.error('Error al generar siguiente etapa:', error_)
      appStore.showError('Error al generar siguiente etapa automáticamente')
    }
  }

  // Observar cambios en los partidos para generar automáticamente
  watch(matches, () => {
    checkAndGenerateNextStage()
  }, { deep: true })

  // Cargar datos al montar el componente
  onMounted(() => {
    loadTournament()
  })
</script>

<style scoped>
.tournament-bracket {
  width: 100%;
}

.bracket-header {
  text-align: center;
}

.bracket-container {
  overflow-x: auto;
  margin: 20px 0;
}

.bracket-grid {
  display: flex;
  gap: 40px;
  min-width: max-content;
  padding: 20px;
}

.bracket-round {
  min-width: 300px;
}

.round-title {
  text-align: center;
  margin-bottom: 20px;
  font-weight: bold;
  color: var(--v-primary-base);
  background-color: white;
  padding: 8px 16px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.team-details {
  display: flex;
  flex-direction: column;
}

.team-players {
  margin-top: 2px;
}
</style>
