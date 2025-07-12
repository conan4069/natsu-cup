<template>
  <div class="tournament-league-overview">
    <v-row>
      <!-- Estado de la liga -->
      <v-col cols="12" md="6">
        <v-card class="mb-4" variant="outlined">
          <v-card-title class="text-h6">
            <v-icon start>mdi-chart-line</v-icon>
            Estado de la Liga
          </v-card-title>
          <v-card-text>
            <div class="mb-3">
              <span class="text-body-2 text-grey-darken-1">Estado:</span>
              <div class="mt-1">
                <v-chip
                  :color="getLeagueStatusColor(leagueStatus)"
                  size="small"
                  variant="outlined"
                >
                  {{ getLeagueStatusText(leagueStatus) }}
                </v-chip>
              </div>
            </div>
            <div class="mb-3">
              <span class="text-body-2 text-grey-darken-1">Vueltas:</span>
              <div class="font-weight-medium">{{ tournament.league_rounds || 1 }}</div>
            </div>
            <div class="mb-3">
              <span class="text-body-2 text-grey-darken-1">Partidos jugados:</span>
              <div class="font-weight-medium">{{ playedMatches }}/{{ totalMatches }}</div>
            </div>
            <div class="mb-3">
              <span class="text-body-2 text-grey-darken-1">Progreso:</span>
              <div class="mt-1">
                <v-progress-linear
                  color="primary"
                  height="8"
                  :model-value="leagueProgress"
                  rounded
                />
                <div class="text-caption text-grey-darken-1 mt-1">
                  {{ leagueProgress }}% completado
                </div>
              </div>
            </div>
            <div v-if="tournament.competition_type === 'hybrid'" class="mb-3">
              <span class="text-body-2 text-grey-darken-1">Equipos para playoffs:</span>
              <div class="font-weight-medium">{{ tournament.playoff_teams || 4 }}</div>
            </div>
          </v-card-text>
        </v-card>
      </v-col>

      <!-- Clasificación actual -->
      <v-col cols="12" md="6">
        <v-card class="mb-4" variant="outlined">
          <v-card-title class="text-h6">
            <v-icon start>mdi-trophy</v-icon>
            Clasificación Actual
          </v-card-title>
          <v-card-text>
            <div v-if="standings.length === 0" class="text-center py-4">
              <v-icon class="mb-2" color="grey-lighten-1" size="32">
                mdi-chart-line
              </v-icon>
              <p class="text-body-2 text-grey-darken-1">
                No hay clasificación disponible
              </p>
            </div>
            <div v-else>
              <div
                v-for="(team, index) in standings.slice(0, 5)"
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
                        {{ team.points }} pts • {{ team.matches_played }} PJ
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
              <div v-if="standings.length > 5" class="text-center mt-2">
                <v-btn
                  color="primary"
                  size="small"
                  variant="text"
                  @click="goToLeague"
                >
                  Ver clasificación completa
                </v-btn>
              </div>
            </div>
          </v-card-text>
        </v-card>
      </v-col>

      <!-- Próximos partidos -->
      <v-col cols="12">
        <v-card class="mb-4" variant="outlined">
          <v-card-title class="text-h6">
            <v-icon start>mdi-calendar-clock</v-icon>
            Próximos Partidos
          </v-card-title>
          <v-card-text>
            <div v-if="upcomingMatches.length === 0" class="text-center py-4">
              <v-icon class="mb-2" color="grey-lighten-1" size="32">
                mdi-calendar-remove
              </v-icon>
              <p class="text-body-2 text-grey-darken-1">
                No hay partidos programados
              </p>
            </div>
            <div v-else>
              <div
                v-for="match in upcomingMatches.slice(0, 3)"
                :key="match.id"
                class="mb-3"
              >
                <div class="d-flex align-center justify-space-between">
                  <div class="flex-grow-1">
                    <div class="text-body-2 font-weight-medium">
                      {{ match.team1_name || 'Equipo 1' }} vs {{ match.team2_name || 'Equipo 2' }}
                    </div>
                    <div class="text-caption text-grey-darken-1">
                      Jornada {{ match.round || 'N/A' }}
                    </div>
                  </div>
                  <v-chip
                    color="warning"
                    size="small"
                    variant="outlined"
                  >
                    Pendiente
                  </v-chip>
                </div>
              </div>
              <div v-if="upcomingMatches.length > 3" class="text-center mt-2">
                <v-btn
                  color="primary"
                  size="small"
                  variant="text"
                  @click="goToLeague"
                >
                  Ver todos los partidos
                </v-btn>
              </div>
            </div>
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
                prepend-icon="mdi-chart-line"
                rounded="xl"
                variant="elevated"
                @click="goToLeague"
              >
                Ver Liga Completa
              </v-btn>
              <v-btn
                v-if="leagueStatus === 'not_started'"
                color="success"
                prepend-icon="mdi-play"
                rounded="xl"
                variant="outlined"
                @click="startLeague"
              >
                Generar Partidos
              </v-btn>
              <v-btn
                v-if="tournament.competition_type === 'hybrid' && leagueStatus === 'completed'"
                color="warning"
                prepend-icon="mdi-trophy"
                rounded="xl"
                variant="outlined"
                @click="generatePlayoffs"
              >
                Generar Playoffs
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
  const emit = defineEmits(['go-to-league'])

  // Estado reactivo
  const matches = ref([])
  const standings = ref([])
  const loading = ref(true)

  // Computed properties
  const leagueStatus = computed(() => {
    if (matches.value.length === 0) return 'not_started'
    const playedMatches = matches.value.filter(match => match.played)
    if (playedMatches.length === matches.value.length) return 'completed'
    if (playedMatches.length > 0) return 'in_progress'
    return 'not_started'
  })

  const playedMatches = computed(() => {
    return matches.value.filter(match => match.played).length
  })

  const totalMatches = computed(() => {
    return matches.value.length
  })

  const leagueProgress = computed(() => {
    if (totalMatches.value === 0) return 0
    return Math.round((playedMatches.value / totalMatches.value) * 100)
  })

  const upcomingMatches = computed(() => {
    return matches.value.filter(match => !match.played)
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
      console.error('Error al cargar datos de la liga:', error)
      matches.value = []
      standings.value = []
    } finally {
      loading.value = false
    }
  }

  const getLeagueStatusColor = status => {
    const colorMap = {
      not_started: 'grey',
      in_progress: 'warning',
      completed: 'success',
    }
    return colorMap[status] || 'grey'
  }

  const getLeagueStatusText = status => {
    const textMap = {
      not_started: 'No iniciada',
      in_progress: 'En progreso',
      completed: 'Completada',
    }
    return textMap[status] || 'Desconocido'
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

  const goToLeague = () => {
    emit('go-to-league')
  }

  const startLeague = () => {
    // TODO: Implementar generación de partidos de liga
    console.log('Generar partidos de liga')
  }

  const generatePlayoffs = () => {
    // TODO: Implementar generación de playoffs
    console.log('Generar playoffs')
  }

  // Cargar datos al montar
  onMounted(() => {
    loadData()
  })
</script>

<style scoped>
.tournament-league-overview {
  width: 100%;
}
</style>
