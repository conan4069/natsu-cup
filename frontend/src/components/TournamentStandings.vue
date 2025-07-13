<template>
  <v-card>
    <v-card-title class="text-h6">
      <v-icon start>mdi-trophy</v-icon>
      {{ title }}
    </v-card-title>
    <v-card-text>
      <div v-if="standings.length === 0" class="text-center py-8">
        <v-icon class="mb-4" color="grey-lighten-1" size="48">
          mdi-trophy
        </v-icon>
        <h4 class="text-h6 text-grey-darken-1 mb-2">
          No hay clasificación disponible
        </h4>
        <p class="text-body-2 text-grey-darken-1">
          La clasificación aparecerá cuando se jueguen partidos.
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
            :key="team.id"
            :class="{ 'qualified': isQualified(index) }"
          >
            <td>{{ index + 1 }}</td>
            <td>
              <div class="d-flex align-center">
                <v-avatar class="mr-2" size="24">
                  <v-img
                    v-if="team.assigned_team?.logo && team.assigned_team.logo !== 'null'"
                    alt="Logo"
                    :src="team.assigned_team.logo"
                  />
                  <v-icon v-else>mdi-shield</v-icon>
                </v-avatar>
                {{ team.assigned_team?.name || 'Sin equipo' }}
              </div>
            </td>
            <td>{{ team.matches_played }}</td>
            <td>{{ team.wins }}</td>
            <td>{{ team.draws }}</td>
            <td>{{ team.losses }}</td>
            <td>{{ team.goals_for }}</td>
            <td>{{ team.goals_against }}</td>
            <td>{{ team.goal_difference }}</td>
            <td class="font-weight-bold">{{ team.points }}</td>
          </tr>
        </tbody>
      </v-table>
    </v-card-text>
  </v-card>
</template>

<script setup>
// Props
  const props = defineProps({
    standings: {
      type: Array,
      default: () => [],
    },
    title: {
      type: String,
      default: 'Clasificación',
    },
    qualifiedCount: {
      type: Number,
      default: 0,
    },
  })

  // Computed
  const isQualified = index => {
    return props.qualifiedCount > 0 && index < props.qualifiedCount
  }
</script>

<style scoped>
.qualified {
  background-color: rgba(var(--v-theme-success), 0.1);
}
</style>
