<template>
  <v-container>
    <!-- Header Section -->
    <v-row class="mb-8">
      <v-col cols="12" md="8">
        <h1 class="text-h3 font-weight-bold mb-2">
          Torneos de FIFA
        </h1>
        <p class="text-h6 text-medium-emphasis">
          Encuentra el torneo perfecto para ti y tus amigos
        </p>
      </v-col>
      <v-col cols="12" md="4" class="d-flex align-center justify-end">
        <v-btn
          color="primary"
          size="large"
          variant="elevated"
          @click="createTournament"
        >
          <v-icon start>add</v-icon>
          Crear Torneo
        </v-btn>
      </v-col>
    </v-row>

    <!-- Filters Section -->
    <v-row class="mb-6">
      <v-col cols="12">
        <v-card class="pa-4">
          <v-row align="center">
            <v-col cols="12" md="3">
              <v-text-field
                v-model="searchQuery"
                prepend-inner-icon="search"
                placeholder="Buscar torneos..."
                variant="outlined"
                density="compact"
                hide-details
              />
            </v-col>
            <v-col cols="12" md="3">
              <v-select
                v-model="statusFilter"
                :items="statusOptions"
                label="Estado"
                variant="outlined"
                density="compact"
                hide-details
              />
            </v-col>
            <v-col cols="12" md="3">
              <v-select
                v-model="typeFilter"
                :items="typeOptions"
                label="Tipo"
                variant="outlined"
                density="compact"
                hide-details
              />
            </v-col>
            <v-col cols="12" md="3">
              <v-btn
                color="primary"
                variant="outlined"
                @click="clearFilters"
              >
                Limpiar Filtros
              </v-btn>
            </v-col>
          </v-row>
        </v-card>
      </v-col>
    </v-row>

    <!-- Tournaments Grid -->
    <v-row>
      <v-col
        cols="12"
        md="6"
        lg="4"
        v-for="tournament in filteredTournaments"
        :key="tournament.id"
      >
        <v-card class="h-100 tournament-card" elevation="3">
          <!-- Tournament Image -->
          <v-img
            :src="tournament.image"
            height="200"
            cover
            class="bg-grey-darken-2"
          >
            <template v-slot:placeholder>
              <div class="d-flex fill-height align-center justify-center">
                <v-icon size="64" color="grey">sports_soccer</v-icon>
              </div>
            </template>

            <!-- Status Badge -->
            <div class="d-flex fill-height align-start justify-end pa-4">
              <v-chip
                :color="getStatusColor(tournament.status)"
                size="small"
                class="font-weight-bold"
              >
                {{ getStatusText(tournament.status) }}
              </v-chip>
            </div>

            <!-- Participants Overlay -->
            <div class="d-flex fill-height align-end">
              <div class="pa-4 text-white w-100">
                <div class="d-flex align-center justify-space-between">
                  <div class="d-flex align-center">
                    <v-icon size="16" color="white" class="mr-1">people</v-icon>
                    <span class="text-caption">
                      {{ tournament.participants }}/{{ tournament.maxParticipants }} jugadores
                    </span>
                  </div>
                  <div class="d-flex align-center">
                    <v-icon size="16" color="white" class="mr-1">emoji_events</v-icon>
                    <span class="text-caption">{{ tournament.prize }}</span>
                  </div>
                </div>
              </div>
            </div>
          </v-img>

          <!-- Tournament Info -->
          <v-card-title class="text-h6 pb-2">
            {{ tournament.name }}
          </v-card-title>

          <v-card-text class="pb-2">
            <p class="text-body-2 text-medium-emphasis mb-3">
              {{ tournament.description }}
            </p>

            <div class="d-flex flex-wrap gap-2 mb-3">
              <v-chip
                v-for="tag in tournament.tags"
                :key="tag"
                size="small"
                variant="outlined"
                color="primary"
              >
                {{ tag }}
              </v-chip>
            </div>

            <div class="d-flex align-center justify-space-between">
              <div class="d-flex align-center">
                <v-icon size="16" color="primary" class="mr-1">event</v-icon>
                <span class="text-caption">{{ tournament.date }}</span>
              </div>
              <div class="d-flex align-center">
                <v-icon size="16" color="primary" class="mr-1">schedule</v-icon>
                <span class="text-caption">{{ tournament.duration }}</span>
              </div>
            </div>
          </v-card-text>

          <!-- Tournament Actions -->
          <v-card-actions class="pt-0">
            <v-btn
              v-if="tournament.status === 'active' && tournament.participants < tournament.maxParticipants"
              color="primary"
              variant="elevated"
              size="small"
              @click="joinTournament(tournament.id)"
            >
              Unirse
            </v-btn>
            <v-btn
              v-else-if="tournament.status === 'upcoming'"
              color="warning"
              variant="outlined"
              size="small"
              @click="registerTournament(tournament.id)"
            >
              Registrarse
            </v-btn>
            <v-btn
              v-else
              color="grey"
              variant="outlined"
              size="small"
              disabled
            >
              {{ tournament.status === 'completed' ? 'Finalizado' : 'Lleno' }}
            </v-btn>

            <v-spacer></v-spacer>

            <v-btn
              color="primary"
              variant="text"
              size="small"
              @click="viewTournament(tournament.id)"
            >
              Ver Detalles
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>

    <!-- Empty State -->
    <v-row v-if="filteredTournaments.length === 0">
      <v-col cols="12" class="text-center py-16">
        <v-icon size="64" color="grey" class="mb-4">search_off</v-icon>
        <h3 class="text-h5 font-weight-bold mb-2">No se encontraron torneos</h3>
        <p class="text-body-1 text-medium-emphasis mb-6">
          Intenta ajustar los filtros o crear un nuevo torneo
        </p>
        <v-btn
          color="primary"
          variant="elevated"
          @click="createTournament"
        >
          <v-icon start>add</v-icon>
          Crear Primer Torneo
        </v-btn>
      </v-col>
    </v-row>

    <!-- Load More Button -->
    <v-row v-if="hasMoreTournaments" class="mt-8">
      <v-col cols="12" class="text-center">
        <v-btn
          color="primary"
          variant="outlined"
          size="large"
          @click="loadMoreTournaments"
          :loading="loading"
        >
          Cargar Más Torneos
        </v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
