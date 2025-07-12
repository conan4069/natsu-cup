<template>
  <div class="tournament-team-configuration">
    <!-- Formato 1v1 -->
    <div v-if="tournamentFormat === '1v1'">
      <v-alert class="mb-4" type="info" variant="tonal">
        <strong>Formato 1v1:</strong> Cada participante será un equipo individual.
      </v-alert>

      <!-- Configuración de equipos -->
      <v-card class="mb-6" variant="outlined" rounded="xl">
        <v-card-title class="text-subtitle-1 d-flex align-center justify-space-between">
          Asignación de equipos
          <v-btn
            color="blue-darken-2"
            :loading="assigningTeams"
            prepend-icon="mdi-shuffle"
            rounded="xl"
            size="small"
            variant="elevated"
            @click="assignTeamsRandomly"
          >
            Asignar automáticamente
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
                rounded="xl"
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
                      <div class="d-flex align-center" style="gap: 5px;">
                        <v-chip
                          class="mb-2"
                          color="blue-darken-2"
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
                          Quitar
                        </v-btn>
                      </div>
                    </div>
                    <div v-else class="no-team">
                      <v-alert class="mb-3" type="info" variant="tonal">
                        <strong>Sin equipo asignado</strong>
                      </v-alert>

                      <!-- Select de equipos disponibles -->
                      <v-select
                        v-model="participantTeamAssignments[participant.id]"
                        item-title="name"
                        item-value="id"
                        :items="availableTeamsForSelection"
                        label="Seleccionar equipo"
                        rounded="xl"
                        variant="outlined"
                        @update:model-value="(value) => updateTeamAssignment(participant.id, value)"
                      />
                    </div>
                  </div>
                </v-card-text>
              </v-card>
            </div>

            <!-- Botón para crear equipos faltantes -->
            <div v-if="missingTeamsCount > 0" class="mt-4">
              <v-alert type="warning" variant="tonal">
                <div class="d-flex align-center" style="gap: 12px;">
                  <span>
                    <strong>Equipos faltantes:</strong> Se necesitan {{ missingTeamsCount }} equipos más.
                  </span>
                  <v-btn
                    color="primary"
                    prepend-icon="mdi-plus"
                    rounded="xl"
                    size="small"
                    variant="elevated"
                    @click="goToCreateTeams"
                  >
                    Crear equipo
                  </v-btn>
                </div>
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
          <div class="d-flex gap-2">
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
            <v-btn
              color="secondary"
              prepend-icon="mdi-account-multiple"
              rounded="xl"
              size="small"
              variant="outlined"
              @click="enableManualGrouping"
            >
              Agrupar manualmente
            </v-btn>
          </div>
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
            <!-- Modo de agrupación manual -->
            <div v-if="manualGroupingMode" class="manual-grouping">
              <v-alert class="mb-4" type="info" variant="tonal">
                <strong>Modo manual:</strong> Selecciona participantes para formar equipos de 2.
              </v-alert>

              <!-- Participantes disponibles -->
              <div class="mb-4">
                <h6 class="text-subtitle-2 mb-2">Participantes disponibles:</h6>
                <div class="participants-grid">
                  <v-card
                    v-for="participant in availableForManualGrouping"
                    :key="participant.id"
                    class="participant-card"
                    variant="outlined"
                    @click="selectParticipantForManualTeam(participant)"
                  >
                    <v-card-text class="text-center pa-3">
                      <v-avatar class="mb-2" size="40">
                        <v-img
                          v-if="participant.avatar"
                          alt="Avatar"
                          :src="participant.avatar"
                        />
                        <v-icon v-else>mdi-account</v-icon>
                      </v-avatar>
                      <div class="text-body-2 font-weight-medium">
                        {{ participant.display_name }}
                      </div>
                    </v-card-text>
                  </v-card>
                </div>
              </div>

              <!-- Equipos formados manualmente -->
              <div v-if="manualTeams.length > 0">
                <h6 class="text-subtitle-2 mb-2">Equipos formados:</h6>
                <div class="teams-grid">
                  <v-card
                    v-for="(team, index) in manualTeams"
                    :key="index"
                    class="team-card"
                    variant="outlined"
                  >
                    <v-card-title class="text-subtitle-2">
                      Equipo {{ index + 1 }}
                      <v-btn
                        class="ml-2"
                        color="error"
                        density="comfortable"
                        icon="mdi-delete"
                        size="small"
                        variant="text"
                        @click="removeManualTeam(index)"
                      />
                    </v-card-title>
                    <v-card-text>
                      <div v-for="player in team" :key="player.id" class="mb-1">
                        <div class="d-flex align-center">
                          <v-avatar class="mr-2" size="24">
                            <v-img
                              v-if="player.avatar"
                              alt="Avatar"
                              :src="player.avatar"
                            />
                            <v-icon v-else size="small">mdi-account</v-icon>
                          </v-avatar>
                          <span class="text-body-2">{{ player.display_name }}</span>
                          <v-spacer />
                          <v-btn
                            color="error"
                            density="comfortable"
                            icon="mdi-close"
                            size="x-small"
                            variant="text"
                            @click="removePlayerFromManualTeam(index, player)"
                          />
                        </div>
                      </div>
                    </v-card-text>
                  </v-card>
                </div>
              </div>

              <!-- Botones de acción -->
              <div class="mt-4 d-flex gap-2">
                <v-btn
                  color="primary"
                  prepend-icon="mdi-plus"
                  rounded="xl"
                  size="small"
                  variant="elevated"
                  @click="addManualTeam"
                >
                  Agregar equipo vacío
                </v-btn>
                <v-btn
                  color="success"
                  prepend-icon="mdi-check"
                  rounded="xl"
                  size="small"
                  variant="elevated"
                  @click="applyManualTeams"
                >
                  Aplicar equipos
                </v-btn>
                <v-btn
                  color="grey"
                  prepend-icon="mdi-close"
                  rounded="xl"
                  size="small"
                  variant="outlined"
                  @click="cancelManualGrouping"
                >
                  Cancelar
                </v-btn>
              </div>
            </div>

            <!-- Modo de agrupación automática -->
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
          </div>
        </v-card-text>
      </v-card>

      <!-- Equipos formados -->
      <v-card v-if="teams.length > 0" variant="outlined">
        <v-card-title class="text-subtitle-1 d-flex align-center justify-space-between">
          Equipos formados ({{ teams.length }})
          <div class="d-flex gap-2">
            <v-btn
              :color="swapMode ? 'error' : 'warning'"
              prepend-icon="mdi-swap-horizontal"
              rounded="xl"
              size="small"
              variant="outlined"
              @click="enableSwapMode"
            >
              {{ `${swapMode ? 'Deshacer intercambio de' : 'Intercambiar'} jugadores` }}
            </v-btn>
          </div>
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
                      <div class="d-flex align-center">
                        <v-btn
                          v-if="swapMode"
                          :color="isPlayerSelectedForSwap(player) ? 'success' : 'primary'"
                          density="comfortable"
                          icon="mdi-swap-horizontal"
                          size="x-small"
                          variant="text"
                          @click="selectPlayerForSwap(player, index)"
                        />
                        <v-avatar v-if="player.avatar" class="mr-2" left size="20">
                          <v-img :src="player.avatar" />
                        </v-avatar>
                        <v-icon v-else class="mr-2" size="small">mdi-account</v-icon>
                        <span class="text-body-2">{{ player.display_name }}</span>
                      </div>
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

    <!-- Validación de equipos -->
    <v-alert
      v-if="tournamentFormat === '2v2' && !isTeamsValid"
      class="mt-4"
      type="error"
      variant="tonal"
    >
      <strong>Equipos incompletos:</strong> Todos los participantes deben estar agrupados en equipos de 2.
    </v-alert>
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
  const emit = defineEmits(['update:teams', 'update:team-assignments', 'update:team-entries', 'teams-valid'])

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
  const manualGroupingMode = ref(false)
  const manualTeams = ref([])
  const swapMode = ref(false)
  const selectedPlayerForSwap = ref(null)
  const selectedTeamForSwap = ref(null)

  // Computed
  const availableForGrouping = computed(() => {
    const usedPlayers = new Set()
    for (const team of teams.value) {
      for (const player of team) usedPlayers.add(player.id)
    }
    return props.participants.filter(player => !usedPlayers.has(player.id))
  })

  const availableForManualGrouping = computed(() => {
    const usedPlayers = new Set()
    for (const team of manualTeams.value) {
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

    // Incluir todos los equipos disponibles, incluso los ya seleccionados
    // para que se muestren correctamente en los selects
    return availableTeams.value
  })

  // Validación de equipos para 2v2
  const isTeamsValid = computed(() => {
    if (props.tournamentFormat !== '2v2') return true

    // Verificar que todos los participantes estén en equipos
    const usedPlayers = new Set()
    for (const team of teams.value) {
      for (const player of team) usedPlayers.add(player.id)
    }

    // Verificar que todos los equipos tengan exactamente 2 jugadores
    for (const team of teams.value) {
      if (team.length !== 2) return false
    }

    return usedPlayers.size === props.participants.length
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
        })
      }
    } else if (props.tournamentFormat === '2v2') {
      // Para formato 2v2, cada equipo formado es una entrada
      for (const [index, team] of teams.value.entries()) {
        const teamId = teamGameTeamAssignments.value[index]
        entries.push({
          players: team.map(player => player.id),
          assigned_team: teamId || null,
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

      console.log('Entradas existentes cargadas:', existingEntries.value)
      console.log('Participantes disponibles:', props.participants)

      if (props.tournamentFormat === '1v1') {
        // Para formato 1v1, mapear asignaciones individuales
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
        console.log('Asignaciones 1v1 cargadas:', assignments)
      } else if (props.tournamentFormat === '2v2') {
        // Para formato 2v2, reconstruir equipos y asignaciones
        const reconstructedTeams = []
        const teamAssignments = {}

        console.log('Reconstruyendo equipos para formato 2v2...')

        for (const entry of existingEntries.value) {
          console.log('Procesando entrada:', entry)

          if (entry.players && entry.players.length > 0) {
            // Reconstruir el equipo con los participantes completos
            const teamPlayers = entry.players.map(player => {
              // Buscar el participante completo en props.participants
              const foundPlayer = props.participants.find(p => p.id === player.id)
              if (!foundPlayer) {
                console.warn(`Participante no encontrado:`, player)
              }
              return foundPlayer
            }).filter(Boolean)

            console.log('Jugadores del equipo reconstruido:', teamPlayers)

            if (teamPlayers.length > 0) {
              reconstructedTeams.push(teamPlayers)
              const teamIndex = reconstructedTeams.length - 1
              // Asignar el equipo del juego a este equipo
              teamAssignments[teamIndex] = entry.assigned_team?.id || null
              console.log(`Equipo ${teamIndex} asignado a:`, entry.assigned_team?.id)
            }
          }
        }

        console.log('Equipos reconstruidos:', reconstructedTeams)
        console.log('Asignaciones de equipos:', teamAssignments)

        teams.value = reconstructedTeams
        teamGameTeamAssignments.value = teamAssignments
        emit('update:teams', reconstructedTeams)
      }

      emit('update:team-entries', teamEntries.value)
    } catch (error) {
      console.error('Error al cargar entradas existentes:', error)
    }
  }

  // Método para obtener el equipo completo por ID
  const getTeamById = teamId => {
    return availableTeams.value.find(team => team.id === teamId)
  }

  // Método para obtener el ID del equipo del objeto completo
  const getTeamId = team => {
    return team ? team.id : null
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

  // Métodos para agrupación manual
  const enableManualGrouping = () => {
    manualGroupingMode.value = true
    manualTeams.value = []
  }

  const selectParticipantForManualTeam = participant => {
    // Buscar un equipo que tenga espacio
    let targetTeamIndex = -1
    for (let i = 0; i < manualTeams.value.length; i++) {
      if (manualTeams.value[i].length < 2) {
        targetTeamIndex = i
        break
      }
    }

    // Si no hay equipo con espacio, crear uno nuevo
    if (targetTeamIndex === -1) {
      manualTeams.value.push([])
      targetTeamIndex = manualTeams.value.length - 1
    }

    // Agregar participante al equipo
    manualTeams.value[targetTeamIndex].push(participant)
  }

  const addManualTeam = () => {
    manualTeams.value.push([])
  }

  const removeManualTeam = index => {
    manualTeams.value.splice(index, 1)
  }

  const removePlayerFromManualTeam = (teamIndex, player) => {
    manualTeams.value[teamIndex] = manualTeams.value[teamIndex].filter(p => p.id !== player.id)
    if (manualTeams.value[teamIndex].length === 0) {
      removeManualTeam(teamIndex)
    }
  }

  const applyManualTeams = () => {
    // Filtrar equipos que tengan exactamente 2 jugadores
    const validTeams = manualTeams.value.filter(team => team.length === 2)
    teams.value = validTeams
    emit('update:teams', validTeams)
    emit('update:team-entries', teamEntries.value)
    manualGroupingMode.value = false
  }

  const cancelManualGrouping = () => {
    manualGroupingMode.value = false
    manualTeams.value = []
  }

  // Métodos para intercambio de jugadores
  const enableSwapMode = () => {
    swapMode.value = !swapMode.value
    selectedPlayerForSwap.value = null
    selectedTeamForSwap.value = null
  }

  const isPlayerSelectedForSwap = player => {
    return selectedPlayerForSwap.value && selectedPlayerForSwap.value.id === player.id
  }

  const selectPlayerForSwap = (player, teamIndex) => {
    if (selectedPlayerForSwap.value) {
      // Segundo jugador seleccionado - hacer el intercambio
      const firstPlayer = selectedPlayerForSwap.value
      const firstTeamIndex = selectedTeamForSwap.value

      // Encontrar el segundo jugador en su equipo
      const secondTeamIndex = teamIndex
      const secondPlayerIndex = teams.value[secondTeamIndex].findIndex(p => p.id === player.id)
      const firstPlayerIndex = teams.value[firstTeamIndex].findIndex(p => p.id === firstPlayer.id)

      if (secondPlayerIndex !== -1 && firstPlayerIndex !== -1) {
        // Intercambiar jugadores
        const temp = teams.value[firstTeamIndex][firstPlayerIndex]
        teams.value[firstTeamIndex][firstPlayerIndex] = teams.value[secondTeamIndex][secondPlayerIndex]
        teams.value[secondTeamIndex][secondPlayerIndex] = temp

        // Emitir cambios
        emit('update:teams', teams.value)
        emit('update:team-entries', teamEntries.value)
      }

      // Resetear selección
      selectedPlayerForSwap.value = null
      selectedTeamForSwap.value = null
      swapMode.value = false
    } else {
      // Primer jugador seleccionado
      selectedPlayerForSwap.value = player
      selectedTeamForSwap.value = teamIndex
    }
  }

  const goToCreateTeams = () => {
    router.push('/teams/create')
  }

  // Observar cambios en isTeamsValid para emitir el estado
  watch(isTeamsValid, valid => {
    emit('teams-valid', valid)
  })

  // Observar cambios en teamEntries para emitir actualizaciones
  watch(teamEntries, newEntries => {
    emit('update:team-entries', newEntries)
  }, { deep: true })

  // Observar cambios en tournamentFormat para resetear el estado
  watch(() => props.tournamentFormat, newFormat => {
    if (newFormat === '1v1') {
      // Resetear equipos para formato 1v1
      teams.value = []
      manualGroupingMode.value = false
      manualTeams.value = []
      swapMode.value = false
    } else if (newFormat === '2v2') {
      // Resetear asignaciones individuales para formato 2v2
      participantTeamAssignments.value = {}
    }
  })

  // Observar cambios en participants para recargar entradas cuando cambien
  watch(() => props.participants, newParticipants => {
    if (newParticipants && newParticipants.length > 0) {
      console.log('Participantes actualizados, recargando entradas...')
      loadExistingEntries()
    }
  }, { deep: true })

  // Cargar datos al montar
  onMounted(async () => {
    await loadGameTeams()

    // Esperar a que los participantes estén disponibles antes de cargar entradas
    if (props.participants && props.participants.length > 0) {
      await loadExistingEntries()
    } else {
      // Si no hay participantes, esperar un poco y verificar de nuevo
      setTimeout(async () => {
        if (props.participants && props.participants.length > 0) {
          await loadExistingEntries()
        }
      }, 1000)
    }
  })
</script>

<style scoped>
.participants-grid,
.teams-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
}
.participant-card,
.team-option-card,
.team-card {
  min-width: 220px;
  cursor: pointer;
  transition: box-shadow 0.2s;
}
.participant-card:hover,
.team-option-card:hover {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}
</style>
