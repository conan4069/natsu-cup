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
      <v-btn color="primary" rounded="xl" @click="loadTournament">Reintentar</v-btn>
    </div>

    <!-- Tournament details -->
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
            <div class="flex-grow-1">
              <h1 class="text-h4 font-weight-bold mb-2 page-title">{{ tournament.name }}</h1>
              <p class="text-body-1 page-subtitle">
                {{ tournament.description || 'Torneo de fútbol' }}
              </p>
            </div>
            <div class="d-flex gap-2">
              <v-btn
                color="primary"
                prepend-icon="mdi-pencil"
                rounded="xl"
                variant="outlined"
                @click="editTournament"
              >
                Editar
              </v-btn>
              <v-btn
                color="error"
                prepend-icon="mdi-delete"
                rounded="xl"
                variant="outlined"
                @click="deleteTournament"
              >
                Eliminar
              </v-btn>
            </div>
          </div>
        </v-col>
      </v-row>

      <!-- Tournament info -->
      <v-row>
        <v-col cols="12" md="8">
          <v-card>
            <v-card-title class="text-h6">
              <v-icon start>mdi-information</v-icon>
              Información del Torneo
            </v-card-title>
            <v-card-text>
              <v-row>
                <v-col cols="6">
                  <div class="mb-3">
                    <span class="text-body-2 text-grey-darken-1">Formato:</span>
                    <div class="font-weight-medium">{{ tournament.format }}</div>
                  </div>
                  <div class="mb-3">
                    <span class="text-body-2 text-grey-darken-1">Equipos:</span>
                    <div class="font-weight-medium">{{ tournament.team_count || tournament.total_teams || 0 }}</div>
                  </div>
                  <div class="mb-3">
                    <span class="text-body-2 text-grey-darken-1">Estado:</span>
                    <div>
                      <v-chip
                        :color="getStatusColor(tournament.status)"
                        size="small"
                        variant="outlined"
                      >
                        {{ getStatusText(tournament.status) }}
                      </v-chip>
                    </div>
                  </div>
                  <div class="mb-3">
                    <span class="text-body-2 text-grey-darken-1">Fecha de creación:</span>
                    <div class="font-weight-medium">
                      {{ tournament.created_at ? new Date(tournament.created_at).toLocaleDateString() : 'N/A' }}
                    </div>
                  </div>
                </v-col>
                <v-col cols="6">
                  <div class="mb-3">
                    <span class="text-body-2 text-grey-darken-1">Tipo de competición:</span>
                    <div class="font-weight-medium">{{ getCompetitionTypeText(tournament.competition_type) }}</div>
                  </div>
                  <div v-if="tournament.has_group_stage" class="mb-3">
                    <span class="text-body-2 text-grey-darken-1">Equipos por grupo:</span>
                    <div class="font-weight-medium">{{ tournament.teams_per_group }}</div>
                  </div>
                  <div v-if="tournament.league_rounds" class="mb-3">
                    <span class="text-body-2 text-grey-darken-1">Vueltas:</span>
                    <div class="font-weight-medium">{{ tournament.league_rounds }}</div>
                  </div>
                  <div v-if="tournament.playoff_teams" class="mb-3">
                    <span class="text-body-2 text-grey-darken-1">Equipos para playoffs:</span>
                    <div class="font-weight-medium">{{ tournament.playoff_teams }}</div>
                  </div>
                </v-col>
              </v-row>
            </v-card-text>
          </v-card>
        </v-col>

        <v-col cols="12" md="4">
          <v-card>
            <v-card-title class="text-h6">
              <v-icon start>mdi-chart-line</v-icon>
              Estadísticas Rápidas
            </v-card-title>
            <v-card-text>
              <div class="mb-3">
                <span class="text-body-2 text-grey-darken-1">Participantes:</span>
                <div class="font-weight-medium">{{ tournament.participant_count || 0 }}</div>
              </div>
              <div class="mb-3">
                <span class="text-body-2 text-grey-darken-1">Partidos jugados:</span>
                <div class="font-weight-medium">{{ tournament.matches_played || 0 }}</div>
              </div>
              <div class="mb-3">
                <span class="text-body-2 text-grey-darken-1">Partidos pendientes:</span>
                <div class="font-weight-medium">{{ tournament.matches_pending || 0 }}</div>
              </div>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>

      <!-- Navigation tabs -->
      <v-row class="mt-6">
        <v-col cols="12">
          <v-card>
            <v-tabs v-model="activeTab" color="primary" rounded="xl">
              <v-tab value="overview">
                <v-icon start>mdi-view-dashboard</v-icon>
                Resumen
              </v-tab>
              <v-tab value="teams">
                <v-icon start>mdi-shield</v-icon>
                Equipos
              </v-tab>
              <v-tab value="groups">
                <v-icon start>mdi-account-group</v-icon>
                Grupos
              </v-tab>
              <v-tab value="bracket">
                <v-icon start>mdi-trophy</v-icon>
                Eliminatoria
              </v-tab>
              <v-tab value="league">
                <v-icon start>mdi-chart-line</v-icon>
                Liga
              </v-tab>
              <v-tab value="stats">
                <v-icon start>mdi-chart-bar</v-icon>
                Estadísticas
              </v-tab>
            </v-tabs>

            <v-window v-model="activeTab">
              <v-window-item value="overview">
                <v-card-text class="pa-6">
                  <div class="text-center py-8">
                    <v-icon class="mb-4" color="primary" size="64">mdi-trophy</v-icon>
                    <h3 class="text-h5 mb-2">{{ tournament.name }}</h3>
                    <p class="text-body-1 text-grey-darken-1 mb-4">
                      Selecciona una pestaña para ver los detalles del torneo
                    </p>
                  </div>
                </v-card-text>
              </v-window-item>

              <v-window-item value="teams">
                <v-card-text class="pa-6">
                  <div class="text-center">
                    <v-btn
                      color="primary"
                      prepend-icon="mdi-shield"
                      rounded="xl"
                      variant="elevated"
                      @click="goToTeams"
                    >
                      Ver Equipos
                    </v-btn>
                  </div>
                </v-card-text>
              </v-window-item>

              <v-window-item value="groups">
                <v-card-text class="pa-6">
                  <div class="text-center">
                    <v-btn
                      color="primary"
                      prepend-icon="mdi-account-group"
                      rounded="xl"
                      variant="elevated"
                      @click="goToGroups"
                    >
                      Ver Grupos
                    </v-btn>
                  </div>
                </v-card-text>
              </v-window-item>

              <v-window-item value="bracket">
                <v-card-text class="pa-6">
                  <div class="text-center">
                    <v-btn
                      color="primary"
                      prepend-icon="mdi-trophy"
                      rounded="xl"
                      variant="elevated"
                      @click="goToBracket"
                    >
                      Ver Eliminatoria
                    </v-btn>
                  </div>
                </v-card-text>
              </v-window-item>

              <v-window-item value="league">
                <v-card-text class="pa-6">
                  <div class="text-center">
                    <v-btn
                      color="primary"
                      prepend-icon="mdi-chart-line"
                      rounded="xl"
                      variant="elevated"
                      @click="goToLeague"
                    >
                      Ver Liga
                    </v-btn>
                  </div>
                </v-card-text>
              </v-window-item>

              <v-window-item value="stats">
                <v-card-text class="pa-6">
                  <div class="text-center">
                    <v-btn
                      color="primary"
                      prepend-icon="mdi-chart-bar"
                      rounded="xl"
                      variant="elevated"
                      @click="goToStats"
                    >
                      Ver Estadísticas
                    </v-btn>
                  </div>
                </v-card-text>
              </v-window-item>
            </v-window>
          </v-card>
        </v-col>
      </v-row>
    </div>
  </v-container>
