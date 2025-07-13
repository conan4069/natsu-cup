<template>
  <div class="tournament-teams">
    <!-- Loading state -->
    <div v-if="loading" class="d-flex justify-center align-center" style="min-height: 200px;">
      <v-progress-circular color="primary" indeterminate size="48" />
    </div>

    <!-- Error state -->
    <div v-else-if="error" class="text-center py-6">
      <v-icon class="mb-3" color="error" size="48">mdi-alert-circle</v-icon>
      <h4 class="text-h6 text-grey-darken-1 mb-2">Error al cargar equipos</h4>
      <p class="text-body-2 text-grey-darken-1 mb-3">{{ error }}</p>
      <v-btn color="primary" rounded="xl" size="small" @click="loadTeamEntries">Reintentar</v-btn>
    </div>

    <!-- Team entries -->
    <div v-else>
      <v-card>
        <v-card-title class="text-h6 d-flex align-center justify-space-between">
          <span>
            <v-icon start>mdi-account-group</v-icon>
            Equipos del Torneo ({{ teamEntries.length }})
          </span>
          <!-- Mostrar botón solo si hay equipos sin asignar -->
          <v-btn
            v-if="hasUnassignedTeams"
            color="primary"
            :loading="assigningTeams"
            prepend-icon="mdi-shuffle"
            rounded="xl"
            size="small"
            variant="elevated"
            @click="assignTeamsRandomly"
          >
            Asignar equipos aleatoriamente
          </v-btn>
        </v-card-title>
        <v-card-text>
          <div v-if="teamEntries.length === 0" class="text-center py-8">
            <v-icon class="mb-4" color="grey-lighten-1" size="48">
              mdi-account-group
            </v-icon>
            <h4 class="text-h6 text-grey-darken-1 mb-2">
              No hay equipos registrados
            </h4>
            <p class="text-body-2 text-grey-darken-1">
              Los equipos aparecerán aquí cuando se registren en el torneo.
            </p>
          </div>
          <v-list v-else>
            <v-list-item
              v-for="entry in teamEntries"
              :key="entry.id"
              class="mb-3"
            >
              <template #prepend>
                <v-avatar size="40">
                  <v-img
                    v-if="entry.assigned_team?.logo && entry.assigned_team.logo !== 'null'"
                    alt="Logo"
                    :src="entry.assigned_team.logo"
                  />
                  <v-icon v-else>mdi-shield</v-icon>
                </v-avatar>
              </template>

              <v-list-item-title class="mb-2">
                <strong>{{ entry.assigned_team?.name || 'Sin equipo asignado' }}</strong>
              </v-list-item-title>

              <v-list-item-subtitle>
                <div class="d-flex align-center mb-2">
                  <v-icon class="mr-1" size="16">mdi-account</v-icon>
                  <span>{{ entry.players?.length || 0 }} jugador(es)</span>
                </div>

                <!-- Lista de participantes -->
                <div v-if="entry.players && entry.players.length > 0" class="participants-list">
                  <div class="d-flex flex-wrap gap-1">
                    <v-chip
                      v-for="player in entry.players"
                      :key="player.id"
                      class="ma-1"
                      color="primary"
                      label
                      size="small"
                      variant="outlined"
                    >
                      <v-avatar v-if="player.avatar && player.avatar !== 'null'" left size="16">
                        <v-img :src="player.avatar" />
                      </v-avatar>
                      <v-icon v-else left size="16">mdi-account</v-icon>
                      {{ player.display_name || player.name || 'Sin nombre' }}
                    </v-chip>
                  </div>
                </div>

                <div v-else class="text-grey-darken-1 text-caption">
                  No hay participantes registrados
                </div>
              </v-list-item-subtitle>

              <template #append>
                <v-chip
                  v-if="entry.assigned_team"
                  color="primary"
                  size="small"
                  variant="outlined"
                >
                  {{ entry.assigned_team.name }}
                </v-chip>
                <v-chip
                  v-else
                  color="grey"
                  size="small"
                  variant="outlined"
                >
                  Sin asignar
                </v-chip>
              </template>
            </v-list-item>
          </v-list>
        </v-card-text>
      </v-card>
    </div>
  </div>
</template>

<script setup>
  import { computed, onMounted, ref, watch } from 'vue'
  import { handleApiError, tournamentAPI } from '@/services/api'

  // Props
  const props = defineProps({
    tournamentId: {
      type: [String, Number],
      required: true,
    },
  })

  // Emits
  const emit = defineEmits(['teams-updated'])

  // Estado reactivo
  const teamEntries = ref([])
  const loading = ref(true)
  const error = ref(null)
  const assigningTeams = ref(false)

  // Computed para verificar si hay equipos sin asignar
  const hasUnassignedTeams = computed(() => {
    return teamEntries.value.some(entry => !entry.assigned_team)
  })

  // Cargar entradas de equipos
  const loadTeamEntries = async () => {
    loading.value = true
    error.value = null

    try {
      const entriesResponse = await tournamentAPI.getTeamEntries(props.tournamentId)
      teamEntries.value = entriesResponse.data
      console.log('Entradas de equipos cargadas:', teamEntries.value)
    } catch (error_) {
      const errorInfo = handleApiError(error_)
      error.value = errorInfo.message
      console.error('Error al cargar entradas:', errorInfo.message)
    } finally {
      loading.value = false
    }
  }

  // Asignar equipos aleatoriamente
  const assignTeamsRandomly = async () => {
    assigningTeams.value = true
    try {
      await tournamentAPI.assignRandomTeams(props.tournamentId)

      // Recargar entradas para ver los cambios
      await loadTeamEntries()

      // Emitir evento de actualización
      emit('teams-updated')

      console.log('Equipos asignados aleatoriamente')
    } catch (error_) {
      const errorInfo = handleApiError(error_)
      console.error('Error al asignar equipos:', errorInfo.message)
    } finally {
      assigningTeams.value = false
    }
  }

  // Observar cambios en tournamentId
  watch(() => props.tournamentId, newId => {
    if (newId) {
      loadTeamEntries()
    }
  })

  // Cargar datos al montar el componente
  onMounted(() => {
    if (props.tournamentId) {
      loadTeamEntries()
    }
  })
</script>

<style scoped>
.tournament-teams {
  width: 100%;
}

.participants-list {
  margin-top: 8px;
}
</style>
