<template>
  <v-parallax height="100vh" src="@/assets/fondo2.jpg">
    <v-container fluid>

      <!-- Header -->
      <v-row class="mb-6">
        <v-col cols="12">
          <div class="text-center">
            <v-img
              alt="Natsu Cup Logo"
              class="mx-auto mb-4"
              max-width="200"
              src="@/assets/LogoCup.png"
            />
            <h1 class="text-h3 font-weight-bold mb-2">Natsu Cup</h1>
            <p class="text-h6 text-grey-darken-1">
              Sistema de Gestión de Torneos de Fútbol
            </p>
          </div>
        </v-col>
      </v-row>

      <!-- Loading state -->
      <div v-if="loading" class="d-flex justify-center align-center" style="min-height: 400px;">
        <v-progress-circular color="primary" indeterminate size="64" />
      </div>

      <!-- Dashboard content -->
      <div v-else>
        <!-- Statistics cards -->
        <v-row class="mb-6">
          <v-col cols="12" md="3" sm="6">
            <v-card class="stat-card">
              <v-card-text class="text-center">
                <v-icon class="mb-3" color="primary" size="48">mdi-trophy</v-icon>
                <div class="text-h4 font-weight-bold text-primary mb-2">
                  {{ stats.totalTournaments }}
                </div>
                <div class="text-body-2 text-grey-darken-1">
                  Torneos Creados
                </div>
              </v-card-text>
            </v-card>
          </v-col>

          <v-col cols="12" md="3" sm="6">
            <v-card class="stat-card">
              <v-card-text class="text-center">
                <v-icon class="mb-3" color="success" size="48">mdi-account-group</v-icon>
                <div class="text-h4 font-weight-bold text-success mb-2">
                  {{ stats.totalPlayers }}
                </div>
                <div class="text-body-2 text-grey-darken-1">
                  Jugadores Registrados
                </div>
              </v-card-text>
            </v-card>
          </v-col>

          <v-col cols="12" md="3" sm="6">
            <v-card class="stat-card">
              <v-card-text class="text-center">
                <v-icon class="mb-3" color="warning" size="48">mdi-shield</v-icon>
                <div class="text-h4 font-weight-bold text-warning mb-2">
                  {{ stats.totalTeams }}
                </div>
                <div class="text-body-2 text-grey-darken-1">
                  Equipos Creados
                </div>
              </v-card-text>
            </v-card>
          </v-col>

          <v-col cols="12" md="3" sm="6">
            <v-card class="stat-card">
              <v-card-text class="text-center">
                <v-icon class="mb-3" color="info" size="48">mdi-soccer</v-icon>
                <div class="text-h4 font-weight-bold text-info mb-2">
                  {{ stats.totalMatches }}
                </div>
                <div class="text-body-2 text-grey-darken-1">
                  Partidos Jugados
                </div>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>

        <!-- Recent activity and quick actions -->
        <v-row>
          <!-- Recent tournaments -->
          <v-col cols="12" md="8">
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
                    No hay torneos creados
                  </h4>
                  <p class="text-body-2 text-grey-darken-1 mb-4">
                    Crea tu primer torneo para comenzar
                  </p>
                  <v-btn
                    color="primary"
                    prepend-icon="mdi-plus"
                    variant="elevated"
                    @click="createTournament"
                  >
                    Crear Torneo
                  </v-btn>
                </div>
                <v-list v-else>
                  <v-list-item
                    v-for="tournament in recentTournaments"
                    :key="tournament.id"
                    :subtitle="`${tournament.format} • ${tournament.team_count || 0} equipos`"
                    :title="tournament.name"
                    @click="viewTournament(tournament.id)"
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
                        {{ tournament.status === 'completed' ? 'Completado' : 'En progreso' }}
                      </v-chip>
                    </template>
                  </v-list-item>
                </v-list>
              </v-card-text>
            </v-card>
          </v-col>

          <!-- Quick actions -->
          <v-col cols="12" md="4">
            <v-card>
              <v-card-title class="text-h6">
                <v-icon start>mdi-lightning-bolt</v-icon>
                Acciones Rápidas
              </v-card-title>
              <v-card-text>
                <div class="d-flex flex-column gap-3">
                  <v-btn
                    block
                    color="primary"
                    prepend-icon="mdi-plus"
                    variant="elevated"
                    @click="createTournament"
                  >
                    Crear Torneo
                  </v-btn>

                  <v-btn
                    block
                    color="success"
                    prepend-icon="mdi-account-plus"
                    variant="outlined"
                    @click="createPlayer"
                  >
                    Agregar Jugador
                  </v-btn>

                  <v-btn
                    block
                    color="warning"
                    prepend-icon="mdi-shield-plus"
                    variant="outlined"
                    @click="createTeam"
                  >
                    Crear Equipo
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

        <!-- Top players and teams -->
        <v-row class="mt-6">
          <v-col cols="12" md="6">
            <v-card>
              <v-card-title class="text-h6">
                <v-icon start>mdi-account-star</v-icon>
                Jugadores Destacados
              </v-card-title>
              <v-card-text>
                <div v-if="topPlayers.length === 0" class="text-center py-4">
                  <p class="text-body-2 text-grey-darken-1">
                    No hay jugadores registrados
                  </p>
                </div>
                <v-list v-else>
                  <v-list-item
                    v-for="(player, index) in topPlayers"
                    :key="player.id"
                    :subtitle="`${player.total_matches} partidos • ${player.win_rate}% victorias`"
                    :title="player.display_name"
                  >
                    <template #prepend>
                      <v-avatar class="mr-3" size="32">
                        <v-img
                          v-if="player.avatar"
                          alt="Avatar"
                          :src="player.avatar"
                        />
                        <v-icon v-else>mdi-account</v-icon>
                      </v-avatar>
                    </template>
                    <template #append>
                      <v-chip
                        :color="index === 0 ? 'warning' : 'grey'"
                        size="small"
                        variant="outlined"
                      >
                        #{{ index + 1 }}
                      </v-chip>
                    </template>
                  </v-list-item>
                </v-list>
              </v-card-text>
            </v-card>
          </v-col>

          <v-col cols="12" md="6">
            <v-card>
              <v-card-title class="text-h6">
                <v-icon start>mdi-shield-star</v-icon>
                Equipos Destacados
              </v-card-title>
              <v-card-text>
                <div v-if="topTeams.length === 0" class="text-center py-4">
                  <p class="text-body-2 text-grey-darken-1">
                    No hay equipos registrados
                  </p>
                </div>
                <v-list v-else>
                  <v-list-item
                    v-for="(team, index) in topTeams"
                    :key="team.id"
                    :subtitle="`${team.total_matches} partidos • ${team.win_rate}% victorias`"
                    :title="team.name"
                  >
                    <template #prepend>
                      <v-avatar class="mr-3" size="32">
                        <v-img
                          v-if="team.logo"
                          alt="Logo"
                          :src="team.logo"
                        />
                        <v-icon v-else>mdi-shield</v-icon>
                      </v-avatar>
                    </template>
                    <template #append>
                      <v-chip
                        :color="index === 0 ? 'warning' : 'grey'"
                        size="small"
                        variant="outlined"
                      >
                        #{{ index + 1 }}
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
  </v-parallax>
