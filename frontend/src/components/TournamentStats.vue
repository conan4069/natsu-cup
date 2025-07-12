<template>
  <v-card>
    <v-card-title class="text-h6">
      <v-icon start>mdi-chart-line</v-icon>
      Estadísticas del Torneo
    </v-card-title>
    <v-card-text>
      <div class="mb-3">
        <span class="text-body-2 text-grey-darken-1">Grupos:</span>
        <div class="font-weight-medium">{{ stats.groupsCount }}</div>
      </div>
      <div class="mb-3">
        <span class="text-body-2 text-grey-darken-1">Equipos por grupo:</span>
        <div class="font-weight-medium">{{ stats.teamsPerGroup }}</div>
      </div>
      <div class="mb-3">
        <span class="text-body-2 text-grey-darken-1">Partidos jugados:</span>
        <div class="font-weight-medium">{{ stats.matchesPlayed }}</div>
      </div>
      <div class="mb-3">
        <span class="text-body-2 text-grey-darken-1">Total de partidos:</span>
        <div class="font-weight-medium">{{ stats.totalMatches }}</div>
      </div>
      <div class="mb-3">
        <span class="text-body-2 text-grey-darken-1">Progreso:</span>
        <div class="font-weight-medium">{{ stats.progressPercentage }}%</div>
      </div>

      <!-- Estado de la fase eliminatoria -->
      <v-divider class="my-4" />
      <div class="mb-3">
        <span class="text-body-2 text-grey-darken-1">Fase Eliminatoria:</span>
        <div class="font-weight-medium">
          <v-chip
            :color="knockoutStatus.color"
            size="small"
          >
            {{ knockoutStatus.text }}
          </v-chip>
        </div>
      </div>

      <!-- Equipos clasificados -->
      <div v-if="stats.qualifiedTeams > 0" class="mb-3">
        <span class="text-body-2 text-grey-darken-1">Equipos Clasificados:</span>
        <div class="font-weight-medium">{{ stats.qualifiedTeams }}</div>
      </div>
    </v-card-text>
  </v-card>
</template>

<script setup>
  // Props
  const props = defineProps({
    stats: {
      type: Object,
      default: () => ({
        groupsCount: 0,
        teamsPerGroup: 0,
        matchesPlayed: 0,
        totalMatches: 0,
        progressPercentage: 0,
        qualifiedTeams: 0,
      }),
    },
    tournament: {
      type: Object,
      default: () => ({}),
    },
  })

  // Computed
  const knockoutStatus = computed(() => {
    if (!props.tournament?.has_knockout) {
      return { text: 'No habilitada', color: 'grey' }
    }

    if (props.stats.progressPercentage === 100) {
      return { text: 'Lista para generar', color: 'success' }
    }

    return { text: 'Esperando grupos', color: 'warning' }
  })
</script>
