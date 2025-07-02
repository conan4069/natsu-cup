<template>
  <v-btn
    color="success"
    :loading="loading"
    @click="confirmBracket"
    prepend-icon="mdi-check-bold"
  >
    Confirmar llave de cuartos
  </v-btn>

</template>
<script setup>
const loading = ref(false)

async function confirmBracket() {
  loading.value = true
  try {
    const res = await fetch(`/api/tournaments/${tournamentId}/complete-knockout-stage/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        total_slots: 8,
        next_stage: 'quarterfinal'
      })
    })

    const result = await res.json()
    if (!res.ok) throw new Error(result.error || 'Error al generar llave')

    // ¡Re-renderizar vista!
    await fetchPreview()
    toast.success('¡Llave de cuartos generada con éxito!')
  } catch (err) {
    toast.error(err.message)
  } finally {
    loading.value = false
  }
}

</script>
