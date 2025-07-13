<template>
  <v-container fluid>
    <!-- Loading state -->
    <div v-if="loading" class="d-flex justify-center align-center" style="min-height: 400px;">
      <v-progress-circular color="primary" indeterminate size="64" />
    </div>

    <!-- Error state -->
    <div v-else-if="error" class="text-center py-8">
      <v-icon class="mb-4" color="error" size="64">mdi-alert-circle</v-icon>
      <h3 class="text-h6 text-grey-darken-1 mb-2">Error al cargar grupos</h3>
      <p class="text-body-2 text-grey-darken-1 mb-4">{{ error }}</p>
      <v-btn color="primary" rounded="xl" @click="loadTournament">Reintentar</v-btn>
    </div>

    <!-- Groups management -->
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
              <h1 class="text-h4 font-weight-bold mb-2 page-title text-white">{{ tournament.name }}</h1>
              <p class="text-body-1 text-grey-darken-1">
                Fase de Grupos - {{ tournament.format }}
              </p>
            </div>
            <div class="d-flex gap-2">
              <v-btn
                v-if="!tournament.has_group_stage"
                color="warning"
                disabled
                prepend-icon="mdi-alert"
                rounded="xl"
                variant="outlined"
              >
                Fase de Grupos Deshabilitada
              </v-btn>
              <v-btn
                v-else-if="groups.length === 0"
                color="success"
                :loading="generating"
                prepend-icon="mdi-account-group"
                rounded="xl"
                variant="elevated"
                @click="configureGroups"
              >
                Generar Grupos
              </v-btn>
              <v-btn
                v-if="canGenerateKnockout"
                color="warning"
                :loading="generatingKnockout"
                prepend-icon="mdi-trophy"
                rounded="xl"
                variant="elevated"
                @click="generateKnockoutStage"
              >
                Generar Eliminatoria
              </v-btn>
            </div>
          </div>
        </v-col>
      </v-row>

      <!-- Tournament stats -->
      <v-row class="mb-6">
        <v-col cols="12">
          <v-card class="bg-white" variant="outlined">
            <v-card-title class="text-h6">
              <v-icon start>mdi-chart-line</v-icon>
              Estado de la Fase de Grupos
            </v-card-title>
            <v-card-text>
              <div v-if="!tournament.has_group_stage" class="text-center py-8">
                <v-icon class="mb-4" color="warning" size="64">mdi-alert-circle</v-icon>
                <h3 class="text-h6 text-grey-darken-1 mb-2">Fase de Grupos Deshabilitada</h3>
                <p class="text-body-2 text-grey-darken-1">
                  Este torneo no tiene fase de grupos habilitada. Solo tiene fase eliminatoria.
                </p>
              </div>
              <div v-else-if="groups.length === 0" class="text-center py-8">
                <v-icon class="mb-4" color="info" size="64">mdi-account-group-outline</v-icon>
                <h3 class="text-h6 text-grey-darken-1 mb-2">No hay grupos generados</h3>
                <p class="text-body-2 text-grey-darken-1 mb-4">
                  Los grupos aún no han sido generados. Haz clic en "Generar Grupos" para comenzar.
                </p>
                <v-btn
                  color="success"
                  :loading="generating"
                  prepend-icon="mdi-account-group"
                  rounded="xl"
                  variant="elevated"
                  @click="configureGroups"
                >
                  Generar Grupos
                </v-btn>
              </div>
              <div v-else>
                <v-row>
                  <v-col cols="12" md="3">
                    <div class="text-center">
                      <div class="text-h4 font-weight-bold text-primary">
                        {{ groups.length }}
                      </div>
                      <div class="text-caption text-grey-darken-1">Grupos</div>
                    </div>
                  </v-col>
                  <v-col cols="12" md="3">
                    <div class="text-center">
                      <div class="text-h4 font-weight-bold text-success">
                        {{ matchesPlayed }}
                      </div>
                      <div class="text-caption text-grey-darken-1">Partidos Jugados</div>
                    </div>
                  </v-col>
                  <v-col cols="12" md="3">
                    <div class="text-center">
                      <div class="text-h4 font-weight-bold text-warning">
                        {{ totalMatches }}
                      </div>
                      <div class="text-caption text-grey-darken-1">Total Partidos</div>
                    </div>
                  </v-col>
                  <v-col cols="12" md="3">
                    <div class="text-center">
                      <div class="text-h4 font-weight-bold text-info">
                        {{ qualifiedTeams.total_qualified }}
                      </div>
                      <div class="text-caption text-grey-darken-1">Equipos Clasificados</div>
                    </div>
                  </v-col>
                </v-row>
                <div class="mt-4">
                  <div class="d-flex align-center justify-space-between mb-2">
                    <span class="text-body-2">Progreso general</span>
                    <span class="text-body-2 font-weight-medium">{{ progressPercentage }}%</span>
                  </div>
                  <v-progress-linear
                    color="primary"
                    height="8"
                    :model-value="progressPercentage"
                    rounded
                  />
                </div>
              </div>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>

      <!-- Groups tabs -->
      <v-row v-if="groups.length > 0">
        <v-col cols="12">
          <v-card class="bg-white" variant="outlined">
            <v-tabs v-model="activeGroupTab" color="primary" rounded="xl">
              <v-tab
                v-for="group in groups"
                :key="group.code"
                :value="group.code"
              >
                <v-icon start>mdi-account-group</v-icon>
                Grupo {{ group.code }}
              </v-tab>
            </v-tabs>

            <v-window v-model="activeGroupTab">
              <v-window-item
                v-for="group in groups"
                :key="group.code"
                :value="group.code"
              >
                <v-card-text class="pa-6">
                  <!-- Group standings -->
                  <GroupStandingsTable
                    :group-code="group.code"
                    :standings="group.standings"
                  />

                  <!-- Group matches -->
                  <GroupMatches
                    :group-code="group.code"
                    :matches="group.matches"
                    @edit-match="editMatch"
                  />

                  <!-- Group teams -->
                  <v-expansion-panels>
                    <v-expansion-panel>
                      <v-expansion-panel-title>
                        <v-icon start>mdi-account-group</v-icon>
                        Equipos del Grupo {{ group.code }}
                      </v-expansion-panel-title>
                      <v-expansion-panel-text>
                        <div class="teams-grid">
                          <v-card
                            v-for="team in getGroupTeams(group)"
                            :key="team.id"
                            class="team-card"
                            variant="outlined"
                          >
                            <v-card-text class="pa-3">
                              <div class="d-flex align-center mb-2">
                                <v-avatar class="mr-3" size="40">
                                  <v-img
                                    v-if="team.assigned_team?.logo_url"
                                    :src="team.assigned_team.logo_url"
                                  />
                                  <v-icon v-else>mdi-shield</v-icon>
                                </v-avatar>
                                <div>
                                  <div class="font-weight-medium">
                                    {{ team.assigned_team?.name || `Equipo ${team.id}` }}
                                  </div>
                                </div>
                              </div>
                              <div v-if="team.players && team.players.length > 0">
                                <div class="text-caption text-grey-darken-1 mb-2">Participantes:</div>
                                <div class="d-flex flex-wrap gap-1">
                                  <v-chip
                                    v-for="player in team.players"
                                    :key="player.id"
                                    class="ma-1"
                                    color="primary"
                                    label
                                    size="small"
                                    variant="outlined"
                                  >
                                    <v-avatar v-if="player.avatar_url" left size="16">
                                      <v-img :src="player.avatar_url" />
                                    </v-avatar>
                                    {{ player.display_name }}
                                  </v-chip>
                                </div>
                              </div>
                            </v-card-text>
                          </v-card>
                        </div>
                      </v-expansion-panel-text>
                    </v-expansion-panel>
                  </v-expansion-panels>
                </v-card-text>
              </v-window-item>
            </v-window>
          </v-card>
        </v-col>
      </v-row>

      <!-- Qualified teams section -->
      <v-row v-if="allQualifiedTeams.length > 0" class="mt-6">
        <v-col cols="12">
          <v-card class="bg-white" variant="outlined">
            <v-card-title class="text-h6">
              <v-icon start>mdi-trophy</v-icon>
              Equipos Clasificados para Eliminatoria
            </v-card-title>
            <v-card-text>
              <div class="qualified-teams-grid">
                <v-card
                  v-for="team in allQualifiedTeams"
                  :key="team.team_entry.id"
                  class="qualified-team-card"
                  :class="getQualifiedTeamClass(team)"
                  variant="outlined"
                >
                  <v-card-text class="pa-3">
                    <div class="d-flex align-center justify-space-between">
                      <div class="d-flex align-center">
                        <v-avatar class="mr-3" size="32">
                          <v-img
                            v-if="team.team_entry.assigned_team?.logo_url"
                            :src="team.team_entry.assigned_team.logo_url"
                          />
                          <v-icon v-else size="small">mdi-shield</v-icon>
                        </v-avatar>
                        <div>
                          <div class="font-weight-medium">
                            {{ team.team_entry.assigned_team?.name || `Equipo ${team.team_entry.id}` }}
                          </div>
                          <div class="text-caption text-grey-darken-1">
                            {{ getQualificationTypeText(team.qualification_type) }}
                          </div>
                        </div>
                      </div>
                      <v-chip
                        :color="getQualificationColor(team.qualification_type)"
                        size="small"
                        variant="outlined"
                      >
                        {{ team.group_code }}
                      </v-chip>
                    </div>
                  </v-card-text>
                </v-card>
              </div>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </div>

    <!-- Match result dialog -->
    <MatchResultForm
      v-model="showMatchDialog"
      :match="selectedMatch"
      @save-result="saveMatchResult"
    />
  </v-container>
