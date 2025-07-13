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
          <v-img
            class="mr-2"
            height="150"
            :src="LogoCup"
            style="border-radius: 50%;"
            width="150"
          />
        </v-avatar>
        <span class="text-h5 font-weight-bold">Natsu Cup</span>
      </v-app-bar-title>
    </v-app-bar>
  </template>
  <n-navigation v-model="drawer" />

  <!-- Contenido principal -->
  <v-main>
    <template v-if="!isHome">
      <v-parallax class="champions-parallax" src="@/assets/Champions.jpg">
        <v-container class="pa-0" fluid>
          <router-view />
        </v-container>
      </v-parallax>
    </template>
    <template v-else>
      <v-container class="pa-0" fluid>
        <router-view />
      </v-container>
    </template>
  </v-main>
  <v-footer class="py-1" color="white">
    <v-row align="center" justify="center">
      <v-col class="text-center" cols="12">
        <span class="text-caption text-black">
          © 2025 Natsu Cup. Todos los derechos reservados.
        </span>
      </v-col>
    </v-row>
  </v-footer>
</template>

<script setup>
  import { computed, ref } from 'vue'
  import { useRoute } from 'vue-router'
  import { useDisplay } from 'vuetify'
  import LogoCup from '@/assets/LogoCup.png'
  const { mobile } = useDisplay()
  const drawer = ref(true)
  const route = useRoute()

  // Lista de rutas donde solo quieres mostrar el router-view
  const fullScreenRoutes = new Set(['/'])

  const isFullScreenRoute = computed(() => fullScreenRoutes.has(route.path))
  const isHome = computed(() => route.path === '/')

  watch(
    mobile,
    newVal => {
      drawer.value = !newVal
    },
    { immediate: true },
  )
</script>

<style>

 .champions-parallax .v-img__img,
 .champions-parallax .v-parallax__image {
   filter: brightness(0.55) blur(1.5px) saturate(1.15) !important;
   transition: filter 0.3s;
 }

/* Evitar que los avatares se vean difuminados o pixelados */
.v-avatar .v-img__img,
.v-avatar img {
  filter: none !important;
}
</style>