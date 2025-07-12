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
            size="x-large"
            rounded="xl"
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
          density="comfortable"
          hide-details
          placeholder="Buscar equipos..."
          prepend-inner-icon="mdi-magnify"
          variant="outlined"
          rounded="xl"
          color="primary"
          bg-color="white"
          @input="filterTeams"
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
          color="primary"
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
        <template #item.avatar="{ item }">
          <v-avatar class="mr-3" size="48">
            <v-img
              v-if="item.avatar"
              alt="Avatar del equipo"
              :src="item.avatar"
            />
            <v-icon v-else color="grey" size="24">
              mdi-account-group
            </v-icon>
          </v-avatar>
        </template>

        <!-- Nombre del equipo -->
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
              size="large"
              rounded="xl"
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
          <strong>{{ teamToDelete?.display_name }}</strong>?
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
    { title: 'Logo', key: 'avatar', sortable: false },
    { title: 'Equipo', key: 'display_name', sortable: true },
    { title: 'Acciones', key: 'actions', sortable: false, align: 'end' },
  ]

  // Computed para filtrar equipos
  const filteredTeams = computed(() => {
    if (!searchQuery.value) return teams.value
    const query = searchQuery.value.toLowerCase()
    return teams.value.filter(team =>
      team.display_name.toLowerCase().includes(query)
      || team.id.toString().includes(query),
    )
  })

  // Cargar equipos
  const loadTeams = async () => {
    loading.value = true
    try {
      const response = await teamAPI.getTeams()
      teams.value = response.data
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
