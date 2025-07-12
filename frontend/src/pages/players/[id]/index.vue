<template>
  <v-container fluid>
    <!-- Loading state -->
    <div v-if="loading" class="d-flex justify-center align-center" style="min-height: 400px;">
      <v-progress-circular color="primary" indeterminate size="64" />
    </div>

    <!-- Error state -->
    <div v-else-if="error" class="text-center py-8">
      <v-icon class="mb-4" color="error" size="64">mdi-alert-circle</v-icon>
      <h3 class="text-h6 text-grey-darken-1 mb-2">Error al cargar jugador</h3>
      <p class="text-body-2 text-grey-darken-1 mb-4">{{ error }}</p>
      <v-btn color="primary" @click="loadPlayer">Reintentar</v-btn>
    </div>

    <!-- Player details -->
    <div v-else-if="player">
      <!-- Header -->
      <v-row class="mb-6">
        <v-col cols="12">
          <div class="d-flex align-center mb-4">
            <v-btn
              class="mr-4"
              color="white"
              icon="mdi-arrow-left"
              variant="text"
              @click="goBack"
            />
            <div class="d-flex align-center">
              <v-avatar class="mr-4" size="80">
                <v-img
                  v-if="player.avatar"
                  alt="Avatar del jugador"
                  :src="player.avatar"
                />
                <v-icon v-else color="grey" size="40">
                  mdi-account
                </v-icon>
              </v-avatar>
              <div>
                <h1 class="text-h4 font-weight-bold mb-2" style="color: #f3f2e5;">{{ player.display_name }}</h1>
                <p class="text-body-1" style="color: #deddd6;">
                  Jugador
                </p>
              </div>
            </div>
          </div>
        </v-col>
      </v-row>

      <!-- Content -->
      <v-row>
        <!-- Player info card -->
        <v-col cols="12" md="6">
          <v-card>
            <v-card-title class="text-h6">
              <v-icon start>mdi-account-details</v-icon>
              Información del Jugador
            </v-card-title>
            <v-card-text>
              <v-list>
                <v-list-item>
                  <template #prepend>
                    <v-icon color="primary">mdi-account</v-icon>
                  </template>
                  <v-list-item-title>Nombre</v-list-item-title>
                  <v-list-item-subtitle>{{ player.display_name }}</v-list-item-subtitle>
                </v-list-item>
                <v-list-item v-if="player.avatar">
                  <template #prepend>
                    <v-icon color="primary">mdi-image</v-icon>
                  </template>
                  <v-list-item-title>Imagen</v-list-item-title>
                  <v-list-item-subtitle>Retrato del jugador</v-list-item-subtitle>
                </v-list-item>
              </v-list>
            </v-card-text>
            <v-card-actions>
              <v-spacer />
              <v-btn
                color="warning"
                prepend-icon="mdi-pencil"
                rounded="xl"
                variant="outlined"

                @click="editPlayer"
              >
                Editar
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-col>

        <!-- Statistics card -->
        <v-col cols="12" md="6">
          <v-card>
            <v-card-title class="text-h6">
              <v-icon start>mdi-chart-line</v-icon>
              Estadísticas
            </v-card-title>
            <v-card-text>
              <v-row>
                <v-col cols="6">
                  <div class="text-center">
                    <div class="text-h4 font-weight-bold text-primary mb-2">
                      {{ stats.tournaments || 0 }}
                    </div>
                    <div class="text-caption text-grey-darken-1">
                      Torneos Participados
                    </div>
                  </div>
                </v-col>
                <v-col cols="6">
                  <div class="text-center">
                    <div class="text-h4 font-weight-bold text-success mb-2">
                      {{ stats.matches || 0 }}
                    </div>
                    <div class="text-caption text-grey-darken-1">
                      Partidos Jugados
                    </div>
                  </div>
                </v-col>
                <v-col cols="6">
                  <div class="text-center">
                    <div class="text-h4 font-weight-bold text-warning mb-2">
                      {{ stats.wins || 0 }}
                    </div>
                    <div class="text-caption text-grey-darken-1">
                      Victorias
                    </div>
                  </div>
                </v-col>
                <v-col cols="6">
                  <div class="text-center">
                    <div class="text-h4 font-weight-bold text-error mb-2">
                      {{ stats.losses || 0 }}
                    </div>
                    <div class="text-caption text-grey-darken-1">
                      Derrotas
                    </div>
                  </div>
                </v-col>
              </v-row>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>

      <!-- Recent tournaments -->
      <v-row class="mt-6">
        <v-col cols="12">
          <v-card>
            <v-card-title class="text-h6">
              <v-icon start>mdi-trophy</v-icon>
              Torneos Recientes
            </v-card-title>
            <v-card-text>
              <div v-if="recentTournaments.length === 0" class="text-center py-8">
                <v-icon class="mb-4" color="grey-lighten-1" size="48">
                  mdi-trophy-outline
                </v-icon>
                <h4 class="text-h6 text-grey-darken-1 mb-2">
                  No hay torneos registrados
                </h4>
                <p class="text-body-2 text-grey-darken-1">
                  Este jugador aún no ha participado en ningún torneo.
                </p>
              </div>
              <v-list v-else>
                <v-list-item
                  v-for="tournament in recentTournaments"
                  :key="tournament.id"
                  :subtitle="`Formato: ${tournament.format}`"
                  :title="tournament.name"
                >
                  <template #prepend>
                    <v-icon color="primary">mdi-trophy</v-icon>
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
  import { handleApiError, playerAPI } from '@/services/api'

  // Router y Route
  const router = useRouter()
  const route = useRoute()

  // Estado reactivo
  const player = ref(null)
  const loading = ref(true)
  const error = ref(null)
  const stats = ref({
    tournaments: 0,
    matches: 0,
    wins: 0,
    losses: 0,
  })
  const recentTournaments = ref([])

  // Cargar jugador
  const loadPlayer = async () => {
    const playerId = route.params.id

    loading.value = true
    error.value = null

    try {
      const response = await playerAPI.getPlayer(playerId)
      player.value = response.data

      // Aquí podrías cargar estadísticas y torneos recientes
      // Por ahora usamos datos de ejemplo
      stats.value = {
        tournaments: Math.floor(Math.random() * 5) + 1,
        matches: Math.floor(Math.random() * 20) + 5,
        wins: Math.floor(Math.random() * 10) + 2,
        losses: Math.floor(Math.random() * 8) + 1,
      }

      recentTournaments.value = [
        { id: 1, name: 'Natsu Cup 2024', format: '1v1' },
        { id: 2, name: 'Torneo de Verano', format: '2v2' },
      ]
    } catch (error_) {
      const errorInfo = handleApiError(error_)
      error.value = errorInfo.message
      console.error('Error al cargar jugador:', errorInfo.message)
    } finally {
      loading.value = false
    }
  }

  // Navegación
  const goBack = () => {
    router.push('/players')
  }

  const editPlayer = () => {
    router.push(`/players/${player.value.id}/edit`)
  }

  // Cargar datos al montar el componente
  onMounted(() => {
    loadPlayer()
  })
</script>

<style scoped>
/* Estilos específicos si son necesarios */
</style>
