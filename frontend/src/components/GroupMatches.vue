<template>
  <v-card variant="outlined">
    <v-card-title class="text-subtitle-1 d-flex align-center justify-space-between">
      <span>Partidos del Grupo {{ groupCode }}</span>
      <v-chip
        :color="getGroupProgressColor()"
        size="small"
      >
        {{ getGroupProgressText() }}
      </v-chip>
    </v-card-title>
    <v-card-text>
      <div v-for="match in matches" :key="match.id" class="mb-4">
        <v-card class="match-card" variant="outlined">
          <v-card-text>
            <div class="d-flex align-center justify-space-between">
              <div class="d-flex align-center flex-grow-1">
                <!-- Equipo 1 -->
                <div class="team-info">
                  <div class="team-header">
                    <v-avatar class="mr-2" size="32">
                      <v-img
                        v-if="getTeam1(match)?.assigned_team?.logo"
                        :src="getTeam1(match).assigned_team.logo"
                        alt="Logo equipo 1"
                      />
                      <v-icon v-else size="20">mdi-shield</v-icon>
                    </v-avatar>
                    <div class="team-name">{{ getTeam1Name(match) }}</div>
                  </div>
                  <div v-if="match.played" class="team-score">
                    {{ getTeam1Score(match) }}
                  </div>
                  <!-- Participantes del equipo 1 -->
                  <div class="participants-chips mt-1">
                    <v-chip
                      v-for="player in getTeam1(match)?.players || []"
                      :key="player.id"
                      class="ma-1"
                      color="primary"
                      label
                      size="x-small"
                      variant="outlined"
                    >
                      <v-avatar v-if="player.avatar" left size="16">
                        <v-img :src="player.avatar" />
                      </v-avatar>
                      {{ player.display_name }}
                    </v-chip>
                  </div>
                </div>

                <div class="match-vs">
                  <span class="text-h6 font-weight-bold text-grey">VS</span>
                </div>

                <!-- Equipo 2 -->
                <div class="team-info text-right">
                  <div class="team-header">
                    <div class="team-name">{{ getTeam2Name(match) }}</div>
                    <v-avatar class="ml-2" size="32">
                      <v-img
                        v-if="getTeam2(match)?.assigned_team?.logo"
                        :src="getTeam2(match).assigned_team.logo"
                        alt="Logo equipo 2"
                      />
                      <v-icon v-else size="20">mdi-shield</v-icon>
                    </v-avatar>
                  </div>
                  <div v-if="match.played" class="team-score">
                    {{ getTeam2Score(match) }}
                  </div>
                  <!-- Participantes del equipo 2 -->
                  <div class="participants-chips mt-1">
                    <v-chip
                      v-for="player in getTeam2(match)?.players || []"
                      :key="player.id"
                      class="ma-1"
                      color="primary"
                      label
                      size="x-small"
                      variant="outlined"
                    >
                      <v-avatar v-if="player.avatar" left size="16">
                        <v-img :src="player.avatar" />
                      </v-avatar>
                      {{ player.display_name }}
                    </v-chip>
                  </div>
                </div>
              </div>

              <div class="match-actions">
                <v-chip
                  class="mb-2"
                  :color="match.played ? 'success' : 'warning'"
                  size="small"
                >
                  {{ match.played ? 'Jugado' : 'Pendiente' }}
                </v-chip>

                <v-btn
                  v-if="!match.played"
                  color="primary"
                  prepend-icon="mdi-pencil"
                  size="small"
                  variant="outlined"
                  @click="$emit('edit-match', match)"
                >
                  Registrar
                </v-btn>

                <v-btn
                  v-else
                  color="secondary"
                  prepend-icon="mdi-pencil"
                  size="small"
                  variant="outlined"
                  @click="$emit('edit-match', match)"
                >
                  Editar
                </v-btn>
              </div>
            </div>

            <!-- Resultado del partido -->
            <div v-if="match.played" class="mt-3">
              <v-divider class="mb-2" />
              <div class="d-flex align-center justify-space-between">
                <div class="text-caption text-grey-darken-1">
                  <strong>Resultado:</strong> {{ getTeam1Score(match) }} - {{ getTeam2Score(match) }}
                </div>
                <div class="text-caption">
                  <v-chip
                    :color="getWinnerColor(match)"
                    size="x-small"
                  >
                    {{ getWinnerText(match) }}
                  </v-chip>
                </div>
              </div>
            </div>
          </v-card-text>
        </v-card>
      </div>
    </v-card-text>
  </v-card>
