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

    <!-- Tournament groups -->
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
                Fase de Grupos - {{ tournament.format }}
              </p>
            </div>
          </div>
        </v-col>
      </v-row>

      <!-- Tournament info -->
      <v-row class="mb-6">
        <v-col cols="12" md="4">
          <v-card>
            <v-card-title class="text-h6">
              <v-icon start>mdi-information</v-icon>
              Información del Torneo
            </v-card-title>
            <v-card-text>
              <div class="d-flex justify-space-between mb-2">
                <span class="text-body-2 text-grey-darken-1">Formato:</span>
                <span class="font-weight-medium">{{ tournament.format }}</span>
              </div>
              <div class="d-flex justify-space-between mb-2">
                <span class="text-body-2 text-grey-darken-1">Equipos:</span>
                <span class="font-weight-medium">{{ tournament.team_count || 0 }}</span>
              </div>
              <div class="d-flex justify-space-between mb-2">
                <span class="text-body-2 text-grey-darken-1">Estado:</span>
                <v-chip
                  :color="tournament.status === 'completed' ? 'success' : 'warning'"
                  size="small"
                  variant="outlined"
                >
                  {{ tournament.status === 'completed' ? 'Completado' : 'En progreso' }}
                </v-chip>
              </div>
              <div class="d-flex justify-space-between">
                <span class="text-body-2 text-grey-darken-1">Partidos jugados:</span>
                <span class="font-weight-medium">{{ playedMatches }}/{{ totalMatches }}</span>
              </div>
            </v-card-text>
          </v-card>
        </v-col>

        <v-col cols="12" md="8">
          <v-card>
            <v-card-title class="text-h6">
              <v-icon start>mdi-chart-line</v-icon>
              Progreso de Grupos
            </v-card-title>
            <v-card-text>
              <div class="d-flex align-center mb-4">
                <div class="flex-grow-1 mr-4">
                  <v-progress-linear
                    color="primary"
                    height="8"
                    :model-value="progressPercentage"
                    rounded
                  />
                </div>
                <span class="text-body-2 font-weight-medium">
                  {{ Math.round(progressPercentage) }}%
                </span>
              </div>

              <div class="d-flex justify-space-between text-caption text-grey-darken-1">
                <span>Grupos Generados</span>
                <span>Partidos Jugados</span>
                <span>Clasificados</span>
              </div>

              <div class="d-flex justify-space-between mt-2">
                <v-chip
                  :color="groupsGenerated ? 'success' : 'grey'"
                  size="small"
                  variant="outlined"
                >
                  {{ groupsGenerated ? 'Sí' : 'No' }}
                </v-chip>
                <v-chip
                  :color="progressPercentage > 0 ? 'warning' : 'grey'"
                  size="small"
                  variant="outlined"
                >
                  {{ playedMatches }}/{{ totalMatches }}
                </v-chip>
                <v-chip
                  :color="bracketReady ? 'success' : 'grey'"
                  size="small"
                  variant="outlined"
                >
                  {{ bracketReady ? 'Listo' : 'Pendiente' }}
                </v-chip>
              </div>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>

      <!-- Groups component -->
      <TournamentGroups
        :tournament="tournament"
      />
    </div>
  </v-container>
</template>

<script setup>
  import { computed, onMounted, ref } from 'vue'
  import { useRoute, useRouter } from 'vue-router'
  import TournamentGroups from '@/components/TournamentGroups.vue'
  import { handleApiError, matchAPI, tournamentAPI } from '@/services/api'

  // Router y Route
  const router = useRouter()
  const route = useRoute()

  // Estado reactivo
  const tournament = ref(null)
  const matches = ref([])
  const loading = ref(true)
  const error = ref(null)

  // Computed
  const totalMatches = computed(() => {
    return matches.value.length
  })

  const playedMatches = computed(() => {
    return matches.value.filter(match => match.played).length
  })

  const progressPercentage = computed(() => {
    if (totalMatches.value === 0) return 0
    return (playedMatches.value / totalMatches.value) * 100
  })

  const groupsGenerated = computed(() => {
    // Verificar si hay partidos de grupos
    return matches.value.some(match => match.stage === 'group')
  })

  const bracketReady = computed(() => {
    // Verificar si todos los partidos de grupos están completados
    const groupMatches = matches.value.filter(match => match.stage === 'group')
    return groupMatches.length > 0 && groupMatches.every(match => match.played)
  })

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

      // Cargar partidos del torneo
      try {
        const matchesResponse = await matchAPI.getTournamentMatches(tournamentId)
        matches.value = matchesResponse.data
        console.log('Partidos del torneo cargados:', matches.value)
      } catch (matchesError) {
        console.error('Error al cargar partidos:', matchesError)
        matches.value = []
      }
    } catch (error_) {
      const errorInfo = handleApiError(error_)
      error.value = errorInfo.message
      console.error('Error al cargar torneo:', errorInfo.message)
    } finally {
      loading.value = false
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
