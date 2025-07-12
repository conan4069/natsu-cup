<template>
  <!-- Barra de navegación -->
  <template v-if="!isFullScreenRoute">
    <v-app-bar app color="white" dark elevation="2">
      <template #prepend>
        <v-app-bar-nav-icon v-if="mobile" @click="drawer = !drawer" />
      </template>
      <v-app-bar-title class="d-flex justify-center align-center">
        <!-- <v-icon class="mr-2">mdi-trophy</v-icon>
        Natsu Cup -->
        <v-avatar size="54">
          <v-img :src="LogoCup" width="150" height="150" class="mr-2" style="border-radius: 50%;" />
        </v-avatar>
        <span class="text-h5 font-weight-bold">Natsu Cup</span>
      </v-app-bar-title>
    </v-app-bar>
  </template>
  <n-navigation v-model="drawer" />

  <!-- Contenido principal -->
  <v-main>
    <v-parallax src="@/assets/fondocesped.jpg">
      <v-container class="pa-0" fluid>
      <!-- Slot para el contenido de las rutas -->
      <router-view />
      </v-container>
    </v-parallax>
    
    <!-- Footer (opcional) -->
  </v-main>
  <v-footer class="py-1" color="#f3f2e5">
    <v-row align="center" justify="center">
      <v-col class="text-center" cols="12">
        <span class="text-caption text-grey-darken-3">
          © 2025 Natsu Cup. Todos los derechos reservados.
        </span>
      </v-col>
    </v-row>
  </v-footer>
</template>

<script setup>
  import { useRoute } from 'vue-router'
  import { useDisplay } from 'vuetify'
  import LogoCup from '@/assets/LogoCup.png'
  const { mobile } = useDisplay()
  const drawer = ref(true)
  const route = useRoute()

  // Lista de rutas donde solo quieres mostrar el router-view
  const fullScreenRoutes = new Set(['/'])

  const isFullScreenRoute = computed(() => fullScreenRoutes.has(route.path))

  watch(
    mobile,
    newVal => {
      drawer.value = !newVal
    },
    { immediate: true },
  )
</script>
