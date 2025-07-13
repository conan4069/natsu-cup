<template>
  <div class="tournament-bracket bg-white py-4 px-3">
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

    <!-- Estado vacío -->
    <div v-if="showEmptyState" class="empty-state text-center py-8">
      <v-icon class="mb-4" color="grey-lighten-1" size="64">
        mdi-trophy-outline
      </v-icon>
      <h3 class="text-h6 text-grey-darken-1 mb-2">
        No hay eliminatorias generadas
      </h3>
      <p class="text-body-2 text-grey-darken-1 mb-4">
        Las eliminatorias aparecerán aquí cuando se generen desde la fase de grupos.
      </p>
      <v-btn
        color="primary"
        prepend-icon="mdi-trophy"
        rounded="xl"
        variant="elevated"
        @click="generateQuarterfinals"
      >
        Generar Eliminatorias
      </v-btn>
    </div>

    <!-- Loading state -->
    <div v-else-if="generating" class="text-center py-8">
      <v-progress-circular color="primary" indeterminate size="64" />
      <p class="text-body-2 text-grey-darken-1 mt-4">Generando eliminatorias...</p>
    </div>

    <!-- Contenido del bracket -->
    <div v-else-if="hasKnockoutMatches" class="bracket-container">
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
                        v-if="getTeamLogo(match.team1)"
                        alt="Logo"
                        :src="getTeamLogo(match.team1)"
                      />
                      <v-icon v-else size="20">mdi-shield</v-icon>
                    </v-avatar>
                    <div class="team-details">
                      <span class="team-name">
                        {{ getTeamName(match.team1) }}
                      </span>
                      <div v-if="getTeamPlayers(match.team1)?.length" class="team-players">
                        <span class="text-caption text-grey-darken-1">
                          {{ getTeamPlayers(match.team1).map(p => p.display_name).join(', ') }}
                        </span>
                      </div>
                    </div>
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
                        v-if="getTeamLogo(match.team2)"
                        alt="Logo"
                        :src="getTeamLogo(match.team2)"
                      />
                      <v-icon v-else size="20">mdi-shield</v-icon>
                    </v-avatar>
                    <div class="team-details">
                      <span class="team-name">
                        {{ getTeamName(match.team2) }}
                      </span>
                      <div v-if="getTeamPlayers(match.team2)?.length" class="team-players">
                        <span class="text-caption text-grey-darken-1">
                          {{ getTeamPlayers(match.team2).map(p => p.display_name).join(', ') }}
                        </span>
                      </div>
                    </div>
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
                        v-if="getTeamLogo(match.team1)"
                        alt="Logo"
                        :src="getTeamLogo(match.team1)"
                      />
                      <v-icon v-else size="20">mdi-shield</v-icon>
                    </v-avatar>
                    <div class="team-details">
                      <span class="team-name">
                        {{ getTeamName(match.team1) }}
                      </span>
                      <div v-if="getTeamPlayers(match.team1)?.length" class="team-players">
                        <span class="text-caption text-grey-darken-1">
                          {{ getTeamPlayers(match.team1).map(p => p.display_name).join(', ') }}
                        </span>
                      </div>
                    </div>
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
                        v-if="getTeamLogo(match.team2)"
                        alt="Logo"
                        :src="getTeamLogo(match.team2)"
                      />
                      <v-icon v-else size="20">mdi-shield</v-icon>
                    </v-avatar>
                    <div class="team-details">
                      <span class="team-name">
                        {{ getTeamName(match.team2) }}
                      </span>
                      <div v-if="getTeamPlayers(match.team2)?.length" class="team-players">
                        <span class="text-caption text-grey-darken-1">
                          {{ getTeamPlayers(match.team2).map(p => p.display_name).join(', ') }}
                        </span>
                      </div>
                    </div>
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
                        v-if="getTeamLogo(match.team1)"
                        alt="Logo"
                        :src="getTeamLogo(match.team1)"
                      />
                      <v-icon v-else size="20">mdi-shield</v-icon>
                    </v-avatar>
                    <div class="team-details">
                      <span class="team-name">
                        {{ getTeamName(match.team1) }}
                      </span>
                      <div v-if="getTeamPlayers(match.team1)?.length" class="team-players">
                        <span class="text-caption text-grey-darken-1">
                          {{ getTeamPlayers(match.team1).map(p => p.display_name).join(', ') }}
                        </span>
                      </div>
                    </div>
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
                        v-if="getTeamLogo(match.team2)"
                        alt="Logo"
                        :src="getTeamLogo(match.team2)"
                      />
                      <v-icon v-else size="20">mdi-shield</v-icon>
                    </v-avatar>
                    <div class="team-details">
                      <span class="team-name">
                        {{ getTeamName(match.team2) }}
                      </span>
                      <div v-if="getTeamPlayers(match.team2)?.length" class="team-players">
                        <span class="text-caption text-grey-darken-1">
                          {{ getTeamPlayers(match.team2).map(p => p.display_name).join(', ') }}
                        </span>
                      </div>
                    </div>
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
  import { computed, ref } from 'vue'

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

  // Computed corregidos
  const quarterfinalMatches = computed(() => {
    return props.matches.filter(match => match.stage === 'quarterfinal')
  })

  const semifinalMatches = computed(() => {
    return props.matches.filter(match => match.stage === 'semifinal')
  })

  const finalMatches = computed(() => {
    return props.matches.filter(match => match.stage === 'final')
  })

  const totalMatches = computed(() => {
    return quarterfinalMatches.value.length + semifinalMatches.value.length + finalMatches.value.length
  })

  const playedMatches = computed(() => {
    return props.matches.filter(match => match.played).length
  })

  const progressPercentage = computed(() => {
    if (totalMatches.value === 0) return 0
    return Math.min((playedMatches.value / totalMatches.value) * 100, 100) // Limitar a 100%
  })

  const quarterfinalsCompleted = computed(() => {
    return quarterfinalMatches.value.length > 0
      && quarterfinalMatches.value.every(match => match.played)
  })

  const semifinalsCompleted = computed(() => {
    return semifinalMatches.value.length > 0
      && semifinalMatches.value.every(match => match.played)
  })

  const finalCompleted = computed(() => {
    return finalMatches.value.length > 0
      && finalMatches.value.every(match => match.played)
  })

  // Determinar estado del torneo
  const tournamentStatus = computed(() => {
    if (!props.tournament) return 'unknown'

    const hasGroups = props.tournament.has_group_stage
    const hasKnockout = props.tournament.has_knockout
    const hasLeague = props.tournament.competition_type in ['league', 'hybrid']

    // Verificar si todos los partidos están completados
    const allMatchesCompleted = props.matches.length > 0 && props.matches.every(match => match.played)

    if (hasGroups && hasKnockout) {
      // Torneo con grupos + eliminatorias
      if (finalCompleted.value) return 'completed'
      else if (semifinalsCompleted.value) return 'final_stage'
      else if (quarterfinalsCompleted.value) return 'semifinal_stage'
      else return 'group_stage'
    } else if (hasLeague && hasKnockout) {
      // Liga + playoffs
      if (finalCompleted.value) return 'completed'
      else if (semifinalsCompleted.value) return 'final_stage'
      else if (quarterfinalsCompleted.value) return 'semifinal_stage'
      else return 'league_stage'
    } else if (hasLeague) {
      // Solo liga
      return allMatchesCompleted ? 'completed' : 'league_stage'
    } else if (hasKnockout) {
      // Solo eliminatorias
      if (finalCompleted.value) return 'completed'
      else if (semifinalsCompleted.value) return 'final_stage'
      else if (quarterfinalsCompleted.value) return 'semifinal_stage'
      else return 'knockout_stage'
    }

    return 'unknown'
  })

  const statusText = computed(() => {
    const status = tournamentStatus.value
    const statusMap = {
      completed: 'Completado',
      final_stage: 'Final',
      semifinal_stage: 'Semifinales',
      quarterfinal_stage: 'Cuartos de Final',
      group_stage: 'Fase de Grupos',
      league_stage: 'Fase de Liga',
      knockout_stage: 'Eliminatorias',
      unknown: 'Desconocido',
    }
    return statusMap[status] || 'Desconocido'
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

  // Agregar computed para verificar si hay eliminatorias
  const hasKnockoutMatches = computed(() => {
    return props.matches.length > 0
  })

  const showEmptyState = computed(() => {
    return !hasKnockoutMatches.value && !props.generating
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

  // Helper functions for new template - CORREGIDO
  const getTeamName = team => {
    return team?.name || team?.display_name || team?.team?.name || 'Por definir'
  }

  const getTeamLogo = team => {
    // Si no hay logo del equipo, usar un logo por defecto
    const logoUrl = team?.logo_url || team?.logo || team?.team?.logo_url || team?.team?.logo
    if (logoUrl) {
      return logoUrl
    }

    // Logo por defecto basado en el nombre del equipo
    const teamName = getTeamName(team)
    if (teamName && teamName !== 'Por definir') {
      // Puedes usar un servicio como DiceBear para generar avatares basados en el nombre
      return `https://api.dicebear.com/7.x/initials/svg?seed=${encodeURIComponent(teamName)}&backgroundColor=1f2937&textColor=ffffff`
    }

    return null
  }

  const getTeamPlayers = team => {
    return team?.players || team?.team?.players || []
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
  background-color: white;
  padding: 8px 16px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
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

.team-details {
  display: flex;
  flex-direction: column;
}

.team-players {
  margin-top: 2px;
}
</style>
