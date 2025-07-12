<template>
  <div class="tournament-bracket">
    <!-- Header del bracket -->
    <div class="bracket-header mb-6">
      <h2 class="text-h5 font-weight-bold mb-2">{{ tournament?.name }} - Fase Eliminatoria</h2>
      <div class="d-flex align-center gap-4">
        <v-chip
          v-for="stage in stages"
          :key="stage.value"
          :color="currentStage === stage.value ? 'primary' : 'grey'"
          :variant="currentStage === stage.value ? 'elevated' : 'outlined'"
          @click="setCurrentStage(stage.value)"
        >
          {{ stage.label }}
        </v-chip>
      </div>
    </div>

    <!-- Ganadores destacados -->
    <div v-if="winners.length > 0" class="winners-section mb-6">
      <h3 class="text-h6 font-weight-bold mb-4">Ganadores Destacados</h3>
      <div class="winners-grid">
        <WinnerCard
          v-for="(winner, index) in winners"
          :key="winner.id"
          :is-champion="index === 0"
          :winner="winner"
        />
      </div>
    </div>

    <!-- Contenido del bracket -->
    <div class="bracket-container">
      <div class="bracket-grid">
        <!-- Cuartos de final -->
        <div v-if="showQuarterfinals" class="bracket-round quarterfinals">
          <h3 class="round-title">Cuartos de Final</h3>
          <div class="matches-container">
            <div
              v-for="match in quarterfinalMatches"
              :key="match.id"
              class="match-card"
              :class="{ 'match-completed': match.played }"
            >
              <div class="match-header">
                <span class="match-number">M{{ match.id }}</span>
                <v-chip
                  v-if="match.played"
                  :color="match.winner ? 'success' : 'grey'"
                  size="small"
                >
                  {{ match.winner ? 'Completado' : 'En progreso' }}
                </v-chip>
              </div>

              <div class="match-teams">
                <div
                  class="team"
                  :class="{ 'winner': match.winner === 'team1' }"
                >
                  <div class="team-info">
                    <v-avatar class="mr-3" size="32">
                      <v-img
                        v-if="match.team1?.logo"
                        alt="Logo"
                        :src="match.team1.logo"
                      />
                      <v-icon v-else size="20">mdi-shield</v-icon>
                    </v-avatar>
                    <span class="team-name">
                      {{ match.team1?.name || match.placeholder_team1 || 'TBD' }}
                    </span>
                  </div>
                  <div v-if="match.played" class="team-score">
                    {{ match.team1_score || 0 }}
                  </div>
                </div>

                <div class="vs-divider">VS</div>

                <div
                  class="team"
                  :class="{ 'winner': match.winner === 'team2' }"
                >
                  <div class="team-info">
                    <v-avatar class="mr-3" size="32">
                      <v-img
                        v-if="match.team2?.logo"
                        alt="Logo"
                        :src="match.team2.logo"
                      />
                      <v-icon v-else size="20">mdi-shield</v-icon>
                    </v-avatar>
                    <span class="team-name">
                      {{ match.team2?.name || match.placeholder_team2 || 'TBD' }}
                    </span>
                  </div>
                  <div v-if="match.played" class="team-score">
                    {{ match.team2_score || 0 }}
                  </div>
                </div>
              </div>

              <div class="match-actions">
                <v-btn
                  v-if="!match.played"
                  color="primary"
                  rounded="xl"
                  size="small"
                  variant="outlined"
                  @click="editMatch(match)"
                >
                  <v-icon start>mdi-pencil</v-icon>
                  Editar
                </v-btn>
                <v-btn
                  v-else
                  color="info"
                  rounded="xl"
                  size="small"
                  variant="text"
                  @click="viewMatch(match)"
                >
                  <v-icon start>mdi-eye</v-icon>
                  Ver
                </v-btn>
              </div>
            </div>
          </div>
        </div>

        <!-- Semifinales -->
        <div v-if="showSemifinals" class="bracket-round semifinals">
          <h3 class="round-title">Semifinales</h3>
          <div class="matches-container">
            <div
              v-for="match in semifinalMatches"
              :key="match.id"
              class="match-card"
              :class="{ 'match-completed': match.played }"
            >
              <div class="match-header">
                <span class="match-number">M{{ match.id }}</span>
                <v-chip
                  v-if="match.played"
                  :color="match.winner ? 'success' : 'grey'"
                  size="small"
                >
                  {{ match.winner ? 'Completado' : 'En progreso' }}
                </v-chip>
              </div>

              <div class="match-teams">
                <div
                  class="team"
                  :class="{ 'winner': match.winner === 'team1' }"
                >
                  <div class="team-info">
                    <v-avatar class="mr-3" size="32">
                      <v-img
                        v-if="match.team1?.logo"
                        alt="Logo"
                        :src="match.team1.logo"
                      />
                      <v-icon v-else size="20">mdi-shield</v-icon>
                    </v-avatar>
                    <span class="team-name">
                      {{ match.team1?.name || match.placeholder_team1 || 'TBD' }}
                    </span>
                  </div>
                  <div v-if="match.played" class="team-score">
                    {{ match.team1_score || 0 }}
                  </div>
                </div>

                <div class="vs-divider">VS</div>

                <div
                  class="team"
                  :class="{ 'winner': match.winner === 'team2' }"
                >
                  <div class="team-info">
                    <v-avatar class="mr-3" size="32">
                      <v-img
                        v-if="match.team2?.logo"
                        alt="Logo"
                        :src="match.team2.logo"
                      />
                      <v-icon v-else size="20">mdi-shield</v-icon>
                    </v-avatar>
                    <span class="team-name">
                      {{ match.team2?.name || match.placeholder_team2 || 'TBD' }}
                    </span>
                  </div>
                  <div v-if="match.played" class="team-score">
                    {{ match.team2_score || 0 }}
                  </div>
                </div>
              </div>

              <div class="match-actions">
                <v-btn
                  v-if="!match.played"
                  color="primary"
                  rounded="xl"
                  size="small"
                  variant="outlined"
                  @click="editMatch(match)"
                >
                  <v-icon start>mdi-pencil</v-icon>
                  Editar
                </v-btn>
                <v-btn
                  v-else
                  color="info"
                  rounded="xl"
                  size="small"
                  variant="text"
                  @click="viewMatch(match)"
                >
                  <v-icon start>mdi-eye</v-icon>
                  Ver
                </v-btn>
              </div>
            </div>
          </div>
        </div>

        <!-- Final -->
        <div v-if="showFinal" class="bracket-round final">
          <h3 class="round-title">Final</h3>
          <div class="matches-container">
            <div
              v-for="match in finalMatches"
              :key="match.id"
              class="match-card final-match"
              :class="{ 'match-completed': match.played }"
            >
              <div class="match-header">
                <span class="match-number">M{{ match.id }}</span>
                <v-chip
                  v-if="match.played"
                  :color="match.winner ? 'success' : 'grey'"
                  size="small"
                >
                  {{ match.winner ? 'Campeón' : 'En progreso' }}
                </v-chip>
              </div>

              <div class="match-teams">
                <div
                  class="team"
                  :class="{ 'winner': match.winner === 'team1' }"
                >
                  <div class="team-info">
                    <v-avatar class="mr-3" size="32">
                      <v-img
                        v-if="match.team1?.logo"
                        alt="Logo"
                        :src="match.team1.logo"
                      />
                      <v-icon v-else size="20">mdi-shield</v-icon>
                    </v-avatar>
                    <span class="team-name">
                      {{ match.team1?.name || match.placeholder_team1 || 'TBD' }}
                    </span>
                  </div>
                  <div v-if="match.played" class="team-score">
                    {{ match.team1_score || 0 }}
                  </div>
                </div>

                <div class="vs-divider">VS</div>

                <div
                  class="team"
                  :class="{ 'winner': match.winner === 'team2' }"
                >
                  <div class="team-info">
                    <v-avatar class="mr-3" size="32">
                      <v-img
                        v-if="match.team2?.logo"
                        alt="Logo"
                        :src="match.team2.logo"
                      />
                      <v-icon v-else size="20">mdi-shield</v-icon>
                    </v-avatar>
                    <span class="team-name">
                      {{ match.team2?.name || match.placeholder_team2 || 'TBD' }}
                    </span>
                  </div>
                  <div v-if="match.played" class="team-score">
                    {{ match.team2_score || 0 }}
                  </div>
                </div>
              </div>

              <div class="match-actions">
                <v-btn
                  v-if="!match.played"
                  color="primary"
                  rounded="xl"
                  size="small"
                  variant="outlined"
                  @click="editMatch(match)"
                >
                  <v-icon start>mdi-pencil</v-icon>
                  Editar
                </v-btn>
                <v-btn
                  v-else
                  color="info"
                  rounded="xl"
                  size="small"
                  variant="text"
                  @click="viewMatch(match)"
                >
                  <v-icon start>mdi-eye</v-icon>
                  Ver
                </v-btn>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Botones de acción -->
    <div class="bracket-actions mt-6">
      <v-btn
        v-if="canGenerateQuarterfinals"
        color="primary"
        :loading="generating"
        prepend-icon="mdi-play"
        variant="elevated"
        @click="generateQuarterfinals"
      >
        Generar Cuartos de Final
      </v-btn>

      <v-btn
        v-if="canGenerateSemifinals"
        color="warning"
        :loading="generating"
        prepend-icon="mdi-arrow-right"
        variant="elevated"
        @click="generateSemifinals"
      >
        Generar Semifinales
      </v-btn>

      <v-btn
        v-if="canGenerateFinal"
        color="success"
        :loading="generating"
        prepend-icon="mdi-trophy"
        variant="elevated"
        @click="generateFinal"
      >
        Generar Final
      </v-btn>
    </div>
  </div>
