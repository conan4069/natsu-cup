<template>
  <v-container fluid class="pa-0">
    <!-- Hero Section -->
    <v-row no-gutters class="hero-section">
      <v-col cols="12" class="d-flex align-center justify-center">
        <div class="text-center hero-content">
          <v-icon size="120" color="primary" class="mb-6">sports_soccer</v-icon>
          <h1 class="text-h2 font-weight-bold text-white mb-4">
            Natsu Cup
          </h1>
          <p class="text-h5 text-white mb-8">
            El campeonato de FIFA más épico entre amigos
          </p>
          <v-btn
            size="x-large"
            color="primary"
            variant="elevated"
            class="px-8"
            @click="navigateToTournaments"
          >
            <v-icon start>emoji_events</v-icon>
            Ver Torneos
          </v-btn>
        </div>
      </v-col>
    </v-row>

    <!-- Features Section -->
    <v-row class="py-16 px-4">
      <v-col cols="12" class="text-center mb-12">
        <h2 class="text-h3 font-weight-bold mb-4">
          ¿Por qué Natsu Cup?
        </h2>
        <p class="text-h6 text-medium-emphasis">
          La plataforma definitiva para organizar torneos de FIFA con tus amigos
        </p>
      </v-col>

      <v-col cols="12" md="4" class="text-center pa-6">
        <v-card class="h-100 pa-6" elevation="2">
          <v-icon size="64" color="primary" class="mb-4">groups</v-icon>
          <h3 class="text-h5 font-weight-bold mb-3">Torneos con Amigos</h3>
          <p class="text-body-1 text-medium-emphasis">
            Organiza torneos privados con tu grupo de amigos.
            Compite, ríete y celebra juntos.
          </p>
        </v-card>
      </v-col>

      <v-col cols="12" md="4" class="text-center pa-6">
        <v-card class="h-100 pa-6" elevation="2">
          <v-icon size="64" color="primary" class="mb-4">schedule</v-icon>
          <h3 class="text-h5 font-weight-bold mb-3">Fácil Organización</h3>
          <p class="text-body-1 text-medium-emphasis">
            Crea brackets automáticos, programa partidas y
            mantén un seguimiento en tiempo real.
          </p>
        </v-card>
      </v-col>

      <v-col cols="12" md="4" class="text-center pa-6">
        <v-card class="h-100 pa-6" elevation="2">
          <v-icon size="64" color="primary" class="mb-4">analytics</v-icon>
          <h3 class="text-h5 font-weight-bold mb-3">Estadísticas Detalladas</h3>
          <p class="text-body-1 text-medium-emphasis">
            Revisa tu historial, estadísticas y
            evolución como jugador de FIFA.
          </p>
        </v-card>
      </v-col>
    </v-row>

    <!-- Active Tournaments Section -->
    <v-row class="py-16 px-4 bg-grey-lighten-4">
      <v-col cols="12" class="text-center mb-8">
        <h2 class="text-h3 font-weight-bold mb-4">
          Torneos Activos
        </h2>
        <p class="text-h6 text-medium-emphasis">
          Únete a los torneos en curso o crea uno nuevo
        </p>
      </v-col>

      <v-col cols="12" md="6" lg="4" v-for="tournament in activeTournaments" :key="tournament.id">
        <v-card class="h-100" elevation="3">
          <v-img
            :src="tournament.image"
            height="200"
            cover
            class="bg-grey-darken-2"
          >
            <div class="d-flex fill-height align-end">
              <div class="pa-4 text-white">
                <div class="d-flex align-center mb-2">
                  <v-chip
                    :color="tournament.status === 'active' ? 'success' : 'warning'"
                    size="small"
                    class="mr-2"
                  >
                    {{ tournament.status === 'active' ? 'Activo' : 'Próximo' }}
                  </v-chip>
                  <v-icon size="16" color="white">people</v-icon>
                  <span class="ml-1 text-caption">{{ tournament.participants }}/{{ tournament.maxParticipants }}</span>
                </div>
              </div>
            </div>
          </v-img>

          <v-card-title class="text-h6">
            {{ tournament.name }}
          </v-card-title>

          <v-card-text>
            <p class="text-body-2 text-medium-emphasis mb-3">
              {{ tournament.description }}
            </p>
            <div class="d-flex align-center justify-space-between">
              <div class="d-flex align-center">
                <v-icon size="16" color="primary" class="mr-1">event</v-icon>
                <span class="text-caption">{{ tournament.date }}</span>
              </div>
              <div class="d-flex align-center">
                <v-icon size="16" color="primary" class="mr-1">emoji_events</v-icon>
                <span class="text-caption">{{ tournament.prize }}</span>
              </div>
            </div>
          </v-card-text>

          <v-card-actions>
            <v-btn
              color="primary"
              variant="outlined"
              size="small"
              @click="joinTournament(tournament.id)"
            >
              Unirse
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

      <v-col cols="12" class="text-center mt-8">
        <v-btn
          color="primary"
          size="large"
          variant="elevated"
          @click="createTournament"
        >
          <v-icon start>add</v-icon>
          Crear Nuevo Torneo
        </v-btn>
      </v-col>
    </v-row>

    <!-- Stats Section -->
    <v-row class="py-16 px-4">
      <v-col cols="12" class="text-center mb-8">
        <h2 class="text-h3 font-weight-bold mb-4">
          Natsu Cup en Números
        </h2>
      </v-col>

      <v-col cols="12" md="3" class="text-center">
        <div class="stat-card">
          <v-icon size="48" color="primary" class="mb-4">emoji_events</v-icon>
          <h3 class="text-h4 font-weight-bold text-primary mb-2">150+</h3>
          <p class="text-body-1 text-medium-emphasis">Torneos Completados</p>
        </div>
      </v-col>

      <v-col cols="12" md="3" class="text-center">
        <div class="stat-card">
          <v-icon size="48" color="primary" class="mb-4">people</v-icon>
          <h3 class="text-h4 font-weight-bold text-primary mb-2">500+</h3>
          <p class="text-body-1 text-medium-emphasis">Jugadores Registrados</p>
        </div>
      </v-col>

      <v-col cols="12" md="3" class="text-center">
        <div class="stat-card">
          <v-icon size="48" color="primary" class="mb-4">sports_soccer</v-icon>
          <h3 class="text-h4 font-weight-bold text-primary mb-2">2,500+</h3>
          <p class="text-body-1 text-medium-emphasis">Partidas Jugadas</p>
        </div>
      </v-col>

      <v-col cols="12" md="3" class="text-center">
        <div class="stat-card">
          <v-icon size="48" color="primary" class="mb-4">favorite</v-icon>
          <h3 class="text-h4 font-weight-bold text-primary mb-2">98%</h3>
          <p class="text-body-1 text-medium-emphasis">Satisfacción</p>
        </div>
      </v-col>
    </v-row>

    <!-- CTA Section -->
    <v-row class="py-16 px-4 bg-primary">
      <v-col cols="12" class="text-center">
        <h2 class="text-h3 font-weight-bold text-white mb-4">
          ¿Listo para la Competencia?
        </h2>
        <p class="text-h6 text-white mb-8">
          Únete a Natsu Cup y demuestra que eres el mejor jugador de FIFA
        </p>
        <v-btn
          size="x-large"
          color="white"
          variant="elevated"
          class="px-8 text-primary"
          @click="getStarted"
        >
          <v-icon start>rocket_launch</v-icon>
          Comenzar Ahora
        </v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
