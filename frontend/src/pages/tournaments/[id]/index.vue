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
              color="white"
              icon="mdi-arrow-left"
              variant="text"
              @click="goBack"
            />
            <div class="flex-grow-1">
              <h1 class="text-h4 font-weight-bold mb-2 page-title">{{ tournament.name }}</h1>
              <p class="text-body-1 page-subtitle">
                {{ tournament.description || 'Torneo de FIFA' }}
              </p>
            </div>
            <div class="d-flex justify-center" style="gap: 10px;">
              <v-btn
                v-if="!tournamentHasMatches"
                color="blue-darken-2"
                prepend-icon="mdi-pencil"
                rounded="xl"
                variant="elevated"
                @click="editTournament"
              >
                Editar
              </v-btn>
              <v-btn
                v-else
                color="blue-darken-2"
                prepend-icon="mdi-pencil"
                rounded="xl"
                variant="outlined"
                @click="editTournament"
              >
                Editar Reglas
              </v-btn>
              <v-btn
                color="red-darken-2"
                prepend-icon="mdi-delete"
                rounded="xl"
                variant="elevated"
                @click="deleteTournament"
              >
                Eliminar
              </v-btn>
            </div>
          </div>
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
              <!-- Mostrar pestaña de grupos solo si el torneo tiene fase de grupos -->
              <v-tab v-if="showGroupsTab" value="groups">
                <v-icon start>mdi-account-group</v-icon>
                Grupos
              </v-tab>
              <!-- Mostrar pestaña de eliminatoria solo si el torneo tiene eliminatoria -->
              <v-tab v-if="showBracketTab" value="bracket">
                <v-icon start>mdi-trophy</v-icon>
                Eliminatoria
              </v-tab>
              <!-- Mostrar pestaña de liga solo si el torneo es de tipo liga o híbrido -->
              <v-tab v-if="showLeagueTab" value="league">
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
                  <TournamentOverview
                    :tournament="tournament"
                    @edit-tournament="editTournament"
                    @go-to-bracket="goToBracket"
                    @go-to-groups="goToGroups"
                    @go-to-league="goToLeague"
                    @go-to-stats="goToStats"
                  />
                </v-card-text>
              </v-window-item>

              <v-window-item value="teams">
                <v-card-text class="pa-6">
                  <TournamentTeams
                    :tournament-id="tournament.id"
                    @teams-updated="onTeamsUpdated"
                  />
                </v-card-text>
              </v-window-item>

              <v-window-item v-if="showGroupsTab" value="groups">
                <v-card-text class="pa-6">
                  <TournamentGroupsOverview
                    :tournament="tournament"
                    @go-to-groups="goToGroups"
                  />
                </v-card-text>
              </v-window-item>

              <v-window-item v-if="showBracketTab" value="bracket">
                <v-card-text class="pa-6">
                  <TournamentBracketOverview
                    :tournament="tournament"
                    @go-to-bracket="goToBracket"
                  />
                </v-card-text>
              </v-window-item>

              <v-window-item v-if="showLeagueTab" value="league">
                <v-card-text class="pa-6">
                  <TournamentLeagueOverview
                    :tournament="tournament"
                    @go-to-league="goToLeague"
                  />
                </v-card-text>
              </v-window-item>

              <v-window-item value="stats">
                <v-card-text class="pa-6">
                  <TournamentStatsOverview
                    :tournament="tournament"
                    @go-to-stats="goToStats"
                  />
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
  import { computed, onMounted, ref } from 'vue'
  import { useRoute, useRouter } from 'vue-router'
  import TournamentBracketOverview from '@/components/TournamentBracketOverview.vue'
  import TournamentGroupsOverview from '@/components/TournamentGroupsOverview.vue'
  import TournamentLeagueOverview from '@/components/TournamentLeagueOverview.vue'
  import TournamentOverview from '@/components/TournamentOverview.vue'
  import TournamentStatsOverview from '@/components/TournamentStatsOverview.vue'
  import TournamentTeams from '@/components/TournamentTeams.vue'
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

  // Computed properties para mostrar/ocultar pestañas
  const showGroupsTab = computed(() => {
    return tournament.value?.has_group_stage === true
  })

  const showBracketTab = computed(() => {
    return tournament.value?.has_knockout === true
  })

  const showLeagueTab = computed(() => {
    return tournament.value?.competition_type === 'league'
      || tournament.value?.competition_type === 'hybrid'
  })

  // Agregar la verificación de partidos
  const tournamentHasMatches = ref(false)

  // Cargar torneo
  const loadTournament = async () => {
    const tournamentId = route.params.id

    loading.value = true
    error.value = null

    try {
      const response = await tournamentAPI.getTournament(tournamentId)
      tournament.value = response.data

      // Verificar si hay partidos generados
      try {
        const matchesResponse = await tournamentAPI.getTournamentMatches(tournamentId)
        tournamentHasMatches.value = matchesResponse.data.length > 0
      } catch {
        tournamentHasMatches.value = false
      }
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

  // Método para manejar actualizaciones de equipos
  const onTeamsUpdated = () => {
    console.log('Equipos actualizados')
    // Aquí podrías recargar datos del torneo si es necesario
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
