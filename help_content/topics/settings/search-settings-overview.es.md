---
title: Comprensión de la configuración de búsqueda
---

La interfaz SearchSettings controla todo el comportamiento de búsqueda global en su tienda Spwig. Esta única página de configuración utiliza una interfaz de 8 pestañas para organizar las opciones de búsqueda, desde la habilitación básica hasta el ajuste de rendimiento avanzado. Los cambios realizados aquí se aplican a todos los motores de búsqueda, a menos que se anulen a nivel del motor.

Esta guía recorre cada pestaña, explicando qué hace cada configuración y cuándo ajustarla.

![Pestaña General de Configuración de Búsqueda](/static/core/admin/img/help/search-settings-overview/search-settings-general.webp)

## La interfaz de 8 pestañas

SearchSettings es un modelo singleton - solo existe un registro de configuración (pk=1) para toda su tienda. La interfaz se divide en ocho pestañas:

| Pestaña | Propósito |
|--------|----------|
| **General** | Habilitar/deshabilitar búsqueda, establecer parámetros básicos |
| **Autocomplete** | Configurar el comportamiento del menú desplegable de búsqueda predictiva |
| **Tipos de contenido** | Elegir qué tipos de contenido son buscables |
| **Indexación profunda** | Controlar qué datos del producto se indexan (impacto en el rendimiento) |
| **Coincidencia difusa** | Tolerancia a errores de escritura y umbrales de similitud |
| **Pesos** | Multiplicadores de relevancia para el ranking de resultados |
| **Caché** | Compromiso entre tiempo de respuesta y frescura |
| **Análisis** | Seguimiento de consultas y configuraciones de privacidad |

Cada pestaña se centra en un aspecto específico de la configuración de búsqueda.

## Pestaña General

La pestaña General contiene ajustes básicos que afectan a todas las búsquedas:

**Habilitar búsqueda** - Interruptor principal del sistema de búsqueda. Cuando se deshabilita, todas las funciones de búsqueda están inactivas en toda su tienda, incluyendo el autocompletado y la página de resultados de búsqueda.

**Longitud mínima de consulta** - Valor predeterminado: 2 caracteres. Las búsquedas más cortas que esto se rechazan. Establecer esto en 1 permite búsquedas de un solo carácter (por ejemplo, "A") pero aumenta la carga del servidor.

**Resultados por página** - Valor predeterminado: 20 elementos. Controla la paginación para las páginas de resultados de búsqueda. Valores más altos (30-50) reducen los clics de paginación pero aumentan el tiempo de carga de la página.

## Pestaña Tipos de Contenido

![Configuración de Tipos de Contenido](/static/core/admin/img/help/search-settings-overview/search-settings-content-types.webp)

Active o desactive qué tipos de contenido aparecen en los resultados de búsqueda:

- **Productos** - Productos físicos, digitales y de suscripción
- **Categorías** - Categorías de productos
- **Marcas** - Marcas de productos
- **Entradas del blog** - Contenido del blog

**Nota de rendimiento**: Menos tipos de contenido = búsquedas más rápidas. Cada tipo habilitado agrega consultas adicionales a la base de datos. Si no tiene un blog, desactive Entradas del blog para mejorar los tiempos de respuesta.

## Pestaña Indexación Profunda

⚠️ **ADVERTENCIA DE RENDIMIENTO** - Estas configuraciones tienen implicaciones significativas en el rendimiento.

![Configuración de Indexación Profunda](/static/core/admin/img/help/search-settings-overview/search-settings-deep-indexing.webp)

La indexación profunda controla qué datos relacionados con los productos se incluyen en las búsquedas:

**Índice de SKUs** - Valor predeterminado: ACTIVADO, bajo impacto. Incluye SKUs de productos y variantes en la búsqueda. Esencial para tiendas B2B donde los clientes buscan por códigos de producto.

**Índice de atributos** - Valor predeterminado: ACTIVADO, impacto medio. Incluye atributos de productos (color, tamaño, material) en la búsqueda. Agrega una unión a la tabla de atributos. Importante para productos de moda y configurables.

**Índice de campos personalizados** - Valor predeterminado: ACTIVADO, impacto medio. Incluye campos personalizados definidos por el comerciante en los resultados de búsqueda. Requiere recorrido de campos JSON.

**Índice de reseñas** - Valor predeterminado: ACTIVADO, impacto medio-alto. Incluye títulos y comentarios de reseñas aprobadas en la búsqueda. Une a la tabla de reseñas y agrega sobrecarga de búsqueda de texto. Útil para catálogos con muchas reseñas.

**Índice de documentos** - Valor predeterminado: DESACTIVADO, **IMPACTO MUY ALTO** ⚠️

La indexación de documentos extrae texto de archivos PDF, DOCX y XLSX adjuntos a productos digitales. Esta función:

