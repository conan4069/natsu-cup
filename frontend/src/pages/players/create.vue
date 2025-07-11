<template>
  <v-container fluid>
    <!-- Header -->
    <v-row class="mb-6">
      <v-col cols="12">
        <div class="d-flex align-center mb-4">
          <v-btn
            class="mr-4"
            icon="mdi-arrow-left"
            variant="text"
            @click="goBack"
          />
          <div>
            <h1 class="text-h4 font-weight-bold mb-2">Nuevo Jugador</h1>
            <p class="text-body-1 text-grey-darken-1">
              Agrega un nuevo jugador al campeonato Natsu Cup
            </p>
          </div>
        </div>
      </v-col>
    </v-row>

    <!-- Formulario -->
    <v-row justify="center">
      <v-col cols="12" lg="6" md="8">
        <v-card>
          <v-card-title class="text-h6 pa-6 pb-0">
            Información del Jugador
          </v-card-title>

          <v-card-text class="pa-6">
            <PlayerForm
              ref="playerFormRef"
              mode="create"
              @valid-change="handleValidChange"
            />
          </v-card-text>

          <v-card-actions class="pa-6 pt-0">
            <v-spacer />
            <v-btn
              :disabled="saving"
              variant="text"
              @click="goBack"
            >
              Cancelar
            </v-btn>
            <v-btn
              color="primary"
              :disabled="!formValid"
              :loading="saving"
              variant="elevated"
              @click="savePlayer"
            >
              <v-icon start>mdi-content-save</v-icon>
              Guardar Jugador
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
  import { ref } from 'vue'
  import { useRouter } from 'vue-router'
  import PlayerForm from '@/components/PlayerForm.vue'
  import { handleApiError, playerAPI } from '@/services/api'

  // Router
  const router = useRouter()

  // Referencias
  const playerFormRef = ref(null)
  const formValid = ref(false)
  const saving = ref(false)

  // Navegación
  const goBack = () => {
    router.push('/players')
  }

  // Manejar cambios de validación
  const handleValidChange = valid => {
    formValid.value = valid
  }

  // Guardar jugador
  const savePlayer = async () => {
    if (!formValid.value) return

    saving.value = true
    try {
      // Obtener FormData del formulario
      const formData = playerFormRef.value.getFormData()

      // Enviar a la API
      await playerAPI.createPlayer(formData)

      // Redirigir al listado con mensaje de éxito
      router.push({
        path: '/players',
        query: {
          success: 'true',
          message: 'Jugador creado exitosamente',
        },
      })
    } catch (error) {
      const errorInfo = handleApiError(error)
      console.error('Error al crear jugador:', errorInfo.message)

    // Aquí podrías mostrar una notificación de error
    // Por ejemplo, usando un snackbar o toast
    } finally {
      saving.value = false
    }
  }
</script>

<style scoped>
/* Estilos específicos si son necesarios */
</style>
