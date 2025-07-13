<template>
  <v-container fluid>
    <!-- Loading state -->
    <div v-if="loading" class="d-flex justify-center align-center" style="min-height: 400px;">
      <v-progress-circular color="primary" indeterminate size="64" />
    </div>

    <!-- Error state -->
    <div v-else-if="error" class="text-center py-8">
      <v-icon class="mb-4" color="error" size="64">mdi-alert-circle</v-icon>
      <h3 class="text-h6 text-grey-darken-1 mb-2">Error al cargar jugador</h3>
      <p class="text-body-2 text-grey-darken-1 mb-4">{{ error }}</p>
      <v-btn color="primary" rounded="xl" @click="loadPlayer">Reintentar</v-btn>
    </div>

    <!-- Edit form -->
    <div v-else-if="player">
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
              <h1 class="text-h4 text-white mb-2 page-title">Editar Jugador</h1>
              <p class="text-body-1 text-white page-subtitle">
                Modifica la información de {{ player.display_name }}
              </p>
            </div>
          </div>
        </v-col>
      </v-row>

      <!-- Formulario -->
      <v-row justify="center">
        <v-col cols="12" lg="6" md="8" >
          <v-card rounded="xl">
            <v-card-title class="text-h6 pa-6 pb-0">
              <v-icon start>mdi-account-edit</v-icon>
              Información del Jugador
            </v-card-title>
            <v-card-text class="pa-6">
              <PlayerForm
                ref="playerFormRef"
                mode="edit"
                :player="player"
                @valid-change="onValidChange"
              />
            </v-card-text>
            <v-card-actions class="pa-6 pt-0">
              <v-spacer />
              <v-btn
                color="black"
                rounded="xl"
                variant="outlined"
                @click="goBack"
              >
                Cancelar
              </v-btn>
              <v-btn
                color="primary"
                :disabled="!isValid"
                :loading="saving"
                prepend-icon="mdi-content-save"
                rounded="xl"
                variant="elevated"
                @click="savePlayer"
              >
                Guardar
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
    </div>
  </v-container>
</template>

<script setup>
  import { onMounted, ref } from 'vue'
  import { useRoute, useRouter } from 'vue-router'
  import PlayerForm from '@/components/PlayerForm.vue'
  import { handleApiError, playerAPI } from '@/services/api'

  // Router y Route
  const router = useRouter()
  const route = useRoute()

  // Estado reactivo
  const player = ref(null)
  const loading = ref(true)
  const error = ref(null)
  const saving = ref(false)
  const isValid = ref(false)
  const playerFormRef = ref(null)

  // Cargar jugador
  const loadPlayer = async () => {
    const playerId = route.params.id

    loading.value = true
    error.value = null

    try {
      console.log('Cargando jugador con ID:', playerId)

      // Cargar datos del jugador
      const playerResponse = await playerAPI.getPlayer(playerId)
      player.value = playerResponse.data
      console.log('Datos del jugador cargados:', player.value)
    } catch (error_) {
      const errorInfo = handleApiError(error_)
      error.value = errorInfo.message
      console.error('Error al cargar jugador:', errorInfo.message)
    } finally {
      loading.value = false
    }
  }

  // Guardar jugador
  const savePlayer = async () => {
    if (!isValid.value || !playerFormRef.value) return

    saving.value = true
    try {
      // Validar formulario
      const isValidForm = await playerFormRef.value.validate()
      if (!isValidForm) {
        console.error('Formulario inválido')
        return
      }

      // Obtener datos del formulario
      const formData = playerFormRef.value.getFormData()

      // Actualizar jugador
      await playerAPI.updatePlayer(player.value.id, formData)

      console.log('Jugador actualizado exitosamente')

      // Redirigir a la vista del jugador
      router.push(`/players/${player.value.id}`)
    } catch (error_) {
      const errorInfo = handleApiError(error_)
      console.error('Error al actualizar jugador:', errorInfo.message)
      // Aquí podrías mostrar un mensaje de error al usuario
    } finally {
      saving.value = false
    }
  }

  // Callback para cambios de validación
  const onValidChange = valid => {
    isValid.value = valid
  }

  // Navegación
  const goBack = () => {
    router.push(`/players/${route.params.id}`)
  }

  // Cargar datos al montar el componente
  onMounted(() => {
    loadPlayer()
  })
</script>

<style scoped>
/* Estilos específicos si son necesarios */
</style>
