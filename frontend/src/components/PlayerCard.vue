<template>
  <v-card
    class="player-card"
    :class="{ 'selected': isSelected }"
    variant="outlined"
    @click="toggleSelection"
  >
    <v-card-text class="text-center pa-4">
      <!-- Avatar del jugador -->
      <v-avatar size="80" class="mb-3">
        <v-img
          v-if="player.avatar"
          :src="player.avatar"
          alt="Avatar del jugador"
          cover
        />
        <v-icon v-else size="40" color="grey">mdi-account-question</v-icon>
      </v-avatar>

      <!-- Nombre del jugador -->
      <h3 class="text-h6 font-weight-medium mb-2">{{ player.display_name }}</h3>

      <!-- Nickname si existe -->
      <p v-if="player.nickname" class="text-body-2 text-grey-darken-1 mb-0">
        {{ player.nickname }}
      </p>

      <!-- Indicador de selección -->
      <v-icon
        v-if="isSelected"
        class="selection-indicator"
        color="primary"
        size="24"
      >
        mdi-check-circle
      </v-icon>
    </v-card-text>
  </v-card>
</template>

<script setup>
import { computed } from 'vue'

// Props
const props = defineProps({
  player: {
    type: Object,
    required: true
  },
  isSelected: {
    type: Boolean,
    default: false
  }
})

// Emits
const emit = defineEmits(['toggle-selection'])

// Métodos
const toggleSelection = () => {
  emit('toggle-selection', props.player)
}
</script>

<style scoped>
.player-card {
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.player-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.player-card.selected {
  border-color: var(--v-primary-base);
  background-color: rgba(var(--v-theme-primary), 0.05);
}

.selection-indicator {
  position: absolute;
  top: 8px;
  right: 8px;
  background: white;
  border-radius: 50%;
  padding: 2px;
}

.player-card:hover {
  border-color: var(--v-primary-base);
}
</style>