- Requiere una indexación inicial muy costosa
- Agrega una sobrecarga significativa en cada búsqueda
- Puede causar tiempos de espera en archivos grandes
- **Debería activarse solo para tiendas de productos digitales con documentos buscables**
- **Nunca active esta opción casualmente** - pruebe el impacto en el rendimiento exhaustivamente

## Pestaña de coincidencia difusa

![Configuración de coincidencia difusa](/static/core/admin/img/help/search-settings-overview/search-settings-fuzzy-matching.webp)

La coincidencia difusa utiliza la distancia de Levenshtein para manejar errores de escritura:

**Habilitar coincidencia difusa** - Permite que las búsquedas coincidan con términos similares (por ejemplo, "laptop" coincide con "labtop")

**Umbral de similitud** - Valor predeterminado: 0.80 (80% de similitud). Rango: 0.0-1.0. Valores más altos requieren coincidencias más cercanas y funcionan más rápido. Valores más bajos capturan más errores de escritura pero pueden devolver resultados irrelevantes.

**Máximo de distancia de edición** - Valor predeterminado: 2 cambios de caracteres. Número máximo de inserciones, eliminaciones o sustituciones permitidas. Valores más bajos (1) mejoran el rendimiento pero capturan menos errores de escritura.

## Pestaña de Pesos

Los pesos controlan el puntaje de relevancia - cómo se clasifican los resultados. La pestaña de Pesos muestra los multiplicadores predeterminados para cada campo buscable:

- weight_name: 1.50 (los nombres de productos son lo más importante)
- weight_sku: 1.20
- weight_description: 0.80
- weight_categories: 0.80
- weight_attributes: 0.70
- weight_brands: 0.70
- weight_blog_posts: 0.60
- weight_reviews: 0.50

Estos valores predeterminados funcionan bien para la mayoría de las tiendas de comercio electrónico. Para información detallada sobre el ajuste de pesos y su impacto, consulte el tema [Pesos de relevancia y indexación profunda](/en/admin/help/relevance-weights-deep-indexing/).

## Pestaña de Caché

![Configuración de Caché](/static/core/admin/img/help/search-settings-overview/search-settings-caching.webp)

El caché mejora significativamente el rendimiento de la búsqueda almacenando resultados recientes:

**Tiempo de vida del caché de autocompletado** - Valor predeterminado: 60 segundos. Duración del caché de resultados de autocompletado. Un TTL más corto (30-45s) = resultados más recientes pero más consultas a la base de datos. Un TTL más largo (90-120s) = más rápido pero resultados potencialmente obsoletos.

**Tiempo de vida del caché de resultados** - Valor predeterminado: 300 segundos (5 minutos). Duración del caché de la página completa de resultados de búsqueda. Un TTL más largo mejora significativamente el rendimiento pero retrasa la visibilidad de nuevos productos.

**Compromisos**: El caché es la optimización de rendimiento más efectiva. Si las búsquedas son lentas, aumente estos valores antes de deshabilitar funciones.

## Pestaña de Análisis

![Configuración de Análisis](/static/core/admin/img/help/search-settings-overview/search-settings-analytics.webp)

**Seguimiento de consultas de búsqueda** - Habilita el panel de análisis de búsqueda. Registra el texto de la consulta, el recuento de resultados, el tiempo de respuesta y la marca de tiempo.

**Seguimiento de información del usuario** - Asocia búsquedas con usuarios conectados. Désablelo para cumplir con normas de privacidad (GDPR, CCPA).

**Seguimiento de información de sesión** - Usa IDs de sesión para seguir búsquedas de usuarios anónimos. Útil para identificar patrones de búsqueda sin datos personales.

## Patrón Singleton

SearchSettings utiliza un patrón singleton - solo existe un registro de configuración en su base de datos (pk=1). Cuando navega a Configuración de búsqueda en el administrador, siempre está editando el mismo registro.

No hay opciones de "Añadir" o "Eliminar" - solo "Cambiar". Todos los motores de búsqueda heredan estas configuraciones a menos que especifiquen anulaciones por motor (raro).

## Consejos

- **Mantenga los valores predeterminados a menos que tenga una necesidad específica** - Las configuraciones predeterminadas están optimizadas para tiendas de comercio electrónico típicas
- **NUNCA active la indexación de documentos de forma casual** - Solo para tiendas de productos digitales con documentos buscables, y pruebe primero el impacto en el rendimiento
- **Monitorea los tiempos de respuesta en el análisis** - Objetivo: <200ms para autocompletado, <500ms para búsqueda completa
- **Aumenta el TTL del caché si el rendimiento es lento** - El caché es el mayor beneficio de rendimiento
- **Revisa las consultas sin resultados semanalmente** - Revelan productos faltantes o sinónimos necesarios
- **Deshabilite los tipos de contenido no utilizados** - Si no tiene un blog, desactive Entradas del blog para acelerar las búsquedas

Recuerde: preserve all markdown formatting, image paths, code blocks, and technical terms exactly as shown in the preservation rules.