<template>
  <div class="tournament-overview">
    <v-row>
      <!-- Información general del torneo -->
      <v-col cols="12" md="6">
        <v-card class="mb-4" variant="outlined" rounded="xl">
          <v-card-title class="text-h6">
            <v-icon start>mdi-information</v-icon>
            Información General
          </v-card-title>
          <v-card-text>
            <div class="mb-3">
              <span class="text-body-2 text-grey-darken-1">Estado:</span>
              <div class="mt-1">
                <v-chip
                  :color="getStatusColor(tournament.status)"
                  size="small"
                  variant="outlined"
                >
                  {{ getStatusText(tournament.status) }}
                </v-chip>
              </div>
            </div>
            <div class="mb-3">
              <span class="text-body-2 text-grey-darken-1">Formato:</span>
              <div class="font-weight-medium">{{ tournament.format }}</div>
            </div>
            <div class="mb-3">
              <span class="text-body-2 text-grey-darken-1">Tipo de competición:</span>
              <div class="font-weight-medium">{{ getCompetitionTypeText(tournament.competition_type) }}</div>
            </div>
            <div class="mb-3">
              <span class="text-body-2 text-grey-darken-1">Equipos totales:</span>
              <div class="font-weight-medium">{{ tournament.total_teams || 0 }}</div>
            </div>
            <div v-if="tournament.rules" class="mb-3">
              <span class="text-body-2 text-grey-darken-1">Reglas:</span>
              <div class="font-weight-medium text-body-2">{{ tournament.rules }}</div>
            </div>
          </v-card-text>
        </v-card>
      </v-col>

      <!-- Estadísticas rápidas -->
      <v-col cols="12" md="6">
        <v-card class="mb-4" variant="outlined" rounded="xl">
          <v-card-title class="text-h6">
            <v-icon start>mdi-chart-line</v-icon>
            Estadísticas Rápidas
          </v-card-title>
          <v-card-text>
            <div class="mb-3">
              <span class="text-body-2 text-grey-darken-1">Participantes:</span>
              <div class="font-weight-medium">{{ tournament.participant_count || 0 }}</div>
            </div>
            <div class="mb-3">
              <span class="text-body-2 text-grey-darken-1">Partidos jugados:</span>
              <div class="font-weight-medium">{{ tournament.matches_played || 0 }}</div>
            </div>
            <div class="mb-3">
              <span class="text-body-2 text-grey-darken-1">Partidos pendientes:</span>
              <div class="font-weight-medium">{{ tournament.matches_pending || 0 }}</div>
            </div>
            <div class="mb-3">
              <span class="text-body-2 text-grey-darken-1">Progreso:</span>
              <div class="mt-1">
                <v-progress-linear
                  :model-value="progressPercentage"
                  color="primary"
                  height="8"
                  rounded
                />
                <div class="text-caption text-grey-darken-1 mt-1">
                  {{ progressPercentage }}% completado
                </div>
              </div>
            </div>
          </v-card-text>
        </v-card>
      </v-col>

      <!-- Configuración específica según tipo de torneo -->
      <v-col cols="12">
        <v-card class="mb-4" variant="outlined" rounded="xl">
          <v-card-title class="text-h6">
            <v-icon start>mdi-cog</v-icon>
            Configuración del Torneo
          </v-card-title>
          <v-card-text>
            <v-row>
              <!-- Configuración para liga -->
              <v-col v-if="showLeagueConfig" cols="12" md="6">
                <div class="mb-3">
                  <span class="text-body-2 text-grey-darken-1">Vueltas:</span>
                  <div class="font-weight-medium">{{ tournament.league_rounds || 1 }}</div>
                </div>
                <div v-if="tournament.competition_type === 'hybrid'" class="mb-3">
                  <span class="text-body-2 text-grey-darken-1">Equipos para playoffs:</span>
                  <div class="font-weight-medium">{{ tournament.playoff_teams || 4 }}</div>
                </div>
                <div class="mb-3">
                  <span class="text-body-2 text-grey-darken-1">Total de partidos:</span>
                  <div class="font-weight-medium">{{ calculateTotalLeagueMatches() }}</div>
                </div>
              </v-col>

              <!-- Configuración para grupos -->
              <v-col v-if="showGroupConfig" cols="12" md="6">
                <div class="mb-3">
                  <span class="text-body-2 text-grey-darken-1">Equipos por grupo:</span>
                  <div class="font-weight-medium">{{ tournament.teams_per_group || 4 }}</div>
                </div>
                <div class="mb-3">
                  <span class="text-body-2 text-grey-darken-1">Número de grupos:</span>
                  <div class="font-weight-medium">{{ numberOfGroups }}</div>
                </div>
                <div class="mb-3">
                  <span class="text-body-2 text-grey-darken-1">Partidos por grupo:</span>
                  <div class="font-weight-medium">{{ calculateMatchesPerGroup() }}</div>
                </div>
                <div class="mb-3">
                  <span class="text-body-2 text-grey-darken-1">Total partidos grupos:</span>
                  <div class="font-weight-medium">{{ calculateTotalGroupMatches() }}</div>
                </div>
              </v-col>

              <!-- Configuración para copa -->
              <v-col v-if="showCupConfig" cols="12" md="6">
                <div class="mb-3">
                  <span class="text-body-2 text-grey-darken-1">Rondas de eliminatoria:</span>
                  <div class="font-weight-medium">{{ calculateKnockoutRounds() }}</div>
                </div>
                <div class="mb-3">
                  <span class="text-body-2 text-grey-darken-1">Total partidos eliminatoria:</span>
                  <div class="font-weight-medium">{{ calculateTotalKnockoutMatches() }}</div>
                </div>
              </v-col>

              <!-- Configuración general -->
              <v-col cols="12" md="6">
                <div class="mb-3">
                  <span class="text-body-2 text-grey-darken-1">Formato de juego:</span>
                  <div class="font-weight-medium">{{ tournament.format }}</div>
                </div>
                <div class="mb-3">
                  <span class="text-body-2 text-grey-darken-1">Fecha de creación:</span>
                  <div class="font-weight-medium">
                    {{ tournament.created_at ? new Date(tournament.created_at).toLocaleDateString() : 'N/A' }}
                  </div>
                </div>
                <div v-if="tournament.rules" class="mb-3">
                  <span class="text-body-2 text-grey-darken-1">Reglas especiales:</span>
                  <div class="font-weight-medium text-body-2">{{ tournament.rules }}</div>
                </div>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>

      <!-- Acciones rápidas -->
      <v-col cols="12">
        <v-card variant="outlined" rounded="xl">
          <v-card-title class="text-h6">
            <v-icon start>mdi-lightning-bolt</v-icon>
            Acciones Rápidas
          </v-card-title>
          <v-card-text>
            <div class="d-flex flex-wrap align-center" style="gap: 5px;">
              <!-- Editar torneo -->
              <v-btn
                color="primary"
                prepend-icon="mdi-pencil"
                rounded="xl"
                variant="elevated"
                @click="editTournament"
              >
                Editar Torneo
              </v-btn>

              <!-- Generar grupos si aplica -->
              <v-btn
                v-if="showGroupsTab && tournament.status === 'draft'"
                color="success"
                prepend-icon="mdi-account-group"
                rounded="xl"
                variant="outlined"
                @click="goToGroups"
              >
                Configurar Grupos
              </v-btn>

              <!-- Generar partidos de liga si aplica -->
              <v-btn
                v-if="showLeagueTab && tournament.status === 'draft'"
                color="success"
                prepend-icon="mdi-calendar"
                rounded="xl"
                variant="elevated"
                @click="goToLeague"
              >
                Generar Partidos
              </v-btn>

              <!-- Ver eliminatoria si aplica -->
              <v-btn
                v-if="showBracketTab"
                color="warning"
                prepend-icon="mdi-trophy"
                rounded="xl"
                variant="elevated"
                @click="goToBracket"
              >
                Ver Eliminatoria
              </v-btn>

              <!-- Ver estadísticas -->
              <v-btn
                color="info"
                prepend-icon="mdi-chart-bar"
                rounded="xl"
                variant="elevated"
                @click="goToStats"
              >
                Ver Estadísticas
              </v-btn>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script setup>
  import { computed } from 'vue'

  // Props
  const props = defineProps({
    tournament: {
      type: Object,
      required: true,
    },
  })

  // Emits
  const emit = defineEmits(['edit-tournament', 'go-to-groups', 'go-to-league', 'go-to-bracket', 'go-to-stats'])

  // Computed properties
  const progressPercentage = computed(() => {
    const total = (props.tournament.matches_played || 0) + (props.tournament.matches_pending || 0)
    if (total === 0) return 0
    return Math.round(((props.tournament.matches_played || 0) / total) * 100)
  })

  const showLeagueConfig = computed(() => {
    return props.tournament.competition_type === 'league' || props.tournament.competition_type === 'hybrid'
  })

  const showGroupConfig = computed(() => {
    return props.tournament.has_group_stage === true
  })

  const showCupConfig = computed(() => {
    return props.tournament.competition_type === 'cup'
  })

  const numberOfGroups = computed(() => {
    if (!props.tournament.has_group_stage) return 0
    const totalTeams = props.tournament.total_teams || 0
    const teamsPerGroup = props.tournament.teams_per_group || 4
    return Math.ceil(totalTeams / teamsPerGroup)
  })

  const showGroupsTab = computed(() => {
    return props.tournament.has_group_stage === true
  })

  const showBracketTab = computed(() => {
    return props.tournament.has_knockout === true
  })

  const showLeagueTab = computed(() => {
    return props.tournament.competition_type === 'league' || props.tournament.competition_type === 'hybrid'
  })

  // Métodos
  const getStatusColor = status => {
    const colorMap = {
      draft: 'grey',
      active: 'success',
      completed: 'primary',
      cancelled: 'error',
    }
    return colorMap[status] || 'grey'
  }

  const getStatusText = status => {
    const textMap = {
      draft: 'Borrador',
      active: 'Activo',
      completed: 'Completado',
      cancelled: 'Cancelado',
    }
    return textMap[status] || 'Desconocido'
  }

  const getCompetitionTypeText = type => {
    const typeMap = {
      cup: 'Copa (Eliminatoria directa)',
      league: 'Liga (Todos contra todos)',
      hybrid: 'Liga + Playoffs',
      groups: 'Fase de grupos + Eliminatoria',
    }
    return typeMap[type] || 'Desconocido'
  }

  // Métodos de navegación
  const editTournament = () => {
    emit('edit-tournament')
  }

  const goToGroups = () => {
    emit('go-to-groups')
  }

  const goToLeague = () => {
    emit('go-to-league')
  }

  const goToBracket = () => {
    emit('go-to-bracket')
  }

  const goToStats = () => {
    emit('go-to-stats')
  }

  // Métodos de cálculo de partidos
  const calculateTotalLeagueMatches = () => {
    const teams = props.tournament.total_teams || 0
    const rounds = props.tournament.league_rounds || 1
    return Math.round((teams * (teams - 1) / 2) * rounds)
  }

  const calculateMatchesPerGroup = () => {
    const teamsPerGroup = props.tournament.teams_per_group || 4
    return Math.round(teamsPerGroup * (teamsPerGroup - 1) / 2)
  }

  const calculateTotalGroupMatches = () => {
    const totalTeams = props.tournament.total_teams || 0
    const teamsPerGroup = props.tournament.teams_per_group || 4
    const numberOfGroups = Math.ceil(totalTeams / teamsPerGroup)
    return numberOfGroups * calculateMatchesPerGroup()
  }

  const calculateKnockoutRounds = () => {
    const teams = props.tournament.total_teams || 0
    return Math.ceil(Math.log2(teams))
  }

  const calculateTotalKnockoutMatches = () => {
    const teams = props.tournament.total_teams || 0
    return teams - 1
  }
</script>

<style scoped>
.tournament-overview {
  width: 100%;
}
</style>
