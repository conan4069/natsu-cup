<template>
  <div class="tournament-stats-overview">
    <v-row>
      <!-- Estadísticas generales -->
      <v-col cols="12" md="6">
        <v-card class="mb-4" variant="outlined">
          <v-card-title class="text-h6">
            <v-icon start>mdi-chart-line</v-icon>
            Estadísticas Generales
          </v-card-title>
          <v-card-text>
            <div class="mb-3">
              <span class="text-body-2 text-grey-darken-1">Participantes:</span>
              <div class="font-weight-medium">{{ tournament.participant_count || 0 }}</div>
            </div>
            <div class="mb-3">
              <span class="text-body-2 text-grey-darken-1">Partidos jugados:</span>
              <div class="font-weight-medium">{{ stats.playedMatches }}</div>
            </div>
            <div class="mb-3">
              <span class="text-body-2 text-grey-darken-1">Partidos pendientes:</span>
              <div class="font-weight-medium">{{ stats.pendingMatches }}</div>
            </div>
            <div class="mb-3">
              <span class="text-body-2 text-grey-darken-1">Total de partidos:</span>
              <div class="font-weight-medium">{{ stats.totalMatches }}</div>
            </div>
            <div class="mb-3">
              <span class="text-body-2 text-grey-darken-1">Progreso general:</span>
              <div class="mt-1">
                <v-progress-linear
                  :model-value="stats.progressPercentage"
                  color="primary"
                  height="8"
                  rounded
                />
                <div class="text-caption text-grey-darken-1 mt-1">
                  {{ stats.progressPercentage }}% completado
                </div>
              </div>
            </div>
          </v-card-text>
        </v-card>
      </v-col>

      <!-- Estadísticas de goles -->
      <v-col cols="12" md="6">
        <v-card class="mb-4" variant="outlined">
          <v-card-title class="text-h6">
            <v-icon start>mdi-soccer</v-icon>
            Estadísticas de Goles
          </v-card-title>
          <v-card-text>
            <div class="mb-3">
              <span class="text-body-2 text-grey-darken-1">Total de goles:</span>
              <div class="font-weight-medium">{{ stats.totalGoals }}</div>
            </div>
            <div class="mb-3">
              <span class="text-body-2 text-grey-darken-1">Promedio por partido:</span>
              <div class="font-weight-medium">{{ stats.averageGoalsPerMatch }}</div>
            </div>
            <div class="mb-3">
              <span class="text-body-2 text-grey-darken-1">Partido con más goles:</span>
              <div class="font-weight-medium">{{ stats.highestScoringMatch }}</div>
            </div>
            <div class="mb-3">
              <span class="text-body-2 text-grey-darken-1">Partidos sin goles:</span>
              <div class="font-weight-medium">{{ stats.goallessMatches }}</div>
            </div>
          </v-card-text>
        </v-card>
      </v-col>

      <!-- Top equipos -->
      <v-col cols="12" md="6">
        <v-card class="mb-4" variant="outlined">
          <v-card-title class="text-h6">
            <v-icon start>mdi-trophy</v-icon>
            Top Equipos
          </v-card-title>
          <v-card-text>
            <div v-if="topTeams.length === 0" class="text-center py-4">
              <v-icon class="mb-2" color="grey-lighten-1" size="32">
                mdi-trophy-outline
              </v-icon>
              <p class="text-body-2 text-grey-darken-1">
                No hay datos de equipos disponibles
              </p>
            </div>
            <div v-else>
              <div
                v-for="(team, index) in topTeams.slice(0, 5)"
                :key="team.team_entry.id"
                class="mb-2"
              >
                <div class="d-flex align-center justify-space-between">
                  <div class="d-flex align-center">
                    <div class="mr-3 text-h6 font-weight-bold" style="min-width: 24px;">
                      {{ index + 1 }}
                    </div>
                    <div>
                      <div class="text-body-2 font-weight-medium">
                        {{ team.team_entry.assigned_team?.name || `Equipo ${team.team_entry.id}` }}
                      </div>
                      <div class="text-caption text-grey-darken-1">
                        {{ team.points }} pts • {{ team.goals_for }} GF • {{ team.goals_against }} GC
                      </div>
                    </div>
                  </div>
                  <v-chip
                    v-if="index < 3"
                    :color="getPositionColor(index + 1)"
                    size="small"
                    variant="outlined"
                  >
                    {{ getPositionText(index + 1) }}
                  </v-chip>
                </div>
              </div>
            </div>
          </v-card-text>
        </v-card>
      </v-col>

      <!-- Estadísticas por fase -->
      <v-col cols="12" md="6">
        <v-card class="mb-4" variant="outlined">
          <v-card-title class="text-h6">
            <v-icon start>mdi-chart-bar</v-icon>
            Estadísticas por Fase
          </v-card-title>
          <v-card-text>
            <div v-if="phaseStats.length === 0" class="text-center py-4">
              <v-icon class="mb-2" color="grey-lighten-1" size="32">
                mdi-chart-line
              </v-icon>
              <p class="text-body-2 text-grey-darken-1">
                No hay datos por fase disponibles
              </p>
            </div>
            <div v-else>
              <div
                v-for="phase in phaseStats"
                :key="phase.stage"
                class="mb-3"
              >
                <div class="d-flex align-center justify-space-between mb-1">
                  <span class="text-body-2 font-weight-medium">
                    {{ getPhaseText(phase.stage) }}
                  </span>
                  <v-chip
                    :color="phase.completed ? 'success' : 'warning'"
                    size="x-small"
                    variant="outlined"
                  >
                    {{ phase.completed ? 'Completada' : 'En progreso' }}
                  </v-chip>
                </div>
                <div class="text-caption text-grey-darken-1">
                  {{ phase.played }}/{{ phase.total }} partidos • {{ phase.goals }} goles
                </div>
                <v-progress-linear
                  :model-value="phase.progress"
                  color="primary"
                  height="4"
                  rounded
                  class="mt-1"
                />
              </div>
            </div>
          </v-card-text>
        </v-card>
      </v-col>

      <!-- Gráficos y visualizaciones -->
      <v-col cols="12">
        <v-card class="mb-4" variant="outlined">
          <v-card-title class="text-h6">
            <v-icon start>mdi-chart-pie</v-icon>
            Distribución de Resultados
          </v-card-title>
          <v-card-text>
            <v-row>
              <v-col cols="12" md="4">
                <div class="text-center">
                  <div class="text-h4 font-weight-bold text-success">
                    {{ stats.winPercentage }}%
                  </div>
                  <div class="text-caption text-grey-darken-1">Victorias locales</div>
                </div>
              </v-col>
              <v-col cols="12" md="4">
                <div class="text-center">
                  <div class="text-h4 font-weight-bold text-grey">
                    {{ stats.drawPercentage }}%
                  </div>
                  <div class="text-caption text-grey-darken-1">Empates</div>
                </div>
              </v-col>
              <v-col cols="12" md="4">
                <div class="text-center">
                  <div class="text-h4 font-weight-bold text-error">
                    {{ stats.lossPercentage }}%
                  </div>
                  <div class="text-caption text-grey-darken-1">Derrotas locales</div>
                </div>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>

      <!-- Acciones -->
      <v-col cols="12">
        <v-card variant="outlined">
          <v-card-title class="text-h6">
            <v-icon start>mdi-lightning-bolt</v-icon>
            Acciones
          </v-card-title>
          <v-card-text>
            <div class="d-flex flex-wrap gap-3">
              <v-btn
                color="primary"
                prepend-icon="mdi-chart-bar"
                rounded="xl"
                variant="elevated"
                @click="goToStats"
              >
                Ver Estadísticas Completas
              </v-btn>
              <v-btn
                color="secondary"
                prepend-icon="mdi-download"
                rounded="xl"
                variant="outlined"
                @click="exportStats"
              >
                Exportar Estadísticas
              </v-btn>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script setup>
  import { computed, onMounted, ref } from 'vue'
  import { tournamentAPI } from '@/services/api'

  // Props
  const props = defineProps({
    tournament: {
      type: Object,
      required: true,
    },
  })

  // Emits
  const emit = defineEmits(['go-to-stats'])

  // Estado reactivo
  const matches = ref([])
  const standings = ref([])
  const loading = ref(true)

  // Computed properties
  const stats = computed(() => {
    const playedMatches = matches.value.filter(match => match.played)
    const totalMatches = matches.value.length
    const totalGoals = playedMatches.reduce((sum, match) => {
      return sum + Object.values(match.goals || {}).reduce((a, b) => a + b, 0)
    }, 0)

    const averageGoalsPerMatch = playedMatches.length > 0
      ? (totalGoals / playedMatches.length).toFixed(1)
      : '0.0'

    const highestScoringMatch = playedMatches.reduce((max, match) => {
      const matchGoals = Object.values(match.goals || {}).reduce((a, b) => a + b, 0)
      return matchGoals > max ? matchGoals : max
    }, 0)

    const goallessMatches = playedMatches.filter(match => {
      return Object.values(match.goals || {}).reduce((a, b) => a + b, 0) === 0
    }).length

    const progressPercentage = totalMatches > 0
      ? Math.round((playedMatches.length / totalMatches) * 100)
      : 0

    return {
      playedMatches: playedMatches.length,
      pendingMatches: totalMatches - playedMatches.length,
      totalMatches,
      totalGoals,
      averageGoalsPerMatch,
      highestScoringMatch,
      goallessMatches,
      progressPercentage,
    }
  })

  const topTeams = computed(() => {
    return standings.value.slice(0, 5)
  })

  const phaseStats = computed(() => {
    const phases = ['group', 'league', 'quarterfinal', 'semifinal', 'final']
    const phaseMap = {
      group: 'Grupos',
      league: 'Liga',
      quarterfinal: 'Cuartos',
      semifinal: 'Semifinal',
      final: 'Final',
    }

    return phases.map(phase => {
      const phaseMatches = matches.value.filter(match => match.stage === phase)
      const playedMatches = phaseMatches.filter(match => match.played)
      const totalGoals = playedMatches.reduce((sum, match) => {
        return sum + Object.values(match.goals || {}).reduce((a, b) => a + b, 0)
      }, 0)

      return {
        stage: phase,
        name: phaseMap[phase],
        total: phaseMatches.length,
        played: playedMatches.length,
        goals: totalGoals,
        completed: playedMatches.length === phaseMatches.length,
        progress: phaseMatches.length > 0
          ? Math.round((playedMatches.length / phaseMatches.length) * 100)
          : 0,
      }
    }).filter(phase => phase.total > 0)
  })

  // Métodos
  const loadData = async () => {
    loading.value = true
    try {
      // Cargar partidos
      const matchesResponse = await tournamentAPI.getTournamentMatches(props.tournament.id)
      matches.value = matchesResponse.data?.matches || matchesResponse.data || []

      // Cargar clasificación
      const standingsResponse = await tournamentAPI.getTournamentStandings(props.tournament.id)
      standings.value = standingsResponse.data || []
    } catch (error) {
      console.error('Error al cargar estadísticas:', error)
      matches.value = []
      standings.value = []
    } finally {
      loading.value = false
    }
  }

  const getPositionColor = position => {
    const colorMap = {
      1: 'gold',
      2: 'grey',
      3: 'brown',
    }
    return colorMap[position] || 'primary'
  }

  const getPositionText = position => {
    const textMap = {
      1: '1º',
      2: '2º',
      3: '3º',
    }
    return textMap[position] || `${position}º`
  }

  const getPhaseText = stage => {
    const phaseMap = {
      group: 'Grupos',
      league: 'Liga',
      quarterfinal: 'Cuartos de Final',
      semifinal: 'Semifinal',
      final: 'Final',
    }
    return phaseMap[stage] || stage
  }

  const goToStats = () => {
    emit('go-to-stats')
  }

  const exportStats = () => {
    // TODO: Implementar exportación de estadísticas
    console.log('Exportar estadísticas')
  }

  // Cargar datos al montar
  onMounted(() => {
    loadData()
  })
</script>

<style scoped>
.tournament-stats-overview {
  width: 100%;
}
</style>
