# 🎨 Sistema de Fuentes - Natsu Cup

## 📋 Resumen

Este proyecto utiliza `unplugin-fonts/vite` para cargar y optimizar automáticamente las fuentes de Google Fonts.

## 🔧 Configuración

### Fuentes Incluidas

- **Roboto**: Fuente principal (pesos: 100, 300, 400, 500, 700, 900)
- **Material Icons**: Iconos de Material Design

### Configuración en Vite

```javascript
// vite.config.mjs
Fonts({
  google: {
    families: [{
      name: 'Roboto',
      styles: 'wght@100;300;400;500;700;900',
    }],
  },
})
```

## 🚀 Ventajas

✅ **Optimización automática** - Las fuentes se optimizan automáticamente  
✅ **Preload inteligente** - Solo carga lo necesario  
✅ **Display swap** - Evita FOUT (Flash of Unstyled Text)  
✅ **Subsetting** - Reduce tamaño de archivos  
✅ **Fácil mantenimiento** - Todo centralizado  

## 📝 Uso

### En Componentes Vue

```vue
<template>
  <!-- Las fuentes se aplican automáticamente -->
  <h1 class="text-h3">Título con Roboto</h1>
  <p class="text-body-1">Texto con Roboto</p>
  
  <!-- Material Icons -->
  <v-icon>home</v-icon>
  <v-icon>favorite</v-icon>
  <v-icon>star</v-icon>
</template>
```

### En SCSS

```scss
// Las fuentes están disponibles automáticamente
.my-component {
  font-family: 'Roboto', sans-serif;
  font-weight: 500;
}
```

## 🔧 Agregar Nuevas Fuentes

### Google Fonts

1. Editar `vite.config.mjs`:
```javascript
Fonts({
  google: {
    families: [
      {
        name: 'Roboto',
        styles: 'wght@100;300;400;500;700;900',
      },
      {
        name: 'Inter',  // Nueva fuente
        styles: 'wght@300;400;500;600;700',
      },
    ],
  },
})
```

2. Usar en tu código:
```scss
.my-text {
  font-family: 'Inter', sans-serif;
}
```

### Fuentes Locales

1. Agregar archivo de fuente en `src/assets/fonts/`
2. Configurar en `vite.config.mjs`:
```javascript
Fonts({
  custom: {
    families: {
      'MiFuente': './src/assets/fonts/MiFuente.woff2'
    },
  },
})
```

## 📊 Pesos Disponibles

- **100** - Thin
- **300** - Light
- **400** - Regular
- **500** - Medium
- **700** - Bold
- **900** - Black

## 🎯 Material Icons

Los iconos de Material Design están disponibles automáticamente:

```vue
<template>
  <!-- Iconos básicos -->
  <v-icon>home</v-icon>
  <v-icon>favorite</v-icon>
  <v-icon>star</v-icon>
  <v-icon>settings</v-icon>
  <v-icon>notifications</v-icon>
</template>
```

## 🔍 Verificación

Para verificar que las fuentes se cargan correctamente:

1. Abrir DevTools (F12)
2. Ir a la pestaña Network
3. Filtrar por "Font"
4. Deberías ver las fuentes cargándose desde Google Fonts

## 📚 Recursos

- [unplugin-fonts Documentation](https://github.com/unplugin/unplugin-fonts)
- [Google Fonts](https://fonts.google.com/)
- [Material Icons](https://fonts.google.com/icons)

## 🐛 Solución de Problemas

### Las fuentes no se cargan
- Verificar configuración en `vite.config.mjs`
- Revisar conexión a internet
- Limpiar cache del navegador

### Fuentes muy grandes
- Verificar que no haya duplicados en la configuración
- Usar subsetting para reducir tamaño

### FOUT (Flash of Unstyled Text)
- El plugin maneja esto automáticamente con `display: 'swap'`
- Si persiste, verificar configuración de preload 