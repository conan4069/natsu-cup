<template>
  <v-timeline align="start" dense side="start">
    <v-timeline-item
      v-for="(item, index) in steps"
      :key="index"
      :dot-color="getColor(item.type)"
      :icon="getIcon(item.type)"
    >
      <template #opposite>
        <strong>{{ formatStepType(item) }}</strong>
      </template>

      <v-card class="pa-3" elevation="2">
        <v-card-title class="text-subtitle-1">{{
          item.team_name
        }}</v-card-title>
        <v-card-subtitle v-if="item.group">
          Grupo {{ item.group }}
        </v-card-subtitle>
        <v-card-text v-if="item.status">
          Estado:
          <strong v-if="item.status === 'qualified'">Clasificado ✅</strong>
          <strong v-else-if="item.status === 'pending'">Esperando ⏳</strong>
        </v-card-text>
      </v-card>
    </v-timeline-item>
  </v-timeline>
</template>

<script setup>
defineProps({
  steps: { type: Array, required: true },
})

function getColor(type) {
  switch (type) {
    case 'group_winner':
      return 'green'
    case 'group_runner_up':
      return 'blue'
    case 'best_third':
      return 'orange'
    default:
      return 'grey'
  }
}

function getIcon(type) {
  switch (type) {
    case 'group_winner':
      return 'mdi-trophy'
    case 'group_runner_up':
      return 'mdi-medal'
    case 'best_third':
      return 'mdi-soccer'
    default:
      return 'mdi-help-circle'
  }
}

function formatStepType(item) {
  if (item.type === 'group_winner') return '1º Grupo ' + item.group
  if (item.type === 'group_runner_up') return '2º Grupo ' + item.group
  if (item.type === 'best_third') return 'Mejor 3º'
  return 'Clasificación'
}
</script>
