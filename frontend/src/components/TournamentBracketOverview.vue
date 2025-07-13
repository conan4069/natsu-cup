<template>
  <div class="tournament-bracket-overview">
    <v-row>
      <!-- Estado de la eliminatoria -->
      <v-col cols="12" md="6">
        <v-card class="mb-4" rounded="xl" variant="outlined">
          <v-card-title class="text-h6">
            <v-icon start>mdi-trophy</v-icon>
            Estado de la Eliminatoria
          </v-card-title>
          <v-card-text>
            <div class="mb-3">
              <span class="text-body-2 text-grey-darken-1">Estado:</span>
              <div class="mt-1">
                <v-chip
                  :color="getBracketStatusColor(bracketStatus)"
                  size="small"
                  variant="outlined"
                >
                  {{ getBracketStatusText(bracketStatus) }}
                </v-chip>
              </div>
            </div>
            <div class="mb-3">
              <span class="text-body-2 text-grey-darken-1">Fase actual:</span>
              <div class="font-weight-medium">{{ currentPhase }}</div>
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
                  :model-value="bracketProgress"
                  rounded
                />
                <div class="text-caption text-grey-darken-1 mt-1">
                  {{ bracketProgress }}% completado
                </div>
              </div>
            </div>
          </v-card-text>
        </v-card>
      </v-col>

      <!-- Próximos partidos -->
      <v-col cols="12" md="6">
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
                    <div class="text-body-2 font-weight-medium">
                      {{ match.team1?.name || 'Por definir' }} vs {{ match.team2?.name || 'Por definir' }}
                    </div>
                    <div class="text-caption text-grey-darken-1">
                      {{ getPhaseText(match.stage) }}
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
                  @click="goToBracket"
                >
                  Ver todos los partidos
                </v-btn>
              </div>
            </div>
          </v-card-text>
        </v-card>
      </v-col>

      <!-- Ganador actual -->
      <v-col v-if="currentWinner" cols="12">
        <v-card class="mb-4" rounded="xl" variant="outlined">
          <v-card-title class="text-h6">
            <v-icon start>mdi-crown</v-icon>
            Ganador Actual
          </v-card-title>
          <v-card-text>
            <div class="d-flex align-center">
              <v-avatar class="mr-3" size="48">
                <v-img
                  v-if="currentWinner.assigned_team?.logo"
                  :src="currentWinner.assigned_team.logo"
                />
                <v-icon v-else>mdi-trophy</v-icon>
              </v-avatar>
              <div>
                <div class="text-h6 font-weight-bold">
                  {{ currentWinner.assigned_team?.name || 'Equipo Ganador' }}
                </div>
                <div class="text-body-2 text-grey-darken-1">
                  Campeón del torneo
                </div>
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
                prepend-icon="mdi-trophy"
                rounded="xl"
                variant="elevated"
                @click="goToBracket"
              >
                Ver Eliminatoria Completa
              </v-btn>
              <v-btn
                v-if="bracketStatus === 'not_started'"
                color="success"
                prepend-icon="mdi-play"
                rounded="xl"
                variant="elevated"
                @click="startBracket"
              >
                Iniciar Eliminatoria
              </v-btn>
              <v-btn
                v-if="bracketStatus === 'in_progress'"
                color="warning"
                prepend-icon="mdi-pause"
                rounded="xl"
                variant="elevated"
                @click="pauseBracket"
              >
                Pausar Eliminatoria
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
  const emit = defineEmits(['go-to-bracket'])

  // Estado reactivo
  const matches = ref([])
  const loading = ref(true)

  // Computed properties
  const bracketStatus = computed(() => {
    if (matches.value.length === 0) return 'not_started'
    const playedMatches = matches.value.filter(match => match.played)
    if (playedMatches.length === matches.value.length) return 'completed'
    if (playedMatches.length > 0) return 'in_progress'
    return 'not_started'
  })

  const currentPhase = computed(() => {
    if (matches.value.length === 0) return 'No iniciada'

    const phases = {
      final: 'Final',
      semifinal: 'Semifinal',
      quarterfinal: 'Cuartos de Final',
      round_of_16: 'Octavos de Final',
      round_of_32: 'Ronda de 32',
    }

    // Encontrar la fase más alta con partidos
    const phaseOrder = ['final', 'semifinal', 'quarterfinal', 'round_of_16', 'round_of_32']
    for (const phase of phaseOrder) {
      const phaseMatches = matches.value.filter(match => match.stage === phase)
      if (phaseMatches.length > 0) {
        return phases[phase] || 'Fase de Eliminación'
      }
    }

    return 'Fase de Eliminación'
  })

  const playedMatches = computed(() => {
    return matches.value.filter(match => match.played).length
  })

  const totalMatches = computed(() => {
    return matches.value.length
  })

  const bracketProgress = computed(() => {
    if (totalMatches.value === 0) return 0
    return Math.round((playedMatches.value / totalMatches.value) * 100)
  })

  const upcomingMatches = computed(() => {
    return matches.value.filter(match => !match.played)
  })

  const currentWinner = computed(() => {
    if (bracketStatus.value !== 'completed') return null

    // Buscar el ganador de la final
    const finalMatch = matches.value.find(match => match.stage === 'final' && match.played)
    if (!finalMatch) return null

    // Determinar el ganador basado en los goles
    const team1Goals = finalMatch.goals?.[finalMatch.participants?.[0]?.id] || 0
    const team2Goals = finalMatch.goals?.[finalMatch.participants?.[1]?.id] || 0

    return team1Goals > team2Goals ? finalMatch.participants?.[0] : finalMatch.participants?.[1]
  })

  // Métodos
  const loadMatches = async () => {
    loading.value = true
    try {
      const response = await tournamentAPI.getTournamentMatches(props.tournament.id)
      matches.value = response.data.matches || []
    } catch (error) {
      console.error('Error al cargar partidos:', error)
      matches.value = []
    } finally {
      loading.value = false
    }
  }

  const getBracketStatusColor = status => {
    const colorMap = {
      not_started: 'grey',
      in_progress: 'warning',
      completed: 'success',
    }
    return colorMap[status] || 'grey'
  }

  const getBracketStatusText = status => {
    const textMap = {
      not_started: 'No iniciada',
      in_progress: 'En progreso',
      completed: 'Completada',
    }
    return textMap[status] || 'Desconocido'
  }

  const getPhaseText = stage => {
    const phaseMap = {
      final: 'Final',
      semifinal: 'Semifinal',
      quarterfinal: 'Cuartos de Final',
      round_of_16: 'Octavos de Final',
      round_of_32: 'Ronda de 32',
    }
    return phaseMap[stage] || 'Eliminatoria'
  }

  const goToBracket = () => {
    emit('go-to-bracket')
  }

  const startBracket = () => {
    // TODO: Implementar inicio de eliminatoria
    console.log('Iniciar eliminatoria')
  }

  const pauseBracket = () => {
    // TODO: Implementar pausa de eliminatoria
    console.log('Pausar eliminatoria')
  }

  // Cargar datos al montar
  onMounted(() => {
    loadMatches()
  })
</script>

<style scoped>
.tournament-bracket-overview {
  width: 100%;
}
</style>
