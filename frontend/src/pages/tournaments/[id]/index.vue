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
              <h1 class="text-h4 font-weight-bold mb-2">{{ tournament.name }}</h1>
              <p class="text-body-1 text-grey-darken-1">
                {{ tournament.description || 'Torneo de fútbol' }}
              </p>
            </div>
            <div class="d-flex gap-2">
              <v-btn
                color="primary"
                prepend-icon="mdi-pencil"
                variant="outlined"
                @click="editTournament"
              >
                Editar
              </v-btn>
              <v-btn
                color="error"
                prepend-icon="mdi-delete"
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
                    <span class="text-body-2 text-grey-darken-1">Estado:</span>
                    <div>
                      <v-chip
                        :color="tournament.status === 'completed' ? 'success' : 'warning'"
                        size="small"
                        variant="outlined"
                      >
                        {{ tournament.status === 'completed' ? 'Completado' : 'En progreso' }}
                      </v-chip>
                    </div>
                  </div>
                  <div class="mb-3">
                    <span class="text-body-2 text-grey-darken-1">Fecha de creación:</span>
                    <div class="font-weight-medium">
                      {{ new Date(tournament.created_at).toLocaleDateString() }}
                    </div>
                  </div>
                </v-col>
              </v-row>
            </v-card-text>
          </v-card>
        </v-col>

        <v-col cols="12" md="4">
          <v-card>
            <v-card-title class="text-h6">
              <v-icon start>mdi-trophy</v-icon>
              Acciones
            </v-card-title>
            <v-card-text>
              <div class="d-flex flex-column gap-3">
                <!-- Mostrar botones según el tipo de competición -->
                <v-btn
                  v-if="shouldShowGroups"
                  block
                  color="primary"
                  prepend-icon="mdi-play"
                  variant="elevated"
                  @click="goToGroups"
                >
                  Fase de Grupos
                </v-btn>

                <v-btn
                  v-if="shouldShowLeague"
                  block
                  color="primary"
                  prepend-icon="mdi-chart-line"
                  variant="elevated"
                  @click="goToLeague"
                >
                  Liga
                </v-btn>

                <v-btn
                  v-if="shouldShowBracket"
                  block
                  color="warning"
                  prepend-icon="mdi-trophy"
                  variant="outlined"
                  @click="goToBracket"
                >
                  Fase Eliminatoria
                </v-btn>

                <v-btn
                  block
                  color="secondary"
                  prepend-icon="mdi-account-group"
                  variant="outlined"
                  @click="manageTeams"
                >
                  Gestionar Equipos
                </v-btn>

                <v-btn
                  block
                  color="info"
                  prepend-icon="mdi-chart-line"
                  variant="outlined"
                  @click="viewStats"
                >
                  Ver Estadísticas
                </v-btn>
              </div>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>

      <!-- Recent matches -->
      <v-row class="mt-6">
        <v-col cols="12">
          <v-card>
            <v-card-title class="text-h6">
              <v-icon start>mdi-soccer</v-icon>
              Partidos Recientes
            </v-card-title>
            <v-card-text>
              <div v-if="recentMatches.length === 0" class="text-center py-8">
                <v-icon class="mb-4" color="grey-lighten-1" size="48">
                  mdi-soccer
                </v-icon>
                <h4 class="text-h6 text-grey-darken-1 mb-2">
                  No hay partidos registrados
                </h4>
                <p class="text-body-2 text-grey-darken-1">
                  Los partidos aparecerán aquí cuando se generen las fases eliminatorias.
                </p>
              </div>
              <v-list v-else>
                <v-list-item
                  v-for="match in recentMatches"
                  :key="match.id"
                  :subtitle="`${match.stage} • ${match.played ? 'Completado' : 'Pendiente'}`"
                  :title="`${match.team1?.name || 'TBD'} vs ${match.team2?.name || 'TBD'}`"
                >
                  <template #prepend>
                    <v-icon color="primary">mdi-soccer</v-icon>
                  </template>
                  <template #append>
                    <v-chip
                      :color="match.played ? 'success' : 'warning'"
                      size="small"
                      variant="outlined"
                    >
                      {{ match.played ? 'Completado' : 'Pendiente' }}
                    </v-chip>
                  </template>
                </v-list-item>
              </v-list>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </div>
  </v-container>
</template>

<script setup>
  import { computed, onMounted, ref } from 'vue'
  import { useRoute, useRouter } from 'vue-router'
  import { handleApiError, matchAPI, tournamentAPI } from '@/services/api'

  // Router y Route
  const router = useRouter()
  const route = useRoute()

  // Estado reactivo
  const tournament = ref(null)
  const recentMatches = ref([])
  const loading = ref(true)
  const error = ref(null)

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

      // Cargar partidos recientes
      try {
        const matchesResponse = await matchAPI.getTournamentMatches(tournamentId)
        recentMatches.value = matchesResponse.data.slice(0, 5) // Solo los últimos 5
        console.log('Partidos recientes cargados:', recentMatches.value)
      } catch (matchesError) {
        console.error('Error al cargar partidos:', matchesError)
        recentMatches.value = []
      }
    } catch (error_) {
      const errorInfo = handleApiError(error_)
      error.value = errorInfo.message
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

  const deleteTournament = async () => {
    if (!confirm('¿Estás seguro de que quieres eliminar este torneo?')) return

    try {
      await tournamentAPI.deleteTournament(tournament.value.id)
      router.push('/tournaments')
    } catch (error_) {
      const errorInfo = handleApiError(error_)
      console.error('Error al eliminar torneo:', errorInfo.message)
    }
  }

  // Agregar las funciones de navegación faltantes
  const manageTeams = () => {
    router.push(`/tournaments/${route.params.id}/teams`)
  }

  const viewStats = () => {
    router.push(`/tournaments/${route.params.id}/stats`)
  }

  const goToGroups = () => {
    router.push(`/tournaments/${route.params.id}/groups`)
  }

  const goToBracket = () => {
    router.push(`/tournaments/${route.params.id}/bracket`)
  }

  const goToLeague = () => {
    router.push(`/tournaments/${route.params.id}/league`)
  }

  // Cargar datos al montar el componente
  onMounted(() => {
    loadTournament()
  })

  // Agregar métodos para manejar estados
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

  // Agregar computed properties
  const shouldShowGroups = computed(() => {
    return tournament.value?.competition_type === 'groups' || tournament.value?.has_group_stage
  })

  const shouldShowLeague = computed(() => {
    return tournament.value?.competition_type === 'league' || tournament.value?.competition_type === 'hybrid'
  })

  const shouldShowBracket = computed(() => {
    return tournament.value?.competition_type === 'cup' || tournament.value?.has_knockout
  })
</script>

<style scoped>
/* Estilos específicos si son necesarios */
</style>
