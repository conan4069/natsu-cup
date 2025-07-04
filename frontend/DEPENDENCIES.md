# 📦 Dependencias - Natsu Cup Frontend

## ✅ Dependencias Instaladas

### Dependencias Principales
- **vue**: ^3.5.13 - Framework principal
- **vuetify**: ^3.8.1 - Framework de componentes Material Design
- **axios**: ^1.10.0 - Cliente HTTP para APIs
- **@fontsource/roboto**: 5.2.5 - Fuente Roboto
- **@mdi/font**: 7.4.47 - Iconos Material Design

### Dependencias de Desarrollo
- **@vitejs/plugin-vue**: ^5.2.3 - Plugin de Vue para Vite
- **vite**: ^6.2.2 - Herramienta de construcción
- **vite-plugin-vuetify**: ^2.1.1 - Plugin de Vuetify para Vite
- **unplugin-auto-import**: ^19.1.1 - Auto-importación de funciones
- **unplugin-vue-components**: ^28.4.1 - Auto-importación de componentes
- **unplugin-vue-router**: ^0.12.0 - Enrutador automático
- **unplugin-fonts**: ^1.3.1 - Gestión de fuentes
- **vite-plugin-vue-layouts-next**: ^0.0.8 - Sistema de layouts
- **pinia**: ^3.0.1 - Store de estado
- **vue-router**: ^4.5.0 - Enrutador oficial
- **sass-embedded**: ^1.86.3 - Preprocesador SCSS
- **eslint**: ^9.23.0 - Linter de código
- **eslint-config-vuetify**: ^4.0.0 - Configuración ESLint para Vuetify
- **globals**: ^16.0.0 - Variables globales para ESLint

## ⚠️ Dependencias Faltantes (Opcionales)

### ESLint Plugins (Recomendados)
```bash
npm install --save-dev @eslint/js eslint-plugin-vue @stylistic/eslint-plugin --legacy-peer-deps
```

### Prettier (Opcional)
```bash
npm install --save-dev prettier eslint-config-prettier eslint-plugin-prettier
```

### Testing (Opcional)
```bash
npm install --save-dev vitest @vue/test-utils jsdom
```

### TypeScript (Opcional)
```bash
npm install --save-dev typescript @vue/tsconfig
```

## 🔧 Configuración Actual

### Vite Config
- ✅ Vue 3 con Composition API
- ✅ Vuetify con auto-importación
- ✅ Auto-importación de componentes y funciones
- ✅ Sistema de layouts automático
- ✅ Gestión de fuentes con unplugin-fonts
- ✅ Enrutador automático basado en archivos

### ESLint Config
- ✅ Configuración básica de Vuetify
- ✅ Reglas para Vue 3
- ✅ Auto-importación configurada

### SCSS Config
- ✅ Preprocesador configurado
- ✅ Variables de Vuetify disponibles
- ✅ API moderna del compilador

## 🚀 Scripts Disponibles

```json
{
  "dev": "vite",
  "build": "vite build", 
  "preview": "vite preview",
  "lint": "eslint . --fix"
}
```

## 📋 Estado del Proyecto

### ✅ Funcionalidades Implementadas
- [x] Configuración base de Vue 3 + Vuetify
- [x] Sistema de rutas automático
- [x] Auto-importación de componentes
- [x] Layouts automáticos
- [x] Gestión de fuentes optimizada
- [x] Configuración de ESLint
- [x] Páginas de ejemplo (Home, Tournaments)
- [x] Sistema de navegación
- [x] Documentación completa

### 🔄 Próximos Pasos
- [ ] Instalar dependencias opcionales de ESLint
- [ ] Configurar Prettier (opcional)
- [ ] Agregar testing (opcional)
- [ ] Configurar TypeScript (opcional)

## 🐛 Solución de Problemas

### Conflictos de Versiones
Si encuentras conflictos de versiones con Vite 7:
```bash
npm install --legacy-peer-deps
```

### ESLint Errors
Si hay errores de ESLint:
```bash
npm run lint
```

### Fuentes No Cargadas
Verificar configuración en `vite.config.mjs`:
```javascript
Fonts({
  google: {
    families: [{
      name: 'Roboto',
      styles: 'wght@100;300;400;500;700;900',
    }],
  },
})
```

## 📚 Recursos

- [Vue 3 Documentation](https://vuejs.org/)
- [Vuetify Documentation](https://vuetifyjs.com/)
- [Vite Documentation](https://vitejs.dev/)
- [unplugin-fonts](https://github.com/unplugin/unplugin-fonts)
- [unplugin-vue-router](https://github.com/posva/unplugin-vue-router) 