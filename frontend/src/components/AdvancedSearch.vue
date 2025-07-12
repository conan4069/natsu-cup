<template>
  <v-card class="mb-4">
    <v-card-title class="text-h6">
      <v-icon start>mdi-magnify</v-icon>
      Búsqueda Avanzada
    </v-card-title>
    <v-card-text>
      <v-row>
        <!-- Búsqueda por texto -->
        <v-col cols="12" md="4">
          <v-text-field
            v-model="searchQuery"
            label="Buscar..."
            prepend-inner-icon="mdi-magnify"
            variant="outlined"
            density="comfortable"
            clearable
            @update:model-value="onSearch"
            @click:clear="onClear"
          />
        </v-col>

        <!-- Filtro por estado -->
        <v-col cols="12" md="3" v-if="showStatusFilter">
          <v-select
            v-model="statusFilter"
            label="Estado"
            :items="statusOptions"
            variant="outlined"
            density="comfortable"
            clearable
            @update:model-value="onSearch"
          />
        </v-col>

        <!-- Filtro por formato -->
        <v-col cols="12" md="3" v-if="showFormatFilter">
          <v-select
            v-model="formatFilter"
            label="Formato"
            :items="formatOptions"
            variant="outlined"
            density="comfortable"
            clearable
            @update:model-value="onSearch"
          />
        </v-col>

        <!-- Filtro por fecha -->
        <v-col cols="12" md="2" v-if="showDateFilter">
          <v-menu
            v-model="dateMenu"
            :close-on-content-click="false"
          >
            <template #activator="{ props }">
              <v-text-field
                v-model="dateFilter"
                label="Fecha"
                prepend-inner-icon="mdi-calendar"
                variant="outlined"
                density="comfortable"
                readonly
                v-bind="props"
                clearable
                @click:clear="clearDateFilter"
              />
            </template>
            <v-date-picker
              v-model="dateFilter"
              @update:model-value="onDateChange"
            />
          </v-menu>
        </v-col>
      </v-row>

      <!-- Filtros adicionales -->
      <v-row v-if="showAdvancedFilters">
        <v-col cols="12" md="3">
          <v-select
            v-model="sortBy"
            label="Ordenar por"
            :items="sortOptions"
            variant="outlined"
            density="comfortable"
            @update:model-value="onSearch"
          />
        </v-col>

        <v-col cols="12" md="3">
          <v-select
            v-model="sortOrder"
            label="Orden"
            :items="[
              { title: 'Ascendente', value: 'asc' },
              { title: 'Descendente', value: 'desc' }
            ]"
            variant="outlined"
            density="comfortable"
            @update:model-value="onSearch"
          />
        </v-col>

        <v-col cols="12" md="3">
          <v-text-field
            v-model.number="limit"
            label="Mostrar"
            type="number"
            min="5"
            max="100"
            variant="outlined"
            density="comfortable"
            @update:model-value="onSearch"
          />
        </v-col>

        <v-col cols="12" md="3">
          <v-btn
            color="secondary"
            variant="outlined"
            block
            @click="resetFilters"
          >
            <v-icon start>mdi-refresh</v-icon>
            Limpiar Filtros
          </v-btn>
        </v-col>
      </v-row>

      <!-- Toggle filtros avanzados -->
      <v-row>
        <v-col cols="12">
          <v-btn
            variant="text"
            size="small"
            @click="showAdvancedFilters = !showAdvancedFilters"
          >
            <v-icon start>{{ showAdvancedFilters ? 'mdi-chevron-up' : 'mdi-chevron-down' }}</v-icon>
            {{ showAdvancedFilters ? 'Ocultar' : 'Mostrar' }} filtros avanzados
          </v-btn>
        </v-col>
      </v-row>
    </v-card-text>
  </v-card>
</template>

<script setup>
import { ref, watch } from 'vue'

// Props
const props = defineProps({
  showStatusFilter: {
    type: Boolean,
    default: false
  },
  showFormatFilter: {
    type: Boolean,
    default: false
  },
  showDateFilter: {
    type: Boolean,
    default: false
  },
  statusOptions: {
    type: Array,
    default: () => [
      { title: 'Activo', value: 'active' },
      { title: 'Completado', value: 'completed' },
      { title: 'Pendiente', value: 'pending' }
    ]
  },
  formatOptions: {
    type: Array,
    default: () => [
      { title: '1v1', value: '1v1' },
      { title: '2v2', value: '2v2' },
      { title: '3v3', value: '3v3' },
      { title: '5v5', value: '5v5' }
    ]
  },
  sortOptions: {
    type: Array,
    default: () => [
      { title: 'Nombre', value: 'name' },
      { title: 'Fecha de creación', value: 'created_at' },
      { title: 'Estado', value: 'status' },
      { title: 'Formato', value: 'format' }
    ]
  }
})

// Emits
const emit = defineEmits(['search', 'clear'])

// Estado reactivo
const searchQuery = ref('')
const statusFilter = ref(null)
const formatFilter = ref(null)
const dateFilter = ref(null)
const dateMenu = ref(false)
const sortBy = ref('created_at')
const sortOrder = ref('desc')
const limit = ref(20)
const showAdvancedFilters = ref(false)

// Métodos
const onSearch = () => {
  const filters = {
    query: searchQuery.value,
    status: statusFilter.value,
    format: formatFilter.value,
    date: dateFilter.value,
    sortBy: sortBy.value,
    sortOrder: sortOrder.value,
    limit: limit.value
  }

  emit('search', filters)
}

const onClear = () => {
  searchQuery.value = ''
  onSearch()
}

const onDateChange = () => {
  dateMenu.value = false
  onSearch()
}

const clearDateFilter = () => {
  dateFilter.value = null
  onSearch()
}

const resetFilters = () => {
  searchQuery.value = ''
  statusFilter.value = null
  formatFilter.value = null
  dateFilter.value = null
  sortBy.value = 'created_at'
  sortOrder.value = 'desc'
  limit.value = 20

  emit('clear')
}

// Watch para cambios en los filtros
watch([searchQuery, statusFilter, formatFilter, dateFilter, sortBy, sortOrder, limit], () => {
  onSearch()
}, { deep: true })
</script>

<style scoped>
/* Estilos específicos si son necesarios */
</style>
