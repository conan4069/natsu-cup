<template>
  <div class="team-configuration">
    <!-- Formato 1v1 -->
    <div v-if="tournamentFormat === '1v1'">
      <v-alert class="mb-4" type="info" variant="tonal">
        <strong>Formato 1v1:</strong> Cada participante será un equipo individual.
      </v-alert>
      <v-card variant="outlined">
        <v-card-title class="text-subtitle-1">
          Participantes ({{ participants.length }})
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
          <v-list v-else>
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
                <v-chip color="primary" size="small" variant="outlined">
                  Equipo individual
                </v-chip>
              </template>
            </v-list-item>
          </v-list>
        </v-card-text>
      </v-card>
    </div>

    <!-- Formato 2v2 -->
    <div v-else-if="tournamentFormat === '2v2'">
      <v-alert class="mb-4" type="info" variant="tonal">
        <strong>Formato 2v2:</strong> Los participantes se agruparán en equipos de 2 jugadores.
      </v-alert>

      <!-- Opciones de generación -->
      <v-card class="mb-4" variant="outlined">
        <v-card-title class="text-subtitle-1">
          Opciones de generación
        </v-card-title>
        <v-card-text>
          <v-radio-group v-model="teamGenerationMode" class="mb-4" inline>
            <v-radio value="automatic" label="Generación automática" />
            <v-radio value="manual" label="Asignación manual de equipos" />
          </v-radio-group>
        </v-card-text>
      </v-card>

      <!-- Asignación manual de equipos -->
      <div v-if="teamGenerationMode === 'manual'" class="mb-4">
        <v-card variant="outlined">
          <v-card-title class="text-subtitle-1 d-flex align-center justify-space-between">
            Asignar equipos manualmente
            <v-btn
              color="success"
              prepend-icon="mdi-check"
              variant="elevated"
              rounded="xl"
              size="small"
              @click="applyManualTeams"
            >
              Aplicar cambios
            </v-btn>
          </v-card-title>
          <v-card-text>
            <div class="participants-grid">
              <v-card
                v-for="participant in participants"
                :key="participant.id"
                variant="outlined"
                class="participant-card"
                :class="{ 'assigned': getParticipantTeam(participant.id) !== null }"
              >
                <v-card-text class="pa-3">
                  <div class="d-flex align-center mb-3">
                    <v-avatar size="40" class="mr-3">
                      <v-img
                        v-if="participant.avatar"
                        alt="Avatar"
                        :src="participant.avatar"
                      />
                      <v-icon v-else size="20">mdi-account</v-icon>
                    </v-avatar>
                    <div>
                      <div class="text-body-1 font-weight-medium">{{ participant.display_name }}</div>
                      <div v-if="getParticipantTeam(participant.id)" class="text-caption text-success">
                        Asignado a: {{ getParticipantTeamName(getParticipantTeam(participant.id)) }}
                      </div>
                    </div>
                  </div>

                  <v-select
                    v-model="participantTeams[participant.id]"
                    :items="availableTeams"
                    item-title="name"
                    item-value="id"
                    label="Asignar a equipo"
                    density="compact"
                    variant="outlined"
                    rounded="xl"
                    clearable
                    @update:model-value="updateParticipantTeam(participant.id, $event)"
                  >
                    <template #item="{ item }">
                      <div class="d-flex align-center">
                        <v-avatar color="primary" size="20" class="mr-2">
                          <span class="text-white text-caption">{{ item.raw.id }}</span>
                        </v-avatar>
                        {{ item.raw.name }}
                      </div>
                    </template>
                  </v-select>
                </v-card-text>
              </v-card>
            </div>
          </v-card-text>
        </v-card>
      </div>

      <!-- Equipos formados -->
      <v-card class="mb-4" variant="outlined">
        <v-card-title class="text-subtitle-1 d-flex align-center justify-space-between">
          Equipos formados ({{ teams.length }})
          <v-btn
            v-if="teamGenerationMode === 'automatic'"
            color="primary"
            :loading="generatingTeams"
            prepend-icon="mdi-shuffle"
            variant="elevated"
            rounded="xl"
            size="small"
            @click="generateTeams"
          >
            Generar equipos
          </v-btn>
        </v-card-title>
        <v-card-text>
          <div v-if="teams.length === 0" class="text-center py-4">
            <p class="text-body-2 text-grey-darken-1">
              {{ teamGenerationMode === 'automatic'
                ? 'Haz clic en "Generar equipos" para crear los equipos automáticamente.'
                : 'Asigna participantes a equipos usando las opciones de arriba.' }}
            </p>
          </div>
          <div v-else class="teams-grid">
            <v-card
              v-for="(team, index) in teams"
              :key="index"
              variant="outlined"
              class="team-card"
            >
              <v-card-title class="text-subtitle-2 d-flex align-center">
                <v-avatar color="primary" size="24" class="mr-2">
                  <span class="text-white text-caption">{{ index + 1 }}</span>
                </v-avatar>
                Equipo {{ index + 1 }}
                <v-spacer />
                <v-btn
                  v-if="teamGenerationMode === 'manual'"
                  color="error"
                  icon="mdi-delete"
                  size="small"
                  variant="text"
                  @click="removeTeam(index)"
                />
              </v-card-title>
              <v-card-text class="pa-3">
                <div
                  v-for="player in team"
                  :key="player.id"
                  class="d-flex align-center mb-2"
                >
                  <v-avatar size="24" class="mr-2">
                    <v-img
                      v-if="player.avatar"
                      alt="Avatar"
                      :src="player.avatar"
                    />
                    <v-icon v-else size="16">mdi-account</v-icon>
                  </v-avatar>
                  <span class="text-body-2">{{ player.display_name }}</span>
                </div>
              </v-card-text>
            </v-card>
          </div>
        </v-card-text>
      </v-card>

      <!-- Botón para crear equipo manual -->
      <div v-if="teamGenerationMode === 'manual'" class="d-flex justify-center">
        <v-btn
          color="secondary"
          prepend-icon="mdi-plus"
          variant="elevated"
          rounded="xl"
          @click="createNewTeam"
        >
          Crear nuevo equipo
        </v-btn>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, watch, onMounted } from 'vue'

