# Frontend - Natsu Cup

## Configuración

Este proyecto utiliza Vue 3 con Vuetify 3 y axios para las comunicaciones con la API.

### Dependencias principales

- **Vue 3**: Framework de JavaScript progresivo
- **Vuetify 3**: Framework de componentes de Material Design
- **Axios**: Cliente HTTP para realizar peticiones a la API
- **Vue Router**: Enrutador oficial para Vue.js
- **Pinia**: Store de estado para Vue

### Configuración de Vuetify

Vuetify está configurado en `src/plugins/vuetify.js` con:

- Tema personalizado con colores Material Design
- Iconos de Material Design Icons
- Configuración de componentes por defecto

### Configuración de Vite

El archivo `vite.config.js` incluye:

- Configuración de alias para imports (`@` apunta a `src/`)
- Soporte para SCSS con importación automática de variables
- Configuración de servidor de desarrollo
- Optimizaciones para producción

### Estilos SCSS

El archivo `src/styles/settings.scss` contiene:

- Variables de color, espaciado y tipografía
- Mixins útiles para flexbox y responsive design
- Clases de utilidad para márgenes y padding
- Configuración global de componentes Vuetify

### Configuración de API

La configuración de API está separada en dos archivos:

- `src/utils/axios.js`: Configuración base de axios con interceptores
- `src/services/api.js`: Funciones específicas para endpoints de Django REST Framework

Características:
- Instancia de axios configurada con interceptores
- Manejo automático de tokens de autenticación
- Funciones específicas para todos los endpoints de Django
- Manejo de errores centralizado
- Rutas que coinciden exactamente con `apps/league/urls.py`

### Variables de entorno

Crear un archivo `.env` en la raíz del frontend basado en `env.example`:

```bash
# Copiar el archivo de ejemplo
cp env.example .env
```

Variables disponibles:
- `VITE_API_URL`: URL base de la API de Django (por defecto: http://localhost:8000/api)
- `VITE_DEV_MODE`: Modo de desarrollo
- `VITE_AUTH_ENABLED`: Habilitar autenticación
- `VITE_AUTH_TOKEN_KEY`: Clave para el token de autenticación

### Uso de la API

```javascript
import { tournamentAPI, matchAPI, playerAPI, gameTeamAPI, handleApiError } from '@/services/api'

// Ejemplo de uso con torneos
try {
  const response = await tournamentAPI.getTournaments()
  console.log(response.data)
} catch (error) {
  const errorInfo = handleApiError(error)
  console.error(errorInfo.message)
}

// Ejemplo de uso con partidos
const match = await matchAPI.getMatch(1)

// Ejemplo de uso con jugadores
const players = await playerAPI.getPlayers()

// Ejemplo de uso con equipos del juego
const teams = await gameTeamAPI.getGameTeams()
```

### Comandos disponibles

```bash
# Instalar dependencias
npm install

# Servidor de desarrollo
npm run dev

# Construir para producción
npm run build

# Vista previa de producción
npm run preview
```

### Estructura de archivos

```
src/
├── plugins/
│   └── vuetify.js          # Configuración de Vuetify
├── utils/
│   └── axios.js           # Configuración base de axios
├── services/
│   └── api.js             # Funciones específicas de API
├── styles/
│   └── settings.scss      # Variables y mixins SCSS
├── components/            # Componentes Vue
├── views/                 # Vistas de la aplicación
├── router/                # Configuración de rutas
└── stores/                # Stores de Pinia
```

## Recommended IDE Setup

[VSCode](https://code.visualstudio.com/) + [Volar](https://marketplace.visualstudio.com/items?itemName=Vue.volar) (and disable Vetur).

## Customize configuration

See [Vite Configuration Reference](https://vite.dev/config/).

## Project Setup

```sh
npm install
```

### Compile and Hot-Reload for Development

```sh
npm run dev
```

### Compile and Minify for Production

```sh
npm run build
```

### Lint with [ESLint](https://eslint.org/)

```sh
npm run lint
```
