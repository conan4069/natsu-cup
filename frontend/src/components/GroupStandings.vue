<template>
  <v-card class="mb-4" variant="outlined">
    <v-card-title class="text-subtitle-1">
      <v-icon start>mdi-trophy</v-icon>
      Clasificación
    </v-card-title>
    <v-card-text>
      <v-table density="compact">
        <thead>
          <tr>
            <th class="text-left">Pos</th>
            <th class="text-left">Equipo</th>
            <th class="text-center">PJ</th>
            <th class="text-center">PG</th>
            <th class="text-center">PE</th>
            <th class="text-center">PP</th>
            <th class="text-center">GF</th>
            <th class="text-center">GC</th>
            <th class="text-center">DG</th>
            <th class="text-center">Pts</th>
            <th class="text-center">Clas.</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="(standing, index) in standings"
            :key="standing.team_entry.id"
            :class="getStandingRowClass(index)"
          >
            <td class="font-weight-bold">{{ index + 1 }}</td>
            <td>
              <div class="d-flex align-center">
                <v-avatar class="mr-2" size="24">
                  <v-img
                    v-if="standing.team_entry.assigned_team?.logo && standing.team_entry.assigned_team.logo !== 'null'"
                    :src="standing.team_entry.assigned_team.logo"
                  />
                  <v-icon v-else size="16">mdi-shield</v-icon>
                </v-avatar>
                {{ getTeamName(standing.team_entry) }}
              </div>
            </td>
            <td class="text-center">{{ standing.matches_played || 0 }}</td>
            <td class="text-center">{{ standing.wins || 0 }}</td>
            <td class="text-center">{{ standing.draws || 0 }}</td>
            <td class="text-center">{{ standing.losses || 0 }}</td>
            <td class="text-center">{{ standing.goals_for || 0 }}</td>
            <td class="text-center">{{ standing.goals_against || 0 }}</td>
            <td class="text-center">{{ standing.goal_difference || 0 }}</td>
            <td class="text-center font-weight-bold">{{ standing.points || 0 }}</td>
            <td class="text-center">
              <v-chip
                v-if="getQualificationStatus(standing.team_entry.id)"
                :color="getQualificationColor(standing.team_entry.id)"
                size="x-small"
              >
                {{ getQualificationText(standing.team_entry.id) }}
              </v-chip>
            </td>
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
    qualifiedTeams: {
      type: Object,
      default: () => ({
        group_winners: [],
        group_runners_up: [],
        best_third_place: [],
      }),
    },
  })

  // Métodos
  const getStandingRowClass = index => {
    if (index === 0) return 'first-place'
    if (index === 1) return 'second-place'
    if (index === 2) return 'third-place'
    return ''
  }

  const getTeamName = teamEntry => {
    if (teamEntry.assigned_team) {
      return teamEntry.assigned_team.name
    }

    const playerNames = teamEntry.players.map(player => player.display_name)
    return playerNames.join(' & ')
  }

  const getQualificationStatus = teamEntryId => {
    const allQualified = [
      ...props.qualifiedTeams.group_winners,
      ...props.qualifiedTeams.group_runners_up,
      ...props.qualifiedTeams.best_third_place,
    ]
    return allQualified.find(team => team.team_entry.id === teamEntryId)
  }

  const getQualificationColor = teamEntryId => {
    const qualified = getQualificationStatus(teamEntryId)
    if (!qualified) return 'grey'

    if (qualified.qualification_type === 'group_winner') return 'success'
    if (qualified.qualification_type === 'group_runner_up') return 'warning'
    return 'info'
  }

  const getQualificationText = teamEntryId => {
    const qualified = getQualificationStatus(teamEntryId)
    if (!qualified) return ''

    if (qualified.qualification_type === 'group_winner') return '1º'
    if (qualified.qualification_type === 'group_runner_up') return '2º'
    return '3º'
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

/* Responsive */
@media (max-width: 768px) {
  .v-table {
    font-size: 0.875rem;
  }
}
</style>
