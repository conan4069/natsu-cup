<template>
  <v-row class="mb-6">
    <v-col cols="12">
      <div class="d-flex align-center mb-4">
        <v-btn
          class="mr-4"
          icon="mdi-arrow-left"
          variant="text"
          @click="$emit('go-back')"
        />
        <div>
          <h1 class="text-h4 font-weight-bold mb-2 page-title">{{ tournament.name }}</h1>
          <p class="text-body-1 page-subtitle">
            Fase de Grupos - {{ tournament.format }}
          </p>
        </div>
      </div>
    </v-col>
  </v-row>
</template>

<script setup>
  // Props
  const props = defineProps({
    tournament: {
      type: Object,
      required: true,
    },
  })

  // Emits
  const emit = defineEmits(['go-back'])
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
