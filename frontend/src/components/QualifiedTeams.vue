<template>
  <v-card>
    <v-card-title class="text-h6">
      <v-icon start>mdi-trophy</v-icon>
      Equipos Clasificados para Fase Eliminatoria
    </v-card-title>
    <v-card-text>
      <!-- Resumen de clasificados -->
      <div class="mb-4">
        <v-alert
          class="mb-4"
          type="success"
          variant="tonal"
        >
          <template #prepend>
            <v-icon>mdi-check-circle</v-icon>
          </template>
          <strong>{{ qualifiedTeams.total_qualified }} equipos clasificados</strong>
          <div class="mt-1">
            {{ qualifiedTeams.group_winners.length }} ganadores de grupo •
            {{ qualifiedTeams.group_runners_up.length }} segundos lugares •
            {{ qualifiedTeams.best_third_place.length }} mejores terceros
          </div>
        </v-alert>
      </div>

      <!-- Ganadores de Grupo -->
      <div v-if="qualifiedTeams.group_winners.length > 0" class="mb-4">
        <h5 class="text-subtitle-1 mb-3">
          <v-icon color="gold" size="small">mdi-trophy</v-icon>
          Ganadores de Grupo
        </h5>
        <div class="d-flex flex-wrap gap-2">
          <v-card
            v-for="team in qualifiedTeams.group_winners"
            :key="team.team_entry.id"
            class="qualified-team-card winner"
            variant="outlined"
          >
            <v-card-text class="pa-3">
              <div class="d-flex align-center">
                <v-avatar class="mr-2" size="32">
                  <v-img
                    v-if="team.team_entry.assigned_team?.logo"
                    :src="team.team_entry.assigned_team.logo"
                  />
                  <v-icon v-else size="16">mdi-shield</v-icon>
                </v-avatar>
                <div>
                  <div class="font-weight-medium">{{ getTeamName(team.team_entry) }}</div>
                  <div class="text-caption text-grey-darken-1">
                    Grupo {{ team.group_code }} • {{ team.points }} pts
                  </div>
                </div>
              </div>
            </v-card-text>
          </v-card>
        </div>
      </div>

      <!-- Segundos Lugares -->
      <div v-if="qualifiedTeams.group_runners_up.length > 0" class="mb-4">
        <h5 class="text-subtitle-1 mb-3">
          <v-icon color="silver" size="small">mdi-medal</v-icon>
          Segundos Lugares
        </h5>
        <div class="d-flex flex-wrap gap-2">
          <v-card
            v-for="team in qualifiedTeams.group_runners_up"
            :key="team.team_entry.id"
            class="qualified-team-card runner-up"
            variant="outlined"
          >
            <v-card-text class="pa-3">
              <div class="d-flex align-center">
                <v-avatar class="mr-2" size="32">
                  <v-img
                    v-if="team.team_entry.assigned_team?.logo"
                    :src="team.team_entry.assigned_team.logo"
                  />
                  <v-icon v-else size="16">mdi-shield</v-icon>
                </v-avatar>
                <div>
                  <div class="font-weight-medium">{{ getTeamName(team.team_entry) }}</div>
                  <div class="text-caption text-grey-darken-1">
                    Grupo {{ team.group_code }} • {{ team.points }} pts
                  </div>
                </div>
              </div>
            </v-card-text>
          </v-card>
        </div>
      </div>

      <!-- Mejores Terceros -->
      <div v-if="qualifiedTeams.best_third_place.length > 0" class="mb-4">
        <h5 class="text-subtitle-1 mb-3">
          <v-icon color="bronze" size="small">mdi-medal-outline</v-icon>
          Mejores Terceros
        </h5>
        <div class="d-flex flex-wrap gap-2">
          <v-card
            v-for="team in qualifiedTeams.best_third_place"
            :key="team.team_entry.id"
            class="qualified-team-card third-place"
            variant="outlined"
          >
            <v-card-text class="pa-3">
              <div class="d-flex align-center">
                <v-avatar class="mr-2" size="32">
                  <v-img
                    v-if="team.team_entry.assigned_team?.logo"
                    :src="team.team_entry.assigned_team.logo"
                  />
                  <v-icon v-else size="16">mdi-shield</v-icon>
                </v-avatar>
                <div>
                  <div class="font-weight-medium">{{ getTeamName(team.team_entry) }}</div>
                  <div class="text-caption text-grey-darken-1">
                    Grupo {{ team.group_code }} • {{ team.points }} pts
                  </div>
                </div>
              </div>
            </v-card-text>
          </v-card>
        </div>
      </div>

      <!-- Botón para generar fase eliminatoria -->
      <div v-if="canGenerateKnockout" class="mt-4">
        <v-btn
          color="success"
          :loading="generatingKnockout"
          prepend-icon="mdi-trophy"
          rounded="xl"
          variant="elevated"
          @click="$emit('generate-knockout')"
        >
          {{ generatingKnockout ? 'Generando Eliminatoria...' : 'Generar Fase Eliminatoria' }}
        </v-btn>
      </div>
    </v-card-text>
  </v-card>
</template>

<script setup>
  // Props
  const props = defineProps({
    qualifiedTeams: {
      type: Object,
      default: () => ({
        group_winners: [],
        group_runners_up: [],
        best_third_place: [],
        total_qualified: 0,
      }),
    },
    canGenerateKnockout: {
      type: Boolean,
      default: false,
    },
    generatingKnockout: {
      type: Boolean,
      default: false,
    },
  })

  // Emits
  const emit = defineEmits(['generate-knockout'])

  // Métodos
  const getTeamName = teamEntry => {
    if (teamEntry.assigned_team) {
      return teamEntry.assigned_team.name
    }

    const playerNames = teamEntry.players.map(player => player.display_name)
    return playerNames.join(' & ')
  }
</script>

<style scoped>
.qualified-team-card {
  transition: transform 0.2s, box-shadow 0.2s;
  min-width: 200px;
}

.qualified-team-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.qualified-team-card.winner {
  border-left: 4px solid gold;
}

.qualified-team-card.runner-up {
  border-left: 4px solid silver;
}

.qualified-team-card.third-place {
  border-left: 4px solid #cd7f32;
}

/* Responsive */
@media (max-width: 768px) {
  .qualified-team-card {
    min-width: 100%;
  }
}
</style>