</template>

<script setup>
  import { computed, ref, watch } from 'vue'

  // Props
  const props = defineProps({
    tournament: {
      type: Object,
      default: null,
    },
    matches: {
      type: Array,
      default: () => [],
    },
    generating: {
      type: Boolean,
      default: false,
    },
  })

  // Emits
  const emit = defineEmits(['generate-stage', 'edit-match', 'view-match'])

  // Estado reactivo
  const currentStage = ref('quarterfinal')

  // Etapas disponibles
  const stages = [
    { label: 'Cuartos', value: 'quarterfinal' },
    { label: 'Semifinales', value: 'semifinal' },
    { label: 'Final', value: 'final' },
  ]

  // Computed
  const quarterfinalMatches = computed(() => {
    return props.matches.filter(match => match.stage === 'quarterfinal')
  })

  const semifinalMatches = computed(() => {
    return props.matches.filter(match => match.stage === 'semifinal')
  })

  const finalMatches = computed(() => {
    return props.matches.filter(match => match.stage === 'final')
  })

  const showQuarterfinals = computed(() => {
    return currentStage.value === 'quarterfinal'
      || currentStage.value === 'semifinal'
      || currentStage.value === 'final'
  })

  const showSemifinals = computed(() => {
    return currentStage.value === 'semifinal'
      || currentStage.value === 'final'
  })

  const showFinal = computed(() => {
    return currentStage.value === 'final'
  })

  const canGenerateQuarterfinals = computed(() => {
    return quarterfinalMatches.value.length === 0
  })

  const canGenerateSemifinals = computed(() => {
    return quarterfinalMatches.value.length > 0
      && semifinalMatches.value.length === 0
      && quarterfinalMatches.value.every(match => match.played)
  })

  const canGenerateFinal = computed(() => {
    return semifinalMatches.value.length > 0
      && finalMatches.value.length === 0
      && semifinalMatches.value.every(match => match.played)
  })

  // Métodos
  const setCurrentStage = stage => {
    currentStage.value = stage
  }

  const generateQuarterfinals = () => {
    emit('generate-stage', { stage: 'quarterfinal', total_slots: 8 })
  }

  const generateSemifinals = () => {
    emit('generate-stage', { stage: 'semifinal', total_slots: 4 })
  }

  const generateFinal = () => {
    emit('generate-stage', { stage: 'final', total_slots: 2 })
  }

  const editMatch = match => {
    emit('edit-match', match)
  }

  const viewMatch = match => {
    emit('view-match', match)
  }
