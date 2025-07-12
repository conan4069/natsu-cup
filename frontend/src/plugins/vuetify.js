/**
 * plugins/vuetify.js
 *
 * Framework documentation: https://vuetifyjs.com`
 */

// Composables
import { createVuetify } from 'vuetify'
import { es } from 'vuetify/locale'

// Styles
import '@mdi/font/css/materialdesignicons.css'
import 'vuetify/styles'

// https://vuetifyjs.com/en/introduction/why-vuetify/#feature-guides
export default createVuetify({
  locale: {
    locale: 'es',
    messages: { es },
  },
  theme: {
    defaultTheme: 'light',
    themes: {
      light: {
        dark: false,
        colors: {
          primary: '#991e12',
          secondary: '#e61f12',
          accent: '#EF5350',
          surface: '#FFFFFF',
          background: '#f3f2e5',
          error: '#EF5350',
          info: '#64B5F6',
          success: '#2E7D33',
          warning: '#FFC107',
          disabled: '#757575',
          secondaryLight: '#26234F26',
          secondaryDark: '#242C50',
        },
      },
    },
  },
})
