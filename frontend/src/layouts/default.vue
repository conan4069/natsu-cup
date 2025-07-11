<template>
  <!-- Barra de navegación -->
  <template v-if="!isFullScreenRoute">
    <v-app-bar app color="primary" dark elevation="2">
      <template #prepend>
        <v-app-bar-nav-icon v-if="mobile" @click="drawer = !drawer" />
      </template>
      <v-app-bar-title class="d-flex align-center">
        <v-icon class="mr-2">mdi-trophy</v-icon>
        Natsu Cup
      </v-app-bar-title>

      <v-spacer />
    </v-app-bar>
    <n-navigation v-model="drawer" />
  </template>

  <!-- Contenido principal -->
  <v-main>
    <v-container class="pa-0" fluid>
      <!-- Slot para el contenido de las rutas -->
      <router-view />
    </v-container>
    <!-- Footer (opcional) -->
  </v-main>
  <v-footer app class="py-3" color="grey-lighten-3">
    <v-row align="center" justify="center">
      <v-col class="text-center" cols="12">
        <span class="text-caption text-grey-darken-1">
          © 2025 Natsu Cup. Todos los derechos reservados.
        </span>
      </v-col>
    </v-row>
  </v-footer>
</template>

<script setup>
  import { useRoute } from 'vue-router'
  import { useDisplay } from 'vuetify'

  const { mobile } = useDisplay()
  const drawer = ref(true)
  const route = useRoute()

  // Lista de rutas donde solo quieres mostrar el router-view
  const fullScreenRoutes = new Set(['/auth/login', '/auth/register', '/auth/forgot'])

  const isFullScreenRoute = computed(() => fullScreenRoutes.has(route.path))

  watch(
    mobile,
    newVal => {
      drawer.value = !newVal
    },
    { immediate: true },
  )
</script>
