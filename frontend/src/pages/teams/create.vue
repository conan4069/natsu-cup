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
            <h1 class="text-h4 font-weight-bold mb-2">Nuevo Equipo</h1>
            <p class="text-body-1 text-grey-darken-1">
              Agrega un nuevo equipo al formato de la Natsu Cup
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
            Información del equipo
          </v-card-title>

          <v-card-text class="pa-6">
            <TeamForm
              ref="teamFormRef"
              mode="create"
              @valid-change="handleValidChange"
            />
          </v-card-text>

          <v-card-actions class="pa-6 pt-0">
            <v-spacer />
            <v-btn
              :disabled="saving"
              variant="outlined"
              rounded="xl"
              @click="goBack"
            >
              Cancelar
            </v-btn>
            <v-btn
              color="primary"
              :disabled="!formValid"
              :loading="saving"
              variant="elevated"
              rounded="xl"
              @click="createTeam"
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
  import TeamForm from '@/components/TeamForm.vue'
  import { handleApiError, teamAPI } from '@/services/api'

  // Router
  const router = useRouter()

  // Referencias
  const teamFormRef = ref(null)
  const formValid = ref(false)
  const saving = ref(false)

  // Navegación
  const goBack = () => {
    router.push('/teams')
  }

  // Manejar cambios de validación
  const handleValidChange = valid => {
    formValid.value = valid
  }

  // Crear equipo
  const createTeam = async () => {
    if (!teamFormRef.value) return

    saving.value = true
    try {
      const formData = teamFormRef.value.getFormData()
      await teamAPI.createTeam(formData)
      router.push('/teams')
    } catch (error) {
      const errorInfo = handleApiError(error)
      console.error('Error al crear equipo:', errorInfo.message)
    } finally {
      saving.value = false
    }
  }
</script>

<style scoped>
/* Estilos específicos si son necesarios */
</style>
