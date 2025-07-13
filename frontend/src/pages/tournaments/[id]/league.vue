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

    <!-- Content -->
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
              <h1 class="text-h4 font-weight-bold mb-2">{{ tournament.name }}</h1>
              <p class="text-body-1 text-grey-darken-1">
                Liga - {{ tournament.format }}
              </p>
            </div>
          </div>
        </v-col>
      </v-row>

      <!-- Tournament info -->
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
                  :color="getStatusColor(tournament.status)"
                  size="small"
                  variant="outlined"
                >
                  {{ getStatusText(tournament.status) }}
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
              <v-icon start>mdi-chart-line</v-icon>
              Progreso de la Liga
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
                <span>Partidos Generados</span>
                <span>Partidos Jugados</span>
                <span>Clasificados</span>
              </div>

              <div class="d-flex justify-space-between mt-2">
                <v-chip
                  :color="matchesGenerated ? 'success' : 'grey'"
                  size="small"
                  variant="outlined"
                >
                  {{ totalMatches }}
                </v-chip>
                <v-chip
                  :color="progressPercentage > 0 ? 'warning' : 'grey'"
                  size="small"
                  variant="outlined"
                >
                  {{ playedMatches }}
                </v-chip>
                <v-chip
                  :color="playoffsReady ? 'success' : 'grey'"
                  size="small"
                  variant="outlined"
                >
                  {{ tournament.playoff_teams || 4 }}
                </v-chip>
              </div>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>

      <!-- League standings -->
      <v-row>
        <v-col cols="12">
          <TournamentStandings
            :qualified-count="tournament.playoff_teams || 4"
            :standings="standings"
            title="Clasificación de la Liga"
          />
        </v-col>
      </v-row>

      <!-- League matches -->
      <v-row class="mt-6">
        <v-col cols="12">
          <v-card>
            <v-card-title class="text-h6">
              <v-icon start>mdi-soccer</v-icon>
              Partidos de la Liga
              <v-spacer />
              <v-btn
                v-if="leagueMatches.length === 0"
                color="primary"
                :loading="generating"
                @click="generateLeagueMatches"
              >
                Generar Partidos
              </v-btn>
            </v-card-title>
            <v-card-text>
              <div v-if="leagueMatches.length === 0" class="text-center py-8">
                <v-icon class="mb-4" color="grey-lighten-1" size="48">
                  mdi-soccer
                </v-icon>
                <h4 class="text-h6 text-grey-darken-1 mb-2">
                  No hay partidos generados
                </h4>
                <p class="text-body-2 text-grey-darken-1">
                  Genera los partidos de la liga para comenzar.
                </p>
              </div>
              <div v-else>
                <!-- Lista de partidos -->
                <v-list>
                  <v-list-item
                    v-for="match in leagueMatches"
                    :key="match.id"
                    :subtitle="`Jornada ${match.round || 'N/A'} • ${match.played ? 'Completado' : 'Pendiente'}`"
                    :title="`${match.team1?.name || 'TBD'} vs ${match.team2?.name || 'TBD'}`"
                  >
                    <template #prepend>
                      <v-icon color="primary">mdi-soccer</v-icon>
                    </template>
                    <template #append>
                      <div class="d-flex align-center">
                        <span v-if="match.played" class="text-body-2 font-weight-bold mr-2">
                          {{ match.team1_score }} - {{ match.team2_score }}
                        </span>
                        <v-btn
                          v-if="!match.played"
                          color="primary"
                          size="small"
                          variant="outlined"
                          @click="editMatch(match)"
                        >
                          Editar
                        </v-btn>
                        <v-chip
                          v-else
                          :color="match.winner ? 'success' : 'grey'"
                          size="small"
                          variant="outlined"
                        >
                          {{ match.winner ? 'Completado' : 'En progreso' }}
                        </v-chip>
                      </div>
                    </template>
                  </v-list-item>
                </v-list>
              </div>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>

      <!-- Generate playoffs button -->
      <v-row v-if="playoffsReady" class="mt-6">
        <v-col cols="12">
          <v-card>
            <v-card-title class="text-h6">
              <v-icon start>mdi-trophy</v-icon>
              Playoffs
            </v-card-title>
            <v-card-text>
              <p class="text-body-2 mb-4">
                La liga está completada. Los mejores {{ tournament.playoff_teams || 4 }} equipos pueden avanzar a los playoffs.
              </p>
              <v-btn
                color="warning"
                :loading="generatingPlayoffs"
                prepend-icon="mdi-trophy"
                @click="generatePlayoffs"
              >
                Generar Playoffs
              </v-btn>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </div>

    <!-- Match result dialog -->
    <MatchResultForm
      v-model="showMatchDialog"
      :match="selectedMatch"
      @save-result="saveMatchResult"
    />
  </v-container>
