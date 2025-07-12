<template>
  <v-container fluid>
    <!-- Header con título y botón de crear -->
    <v-row class="mb-6">
      <v-col cols="12">
        <div class="d-flex align-center justify-space-between">
          <div>
            <h1 class="text-h4 font-weight-bold mb-2">Jugadores</h1>
            <p class="text-body-1 text-grey-darken-1">
              Gestiona los jugadores del campeonato Natsu Cup
            </p>
          </div>
          <v-btn
            color="primary"
            prepend-icon="mdi-plus"
            size="x-large"
            rounded="xl"
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
          density="comfortable"
          hide-details
          placeholder="Buscar jugadores..."
          prepend-inner-icon="mdi-magnify"
          variant="outlined"
          rounded="xl"
          color="primary"
          bg-color="white"
          @input="filterPlayers"
        />
      </v-col>
      <v-col class="d-flex justify-end" cols="12" md="6">
        <v-btn
          :loading="loading"
          prepend-icon="mdi-refresh"
          variant="outlined"
          rounded="xl"
          size="large"
          class="pt-3 pb-4 "
          color="secondary"
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
        <!-- Avatar del jugador -->
        <template #item.avatar="{ item }">
          <v-avatar class="mr-3" size="48">
            <v-img
              v-if="item.avatar"
              alt="Avatar del jugador"
              :src="item.avatar"
            />
            <v-icon v-else color="grey" size="24">
              mdi-account
            </v-icon>
          </v-avatar>
        </template>

        <!-- Nombre del jugador -->
        <template #item.display_name="{ item }">
          <div class="d-flex align-center">
            <div>
              <div class="font-weight-medium text-h6">{{ item.display_name }}</div>
            </div>
          </div>
        </template>

        <!-- Acciones -->
        <template #item.actions="{ item }">
          <div class="d-flex" style="gap: 15px">
            <v-btn
              color="primary"
              icon="mdi-eye"
              size="medium"
              title="Ver detalles"
              variant="text"
              @click="viewPlayer(item)"
            />
            <v-btn
              color="warning"
              icon="mdi-pencil"
              size="medium"
              title="Editar"
              variant="text"
              @click="editPlayer(item)"
            />
            <v-btn
              color="error"
              icon="mdi-delete"
              size="small"
              title="Eliminar"
              variant="text"
              @click="confirmDelete(item)"
            />
          </div>
        </template>

        <!-- Estado vacío -->
        <template #no-data>
          <div class="text-center py-8">
            <v-icon class="mb-4" color="grey-lighten-1" size="64">
              mdi-account-group
            </v-icon>
            <h3 class="text-h6 text-grey-darken-1 mb-2">
              No hay jugadores registrados
            </h3>
            <p class="text-body-2 text-grey-darken-1 mb-4">
              Comienza agregando el primer jugador al campeonato
            </p>
            <v-btn
              color="primary"
              prepend-icon="mdi-plus"
              size="large"
              rounded="xl"
              @click="navigateToCreate"
            >
              Agregar Jugador
            </v-btn>
          </div>
        </template>
      </v-data-table>
    </v-card>

    <!-- Diálogo de confirmación de eliminación -->
    <v-dialog v-model="deleteDialog" max-width="400">
      <v-card>
        <v-card-title class="text-h6">
          Confirmar eliminación
        </v-card-title>
        <v-card-text>
          ¿Estás seguro de que quieres eliminar al jugador
          <strong>{{ playerToDelete?.display_name }}</strong>?
          Esta acción no se puede deshacer.
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn
            variant="outlined"
            rounded="xl"
            @click="deleteDialog = false"
          >
            Cancelar
          </v-btn>
          <v-btn
            color="error"
            :loading="deleting"
            variant="elevated"
            rounded="xl"
            @click="deletePlayer"
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
import { samplePlayers } from '@/data/sampleData'

  // Router
  const router = useRouter()

  // Estado reactivo
  const players = ref([])
  const loading = ref(false)
  const searchQuery = ref('')
  const deleteDialog = ref(false)
  const playerToDelete = ref(null)
  const deleting = ref(false)

  // Headers de la tabla
  const headers = [
    { title: 'Avatar', key: 'avatar', sortable: false },
    { title: 'Jugador', key: 'display_name', sortable: true },
    { title: 'Acciones', key: 'actions', sortable: false},
  ]

  // Computed para filtrar jugadores
  const filteredPlayers = computed(() => {
    if (!searchQuery.value) return players.value

    const query = searchQuery.value.toLowerCase()
    return players.value.filter(player =>
      player.display_name.toLowerCase().includes(query)
      || player.id.toString().includes(query),
    )
  })

  // Cargar jugadores
  const loadPlayers = async () => {
    loading.value = true
    try {
      // Intentar cargar datos reales primero
      try {
        const response = await playerAPI.getPlayers()
        players.value = response.data
      } catch (apiError) {
        console.log('API no disponible, usando datos de ejemplo')
        // Usar datos de ejemplo si la API no está disponible
        players.value = samplePlayers
      }
    } catch (error) {
      const errorInfo = handleApiError(error)
      console.error('Error al cargar jugadores:', errorInfo.message)
    // Aquí podrías mostrar una notificación de error
    } finally {
      loading.value = false
    }
  }

  // Filtrar jugadores
  const filterPlayers = () => {
  // La función se ejecuta automáticamente por el computed
  }

  // Navegación
  const navigateToCreate = () => {
    router.push('/players/create')
  }

  const viewPlayer = player => {
    router.push(`/players/${player.id}`)
  }

  const editPlayer = player => {
    router.push(`/players/${player.id}/edit`)
  }

  // Eliminación
  const confirmDelete = player => {
    playerToDelete.value = player
    deleteDialog.value = true
  }

  const deletePlayer = async () => {
    if (!playerToDelete.value) return

    deleting.value = true
    try {
      await playerAPI.deletePlayer(playerToDelete.value.id)

      // Remover de la lista local
      const index = players.value.findIndex(p => p.id === playerToDelete.value.id)
      if (index !== -1) {
        players.value.splice(index, 1)
      }

      deleteDialog.value = false
      playerToDelete.value = null

    // Aquí podrías mostrar una notificación de éxito
    } catch (error) {
      const errorInfo = handleApiError(error)
      console.error('Error al eliminar jugador:', errorInfo.message)
    // Aquí podrías mostrar una notificación de error
    } finally {
      deleting.value = false
    }
  }

  // Cargar datos al montar el componente
  onMounted(() => {
    loadPlayers()
  })
</script>

<style scoped>
/* Estilos específicos si son necesarios */
</style>
