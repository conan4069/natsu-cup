<template>
  <v-container fluid>
    <!-- Header -->
    <v-row class="mb-6">
      <v-col cols="12">
        <div class="d-flex align-center mb-4">
          <v-btn
            class="mr-4"
            color="white"
            icon="mdi-arrow-left"
            variant="text"
            @click="goBack"
          />
          <div>
            <h1 class="text-h4 font-weight-bold mb-2 page-title">Nuevo Jugador</h1>
            <p class="text-body-1 page-subtitle">
              Agrega un nuevo jugador al formato
            </p>
          </div>
        </div>
      </v-col>
    </v-row>

    <!-- Formulario -->
    <v-row justify="center">
      <v-col cols="12" lg="6" md="8">
        <v-card rounded="xl">
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
              rounded="xl"
              variant="outlined"
              @click="goBack"
            >
              Cancelar
            </v-btn>
            <v-btn
              color="primary"
              :disabled="!formValid"
              :loading="saving"
              rounded="xl"
              variant="elevated"
              @click="savePlayer"
            >
              <v-icon start>mdi-content-save</v-icon>
              Guardar
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
  import { useAppStore } from '@/stores/app'

  // Router y Store
  const router = useRouter()
  const appStore = useAppStore()

  // Referencias
  const playerFormRef = ref(null)

  // Estado reactivo
  const formValid = ref(false)
  const saving = ref(false)

  // Métodos
  const goBack = () => {
    router.push('/players')
  }

  const handleValidChange = valid => {
    formValid.value = valid
  }

  const savePlayer = async () => {
    if (!formValid.value) return

    saving.value = true
    try {
      const formData = playerFormRef.value.getFormData()
      const response = await playerAPI.createPlayer(formData)

      appStore.showSuccess('Jugador creado exitosamente')
      router.push(`/players/${response.data.id}`)
    } catch (error) {
      const errorInfo = handleApiError(error)
      appStore.showError(`Error al crear jugador: ${errorInfo.message}`)
      console.error('Error al crear jugador:', errorInfo.message)
    } finally {
      saving.value = false
    }
  }
</script>

<style scoped>
.page-title {
  color: white !important;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
}

.page-subtitle {
  color: #f3f2e5 !important;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
}
</style>
