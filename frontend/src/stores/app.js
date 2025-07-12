// Utilities
import { defineStore } from 'pinia'

export const useAppStore = defineStore('app', {
  state: () => ({
    snackbar: {
      show: false,
      message: '',
      color: 'success', // success, error, warning, info
      timeout: 5000
    }
  }),

  actions: {
    showSnackbar(message, color = 'success', timeout = 5000) {
      this.snackbar = {
        show: true,
        message,
        color,
        timeout
      }
    },

    hideSnackbar() {
      this.snackbar.show = false
    },

    showError(message) {
      this.showSnackbar(message, 'error')
    },

    showSuccess(message) {
      this.showSnackbar(message, 'success')
    },

    showWarning(message) {
      this.showSnackbar(message, 'warning')
    },

    showInfo(message) {
      this.showSnackbar(message, 'info')
    }
  }
})
