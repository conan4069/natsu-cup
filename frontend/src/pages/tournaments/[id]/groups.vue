<template>
  <GroupsContainer
    :can-generate-knockout="canGenerateKnockout"
    :error="error"
    :generating="generating"
    :generating-knockout="generatingKnockout"
    :groups="groups"
    :loading="loading"
    :qualified-teams="qualifiedTeams"
    :tournament="tournament"
    :tournament-stats="tournamentStats"
    @configure-groups="configureGroups"
    @edit-match="editMatch"
    @generate-knockout="generateKnockoutStage"
    @go-back="goBack"
    @retry="loadTournament"
  />

  <!-- Dialog para registrar/editar resultado -->
  <MatchResultForm
    v-model="showMatchDialog"
    :match="selectedMatch"
    @save-result="saveMatchResult"
  />
</template>

<script setup>
  import { computed, onMounted, ref } from 'vue'
  import { useRoute, useRouter } from 'vue-router'
  import GroupsContainer from '@/components/GroupsContainer.vue'
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

  // Computed
  const matchesPlayed = computed(() => {
    return matches.value.filter(match => match.played).length
  })

  const totalMatches = computed(() => {
    return matches.value.length
  })

  const progressPercentage = computed(() => {
    if (totalMatches.value === 0) return 0
    return Math.round((matchesPlayed.value / totalMatches.value) * 100)
  })

  const canGenerateKnockout = computed(() => {
    return progressPercentage.value === 100 && tournament.value?.has_knockout
  })

  const tournamentStats = computed(() => ({
    groupsCount: groups.value.length,
    teamsPerGroup: tournament.value?.teams_per_group || 0,
    matchesPlayed: matchesPlayed.value,
    totalMatches: totalMatches.value,
    progressPercentage: progressPercentage.value,
    qualifiedTeams: qualifiedTeams.value.total_qualified,
  }))

  // Cargar torneo
  const loadTournament = async () => {
    const tournamentId = route.params.id

    loading.value = true
    error.value = null

    try {
      const response = await tournamentAPI.getTournament(tournamentId)
      tournament.value = response.data

      // Cargar partidos del torneo
      await loadTournamentMatches(tournamentId)

      // Cargar clasificaciones de grupos
      await loadGroupStandings(tournamentId)

      // Cargar equipos clasificados
      await loadQualifiedTeams(tournamentId)
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
      // Asegurar que matches sea siempre un array
      matches.value = matchesResponse.data?.matches || []

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
      const standingsResponse = await tournamentAPI.getGroupStandings(tournamentId)
      groupStandings.value = standingsResponse.data

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
      qualifiedTeams.value = qualifiedResponse.data
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
      if (!groupMap[groupCode]) {
        groupMap[groupCode] = {
          code: groupCode,
          teams: new Set(),
          matches: [],
          standings: [],
        }
      }

      // Agregar equipos del partido usando la nueva estructura
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
        // Información para mostrar en la UI
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

  // Navegación
  const goBack = () => {
    router.push(`/tournaments/${route.params.id}`)
  }

  const configureGroups = async () => {
    try {
      generating.value = true

      // Verificar que el torneo tenga fase de grupos habilitada
      if (!tournament.value.has_group_stage) {
        appStore.showError('Este torneo no tiene fase de grupos habilitada')
        return
      }

      // Verificar que haya equipos registrados
      const entriesResponse = await tournamentAPI.getTeamEntries(tournament.value.id)
      if (!entriesResponse.data || entriesResponse.data.length === 0) {
        appStore.showError('No hay equipos registrados en el torneo. Primero debes agregar equipos.')
        return
      }

      // Generar grupos y partidos
      await tournamentAPI.generateGroups(tournament.value.id)

      // Recargar datos del torneo
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

      await tournamentAPI.generateKnockoutStage(tournament.value.id)

      appStore.showSuccess('Fase eliminatoria generada exitosamente')

      // Redirigir al bracket
      router.push(`/tournaments/${tournament.value.id}/bracket`)
    } catch (error) {
      const errorInfo = handleApiError(error)
      appStore.showError(`Error al generar fase eliminatoria: ${errorInfo.message}`)
      console.error('Error al generar fase eliminatoria:', errorInfo.message)
    } finally {
      generatingKnockout.value = false
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
      // Preparar datos para el backend
      const goals = {}
      const participants = selectedMatch.value.participants || []

      if (participants.length >= 2) {
        const team1Id = participants[0].id
        const team2Id = participants[1].id

        goals[team1Id] = result.team1Score
        goals[team2Id] = result.team2Score
      }

      // Enviar al backend
      await matchAPI.saveMatchResult(selectedMatch.value.id, { goals })

      // Recargar datos
      await loadTournament()

      appStore.showSuccess('Resultado guardado exitosamente')
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
.page-title {
  color: white !important;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
}

.page-subtitle {
  color: #f3f2e5 !important;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
}

.match-card {
  transition: box-shadow 0.2s;
}

.match-card:hover {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.team-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.team-info.text-right {
  align-items: flex-end;
}

.team-name {
  font-weight: 500;
  margin-bottom: 4px;
}

.team-score {
  font-size: 1.5rem;
  font-weight: bold;
  color: var(--v-primary-base);
}

.match-vs {
  margin: 0 16px;
  display: flex;
  align-items: center;
}

.match-actions {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 8px;
}

/* Estilos para clasificación */
.first-place {
  background-color: rgba(255, 215, 0, 0.1) !important;
  border-left: 4px solid gold;
}

.second-place {
  background-color: rgba(192, 192, 192, 0.1) !important;
  border-left: 4px solid silver;
}

.third-place {
  background-color: rgba(205, 127, 50, 0.1) !important;
  border-left: 4px solid #cd7f32;
}

/* Estilos para equipos clasificados */
.qualified-team-card {
  transition: transform 0.2s, box-shadow 0.2s;
  min-width: 200px;
}

.qualified-team-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.qualified-team-card.winner {
  border-left: 4px solid gold;
}

.qualified-team-card.runner-up {
  border-left: 4px solid silver;
}

.qualified-team-card.third-place {
  border-left: 4px solid #cd7f32;
}

/* Responsive */
@media (max-width: 768px) {
  .d-flex.align-center.justify-space-between {
    flex-direction: column;
    gap: 16px;
  }

  .match-actions {
    align-items: center;
  }

  .team-info {
    align-items: center !important;
  }

  .v-table {
    font-size: 0.875rem;
  }

  .qualified-team-card {
    min-width: 100%;
  }
}
</style>