</template>

<script setup>
  import { computed, onMounted, ref } from 'vue'
  import { useRoute, useRouter } from 'vue-router'
  import MatchResultForm from '@/components/MatchResultForm.vue'
  import TournamentStandings from '@/components/TournamentStandings.vue'
  import { handleApiError, matchAPI, tournamentAPI } from '@/services/api'

  // Router y Route
  const router = useRouter()
  const route = useRoute()

  // Estado reactivo
  const tournament = ref(null)
  const matches = ref([])
  const standings = ref([])
  const loading = ref(true)
  const error = ref(null)
  const generating = ref(false)
  const generatingPlayoffs = ref(false)
  const showMatchDialog = ref(false)
  const selectedMatch = ref(null)

  // Computed
  const leagueMatches = computed(() => {
    return matches.value.filter(match => match.stage === 'league')
  })

  const totalMatches = computed(() => {
    return leagueMatches.value.length
  })

  const playedMatches = computed(() => {
    return leagueMatches.value.filter(match => match.played).length
  })

  const progressPercentage = computed(() => {
    if (totalMatches.value === 0) return 0
    return (playedMatches.value / totalMatches.value) * 100
  })

  const matchesGenerated = computed(() => {
    return totalMatches.value > 0
  })

  const playoffsReady = computed(() => {
    return progressPercentage.value === 100 && standings.value.length >= (tournament.value?.playoff_teams || 4)
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

      // Cargar clasificación
      await loadStandings(tournamentId)
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
      matches.value = matchesResponse.data
      console.log('Partidos del torneo cargados:', matches.value)
    } catch (error_) {
      console.error('Error al cargar partidos:', error_)
      matches.value = []
    }
  }

  // Cargar clasificación
  const loadStandings = async tournamentId => {
    try {
      const standingsResponse = await tournamentAPI.getStandings(tournamentId, 'tournament')
      standings.value = standingsResponse.data
      console.log('Clasificación cargada:', standings.value)
    } catch (error_) {
      console.error('Error al cargar clasificación:', error_)
      standings.value = []
    }
  }

  // Generar partidos de liga
  const generateLeagueMatches = async () => {
    const tournamentId = route.params.id

    generating.value = true

    try {
      await tournamentAPI.generateLeagueMatches(tournamentId)
      await loadMatches(tournamentId)
      console.log('Partidos de liga generados')
    } catch (error_) {
      const errorInfo = handleApiError(error_)
      console.error('Error al generar partidos:', errorInfo.message)
    } finally {
      generating.value = false
    }
  }

  // Generar playoffs
  const generatePlayoffs = async () => {
    const tournamentId = route.params.id

    generatingPlayoffs.value = true

    try {
      await tournamentAPI.generatePlayoffs(tournamentId)
      router.push(`/tournaments/${tournamentId}/bracket`)
      console.log('Playoffs generados')
    } catch (error_) {
      const errorInfo = handleApiError(error_)
      console.error('Error al generar playoffs:', errorInfo.message)
    } finally {
      generatingPlayoffs.value = false
    }
  }

  // Editar partido
  const editMatch = match => {
    selectedMatch.value = match
    showMatchDialog.value = true
  }

  // Guardar resultado
  const saveMatchResult = async result => {
    try {
      await matchAPI.saveMatchResult(selectedMatch.value.id, result)
      await loadMatches(route.params.id)
      await loadStandings(route.params.id)
      showMatchDialog.value = false
      console.log('Resultado guardado')
    } catch (error_) {
      const errorInfo = handleApiError(error_)
      console.error('Error al guardar resultado:', errorInfo.message)
    }
  }

  // Navegación
  const goBack = () => {
    router.push(`/tournaments/${route.params.id}`)
  }

  // Utilidades
  const getStatusColor = status => {
    const colors = {
      draft: 'grey',
      active: 'warning',
      completed: 'success',
      cancelled: 'error',
    }
    return colors[status] || 'grey'
  }

  const getStatusText = status => {
    const texts = {
      draft: 'Borrador',
      active: 'En progreso',
      completed: 'Completado',
      cancelled: 'Cancelado',
    }
    return texts[status] || 'Desconocido'
  }

  // Cargar datos al montar el componente
  onMounted(() => {
    loadTournament()
  })
</script>

<style scoped>
.qualified {
  background-color: rgba(var(--v-theme-success), 0.1);
}
</style>
