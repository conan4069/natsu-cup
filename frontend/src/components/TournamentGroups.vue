<template>
  <div class="tournament-groups">
    <!-- Header -->
    <div class="groups-header mb-6">
      <div class="d-flex align-center justify-space-between">
        <h2 class="text-h5 font-weight-bold">Fase de Grupos - {{ tournament?.name }}</h2>
        <div class="d-flex gap-2">
          <v-btn
            v-if="!groupsGenerated"
            color="primary"
            :loading="generating"
            prepend-icon="mdi-play"
            variant="elevated"
            @click="generateGroups"
          >
            Generar Grupos
          </v-btn>
          <v-btn
            v-if="groupsGenerated && !bracketReady"
            color="warning"
            prepend-icon="mdi-arrow-right"
            variant="elevated"
            @click="goToBracket"
          >
            Ir a Eliminatorias
          </v-btn>
        </div>
      </div>
    </div>

    <!-- Loading state -->
    <div v-if="loading" class="d-flex justify-center align-center" style="min-height: 400px;">
      <v-progress-circular color="primary" indeterminate size="64" />
    </div>

    <!-- Groups content -->
    <div v-else>
      <!-- No groups generated -->
      <div v-if="!groupsGenerated" class="text-center py-8">
        <v-icon class="mb-4" color="grey-lighten-1" size="64">
          mdi-account-group
        </v-icon>
        <h3 class="text-h6 text-grey-darken-1 mb-2">
          No hay grupos generados
        </h3>
        <p class="text-body-2 text-grey-darken-1 mb-4">
          Genera los grupos para comenzar la fase de grupos del torneo.
        </p>
        <v-btn
          color="primary"
          :loading="generating"
          prepend-icon="mdi-play"
          variant="elevated"
          @click="generateGroups"
        >
          Generar Grupos
        </v-btn>
      </div>

      <!-- Groups display -->
      <div v-else>
        <v-row>
          <v-col
            v-for="group in groups"
            :key="group.id"
            cols="12"
            lg="4"
            md="6"
          >
            <v-card class="group-card">
              <v-card-title class="text-h6">
                <v-icon start>mdi-account-group</v-icon>
                Grupo {{ group.name }}
              </v-card-title>
              <v-card-text>
                <!-- Teams in group -->
                <div class="teams-list mb-4">
                  <div
                    v-for="(team, index) in group.teams"
                    :key="team.id"
                    class="team-item d-flex align-center justify-space-between mb-2"
                  >
                    <div class="d-flex align-center">
                      <span class="team-position mr-3">{{ index + 1 }}</span>
                      <v-avatar class="mr-3" size="32">
                        <v-img
                          v-if="team.logo"
                          alt="Logo"
                          :src="team.logo"
                        />
                        <v-icon v-else>mdi-shield</v-icon>
                      </v-avatar>
                      <span class="team-name">{{ team.name }}</span>
                    </div>
                    <div class="team-stats">
                      <span class="text-caption text-grey-darken-1">
                        {{ team.points || 0 }} pts
                      </span>
                    </div>
                  </div>
                </div>

                <!-- Group matches -->
                <div class="matches-section">
                  <h4 class="text-subtitle-2 mb-3">Partidos del Grupo</h4>
                  <div
                    v-for="match in group.matches"
                    :key="match.id"
                    class="match-item mb-2"
                  >
                    <div class="d-flex align-center justify-space-between">
                      <div class="d-flex align-center">
                        <v-avatar class="mr-2" size="24">
                          <v-img
                            v-if="match.team1?.logo"
                            alt="Logo"
                            :src="match.team1.logo"
                          />
                          <v-icon v-else size="16">mdi-shield</v-icon>
                        </v-avatar>
                        <span class="text-body-2">{{ match.team1?.name || 'TBD' }}</span>
                      </div>

                      <div class="match-score">
                        <span v-if="match.played" class="text-body-2 font-weight-bold">
                          {{ match.team1_score || 0 }} - {{ match.team2_score || 0 }}
                        </span>
                        <span v-else class="text-caption text-grey">VS</span>
                      </div>

                      <div class="d-flex align-center">
                        <span class="text-body-2">{{ match.team2?.name || 'TBD' }}</span>
                        <v-avatar class="ml-2" size="24">
                          <v-img
                            v-if="match.team2?.logo"
                            alt="Logo"
                            :src="match.team2.logo"
                          />
                          <v-icon v-else size="16">mdi-shield</v-icon>
                        </v-avatar>
                      </div>
                    </div>

                    <div class="match-actions mt-2">
                      <v-btn
                        v-if="!match.played"
                        color="primary"
                        size="small"
                        variant="outlined"
                        @click="editMatch(match)"
                      >
                        <v-icon start>mdi-pencil</v-icon>
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
                  </div>
                </div>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>

        <!-- Group standings -->
        <v-row class="mt-6">
          <v-col cols="12">
            <v-card>
              <v-card-title class="text-h6">
                <v-icon start>mdi-chart-line</v-icon>
                Clasificación General
              </v-card-title>
              <v-card-text>
                <v-table>
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
                      v-for="(team, index) in sortedStandings"
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
    </div>

    <!-- Match result dialog -->
    <MatchResultForm
      v-model="showMatchDialog"
      :match="selectedMatch"
      @save-result="saveMatchResult"
    />
  </div>
</template>

