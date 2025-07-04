# Natsu Cup - Frontend

Frontend de la aplicación Natsu Cup desarrollado con Vue 3, Vuetify y Vite.

## 🚀 Tecnologías

- **Vue 3** - Framework de JavaScript progresivo
- **Vuetify 3** - Framework de componentes Material Design
- **Vite** - Herramienta de construcción rápida
- **Vue Router** - Enrutador oficial de Vue
- **Pinia** - Store de estado para Vue
- **SCSS** - Preprocesador de CSS
- **ESLint + Prettier** - Linting y formateo de código

## 📁 Estructura del Proyecto

```
frontend/
├── public/                 # Archivos estáticos
├── src/
│   ├── assets/            # Recursos estáticos (imágenes, iconos)
│   │   └── ...
│   ├── components/        # Componentes reutilizables
│   │   ├── btnConfirm/    # Componente de botón de confirmación
│   │   ├── bracketView/   # Componentes para visualización de brackets
│   │   ├── phaseStepper/  # Componente de pasos de fase
│   │   ├── phaseTimeLine/ # Componente de línea de tiempo
│   │   └── tableFase/     # Componente de tabla de fases
│   ├── layouts/           # Layouts de la aplicación
│   │   └── default.vue    # Layout principal
│   ├── pages/             # Páginas de la aplicación (auto-importadas)
│   ├── plugins/           # Plugins de Vue
│   ├── router/            # Configuración de rutas
│   ├── services/          # Servicios y APIs
│   │   └── api.js         # Configuración base de axios
│   ├── stores/            # Stores de Pinia
│   ├── styles/            # Estilos globales
│   │   └── settings.scss  # Variables y configuración de Vuetify
│   ├── utils/             # Utilidades y helpers
│   ├── App.vue            # Componente raíz
│   └── main.js            # Punto de entrada
├── .eslintrc-auto-import.json  # Configuración de auto-imports
├── auto-imports.d.ts      # Tipos de auto-imports
├── components.d.ts        # Tipos de componentes
├── env.example            # Variables de entorno de ejemplo
├── eslint.config.js       # Configuración de ESLint
├── jsconfig.json          # Configuración de JavaScript
├── package.json           # Dependencias del proyecto
├── vite.config.mjs        # Configuración de Vite
└── README.md              # Este archivo
```

## 🛠️ Configuración

### Prerrequisitos

- Node.js 18+ 
- npm o yarn

### Instalación

1. **Clonar el repositorio**
   ```bash
   git clone <url-del-repositorio>
   cd natsu-cup/frontend
   ```

2. **Instalar dependencias**
   ```bash
   npm install
   ```

3. **Configurar variables de entorno**
   ```bash
   cp env.example .env
   ```
   Edita el archivo `.env` con tus configuraciones:
   ```env
   VITE_API_URL=http://localhost:8000/api
   VITE_APP_TITLE=Natsu Cup
   VITE_APP_VERSION=1.0.0
   ```

4. **Ejecutar en desarrollo**
   ```bash
   npm run dev
   ```

## 🔧 Scripts Disponibles

```bash
# Desarrollo
npm run dev              # Servidor de desarrollo en http://localhost:3000

# Construcción
npm run build            # Construir para producción
npm run preview          # Previsualizar build de producción

# Linting y formateo
npm run lint             # Ejecutar ESLint
npm run lint:fix         # Corregir errores de ESLint automáticamente
npm run format           # Formatear código con Prettier

# Análisis
npm run analyze          # Analizar bundle de producción
```

## 🎨 Sistema de Diseño

### Fuentes
- **Roboto**: Fuente principal (pesos: 100, 300, 400, 500, 700, 900)
- Configurado con `unplugin-fonts/vite` para optimización automática

### Estilos
- **SCSS** como preprocesador
- Variables globales en `src/styles/settings.scss`
- Integración completa con Vuetify

## 🔌 Plugins Configurados

### Auto-Imports
- **Vue Router**: Rutas y navegación
- **Pinia**: Stores y estado
- **Vue**: Composables y utilidades

### Componentes
- **Vuetify**: Componentes Material Design
- **Auto-importación**: Componentes de `src/components/` y `src/pages/`

### Layouts
- **vite-plugin-vue-layouts**: Sistema de layouts automático
- Layouts en `src/layouts/`

## 🌐 API y Servicios

### Configuración Base
- **Axios** configurado en `src/services/api.js`
- Interceptores para manejo de errores
- Configuración base desde variables de entorno

### Rutas API
Las rutas están sincronizadas con el backend Django:
- `/api/tournaments/` - Gestión de torneos
- `/api/teams/` - Gestión de equipos
- `/api/matches/` - Gestión de partidas
- `/api/brackets/` - Gestión de brackets

## 📱 Componentes Principales

### Brackets
- `BracketView.vue` - Visualización principal de brackets
- `KnockoutBracket.vue` - Brackets de eliminación

### Fases
- `phaseStepper.vue` - Navegación por pasos
- `phaseTimeLine.vue` - Línea de tiempo de fases
- `tableFase.vue` - Tabla de fases

### Utilidades
- `btnConfirm.vue` - Botón de confirmación reutilizable

## 🚀 Despliegue

### Docker
```bash
# Construir imagen
docker build -t natsu-cup-frontend .

# Ejecutar contenedor
docker run -p 3000:3000 natsu-cup-frontend
```

### Producción
```bash
# Construir
npm run build

# Los archivos se generan en dist/
```

## 🔍 Desarrollo

### Estructura de Componentes
Cada componente debe seguir esta estructura:
```vue
<template>
  <!-- Template aquí -->
</template>

<script setup>
// Lógica del componente
</script>

<style scoped>
/* Estilos específicos del componente */
</style>
```

### Convenciones de Nomenclatura
- **Componentes**: PascalCase (`MyComponent.vue`)
- **Archivos**: kebab-case (`my-file.js`)
- **Variables**: camelCase (`myVariable`)
- **Constantes**: UPPER_SNAKE_CASE (`MY_CONSTANT`)

### Rutas
- Las rutas se crean automáticamente desde `src/pages/`
- Usar `definePageMeta()` para metadatos de página
- Layouts se asignan automáticamente

## 📚 Documentación Adicional

- [📁 Estructura del Proyecto](./STRUCTURE.md) - Guía visual de la estructura de carpetas
- [📦 Dependencias](./DEPENDENCIES.md) - Estado y configuración de dependencias
- [🎨 Sistema de Fuentes](./FONTS.md) - Configuración y uso de fuentes
- [🔗 API Routes Validation](./API_ROUTES_VALIDATION.md) - Validación de rutas API
- [🎨 Vuetify Documentation](https://vuetifyjs.com/) - Documentación oficial de Vuetify
- [⚡ Vue 3 Documentation](https://vuejs.org/) - Documentación oficial de Vue

## 🤝 Contribución

1. Crear una rama para tu feature
2. Hacer commits descriptivos
3. Ejecutar `npm run lint` antes de hacer push
4. Crear un Pull Request

## 📄 Licencia

Este proyecto está bajo la licencia MIT.
