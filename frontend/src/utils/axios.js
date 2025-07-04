import axios from 'axios'

// Crear instancia de axios con configuración base
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Interceptor para requests
api.interceptors.request.use(
  config => {
    // Agregar token de autenticación si existe
    const token = localStorage.getItem('authToken')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// Interceptor para responses
api.interceptors.response.use(
  response => {
    return response
  },
  error => {
    // Manejar errores de autenticación
    if (error.response?.status === 401) {
      localStorage.removeItem('authToken')
      // Redirigir al login si es necesario
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

// Función para manejar errores de API
export const handleApiError = error => {
  if (error.response) {
    // El servidor respondió con un código de estado de error
    console.error('Error de API:', error.response.data)
    return {
      message: error.response.data.message || 'Error en el servidor',
      status: error.response.status,
    }
  } else if (error.request) {
    // La petición fue hecha pero no se recibió respuesta
    console.error('Error de red:', error.request)
    return {
      message: 'Error de conexión. Verifica tu conexión a internet.',
      status: 0,
    }
  } else {
    // Algo más causó el error
    console.error('Error:', error.message)
    return {
      message: 'Error inesperado',
      status: 0,
    }
  }
}

export default api
