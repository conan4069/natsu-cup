<template>
  <v-parallax class="champions-parallax" src="@/assets/fondo2.jpg">
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
            <h1 class="text-h3 font-weight-bold mb-2 page-title">Natsu Cup</h1>
            <p class="text-h6 text-black">
              Tú Liga de FIFA de confianza
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
        <v-row class="mt-6">
          <v-col cols="12" md="3" sm="6">
            <v-card class="stat-card" rounded="xl">
              <v-card-text class="text-center">
                <v-icon class="mb-3" color="primary" size="48">mdi-trophy</v-icon>
                <div class="text-h4 font-weight-bold text-primary mb-2">
                  {{ stats.totalTournaments }}
                </div>
                <div class="text-body-2 text-grey-darken-1">
                  Torneos Activos
                </div>
              </v-card-text>
            </v-card>
          </v-col>

          <v-col cols="12" md="3" sm="6">
            <v-card class="stat-card" rounded="xl">
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
            <v-card class="stat-card" rounded="xl">
              <v-card-text class="text-center">
                <v-icon class="mb-3" color="warning" size="48">mdi-shield</v-icon>
                <div class="text-h4 font-weight-bold text-warning mb-2">
                  {{ stats.totalTeams }}
                </div>
                <div class="text-body-2 text-grey-darken-1">
                  Equipos Disponibles
                </div>
              </v-card-text>
            </v-card>
          </v-col>

          <v-col cols="12" md="3" sm="6">
            <v-card class="stat-card" rounded="xl">
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
            <v-card rounded="xl">
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
                    rounded="xl"
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
            <v-card rounded="xl">
              <v-card-title class="text-h6">
                <v-icon start>mdi-lightning-bolt</v-icon>
                Atajos Rápidos
              </v-card-title>
              <v-card-text>
                <div class="d-flex flex-column" style="gap: 5px;">
                  <v-btn
                    block
                    color="primary"
                    prepend-icon="mdi-plus"
                    rounded="xl"
                    variant="elevated"
                    @click="createTournament"
                  >
                    Crear Torneo
                  </v-btn>

                  <v-btn
                    block
                    color="success"
                    prepend-icon="mdi-account-plus"
                    rounded="xl"
                    variant="elevated"
                    @click="createPlayer"
                  >
                    Agregar Jugador
                  </v-btn>

                  <v-btn
                    block
                    color="warning"
                    prepend-icon="mdi-shield-plus"
                    rounded="xl"
                    variant="elevated"
                    @click="createTeam"
                  >
                    Crear Equipo
                  </v-btn>

                  <v-btn
                    block
                    color="info"
                    prepend-icon="mdi-chart-line"
                    rounded="xl"
                    variant="elevated"
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
        <v-row>
          <!-- Top players -->
          <v-col cols="12" md="6">
            <v-card rounded="xl">
              <v-card-title class="text-h6">
                <v-icon start>mdi-account-star</v-icon>
                Mejores Jugadores
              </v-card-title>
              <v-card-text>
                <div v-if="topPlayers.length === 0" class="text-center py-8">
                  <v-icon class="mb-4" color="grey-lighten-1" size="48">
                    mdi-account-outline
                  </v-icon>
                  <h4 class="text-h6 text-grey-darken-1 mb-2">
                    No hay jugadores registrados
                  </h4>
                  <p class="text-body-2 text-grey-darken-1">
                    Los jugadores aparecerán aquí cuando se registren
                  </p>
                </div>
                <v-list v-else>
                  <v-list-item
                    v-for="(player, index) in topPlayers"
                    :key="player.id"
                    :subtitle="`${player.goals || 0} goles • ${player.assists || 0} asistencias`"
                    :title="player.display_name"
                    @click="viewPlayer(player.id)"
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
                        :color="index < 3 ? 'warning' : 'grey'"
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

          <!-- Top teams -->
          <v-col cols="12" md="6">
            <v-card rounded="xl">
              <v-card-title class="text-h6">
                <v-icon start>mdi-shield-star</v-icon>
                Mejores Equipos
              </v-card-title>
              <v-card-text>
                <div v-if="topTeams.length === 0" class="text-center py-8">
                  <v-icon class="mb-4" color="grey-lighten-1" size="48">
                    mdi-shield-outline
                  </v-icon>
                  <h4 class="text-h6 text-grey-darken-1 mb-2">
                    No hay equipos registrados
                  </h4>
                  <p class="text-body-2 text-grey-darken-1">
                    Los equipos aparecerán aquí cuando se registren
                  </p>
                </div>
                <v-list v-else>
                  <v-list-item
                    v-for="(team, index) in topTeams"
                    :key="team.id"
                    :subtitle="`${team.wins || 0} victorias • ${team.goals || 0} goles`"
                    :title="team.name"
                    @click="viewTeam(team.id)"
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
                        :color="index < 3 ? 'warning' : 'grey'"
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
  const loadDashboardData = async () => {
    loading.value = true
    try {
      // Cargar estadísticas
      const [tournamentsRes, playersRes, teamsRes] = await Promise.all([
        tournamentAPI.getTournaments(),
        playerAPI.getPlayers(),
        teamAPI.getTeams(),
      ])

      stats.value = {
        totalTournaments: tournamentsRes.data.length,
        totalPlayers: playersRes.data.length,
        totalTeams: teamsRes.data.length,
        totalMatches: 0, // TODO: Implementar contador de partidos
      }

      // Cargar torneos recientes
      recentTournaments.value = tournamentsRes.data.slice(0, 5)

      // Cargar mejores jugadores (ejemplo)
      topPlayers.value = playersRes.data.slice(0, 5).map(player => ({
        ...player,
        goals: Math.floor(Math.random() * 20),
        assists: Math.floor(Math.random() * 15),
      }))

      // Cargar mejores equipos (ejemplo)
      topTeams.value = teamsRes.data.slice(0, 5).map(team => ({
        ...team,
        wins: Math.floor(Math.random() * 10),
        goals: Math.floor(Math.random() * 50),
      }))
    } catch (error) {
      const errorInfo = handleApiError(error)
      console.error('Error al cargar datos del dashboard:', errorInfo.message)
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
    // TODO: Implementar página de estadísticas
    console.log('Ver estadísticas')
  }

  const viewTournament = id => {
    router.push(`/tournaments/${id}`)
  }

  const viewPlayer = id => {
    router.push(`/players/${id}`)
  }

  const viewTeam = id => {
    router.push(`/teams/${id}`)
  }

  // Cargar datos al montar
  onMounted(() => {
    loadDashboardData()
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

.stat-card {
  transition: transform 0.2s;
}

.stat-card:hover {
  transform: translateY(-2px);
}
</style>

<style>
.champions-parallax .v-img__img,
.champions-parallax .v-parallax__image {
  filter: brightness(0.55) blur(1.5px) saturate(1.15) !important;
  transition: filter 0.3s;
}
</style>
