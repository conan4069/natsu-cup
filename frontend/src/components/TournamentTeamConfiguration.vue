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
            <v-list>
              <v-list-item
                v-for="participant in participants"
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
                  <v-select
                    v-model="participantTeamAssignments[participant.id]"
                    density="compact"
                    item-title="name"
                    item-value="id"
                    :items="availableTeams"
                    label="Equipo"
                    rounded="xl"
                    variant="outlined"
                    @update:model-value="updateTeamAssignment"
                  />
                </template>
              </v-list-item>
            </v-list>

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
                      <v-icon class="mr-2" size="small">mdi-account</v-icon>
                      {{ player.display_name }}
                    </div>
                  </div>
                  <v-select
                    v-model="teamGameTeamAssignments[index]"
                    density="compact"
                    item-title="name"
                    item-value="id"
                    :items="availableTeams"
                    label="Equipo del juego"
                    rounded="xl"
                    variant="outlined"
                    @update:model-value="updateTeamGameTeamAssignment"
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
  import { computed, ref, watch } from 'vue'
  import { useRouter } from 'vue-router'
  import { gameTeamAPI } from '@/services/api'

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
  })

  // Emits
  const emit = defineEmits(['update:teams', 'update:team-assignments'])

  // Router
  const router = useRouter()

  // Estado reactivo
  const availableTeams = ref([])
  const teams = ref([])
  const generatingTeams = ref(false)
  const assigningTeams = ref(false)
  const participantTeamAssignments = ref({})
  const teamGameTeamAssignments = ref({})

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

  const assignTeamsRandomly = async () => {
    assigningTeams.value = true
    try {
      // Simular asignación aleatoria
      const shuffled = [...props.participants].sort(() => Math.random() - 0.5)
      const assignments = {}

      for (const [i, element] of shuffled.entries()) {
        const teamIndex = i % availableTeams.value.length
        assignments[element.id] = availableTeams.value[teamIndex].id
      }

      participantTeamAssignments.value = assignments
      emit('update:team-assignments', assignments)
    } finally {
      assigningTeams.value = false
    }
  }

  const updateTeamAssignment = (participantId, teamId) => {
    participantTeamAssignments.value[participantId] = teamId
    emit('update:team-assignments', participantTeamAssignments.value)
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
  }

  const goToCreateTeams = () => {
    router.push('/teams/create')
  }

  // Cargar equipos del juego al montar
  loadGameTeams()

  // Observar cambios en participantes para formato 2v2
  watch(() => props.participants, newParticipants => {
    if (props.tournamentFormat === '2v2' && newParticipants.length % 2 !== 0) {
      // Cambiar automáticamente a 1v1 si hay participantes impares
      emit('format-change', '1v1')
    }
  }, { immediate: true })
</script>

<style scoped>
/* Estilos específicos si son necesarios */
</style>