// Datos de ejemplo para torneos
const tournaments = ref([
  {
    id: 1,
    name: 'Torneo de Verano 2024',
    description: 'El torneo más caliente del año. ¿Quién será el campeón?',
    status: 'active',
    participants: 12,
    maxParticipants: 16,
    date: '15 Jul 2024',
    duration: '2 semanas',
    prize: '🏆 Trofeo + $500',
    type: 'eliminación',
    tags: ['Verano', 'Premio', 'Competitivo'],
    image: '/api/placeholder/400/200'
  },
  {
    id: 2,
    name: 'Clásico de Amigos',
    description: 'Solo para el grupo de amigos de siempre. Sin presión, solo diversión.',
    status: 'active',
    participants: 8,
    maxParticipants: 8,
    date: '20 Jul 2024',
    duration: '1 semana',
    prize: '🏆 Trofeo + Cena',
    type: 'liga',
    tags: ['Amigos', 'Casual', 'Diversión'],
    image: '/api/placeholder/400/200'
  },
  {
    id: 3,
    name: 'Nueva Sangre',
    description: 'Torneo para nuevos jugadores. ¡Perfecto para empezar!',
    status: 'upcoming',
    participants: 4,
    maxParticipants: 12,
    date: '25 Jul 2024',
    duration: '3 semanas',
    prize: '🏆 Trofeo + Entrenamiento',
    type: 'eliminación',
    tags: ['Principiantes', 'Aprendizaje', 'Inclusivo'],
    image: '/api/placeholder/400/200'
  },
  {
    id: 4,
    name: 'Campeonato Profesional',
    description: 'Para los mejores jugadores. Solo los más hábiles sobrevivirán.',
    status: 'upcoming',
    participants: 0,
    maxParticipants: 32,
    date: '1 Ago 2024',
    duration: '1 mes',
    prize: '🏆 Trofeo + $1000',
    type: 'eliminación',
    tags: ['Profesional', 'Premio Alto', 'Competitivo'],
    image: '/api/placeholder/400/200'
  },
  {
    id: 5,
    name: 'Torneo de Oficina',
    description: 'Competencia entre compañeros de trabajo. ¿Quién es el mejor?',
    status: 'completed',
    participants: 16,
    maxParticipants: 16,
    date: '10 Jul 2024',
    duration: '2 semanas',
    prize: '🏆 Trofeo + Reconocimiento',
    type: 'liga',
    tags: ['Oficina', 'Compañeros', 'Finalizado'],
    image: '/api/placeholder/400/200'
  },
  {
    id: 6,
    name: 'Liga de Vecinos',
    description: 'Torneo entre vecinos del barrio. ¡Conoce a tu comunidad!',
    status: 'active',
    participants: 6,
    maxParticipants: 12,
    date: '18 Jul 2024',
    duration: '4 semanas',
    prize: '🏆 Trofeo + BBQ',
    type: 'liga',
    tags: ['Vecinos', 'Comunidad', 'Social'],
    image: '/api/placeholder/400/200'
  }
])