// Props
const props = defineProps({
  participants: {
    type: Array,
    default: () => []
  },
  tournamentFormat: {
    type: String,
    default: '1v1'
  },
  teams: {
    type: Array,
    default: () => []
  },
  generatingTeams: {
    type: Boolean,
    default: false
  },
  gameTeams: {
    type: Array,
    default: () => []
  }
})

// Emits
const emit = defineEmits(['update:teams', 'generate-teams', 'update:team-generation-mode'])

// Estado reactivo
const teamGenerationMode = ref('automatic')
const participantTeams = ref({}) // Mapeo de participante -> equipo
const nextTeamId = ref(1)

// Computed
const availablePlayers = computed(() => {
  const usedPlayers = new Set()
  props.teams.forEach(team => {
    team.forEach(player => usedPlayers.add(player.id))
  })
  return props.participants.filter(player => !usedPlayers.has(player.id))
})

// Equipos disponibles para asignación manual
const availableTeams = computed(() => {
  const teams = []
  const maxTeams = Math.ceil(props.participants.length / 2)

  for (let i = 1; i <= maxTeams; i++) {
    teams.push({
      id: i,
      name: `Equipo ${i}`
    })
  }
  return teams
})

// Métodos
const generateTeams = () => {
  emit('generate-teams')
}

const removeTeam = (index) => {
  const newTeams = [...props.teams]
  newTeams.splice(index, 1)
  emit('update:teams', newTeams)
}

const getParticipantTeam = (participantId) => {
  return participantTeams.value[participantId] || null
}

const getParticipantTeamName = (teamId) => {
  const team = availableTeams.value.find(t => t.id === teamId)
  return team ? team.name : 'Sin asignar'
}

const updateParticipantTeam = (participantId, teamId) => {
  console.log('Actualizando equipo:', participantId, '->', teamId)
  if (teamId) {
    participantTeams.value[participantId] = teamId
  } else {
    delete participantTeams.value[participantId]
  }
}

const createNewTeam = () => {
  nextTeamId.value++
}

const applyManualTeams = () => {
  console.log('Aplicando equipos manuales:', participantTeams.value)

  // Agrupar participantes por equipo asignado
  const teamGroups = {}

  Object.entries(participantTeams.value).forEach(([participantId, teamId]) => {
    if (!teamGroups[teamId]) {
      teamGroups[teamId] = []
    }
    const participant = props.participants.find(p => p.id == participantId)
    if (participant) {
      teamGroups[teamId].push(participant)
    }
  })

  // Crear equipos con los participantes asignados
  const newTeams = Object.values(teamGroups).filter(team => team.length > 0)

  // Agregar participantes no asignados a equipos automáticos
  const assignedParticipants = new Set(Object.keys(participantTeams.value))
  const unassignedParticipants = props.participants.filter(p => !assignedParticipants.has(p.id.toString()))

  // Crear equipos automáticos para los no asignados
  for (let i = 0; i < unassignedParticipants.length; i += 2) {
    const team = [unassignedParticipants[i]]
    if (i + 1 < unassignedParticipants.length) {
      team.push(unassignedParticipants[i + 1])
    }
    newTeams.push(team)
  }

  console.log('Nuevos equipos:', newTeams)
  emit('update:teams', newTeams)
}

// Cargar equipos existentes al componente
const loadExistingTeams = () => {
  if (props.teams.length > 0) {
    // Mapear equipos existentes a participantes
    props.teams.forEach((team, teamIndex) => {
      team.forEach(player => {
        participantTeams.value[player.id] = teamIndex + 1
      })
    })
  }
}

// Watch para emitir cambios en el modo de generación
watch(teamGenerationMode, (newMode) => {
  emit('update:team-generation-mode', newMode)
})

// Watch para resetear cuando cambia el formato
watch(() => props.tournamentFormat, (newFormat, oldFormat) => {
  console.log('Formato cambiado de', oldFormat, 'a', newFormat)
  if (newFormat === '1v1') {
    teamGenerationMode.value = 'automatic'
    participantTeams.value = {}
    emit('update:teams', [])
  }
}, { immediate: true })

// Watch para cargar equipos existentes
watch(() => props.teams, (newTeams) => {
  if (newTeams.length > 0 && teamGenerationMode.value === 'manual') {
    loadExistingTeams()
  }
}, { immediate: true })

// Cargar equipos existentes al montar
onMounted(() => {
  if (props.teams.length > 0) {
    loadExistingTeams()
  }
})
</script>

<style scoped>
.teams-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 16px;
}

.team-card {
  transition: all 0.3s ease;
}

.team-card:hover {
  border-color: var(--v-primary-base);
}

.participants-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 16px;
}

.participant-card {
  transition: all 0.3s ease;
}

.participant-card.assigned {
  border-color: var(--v-success-base);
  background-color: rgba(var(--v-theme-success), 0.05);
}

.participant-card:hover {
  border-color: var(--v-primary-base);
}
</style>
