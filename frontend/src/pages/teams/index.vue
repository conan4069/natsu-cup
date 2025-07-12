<template>
  <v-container fluid>
    <!-- Header con título y botón de crear -->
    <v-row class="mb-6">
      <v-col cols="12">
        <div class="d-flex align-center justify-space-between">
          <div>
            <h1 class="text-h4 font-weight-bold mb-2">Equipos</h1>
            <p class="text-body-1 text-grey-darken-1">
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
          class="pt-3 pb-4 "
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
        <!-- imagen del equipo -->
        <template #item.logo="{ item }">
          <v-avatar class="mr-3" size="48">
            <v-img
              v-if="item.logo"
              alt="Logo del equipo"
              :src="item.logo"
            />
            <v-icon v-else color="grey" size="24">
              mdi-shield
            </v-icon>
          </v-avatar>
        </template>

        <!-- Nombre del equipo -->
        <template #item.name="{ item }">
          <div class="d-flex align-center">
            <div>
              <div class="font-weight-medium text-h6">{{ item.name }}</div>
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
              @click="viewTeam(item)"
            />
            <v-btn
              color="warning"
              icon="mdi-pencil"
              size="medium"
              title="Editar"
              variant="text"
              @click="editTeam(item)"
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
              No hay equipos registrados
            </h3>
            <p class="text-body-2 text-grey-darken-1 mb-4">
              Comienza agregando el primer equipo al campeonato
            </p>
            <v-btn
              color="primary"
              prepend-icon="mdi-plus"
              rounded="xl"
              size="large"
              @click="navigateToCreate"
            >
              Agregar Equipo
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
          ¿Estás seguro de que quieres eliminar al equipo
          <strong>{{ teamToDelete?.name }}</strong>?
          Esta acción no se puede deshacer.
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn
            rounded="xl"
            variant="outlined"
            @click="deleteDialog = false"
          >
            Cancelar
          </v-btn>
          <v-btn
            color="error"
            :loading="deleting"
            rounded="xl"
            variant="elevated"
            @click="deleteTeam"
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
import { sampleTeams } from '@/data/sampleData'

  // Router
  const router = useRouter()

  // Estado reactivo
  const teams = ref([])
  const loading = ref(false)
  const searchQuery = ref('')
  const deleteDialog = ref(false)
  const teamToDelete = ref(null)
  const deleting = ref(false)

  // Headers de la tabla
  const headers = [
    { title: 'Logo', key: 'logo', sortable: false },
    { title: 'Equipo', key: 'name', sortable: true },
    { title: 'Acciones', key: 'actions', sortable: false, align: 'end' },
  ]

  // Computed para filtrar equipos
  const filteredTeams = computed(() => {
    if (!searchQuery.value) return teams.value
    const query = searchQuery.value.toLowerCase()
    return teams.value.filter(team =>
      team.name.toLowerCase().includes(query)
      || team.id.toString().includes(query),
    )
  })

  // Cargar equipos
  const loadTeams = async () => {
    loading.value = true
    try {
      // Intentar cargar datos reales primero
      try {
        const response = await teamAPI.getTeams()
        teams.value = response.data
      } catch (apiError) {
        console.log('API no disponible, usando datos de ejemplo')
        // Usar datos de ejemplo si la API no está disponible
        teams.value = sampleTeams
      }
    } catch (error) {
      const errorInfo = handleApiError(error)
      console.error('Error al cargar equipos:', errorInfo.message)
    } finally {
      loading.value = false
    }
  }

  // Filtrar equipos
  const filterTeams = () => {
    // La función se ejecuta automáticamente por el computed
  }

  // Navegación
  const navigateToCreate = () => {
    router.push('/teams/create')
  }

  const viewTeam = team => {
    router.push(`/teams/${team.id}`)
  }

  const editTeam = team => {
    router.push(`/teams/${team.id}/edit`)
  }

  // Eliminación
  const confirmDelete = team => {
    teamToDelete.value = team
    deleteDialog.value = true
  }

  const deleteTeam = async () => {
    if (!teamToDelete.value) return
    deleting.value = true
    try {
      await teamAPI.deleteTeam(teamToDelete.value.id)
      // Remover de la lista local
      const index = teams.value.findIndex(t => t.id === teamToDelete.value.id)
      if (index !== -1) {
        teams.value.splice(index, 1)
      }
      deleteDialog.value = false
      teamToDelete.value = null
    } catch (error) {
      const errorInfo = handleApiError(error)
      console.error('Error al eliminar equipo:', errorInfo.message)
    } finally {
      deleting.value = false
    }
  }

  // Cargar datos al montar el componente
  onMounted(() => {
    loadTeams()
  })
</script>

<style scoped>
/* Estilos específicos si son necesarios */
</style>
