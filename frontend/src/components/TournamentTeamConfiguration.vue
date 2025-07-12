<template>
  <div class="tournament-team-configuration">
    <!-- Formato 1v1 -->
    <div v-if="tournamentFormat === '1v1'">
      <v-alert class="mb-4" type="info" variant="tonal">
        <strong>Formato 1v1:</strong> Cada participante será un equipo individual.
      </v-alert>

      <!-- Configuración de equipos -->
      <v-card class="mb-6" variant="outlined">
        <v-card-title class="text-subtitle-1 d-flex align-center justify-space-between">
          Asignación de equipos
          <v-btn
            color="primary"
            :loading="assigningTeams"
            prepend-icon="mdi-shuffle"
            rounded="xl"
            size="small"
            variant="elevated"
            @click="assignTeamsRandomly"
          >
            Asignar equipos automáticamente
          </v-btn>
        </v-card-title>
        <v-card-text>
          <div v-if="participants.length === 0" class="text-center py-8">
            <v-icon class="mb-4" color="grey-lighten-1" size="48">
              mdi-account-group
            </v-icon>
            <h4 class="text-h6 text-grey-darken-1 mb-2">
              No hay participantes
            </h4>
            <p class="text-body-2 text-grey-darken-1">
              Agrega participantes en la pestaña anterior.
            </p>
          </div>
          <div v-else>
            <!-- Lista de participantes con equipos asignados -->
            <div class="participants-grid">
              <v-card
                v-for="participant in participants"
                :key="participant.id"
                class="participant-card mb-4"
                variant="outlined"
              >
                <v-card-text>
                  <div class="d-flex align-center mb-3">
                    <v-avatar class="mr-3" size="40">
                      <v-img
                        v-if="participant.avatar"
                        alt="Avatar"
                        :src="participant.avatar"
                      />
                      <v-icon v-else>mdi-account</v-icon>
                    </v-avatar>
                    <div class="flex-grow-1">
                      <h4 class="text-h6 mb-1">{{ participant.display_name }}</h4>
                      <p class="text-body-2 text-grey-darken-1 mb-0">
                        Participante
                      </p>
                    </div>
                  </div>

                  <!-- Equipo asignado -->
                  <div class="team-assignment">
                    <h5 class="text-subtitle-2 mb-2">Equipo asignado:</h5>
                    <div v-if="participantTeamAssignments[participant.id]" class="selected-team">
                      <v-chip
                        class="mb-2"
                        color="primary"
                        size="large"
                        variant="elevated"
                      >
                        {{ getTeamName(participantTeamAssignments[participant.id]) }}
                      </v-chip>
                      <v-btn
                        color="error"
                        prepend-icon="mdi-close"
                        rounded="xl"
                        size="small"
                        variant="outlined"
                        @click="removeTeamAssignment(participant.id)"
                      >
                        Quitar equipo
                      </v-btn>
                    </div>
                    <div v-else class="no-team">
                      <v-alert class="mb-3" type="info" variant="tonal">
                        <strong>Sin equipo asignado</strong>
                      </v-alert>

                      <!-- Lista de equipos disponibles -->
                      <div class="available-teams">
                        <h6 class="text-caption mb-2">Equipos disponibles:</h6>
                        <div class="teams-grid">
                          <v-card
                            v-for="team in availableTeamsForSelection"
                            :key="team.id"
                            class="team-option-card"
                            variant="outlined"
                            @click="updateTeamAssignment(participant.id, team.id)"
                          >
                            <v-card-text class="text-center pa-3">
                              <v-icon class="mb-2" color="primary" size="24">
                                mdi-shield
                              </v-icon>
                              <div class="text-body-2 font-weight-medium">
                                {{ team.name }}
                              </div>
                            </v-card-text>
                          </v-card>
                        </div>
                      </div>
                    </div>
                  </div>
                </v-card-text>
              </v-card>
            </div>

            <!-- Botón para crear equipos faltantes -->
            <div v-if="missingTeamsCount > 0" class="mt-4">
              <v-alert type="warning" variant="tonal">
                <strong>Equipos faltantes:</strong> Se necesitan {{ missingTeamsCount }} equipos más.
                <v-btn
                  class="mt-2"
                  color="primary"
                  prepend-icon="mdi-plus"
                  rounded="xl"
                  size="small"
                  variant="elevated"
                  @click="goToCreateTeams"
                >
                  Crear equipos faltantes
                </v-btn>
              </v-alert>
            </div>
          </div>
        </v-card-text>
      </v-card>
    </div>

    <!-- Formato 2v2 -->
    <div v-else-if="tournamentFormat === '2v2'">
      <v-alert class="mb-4" type="info" variant="tonal">
        <strong>Formato 2v2:</strong> Los participantes se agruparán en equipos de 2.
      </v-alert>

      <!-- Validación de participantes -->
      <v-alert
        v-if="participants.length % 2 !== 0"
        class="mb-4"
        type="warning"
        variant="tonal"
      >
        <strong>Participantes impares:</strong> Se necesitan {{ participants.length % 2 === 1 ? 1 : 2 }} participante(s) más para formar equipos de 2.
        El modo se cambiará automáticamente a 1v1 hasta que haya suficientes participantes.
      </v-alert>

      <!-- Configuración de grupos -->
      <v-card class="mb-6" variant="outlined">
        <v-card-title class="text-subtitle-1 d-flex align-center justify-space-between">
          Formación de equipos
          <v-btn
            color="primary"
            :loading="generatingTeams"
            prepend-icon="mdi-shuffle"
            rounded="xl"
            size="small"
            variant="elevated"
            @click="generateTeams"
          >
            Agrupar automáticamente
          </v-btn>
        </v-card-title>
        <v-card-text>
          <div v-if="participants.length === 0" class="text-center py-8">
            <v-icon class="mb-4" color="grey-lighten-1" size="48">
              mdi-account-group
            </v-icon>
            <h4 class="text-h6 text-grey-darken-1 mb-2">
              No hay participantes
            </h4>
            <p class="text-body-2 text-grey-darken-1">
              Agrega participantes en la pestaña anterior.
            </p>
          </div>
          <div v-else>
            <!-- Participantes disponibles para agrupar -->
            <v-list>
              <v-list-item
                v-for="participant in availableForGrouping"
                :key="participant.id"
              >
                <template #prepend>
                  <v-avatar size="32">
                    <v-img
                      v-if="participant.avatar"
                      alt="Avatar"
                      :src="participant.avatar"
                    />
                    <v-icon v-else>mdi-account</v-icon>
                  </v-avatar>
                </template>
                <v-list-item-title>{{ participant.display_name }}</v-list-item-title>
                <template #append>
                  <v-chip
                    v-if="getParticipantTeam(participant.id)"
                    color="primary"
                    size="small"
                    variant="outlined"
                  >
                    {{ getParticipantTeam(participant.id) }}
                  </v-chip>
                </template>
              </v-list-item>
            </v-list>
          </div>
        </v-card-text>
      </v-card>

      <!-- Equipos formados -->
      <v-card v-if="teams.length > 0" variant="outlined">
        <v-card-title class="text-subtitle-1">
          Equipos formados ({{ teams.length }})
        </v-card-title>
        <v-card-text>
          <div v-for="(team, index) in teams" :key="index" class="mb-4">
            <v-card variant="outlined">
              <v-card-title class="text-subtitle-2">
                Equipo {{ index + 1 }}
              </v-card-title>
              <v-card-text>
                <div class="d-flex align-center mb-3">
                  <div class="flex-grow-1">
                    <div v-for="player in team" :key="player.id" class="mb-1">
                      <v-avatar v-if="player.avatar" class="mr-2" left size="20">
                        <v-img :src="player.avatar" />
                      </v-avatar>
                      <v-icon v-else class="mr-2" size="small">mdi-account</v-icon>
                      {{ player.display_name }}
                    </div>
                  </div>
                  <v-select
                    v-model="teamGameTeamAssignments[index]"
                    density="compact"
                    item-title="name"
                    item-value="id"
                    :items="availableTeamsForSelection"
                    label="Equipo del juego"
                    rounded="xl"
                    variant="outlined"
                    @update:model-value="(value) => updateTeamGameTeamAssignment(index, value)"
                  />
                </div>
              </v-card-text>
            </v-card>
          </div>
        </v-card-text>
      </v-card>
    </div>
  </div>
