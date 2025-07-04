<template>
  <div class="api-usage-example">
    <v-card class="mb-4">
      <v-card-title>Ejemplo de uso de API</v-card-title>
      <v-card-text>
        <v-btn
          class="mb-3"
          color="primary"
          :loading="loading"
          @click="fetchTournaments"
        >
          Obtener Torneos
        </v-btn>

        <div v-if="tournaments.length > 0">
          <h3>Torneos disponibles:</h3>
          <v-list>
            <v-list-item
              v-for="tournament in tournaments"
              :key="tournament.id"
              class="mb-2"
            >
              <v-list-item-title>{{ tournament.name }}</v-list-item-title>
              <v-list-item-subtitle>{{
                tournament.description
              }}</v-list-item-subtitle>
            </v-list-item>
          </v-list>
        </div>

        <div v-if="error" class="error-message">
          <v-alert :text="error" type="error" />
        </div>
      </v-card-text>
    </v-card>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { handleApiError, tournamentAPI } from '../../../natsu-cup/src/services/api'

const tournaments = ref([])
const loading = ref(false)
const error = ref('')

const fetchTournaments = async () => {
  loading.value = true
  error.value = ''

  try {
    const response = await tournamentAPI.getTournaments()
    tournaments.value = response.data
  } catch (err) {
    const errorInfo = handleApiError(err)
    error.value = errorInfo.message
  } finally {
    loading.value = false
  }
}
</script>

<style lang="scss" scoped>
.api-usage-example {
  @include flex-column;

  .error-message {
    margin-top: $spacing-md;
  }

  // Ejemplo de uso de mixins personalizados
  .custom-button {
    @include button-primary;
    margin-right: $spacing-sm;
  }

  .custom-card {
    @include card-shadow;
    border-radius: $border-radius-lg;
  }
}
</style>
