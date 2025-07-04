<template>
  <v-stepper v-model="step">
    <v-stepper-header>
      <v-stepper-step
        v-for="(item, index) in steps"
        :key="index"
        :complete="step > index"
        :step="index + 1"
      >
        {{ getStepLabel(item) }}
      </v-stepper-step>
    </v-stepper-header>

    <v-stepper-items>
      <v-stepper-content
        v-for="(item, index) in steps"
        :key="'content-' + index"
        :step="index + 1"
      >
        <v-card class="mb-4" outlined>
          <v-card-title class="text-h6">{{ item.team_name }}</v-card-title>
          <v-card-text>
            <span v-if="item.type === 'group_winner'"
              >Clasificado por 🏆 1º del grupo {{ item.group }}</span
            >
            <span v-else-if="item.type === 'group_runner_up'"
              >Clasificado por 🥈 2º del grupo {{ item.group }}</span
            >
            <span v-else-if="item.type === 'best_third'">
              Tercero destacado
              {{
                item.status === 'qualified'
                  ? '✅ clasificado'
                  : '⏳ esperando repechaje'
              }}
            </span>
          </v-card-text>
        </v-card>
        <v-btn
          color="primary"
          :disabled="step >= steps.length"
          @click="nextStep"
        >
          Siguiente
        </v-btn>
      </v-stepper-content>
    </v-stepper-items>
  </v-stepper>
</template>

<script setup>
import { ref } from 'vue'

defineProps({
  steps: { type: Array, required: true },
})

const step = ref(1)

function getStepLabel(item) {
  if (item.type === 'group_winner') return `1º Grupo ${item.group}`
  if (item.type === 'group_runner_up') return `2º Grupo ${item.group}`
  if (item.type === 'best_third') return 'Mejor 3º'
  return 'Otro'
}

function nextStep() {
  step.value++
}
</script>

<style scoped>
.v-stepper-step {
  white-space: nowrap;
}
</style>