</template>

<script setup>
  import { computed, onMounted, ref, watch } from 'vue'
  import { useRouter } from 'vue-router'
  import { gameTeamAPI, tournamentAPI } from '@/services/api'

  // Props
  const props = defineProps({
    participants: {
      type: Array,
      default: () => [],
    },
    tournamentFormat: {
      type: String,
      default: '1v1',
    },
    tournamentId: {
      type: [String, Number],
      required: true,
    },
  })

  // Emits
  const emit = defineEmits(['update:teams', 'update:team-assignments', 'update:team-entries'])

  // Router
  const router = useRouter()

  // Estado reactivo
  const availableTeams = ref([])
  const teams = ref([])
  const generatingTeams = ref(false)
  const assigningTeams = ref(false)
  const participantTeamAssignments = ref({})
  const teamGameTeamAssignments = ref({})
  const existingEntries = ref([])

  // Computed
  const availableForGrouping = computed(() => {
    const usedPlayers = new Set()
    for (const team of teams.value) {
      for (const player of team) usedPlayers.add(player.id)
    }
    return props.participants.filter(player => !usedPlayers.has(player.id))
  })

  const missingTeamsCount = computed(() => {
    const assignedTeams = new Set(Object.values(participantTeamAssignments.value))
    return Math.max(0, props.participants.length - availableTeams.value.length)
  })

  // Computed para equipos disponibles (excluyendo los ya seleccionados)
  const availableTeamsForSelection = computed(() => {
    const selectedTeamIds = new Set()

    // Agregar equipos seleccionados en formato 1v1
    for (const teamId of Object.values(participantTeamAssignments.value)) {
      if (teamId) selectedTeamIds.add(teamId)
    }

    // Agregar equipos seleccionados en formato 2v2
    for (const teamId of Object.values(teamGameTeamAssignments.value)) {
      if (teamId) selectedTeamIds.add(teamId)
    }

    return availableTeams.value.filter(team => !selectedTeamIds.has(team.id))
  })

  // Computed para generar las entradas de equipos en formato correcto para la API
  const teamEntries = computed(() => {
    const entries = []

    if (props.tournamentFormat === '1v1') {
      // Para formato 1v1, cada participante es una entrada individual
      for (const participant of props.participants) {
        const teamId = participantTeamAssignments.value[participant.id]
        entries.push({
          players: [participant.id],
          assigned_team: teamId || null,
          // NO incluir tournament aquí - el backend lo maneja automáticamente
        })
      }
    } else if (props.tournamentFormat === '2v2') {
      // Para formato 2v2, cada equipo formado es una entrada
      for (const [index, team] of teams.value.entries()) {
        const teamId = teamGameTeamAssignments.value[index]
        entries.push({
          players: team.map(player => player.id),
          assigned_team: teamId || null,
          // NO incluir tournament aquí - el backend lo maneja automáticamente
        })
      }
    }

    return entries
  })

  // Métodos
  const loadGameTeams = async () => {
    try {
      const response = await gameTeamAPI.getGameTeams()
      availableTeams.value = response.data
    } catch (error) {
      console.error('Error al cargar equipos del juego:', error)
      availableTeams.value = []
    }
  }

  // Cargar entradas existentes del torneo
  const loadExistingEntries = async () => {
    try {
      const response = await tournamentAPI.getTeamEntries(props.tournamentId)
      existingEntries.value = response.data

      // Mapear las asignaciones existentes
      const assignments = {}
      for (const entry of existingEntries.value) {
        if (entry.players && entry.players.length > 0) {
          for (const player of entry.players) {
            assignments[player.id] = entry.assigned_team?.id || null
          }
        }
      }

      participantTeamAssignments.value = assignments
      emit('update:team-assignments', assignments)
      emit('update:team-entries', teamEntries.value)

      console.log('Entradas existentes cargadas:', existingEntries.value)
    } catch (error) {
      console.error('Error al cargar entradas existentes:', error)
    }
  }

  const assignTeamsRandomly = async () => {
    assigningTeams.value = true
    try {
      // Llamar a la API del backend para asignar equipos aleatoriamente
      await tournamentAPI.assignRandomTeams(props.tournamentId)

      // Recargar las entradas para ver los cambios
      await loadExistingEntries()

      console.log('Equipos asignados aleatoriamente')
    } catch (error) {
      console.error('Error al asignar equipos aleatoriamente:', error)
    } finally {
      assigningTeams.value = false
    }
  }

  const updateTeamAssignment = (participantId, teamId) => {
    participantTeamAssignments.value[participantId] = teamId
    emit('update:team-assignments', participantTeamAssignments.value)
    emit('update:team-entries', teamEntries.value)
  }

  // Métodos auxiliares para mostrar el nombre del equipo
  const getTeamName = teamId => {
    const team = availableTeams.value.find(t => t.id === teamId)
    return team ? team.name : teamId
  }

  const removeTeamAssignment = participantId => {
    participantTeamAssignments.value[participantId] = null
    emit('update:team-assignments', participantTeamAssignments.value)
    emit('update:team-entries', teamEntries.value)
  }

  const removeGameTeamAssignment = teamIndex => {
    teamGameTeamAssignments.value[teamIndex] = null
    emit('update:team-entries', teamEntries.value)
  }

  const generateTeams = () => {
    generatingTeams.value = true
    setTimeout(() => {
      const shuffled = [...availableForGrouping.value].sort(() => Math.random() - 0.5)
      const newTeams = []

      for (let i = 0; i < shuffled.length; i += 2) {
        if (i + 1 < shuffled.length) {
          newTeams.push([shuffled[i], shuffled[i + 1]])
        } else {
          newTeams.push([shuffled[i]])
        }
      }

      teams.value = newTeams
      emit('update:teams', newTeams)
      emit('update:team-entries', teamEntries.value)
      generatingTeams.value = false
    }, 1000)
  }

  const getParticipantTeam = participantId => {
    for (const [teamIndex, team] of teams.value.entries()) {
      if (team.some(player => player.id === participantId)) {
        return `Equipo ${teamIndex + 1}`
      }
    }
    return null
  }

  const updateTeamGameTeamAssignment = (teamIndex, gameTeamId) => {
    teamGameTeamAssignments.value[teamIndex] = gameTeamId
    emit('update:team-entries', teamEntries.value)
  }

  const goToCreateTeams = () => {
    router.push('/teams/create')
  }

  // Cargar datos al montar
  onMounted(async () => {
    await loadGameTeams()
    await loadExistingEntries()
  })

  // Observar cambios en teamEntries para emitir actualizaciones
  watch(teamEntries, newEntries => {
    emit('update:team-entries', newEntries)
  }, { deep: true })
</script>

<style scoped>
.participants-grid,
.teams-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
}
.participant-card,
.team-option-card {
  min-width: 220px;
  cursor: pointer;
  transition: box-shadow 0.2s;
}
.team-option-card:hover {
  box-shadow: 0 2px 12px rgba(0,0,0,0.08);
}
</style>
