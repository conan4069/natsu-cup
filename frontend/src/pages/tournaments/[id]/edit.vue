<template>
  <v-container fluid>
    <!-- Loading state -->
    <div v-if="loading" class="d-flex justify-center align-center" style="min-height: 400px;">
      <v-progress-circular color="primary" indeterminate size="64" />
    </div>

    <!-- Error state -->
    <div v-else-if="error" class="text-center py-8">
      <v-icon class="mb-4" color="error" size="64">mdi-alert-circle</v-icon>
      <h3 class="text-h6 text-grey-darken-1 mb-2">Error al cargar torneo</h3>
      <p class="text-body-2 text-grey-darken-1 mb-4">{{ error }}</p>
      <v-btn color="primary" rounded="xl" @click="loadTournament">Reintentar</v-btn>
    </div>

    <!-- Edit form -->
    <div v-else-if="tournament">
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
            <div class="flex-grow-1">
              <h1 class="text-h4 font-weight-bold mb-2">Editar Torneo</h1>
              <p class="text-body-1 text-grey-darken-1">
                Modifica la información del torneo "{{ tournament.name }}"
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
            mode="edit"
            :readonly="tournamentHasMatches"
            :tournament="tournament"
            @valid-change="handleValidChange"
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
              <v-alert
                v-if="tournamentHasMatches"
                class="mb-4"
                type="warning"
                variant="tonal"
              >
                <strong>Advertencia:</strong> No se pueden cambiar los participantes porque ya se han generado partidos.
              </v-alert>

              <div v-if="!tournamentHasMatches">
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
                        :is-selected="false"
                        :player="player"
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
                        :is-selected="true"
                        :player="player"
                        @toggle-selection="removeParticipant"
                      />
                    </div>
                  </v-card-text>
                </v-card>
              </div>

              <!-- Vista de solo lectura si hay partidos -->
              <div v-else>
                <v-card variant="outlined">
                  <v-card-title class="text-subtitle-1">
                    Participantes actuales ({{ participants.length }})
                  </v-card-title>
                  <v-card-text>
                    <div class="players-grid">
                      <PlayerCard
                        v-for="player in participants"
                        :key="player.id"
                        :is-selected="true"
                        :player="player"
                        @toggle-selection="() => {}"
                      />
                    </div>
                  </v-card-text>
                </v-card>
              </div>
            </v-card-text>
          </v-window-item>

          <!-- Tab de configuración de equipos -->
          <v-window-item value="teams">
            <v-card-text class="pa-6">
              <TeamConfiguration
                :generating-teams="generatingTeams"
                :participants="participants"
                :teams="teams"
                :tournament-format="tournamentData.format"
                @generate-teams="generateTeams"
                @update:team-generation-mode="updateTeamGenerationMode"
                @update:teams="updateTeams"
              />
            </v-card-text>
          </v-window-item>
        </v-window>
      </v-card>

      <!-- Botón de guardar cambios -->
      <v-row class="mt-6">
        <v-col class="d-flex justify-end" cols="12">
          <v-btn
            color="primary"
            :disabled="!canSaveChanges"
            :loading="saving"
            rounded="xl"
            size="large"
            variant="elevated"
            @click="saveTournament"
          >
            <v-icon start>mdi-content-save</v-icon>
            Guardar cambios
          </v-btn>
        </v-col>
      </v-row>
    </div>
  </v-container>
</template>

