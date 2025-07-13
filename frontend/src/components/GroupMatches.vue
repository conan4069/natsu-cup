<template>
  <v-expansion-panels class="mb-4">
    <v-expansion-panel>
      <v-expansion-panel-title>
        <v-icon start>mdi-soccer</v-icon>
        Partidos del Grupo {{ groupCode }}
      </v-expansion-panel-title>
      <v-expansion-panel-text>
        <div v-if="matches.length === 0" class="text-center py-8">
          <v-icon class="mb-4" color="grey-lighten-1" size="48">
            mdi-soccer
          </v-icon>
          <h4 class="text-h6 text-grey-darken-1 mb-2">
            No hay partidos programados
          </h4>
          <p class="text-body-2 text-grey-darken-1">
            Los partidos aparecerán aquí cuando se generen los grupos.
          </p>
        </div>
        <div v-else>
          <v-card
            v-for="match in matches"
            :key="match.id"
            class="mb-3 match-card"
            variant="outlined"
          >
            <v-card-text>
              <div class="d-flex align-center justify-space-between">
                <div class="team-info">
                  <div class="d-flex align-center mb-2">
                    <v-avatar class="mr-2" size="32">
                      <v-img
                        v-if="getTeamLogo(match, 0)"
                        :src="getTeamLogo(match, 0)"
                      />
                      <v-icon v-else>mdi-shield</v-icon>
                    </v-avatar>
                    <div class="team-name">{{ match.team1_name }}</div>
                  </div>
                  <div class="team-score">{{ match.team1_score }}</div>
                </div>
                <div class="match-vs">
                  <v-chip
                    :color="match.played ? 'success' : 'warning'"
                    size="small"
                    variant="outlined"
                  >
                    {{ match.played ? 'Finalizado' : 'Pendiente' }}
                  </v-chip>
                </div>
                <div class="team-info">
                  <div class="d-flex align-center justify-start mb-2">
                    <div class="team-name">{{ match.team2_name }}</div>
                    <v-avatar class="ml-2" size="32">
                      <v-img
                        v-if="getTeamLogo(match, 1)"
                        :src="getTeamLogo(match, 1)"
                      />
                      <v-icon v-else>mdi-shield</v-icon>
                    </v-avatar>
                  </div>
                  <div class="team-score">{{ match.team2_score }}</div>
                </div>
                <div class="match-actions">
                  <v-btn
                    v-if="!match.played"
                    color="primary"
                    density="comfortable"
                    icon="mdi-pencil"
                    size="small"
                    variant="text"
                    @click="editMatch(match)"
                  />
                </div>
              </div>
            </v-card-text>
          </v-card>
        </div>
      </v-expansion-panel-text>
    </v-expansion-panel>
  </v-expansion-panels>
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

  // Métodos
  const getTeamLogo = (match, teamIndex) => {
    const participant = match.participants?.[teamIndex]
    return participant?.assigned_team?.logo || null
  }

  const editMatch = match => {
    emit('edit-match', match)
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
}
</style>
