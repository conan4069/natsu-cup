<template>
  <v-container fluid>
    <!-- Header -->
    <v-row class="mb-6">
      <v-col cols="12">
        <div class="d-flex align-center mb-4">
          <v-btn
            class="mr-4"
            icon="mdi-arrow-left"
            variant="text"
            @click="goBack"
          />
          <div>
            <h1 class="text-h4 font-weight-bold mb-2">Nuevo Torneo</h1>
            <p class="text-body-1 text-grey-darken-1">
              Crea y configura un nuevo torneo para la Natsu Cup
            </p>
          </div>
        </div>
      </v-col>
    </v-row>

    <!-- Formulario del torneo -->
    <v-card class="mb-6">
      <v-card-title class="text-h6 pa-6 pb-0">
        Información del torneo
      </v-card-title>
      <v-card-text class="pa-6">
        <TournamentForm
          ref="tournamentFormRef"
          mode="create"
          @valid-change="handleTournamentValidChange"
        />
      </v-card-text>
    </v-card>

    <!-- Tabs para configuración -->
    <v-card>
      <v-tabs v-model="activeTab" color="primary" rounded="xl">
        <v-tab value="participants">Participantes</v-tab>
        <v-tab value="teams">Configuración de equipos</v-tab>
      </v-tabs>

      <v-window v-model="activeTab">
        <!-- Tab de participantes -->
        <v-window-item value="participants">
          <v-card-text class="pa-6">
            <v-row>
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="searchQuery"
                  class="mb-4"
                  label="Buscar jugadores"
                  prepend-inner-icon="mdi-magnify"
                  rounded="xl"
                  variant="outlined"
                />
              </v-col>
            </v-row>

            <!-- Jugadores disponibles -->
            <v-card class="mb-4" variant="outlined">
              <v-card-title class="text-subtitle-1">
                Jugadores disponibles ({{ filteredAvailablePlayers.length }})
              </v-card-title>
              <v-card-text>
                <div v-if="filteredAvailablePlayers.length === 0" class="text-center py-8">
                  <v-icon class="mb-4" color="grey-lighten-1" size="48">
                    mdi-account-group
                  </v-icon>
                  <h4 class="text-h6 text-grey-darken-1 mb-2">
                    No hay jugadores disponibles
                  </h4>
                  <p class="text-body-2 text-grey-darken-1">
                    Todos los jugadores han sido seleccionados o no hay jugadores en el sistema.
                  </p>
                </div>
                <div v-else class="players-grid">
                  <PlayerCard
                    v-for="player in filteredAvailablePlayers"
                    :key="player.id"
                    :player="player"
                    :is-selected="false"
                    @toggle-selection="addParticipant"
                  />
                </div>
              </v-card-text>
            </v-card>

            <!-- Participantes seleccionados -->
            <v-card variant="outlined">
              <v-card-title class="text-subtitle-1">
                Participantes seleccionados ({{ participants.length }})
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
                    Selecciona jugadores de la lista superior para agregarlos al torneo.
                  </p>
                </div>
                <div v-else class="players-grid">
                  <PlayerCard
                    v-for="player in participants"
                    :key="player.id"
                    :player="player"
                    :is-selected="true"
                    @toggle-selection="removeParticipant"
                  />
                </div>
              </v-card-text>
            </v-card>
          </v-card-text>
        </v-window-item>

        <!-- Tab de configuración de equipos -->
        <v-window-item value="teams">
          <v-card-text class="pa-6">
            <TeamConfiguration
              :participants="participants"
              :tournament-format="tournamentData.format"
              :teams="teams"
              :generating-teams="generatingTeams"
              :game-teams="gameTeams"
              @update:teams="updateTeams"
              @generate-teams="generateTeams"
              @update:team-generation-mode="updateTeamGenerationMode"
            />
          </v-card-text>
        </v-window-item>
      </v-window>
    </v-card>

    <!-- Botón de crear torneo -->
    <v-row class="mt-6">
      <v-col cols="12" class="d-flex justify-end">
        <v-btn
          color="success"
          :loading="creating"
          :disabled="!canCreateTournament"
          variant="elevated"
          rounded="xl"
          size="large"
          @click="createTournament"
        >
          <v-icon start>mdi-check</v-icon>
          Crear torneo
        </v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
  import { computed, onMounted, ref } from 'vue'
  import { useRouter } from 'vue-router'
  import { useAppStore } from '@/stores/app'
  import TournamentForm from '@/components/TournamentForm.vue'
  import PlayerCard from '@/components/PlayerCard.vue'
  import TeamConfiguration from '@/components/TeamConfiguration.vue'
  import { samplePlayers } from '@/data/sampleData'
  import { handleApiError, playerAPI, tournamentAPI, gameTeamAPI } from '@/services/api'

  // Router
  const router = useRouter()
  const appStore = useAppStore()

  // Referencias
  const tournamentFormRef = ref(null)

  // Estado reactivo
  const activeTab = ref('participants')
  const tournamentValid = ref(false)
  const searchQuery = ref('')

  // Datos del torneo
  const tournamentData = ref({
    name: '',
    format: '1v1',
    total_teams: 8,
    teams_per_group: 4,
    has_group_stage: false,
    has_knockout: true,
    rules: '',
  })

  // Participantes
  const allPlayers = ref([])
  const participants = ref([])

  // Equipos
  const teams = ref([])
  const generatingTeams = ref(false)
  const teamGenerationMode = ref('automatic')
  const gameTeams = ref([])

  // Estado de creación
  const creating = ref(false)

  // Computed
  const filteredAvailablePlayers = computed(() => {
    const selectedIds = new Set(participants.value.map(p => p.id))
    let available = allPlayers.value.filter(player => !selectedIds.has(player.id))

    if (searchQuery.value) {
      const query = searchQuery.value.toLowerCase()
      available = available.filter(player =>
        player.display_name.toLowerCase().includes(query)
      )
    }

    return available
  })

  const canCreateTournament = computed(() => {
    return tournamentValid.value &&
           participants.value.length > 1 &&
           (tournamentData.value.format === '1v1' || teams.value.length > 0)
  })

  // Métodos
  const goBack = () => {
    router.push('/tournaments')
  }

  const handleTournamentValidChange = valid => {
    tournamentValid.value = valid
    if (valid && tournamentFormRef.value) {
      tournamentData.value = tournamentFormRef.value.getFormData()
    }
  }

  const addParticipant = (player) => {
    if (!participants.value.some(p => p.id === player.id)) {
      participants.value.push(player)
    }
  }

  const removeParticipant = (player) => {
    const index = participants.value.findIndex(p => p.id === player.id)
    if (index !== -1) {
      participants.value.splice(index, 1)
    }
  }

  const updateTeams = (newTeams) => {
    teams.value = newTeams
  }

  const updateTeamGenerationMode = (mode) => {
    teamGenerationMode.value = mode
  }

  const generateTeams = () => {
    generatingTeams.value = true
    setTimeout(() => {
      const shuffled = [...participants.value].sort(() => Math.random() - 0.5)
      teams.value = []

      for (let i = 0; i < shuffled.length; i += 2) {
        if (i + 1 < shuffled.length) {
          teams.value.push([shuffled[i], shuffled[i + 1]])
        } else {
          teams.value.push([shuffled[i]])
        }
      }

      generatingTeams.value = false
    }, 1000)
  }

  const createTournament = async () => {
    creating.value = true
    try {
      // Crear el torneo
      const tournamentResponse = await tournamentAPI.createTournament(tournamentData.value)
      const tournamentId = tournamentResponse.data.id

      // Crear las entradas de equipo
      if (tournamentData.value.format === '2v2') {
        // Para formato 2v2, crear entradas por equipo
        for (const team of teams.value) {
          const teamEntryData = {
            players: team.map(p => p.id),
          }
          await tournamentAPI.createTeamEntry(tournamentId, teamEntryData)
        }
      } else {
        // Para formato 1v1, crear una entrada por jugador
        for (const player of participants.value) {
          const teamEntryData = {
            players: [player.id],
          }
          await tournamentAPI.createTeamEntry(tournamentId, teamEntryData)
        }
      }

      // Asignar equipos automáticamente
      await tournamentAPI.assignRandomTeams(tournamentId)

      appStore.showSuccess('Torneo creado exitosamente')

      // Redirigir al torneo creado
      router.push(`/tournaments/${tournamentId}`)
    } catch (error) {
      const errorInfo = handleApiError(error)
      appStore.showError(`Error al crear torneo: ${errorInfo.message}`)
      console.error('Error al crear torneo:', errorInfo.message)
    } finally {
      creating.value = false
    }
  }

  // Cargar jugadores
  const loadPlayers = async () => {
    try {
      // Intentar cargar datos reales primero
      try {
        const response = await playerAPI.getPlayers()
        allPlayers.value = response.data
      } catch {
        console.log('API no disponible, usando datos de ejemplo')
        // Usar datos de ejemplo si la API no está disponible
        allPlayers.value = samplePlayers
      }
    } catch (error) {
      const errorInfo = handleApiError(error)
      appStore.showError(`Error al cargar jugadores: ${errorInfo.message}`)
      console.error('Error al cargar jugadores:', errorInfo.message)
    }
  }

  // Cargar equipos del juego
  const loadGameTeams = async () => {
    try {
      try {
        const response = await gameTeamAPI.getGameTeams()
        gameTeams.value = response.data
      } catch {
        console.log('API de equipos no disponible')
        gameTeams.value = []
      }
    } catch (error) {
      console.error('Error al cargar equipos del juego:', error)
      gameTeams.value = []
    }
  }

  // Cargar datos al montar el componente
  onMounted(() => {
    loadPlayers()
    loadGameTeams()
  })
</script>

<style scoped>
.players-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 16px;
}
</style>
