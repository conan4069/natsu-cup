<template>
  <v-container>
    <v-row>
      <!-- Clasificación paso a paso -->
      <v-col cols="12" md="5">
        <PhaseTimeline :steps="qualificationSteps" />
      </v-col>

      <!-- Bracket render dinámico -->
      <v-col cols="12" md="7">
        <transition name="fade">
          <KnockoutBracket :matches="knockoutMatches" />
        </transition>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import PhaseTimeline from '../phaseTimeLine/phaseTimeLine.vue'
import KnockoutBracket from './KnockoutBracket.vue' // componente que dibuja rondas

const qualificationSteps = ref([])
const knockoutMatches = ref([])

onMounted(async () => {
  const res = await fetch('/api/tournaments/3/knockout-preview/')  // <- construir este endpoint
  const data = await res.json()
  qualificationSteps.value = data.qualification_steps
  knockoutMatches.value = data.main_bracket.matches
})
</script>

<style>
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.5s;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
</style>
