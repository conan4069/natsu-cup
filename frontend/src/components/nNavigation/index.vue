<template>
  <v-navigation-drawer
    app
    color="#dedee5"
    expand-on-hover
    :model-value="drawer"
    :rail="true && !mobile"
    :temporary="mobile"
    @update:model-value="emit('update:modelValue')"
  >
    <v-list
      base-color="transparent"
      class="pt-0"
      color="primary"
      density="compact"
      slim
      variant="elevated"
    >
      <v-list-item
        v-for="(menuItem, key) in menuItems"
        :key="`menu-item-${key}`"
        :prepend-icon="menuItem.icon"
        :title="menuItem.title"
        :to="menuItem.href"
      />
    </v-list>
  </v-navigation-drawer>
</template>

<script setup>
  import { useDisplay } from 'vuetify'

  const menuItems = ref([
    {
      title: 'Inicio',
      icon: 'mdi-home',
      href: '/',
    },
    {
      title: 'Torneos',
      icon: 'mdi-trophy-outline',
      href: '/tournaments',
    },
    {
      title: 'Brackets',
      icon: 'mdi-tournament',
      href: '/brackets',
    },
    {
      title: 'Jugadores',
      icon: 'mdi-account-group',
      href: '/players',
    },
  ])

  const { modelValue: drawer } = defineProps({
    modelValue: {
      type: Boolean,
      required: true,
    },
  })

  const { mobile } = useDisplay()
  const emit = defineEmits(['update:modelValue'])
</script>

<style lang="scss" scoped>
:deep(.v-list-item--active .v-list-item-title) {
  font-weight: 700;
}
</style>
