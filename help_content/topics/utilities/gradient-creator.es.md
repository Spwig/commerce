---
title: Creador de Gradientes
---

El Creador de Gradientes te permite crear transiciones de color suaves para los fondos de elementos. Se accede a través de la pestaña de Gradientes del Editor de Fondo y se abre como un panel flotante con una barra de gradiente visual, controles de puntos de color y opciones predefinidas.

![Creador de Gradientes](/static/core/admin/img/help/gradient-creator/gradient-creator.webp)

## Accediendo al Creador de Gradientes

1. Selecciona un elemento en el Page Builder o en el Header/Footer Builder
2. Abre la pestaña **Estilo** en el panel de propiedades
3. Haz clic en la sección **Fondo** para abrir el Editor de Fondo
4. Cambia a la pestaña **Gradiente**
5. El panel del Creador de Gradientes se abre con una vista previa en vivo y controles de edición

## Vista previa en vivo

En la parte superior del panel se muestra una comparación lado a lado:

| Caja | Propósito |
|------|----------|
| **Actual** | El gradiente existente (o transparente si no se ha establecido ninguno) |
| **Nuevo** | Se actualiza en tiempo real a medida que realizas cambios |

Una flecha entre las dos cajas indica la dirección del cambio.

## Tipos de Gradiente

Tres tipos de gradiente están disponibles, seleccionables mediante pestañas en la parte superior del editor:

| Tipo | Descripción | Controles |
|------|-------------|----------|
| **Lineal** | Transiciones de color a lo largo de una línea recta | Deslizador de ángulo (0-360 grados) con botones de dirección predefinida (hacia arriba, diagonal, hacia la derecha, hacia abajo, etc.) |
| **Radial** | Transiciones de color que se expanden desde un punto central | Selector de forma (círculo o elipse) y selector de posición (centro, arriba, abajo, esquinas) |
| **Cónico** | Transiciones de color que giran alrededor de un punto central | Deslizador de ángulo de inicio (0-360 grados) y selector de posición |

### Controles de Dirección Lineal

Para los gradientes lineales, puedes establecer el ángulo de tres maneras:
- **Deslizador de ángulo** — arrastra desde 0 a 360 grados
- **Campo de entrada de ángulo** — escribe un valor preciso en grados
- **Botones predefinidos** — haz clic en los iconos de flecha para direcciones comunes (hacia arriba, hacia arriba-derecha, hacia la derecha, hacia abajo-derecha, hacia abajo, hacia abajo-izquierda, hacia la izquierda, hacia arriba-izquierda)

## Puntos de Color

La barra de gradiente muestra tus puntos de color actuales como marcadores arrastrables. Cada punto define un color en una posición específica del gradiente.

**Añadir puntos** — Haz clic en el botón **+** en la sección de Puntos de Color para añadir un nuevo punto. No hay un límite estricto en el número de puntos.

**Editar puntos** — Cada punto en la lista muestra:
- Un cuadro de color que abre el selector de color al hacer clic
- Un valor de posición (0% a 100%) que puedes escribir o ajustar
- Un control de opacidad (0 a 1)
- Un botón de eliminar para quitar el punto

**Reordenar** — Arrastra los puntos a lo largo de la barra de gradiente para reubicarlos visualmente.

## Preset de Gradientes

Seis presets predefinidos están disponibles como puntos de partida rápidos. Haz clic en cualquier preset para aplicarlo de inmediato:

| Preset | Colores | Ángulo |
|--------|--------|-------|
| **Océano** | Azul claro a azul | 120 grados |
| **Atardecer** | Naranja cálido a rosa coral (3 puntos) | 45 grados |
| **Bosque** | Indigo a verde esmeralda | 135 grados |
| **Bayas** | Rosa a púrpura-azul | 90 grados |
| **Fuego** | Rojo a amarillo dorado | 45 grados |
| **Noche** | Plomo oscuro a azul marino | 180 grados |

Los presets son puntos de partida. Después de aplicar uno, puedes modificar los colores, añadir o eliminar puntos y cambiar el ángulo para crear tu propia variación.

## Acciones del Pie de Página

| Botón | Acción |
|--------|--------|
| **Limpiar** | Elimina completamente el gradiente, reiniciando a transparente |
| **Aplicar** | Guarda el gradiente y cierra el editor |

Cerrar el editor sin hacer clic en Aplicar descarta tus cambios.

## Dónde se Utiliza

El Creador de Gradientes se utiliza en:

- **Page Builder** — a través de la pestaña de Gradientes del Editor de Fondo en cualquier elemento
- **Header/Footer Builder** — para fondos de gradiente en secciones de encabezado, barras de navegación y áreas del pie de página

Trabaja junto con el Editor de Fondo, que también ofrece opciones de fondo en color sólido, imagen y video.

## Consejos

- **Empieza con un preset** — aplica un preset que esté cerca de lo que deseas, y luego ajusta los colores y el ángulo en lugar de construir desde cero.
- **Usa dos o tres puntos** — los gradientes simples con dos puntos lucen limpios y profesionales. Más puntos son útiles para efectos complejos, pero pueden volverse abrumadores rápidamente.
- **Alinea con tus colores de marca** — usa el selector de color para ingresar valores hex exactos de tu paleta de colores de marca para gradientes coherentes y alineados con tu marca.
- **Prueba con contenido** — los gradientes que lucen impactantes por sí mismos pueden reducir la legibilidad del texto. Siempre verifica que el texto sobre fondos de gradiente tenga suficiente contraste.
- **Prueba radial para efectos de foco** — los gradientes radiales funcionan bien para llamar la atención a un área central, como un punto focal de una sección hero.