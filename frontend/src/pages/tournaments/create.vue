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
            <h1 class="text-h4 font-weight-bold mb-2">Nuevo Torneo</h1>
            <p class="text-body-1 text-grey-darken-1">
              Crea un nuevo torneo para la Natsu Cup
            </p>
          </div>
        </div>
      </v-col>
    </v-row>

    <!-- Formulario del torneo -->
    <v-card class="mb-6">
      <v-card-title class="text-h6 pa-6 pb-0">
        Información del torneo
      </v-card-title>
      <v-card-text class="pa-6">
        <TournamentForm
          ref="tournamentFormRef"
          mode="create"
          @valid-change="handleTournamentValidChange"
        />
      </v-card-text>
    </v-card>

    <!-- Botón de crear torneo -->
    <v-row class="mt-6">
      <v-col class="d-flex justify-end" cols="12">
        <v-btn
          color="success"
          :disabled="!canCreateTournament"
          :loading="creating"
          rounded="xl"
          size="large"
          variant="elevated"
          @click="createTournament"
        >
          <v-icon start>mdi-check</v-icon>
          Crear torneo
        </v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
  import { computed, ref } from 'vue'
  import { useRouter } from 'vue-router'
  import TournamentForm from '@/components/TournamentForm.vue'
  import { handleApiError, tournamentAPI } from '@/services/api'
  import { useAppStore } from '@/stores/app'

  // Router
  const router = useRouter()
  const appStore = useAppStore()

  // Referencias
  const tournamentFormRef = ref(null)

  // Estado reactivo
  const tournamentValid = ref(false)
  const creating = ref(false)

  // Datos del torneo
  const tournamentData = ref({
    name: '',
    format: '1v1',
    rules: '',
  })

  // Computed
  const canCreateTournament = computed(() => {
    return tournamentValid.value
  })

  // Métodos
  const goBack = () => {
    router.push('/tournaments')
  }

  const handleTournamentValidChange = valid => {
    tournamentValid.value = valid
    if (valid && tournamentFormRef.value) {
      tournamentData.value = tournamentFormRef.value.getFormData()
    }
  }

  const createTournament = async () => {
    creating.value = true
    try {
      // Crear el torneo
      const tournamentResponse = await tournamentAPI.createTournament(tournamentData.value)
      const tournamentId = tournamentResponse.data.id

      appStore.showSuccess('Torneo creado exitosamente')

      // Redirigir a la página de edición del torneo creado
      router.push(`/tournaments/${tournamentId}/edit`)
    } catch (error) {
      const errorInfo = handleApiError(error)
      appStore.showError(`Error al crear torneo: ${errorInfo.message}`)
      console.error('Error al crear torneo:', errorInfo.message)
    } finally {
      creating.value = false
    }
  }
</script>

<style scoped>
/* Estilos específicos si son necesarios */
</style>
