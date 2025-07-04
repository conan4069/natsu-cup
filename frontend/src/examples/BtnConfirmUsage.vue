<template>
  <div class="btn-confirm-usage">
    <v-card class="mb-4">
      <v-card-title>Ejemplo de uso de btnConfirm</v-card-title>
      <v-card-text>
        <p class="mb-3">Tournament ID: {{ tournamentId }}</p>

        <!-- Uso básico del componente -->
        <btnConfirm
          :tournament-id="tournamentId"
          @error="handleError"
          @success="handleSuccess"
        />

        <!-- Uso con callback personalizado -->
        <btnConfirm
          class="mt-3"
          :on-success="customSuccessCallback"
          :tournament-id="tournamentId"
          @error="handleError"
          @success="handleSuccess"
        />
      </v-card-text>
    </v-card>

    <!-- Mostrar resultados -->
    <v-card v-if="result" class="mb-4">
      <v-card-title>Resultado</v-card-title>
      <v-card-text>
        <pre>{{ JSON.stringify(result, null, 2) }}</pre>
      </v-card-text>
    </v-card>

    <!-- Mostrar errores -->
    <v-alert v-if="error" class="mb-4" :text="error.message" type="error" />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import btnConfirm from '@/components/btnConfirm/btnConfirm.vue'

const tournamentId = ref(1) // Ejemplo de ID de torneo
const result = ref(null)
const error = ref(null)

// Manejador de éxito
const handleSuccess = data => {
  result.value = data
  error.value = null
  console.log('Éxito:', data)
}

// Manejador de error
const handleError = errorInfo => {
  error.value = errorInfo
  result.value = null
  console.error('Error:', errorInfo)
}

// Callback personalizado de éxito
const customSuccessCallback = async data => {
  console.log('Callback personalizado ejecutado:', data)
  // Aquí puedes hacer cualquier lógica adicional
  // Por ejemplo, actualizar el estado del componente padre
  // o hacer otra llamada a la API
}
</script>

<style lang="scss" scoped>
.btn-confirm-usage {
  @include flex-column;

  pre {
    background-color: #f5f5f5;
    padding: $spacing-md;
    border-radius: $border-radius-sm;
    font-size: $font-size-sm;
    overflow-x: auto;
  }
}
</style>
