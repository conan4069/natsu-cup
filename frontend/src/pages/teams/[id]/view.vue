<template>
  <v-container fluid>
    <!-- Loading state -->
    <div v-if="loading" class="d-flex justify-center align-center" style="min-height: 400px;">
      <v-progress-circular color="primary" indeterminate size="64" />
    </div>

    <!-- Error state -->
    <div v-else-if="error" class="text-center py-8">
      <v-icon class="mb-4" color="error" size="64">mdi-alert-circle</v-icon>
      <h3 class="text-h6 text-grey-darken-1 mb-2">Error al cargar equipo</h3>
      <p class="text-body-2 text-grey-darken-1 mb-4">{{ error }}</p>
      <v-btn color="primary" @click="loadTeam">Reintentar</v-btn>
    </div>

    <!-- Team details -->
    <div v-else-if="team">
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
            <div class="d-flex align-center">
              <v-avatar class="mr-4" size="80">
                <v-img
                  v-if="team.logo"
                  alt="Logo del equipo"
                  :src="team.logo"
                />
                <v-icon v-else color="grey" size="40">
                  mdi-shield
                </v-icon>
              </v-avatar>
              <div>
                <h1 class="text-h4 font-weight-bold mb-2">{{ team.name }}</h1>
                <p class="text-body-1 text-grey-darken-1">
                  Equipo del campeonato Natsu Cup
                </p>
              </div>
            </div>
          </div>
        </v-col>
      </v-row>

      <!-- Content -->
      <v-row>
        <!-- Team info card -->
        <v-col cols="12" md="6">
          <v-card>
            <v-card-title class="text-h6">
              <v-icon start>mdi-shield-account</v-icon>
              Información del Equipo
            </v-card-title>
            <v-card-text>
              <TeamForm
                mode="view"
                :team="team"
                readonly
              />
            </v-card-text>
            <v-card-actions>
              <v-spacer />
              <v-btn
                color="warning"
                prepend-icon="mdi-pencil"
                variant="outlined"
                @click="editTeam"
              >
                Editar
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-col>

        <!-- Statistics card -->
        <v-col cols="12" md="6">
          <v-card>
            <v-card-title class="text-h6">
              <v-icon start>mdi-chart-line</v-icon>
              Estadísticas
              <v-progress-circular
                v-if="loadingStats"
                indeterminate
                size="20"
                class="ml-2"
              />
            </v-card-title>
            <v-card-text>
              <v-row>
                <v-col cols="6">
                  <div class="text-center">
                    <div class="text-h4 font-weight-bold text-primary mb-2">
                      {{ stats.total_tournaments || 0 }}
                    </div>
                    <div class="text-caption text-grey-darken-1">
                      Torneos Participados
                    </div>
                  </div>
                </v-col>
                <v-col cols="6">
                  <div class="text-center">
                    <div class="text-h4 font-weight-bold text-success mb-2">
                      {{ stats.total_matches || 0 }}
                    </div>
                    <div class="text-caption text-grey-darken-1">
                      Partidos Jugados
                    </div>
                  </div>
                </v-col>
                <v-col cols="6">
                  <div class="text-center">
                    <div class="text-h4 font-weight-bold text-warning mb-2">
                      {{ stats.wins || 0 }}
                    </div>
                    <div class="text-caption text-grey-darken-1">
                      Victorias
                    </div>
                  </div>
                </v-col>
                <v-col cols="6">
                  <div class="text-center">
                    <div class="text-h4 font-weight-bold text-error mb-2">
                      {{ stats.losses || 0 }}
                    </div>
                    <div class="text-caption text-grey-darken-1">
                      Derrotas
                    </div>
                  </div>
                </v-col>
                <v-col cols="6">
                  <div class="text-center">
                    <div class="text-h4 font-weight-bold text-info mb-2">
                      {{ stats.draws || 0 }}
                    </div>
                    <div class="text-caption text-grey-darken-1">
                      Empates
                    </div>
                  </div>
                </v-col>
                <v-col cols="6">
                  <div class="text-center">
                    <div class="text-h4 font-weight-bold text-success mb-2">
                      {{ stats.win_rate || 0 }}%
                    </div>
                    <div class="text-caption text-grey-darken-1">
                      % Victorias
                    </div>
                  </div>
                </v-col>
              </v-row>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>

      <!-- Recent tournaments -->
      <v-row class="mt-6">
        <v-col cols="12">
          <v-card>
            <v-card-title class="text-h6">
              <v-icon start>mdi-trophy</v-icon>
              Torneos Recientes
            </v-card-title>
            <v-card-text>
              <div v-if="recentTournaments.length === 0" class="text-center py-8">
                <v-icon class="mb-4" color="grey-lighten-1" size="48">
                  mdi-trophy-outline
                </v-icon>
                <h4 class="text-h6 text-grey-darken-1 mb-2">
                  No hay torneos registrados
                </h4>
                <p class="text-body-2 text-grey-darken-1">
                  Este equipo aún no ha participado en ningún torneo.
                </p>
              </div>
              <v-list v-else>
                <v-list-item
                  v-for="tournament in recentTournaments"
                  :key="tournament.id"
                  :subtitle="`${tournament.format} • ${tournament.matches_played} partidos • ${tournament.win_rate}% victorias`"
                  :title="tournament.name"
                >
                  <template #prepend>
                    <v-icon color="primary">mdi-trophy</v-icon>
                  </template>
                  <template #append>
                    <v-chip
                      :color="tournament.status === 'completed' ? 'success' : 'warning'"
                      size="small"
                      variant="outlined"
                    >
                      {{ tournament.status === 'completed' ? 'Completado' : 'Registrado' }}
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
  import { onMounted, ref } from 'vue'
  import { useRoute, useRouter } from 'vue-router'
  import TeamForm from '@/components/TeamForm.vue'
  import { handleApiError, teamAPI } from '@/services/api'

  // Router y Route
  const router = useRouter()
  const route = useRoute()

  // Estado reactivo
  const team = ref(null)
  const loading = ref(true)
  const loadingStats = ref(false)
  const loadingTournaments = ref(false)
  const error = ref(null)
  const stats = ref({
    total_tournaments: 0,
    total_matches: 0,
    wins: 0,
    losses: 0,
    draws: 0,
    win_rate: 0,
    loss_rate: 0,
    draw_rate: 0,
    total_points: 0
  })
  const recentTournaments = ref([])

  // Cargar equipo
  const loadTeam = async () => {
    const teamId = route.params.id

    loading.value = true
    error.value = null

    try {
      console.log('Cargando equipo con ID:', teamId)

      // Cargar datos del equipo
      const teamResponse = await teamAPI.getTeam(teamId)
      team.value = teamResponse.data
      console.log('Datos del equipo cargados:', team.value)

      // Cargar estadísticas del equipo
      try {
        loadingStats.value = true
        const statsResponse = await teamAPI.getTeamStats(teamId)
        stats.value = statsResponse.data
        console.log('Estadísticas del equipo cargadas:', stats.value)
      } catch (statsError) {
        console.error('Error al cargar estadísticas:', statsError)
        // No fallar completamente si las estadísticas fallan
        stats.value = {
          total_tournaments: 0,
          total_matches: 0,
          wins: 0,
          losses: 0,
          draws: 0,
          win_rate: 0,
          loss_rate: 0,
          draw_rate: 0,
          total_points: 0
        }
      } finally {
        loadingStats.value = false
      }

      // Cargar torneos del equipo
      try {
        loadingTournaments.value = true
        const tournamentsResponse = await teamAPI.getTeamTournaments(teamId)
        recentTournaments.value = tournamentsResponse.data.tournaments
        console.log('Torneos del equipo cargados:', recentTournaments.value)
      } catch (tournamentsError) {
        console.error('Error al cargar torneos:', tournamentsError)
        // No fallar completamente si los torneos fallan
        recentTournaments.value = []
      } finally {
        loadingTournaments.value = false
      }
    } catch (error_) {
      const errorInfo = handleApiError(error_)
      error.value = errorInfo.message
      console.error('Error al cargar equipo:', errorInfo.message)
    } finally {
      loading.value = false
    }
  }

  // Navegación
  const goBack = () => {
    router.push('/teams')
  }

  const editTeam = () => {
    router.push(`/teams/${team.value.id}/edit`)
  }

  // Cargar datos al montar el componente
  onMounted(() => {
    loadTeam()
  })
</script>

<style scoped>
/* Estilos específicos si son necesarios */
</style>