// Filtros
const searchQuery = ref('')
const statusFilter = ref('all')
const typeFilter = ref('all')
const loading = ref(false)

// Opciones de filtros
const statusOptions = [
  { title: 'Todos', value: 'all' },
  { title: 'Activos', value: 'active' },
  { title: 'Próximos', value: 'upcoming' },
  { title: 'Finalizados', value: 'completed' }
]

const typeOptions = [
  { title: 'Todos', value: 'all' },
  { title: 'Eliminación', value: 'eliminación' },
  { title: 'Liga', value: 'liga' }
]

// Computed properties
const filteredTournaments = computed(() => {
  return tournaments.value.filter(tournament => {
    const matchesSearch = tournament.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
                         tournament.description.toLowerCase().includes(searchQuery.value.toLowerCase())

    const matchesStatus = statusFilter.value === 'all' || tournament.status === statusFilter.value
    const matchesType = typeFilter.value === 'all' || tournament.type === typeFilter.value

    return matchesSearch && matchesStatus && matchesType
  })
})

const hasMoreTournaments = computed(() => {
  // Simular que hay más torneos para cargar
  return tournaments.value.length < 20
})

// Métodos
const getStatusColor = (status) => {
  const colors = {
    active: 'success',
    upcoming: 'warning',
    completed: 'grey'
  }
  return colors[status] || 'grey'
}

const getStatusText = (status) => {
  const texts = {
    active: 'Activo',
    upcoming: 'Próximo',
    completed: 'Finalizado'
  }
  return texts[status] || 'Desconocido'
}

const clearFilters = () => {
  searchQuery.value = ''
  statusFilter.value = 'all'
  typeFilter.value = 'all'
}

const joinTournament = (tournamentId) => {
  console.log('Uniéndose al torneo:', tournamentId)
  // Aquí iría la lógica para unirse al torneo
}

const registerTournament = (tournamentId) => {
  console.log('Registrándose al torneo:', tournamentId)
  // Aquí iría la lógica para registrarse al torneo
}

const viewTournament = (tournamentId) => {
  console.log('Viendo torneo:', tournamentId)
  // Aquí iría la lógica para ver detalles del torneo
}

const createTournament = () => {
  console.log('Creando nuevo torneo')
  // Aquí iría la lógica para crear un torneo
}

const loadMoreTournaments = async () => {
  loading.value = true
  // Simular carga de más torneos
  await new Promise(resolve => setTimeout(resolve, 1000))

  // Agregar más torneos de ejemplo
  const newTournaments = [
    {
      id: tournaments.value.length + 1,
      name: `Torneo Extra ${tournaments.value.length + 1}`,
      description: 'Torneo adicional para demostrar la funcionalidad.',
      status: 'upcoming',
      participants: Math.floor(Math.random() * 10),
      maxParticipants: 16,
      date: '30 Jul 2024',
      duration: '2 semanas',
      prize: '🏆 Trofeo',
      type: 'eliminación',
      tags: ['Extra', 'Demo'],
      image: '/api/placeholder/400/200'
    }
  ]

  tournaments.value.push(...newTournaments)
  loading.value = false
}
</script>

<style scoped>
.tournament-card {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.tournament-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 25px rgba(0,0,0,0.15) !important;
}

.gap-2 {
  gap: 8px;
}
</style>
