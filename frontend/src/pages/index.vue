<template>
  <v-container fluid class="pa-0">
  <!-- Hero Section -->
  <v-parallax src="@/assets/fondocesped.jpg">
    <v-row no-gutters>
      <v-col cols="12" class="d-flex justify-center">
        <div class="text-center" style="transform: translateX(-4%);">
          <v-img src="@/assets/LogoCup.png" width="600" class="mb-16" style="transform: translateX(6.4%);"></v-img>
          <v-icon size="120" color="primary" class="mb-16" style="padding-bottom: 700px;"></v-icon>
          <v-btn
            prepend-icon="mdi-account" stacked
            size="x-large"
            color="primary"
            variant="elevated"
            class="px-5 mr-11"
            style="transform: translateY(-175%);"
            rounded="xl"
            @click="navigateToTournaments"
          > 
          <h4>Registrarse</h4>
          </v-btn>
        </div>
      </v-col>
    </v-row>
  </v-parallax>

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
