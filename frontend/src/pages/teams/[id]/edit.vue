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
      <v-btn color="primary" rounded="xl" @click="loadTeam">Reintentar</v-btn>
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
              <h1 class="text-h4 font-weight-bold mb-2 page-title">Editar Equipo</h1>
              <p class="text-body-1 page-subtitle">
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
              <v-icon start>mdi-shield-edit</v-icon>
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
                prepend-icon="mdi-content-save"
                rounded="xl"
                variant="elevated"
                @click="saveTeam"
              >
                Guardar Cambios
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
  import TeamForm from '@/components/TeamForm.vue'
  import { handleApiError, teamAPI } from '@/services/api'
  import { useAppStore } from '@/stores/app'

  // Router y Route
  const router = useRouter()
  const route = useRoute()
  const appStore = useAppStore()

  // Referencias
  const teamFormRef = ref(null)

  // Estado reactivo
  const loading = ref(true)
  const saving = ref(false)
  const formValid = ref(false)
  const error = ref(null)
  const team = ref(null)

  // Cargar equipo
  const loadTeam = async () => {
    const teamId = route.params.id

    loading.value = true
    error.value = null

    try {
      console.log('Cargando equipo con ID:', teamId)
      const response = await teamAPI.getTeam(teamId)
      team.value = response.data
      console.log('Datos del equipo cargados:', team.value)
    } catch (error_) {
      const errorInfo = handleApiError(error_)
      error.value = errorInfo.message
      appStore.showError(`Error al cargar equipo: ${errorInfo.message}`)
      console.error('Error al cargar equipo:', errorInfo.message)
    } finally {
      loading.value = false
    }
  }

  // Navegación
  const goBack = () => {
    router.push(`/teams/${route.params.id}`)
  }

  const handleValidChange = valid => {
    formValid.value = valid
  }

  const saveTeam = async () => {
    if (!formValid.value || !teamFormRef.value) return

    saving.value = true
    try {
      // Validar formulario
      const isValidForm = await teamFormRef.value.validate()
      if (!isValidForm) {
        console.error('Formulario inválido')
        return
      }

      // Obtener datos del formulario
      const formData = teamFormRef.value.getFormData()

      // Actualizar equipo
      await teamAPI.updateTeam(team.value.id, formData)

      appStore.showSuccess('Equipo actualizado exitosamente')
      console.log('Equipo actualizado exitosamente')

      // Redirigir a la vista del equipo
      router.push(`/teams/${team.value.id}`)
    } catch (error_) {
      const errorInfo = handleApiError(error_)
      appStore.showError(`Error al actualizar equipo: ${errorInfo.message}`)
      console.error('Error al actualizar equipo:', errorInfo.message)
    } finally {
      saving.value = false
    }
  }

  // Cargar datos al montar
  onMounted(() => {
    loadTeam()
  })
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
