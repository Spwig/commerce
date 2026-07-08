/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

// ESLint flat config (ESLint 9+)
import js from '@eslint/js';
import tsPlugin from '@typescript-eslint/eslint-plugin';
import tsParser from '@typescript-eslint/parser';

export default [
  js.configs.recommended,
  {
    files: ['**/*.{js,jsx,ts,tsx}'],
    languageOptions: {
      ecmaVersion: 2021,
      sourceType: 'module',
      parser: tsParser,
      globals: {
        // Browser globals
        window: 'readonly',
        document: 'readonly',
        console: 'readonly',
        // Node globals
        process: 'readonly',
        __dirname: 'readonly',
        module: 'readonly',
        require: 'readonly',
        // Django/common globals
        django: 'readonly',
        jQuery: 'readonly',
        $: 'readonly',
      },
    },
    plugins: {
      '@typescript-eslint': tsPlugin,
    },
    rules: {
      'no-unused-vars': 'warn',
      'no-console': 'off', // Allow console in development
      semi: ['error', 'always'],
      quotes: ['error', 'single', { avoidEscape: true }],
      'prefer-const': 'warn',
      'no-var': 'warn',
    },
  },
  {
    ignores: [
      'node_modules/',
      'staticfiles/',
      'shop_venv/',
      '.archive/',
      '**/vendor/',
      '**/ckeditor5/',
      '**/*.min.js',
      'pos_app/dist/',
      'pos_app/frontend_build/',
      'pos_app/frontend/node_modules/',
    ],
  },
];
