<template>
  <v-container class="pa-0 bracket-container" fluid>
    <v-row no-gutters>
      <v-col
        v-for="(round, index) in rounds"
        :key="'round-' + index"
        class="pr-4"
        cols="auto"
      >
        <h4 class="text-center mb-2">Fase {{ formatRound(index) }}</h4>
        <v-card
          v-for="match in round"
          :key="'match-' + match.id"
          class="mb-4 pa-2 text-center match-card"
          outlined
        >
          <div>{{ getTeamName(match, 'team1') }}</div>
          <div>vs</div>
          <div>{{ getTeamName(match, 'team2') }}</div>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  matches: {
    type: Array,
    required: true,
  },
})

// Agrupar por etapas (rondas) según el campo match.stage
const rounds = computed(() => {
  const stageMap = {}
  for (const match of props.matches) {
    if (!stageMap[match.stage]) {
      stageMap[match.stage] = []
    }
    stageMap[match.stage].push(match)
  }
  return Object.values(stageMap)
})

// Helper para nombres
function getTeamName(match, side) {
  const team = match[side]
  if (team?.name) return team.name
  if (match[`placeholder_${side}`]) return match[`placeholder_${side}`]
  return '—'
}

function formatRound(index) {
  const titles = ['Octavos', 'Cuartos', 'Semifinales', 'Final']
  return titles[index] || `Fase ${index + 1}`
}
</script>

<style scoped>
.bracket-container {
  overflow-x: auto;
  white-space: nowrap;
}

.match-card {
  min-width: 160px;
}
</style>