</script>

<style scoped>
.tournament-bracket {
  width: 100%;
}

.bracket-header {
  text-align: center;
}

.bracket-container {
  overflow-x: auto;
  margin: 20px 0;
}

.bracket-grid {
  display: flex;
  gap: 40px;
  min-width: max-content;
  padding: 20px;
}

.bracket-round {
  min-width: 300px;
}

.round-title {
  text-align: center;
  margin-bottom: 20px;
  font-weight: bold;
  color: var(--v-primary-base);
}

.matches-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.match-card {
  background: white;
  border: 2px solid #e0e0e0;
  border-radius: 12px;
  padding: 16px;
  transition: all 0.3s ease;
  position: relative;
}

.match-card:hover {
  border-color: var(--v-primary-base);
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.match-card.match-completed {
  border-color: var(--v-success-base);
  background: #f8fff8;
}

.match-card.final-match {
  border-width: 3px;
  border-color: var(--v-warning-base);
  background: #fff8f0;
}

.match-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.match-number {
  font-weight: bold;
  color: var(--v-primary-base);
}

.match-teams {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.team {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.team.winner {
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
  font-size: 1.2em;
  color: var(--v-primary-base);
  min-width: 30px;
  text-align: center;
}

.vs-divider {
  text-align: center;
  font-weight: bold;
  color: var(--v-grey-base);
  margin: 8px 0;
}

.match-actions {
  margin-top: 12px;
  text-align: center;
}

.bracket-actions {
  text-align: center;
  display: flex;
  justify-content: center;
  gap: 16px;
  flex-wrap: wrap;
}

/* Animaciones */
.match-card {
  animation: slideIn 0.5s ease-out;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.team.winner {
  animation: winnerGlow 0.5s ease-out;
}

@keyframes winnerGlow {
  0% {
    box-shadow: 0 0 0 rgba(76, 175, 80, 0);
  }
  50% {
    box-shadow: 0 0 20px rgba(76, 175, 80, 0.5);
  }
  100% {
    box-shadow: 0 0 0 rgba(76, 175, 80, 0);
  }
}

/* Responsive */
@media (max-width: 768px) {
  .bracket-grid {
    flex-direction: column;
    gap: 20px;
  }

  .bracket-round {
    min-width: auto;
  }

  .bracket-actions {
    flex-direction: column;
    align-items: center;
  }
}
</style>
