<template>
  <v-dialog v-model="dialog" max-width="900">
    <v-card>
      <v-card-title class="text-h6">
        <v-icon start>mdi-soccer</v-icon>
        Resultado del Partido
      </v-card-title>

      <v-card-text>
        <div v-if="match" class="match-info mb-4">
          <div class="d-flex align-center justify-space-between mb-3">
            <!-- Equipo 1 -->
            <div class="team-display">
              <v-avatar class="mr-3" size="48">
                <v-img
                  v-if="getTeam(0)?.assigned_team?.logo && getTeam(0).assigned_team.logo !== 'null'"
                  alt="Logo equipo 1"
                  :src="getTeam(0).assigned_team.logo"
                />
                <v-icon v-else size="24">mdi-shield</v-icon>
              </v-avatar>
              <span class="text-h6 font-weight-bold">
                {{ getTeam(0)?.assigned_team?.name || getTeam(0)?.team_name || 'Equipo 1' }}
              </span>
              <div class="mt-2">
                <v-chip
                  v-for="player in getTeam(0)?.players || []"
                  :key="player.id"
                  class="ma-1"
                  color="primary"
                  label
                  size="small"
                  variant="outlined"
                >
                  <v-avatar v-if="player.avatar && player.avatar !== 'null'" left size="20">
                    <v-img :src="player.avatar" />
                  </v-avatar>
                  <v-icon v-else left size="20">mdi-account</v-icon>
                  {{ player.display_name }}
                </v-chip>
              </div>
            </div>
            <div class="vs-divider">
              <span class="text-h4 font-weight-bold text-grey">VS</span>
            </div>
            <!-- Equipo 2 -->
            <div class="team-display">
              <span class="text-h6 font-weight-bold">
                {{ getTeam(1)?.assigned_team?.name || getTeam(1)?.team_name || 'Equipo 2' }}
              </span>
              <v-avatar class="ml-3" size="48">
                <v-img
                  v-if="getTeam(1)?.assigned_team?.logo && getTeam(1).assigned_team.logo !== 'null'"
                  alt="Logo equipo 2"
                  :src="getTeam(1).assigned_team.logo"
                />
                <v-icon v-else size="24">mdi-shield</v-icon>
              </v-avatar>
              <div class="mt-2">
                <v-chip
                  v-for="player in getTeam(1)?.players || []"
                  :key="player.id"
                  class="ma-1"
                  color="primary"
                  label
                  size="small"
                  variant="outlined"
                >
                  <v-avatar v-if="player.avatar && player.avatar !== 'null'" left size="20">
                    <v-img :src="player.avatar" />
                  </v-avatar>
                  <v-icon v-else left size="20">mdi-account</v-icon>
                  {{ player.display_name }}
                </v-chip>
              </div>
            </div>
          </div>

          <v-divider class="mb-4" />

          <div class="score-inputs">
            <div class="d-flex align-center justify-space-between">
              <div class="team-score-input">
                <label class="text-subtitle-2 mb-2 d-block">
                  {{ getTeam(0)?.assigned_team?.name || getTeam(0)?.team_name || 'Equipo 1' }}
                </label>
                <v-text-field
                  v-model.number="team1Score"
                  class="score-field"
                  density="comfortable"
                  min="0"
                  placeholder="0"
                  rounded="xl"
                  :rules="scoreRules"
                  type="number"
                  variant="outlined"
                />
              </div>

              <div class="score-separator">
                <span class="text-h4 font-weight-bold text-grey">-</span>
              </div>

              <div class="team-score-input">
                <label class="text-subtitle-2 mb-2 d-block">
                  {{ getTeam(1)?.assigned_team?.name || getTeam(1)?.team_name || 'Equipo 2' }}
                </label>
                <v-text-field
                  v-model.number="team2Score"
                  class="score-field"
                  density="comfortable"
                  min="0"
                  placeholder="0"
                  rounded="xl"
                  :rules="scoreRules"
                  type="number"
                  variant="outlined"
                />
              </div>
            </div>
          </div>

          <v-alert
            v-if="isDraw"
            class="mt-4"
            type="warning"
            variant="tonal"
          >
            <strong>Empate detectado:</strong> En caso de empate, se puede definir un ganador por penales o tiempo extra.
          </v-alert>

          <v-alert
            v-if="winner"
            class="mt-4"
            type="success"
            variant="tonal"
          >
            <strong>Ganador:</strong> {{ winner }}
          </v-alert>
        </div>
      </v-card-text>

      <v-card-actions>
        <v-spacer />
        <v-btn
          rounded="xl"
          variant="outlined"
          @click="closeDialog"
        >
          Cancelar
        </v-btn>
        <v-btn
          color="primary"
          :disabled="!isValid"
          :loading="saving"
          rounded="xl"
          variant="elevated"
          @click="saveResult"
        >
          <v-icon start>mdi-content-save</v-icon>
          {{ isEditing ? 'Actualizar' : 'Guardar' }} Resultado
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup>
  import { computed, ref, watch } from 'vue'

  // Props
  const props = defineProps({
    modelValue: {
      type: Boolean,
      default: false,
    },
    match: {
      type: Object,
      default: null,
    },
  })

  // Emits
  const emit = defineEmits(['update:modelValue', 'save-result'])

  // Estado reactivo
  const team1Score = ref(null)
  const team2Score = ref(null)
  const saving = ref(false)

  // Computed
  const dialog = computed({
    get: () => props.modelValue,
    set: value => emit('update:modelValue', value),
  })

  const isEditing = computed(() => {
    return props.match?.played || false
  })

  const scoreRules = [
    v => (v !== null && v !== undefined && v !== '') || 'El marcador es requerido',
    v => v >= 0 || 'El marcador no puede ser negativo',
    v => v <= 50 || 'El marcador no puede ser mayor a 50',
  ]

  const isValid = computed(() => {
    return team1Score.value !== null
      && team2Score.value !== null
      && team1Score.value >= 0
      && team2Score.value >= 0
      && (team1Score.value > 0 || team2Score.value > 0)
  })

  const isDraw = computed(() => {
    return team1Score.value === team2Score.value
      && team1Score.value > 0
      && team2Score.value > 0
  })

  const winner = computed(() => {
    if (!isValid.value) return null

    if (team1Score.value > team2Score.value) {
      return getTeam(0)?.assigned_team?.name || getTeam(0)?.team_name || 'Equipo 1'
    } else if (team2Score.value > team1Score.value) {
      return getTeam(1)?.assigned_team?.name || getTeam(1)?.team_name || 'Equipo 2'
    }

    return null
  })

  // Métodos para obtener info de los equipos
  function getTeam (idx) {
    return props.match?.participants?.[idx] || null
  }

  // Métodos
  const closeDialog = () => {
    dialog.value = false
    resetForm()
  }

  const resetForm = () => {
    team1Score.value = null
    team2Score.value = null
  }

  const saveResult = async () => {
    if (!isValid.value) return

    saving.value = true
    try {
      const participants = props.match?.participants || []
      const team1Id = participants[0]?.id
      const team2Id = participants[1]?.id

      console.log('Match data:', props.match)
      console.log('Participants:', participants)
      console.log('Team1 ID:', team1Id)
      console.log('Team2 ID:', team2Id)
      console.log('Team1 Score:', team1Score.value)
      console.log('Team2 Score:', team2Score.value)

      const result = {
        matchId: props.match.id,
        team1Id: team1Id,
        team2Id: team2Id,
        team1Score: team1Score.value,
        team2Score: team2Score.value,
        winner: winner.value,
        isDraw: isDraw.value,
      }

      console.log('Resultado a enviar:', result)

      emit('save-result', result)
      closeDialog()
    } catch (error) {
      console.error('Error al guardar resultado:', error)
    } finally {
      saving.value = false
    }
  }

  // Cargar datos del partido cuando se abre
  watch(() => props.match, newMatch => {
    if (newMatch && newMatch.played) {
      // Si el partido ya tiene resultado, cargarlo
      const goals = newMatch.goals || {}
      const participants = newMatch.participants || []

      if (participants.length >= 2) {
        const team1Id = participants[0].id
        const team2Id = participants[1].id

        team1Score.value = goals[team1Id] || 0
        team2Score.value = goals[team2Id] || 0
      }
    } else {
      resetForm()
    }
  }, { immediate: true })
</script>

<style scoped>
.match-info {
  text-align: center;
}

.team-display {
  display: flex;
  align-items: center;
  flex: 1;
}

.team-display:first-child {
  justify-content: flex-start;
}

.team-display:last-child {
  justify-content: flex-end;
}

.vs-divider {
  margin: 0 20px;
}

.score-inputs {
  margin-top: 20px;
}

.team-score-input {
  flex: 1;
  max-width: 200px;
}

.score-field {
  text-align: center;
}

.score-separator {
  margin: 0 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 60px;
}

/* Responsive */
@media (max-width: 600px) {
  .d-flex.align-center.justify-space-between {
    flex-direction: column;
    gap: 20px;
  }

  .team-display {
    justify-content: center !important;
  }

  .vs-divider {
    margin: 10px 0;
  }

  .score-inputs .d-flex {
    flex-direction: column;
    gap: 20px;
  }

  .team-score-input {
    max-width: none;
  }

  .score-separator {
    margin: 10px 0;
  }
}
</style>
