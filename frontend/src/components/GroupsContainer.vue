<template>
  <v-container fluid>
    <!-- Loading state -->
    <GroupsLoading v-if="loading" />

    <!-- Error state -->
    <GroupsError
      v-else-if="error"
      :error="error"
      @retry="$emit('retry')"
    />

    <!-- Tournament groups -->
    <div v-else-if="tournament">
      <!-- Header -->
      <GroupsHeader
        :tournament="tournament"
        @go-back="$emit('go-back')"
      />

      <!-- Equipos Clasificados -->
      <v-row v-if="qualifiedTeams.total_qualified > 0" class="mb-6">
        <v-col cols="12">
          <QualifiedTeams
            :qualified-teams="qualifiedTeams"
            :can-generate-knockout="canGenerateKnockout"
            :generating-knockout="generatingKnockout"
            @generate-knockout="$emit('generate-knockout')"
          />
        </v-col>
      </v-row>

      <!-- Tournament info -->
      <v-row>
        <v-col cols="12" md="8">
          <v-card>
            <v-card-title class="text-h6">
              <v-icon start>mdi-information</v-icon>
              Información de Grupos
            </v-card-title>
            <v-card-text>
              <!-- Mostrar grupos si están generados -->
              <div v-if="groups.length > 0">
                <GroupCard
                  v-for="group in groups"
                  :key="group.code"
                  :group="group"
                  :qualified-teams="qualifiedTeams"
                  @edit-match="$emit('edit-match', $event)"
                />
              </div>

              <!-- Mostrar botón de configuración si no hay grupos -->
              <GroupsEmptyState
                v-else
                :generating="generating"
                @configure-groups="$emit('configure-groups')"
              />
            </v-card-text>
          </v-card>
        </v-col>

        <v-col cols="12" md="4">
          <TournamentStats
            :stats="tournamentStats"
            :tournament="tournament"
          />
        </v-col>
      </v-row>
    </div>
  </v-container>
</template>

<script setup>
  import GroupsLoading from './GroupsLoading.vue'
  import GroupsError from './GroupsError.vue'
  import GroupsHeader from './GroupsHeader.vue'
  import GroupsEmptyState from './GroupsEmptyState.vue'
  import GroupCard from './GroupCard.vue'
  import QualifiedTeams from './QualifiedTeams.vue'
  import TournamentStats from './TournamentStats.vue'

  // Props
  const props = defineProps({
    loading: {
      type: Boolean,
      default: false,
    },
    error: {
      type: String,
      default: null,
    },
    tournament: {
      type: Object,
      default: null,
    },
    groups: {
      type: Array,
      default: () => [],
    },
    qualifiedTeams: {
      type: Object,
      default: () => ({
        group_winners: [],
        group_runners_up: [],
        best_third_place: [],
        total_qualified: 0,
      }),
    },
    tournamentStats: {
      type: Object,
      default: () => ({
        groupsCount: 0,
        teamsPerGroup: 0,
        matchesPlayed: 0,
        totalMatches: 0,
        progressPercentage: 0,
        qualifiedTeams: 0,
      }),
    },
    generating: {
      type: Boolean,
      default: false,
    },
    generatingKnockout: {
      type: Boolean,
      default: false,
    },
    canGenerateKnockout: {
      type: Boolean,
      default: false,
    },
  })

  // Emits
  const emit = defineEmits([
    'retry',
    'go-back',
    'configure-groups',
    'edit-match',
    'generate-knockout',
  ])
</script>
