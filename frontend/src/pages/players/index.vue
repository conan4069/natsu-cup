<template>
  <v-container fluid>
    <!-- Header con título y botón de crear -->
    <v-row class="mb-6">
      <v-col cols="12">
        <div class="d-flex align-center justify-space-between">
          <div>
            <h1 class="text-h4 font-weight-bold mb-2 page-title">Jugadores</h1>
            <p class="text-body-1 page-subtitle">
              Gestiona los jugadores del campeonato
            </p>
          </div>
          <v-btn
            color="primary"
            prepend-icon="mdi-plus"
            rounded="xl"
            size="x-large"
            @click="navigateToCreate"
          >
            Nuevo Jugador
          </v-btn>
        </div>
      </v-col>
    </v-row>

    <!-- Filtros y búsqueda -->
    <v-row class="mb-4">
      <v-col cols="12" md="6" style="transform: translateX(50%);">
        <v-text-field
          v-model="searchQuery"
          bg-color="white"
          color="primary"
          density="comfortable"
          hide-details
          placeholder="Buscar jugadores..."
          prepend-inner-icon="mdi-magnify"
          rounded="xl"
          variant="outlined"
          @input="filterPlayers"
        />
      </v-col>
      <v-col class="d-flex justify-end" cols="12" md="6">
        <v-btn
          class="pt-3 pb-4"
          color="blue-darken-2"
          :loading="loading"
          prepend-icon="mdi-refresh"
          rounded="xl"
          size="large"
          variant="elevated"
          @click="loadPlayers"
        >
          Actualizar
        </v-btn>
      </v-col>
    </v-row>

    <!-- Tabla de jugadores -->
    <v-card rounded="xl">
      <v-data-table
        class="elevation-1"
        :headers="headers"
        :items="filteredPlayers"
        :items-per-page="10"
        :loading="loading"
      >
        <!-- Avatar y nombre -->
        <template #item.name="{ item }">
          <div class="d-flex align-center">
            <v-avatar class="mr-3" size="40">
              <v-img
                v-if="item.avatar"
                alt="Avatar"
                :src="item.avatar"
              />
              <v-icon v-else>mdi-account</v-icon>
            </v-avatar>
            <div>
              <div class="font-weight-medium text-h6">{{ item.display_name }}</div>
              <div v-if="item.nickname" class="text-caption text-grey-darken-1">
                {{ item.nickname }}
              </div>
            </div>
          </div>
        </template>

        <!-- Estadísticas -->
        <template #item.stats="{ item }">
          <div class="d-flex flex-column">
            <div class="text-caption">
              <v-icon size="small">mdi-soccer</v-icon>
              {{ item.goals || 0 }} goles
            </div>
            <div class="text-caption">
              <v-icon size="small">mdi-handshake</v-icon>
              {{ item.assists || 0 }} asistencias
            </div>
          </div>
        </template>

        <!-- Acciones -->
        <template #item.actions="{ item }">
          <div class="d-flex justify-center align-center" style="gap: 3px;">
            <v-btn
              color="primary"
              density="comfortable"
              icon="mdi-eye"
              rounded="xl"
              size="small"
              variant="outlined"
              @click="viewPlayer(item.id)"
            />
            <v-btn
              color="warning"
              density="comfortable"
              icon="mdi-pencil"
              rounded="xl"
              size="small"
              variant="outlined"
              @click="editPlayer(item.id)"
            />
            <v-btn
              color="error"
              density="comfortable"
              icon="mdi-delete"
              rounded="xl"
              size="small"
              variant="outlined"
              @click="deletePlayer(item.id)"
            />
          </div>
        </template>
      </v-data-table>
    </v-card>

    <!-- Dialog de confirmación para eliminar -->
    <v-dialog v-model="showDeleteDialog" max-width="400">
      <v-card>
        <v-card-title class="text-h6">
          <v-icon start color="error">mdi-alert</v-icon>
          Confirmar eliminación
        </v-card-title>
        <v-card-text>
          ¿Estás seguro de que quieres eliminar al jugador "{{ playerToDelete?.display_name }}"?
          Esta acción no se puede deshacer.
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn
            color="grey"
            rounded="xl"
            variant="outlined"
            @click="showDeleteDialog = false"
          >
            Cancelar
          </v-btn>
          <v-btn
            color="error"
            :loading="deleting"
            rounded="xl"
            variant="elevated"
            @click="confirmDelete"
          >
            Eliminar
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup>
  import { computed, onMounted, ref } from 'vue'
  import { useRouter } from 'vue-router'
  import { handleApiError, playerAPI } from '@/services/api'
  import { useAppStore } from '@/stores/app'

  // Router y Store
  const router = useRouter()
  const appStore = useAppStore()

  // Estado reactivo
  const loading = ref(false)
  const deleting = ref(false)
  const players = ref([])
  const searchQuery = ref('')
  const showDeleteDialog = ref(false)
  const playerToDelete = ref(null)

  // Headers de la tabla
  const headers = [
    { title: 'Nombre', key: 'name', sortable: true },
    { title: 'Estadísticas', key: 'stats', sortable: false },
    { title: 'Acciones', key: 'actions', sortable: false, align: 'center' },
  ]

  // Computed
  const filteredPlayers = computed(() => {
    if (!searchQuery.value) return players.value

    const query = searchQuery.value.toLowerCase()
    return players.value.filter(player =>
      player.display_name.toLowerCase().includes(query) ||
      player.nickname.toLowerCase().includes(query)
    )
  })

  // Métodos
  const loadPlayers = async () => {
    loading.value = true
    try {
      const response = await playerAPI.getPlayers()
      players.value = response.data
    } catch (error) {
      const errorInfo = handleApiError(error)
      appStore.showError(`Error al cargar jugadores: ${errorInfo.message}`)
      console.error('Error al cargar jugadores:', errorInfo.message)
    } finally {
      loading.value = false
    }
  }

  const filterPlayers = () => {
    // La función se ejecuta automáticamente por el computed
  }

  const navigateToCreate = () => {
    router.push('/players/create')
  }

  const viewPlayer = (id) => {
    router.push(`/players/${id}`)
  }

  const editPlayer = (id) => {
    router.push(`/players/${id}/edit`)
  }

  const deletePlayer = (id) => {
    playerToDelete.value = players.value.find(p => p.id === id)
    showDeleteDialog.value = true
  }

  const confirmDelete = async () => {
    if (!playerToDelete.value) return

    deleting.value = true
    try {
      await playerAPI.deletePlayer(playerToDelete.value.id)
      appStore.showSuccess('Jugador eliminado exitosamente')
      await loadPlayers()
    } catch (error) {
      const errorInfo = handleApiError(error)
      appStore.showError(`Error al eliminar jugador: ${errorInfo.message}`)
      console.error('Error al eliminar jugador:', errorInfo.message)
    } finally {
      deleting.value = false
      showDeleteDialog.value = false
      playerToDelete.value = null
    }
  }

  // Cargar datos al montar
  onMounted(() => {
    loadPlayers()
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
