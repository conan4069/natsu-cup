<template>
  <div class="tournament-league-overview">
    <v-row>
      <!-- Estado de la liga -->
      <v-col cols="12" md="6">
        <v-card class="mb-4" rounded="xl" variant="outlined">
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
        <v-card class="mb-4" rounded="xl" variant="outlined">
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
                :key="team.id"
                class="mb-2"
              >
                <div class="d-flex align-center justify-space-between">
                  <div class="d-flex align-center">
                    <div class="mr-3 text-h6 font-weight-bold" style="min-width: 24px;">
                      {{ index + 1 }}
                    </div>
                    <div>
                      <div class="text-body-2 font-weight-medium">
                        {{ team.assigned_team?.name || `Equipo ${team.id}` }}
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
        <v-card class="mb-4" rounded="xl" variant="outlined">
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
                    <div class="d-flex align-center mb-1">
                      <div class="text-body-2 font-weight-medium">
                        {{ getTeamName(match, 0) }} vs {{ getTeamName(match, 1) }}
                      </div>
                      <v-chip
                        v-if="match.round"
                        class="ml-2"
                        color="primary"
                        size="x-small"
                        variant="outlined"
                      >
                        Jornada {{ match.round }}
                      </v-chip>
                    </div>
                    <div class="text-caption text-grey-darken-1">
                      Partido pendiente
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
        <v-card rounded="xl" variant="outlined">
          <v-card-title class="text-h6">
            <v-icon start>mdi-lightning-bolt</v-icon>
            Acciones
          </v-card-title>
          <v-card-text>
            <div class="d-flex flex-wrap align-center" style="gap: 5px;">
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
                :disabled="generating"
                :loading="generating"
                prepend-icon="mdi-play"
                rounded="xl"
                variant="elevated"
                @click="startLeague"
              >
                Generar Partidos
              </v-btn>
              <v-btn
                v-if="tournament.competition_type === 'hybrid' && leagueStatus === 'completed'"
                color="warning"
                :disabled="generating"
                :loading="generating"
                prepend-icon="mdi-trophy"
                rounded="xl"
                variant="elevated"
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
  import { handleApiError, tournamentAPI } from '@/services/api'
  import { useAppStore } from '@/stores/app'

  // Props
  const props = defineProps({
    tournament: {
      type: Object,
      required: true,
    },
  })

  // Emits
  const emit = defineEmits(['go-to-league'])

  // Store
  const appStore = useAppStore()

  // Estado reactivo
  const matches = ref([])
  const standings = ref([])
  const loading = ref(true)
  const generating = ref(false)

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
  async function loadData () {
    loading.value = true
    try {
      // Cargar partidos
      const matchesResponse = await tournamentAPI.getTournamentMatches(props.tournament.id)
      matches.value = matchesResponse.data?.matches || matchesResponse.data || []

      // Cargar clasificación
      const standingsResponse = await tournamentAPI.getStandings(props.tournament.id, 'tournament')
      standings.value = standingsResponse.data || []
    } catch (error) {
      console.error('Error al cargar datos de la liga:', error)
      matches.value = []
      standings.value = []
    } finally {
      loading.value = false
    }
  }

  function getLeagueStatusColor (status) {
    const colorMap = {
      not_started: 'grey',
      in_progress: 'warning',
      completed: 'success',
    }
    return colorMap[status] || 'grey'
  }

  function getLeagueStatusText (status) {
    const textMap = {
      not_started: 'No iniciada',
      in_progress: 'En progreso',
      completed: 'Completada',
    }
    return textMap[status] || 'Desconocido'
  }

  function getPositionColor (position) {
    const colorMap = {
      1: 'gold',
      2: 'grey',
      3: 'brown',
    }
    return colorMap[position] || 'primary'
  }

  function getPositionText (position) {
    const textMap = {
      1: '1º',
      2: '2º',
      3: '3º',
    }
    return textMap[position] || `${position}º`
  }

  function goToLeague () {
    emit('go-to-league')
  }

  function getTeamName (match, index) {
    if (!match?.participants || !Array.isArray(match.participants)) {
      return 'Por definir'
    }
    const participant = match.participants[index]
    if (!participant) return 'Por definir'
    return participant.assigned_team?.name || `Equipo ${participant.id}` || 'Por definir'
  }

  async function startLeague () {
    generating.value = true
    try {
      const response = await tournamentAPI.generateLeagueMatches(props.tournament.id)
      const matchesCount = response.data?.matches_count || 0

      appStore.showSuccess(
        matchesCount > 0
          ? `Se generaron ${matchesCount} partidos de liga exitosamente`
          : response.data?.message || 'Partidos de liga generados exitosamente',
      )

      // Recargar datos para mostrar los nuevos partidos
      await loadData()
    } catch (error) {
      const errorInfo = handleApiError(error)
      appStore.showError(
        errorInfo.message || 'Error al generar los partidos de liga',
      )
      console.error('Error al generar partidos de liga:', errorInfo)
    } finally {
      generating.value = false
    }
  }

  async function generatePlayoffs () {
    generating.value = true
    try {
      const response = await tournamentAPI.generatePlayoffs(props.tournament.id)
      const matchesCount = response.data?.matches_count || 0
      const stage = response.data?.stage || 'playoffs'

      appStore.showSuccess(
        matchesCount > 0
          ? `Se generaron ${matchesCount} partidos de ${stage} exitosamente`
          : response.data?.message || 'Partidos de playoffs generados exitosamente',
      )

      // Recargar datos para mostrar los nuevos partidos
      await loadData()
    } catch (error) {
      const errorInfo = handleApiError(error)
      appStore.showError(
        errorInfo.message || 'Error al generar los partidos de playoffs',
      )
      console.error('Error al generar playoffs:', errorInfo)
    } finally {
      generating.value = false
    }
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
