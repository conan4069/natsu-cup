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
      <v-btn color="primary" @click="loadTournament">Reintentar</v-btn>
    </div>

    <!-- Tournament teams management -->
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
            <div>
              <h1 class="text-h4 font-weight-bold mb-2">{{ tournament.name }}</h1>
              <p class="text-body-1 text-grey-darken-1">
                Gestión de Equipos - {{ tournament.format }}
              </p>
            </div>
          </div>
        </v-col>
      </v-row>

      <!-- Team entries -->
      <v-row>
        <v-col cols="12">
          <v-card>
            <v-card-title class="text-h6 d-flex align-center justify-space-between">
              <span>
                <v-icon start>mdi-account-group</v-icon>
                Equipos del Torneo ({{ teamEntries.length }})
              </span>
              <v-btn
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
                        v-if="entry.assigned_team?.logo"
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
                          <v-avatar v-if="player.avatar" left size="16">
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
        </v-col>
      </v-row>
    </div>
  </v-container>
</template>

<script setup>
  import { onMounted, ref } from 'vue'
  import { useRoute, useRouter } from 'vue-router'
  import { handleApiError, tournamentAPI } from '@/services/api'

  // Router y Route
  const router = useRouter()
  const route = useRoute()

  // Estado reactivo
  const tournament = ref(null)
  const teamEntries = ref([])
  const loading = ref(true)
  const error = ref(null)
  const assigningTeams = ref(false)

  // Cargar torneo
  const loadTournament = async () => {
    const tournamentId = route.params.id

    loading.value = true
    error.value = null

    try {
      console.log('Cargando torneo con ID:', tournamentId)

      // Cargar datos del torneo
      const tournamentResponse = await tournamentAPI.getTournament(tournamentId)
      tournament.value = tournamentResponse.data
      console.log('Datos del torneo cargados:', tournament.value)

      // Cargar entradas de equipos
      try {
        const entriesResponse = await tournamentAPI.getTeamEntries(tournamentId)
        teamEntries.value = entriesResponse.data
        console.log('Entradas de equipos cargadas:', teamEntries.value)
      } catch (entriesError) {
        console.error('Error al cargar entradas:', entriesError)
        teamEntries.value = []
      }
    } catch (error_) {
      const errorInfo = handleApiError(error_)
      error.value = errorInfo.message
      console.error('Error al cargar torneo:', errorInfo.message)
    } finally {
      loading.value = false
    }
  }

  // Asignar equipos aleatoriamente
  const assignTeamsRandomly = async () => {
    assigningTeams.value = true
    try {
      await tournamentAPI.assignRandomTeams(tournament.value.id)

      // Recargar entradas para ver los cambios
      const entriesResponse = await tournamentAPI.getTeamEntries(tournament.value.id)
      teamEntries.value = entriesResponse.data

      console.log('Equipos asignados aleatoriamente')
    } catch (error_) {
      const errorInfo = handleApiError(error_)
      console.error('Error al asignar equipos:', errorInfo.message)
    } finally {
      assigningTeams.value = false
    }
  }

  // Navegación
  const goBack = () => {
    router.push(`/tournaments/${route.params.id}`)
  }

  // Cargar datos al montar el componente
  onMounted(() => {
    loadTournament()
  })
</script>

<style scoped>
/* Estilos específicos si son necesarios */
</style>
