<template>
  <v-btn
    color="success"
    :loading="loading"
    prepend-icon="mdi-check-bold"
    @click="confirmBracket"
  >
    Confirmar llave de cuartos
  </v-btn>
</template>

<script setup>
  import { ref } from 'vue'
  import { handleApiError, tournamentAPI } from '../../../../natsu-cup/src/services/api'

  // Props
  const props = defineProps({
    tournamentId: {
      type: [String, Number],
      required: true,
    },
    onSuccess: {
      type: Function,
      default: null,
    },
  })

  // Emits
  const emit = defineEmits(['success', 'error'])

  const loading = ref(false)

  async function confirmBracket () {
    loading.value = true

    try {
      // Usar la función unificada knockoutStage
      const response = await tournamentAPI.knockoutStage(
        props.tournamentId,
        {
          stage: 'quarterfinal',
        },
      )

      // Emitir evento de éxito
      emit('success', response.data)

      // Llamar callback de éxito si existe
      if (props.onSuccess) {
        await props.onSuccess(response.data)
      }

      // Mostrar mensaje de éxito (puedes usar un toast aquí)
      console.log('¡Llave de cuartos generada con éxito!')
    } catch (error) {
      const errorInfo = handleApiError(error)
      console.error('Error:', errorInfo.message)

      // Emitir evento de error
      emit('error', errorInfo)

      // Mostrar mensaje de error (puedes usar un toast aquí)
      console.error(errorInfo.message)
    } finally {
      loading.value = false
    }
  }
</script>
