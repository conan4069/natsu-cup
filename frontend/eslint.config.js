// eslint.config.js
import globals from 'globals'
import vue from 'eslint-plugin-vue'
import prettier from 'eslint-plugin-prettier/recommended'
import js from '@eslint/js'

// Para autoimportadores como unplugin-vue-components no hay que usar import/no-unresolved,
// pero puedes agregar resolvers si lo deseas.

export default [
  {
    ignores: ['node_modules/**', 'dist/**'],
  },
  {
    languageOptions: {
      ecmaVersion: 2022,
      sourceType: 'module',
      globals: {
        ...globals.browser,
        ...globals.node,
      },
    },
    plugins: {
      vue,
    },
    rules: {
      // Reglas generales
      ...js.configs.recommended.rules,
      ...vue.configs['flat/recommended'].rules,
      'vue/attributes-order': [
        'error',
        {
          alphabetical: true,
        },
      ],
      'no-trailing-spaces': 'error',
      'no-multi-spaces': 'error',
      'no-irregular-whitespace': 'error',
      semi: ['error', 'never'],
      quotes: ['error', 'single'],
      indent: ['error', 2],
      'comma-dangle': ['error', 'always-multiline'],
      'max-len': ['warn', { code: 80 }],
      'arrow-parens': ['error', 'as-needed'],

      'prettier/prettier': [
        'error',
        {
          semi: false,
          singleQuote: true,
          trailingComma: 'es5',
          tabWidth: 2,
          printWidth: 80,
          arrowParens: 'avoid',
          bracketSpacing: true,
          endOfLine: 'lf',
        },
      ],

      // Reglas Vue específicas
      'vue/multi-word-component-names': 'off',
    },
  },
  prettier,
]
