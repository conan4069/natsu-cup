# 📁 Estructura del Proyecto - Natsu Cup Frontend

## 🗂️ Vista General

```
natsu-cup/frontend/
├── 📄 Archivos de Configuración
├── 📁 src/                    # Código fuente principal
├── 📁 public/                 # Archivos estáticos
└── 📁 node_modules/           # Dependencias (no versionado)
```

## 🔧 Archivos de Configuración

| Archivo | Descripción |
|---------|-------------|
| `package.json` | Dependencias y scripts del proyecto |
| `vite.config.mjs` | Configuración de Vite y plugins |
| `eslint.config.js` | Reglas de linting |
| `jsconfig.json` | Configuración de JavaScript |
| `env.example` | Variables de entorno de ejemplo |
| `Dockerfile` | Configuración para Docker |

## 📁 Estructura de `src/`

```
src/
├── 🎨 assets/                 # Recursos estáticos
│   ├── base.css              # Estilos base
│   ├── logo.svg              # Logo de la aplicación
│   └── main.css              # Estilos principales
│
├── 🧩 components/            # Componentes reutilizables
│   ├── btnConfirm/           # Botón de confirmación
│   │   └── btnConfirm.vue
│   ├── bracketView/          # Visualización de brackets
│   │   ├── BracketView.vue
│   │   └── KnockoutBracket.vue
│   ├── phaseStepper/         # Navegación por pasos
│   │   └── phaseStepper.vue
│   ├── phaseTimeLine/        # Línea de tiempo
│   │   └── phaseTimeLine.vue
│   ├── tableFase/            # Tabla de fases
│   │   └── tableFase.vue
│   ├── AppFooter.vue         # Pie de página
│   └── HelloWorld.vue        # Componente de ejemplo
│
├── 🎭 layouts/               # Layouts de la aplicación
│   └── default.vue           # Layout principal
│
├── 📄 pages/                 # Páginas (auto-importadas)
│   └── ...                   # Las rutas se crean automáticamente
│
├── 🔌 plugins/               # Plugins de Vue
│   └── ...                   # Configuraciones de plugins
│
├── 🛣️ router/                # Configuración de rutas
│   └── index.js              # Configuración principal
│
├── 🌐 services/              # Servicios y APIs
│   └── api.js                # Configuración de axios
│
├── 📦 stores/                # Stores de Pinia
│   └── counter.js            # Store de ejemplo
│
├── 🎨 styles/                # Estilos globales
│   └── settings.scss         # Variables de Vuetify
│
├── 🛠️ utils/                 # Utilidades y helpers
│   └── join.js               # Utilidades de unión
│
├── 📄 App.vue                # Componente raíz
└── 📄 main.js                # Punto de entrada
```

## 🧩 Componentes Principales

### 📊 Brackets (`components/bracketView/`)
- **BracketView.vue**: Visualización principal de brackets de torneos
- **KnockoutBracket.vue**: Brackets de eliminación directa

### ⏱️ Fases (`components/phaseStepper/`, `components/phaseTimeLine/`)
- **phaseStepper.vue**: Navegación por pasos de torneo
- **phaseTimeLine.vue**: Línea de tiempo de fases

### 📋 Tablas (`components/tableFase/`)
- **tableFase.vue**: Tabla para mostrar fases de torneo

### 🔘 Utilidades (`components/btnConfirm/`)
- **btnConfirm.vue**: Botón de confirmación reutilizable

## 🎭 Layouts

### `layouts/default.vue`
Layout principal que incluye:
- Header con navegación
- Contenido principal
- Footer
- Sistema de navegación

## 🌐 Servicios

### `services/api.js`
Configuración centralizada de axios con:
- URL base desde variables de entorno
- Interceptores para manejo de errores
- Configuración de headers
- Manejo de respuestas

## 🎨 Estilos

### `styles/settings.scss`
Configuración de Vuetify con:
- Variables de color personalizadas
- Configuración de fuentes
- Variables de espaciado
- Mixins útiles

## 📄 Páginas

Las páginas en `src/pages/` se convierten automáticamente en rutas:
- `index.vue` → `/`
- `about.vue` → `/about`
- `tournaments.vue` → `/tournaments`
- `teams.vue` → `/teams`

## 🔌 Plugins Configurados

### Auto-Imports
- **Vue Router**: `useRouter()`, `useRoute()`
- **Pinia**: `defineStore()`, `storeToRefs()`
- **Vue**: `ref()`, `computed()`, `watch()`

### Componentes
- **Vuetify**: Todos los componentes de Vuetify
- **Auto-importación**: Componentes de `src/components/`

### Layouts
- **vite-plugin-vue-layouts**: Sistema automático de layouts

## 🚀 Flujo de Desarrollo

1. **Crear página**: Agregar archivo en `src/pages/`
2. **Crear componente**: Agregar en `src/components/`
3. **Configurar API**: Usar `src/services/api.js`
4. **Estilos**: Usar variables de `src/styles/settings.scss`
5. **Layout**: Asignar en `definePageMeta()`

## 📋 Convenciones

### Nomenclatura
- **Componentes**: PascalCase (`MyComponent.vue`)
- **Archivos**: kebab-case (`my-file.js`)
- **Carpetas**: kebab-case (`my-folder/`)

### Estructura de Componentes
```vue
<template>
  <!-- Template aquí -->
</template>

<script setup>
// Lógica del componente
</script>

<style scoped>
/* Estilos específicos */
</style>
```

### Imports
- Usar auto-imports cuando sea posible
- Imports relativos para archivos locales
- Imports absolutos con `@/` para archivos de src

## 🔍 Archivos Generados

Estos archivos se generan automáticamente:
- `auto-imports.d.ts` - Tipos de auto-imports
- `components.d.ts` - Tipos de componentes
- `.eslintrc-auto-import.json` - Configuración de ESLint

## 📚 Recursos Adicionales

- [README.md](./README.md) - Documentación principal
- [API_ROUTES_VALIDATION.md](./API_ROUTES_VALIDATION.md) - Validación de rutas API
- [Documentación de Vuetify](https://vuetifyjs.com/)
- [Documentación de Vue 3](https://vuejs.org/) 