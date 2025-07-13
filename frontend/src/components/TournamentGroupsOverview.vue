<template>
  <div class="tournament-groups-overview">
    <v-row>
      <!-- Estado de los grupos -->
      <v-col cols="12" md="6">
        <v-card class="mb-4" rounded="xl" variant="outlined">
          <v-card-title class="text-h6">
            <v-icon start>mdi-account-group</v-icon>
            Estado de los Grupos
          </v-card-title>
          <v-card-text>
            <div class="mb-3">
              <span class="text-body-2 text-grey-darken-1">Estado:</span>
              <div class="mt-1">
                <v-chip
                  :color="getGroupsStatusColor(groupsStatus)"
                  size="small"
                  variant="outlined"
                >
                  {{ getGroupsStatusText(groupsStatus) }}
                </v-chip>
              </div>
            </div>
            <div class="mb-3">
              <span class="text-body-2 text-grey-darken-1">Número de grupos:</span>
              <div class="font-weight-medium">{{ groupsCount }}</div>
            </div>
            <div class="mb-3">
              <span class="text-body-2 text-grey-darken-1">Equipos por grupo:</span>
              <div class="font-weight-medium">{{ tournament.teams_per_group || 4 }}</div>
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
                  :model-value="groupsProgress"
                  rounded
                />
                <div class="text-caption text-grey-darken-1 mt-1">
                  {{ groupsProgress }}% completado
                </div>
              </div>
            </div>
          </v-card-text>
        </v-card>
      </v-col>

      <!-- Equipos clasificados -->
      <v-col cols="12" md="6">
        <v-card class="mb-4" rounded="xl" variant="outlined">
          <v-card-title class="text-h6">
            <v-icon start>mdi-trophy</v-icon>
            Equipos Clasificados
          </v-card-title>
          <v-card-text>
            <div v-if="loading" class="text-center py-4">
              <v-progress-circular color="primary" indeterminate size="32" />
              <p class="text-body-2 text-grey-darken-1 mt-2">
                Cargando equipos clasificados...
              </p>
            </div>
            <div v-else-if="allQualifiedTeams.length === 0" class="text-center py-4">
              <v-icon class="mb-2" color="grey-lighten-1" size="32">
                mdi-trophy-outline
              </v-icon>
              <p class="text-body-2 text-grey-darken-1">
                {{ groupsStatus === 'completed' ? 'No hay equipos clasificados aún' : 'Los grupos aún no están completados' }}
              </p>
            </div>
            <div v-else>
              <div
                v-for="team in allQualifiedTeams.slice(0, 6)"
                :key="team.team_entry.id"
                class="mb-2"
              >
                <div class="d-flex align-center justify-space-between">
                  <div class="d-flex align-center">
                    <v-avatar class="mr-2" size="24">
                      <v-img
                        v-if="team.team_entry.assigned_team?.logo_url && team.team_entry.assigned_team.logo_url !== 'null'"
                        :src="team.team_entry.assigned_team.logo_url"
                      />
                      <v-icon v-else size="small">mdi-shield</v-icon>
                    </v-avatar>
                    <div>
                      <div class="text-body-2 font-weight-medium">
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
              </div>
              <div v-if="allQualifiedTeams.length > 6" class="text-center mt-2">
                <v-btn
                  color="primary"
                  size="small"
                  variant="text"
                  @click="goToGroups"
                >
                  Ver todos los clasificados ({{ qualifiedTeams.total_qualified || allQualifiedTeams.length > 0 ? allQualifiedTeams.length : 0 }})
                </v-btn>
              </div>
            </div>
          </v-card-text>
        </v-card>
      </v-col>

      <!-- Resumen de grupos -->
      <v-col cols="12">
        <v-card class="mb-4" rounded="xl" variant="outlined">
          <v-card-title class="text-h6">
            <v-icon start>mdi-view-grid</v-icon>
            Resumen de Grupos
          </v-card-title>
          <v-card-text>
            <div v-if="loading" class="text-center py-4">
              <v-progress-circular color="primary" indeterminate size="32" />
              <p class="text-body-2 text-grey-darken-1 mt-2">
                Cargando resumen de grupos...
              </p>
            </div>
            <div v-else-if="groupsSummary.length === 0" class="text-center py-4">
              <v-icon class="mb-2" color="grey-lighten-1" size="32">
                mdi-account-group-outline
              </v-icon>
              <p class="text-body-2 text-grey-darken-1">
                {{ groupsStatus === 'not_started' ? 'No hay grupos generados' : 'No hay datos de grupos disponibles' }}
              </p>
            </div>
            <div v-else>
              <v-row>
                <v-col
                  v-for="group in groupsSummary"
                  :key="group.code"
                  cols="12"
                  md="4"
                  sm="6"
                >
                  <v-card class="pa-3" variant="outlined">
                    <div class="d-flex align-center justify-space-between mb-2">
                      <h6 class="text-subtitle-2 font-weight-bold">
                        Grupo {{ group.code }}
                      </h6>
                      <v-chip
                        :color="group.completed ? 'success' : 'warning'"
                        size="x-small"
                        variant="outlined"
                      >
                        {{ group.completed ? 'Completado' : 'En progreso' }}
                      </v-chip>
                    </div>
                    <div class="text-caption text-grey-darken-1 mb-2">
                      {{ group.teams_count }} equipos • {{ group.matches_played }}/{{ group.total_matches }} partidos
                    </div>
                    <div class="text-caption">
                      <div v-if="group.leader" class="font-weight-medium">
                        Líder: {{ group.leader }}
                      </div>
                    </div>
                  </v-card>
                </v-col>
              </v-row>
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
                prepend-icon="mdi-account-group"
                rounded="xl"
                variant="elevated"
                @click="goToGroups"
              >
                Ver Grupos Completos
              </v-btn>
              <v-btn
                v-if="groupsStatus === 'not_started'"
                color="success"
                prepend-icon="mdi-play"
                rounded="xl"
                variant="elevated"
                @click="generateGroups"
              >
                Generar Grupos
              </v-btn>
              <v-btn
                v-if="groupsStatus === 'completed' && tournament.has_knockout"
                color="warning"
                prepend-icon="mdi-trophy"
                rounded="xl"
                variant="elevated"
                @click="generateKnockout"
              >
                Generar Eliminatoria
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
  const emit = defineEmits(['go-to-groups'])

  // Estado reactivo
  const matches = ref([])
  const qualifiedTeams = ref({
    group_winners: [],
    group_runners_up: [],
    best_third_place: [],
    total_qualified: 0,
  })
  const groupsSummary = ref([])
  const loading = ref(true)

  // Computed properties
  const groupsStatus = computed(() => {
    if (matches.value.length === 0) return 'not_started'
    const groupMatches = matches.value.filter(match => match.stage === 'group')
    const playedMatches = groupMatches.filter(match => match.played)
    if (playedMatches.length === groupMatches.length && groupMatches.length > 0) return 'completed'
    if (playedMatches.length > 0) return 'in_progress'
    return 'not_started'
  })

  const groupsCount = computed(() => {
    const groupMatches = matches.value.filter(match => match.stage === 'group')
    const groupCodes = new Set(groupMatches.map(match => match.group_code).filter(Boolean))
    return groupCodes.size
  })

  const playedMatches = computed(() => {
    const groupMatches = matches.value.filter(match => match.stage === 'group')
    return groupMatches.filter(match => match.played).length
  })

  const totalMatches = computed(() => {
    const groupMatches = matches.value.filter(match => match.stage === 'group')
    return groupMatches.length
  })

  const groupsProgress = computed(() => {
    if (totalMatches.value === 0) return 0
    return Math.round((playedMatches.value / totalMatches.value) * 100)
  })

  // Combinar todos los equipos clasificados en un solo array
  const allQualifiedTeams = computed(() => {
    return [
      ...qualifiedTeams.value.group_winners,
      ...qualifiedTeams.value.group_runners_up,
      ...qualifiedTeams.value.best_third_place,
    ]
  })

  // Métodos
  const loadData = async () => {
    loading.value = true
    try {
      // Cargar partidos
      const matchesResponse = await tournamentAPI.getTournamentMatches(props.tournament.id)
      matches.value = matchesResponse.data?.matches || matchesResponse.data || []

      // Cargar equipos clasificados solo si los grupos están completados
      if (groupsStatus.value === 'completed') {
        try {
          const qualifiedResponse = await tournamentAPI.getQualifiedTeams(props.tournament.id)
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
      } else {
        qualifiedTeams.value = {
          group_winners: [],
          group_runners_up: [],
          best_third_place: [],
          total_qualified: 0,
        }
      }

      // Generar resumen de grupos
      generateGroupsSummary()
    } catch (error) {
      console.error('Error al cargar datos de grupos:', error)
      matches.value = []
      qualifiedTeams.value = {
        group_winners: [],
        group_runners_up: [],
        best_third_place: [],
        total_qualified: 0,
      }
      groupsSummary.value = []
    } finally {
      loading.value = false
    }
  }

  const generateGroupsSummary = () => {
    const groupMatches = matches.value.filter(match => match.stage === 'group')
    const groupMap = {}

    for (const match of groupMatches) {
      const groupCode = match.group_code
      if (!groupCode) continue

      if (!groupMap[groupCode]) {
        groupMap[groupCode] = {
          code: groupCode,
          teams_count: 0,
          matches_played: 0,
          total_matches: 0,
          leader: null,
          completed: false,
        }
      }

      groupMap[groupCode].total_matches++
      if (match.played) {
        groupMap[groupCode].matches_played++
      }

      // Contar equipos únicos
      if (match.participants && Array.isArray(match.participants)) {
        const teamIds = new Set()
        for (const participant of match.participants) {
          teamIds.add(participant.id)
        }
        groupMap[groupCode].teams_count = Math.max(groupMap[groupCode].teams_count, teamIds.size)
      }
    }

    // Determinar si el grupo está completado
    for (const group of Object.values(groupMap)) {
      group.completed = group.matches_played === group.total_matches && group.total_matches > 0
    }

    groupsSummary.value = Object.values(groupMap)
  }

  const getGroupsStatusColor = status => {
    const colorMap = {
      not_started: 'grey',
      in_progress: 'warning',
      completed: 'success',
    }
    return colorMap[status] || 'grey'
  }

  const getGroupsStatusText = status => {
    const textMap = {
      not_started: 'No iniciados',
      in_progress: 'En progreso',
      completed: 'Completados',
    }
    return textMap[status] || 'Desconocido'
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

  const goToGroups = () => {
    emit('go-to-groups')
  }

  const generateGroups = () => {
    // TODO: Implementar generación de grupos
    console.log('Generar grupos')
  }

  const generateKnockout = () => {
    // TODO: Implementar generación de eliminatoria
    console.log('Generar eliminatoria')
  }

  // Cargar datos al montar
  onMounted(() => {
    loadData()
  })
</script>

<style scoped>
.tournament-groups-overview {
  width: 100%;
}
</style>
