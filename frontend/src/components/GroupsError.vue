<template>
  <div class="text-center py-8">
    <v-icon class="mb-4" color="error" size="64">mdi-alert-circle</v-icon>
    <h3 class="text-h6 text-grey-darken-1 mb-2">Error al cargar torneo</h3>
    <p class="text-body-2 text-grey-darken-1 mb-4">{{ error }}</p>
    <v-btn color="primary" rounded="xl" @click="$emit('retry')">
      Reintentar
    </v-btn>
  </div>
</template>

<script setup>
  // Props
  const props = defineProps({
    error: {
      type: String,
      required: true,
    },
  })

  // Emits
  const emit = defineEmits(['retry'])
</script>
