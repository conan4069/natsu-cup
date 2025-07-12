<template>
  <v-card
    class="winner-card"
    :class="{ 'champion': isChampion }"
    variant="outlined"
  >
    <v-card-text class="text-center pa-6">
      <!-- Avatar del equipo/jugador -->
      <v-avatar class="mb-4" size="100">
        <v-img
          v-if="winner.avatar || winner.logo"
          alt="Avatar del ganador"
          cover
          :src="winner.avatar || winner.logo"
        />
        <v-icon v-else color="grey" size="50">mdi-trophy</v-icon>
      </v-avatar>

      <!-- Nombre del ganador -->
      <h2 class="text-h5 font-weight-bold mb-2">{{ winner.display_name || winner.name }}</h2>

      <!-- Tipo de ganador -->
      <v-chip
        class="mb-3"
        :color="isChampion ? 'success' : 'primary'"
        variant="elevated"
      >
        {{ isChampion ? '🏆 Campeón' : 'Ganador' }}
      </v-chip>

      <!-- Información adicional -->
      <div v-if="winner.players && winner.players.length > 1" class="mt-3">
        <p class="text-body-2 text-grey-darken-1 mb-2">Equipo:</p>
        <div class="d-flex flex-wrap justify-center gap-1">
          <v-chip
            v-for="player in winner.players"
            :key="player.id"
            size="small"
            variant="outlined"
          >
            {{ player.display_name }}
          </v-chip>
        </div>
      </div>

      <!-- Efectos visuales para campeón -->
      <div v-if="isChampion" class="champion-effects">
        <v-icon class="trophy-icon" color="amber" size="32">
          mdi-trophy
        </v-icon>
      </div>
    </v-card-text>
  </v-card>
</template>

<script setup>
// Props
  const props = defineProps({
    winner: {
      type: Object,
      required: true,
    },
    isChampion: {
      type: Boolean,
      default: false,
    },
  })
</script>

<style scoped>
.winner-card {
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.winner-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
}

.winner-card.champion {
  border-color: var(--v-success-base);
  background: linear-gradient(135deg, rgba(var(--v-theme-success), 0.1), rgba(var(--v-theme-primary), 0.05));
}

.champion-effects {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  pointer-events: none;
  display: flex;
  align-items: center;
  justify-content: center;
}

.trophy-icon {
  animation: bounce 2s infinite;
}

@keyframes bounce {
  0%, 20%, 50%, 80%, 100% {
    transform: translateY(0);
  }
  40% {
    transform: translateY(-10px);
  }
  60% {
    transform: translateY(-5px);
  }
}
</style>
