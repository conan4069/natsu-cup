<template>
  <v-data-table :items="steps" :headers="headers">
    <template #item.type="{ item }">
      <span v-if="item.type === 'group_winner'">🏆 Ganador Grupo {{ item.group }}</span>
      <span v-else-if="item.type === 'group_runner_up'">🥈 Segundo Grupo {{ item.group }}</span>
      <span v-else-if="item.type === 'best_third'">⚔️ Mejor 3º {{ item.status === 'qualified' ? '(Clasificado)' : '' }}</span>
    </template>
    <template #item.team_name="{ item }">
      {{ item.team_name }}
    </template>
    <template #item.status="{ item }">
      <span v-if="item.status === 'qualified'">✅ Clasificado</span>
      <span v-else-if="item.status === 'pending'">⏳ Esperando</span>
      <span v-else>–</span>
    </template>
  </v-data-table>
</template>
<script setup>
const headers = [
  {
    text: 'Clasificación',
    value: 'type',
    sortable: false
  },
  {
    text: 'Equipo',
    value: 'team_name',
    sortable: false
  },
  {
    text: 'Grupo',
    value: 'group',
    sortable: false
  },
  {
    text: 'Estado',
    value: 'status',
    sortable: false
  }
]

</script>
