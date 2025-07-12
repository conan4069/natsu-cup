<template>
  <v-container fluid>
    <!-- Loading state -->
    <div v-if="loading" class="d-flex justify-center align-center" style="min-height: 400px;">
      <v-progress-circular color="primary" indeterminate size="64" />
    </div>

    <!-- Error state -->
    <div v-else-if="error" class="text-center py-8">
      <v-icon class="mb-4" color="error" size="64">mdi-alert-circle</v-icon>
      <h3 class="text-h6 text-grey-darken-1 mb-2">Error al cargar jugador</h3>
      <p class="text-body-2 text-grey-darken-1 mb-4">{{ error }}</p>
      <v-btn color="primary" rounded="xl" @click="loadPlayer">Reintentar</v-btn>
    </div>

    <!-- Edit form -->
    <div v-else-if="player">
      <!-- Header -->
      <v-row class="mb-6">
        <v-col cols="12">
          <div class="d-flex align-center mb-4">
            <v-btn
              class="mr-4"
              color="white"
              icon="mdi-arrow-left"
              variant="text"
              @click="goBack"
            />
            <div>
              <h1 class="text-h4 font-weight-bold mb-2 page-title">Editar Jugador</h1>
              <p class="text-body-1 page-subtitle">
                Modifica la información de {{ player.display_name }}
              </p>
            </div>
          </div>
        </v-col>
      </v-row>

      <!-- Formulario -->
      <v-row justify="center">
        <v-col cols="12" lg="6" md="8">
          <v-card>
            <v-card-title class="text-h6 pa-6 pb-0">
              Información del Ju
