<template>
  <v-dialog v-model="dialog" max-width="600">
    <v-card>
      <v-card-title class="text-h6">
        <v-icon start>mdi-soccer</v-icon>
        Resultado del Partido
      </v-card-title>

      <v-card-text>
        <div v-if="match" class="match-info mb-4">
          <div class="d-flex align-center justify-space-between mb-3">
            <div class="team-display">
              <v-avatar size="48" class="mr-3">
                <v-img
                  v-if="match.team1?.logo"
                  :src="match.team1.logo"
                  alt="Logo equipo 1"
                />
                <v-icon v-else size="24">mdi-shield</v-icon>
              </v-avatar>
              <span class="text-h6 font-weight-bold">
                {{ match.team1?.name || match.placeholder_team1 || 'TBD' }}
              </span>
            </div>
            <div class="vs-divider">
              <span class="text-h4 font-weight-bold text-grey">VS</span>
            </div>
            <div class="team-display">
              <span class="text-h6 font-weight-bold">
                {{ match.team2?.name || match.placeholder_team2 || 'TBD' }}
              </span>
              <v-avatar size="48" class="ml-3">
                <v-img
                  v-if="match.team2?.logo"
                  :src="match.team2.logo"
                  alt="Logo equipo 2"
                />
                <v-icon v-else size="24">mdi-shield</v-icon>
              </v-avatar>
            </div>
          </div>

          <v-divider class="mb-4" />

          <div class="score-inputs">
            <div class="d-flex align-center justify-space-between">
              <div class="team-score-input">
                <label class="text-subtitle-2 mb-2 d-block">
                  {{ match.team1?.name || 'Equipo 1' }}
                </label>
                <v-text-field
                  v-model.number="team1Score"
                  type="number"
                  min="0"
                  variant="outlined"
                  density="comfortable"
                  class="score-field"
                  :rules="scoreRules"
                />
              </div>

              <div class="score-separator">
                <span class="text-h4 font-weight-bold text-grey">-</span>
              </div>

              <div class="team-score-input">
                <label class="text-subtitle-2 mb-2 d-block">
                  {{ match.team2?.name || 'Equipo 2' }}
                </label>
                <v-text-field
                  v-model.number="team2Score"
                  type="number"
                  min="0"
                  variant="outlined"
                  density="comfortable"
                  class="score-field"
                  :rules="scoreRules"
                />
              </div>
            </div>
          </div>

          <v-alert
            v-if="isDraw"
            type="warning"
            variant="tonal"
            class="mt-4"
          >
            <strong>Empate detectado:</strong> En caso de empate, se puede definir un ganador por penales o tiempo extra.
          </v-alert>

          <v-alert
            v-if="winner"
            type="success"
            variant="tonal"
            class="mt-4"
          >
            <strong>Ganador:</strong> {{ winner }}
          </v-alert>
        </div>
      </v-card-text>

      <v-card-actions>
        <v-spacer />
        <v-btn
          variant="outlined"
          @click="closeDialog"
        >
          Cancelar
        </v-btn>
        <v-btn
          color="primary"
          :disabled="!isValid"
          :loading="saving"
          variant="elevated"
          @click="saveResult"
        >
          <v-icon start>mdi-content-save</v-icon>
          Guardar Resultado
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup>
import { ref, computed, watch } from 'vue'

// Props
const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  },
  match: {
    type: Object,
    default: null
  }
})

// Emits
const emit = defineEmits(['update:modelValue', 'save-result'])

// Estado reactivo
const team1Score = ref(0)
const team2Score = ref(0)
const saving = ref(false)

// Computed
const dialog = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

const scoreRules = [
  v => v !== null && v !== undefined || 'El marcador es requerido',
  v => v >= 0 || 'El marcador no puede ser negativo',
  v => v <= 50 || 'El marcador no puede ser mayor a 50'
]

const isValid = computed(() => {
  return team1Score.value >= 0 &&
         team2Score.value >= 0 &&
         (team1Score.value > 0 || team2Score.value > 0)
})

const isDraw = computed(() => {
  return team1Score.value === team2Score.value &&
         team1Score.value > 0 &&
         team2Score.value > 0
})

const winner = computed(() => {
  if (!isValid.value) return null

  if (team1Score.value > team2Score.value) {
    return props.match?.team1?.name || 'Equipo 1'
  } else if (team2Score.value > team1Score.value) {
    return props.match?.team2?.name || 'Equipo 2'
  }

  return null
})

// Métodos
const closeDialog = () => {
  dialog.value = false
  resetForm()
}

const resetForm = () => {
  team1Score.value = 0
  team2Score.value = 0
}

const saveResult = async () => {
  if (!isValid.value) return

  saving.value = true
  try {
    const result = {
      matchId: props.match.id,
      team1Score: team1Score.value,
      team2Score: team2Score.value,
      winner: winner.value,
      isDraw: isDraw.value
    }

    emit('save-result', result)
    closeDialog()
  } catch (error) {
    console.error('Error al guardar resultado:', error)
  } finally {
    saving.value = false
  }
}

// Cargar datos del partido cuando se abre
watch(() => props.match, (newMatch) => {
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
