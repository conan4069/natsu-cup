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
              <h1 class="text-h4 font-weight-bold mb-2 page-title">{{ tournament.name }}</h1>
              <p class="text-body-1 page-subtitle">
                Fase de Grupos - {{ tournament.format }}
              </p>
            </div>
          </div>
        </v-col>
      </v-row>

      <!-- Tournament info -->
      <v-row>
        <v-col cols="12" md="8">
          <v-card>
            <v-card-title class="text-h6">
              <v-icon start>mdi-information</v-icon>
              Información de Grupos
            </v-card-title>
            <v-card-text>
              <div class="text-center py-8">
                <v-icon class="mb-4" color="primary" size="64">mdi-account-group</v-icon>
                <h3 class="text-h5 mb-2">Fase de Grupos</h3>
                <p class="text-body-1 text-grey-darken-1 mb-4">
                  Aquí se mostrarán los grupos del torneo cuando estén configurados
                </p>
                <v-btn
                  color="primary"
                  prepend-icon="mdi-account-group"
                  rounded="xl"
                  variant="elevated"
                  @click="configureGroups"
                >
                  Configurar Grupos
                </v-btn>
              </div>
            </v-card-text>
          </v-card>
        </v-col>

        <v-col cols="12" md="4">
          <v-card>
            <v-card-title class="text-h6">
              <v-icon start>mdi-chart-line</v-icon>
              Estadísticas de Grupos
            </v-card-title>
            <v-card-text>
              <div class="mb-3">
                <span class="text-body-2 text-grey-darken-1">Grupos:</span>
                <div class="font-weight-medium">{{ tournament.groups_count || 0 }}</div>
              </div>
              <div class="mb-3">
                <span class="text-body-2 text-grey-darken-1">Equipos por grupo:</span>
                <div class="font-weight-medium">{{ tournament.teams_per_group || 0 }}</div>
              </div>
              <div class="mb-3">
                <span class="text-body-2 text-grey-darken-1">Partidos jugados:</span>
                <div class="font-weight-medium">{{ tournament.matches_played || 0 }}</div>
              </div>
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
  import { useAppStore } from '@/stores/app'

  // Router y Route
  const router = useRouter()
  const route = useRoute()
  const appStore = useAppStore()

  // Estado reactivo
  const loading = ref(true)
  const error = ref(null)
  const tournament = ref(null)

  // Cargar torneo
  const loadTournament = async () => {
    const tournamentId = route.params.id

    loading.value = true
    error.value = null

    try {
      const response = await tournamentAPI.getTournament(tournamentId)
      tournament.value = response.data
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

  const configureGroups = () => {
    // TODO: Implementar configuración de grupos
    console.log('Configurar grupos')
  }

  // Cargar datos al montar
  onMounted(() => {
    loadTournament()
  })
</script>

<style scoped>
.page-title {
  color: white !important;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
}

.page-subtitle {
  color: #f3f2e5 !important;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
}
</style>