</template>

<script setup>
  import { computed, onMounted, ref } from 'vue'
  import { useRoute, useRouter } from 'vue-router'
  import GroupMatches from '@/components/GroupMatches.vue'
  import GroupStandingsTable from '@/components/GroupStandingsTable.vue'
  import MatchResultForm from '@/components/MatchResultForm.vue'
  import { handleApiError, matchAPI, tournamentAPI } from '@/services/api'
  import { useAppStore } from '@/stores/app'

  // Router y Route
  const router = useRouter()
  const route = useRoute()
  const appStore = useAppStore()

  // Estado reactivo
  const loading = ref(true)
  const generating = ref(false)
  const generatingKnockout = ref(false)
  const error = ref(null)
  const tournament = ref(null)
  const groups = ref([])
  const matches = ref([])
  const groupStandings = ref({})
  const qualifiedTeams = ref({
    group_winners: [],
    group_runners_up: [],
    best_third_place: [],
    total_qualified: 0,
  })
  const showMatchDialog = ref(false)
  const selectedMatch = ref(null)
  const activeGroupTab = ref('')

  // Computed
  const matchesPlayed = computed(() => {
    const groupMatches = matches.value.filter(match => match.stage === 'group')
    return groupMatches.filter(match => match.played).length
  })

  const totalMatches = computed(() => {
    const groupMatches = matches.value.filter(match => match.stage === 'group')
    return groupMatches.length
  })

  const progressPercentage = computed(() => {
    if (totalMatches.value === 0) return 0
    return Math.round((matchesPlayed.value / totalMatches.value) * 100)
  })

  const canGenerateKnockout = computed(() => {
    return progressPercentage.value === 100 && tournament.value?.has_knockout
  })

  const allQualifiedTeams = computed(() => {
    return [
      ...qualifiedTeams.value.group_winners,
      ...qualifiedTeams.value.group_runners_up,
      ...qualifiedTeams.value.best_third_place,
    ]
  })

  // Cargar torneo
  const loadTournament = async () => {
    const tournamentId = route.params.id

    loading.value = true
    error.value = null

    try {
      const response = await tournamentAPI.getTournament(tournamentId)
      tournament.value = response.data

      // Solo cargar datos de grupos si el torneo tiene fase de grupos habilitada
      if (tournament.value.has_group_stage) {
        // Cargar partidos del torneo
        await loadTournamentMatches(tournamentId)

        // Cargar clasificaciones de grupos
        await loadGroupStandings(tournamentId)

        // Cargar equipos clasificados
        await loadQualifiedTeams(tournamentId)

        // Establecer la primera pestaña activa si hay grupos
        if (groups.value.length > 0) {
          activeGroupTab.value = groups.value[0].code
        }
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

  // Cargar partidos del torneo
  const loadTournamentMatches = async tournamentId => {
    try {
      const matchesResponse = await tournamentAPI.getTournamentMatches(tournamentId)
      matches.value = matchesResponse.data || []

      // Organizar partidos por grupos
      organizeGroupsFromMatches()
    } catch (error) {
      console.error('Error al cargar partidos:', error)
      matches.value = []
      groups.value = []
    }
  }

  // Cargar clasificaciones de grupos
  const loadGroupStandings = async tournamentId => {
    try {
      const standingsResponse = await tournamentAPI.getStandings(tournamentId, 'group')
      groupStandings.value = standingsResponse.data || {}

      // Actualizar grupos con clasificaciones
      updateGroupsWithStandings()
    } catch (error) {
      console.error('Error al cargar clasificaciones:', error)
      groupStandings.value = {}
    }
  }

  // Cargar equipos clasificados
  const loadQualifiedTeams = async tournamentId => {
    try {
      const qualifiedResponse = await tournamentAPI.getQualifiedTeams(tournamentId)
      qualifiedTeams.value = qualifiedResponse.data || {
        group_winners: [],
        group_runners_up: [],
        best_third_place: [],
        total_qualified: 0,
      }
    } catch (error) {
      console.error('Error al cargar equipos clasificados:', error)
      qualifiedTeams.value = {
        group_winners: [],
        group_runners_up: [],
        best_third_place: [],
        total_qualified: 0,
      }
    }
  }

  // Organizar partidos en grupos
  const organizeGroupsFromMatches = () => {
    const groupMatches = matches.value.filter(match => match.stage === 'group')

    if (groupMatches.length === 0) {
      groups.value = []
      return
    }

    // Agrupar por código de grupo
    const groupMap = {}
    for (const match of groupMatches) {
      const groupCode = match.group_code
      if (!groupCode) continue

      if (!groupMap[groupCode]) {
        groupMap[groupCode] = {
          code: groupCode,
          teams: new Set(),
          matches: [],
          standings: [],
        }
      }

      // Agregar equipos del partido
      if (match.participants && Array.isArray(match.participants)) {
        for (const participant of match.participants) {
          groupMap[groupCode].teams.add(participant.id)
        }
      }

      // Agregar partido con información completa
      groupMap[groupCode].matches.push({
        id: match.id,
        played: match.played,
        goals: match.goals || {},
        participants: match.participants || [],
        team1_name: match.participants?.[0]?.assigned_team?.name
          || match.participants?.[0]?.team_name || 'Equipo 1',
        team2_name: match.participants?.[1]?.assigned_team?.name
          || match.participants?.[1]?.team_name || 'Equipo 2',
        team1_score: match.goals?.[match.participants?.[0]?.id] || 0,
        team2_score: match.goals?.[match.participants?.[1]?.id] || 0,
      })
    }

    // Convertir a array
    groups.value = Object.values(groupMap).map(group => ({
      ...group,
      teams: Array.from(group.teams).map(teamId => ({
        id: teamId,
        name: `Equipo ${teamId}`,
      })),
    }))
  }

  // Actualizar grupos con clasificaciones
  const updateGroupsWithStandings = () => {
    for (const group of groups.value) {
      const groupCode = group.code
      group.standings = groupStandings.value[groupCode] || []
    }
  }

  // Obtener equipos del grupo con información completa
  const getGroupTeams = group => {
    const teamsMap = {}

    // Recolectar equipos de los partidos
    for (const match of group.matches || []) {
      for (const participant of match.participants || []) {
        if (!teamsMap[participant.id]) {
          teamsMap[participant.id] = participant
        }
      }
    }

    return Object.values(teamsMap)
  }

  // Métodos de utilidad
  const getQualifiedTeamClass = team => {
    const typeMap = {
      group_winner: 'winner',
      group_runner_up: 'runner-up',
      best_third_place: 'third-place',
    }
    return typeMap[team.qualification_type] || ''
  }

  const getQualificationTypeText = type => {
    const typeMap = {
      group_winner: 'Ganador de grupo',
      group_runner_up: 'Segundo de grupo',
      best_third_place: 'Mejor tercero',
    }
    return typeMap[type] || 'Clasificado'
  }

  const getQualificationColor = type => {
    const colorMap = {
      group_winner: 'success',
      group_runner_up: 'warning',
      best_third_place: 'info',
    }
    return colorMap[type] || 'primary'
  }

  // Navegación
  const goBack = () => {
    router.push(`/tournaments/${route.params.id}`)
  }

  const configureGroups = async () => {
    try {
      generating.value = true

      if (!tournament.value.has_group_stage) {
        appStore.showError('Este torneo no tiene fase de grupos habilitada')
        return
      }

      const entriesResponse = await tournamentAPI.getTeamEntries(tournament.value.id)
      if (!entriesResponse.data || entriesResponse.data.length === 0) {
        appStore.showError('No hay equipos registrados en el torneo. Primero debes agregar equipos.')
        return
      }

      await tournamentAPI.generateGroups(tournament.value.id)
      await loadTournament()

      appStore.showSuccess('Grupos generados exitosamente')
    } catch (error) {
      const errorInfo = handleApiError(error)
      appStore.showError(`Error al generar grupos: ${errorInfo.message}`)
      console.error('Error al generar grupos:', errorInfo.message)
    } finally {
      generating.value = false
    }
  }

  // Generar fase eliminatoria
  const generateKnockoutStage = async () => {
    try {
      generatingKnockout.value = true

      // Usar la función unificada knockoutStage
      await tournamentAPI.knockoutStage(tournament.value.id, {})

      appStore.showSuccess('Fase eliminatoria generada exitosamente')
      router.push(`/tournaments/${tournament.value.id}/bracket`)
    } catch (error) {
      const errorInfo = handleApiError(error)
      appStore.showError(`Error al generar fase eliminatoria: ${errorInfo.message}`)
      console.error('Error al generar fase eliminatoria:', errorInfo.message)
    } finally {
      generatingKnockout.value = false
    }
  }

  const editMatch = match => {
    selectedMatch.value = match
    showMatchDialog.value = true
  }

  const saveMatchResult = async result => {
    try {
      const goals = {}
      const participants = selectedMatch.value.participants || []

      // Construir el objeto goals con los IDs de los participantes
      for (const participant of participants) {
        if (participant.id === result.team1Id) {
          goals[participant.id] = result.team1Score
        } else if (participant.id === result.team2Id) {
          goals[participant.id] = result.team2Score
        }
      }

      await matchAPI.saveMatchResult(selectedMatch.value.id, { goals })

      // Recargar datos
      await loadTournament()

      appStore.showSuccess('Resultado guardado exitosamente')
      showMatchDialog.value = false
    } catch (error) {
      const errorInfo = handleApiError(error)
      appStore.showError(`Error al guardar resultado: ${errorInfo.message}`)
      console.error('Error al guardar resultado:', errorInfo.message)
    }
  }

  // Cargar datos al montar
  onMounted(() => {
    loadTournament()
  })
</script>

<style scoped>
.tournament-groups-overview {
  width: 100%;
}

.teams-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 16px;
}

.team-card {
  transition: all 0.3s ease;
}

.team-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.qualified-teams-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 16px;
}

.qualified-team-card {
  transition: all 0.3s ease;
}

.qualified-team-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.qualified-team-card.winner {
  border-left: 4px solid #4caf50;
}

.qualified-team-card.runner-up {
  border-left: 4px solid #ff9800;
}

.qualified-team-card.third-place {
  border-left: 4px solid #2196f3;
}
</style>
