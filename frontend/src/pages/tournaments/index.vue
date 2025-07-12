<template>
  <v-container fluid>
    <!-- Header con título y botón de crear -->
    <v-row class="mb-6">
      <v-col cols="12">
        <div class="d-flex align-center justify-space-between">
          <div>
            <h1 class="text-h4 font-weight-bold mb-2">Torneos</h1>
            <p class="text-body-1 text-grey-darken-1">
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
          <div class="d-flex" style="gap: 15px">
            <v-btn
              color="primary"
              icon="mdi-eye"
              size="medium"
              title="Ver detalles"
              variant="text"
              @click="viewTournament(item)"
            />
            <v-btn
              color="warning"
              icon="mdi-pencil"
              size="medium"
              title="Editar"
              variant="text"
              @click="editTournament(item)"
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

    <!-- Diálogo de confirmación de eliminación -->
    <v-dialog v-model="deleteDialog" max-width="400">
      <v-card>
        <v-card-title class="text-h6">
          Confirmar eliminación
        </v-card-title>
        <v-card-text>
          ¿Estás seguro de que quieres eliminar el torneo
          <strong>{{ tournamentToDelete?.name }}</strong>?
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
            @click="deleteTournament"
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
  import { sampleTournaments } from '@/data/sampleData'
  import { handleApiError, tournamentAPI } from '@/services/api'

  // Router
  const router = useRouter()

  // Estado reactivo
  const tournaments = ref([])
  const loading = ref(false)
  const searchQuery = ref('')
  const deleteDialog = ref(false)
  const tournamentToDelete = ref(null)
  const deleting = ref(false)

  // Headers de la tabla
  const headers = [
    { title: 'Torneo', key: 'name', sortable: true },
    { title: 'Formato', key: 'format', sortable: true },
    { title: 'Configuración', key: 'config', sortable: false },
    { title: 'Acciones', key: 'actions', sortable: false, align: 'end' },
  ]

  // Computed para filtrar torneos
  const filteredTournaments = computed(() => {
    if (!searchQuery.value) return tournaments.value
    const query = searchQuery.value.toLowerCase()
    return tournaments.value.filter(tournament =>
      tournament.name.toLowerCase().includes(query)
      || tournament.format.toLowerCase().includes(query)
      || tournament.id.toString().includes(query),
    )
  })

  // Cargar torneos
  const loadTournaments = async () => {
    loading.value = true
    try {
      // Intentar cargar datos reales primero
      try {
        const response = await tournamentAPI.getTournaments()
        tournaments.value = response.data
      } catch {
        console.log('API no disponible, usando datos de ejemplo')
        // Usar datos de ejemplo si la API no está disponible
        tournaments.value = sampleTournaments
      }
    } catch (error) {
      const errorInfo = handleApiError(error)
      console.error('Error al cargar torneos:', errorInfo.message)
    } finally {
      loading.value = false
    }
  }

  // Filtrar torneos
  const filterTournaments = () => {
    // La función se ejecuta automáticamente por el computed
  }

  // Navegación
  const navigateToCreate = () => {
    router.push('/tournaments/create')
  }

  const viewTournament = tournament => {
    router.push(`/tournaments/${tournament.id}`)
  }

  const editTournament = tournament => {
    router.push(`/tournaments/${tournament.id}/edit`)
  }

  // Eliminación
  const confirmDelete = tournament => {
    tournamentToDelete.value = tournament
    deleteDialog.value = true
  }

  const deleteTournament = async () => {
    if (!tournamentToDelete.value) return
    deleting.value = true
    try {
      await tournamentAPI.deleteTournament(tournamentToDelete.value.id)
      // Remover de la lista local
      const index = tournaments.value.findIndex(t => t.id === tournamentToDelete.value.id)
      if (index !== -1) {
        tournaments.value.splice(index, 1)
      }
      deleteDialog.value = false
      tournamentToDelete.value = null
    } catch (error) {
      const errorInfo = handleApiError(error)
      console.error('Error al eliminar torneo:', errorInfo.message)
    } finally {
      deleting.value = false
    }
  }

  // Cargar datos al montar el componente
  onMounted(() => {
    loadTournaments()
  })
</script>

<style scoped>
/* Estilos específicos si son necesarios */
</style>
