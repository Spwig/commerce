---
title: Explicación de Motores de Búsqueda
---

Los motores de búsqueda en Spwig no son servicios externos como Elasticsearch o Algolia - son contextos de configuración dentro del sistema de búsqueda nativo de la base de datos de su tienda. Cada motor define qué tipos de contenido buscar, qué excluir y cómo deben clasificarse los resultados. Esta guía explica qué son los motores de búsqueda, cuándo crear múltiples motores y cómo configurarlos.

La mayoría de los comerciantes usan un solo motor predeterminado "shop". Cree múltiples motores solo cuando necesite mezclas de contenido diferentes o exclusiones para diferentes casos de uso.

![Lista de Motores de Búsqueda](/static/core/admin/img/help/search-engines-explained/search-engines-list.webp)

## ¿Qué son los Motores de Búsqueda?

Un motor de búsqueda en Spwig es una configuración con nombre que especifica:

- **¿Qué tipos de contenido buscar** (productos, categorías, marcas, entradas de blog)
- **¿Qué excluir** (categorías o marcas específicas que desea ocultar de la búsqueda)
- **Ponderaciones de relevancia personalizadas** (sobrescrituras de ponderación por motor, opcionales)
- **Estado activo** (los motores pueden desactivarse temporalmente)

Cada motor tiene un slug único que se usa en llamadas a la API y en el código del frontend para especificar qué motor debe manejar una solicitud de búsqueda.

## ¿Cuándo crear múltiples motores?

La mayoría de las tiendas necesitan solo un motor. Cree motores adicionales para estos escenarios:

| Caso de Uso | Ejemplo |
|----------|---------|
| **Diferentes mezclas de contenido** | El motor de tienda busca solo productos; el motor de blog busca solo entradas de blog |
| **Exclusiones selectivas** | El motor principal de tienda oculta la categoría de liquidación; el motor de liquidación muestra solo artículos de liquidación |
| **Búsqueda específica por departamento** | El motor de electrónicos excluye categorías de ropa; el motor de ropa excluye electrónicos |
| **Separación B2B vs B2C** | El motor de mayoreo muestra solo productos en cantidad; el motor de venta al por menor muestra productos para consumidores |

Si no está seguro de si necesita múltiples motores, siga con uno. Agregar motores crea complejidad sin beneficios a menos que tenga un caso de uso específico.

## El Asistente de 4 Pasos

![Paso 1 del Asistente - Información Básica](/static/core/admin/img/help/search-engines-explained/wizard-step1-basic.webp)

Navegue a **Búsqueda > Asistente de Configuración** para crear un nuevo motor a través de un proceso guiado de 4 pasos:

### Paso 1: Información Básica

**Nombre del Motor** - Nombre amigable para mostrar (ej. "Búsqueda de Tienda", "Búsqueda de Blog"). Se usa solo en la interfaz de administración.

**Slug** - Identificador seguro para URL (ej. "shop-search", "blog-search"). Se usa en llamadas a la API y en el código del frontend. Se genera automáticamente desde el nombre si se deja en blanco.

**Activo** - Si este motor está disponible para búsquedas. Los motores inactivos no devuelven resultados.

### Paso 2: Tipos de Contenido

Seleccione qué tipos de contenido buscará este motor:

- Productos (incluye todos los tipos de productos: físicos, digitales, suscripciones)
- Categorías
- Marcas
- Entradas de Blog

**Consejo**: Seleccione solo los tipos de contenido relevantes para el propósito de este motor. Un motor enfocado en blogs no necesita productos habilitados.

### Paso 3: Ponderaciones (Opcional)

![Paso 3 del Asistente - Ponderaciones](/static/core/admin/img/help/search-engines-explained/wizard-step3-weights.webp)

Personalice opcionalmente las ponderaciones de relevancia para este motor específico. Si se omite, el motor hereda las ponderaciones globales de SearchSettings.

La mayoría de los motores deben omitir este paso y usar las ponderaciones predeterminadas globales. Solo personalice las ponderaciones si este motor tiene necesidades de clasificación únicas (por ejemplo, un motor de blog podría aumentar weight_blog_posts a 1.2).

### Paso 4: Revisión y Creación

Revise su configuración y haga clic en **Crear Motor** para guardar.

## Campos de Configuración del Motor

Si edita un motor directamente (saltando el asistente), verá estos campos:

**Nombre y Slug** - Nombre de visualización y identificador de URL

**Estado Activo** - Conmutador para habilitar/deshabilitar

**Tipos de Contenido** - Matriz JSON como `[