</template>

<script setup>
  import { onMounted, ref } from 'vue'
  import { useRoute, useRouter } from 'vue-router'
  import { handleApiError, tournamentAPI } from '@/services/api'
  import { useAppStore } from '@/stores/app'

  // Router y Route
  const router = useRouter()
  const route = useRoute()
  const appStore = useAppStore()

  // Estado reactivo
  const loading = ref(true)
  const error = ref(null)
  const tournament = ref(null)
  const activeTab = ref('overview')

  // Cargar torneo
  const loadTournament = async () => {
    const tournamentId = route.params.id

    loading.value = true
    error.value = null

    try {
      const response = await tournamentAPI.getTournament(tournamentId)
      tournament.value = response.data
    } catch (error_) {
      const errorInfo = handleApiError(error_)
      error.value = errorInfo.message
      appStore.showError(`Error al cargar torneo: ${errorInfo.message}`)
      console.error('Error al cargar torneo:', errorInfo.message)
    } finally {
      loading.value = false
    }
  }

  // Navegación
  const goBack = () => {
    router.push('/tournaments')
  }

  const editTournament = () => {
    router.push(`/tournaments/${tournament.value.id}/edit`)
  }

  const deleteTournament = () => {
    // TODO: Implementar eliminación
    console.log('Eliminar torneo')
  }

  const goToTeams = () => {
    router.push(`/tournaments/${tournament.value.id}/teams`)
  }

  const goToGroups = () => {
    router.push(`/tournaments/${tournament.value.id}/groups`)
  }

  const goToBracket = () => {
    router.push(`/tournaments/${tournament.value.id}/bracket`)
  }

  const goToLeague = () => {
    router.push(`/tournaments/${tournament.value.id}/league`)
  }

  const goToStats = () => {
    router.push(`/tournaments/${tournament.value.id}/stats`)
  }

  // Métodos de utilidad
  const getStatusColor = (status) => {
    const colorMap = {
      'draft': 'grey',
      'active': 'success',
      'completed': 'primary',
      'cancelled': 'error',
    }
    return colorMap[status] || 'grey'
  }

  const getStatusText = (status) => {
    const textMap = {
      'draft': 'Borrador',
      'active': 'Activo',
      'completed': 'Completado',
      'cancelled': 'Cancelado',
    }
    return textMap[status] || 'Desconocido'
  }

  const getCompetitionTypeText = (type) => {
    const typeMap = {
      cup: 'Copa (Eliminatoria directa)',
      league: 'Liga (Todos contra todos)',
      hybrid: 'Liga + Playoffs',
      groups: 'Fase de grupos + Eliminatoria',
    }
    return typeMap[type] || 'Desconocido'
  }

  // Cargar datos al montar
  onMounted(() => {
    loadTournament()
  })
</script>

<style scoped>
.page-title {
  color: white !important;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
}

.page-subtitle {
  color: #f3f2e5 !important;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
}
</style>
