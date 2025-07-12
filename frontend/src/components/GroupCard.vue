<template>
  <div class="mb-6">
    <h4 class="text-h6 mb-3">Grupo {{ group.code }}</h4>

    <!-- Clasificación del grupo -->
    <GroupStandings
      :standings="group.standings"
      :qualified-teams="qualifiedTeams"
    />

    <!-- Equipos del grupo -->
    <v-card class="mb-4" variant="outlined">
      <v-card-title class="text-subtitle-1">
        <v-icon start>mdi-account-group</v-icon>
        Equipos del Grupo
      </v-card-title>
      <v-card-text>
        <div class="teams-grid">
          <div
            v-for="team in getGroupTeams()"
            :key="team.id"
            class="team-card"
          >
            <div class="team-header">
              <v-avatar class="mr-3" size="48">
                <v-img
                  v-if="team.assigned_team?.logo"
                  :src="team.assigned_team.logo"
                  alt="Logo equipo"
                />
                <v-icon v-else size="24">mdi-shield</v-icon>
              </v-avatar>
              <div class="team-info">
                <div class="team-name">
                  {{ team.assigned_team?.name || team.team_name || `Equipo ${team.id}` }}
                </div>
                <div class="team-participants">
                  <v-chip
                    v-for="player in team.players || []"
                    :key="player.id"
                    class="ma-1"
                    color="primary"
                    label
                    size="small"
                    variant="outlined"
                  >
                    <v-avatar v-if="player.avatar" left size="20">
                      <v-img :src="player.avatar" />
                    </v-avatar>
                    {{ player.display_name }}
                  </v-chip>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Group matches -->
        <GroupMatches
          :matches="group.matches"
          :group-code="group.code"
          @edit-match="$emit('edit-match', $event)"
        />
      </v-card-text>
    </v-card>
  </div>
</template>

<script setup>
  import GroupStandings from './GroupStandings.vue'
  import GroupMatches from './GroupMatches.vue'

  // Props
  const props = defineProps({
    group: {
      type: Object,
      required: true,
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

  // Emits
  const emit = defineEmits(['edit-match'])

  // Método para obtener la información completa de los equipos del grupo
  function getGroupTeams() {
    // Si el grupo ya trae los equipos completos (con assigned_team y players), los usamos
    if (props.group.teams && props.group.teams.length && props.group.teams[0].assigned_team) {
      return props.group.teams
    }
    // Si no, los buscamos a partir de los participantes de los partidos
    const teamsMap = {}
    for (const match of props.group.matches || []) {
      for (const participant of match.participants || []) {
        teamsMap[participant.id] = participant
      }
    }
    return Object.values(teamsMap)
  }
</script>

<style scoped>
.teams-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
}
.team-card {
  display: flex;
  align-items: center;
  background: #f8f9fa;
  border-radius: 16px;
  padding: 12px 20px;
  min-width: 220px;
  max-width: 320px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}
.team-header {
  display: flex;
  align-items: center;
}
.team-info {
  flex: 1;
}
.team-name {
  font-weight: 500;
  margin-bottom: 4px;
}
.team-participants {
  margin-top: 4px;
}
</style>
