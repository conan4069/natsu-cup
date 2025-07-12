<template>
  <v-container fluid>
    <!-- Header con título y botón de crear -->
    <v-row class="mb-6">
      <v-col cols="12">
        <div class="d-flex align-center justify-space-between">
          <div>
            <h1 class="text-h4 font-weight-bold mb-2 page-title">Equipos</h1>
            <p class="text-body-1 page-subtitle">
              Gestiona los equipos del campeonato Natsu Cup
            </p>
          </div>
          <v-btn
            color="primary"
            prepend-icon="mdi-plus"
            rounded="xl"
            size="x-large"
            @click="navigateToCreate"
          >
            Nuevo Equipo
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
          placeholder="Buscar equipos..."
          prepend-inner-icon="mdi-magnify"
          rounded="xl"
          variant="outlined"
          @input="filterTeams"
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
          @click="loadTeams"
        >
          Actualizar
        </v-btn>
      </v-col>
    </v-row>

    <!-- Tabla de equipos -->
    <v-card rounded="xl">
      <v-data-table
        class="elevation-1"
        :headers="headers"
        :items="filteredTeams"
        :items-per-page="10"
        :loading="loading"
      >
        <!-- Logo y nombre -->
        <template #item.name="{ item }">
          <div class="d-flex align-center">
            <v-avatar class="mr-3" size="40">
              <v-img
                v-if="item.logo"
                alt="Logo"
                :src="item.logo"
              />
              <v-icon v-else>mdi-shield</v-icon>
            </v-avatar>
            <div>
              <div class="font-weight-medium text-h6">{{ item.name }}</div>
            </div>
          </div>
        </template>

        <!-- Estadísticas -->
        <template #item.stats="{ item }">
          <div class="d-flex flex-column">
            <div class="text-caption">
              <v-icon size="small">mdi-trophy</v-icon>
              {{ item.wins || 0 }} victorias
            </div>
            <div class="text-caption">
              <v-icon size="small">mdi-soccer</v-icon>
              {{ item.goals || 0 }} goles
            </div>
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
              @click="viewTeam(item.id)"
            />
            <v-btn
              color="warning"
              density="comfortable"
              icon="mdi-pencil"
              rounded="xl"
              size="small"
              variant="outlined"
              @click="editTeam(item.id)"
            />
            <v-btn
              color="error"
              density="comfortable"
              icon="mdi-delete"
              rounded="xl"
              size="small"
              variant="outlined"
              @click="deleteTeam(item.id)"
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
          ¿Estás seguro de que quieres eliminar el equipo "{{ teamToDelete?.name }}"?
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
  import { handleApiError, teamAPI } from '@/services/api'
  import { useAppStore } from '@/stores/app'

  // Router y Store
  const router = useRouter()
  const appStore = useAppStore()

  // Estado reactivo
  const loading = ref(false)
  const deleting = ref(false)
  const teams = ref([])
  const searchQuery = ref('')
  const showDeleteDialog = ref(false)
  const teamToDelete = ref(null)

  // Headers de la tabla
  const headers = [
    { title: 'Equipo', key: 'name', sortable: true },
    { title: 'Estadísticas', key: 'stats', sortable: false },
    { title: 'Acciones', key: 'actions', sortable: false, align: 'center' },
  ]

  // Computed
  const filteredTeams = computed(() => {
    if (!searchQuery.value) return teams.value

    const query = searchQuery.value.toLowerCase()
    return teams.value.filter(team =>
      team.name.toLowerCase().includes(query)
    )
  })

  // Métodos
  const loadTeams = async () => {
    loading.value = true
    try {
      const response = await teamAPI.getTeams()
      teams.value = response.data
    } catch (error) {
      const errorInfo = handleApiError(error)
      appStore.showError(`Error al cargar equipos: ${errorInfo.message}`)
      console.error('Error al cargar equipos:', errorInfo.message)
    } finally {
      loading.value = false
    }
  }

  const filterTeams = () => {
    // La función se ejecuta automáticamente por el computed
  }

  const navigateToCreate = () => {
    router.push('/teams/create')
  }

  const viewTeam = (id) => {
    router.push(`/teams/${id}`)
  }

  const editTeam = (id) => {
    router.push(`/teams/${id}/edit`)
  }

  const deleteTeam = (id) => {
    teamToDelete.value = teams.value.find(t => t.id === id)
    showDeleteDialog.value = true
  }

  const confirmDelete = async () => {
    if (!teamToDelete.value) return

    deleting.value = true
    try {
      await teamAPI.deleteTeam(teamToDelete.value.id)
      appStore.showSuccess('Equipo eliminado exitosamente')
      await loadTeams()
    } catch (error) {
      const errorInfo = handleApiError(error)
      appStore.showError(`Error al eliminar equipo: ${errorInfo.message}`)
      console.error('Error al eliminar equipo:', errorInfo.message)
    } finally {
      deleting.value = false
      showDeleteDialog.value = false
      teamToDelete.value = null
    }
  }

  // Cargar datos al montar
  onMounted(() => {
    loadTeams()
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