</template>

<script setup>
  // Props
  const props = defineProps({
    matches: {
      type: Array,
      default: () => [],
    },
    groupCode: {
      type: String,
      required: true,
    },
  })

  // Emits
  const emit = defineEmits(['edit-match'])

  // Métodos para obtener información de equipos
  function getTeam1(match) {
    return match.participants?.[0] || null
  }

  function getTeam2(match) {
    return match.participants?.[1] || null
  }

  function getTeam1Name(match) {
    return getTeam1(match)?.assigned_team?.name ||
           getTeam1(match)?.team_name ||
           match.team1_name ||
           'Equipo 1'
  }

  function getTeam2Name(match) {
    return getTeam2(match)?.assigned_team?.name ||
           getTeam2(match)?.team_name ||
           match.team2_name ||
           'Equipo 2'
  }

  function getTeam1Score(match) {
    if (!match.goals || !getTeam1(match)) return 0
    return match.goals[getTeam1(match).id] || 0
  }

  function getTeam2Score(match) {
    if (!match.goals || !getTeam2(match)) return 0
    return match.goals[getTeam2(match).id] || 0
  }

  // Métodos existentes
  const getGroupProgressColor = () => {
    const playedMatches = props.matches.filter(match => match.played).length
    const totalMatches = props.matches.length

    if (totalMatches === 0) return 'grey'
    if (playedMatches === totalMatches) return 'success'
    if (playedMatches > 0) return 'warning'
    return 'grey'
  }

  const getGroupProgressText = () => {
    const playedMatches = props.matches.filter(match => match.played).length
    const totalMatches = props.matches.length

    if (totalMatches === 0) return 'Sin partidos'
    if (playedMatches === totalMatches) return 'Completado'
    return `${playedMatches}/${totalMatches} jugados`
  }

  const getWinnerColor = match => {
    const team1Score = getTeam1Score(match)
    const team2Score = getTeam2Score(match)

    if (team1Score === team2Score) return 'warning'
    return 'success'
  }

  const getWinnerText = match => {
    const team1Score = getTeam1Score(match)
    const team2Score = getTeam2Score(match)

    if (team1Score === team2Score) return 'Empate'
    if (team1Score > team2Score) return 'Ganó ' + getTeam1Name(match)
    return 'Ganó ' + getTeam2Name(match)
  }
</script>

<style scoped>
.match-card {
  transition: box-shadow 0.2s;
}

.match-card:hover {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.team-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.team-info.text-right {
  align-items: flex-end;
}

.team-header {
  display: flex;
  align-items: center;
  margin-bottom: 4px;
}

.team-name {
  font-weight: 500;
  margin-bottom: 4px;
}

.team-score {
  font-size: 1.5rem;
  font-weight: bold;
  color: var(--v-primary-base);
}

.match-vs {
  margin: 0 16px;
  display: flex;
  align-items: center;
}

.match-actions {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 8px;
}

.participants-chips {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  max-width: 200px;
}

.team-info.text-right .participants-chips {
  justify-content: flex-end;
}

/* Responsive */
@media (max-width: 768px) {
  .d-flex.align-center.justify-space-between {
    flex-direction: column;
    gap: 16px;
  }

  .match-actions {
    align-items: center;
  }

  .team-info {
    align-items: center !important;
  }

  .participants-chips {
    max-width: none;
  }
}
</style>