<script setup>
  import { computed, onMounted, ref } from 'vue'
  import { useRoute, useRouter } from 'vue-router'
  import PlayerCard from '@/components/PlayerCard.vue'
  import TeamConfiguration from '@/components/TeamConfiguration.vue'
  import TournamentForm from '@/components/TournamentForm.vue'
  import { samplePlayers } from '@/data/sampleData'
  import { handleApiError, playerAPI, tournamentAPI } from '@/services/api'
  import { useAppStore } from '@/stores/app'

  // Router y Route
  const router = useRouter()
  const route = useRoute()
  const appStore = useAppStore()

  // Referencias
  const tournamentFormRef = ref(null)

  // Estado reactivo
  const activeTab = ref('participants')
  const loading = ref(true)
  const saving = ref(false)
  const formValid = ref(false)
  const error = ref(null)
  const searchQuery = ref('')

  // Datos del torneo
  const tournament = ref(null)
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

  // Estado del torneo
  const tournamentHasMatches = ref(false)

  // Computed
  const filteredAvailablePlayers = computed(() => {
    const selectedIds = new Set(participants.value.map(p => p.id))
    let available = allPlayers.value.filter(player => !selectedIds.has(player.id))

    if (searchQuery.value) {
      const query = searchQuery.value.toLowerCase()
      available = available.filter(player =>
        player.display_name.toLowerCase().includes(query),
      )
    }

    return available
  })

  const canSaveChanges = computed(() => {
    return formValid.value
      && participants.value.length > 1
      && (tournamentData.value.format === '1v1' || teams.value.length > 0)
  })

  // Cargar torneo
  const loadTournament = async () => {
    const tournamentId = route.params.id

    loading.value = true
    error.value = null

    try {
      const response = await tournamentAPI.getTournament(tournamentId)
      tournament.value = response.data
      tournamentData.value = {
        name: tournament.value.name || '',
        format: tournament.value.format || '1v1',
        total_teams: tournament.value.total_teams || 8,
        teams_per_group: tournament.value.teams_per_group || 4,
        has_group_stage: tournament.value.has_group_stage || false,
        has_knockout: tournament.value.has_knockout === undefined ? true : tournament.value.has_knockout,
        rules: tournament.value.rules || '',
      }

      // Verificar si hay partidos generados
      try {
        const matchesResponse = await tournamentAPI.getTournamentMatches(tournamentId)
        tournamentHasMatches.value = matchesResponse.data.length > 0
      } catch {
        tournamentHasMatches.value = false
      }

      // Cargar participantes (simulado por ahora)
      participants.value = samplePlayers.slice(0, 8)
    } catch (error_) {
      const errorInfo = handleApiError(error_)
      error.value = errorInfo.message
      appStore.showError(`Error al cargar torneo: ${errorInfo.message}`)
      console.error('Error al cargar torneo:', errorInfo.message)
    } finally {
      loading.value = false
    }
  }

  // Navegación
  const goBack = () => {
    router.push(`/tournaments/${route.params.id}`)
  }

  // Validación del formulario
  const handleValidChange = valid => {
    formValid.value = valid
  }

  // Métodos de participantes
  const addParticipant = player => {
    if (!tournamentHasMatches.value && !participants.value.some(p => p.id === player.id)) {
      participants.value.push(player)
    }
  }

  const removeParticipant = player => {
    if (!tournamentHasMatches.value) {
      const index = participants.value.findIndex(p => p.id === player.id)
      if (index !== -1) {
        participants.value.splice(index, 1)
      }
    }
  }

  const updateTeams = newTeams => {
    teams.value = newTeams
  }

  const updateTeamGenerationMode = mode => {
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

  // Guardar cambios
  const saveTournament = async () => {
    saving.value = true
    try {
      const formData = tournamentFormRef.value.getFormData()
      await tournamentAPI.updateTournament(tournament.value.id, formData)

      appStore.showSuccess('Torneo actualizado exitosamente')
      router.push(`/tournaments/${tournament.value.id}`)
    } catch (error_) {
      const errorInfo = handleApiError(error_)
      appStore.showError(`Error al actualizar torneo: ${errorInfo.message}`)
      console.error('Error al actualizar torneo:', errorInfo.message)
    } finally {
      saving.value = false
    }
  }

  // Cargar jugadores
  const loadPlayers = async () => {
    try {
      try {
        const response = await playerAPI.getPlayers()
        allPlayers.value = response.data
      } catch {
        console.log('API no disponible, usando datos de ejemplo')
        allPlayers.value = samplePlayers
      }
    } catch (error) {
      const errorInfo = handleApiError(error)
      appStore.showError(`Error al cargar jugadores: ${errorInfo.message}`)
      console.error('Error al cargar jugadores:', errorInfo.message)
    }
  }

  // Cargar datos al montar
  onMounted(() => {
    loadTournament()
    loadPlayers()
  })
</script>

<style scoped>
.players-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 16px;
}
</style>
