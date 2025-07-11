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
                Configura "{{ tournament.name }}"
              </p>
            </div>
          </div>
        </v-col>
      </v-row>

      <!-- Tabs principales -->
      <v-card>
        <v-tabs v-model="activeTab" color="primary" rounded="xl">
          <v-tab value="tournament">
            <v-icon start>mdi-trophy</v-icon>
            Información del Torneo
          </v-tab>
          <v-tab value="participants">
            <v-icon start>mdi-account-group</v-icon>
            Participantes
          </v-tab>
          <v-tab value="teams">
            <v-icon start>mdi-shield</v-icon>
            Configuración de Equipos
          </v-tab>
        </v-tabs>

        <v-window v-model="activeTab">
          <!-- Tab de información del torneo -->
          <v-window-item value="tournament">
            <v-card-text class="pa-6">
              <v-row>
                <v-col cols="12" md="8">
                  <v-card variant="outlined">
                    <v-card-title class="text-h6 pa-6 pb-0">
                      <v-icon start>mdi-trophy</v-icon>
                      Configuración del Torneo
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
                </v-col>

                <v-col cols="12" md="4">
                  <v-card variant="outlined">
                    <v-card-title class="text-h6">
                      <v-icon start>mdi-information</v-icon>
                      Resumen
                    </v-card-title>
                    <v-card-text>
                      <div class="mb-3">
                        <span class="text-body-2 text-grey-darken-1">Tipo:</span>
                        <div class="font-weight-medium">{{ getCompetitionTypeText(tournamentData.competition_type) }}</div>
                      </div>
                      <div class="mb-3">
                        <span class="text-body-2 text-grey-darken-1">Formato:</span>
                        <div class="font-weight-medium">{{ tournamentData.format }}</div>
                      </div>
                      <div class="mb-3">
                        <span class="text-body-2 text-grey-darken-1">Equipos:</span>
                        <div class="font-weight-medium">{{ tournamentData.total_teams }}</div>
                      </div>
                      <div v-if="showLeagueFields" class="mb-3">
                        <span class="text-body-2 text-grey-darken-1">Vueltas:</span>
                        <div class="font-weight-medium">{{ tournamentData.league_rounds }}</div>
                      </div>
                      <div v-if="showLeagueFields" class="mb-3">
                        <span class="text-body-2 text-grey-darken-1">Playoffs:</span>
                        <div class="font-weight-medium">{{ tournamentData.playoff_teams }} equipos</div>
                      </div>
                      <div v-if="showGroupFields" class="mb-3">
                        <span class="text-body-2 text-grey-darken-1">Por Grupo:</span>
                        <div class="font-weight-medium">{{ tournamentData.teams_per_group }} equipos</div>
                      </div>
                    </v-card-text>
                  </v-card>
                </v-col>
              </v-row>
            </v-card-text>
          </v-window-item>

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
                <TournamentParticipants
                  :all-players="allPlayers"
                  :participants="participants"
                  @update:participants="updateParticipants"
                />
              </div>
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
              <TournamentTeamConfiguration
                :participants="participants"
                :teams="teams"
                :tournament-format="tournamentData.format"
                :tournament-id="route.params.id"
                @format-change="updateTournamentFormat"
                @update:team-assignments="updateTeamAssignments"
                @update:team-entries="updateTeamEntries"
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
  import TournamentForm from '@/components/TournamentForm.vue'
  import TournamentParticipants from '@/components/TournamentParticipants.vue'
  import TournamentTeamConfiguration from '@/components/TournamentTeamConfiguration.vue'
  import { handleApiError, playerAPI, tournamentAPI } from '@/services/api'
  import { useAppStore } from '@/stores/app'

  // Router y Route
  const router = useRouter()
  const route = useRoute()
  const appStore = useAppStore()

  // Referencias
  const tournamentFormRef = ref(null)

  // Estado reactivo
  const activeTab = ref('tournament')
  const loading = ref(true)
  const saving = ref(false)
  const formValid = ref(false)
  const error = ref(null)

  // Datos del torneo
  const tournament = ref(null)
  const tournamentData = ref({
    name: '',
    format: '1v1',
    competition_type: 'cup',
    total_teams: 8,
    has_group_stage: false,
    has_knockout: true,
    teams_per_group: 4,
    league_rounds: 1,
    playoff_teams: 4,
    rules: '',
  })

  // Participantes
  const allPlayers = ref([])
  const participants = ref([])

  // Equipos
  const teams = ref([])
  const teamAssignments = ref({})
  const teamEntries = ref([])

  // Estado del torneo
  const tournamentHasMatches = ref(false)

  // Computed
  const canSaveChanges = computed(() => {
    return formValid.value && participants.value.length > 1
  })

  const showLeagueFields = computed(() => {
    return tournamentData.value.competition_type === 'league' || tournamentData.value.competition_type === 'hybrid'
  })

  const showGroupFields = computed(() => {
    return tournamentData.value.competition_type === 'groups'
  })

  // Métodos
  const getCompetitionTypeText = type => {
    const typeMap = {
      cup: 'Copa (Eliminatoria directa)',
      league: 'Liga (Todos contra todos)',
      hybrid: 'Liga + Playoffs',
      groups: 'Fase de grupos + Eliminatoria',
    }
    return typeMap[type] || 'Desconocido'
  }

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
        competition_type: tournament.value.competition_type || 'cup',
        total_teams: tournament.value.total_teams || 8,
        has_group_stage: tournament.value.has_group_stage || false,
        has_knockout: tournament.value.has_knockout === undefined ? true : tournament.value.has_knockout,
        teams_per_group: tournament.value.teams_per_group || 4,
        league_rounds: tournament.value.league_rounds || 1,
        playoff_teams: tournament.value.playoff_teams || 4,
        rules: tournament.value.rules || '',
      }

      // Verificar si hay partidos generados
      try {
        const matchesResponse = await tournamentAPI.getTournamentMatches(tournamentId)
        tournamentHasMatches.value = matchesResponse.data.length > 0
      } catch {
        tournamentHasMatches.value = false
      }

      // Cargar participantes del torneo
      await loadTournamentParticipants(tournamentId)
    } catch (error_) {
      const errorInfo = handleApiError(error_)
      error.value = errorInfo.message
      appStore.showError(`Error al cargar torneo: ${errorInfo.message}`)
      console.error('Error al cargar torneo:', errorInfo.message)
    } finally {
      loading.value = false
    }
  }

  // Cargar participantes del torneo
  const loadTournamentParticipants = async tournamentId => {
    try {
      const entriesResponse = await tournamentAPI.getTeamEntries(tournamentId)
      const entries = entriesResponse.data

      // Extraer participantes únicos de las entradas
      const participantMap = new Map()
      for (const entry of entries) {
        if (entry.players) {
          for (const player of entry.players) {
            if (!participantMap.has(player.id)) {
              participantMap.set(player.id, player)
            }
          }
        }
      }

      participants.value = Array.from(participantMap.values())
    } catch (error) {
      console.error('Error al cargar participantes:', error)
      participants.value = []
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
  const updateParticipants = newParticipants => {
    participants.value = newParticipants
  }

  // Métodos de equipos
  const updateTeams = newTeams => {
    teams.value = newTeams
  }

  const updateTeamAssignments = newAssignments => {
    teamAssignments.value = newAssignments
  }

  const updateTeamEntries = newEntries => {
    teamEntries.value = newEntries
  }

  const updateTournamentFormat = newFormat => {
    tournamentData.value.format = newFormat
  }

  // Guardar cambios
  const saveTournament = async () => {
    saving.value = true
    try {
      // Actualizar datos del torneo
      const formData = tournamentFormRef.value.getFormData()
      await tournamentAPI.updateTournament(tournament.value.id, formData)

      // Si no hay partidos generados, actualizar participantes
      if (!tournamentHasMatches.value) {
        await updateTournamentParticipants()
      }

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

  // Actualizar participantes del torneo
  const updateTournamentParticipants = async () => {
    try {
      const tournamentId = tournament.value.id

      // Eliminar entradas existentes
      const existingEntries = await tournamentAPI.getTeamEntries(tournamentId)
      for (const entry of existingEntries.data) {
        await tournamentAPI.deleteTeamEntry(entry.id)
      }

      // Crear nuevas entradas usando el formato correcto
      for (const entry of teamEntries.value) {
        await tournamentAPI.createTeamEntry(tournamentId, {
          players: entry.players,
          assigned_team: entry.assigned_team,
          // NO incluir tournament aquí - el backend lo maneja automáticamente
        })
      }

      console.log('Participantes actualizados exitosamente')
    } catch (error) {
      console.error('Error al actualizar participantes:', error)
      throw error
    }
  }

  // Cargar jugadores
  const loadPlayers = async () => {
    try {
      const response = await playerAPI.getPlayers()
      allPlayers.value = response.data
    } catch (error) {
      const errorInfo = handleApiError(error)
      appStore.showError(`Error al cargar jugadores: ${errorInfo.message}`)
      console.error('Error al cargar jugadores:', errorInfo.message)
      allPlayers.value = []
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
