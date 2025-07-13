<template>
  <v-expansion-panels class="mb-4">
    <v-expansion-panel>
      <v-expansion-panel-title>
        <v-icon start>mdi-trophy</v-icon>
        Clasificación del Grupo {{ groupCode }}
      </v-expansion-panel-title>
      <v-expansion-panel-text>
        <div v-if="standings.length === 0" class="text-center py-4">
          <v-icon class="mb-2" color="grey-lighten-1" size="32">
            mdi-trophy-outline
          </v-icon>
          <p class="text-body-2 text-grey-darken-1">
            No hay clasificación disponible
          </p>
        </div>
        <v-table v-else>
          <thead>
            <tr>
              <th>Pos</th>
              <th>Equipo</th>
              <th>PJ</th>
              <th>PG</th>
              <th>PE</th>
              <th>PP</th>
              <th>GF</th>
              <th>GC</th>
              <th>DG</th>
              <th>Pts</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="(team, index) in standings"
              :key="team.team_entry.id"
              :class="getStandingRowClass(index)"
            >
              <td>{{ index + 1 }}</td>
              <td>
                <div class="d-flex align-center">
                  <v-avatar class="mr-2" size="24">
                    <v-img
                      v-if="team.team_entry.assigned_team?.logo"
                      :src="team.team_entry.assigned_team.logo"
                    />
                    <v-icon v-else>mdi-shield</v-icon>
                  </v-avatar>
                  {{ team.team_entry.assigned_team?.name || `Equipo ${team.team_entry.id}` }}
                </div>
              </td>
              <td>{{ team.matches_played || 0 }}</td>
              <td>{{ team.wins || 0 }}</td>
              <td>{{ team.draws || 0 }}</td>
              <td>{{ team.losses || 0 }}</td>
              <td>{{ team.goals_for || 0 }}</td>
              <td>{{ team.goals_against || 0 }}</td>
              <td>{{ (team.goals_for || 0) - (team.goals_against || 0) }}</td>
              <td class="font-weight-bold">{{ team.points || 0 }}</td>
            </tr>
          </tbody>
        </v-table>
      </v-expansion-panel-text>
    </v-expansion-panel>
  </v-expansion-panels>
</template>

<script setup>
  // Props
  const props = defineProps({
    standings: {
      type: Array,
      default: () => [],
    },
    groupCode: {
      type: String,
      required: true,
    },
  })

  // Métodos
  const getStandingRowClass = index => {
    const classes = {
      0: 'first-place',
      1: 'second-place',
      2: 'third-place',
    }
    return classes[index] || ''
  }
</script>

<style scoped>
/* Estilos para clasificación */
.first-place {
  background-color: rgba(255, 215, 0, 0.1) !important;
  border-left: 4px solid gold;
}

.second-place {
  background-color: rgba(192, 192, 192, 0.1) !important;
  border-left: 4px solid silver;
}

.third-place {
  background-color: rgba(205, 127, 50, 0.1) !important;
  border-left: 4px solid #cd7f32;
}
</style>
