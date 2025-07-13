<template>
  <div class="tournament-bracket-visual">
    <div class="bracket-grid" :style="{ gridTemplateColumns: `repeat(${bracketStages.length}, 260px)` }">
      <template v-for="(stage, colIdx) in bracketStages" :key="stage">
        <div class="bracket-stage">
          <h3 class="stage-title">{{ getStageLabel(stage) }}</h3>
          <div class="matches-container">
            <div
              v-for="(match, rowIdx) in getMatchesByStage(stage)"
              :key="match.id"
              class="bracket-match"
              :style="{ gridRow: `${getMatchGridRow(stage, rowIdx)}` }"
            >
              <!-- Equipo 1 -->
              <div class="team-slot" :class="{ 'winner': match.winner === 'team1' }">
                <v-avatar class="mr-3" size="32">
                  <v-img
                    v-if="match.team1?.logo && match.team1.logo !== 'null'"
                    :src="match.team1.logo"
                  />
                  <v-icon v-else size="20">mdi-shield</v-icon>
                </v-avatar>
                <span class="team-name">{{ match.team1?.name || 'Por definir' }}</span>
                <span v-if="match.played" class="team-score">{{ match.team1_score ?? '' }}</span>
              </div>
              <!-- Equipo 2 -->
              <div class="team-slot" :class="{ 'winner': match.winner === 'team2' }">
                <v-avatar class="mr-3" size="32">
                  <v-img
                    v-if="match.team2?.logo && match.team2.logo !== 'null'"
                    :src="match.team2.logo"
                  />
                  <v-icon v-else size="20">mdi-shield</v-icon>
                </v-avatar>
                <span class="team-name">{{ match.team2?.name || 'Por definir' }}</span>
                <span v-if="match.played" class="team-score">{{ match.team2_score ?? '' }}</span>
              </div>
              <!-- SVG para líneas de conexión -->
              <svg
                v-if="colIdx < bracketStages.length - 1"
                class="bracket-connector"
                :height="connectorHeight"
                :width="connectorWidth"
              >
                <line
                  stroke="#bdbdbd"
                  stroke-dasharray="6,4"
                  stroke-width="2"
                  :x1="connectorWidth"
                  x2="0"
                  :y1="connectorHeight / 2"
                  :y2="connectorHeight / 2"
                />
              </svg>
            </div>
          </div>
        </div>
      </template>
    </div>
  </div>
</template>

<script setup>
  import { computed } from 'vue'

  const props = defineProps({
    matches: {
      type: Array,
      default: () => [],
    },
  })

  const connectorHeight = 60
  const connectorWidth = 40

  // Extrae todas las etapas únicas y las ordena
  const bracketStages = computed(() => {
    const order = [
      'round_of_32',
      'round_of_16',
      'octavos',
      'quarterfinal',
      'semifinal',
      'final',
    ]
    const uniqueStages = [...new Set(props.matches.map(m => m.stage))]
    return uniqueStages.sort((a, b) => order.indexOf(a) - order.indexOf(b))
  })

  // Devuelve los partidos de una etapa
  const getMatchesByStage = stage => {
    return props.matches.filter(m => m.stage === stage)
  }

  // Devuelve el nombre legible de la etapa
  const getStageLabel = stage => {
    const map = {
      round_of_32: 'Ronda de 32',
      round_of_16: 'Octavos de final',
      octavos: 'Octavos de final',
      quarterfinal: 'Cuartos de final',
      semifinal: 'Semifinal',
      final: 'Final',
      playoff_qualification: 'Repechaje',
    }
    return map[stage] || stage
  }

  // Calcula la fila de grid para alinear los partidos visualmente
  const getMatchGridRow = (stage, idx) => {
    // Puedes mejorar esta lógica para alinear los partidos según la ronda
    // Por ahora, simplemente los apila
    return idx + 1
  }
</script>

<style scoped>
.tournament-bracket-visual {
  width: 100%;
  padding: 16px 0;
  overflow-x: auto;
}
.bracket-grid {
  display: grid;
  gap: 0 40px;
  align-items: start;
}
.bracket-stage {
  display: flex;
  flex-direction: column;
  align-items: center;
}
.stage-title {
  text-align: center;
  margin-bottom: 20px;
  font-weight: bold;
  color: var(--v-primary-base);
  background-color: white;
  padding: 8px 16px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
.matches-container {
  display: flex;
  flex-direction: column;
  gap: 60px;
}
.bracket-match {
  background: white;
  border: 2px solid #e0e0e0;
  border-radius: 12px;
  padding: 12px 8px;
  position: relative;
  min-width: 200px;
  min-height: 60px;
  margin-bottom: 0;
  display: flex;
  flex-direction: column;
  align-items: stretch;
  justify-content: center;
}
.team-slot {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 4px 0;
  border-radius: 8px;
  transition: all 0.3s ease;
}
.team-slot.winner {
  background: var(--v-success-lighten5);
  border: 1px solid var(--v-success-base);
}
.team-info {
  display: flex;
  align-items: center;
  flex: 1;
}
.team-name {
  font-weight: 500;
}
.team-score {
  font-weight: bold;
  font-size: 1.1em;
  color: var(--v-primary-base);
  min-width: 30px;
  text-align: center;
}
.bracket-connector {
  position: absolute;
  right: -40px;
  top: 50%;
  transform: translateY(-50%);
  z-index: 1;
}
@media (max-width: 900px) {
  .bracket-grid {
    grid-template-columns: 1fr !important;
    gap: 20px;
  }
  .bracket-stage {
    min-width: auto;
  }
}
</style>
