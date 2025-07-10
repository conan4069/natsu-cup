<template>
    <!-- Navegación principal -->
    <v-btn
      v-for="(btn, index) in btns"
      :key="index"
      :active="isActiveRoute('/')"
      class="mx-1"
      :to="btn.path"
      variant="outlined"
    >
      <v-icon class="mr-2" left>{{ btn.icon }}</v-icon> 
      {{ btn.name }}
    </v-btn>
</template>
<script setup>
 import { useRoute } from 'vue-router'

const route = useRoute()
const btns = ref([
  {
    name: 'Inicio',
    icon: 'mdi-home',
    path: '/'
  },
  {
    name: 'Torneos',
    icon: 'mdi-trophy-outline',
    path: '/tournaments'
  },
  {
    name: 'Brackets',
    icon: 'mdi-tournament',
    path: '/brackets'
  }
])

// Computed para verificar si una ruta está activa
const isActiveRoute = path => {
  return route.path === path
}

</script>