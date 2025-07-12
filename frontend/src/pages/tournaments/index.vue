<template>
  <v-container fluid>
    <!-- Header con título y botón de crear -->
    <v-row class="mb-6">
      <v-col cols="12">
        <div class="d-flex align-center justify-space-between">
          <div>
            <h1 class="text-h4 font-weight-bold mb-2 page-title">Torneos</h1>
            <p class="text-body-1 page-subtitle">
              Gestiona los torneos de la Natsu Cup
            </p>
          </div>
          <v-btn
            color="primary"
            prepend-icon="mdi-plus"
            rounded="xl"
            size="x-large"
            @click="navigateToCreate"
          >
            Nuevo Torneo
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
          placeholder="Buscar torneos..."
          prepend-inner-icon="mdi-magnify"
          rounded="xl"
          variant="outlined"
          @input="filterTournaments"
        />
      </v-col>
      <v-col class="d-flex justify-end" cols="12" md="6">
        <v-btn
          class="pt-3 pb-4"
          color="primary"
          :loading="loading"
          prepend-icon="mdi-refresh"
          rounded="xl"
          size="large"
          variant="outlined"
          @click="loadTournaments"
        >
          Actualizar
        </v-btn>
      </v-col>
    </v-row>

    <!-- Tabla de torneos -->
    <v-card rounded="xl">
      <v-data-table
        class="elevation-1"
        :headers="headers"
        :items="filteredTournaments"
        :items-per-page="10"
        :loading="loading"
      >
        <!-- Nombre del torneo -->
        <template #item.name="{ item }">
          <div class="d-flex align-center">
            <div>
              <div class="font-weight-medium text-h6">{{ item.name }}</div>
              <div class="text-caption text-grey-darken-1">
                {{ item.format }} • {{ item.total_teams }} equipos
              </div>
            </div>
          </div>
        </template>

        <!-- Formato -->
        <template #item.format="{ item }">
          <v-chip
            :color="item.format === '2v2' ? 'primary' : 'secondary'"
            size="small"
            variant="outlined"
          >
            {{ item.format }}
          </v-chip>
        </template>

        <!-- Configuración -->
        <template #item.config="{ item }">
          <div class="d-flex flex-column">
            <v-chip
              v-if="item.has_group_stage"
              class="mb-1"
              color="success"
              size="x-small"
              variant="outlined"
            >
              Grupos
            </v-chip>
            <v-chip
              v-if="item.has_knockout"
              color="warning"
              size="x-small"
              variant="outlined"
            >
              Eliminatoria
            </v-chip>
          </div>
        </template>

        <!-- Acciones -->
        <template #item.actions="{ item }">
          <div class="d-flex gap-2">
            <v-btn
              color="primary"
              density="comfortable"
              icon="mdi-eye"
              rounded="xl"
              size="small"
              variant="outlined"
              @click="viewTournament(item.id)"
            />
            <v-btn
              color="warning"
              density="comfortable"
              icon="mdi-pencil"
              rounded="xl"
              size="small"
              variant="outlined"
              @click="editTournament(item.id)"
            />
            <v-btn
              color="error"
              density="comfortable"
              icon="mdi-delete"
              rounded="xl"
              size="small"
              variant="outlined"
              @click="deleteTournament(item.id)"
            />
          </div>
        </template>

        <!-- Estado vacío -->
        <template #no-data>
          <div class="text-center py-8">
            <v-icon class="mb-4" color="grey-lighten-1" size="64">
              mdi-trophy
            </v-icon>
            <h3 class="text-h6 text-grey-darken-1 mb-2">
              No hay torneos registrados
            </h3>
            <p class="text-body-2 text-grey-darken-1 mb-4">
              Comienza creando el primer torneo
            </p>
            <v-btn
              color="primary"
              prepend-icon="mdi-plus"
              rounded="xl"
              size="large"
              @click="navigateToCreate"
            >
              Crear Torneo
            </v-btn>
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
          ¿Estás seguro de que quieres eliminar el torneo "{{ tournamentToDelete?.name }}"?
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
  import { handleApiError, tournamentAPI } from '@/services/api'
  import { useAppStore } from '@/stores/app'

  // Router y Store
  const router = useRouter()
  const appStore = useAppStore()

  // Estado reactivo
  const loading = ref(false)
  const deleting = ref(false)
  const tournaments = ref([])
  const searchQuery = ref('')
  const showDeleteDialog = ref(false)
  const tournamentToDelete = ref(null)

  // Headers de la tabla
  const headers = [
    { title: 'Nombre', key: 'name', sortable: true },
    { title: 'Formato', key: 'format', sortable: true },
    { title: 'Configuración', key: 'config', sortable: false },
    { title: 'Acciones', key: 'actions', sortable: false, align: 'center' },
  ]

  // Computed
  const filteredTournaments = computed(() => {
    if (!searchQuery.value) return tournaments.value

    const query = searchQuery.value.toLowerCase()
    return tournaments.value.filter(tournament =>
      tournament.name.toLowerCase().includes(query) ||
      tournament.format.toLowerCase().includes(query)
    )
  })

  // Métodos
  const loadTournaments = async () => {
    loading.value = true
    try {
      const response = await tournamentAPI.getTournaments()
      tournaments.value = response.data
    } catch (error) {
      const errorInfo = handleApiError(error)
      appStore.showError(`Error al cargar torneos: ${errorInfo.message}`)
      console.error('Error al cargar torneos:', errorInfo.message)
    } finally {
      loading.value = false
    }
  }

  const filterTournaments = () => {
    // La función se ejecuta automáticamente por el computed
  }

  const navigateToCreate = () => {
    router.push('/tournaments/create')
  }

  const viewTournament = (id) => {
    router.push(`/tournaments/${id}`)
  }

  const editTournament = (id) => {
    router.push(`/tournaments/${id}/edit`)
  }

  const deleteTournament = (id) => {
    tournamentToDelete.value = tournaments.value.find(t => t.id === id)
    showDeleteDialog.value = true
  }

  const confirmDelete = async () => {
    if (!tournamentToDelete.value) return

    deleting.value = true
    try {
      await tournamentAPI.deleteTournament(tournamentToDelete.value.id)
      appStore.showSuccess('Torneo eliminado exitosamente')
      await loadTournaments()
    } catch (error) {
      const errorInfo = handleApiError(error)
      appStore.showError(`Error al eliminar torneo: ${errorInfo.message}`)
      console.error('Error al eliminar torneo:', errorInfo.message)
    } finally {
      deleting.value = false
      showDeleteDialog.value = false
      tournamentToDelete.value = null
    }
  }

  // Cargar datos al montar
  onMounted(() => {
    loadTournaments()
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
