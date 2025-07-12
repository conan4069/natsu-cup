<template>
  <v-container fluid>
    <!-- Loading state -->
    <div v-if="loading" class="d-flex justify-center align-center" style="min-height: 400px;">
      <v-progress-circular color="primary" indeterminate size="64" />
    </div>

    <!-- Error state -->
    <div v-else-if="error" class="text-center py-8">
      <v-icon class="mb-4" color="error" size="64">mdi-alert-circle</v-icon>
      <h3 class="text-h6 text-grey-darken-1 mb-2">Error al cargar equipo</h3>
      <p class="text-body-2 text-grey-darken-1 mb-4">{{ error }}</p>
      <v-btn color="primary" @click="loadTeam">Reintentar</v-btn>
    </div>

    <!-- Edit form -->
    <div v-else-if="team">
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
              <h1 class="text-h4 font-weight-bold mb-2">Editar Equipo</h1>
              <p class="text-body-1 text-grey-darken-1">
                Modifica la información de {{ team.name }}
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
              Información del Equipo
            </v-card-title>

            <v-card-text class="pa-6">
              <TeamForm
                ref="teamFormRef"
                mode="edit"
                :team="team"
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
                variant="elevated"
                @click="saveTeam"
              >
                <v-icon start>mdi-content-save</v-icon>
                Guardar Cambios
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
          ¿Estás seguro de que quieres eliminar al equipo
          <strong>{{ team?.name }}</strong>?
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
            @click="deleteTeam"
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
  import TeamForm from '@/components/TeamForm.vue'
  import { handleApiError, teamAPI } from '@/services/api'

  // Router y Route
  const router = useRouter()
  const route = useRoute()

  // Referencias
  const teamFormRef = ref(null)
  const formValid = ref(false)

  // Estado reactivo
  const team = ref(null)
  const loading = ref(true)
  const saving = ref(false)
  const deleting = ref(false)
  const error = ref(null)
  const deleteDialog = ref(false)

  // Cargar equipo
  const loadTeam = async () => {
    const teamId = route.params.id

    loading.value = true
    error.value = null

    try {
      const response = await teamAPI.getTeam(teamId)
      team.value = response.data
    } catch (error_) {
      const errorInfo = handleApiError(error_)
      error.value = errorInfo.message
      console.error('Error al cargar equipo:', errorInfo.message)
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
    router.push(`/teams/${team.value.id}`)
  }

  // Guardar cambios
  const saveTeam = async () => {
    if (!formValid.value) return

    saving.value = true
    try {
      const teamId = route.params.id

      // Obtener FormData del formulario
      const formData = teamFormRef.value.getFormData()

      // Enviar a la API
      await teamAPI.updateTeam(teamId, formData)

      // Redirigir al detalle del equipo
      router.push({
        path: `/teams/${teamId}`,
        query: {
          success: 'true',
          message: 'Equipo actualizado exitosamente',
        },
      })
    } catch (error) {
      const errorInfo = handleApiError(error)
      console.error('Error al actualizar equipo:', errorInfo.message)
    // Aquí podrías mostrar una notificación de error
    } finally {
      saving.value = false
    }
  }

  // Eliminación
  const confirmDelete = () => {
    deleteDialog.value = true
  }

  const deleteTeam = async () => {
    if (!team.value) return

    deleting.value = true
    try {
      await teamAPI.deleteTeam(team.value.id)

      deleteDialog.value = false

      // Redirigir al listado
      router.push({
        path: '/teams',
        query: {
          success: 'true',
          message: 'Equipo eliminado exitosamente',
        },
      })
    } catch (error) {
      const errorInfo = handleApiError(error)
      console.error('Error al eliminar equipo:', errorInfo.message)
    // Aquí podrías mostrar una notificación de error
    } finally {
      deleting.value = false
    }
  }

  // Cargar datos al montar el componente
  onMounted(() => {
    loadTeam()
  })
</script>

<style scoped>
/* Estilos específicos si son necesarios */
</style>
