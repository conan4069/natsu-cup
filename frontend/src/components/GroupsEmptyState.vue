<template>
  <div class="text-center py-8">
    <v-icon class="mb-4" color="primary" size="64">mdi-account-group</v-icon>
    <h3 class="text-h5 mb-2">Fase de Grupos</h3>
    <p class="text-body-1 text-grey-darken-1 mb-4">
      Aquí se mostrarán los grupos del torneo cuando estén configurados
    </p>
    <v-btn
      color="primary"
      :loading="generating"
      prepend-icon="mdi-account-group"
      rounded="xl"
      variant="elevated"
      @click="$emit('configure-groups')"
    >
      {{ generating ? 'Generando Grupos...' : 'Configurar Grupos' }}
    </v-btn>
  </div>
</template>

<script setup>
  // Props
  const props = defineProps({
    generating: {
      type: Boolean,
      default: false,
    },
  })

  // Emits
  const emit = defineEmits(['configure-groups'])
</script>
