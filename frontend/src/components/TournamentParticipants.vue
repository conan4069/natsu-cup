<template>
  <div class="tournament-participants">
    <!-- Buscador de jugadores -->
    <v-row class="mb-4">
      <v-col cols="12" md="6">
        <v-text-field
          v-model="searchQuery"
          class="mb-4"
          label="Buscar jugadores"
          prepend-inner-icon="mdi-magnify"
          rounded="xl"
          variant="outlined"
        />
      </v-col>
    </v-row>

    <!-- Jugadores disponibles -->
    <v-card class="mb-6" variant="outlined">
      <v-card-title class="text-subtitle-1">
        Jugadores disponibles ({{ filteredAvailablePlayers.length }})
      </v-card-title>
      <v-card-text>
        <div v-if="filteredAvailablePlayers.length === 0" class="text-center py-8">
          <v-icon class="mb-4" color="grey-lighten-1" size="48">
            mdi-account-group
          </v-icon>
          <h4 class="text-h6 text-grey-darken-1 mb-2">
            No hay jugadores disponibles
          </h4>
          <p class="text-body-2 text-grey-darken-1">
            Todos los jugadores han sido agregados al torneo.
          </p>
        </div>
        <div v-else class="players-grid">
          <PlayerCard
            v-for="player in filteredAvailablePlayers"
            :key="player.id"
            :player="player"
            :is-selected="false"
            @toggle-selection="addParticipant"
          />
        </div>
      </v-card-text>
    </v-card>

    <!-- Participantes seleccionados -->
    <v-card variant="outlined">
      <v-card-title class="text-subtitle-1">
        Participantes seleccionados ({{ participants.length }})
      </v-card-title>
      <v-card-text>
        <div v-if="participants.length === 0" class="text-center py-8">
          <v-icon class="mb-4" color="grey-lighten-1" size="48">
            mdi-account-group
          </v-icon>
          <h4 class="text-h6 text-grey-darken-1 mb-2">
            No hay participantes
          </h4>
          <p class="text-body-2 text-grey-darken-1">
            Selecciona jugadores de la lista superior para agregarlos al torneo.
          </p>
        </div>
        <div v-else class="players-grid">
          <PlayerCard
            v-for="player in participants"
            :key="player.id"
            :player="player"
            :is-selected="true"
            @toggle-selection="removeParticipant"
          />
        </div>
      </v-card-text>
    </v-card>
  </div>
</template>

<script setup>
  import { computed, ref } from 'vue'
  import PlayerCard from './PlayerCard.vue'

  // Props
  const props = defineProps({
    allPlayers: {
      type: Array,
      default: () => [],
    },
    participants: {
      type: Array,
      default: () => [],
    },
  })

  // Emits
  const emit = defineEmits(['update:participants'])

  // Estado reactivo
  const searchQuery = ref('')

  // Computed
  const filteredAvailablePlayers = computed(() => {
    const selectedIds = new Set(props.participants.map(p => p.id))
    let available = props.allPlayers.filter(player => !selectedIds.has(player.id))

    if (searchQuery.value) {
      const query = searchQuery.value.toLowerCase()
      available = available.filter(player =>
        player.display_name.toLowerCase().includes(query)
      )
    }

    return available
  })

  // Métodos
  const addParticipant = (player) => {
    const newParticipants = [...props.participants, player]
    emit('update:participants', newParticipants)
  }

  const removeParticipant = (player) => {
    const newParticipants = props.participants.filter(p => p.id !== player.id)
    emit('update:participants', newParticipants)
  }
</script>

<style scoped>
.players-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 16px;
}
</style>
