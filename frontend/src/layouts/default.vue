<template>
  <v-app>
    <!-- Barra de navegación -->
    <v-app-bar app color="primary" dark elevation="2">
      <v-app-bar-title class="d-flex align-center">
        <v-icon class="mr-2">mdi-trophy</v-icon>
        Natsu Cup
      </v-app-bar-title>

      <v-spacer />

      <!-- Navegación principal -->
      <v-btn
        :active="isActiveRoute('/')"
        class="mx-1"
        text
        to="/"
      >
        <v-icon left>mdi-home</v-icon>
        Inicio
      </v-btn>

      <v-btn
        :active="isActiveRoute('/tournaments')"
        class="mx-1"
        text
        to="/tournaments"
      >
        <v-icon left>mdi-trophy-outline</v-icon>
        Torneos
      </v-btn>

      <v-btn
        :active="isActiveRoute('/brackets')"
        class="mx-1"
        text
        to="/brackets"
      >
        <v-icon left>mdi-bracket-multiple</v-icon>
        Brackets
      </v-btn>

      <v-btn
        :active="isActiveRoute('/about')"
        class="mx-1"
        text
        to="/about"
      >
        <v-icon left>mdi-information</v-icon>
        Sobre
      </v-btn>

      <!-- Menú de usuario (opcional) -->
      <v-menu offset-y>
        <template #activator="{ props }">
          <v-btn
            v-bind="props"
            class="ml-2"
            icon
          >
            <v-icon>mdi-account-circle</v-icon>
          </v-btn>
        </template>

        <v-list>
          <v-list-item @click="handleProfile">
            <v-list-item-title>
              <v-icon left>mdi-account</v-icon>
              Perfil
            </v-list-item-title>
          </v-list-item>

          <v-list-item @click="handleSettings">
            <v-list-item-title>
              <v-icon left>mdi-cog</v-icon>
              Configuración
            </v-list-item-title>
          </v-list-item>

          <v-divider />

          <v-list-item @click="handleLogout">
            <v-list-item-title>
              <v-icon left>mdi-logout</v-icon>
              Cerrar Sesión
            </v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>
    </v-app-bar>

    <!-- Contenido principal -->
    <v-main>
      <v-container class="pa-0" fluid>
        <!-- Slot para el contenido de las rutas -->
        <v-router />
      </v-container>
    </v-main>

    <!-- Footer (opcional) -->
    <v-footer app class="py-3" color="grey-lighten-3">
      <v-container>
        <v-row align="center" justify="center">
          <v-col class="text-center" cols="12">
            <span class="text-caption text-grey-darken-1">
              © 2025 Natsu Cup. Todos los derechos reservados.
            </span>
          </v-col>
        </v-row>
      </v-container>
    </v-footer>
  </v-app>
</template>

<script setup>
  import { useRoute } from 'vue-router'

  const route = useRoute()

  // Computed para verificar si una ruta está activa
  const isActiveRoute = path => {
    return route.path === path
  }

  // Métodos para el menú de usuario
  const handleProfile = () => {
    console.log('Ir al perfil')
  // Aquí puedes agregar la lógica para ir al perfil
  }

  const handleSettings = () => {
    console.log('Ir a configuración')
  // Aquí puedes agregar la lógica para ir a configuración
  }

  const handleLogout = () => {
    console.log('Cerrar sesión')
  // Aquí puedes agregar la lógica para cerrar sesión
  }
</script>