<script setup>
  import { computed, onMounted, ref } from 'vue'
  import { useRouter } from 'vue-router'
  import { handleApiError, matchAPI, tournamentAPI } from '@/services/api'
  import MatchResultForm from './MatchResultForm.vue'

  // Props
  const props = defineProps({
    tournament: {
      type: Object,
      required: true,
    },
  })

  // Router
  const router = useRouter()

  // Estado reactivo
  const loading = ref(true)
  const generating = ref(false)
  const groups = ref([])
  const standings = ref([])
  const showMatchDialog = ref(false)
  const selectedMatch = ref(null)

  // Computed
  const groupsGenerated = computed(() => {
    return groups.value.length > 0
  })

  const bracketReady = computed(() => {
    // Verificar si todos los partidos de grupos están completados
    return groups.value.every(group =>
      group.matches.every(match => match.played),
    )
  })

  const sortedStandings = computed(() => {
    return standings.value.sort((a, b) => {
      // Ordenar por puntos, luego diferencia de goles, luego goles a favor
      if (b.points !== a.points) return b.points - a.points
      const aDiff = (a.goals_for || 0) - (a.goals_against || 0)
      const bDiff = (b.goals_for || 0) - (b.goals_against || 0)
      if (bDiff !== aDiff) return bDiff - aDiff
      return (b.goals_for || 0) - (a.goals_for || 0)
    })
  })

  // Cargar grupos
  const loadGroups = async () => {
    loading.value = true
    try {
      // Aquí necesitarías un endpoint para obtener los grupos
      // Por ahora simulamos los datos
      const response = await tournamentAPI.getTournament(props.tournament.id)
      console.log('Datos del torneo:', response.data)

      // Simular grupos (esto debería venir del backend)
      groups.value = [
        {
          id: 1,
          name: 'A',
          teams: [
            { id: 1, name: 'Equipo A1', logo: null, points: 6 },
            { id: 2, name: 'Equipo A2', logo: null, points: 3 },
            { id: 3, name: 'Equipo A3', logo: null, points: 0 },
          ],
          matches: [
            {
              id: 1,
              team1: { id: 1, name: 'Equipo A1', logo: null },
              team2: { id: 2, name: 'Equipo A2', logo: null },
              team1_score: 2,
              team2_score: 1,
              played: true,
              winner: 'team1',
            },
            {
              id: 2,
              team1: { id: 1, name: 'Equipo A1', logo: null },
              team2: { id: 3, name: 'Equipo A3', logo: null },
              team1_score: 3,
              team2_score: 0,
              played: true,
              winner: 'team1',
            },
            {
              id: 3,
              team1: { id: 2, name: 'Equipo A2', logo: null },
              team2: { id: 3, name: 'Equipo A3', logo: null },
              team1_score: null,
              team2_score: null,
              played: false,
              winner: null,
            },
          ],
        },
      ]

      // Calcular standings
      calculateStandings()
    } catch (error) {
      const errorInfo = handleApiError(error)
      console.error('Error al cargar grupos:', errorInfo.message)
    } finally {
      loading.value = false
    }
  }

  // Calcular clasificación
  const calculateStandings = () => {
    const allTeams = []

    for (const group of groups.value) {
      for (const team of group.teams) {
        const teamStats = {
          id: team.id,
          name: team.name,
          logo: team.logo,
          matches_played: 0,
          wins: 0,
          draws: 0,
          losses: 0,
          goals_for: 0,
          goals_against: 0,
          points: 0,
        }

        // Calcular estadísticas de los partidos
        for (const match of group.matches) {
          if (match.played && (match.team1?.id === team.id || match.team2?.id === team.id)) {
            teamStats.matches_played++

            const isTeam1 = match.team1?.id === team.id
            const goalsFor = isTeam1 ? match.team1_score : match.team2_score
            const goalsAgainst = isTeam1 ? match.team2_score : match.team1_score

            teamStats.goals_for += goalsFor
            teamStats.goals_against += goalsAgainst

            if (goalsFor > goalsAgainst) {
              teamStats.wins++
              teamStats.points += 3
            } else if (goalsFor === goalsAgainst) {
              teamStats.draws++
              teamStats.points += 1
            } else {
              teamStats.losses++
            }
          }
        }

        allTeams.push(teamStats)
      }
    }

    standings.value = allTeams
  }

  // Generar grupos
  const generateGroups = async () => {
    generating.value = true
    try {
      await tournamentAPI.generateGroups(props.tournament.id)
      await loadGroups()
    } catch (error) {
      const errorInfo = handleApiError(error)
      console.error('Error al generar grupos:', errorInfo.message)
    } finally {
      generating.value = false
    }
  }

  // Editar partido
  const editMatch = match => {
    selectedMatch.value = match
    showMatchDialog.value = true
  }

  // Guardar resultado del partido
  const saveMatchResult = async result => {
    try {
      await matchAPI.markMatchAsPlayed(result.matchId, {
        played: true,
        goals: {
          [result.team1Id]: result.team1Score,
          [result.team2Id]: result.team2Score,
        },
      })

      // Recargar grupos
      await loadGroups()
    } catch (error) {
      const errorInfo = handleApiError(error)
      console.error('Error al guardar resultado:', errorInfo.message)
    }
  }

  // Ir a eliminatorias
  const goToBracket = () => {
    router.push(`/tournaments/${props.tournament.id}/bracket`)
  }

  // Cargar datos al montar
  onMounted(() => {
    loadGroups()
  })
</script>

<style scoped>
.group-card {
  height: 100%;
}

.team-item {
  padding: 8px;
  border-radius: 8px;
  transition: background-color 0.2s ease;
}

.team-item:hover {
  background-color: rgba(var(--v-theme-primary), 0.1);
}

.team-position {
  font-weight: bold;
  color: var(--v-theme-primary);
  min-width: 20px;
}

.match-item {
  padding: 8px;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  background-color: #fafafa;
}

.match-score {
  font-weight: bold;
  color: var(--v-theme-primary);
}

.qualified {
  background-color: rgba(var(--v-theme-success), 0.1);
}

.v-table th {
  font-weight: bold;
  background-color: rgba(var(--v-theme-primary), 0.1);
}
</style>
