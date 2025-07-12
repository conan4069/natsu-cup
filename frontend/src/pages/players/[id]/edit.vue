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
      <v-btn color="primary" @click="loadPlayer">Reintentar</v-btn>
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
              <h1 class="text-h4 font-weight-bold mb-2" style="color: #f3f2e5;">Editar Jugador</h1>
              <p class="text-body-1" style="color: #deddd6;">
                Modifica la información de {{ player.display_name }}
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
                mode="edit"
                :player="player"
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
                class="mr-2"
                color="error"
                :loading="deleting"
                rounded="xl"
                variant="outlined"
                @click="confirmDelete"
              >
                <v-icon start>mdi-delete</v-icon>
                Eliminar
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
    </div>

    <!-- Diálogo de confirmación de eliminación -->
    <v-dialog v-model="deleteDialog" max-width="400">
      <v-card>
        <v-card-title class="text-h6">
          Confirmar eliminación
        </v-card-title>
        <v-card-text>
          ¿Estás seguro de que quieres eliminar al jugador
          <strong>{{ player?.display_name }}</strong>?
          Esta acción no se puede deshacer.
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn
            variant="text"
            @click="deleteDialog = false"
          >
            Cancelar
          </v-btn>
          <v-btn
            color="error"
            :loading="deleting"
            variant="elevated"
            @click="deletePlayer"
          >
            Eliminar
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
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

  // Referencias
  const playerFormRef = ref(null)
  const formValid = ref(false)

  // Estado reactivo
  const player = ref(null)
  const loading = ref(true)
  const saving = ref(false)
  const deleting = ref(false)
  const error = ref(null)
  const deleteDialog = ref(false)

  // Cargar jugador
  const loadPlayer = async () => {
    const playerId = route.params.id

    loading.value = true
    error.value = null

    try {
      const response = await playerAPI.getPlayer(playerId)
      player.value = response.data
    } catch (error_) {
      const errorInfo = handleApiError(error_)
      error.value = errorInfo.message
      console.error('Error al cargar jugador:', errorInfo.message)
    } finally {
      loading.value = false
    }
  }

  // Manejar cambios de validación
  const handleValidChange = valid => {
    formValid.value = valid
  }

  // Navegación
  const goBack = () => {
    router.push(`/players/${player.value.id}`)
  }

  // Guardar cambios
  const savePlayer = async () => {
    if (!formValid.value) return

    saving.value = true
    try {
      const playerId = route.params.id

      // Obtener FormData del formulario
      const formData = playerFormRef.value.getFormData()

      // Enviar a la API
      await playerAPI.updatePlayer(playerId, formData)

      // Redirigir al detalle del jugador
      router.push({
        path: `/players/${playerId}`,
        query: {
          success: 'true',
          message: 'Jugador actualizado exitosamente',
        },
      })
    } catch (error) {
      const errorInfo = handleApiError(error)
      console.error('Error al actualizar jugador:', errorInfo.message)
    // Aquí podrías mostrar una notificación de error
    } finally {
      saving.value = false
    }
  }

  // Eliminación
  const confirmDelete = () => {
    deleteDialog.value = true
  }

  const deletePlayer = async () => {
    if (!player.value) return

    deleting.value = true
    try {
      await playerAPI.deletePlayer(player.value.id)

      deleteDialog.value = false

      // Redirigir al listado
      router.push({
        path: '/players',
        query: {
          success: 'true',
          message: 'Jugador eliminado exitosamente',
        },
      })
    } catch (error) {
      const errorInfo = handleApiError(error)
      console.error('Error al eliminar jugador:', errorInfo.message)
    // Aquí podrías mostrar una notificación de error
    } finally {
      deleting.value = false
    }
  }

  // Cargar datos al montar el componente
  onMounted(() => {
    loadPlayer()
  })
</script>

<style scoped>
/* Estilos específicos si son necesarios */
</style>
