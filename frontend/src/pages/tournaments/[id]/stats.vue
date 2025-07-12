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

    <!-- Tournament statistics -->
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
                Estadísticas del Torneo
              </p>
            </div>
          </div>
        </v-col>
      </v-row>

      <!-- Statistics overview -->
      <v-row class="mb-6">
        <v-col cols="12" md="3" sm="6">
          <v-card class="stat-card">
            <v-card-text class="text-center">
              <v-icon class="mb-3" color="primary" size="48">mdi-account-group</v-icon>
              <div class="text-h4 font-weight-bold text-primary mb-2">
                {{ stats.totalTeams }}
              </div>
              <div class="text-body-2 text-grey-darken-1">
                Equipos Participando
              </div>
            </v-card-text>
          </v-card>
        </v-col>

        <v-col cols="12" md="3" sm="6">
          <v-card class="stat-card">
            <v-card-text class="text-center">
              <v-icon class="mb-3" color="success" size="48">mdi-soccer</v-icon>
              <div class="text-h4 font-weight-bold text-success mb-2">
                {{ stats.totalMatches }}
              </div>
              <div class="text-body-2 text-grey-darken-1">
                Partidos Jugados
              </div>
            </v-card-text>
          </v-card>
        </v-col>

        <v-col cols="12" md="3" sm="6">
          <v-card class="stat-card">
            <v-card-text class="text-center">
              <v-icon class="mb-3" color="warning" size="48">mdi-trophy</v-icon>
              <div class="text-h4 font-weight-bold text-warning mb-2">
                {{ stats.totalGoals }}
              </div>
              <div class="text-body-2 text-grey-darken-1">
                Goles Marcados
              </div>
            </v-card-text>
          </v-card>
        </v-col>

        <v-col cols="12" md="3" sm="6">
          <v-card class="stat-card">
            <v-card-text class="text-center">
              <v-icon class="mb-3" color="info" size="48">mdi-chart-line</v-icon>
              <div class="text-h4 font-weight-bold text-info mb-2">
                {{ stats.avgGoalsPerMatch }}
              </div>
              <div class="text-body-2 text-grey-darken-1">
                Promedio Goles/Partido
              </div>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>

      <!-- Team standings -->
      <v-row>
        <v-col cols="12">
          <v-card>
            <v-card-title class="text-h6">
              <v-icon start>mdi-trophy</v-icon>
              Clasificación del Torneo
            </v-card-title>
            <v-card-text>
              <div v-if="teamStandings.length === 0" class="text-center py-8">
                <v-icon class="mb-4" color="grey-lighten-1" size="48">
                  mdi-trophy
                </v-icon>
                <h4 class="text-h6 text-grey-darken-1 mb-2">
                  No hay estadísticas disponibles
                </h4>
                <p class="text-body-2 text-grey-darken-1">
                  Las estadísticas aparecerán aquí cuando se jueguen partidos.
                </p>
              </div>
              <v-table v-else>
                <thead>
                  <tr>
                    <th>Pos</th>
                    <th>Equipo</th>
                    <th>PJ</th>
                    <th>PG</th>
                    <th>PE</th>
                    <th>PP</th>
                    <th>GF</th>
                    <th>GC</th>
                    <th>DG</th>
                    <th>Pts</th>
                  </tr>
                </thead>
                <tbody>
                  <tr
                    v-for="(team, index) in teamStandings"
                    :key="team.id"
                    :class="{ 'qualified': index < 2 }"
                  >
                    <td>{{ index + 1 }}</td>
                    <td>
                      <div class="d-flex align-center">
                        <v-avatar class="mr-2" size="24">
                          <v-img
                            v-if="team.logo"
                            alt="Logo"
                            :src="team.logo"
                          />
                          <v-icon v-else>mdi-shield</v-icon>
                        </v-avatar>
                        {{ team.name }}
                      </div>
                    </td>
                    <td>{{ team.matches_played || 0 }}</td>
                    <td>{{ team.wins || 0 }}</td>
                    <td>{{ team.draws || 0 }}</td>
                    <td>{{ team.losses || 0 }}</td>
                    <td>{{ team.goals_for || 0 }}</td>
                    <td>{{ team.goals_against || 0 }}</td>
                    <td>{{ (team.goals_for || 0) - (team.goals_against || 0) }}</td>
                    <td class="font-weight-bold">{{ team.points || 0 }}</td>
                  </tr>
                </tbody>
              </v-table>
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
  const matches = ref([])
  const teamEntries = ref([])
  const loading = ref(true)
  const error = ref(null)

  // Computed
  const stats = computed(() => {
    // Asegurar que matches.value sea un array
    const matchesArray = Array.isArray(matches.value) ? matches.value : []

    const totalTeams = teamEntries.value.length
    const totalMatches = matchesArray.filter(m => m.played).length
    const totalGoals = matchesArray.reduce((total, m) => {
      if (m.played && m.goals) {
        return total + Object.values(m.goals).reduce((sum, goals) => sum + goals, 0)
      }
      return total
    }, 0)
    const avgGoalsPerMatch = totalMatches > 0 ? (totalGoals / totalMatches).toFixed(1) : 0

    return {
      totalTeams,
      totalMatches,
      totalGoals,
      avgGoalsPerMatch,
    }
  })

  const teamStandings = computed(() => {
    const standings = []

    // Asegurar que teamEntries.value sea un array
    const entriesArray = Array.isArray(teamEntries.value) ? teamEntries.value : []

    for (const entry of entriesArray) {
      if (!entry.assigned_team) continue

      const teamStats = {
        id: entry.assigned_team.id,
        name: entry.assigned_team.name,
        logo: entry.assigned_team.logo,
        matches_played: entry.assigned_team.stats?.total_matches || 0,
        wins: entry.assigned_team.stats?.wins || 0,
        draws: entry.assigned_team.stats?.draws || 0,
        losses: entry.assigned_team.stats?.losses || 0,
        goals_for: entry.assigned_team.stats?.goals_scored || 0,
        goals_against: entry.assigned_team.stats?.goals_conceded || 0,
        points: (entry.assigned_team.stats?.wins || 0) * 3 + (entry.assigned_team.stats?.draws || 0),
      }

      standings.push(teamStats)
    }

    return standings.sort((a, b) => b.points - a.points)
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
      try {
        const matchesResponse = await matchAPI.getTournamentMatches(tournamentId)
        // Asegurar que matches sea siempre un array
        matches.value = matchesResponse.data?.matches || matchesResponse.data || []
        console.log('Partidos del torneo cargados:', matches.value)
      } catch (matchesError) {
        console.error('Error al cargar partidos:', matchesError)
        matches.value = []
      }

      // Cargar entradas de equipos
      try {
        const entriesResponse = await tournamentAPI.getTeamEntries(tournamentId)
        teamEntries.value = entriesResponse.data || []
        console.log('Entradas de equipos cargadas:', teamEntries.value)
      } catch (entriesError) {
        console.error('Error al cargar entradas:', entriesError)
        teamEntries.value = []
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
    router.push(`/tournaments/${route.params.id}`)
  }

  // Cargar datos al montar el componente
  onMounted(() => {
    loadTournament()
  })
</script>

<style scoped>
.stat-card {
  transition: transform 0.2s ease;
}

.stat-card:hover {
  transform: translateY(-2px);
}

.qualified {
  background-color: rgba(var(--v-theme-success), 0.1);
}

.v-table th {
  font-weight: bold;
  background-color: rgba(var(--v-theme-primary), 0.1);
}
</style>