// Datos de ejemplo para torneos activos
const activeTournaments = ref([
  {
    id: 1,
    name: 'Torneo de Verano 2024',
    description: 'El torneo más caliente del año. ¿Quién será el campeón?',
    status: 'active',
    participants: 12,
    maxParticipants: 16,
    date: '15 Jul 2024',
    prize: '🏆 Trofeo + $500',
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
    prize: '🏆 Trofeo + Cena',
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
    prize: '🏆 Trofeo + Entrenamiento',
    image: '/api/placeholder/400/200'
  }
])

// Métodos de navegación
const navigateToTournaments = () => {
  // Navegar a la página de torneos
  console.log('Navegando a torneos')
}

const joinTournament = (tournamentId) => {
  console.log('Uniéndose al torneo:', tournamentId)
  // Aquí iría la lógica para unirse al torneo
}

const viewTournament = (tournamentId) => {
  console.log('Viendo torneo:', tournamentId)
  // Aquí iría la lógica para ver detalles del torneo
}

const createTournament = () => {
  console.log('Creando nuevo torneo')
  // Aquí iría la lógica para crear un torneo
}

const getStarted = () => {
  console.log('Comenzando con Natsu Cup')
  // Aquí iría la lógica para comenzar
}
</script>

<style scoped>
.hero-section {
  background: linear-gradient(135deg, #1976d2 0%, #42a5f5 100%);
  min-height: 80vh;
  position: relative;
}

.hero-section::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grain" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="25" cy="25" r="1" fill="white" opacity="0.1"/><circle cx="75" cy="75" r="1" fill="white" opacity="0.1"/><circle cx="50" cy="10" r="0.5" fill="white" opacity="0.1"/><circle cx="10" cy="60" r="0.5" fill="white" opacity="0.1"/><circle cx="90" cy="40" r="0.5" fill="white" opacity="0.1"/></pattern></defs><rect width="100" height="100" fill="url(%23grain)"/></svg>');
  opacity: 0.3;
}

.hero-content {
  position: relative;
  z-index: 1;
}

.stat-card {
  padding: 2rem;
  border-radius: 12px;
  transition: transform 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-5px);
}

.v-card {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.v-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 25px rgba(0,0,0,0.15) !important;
}
</style>