</template>

<script setup>
  import { onMounted, ref } from 'vue'
  import { useRouter } from 'vue-router'
  import { samplePlayers, sampleTeams, sampleTournaments } from '@/data/sampleData'
  import { handleApiError, playerAPI, teamAPI, tournamentAPI } from '@/services/api'

  // Router
  const router = useRouter()

  // Estado reactivo
  const loading = ref(true)
  const stats = ref({
    totalTournaments: 0,
    totalPlayers: 0,
    totalTeams: 0,
    totalMatches: 0,
  })
  const recentTournaments = ref([])
  const topPlayers = ref([])
  const topTeams = ref([])

  // Cargar datos del dashboard
  const loadDashboard = async () => {
    loading.value = true

    try {
      // Intentar cargar datos reales primero
      try {
        const [tournamentsRes, playersRes, teamsRes] = await Promise.all([
          tournamentAPI.getTournaments(),
          playerAPI.getPlayers(),
          teamAPI.getTeams(),
        ])

        const tournaments = tournamentsRes.data
        const players = playersRes.data
        const teams = teamsRes.data

        // Calcular estadísticas
        stats.value = {
          totalTournaments: tournaments.length,
          totalPlayers: players.length,
          totalTeams: teams.length,
          totalMatches: tournaments.reduce((total, t) => total + (t.matches_count || 0), 0),
        }

        // Obtener torneos recientes
        recentTournaments.value = tournaments
          .sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
          .slice(0, 5)

        // Obtener jugadores destacados
        topPlayers.value = players
          .filter(p => p.stats)
          .sort((a, b) => (b.stats?.win_rate || 0) - (a.stats?.win_rate || 0))
          .slice(0, 5)

        // Obtener equipos destacados
        topTeams.value = teams
          .filter(t => t.stats)
          .sort((a, b) => (b.stats?.win_rate || 0) - (a.stats?.win_rate || 0))
          .slice(0, 5)
      } catch {
        console.log('API no disponible, usando datos de ejemplo')
        // Usar datos de ejemplo si la API no está disponible
        const tournaments = sampleTournaments
        const players = samplePlayers
        const teams = sampleTeams

        // Calcular estadísticas
        stats.value = {
          totalTournaments: tournaments.length,
          totalPlayers: players.length,
          totalTeams: teams.length,
          totalMatches: tournaments.reduce((total, t) => total + (t.matches_count || 0), 0),
        }

        // Obtener torneos recientes
        recentTournaments.value = tournaments
          .sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
          .slice(0, 5)

        // Obtener jugadores destacados
        topPlayers.value = players
          .filter(p => p.stats)
          .sort((a, b) => (b.stats?.win_rate || 0) - (a.stats?.win_rate || 0))
          .slice(0, 5)

        // Obtener equipos destacados
        topTeams.value = teams
          .filter(t => t.stats)
          .sort((a, b) => (b.stats?.win_rate || 0) - (a.stats?.win_rate || 0))
          .slice(0, 5)
      }
    } catch (error) {
      const errorInfo = handleApiError(error)
      console.error('Error al cargar dashboard:', errorInfo.message)
    } finally {
      loading.value = false
    }
  }

  // Navegación
  const createTournament = () => {
    router.push('/tournaments/create')
  }

  const createPlayer = () => {
    router.push('/players/create')
  }

  const createTeam = () => {
    router.push('/teams/create')
  }

  const viewStats = () => {
    // Aquí podrías navegar a una página de estadísticas detalladas
    console.log('Ver estadísticas detalladas')
  }

  const viewTournament = tournamentId => {
    router.push(`/tournaments/${tournamentId}`)
  }

  // Cargar datos al montar el componente
  onMounted(() => {
    loadDashboard()
  })
</script>

<style scoped>
.stat-card {
  transition: transform 0.2s ease;
}

.stat-card:hover {
  transform: translateY(-2px);
}

.v-list-item {
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.v-list-item:hover {
  background-color: rgba(var(--v-theme-primary), 0.1);
}
</style>
