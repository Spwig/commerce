---
title: Editor de bordes
---

El Editor de bordes proporciona un control detallado sobre los bordes de los elementos, incluyendo estilo, color, ancho por lado y radio de esquina por esquina. Se abre como un panel flotante con una vista previa en vivo y dos pestañas para ajustes básicos y avanzados.

![Editor de bordes](/static/core/admin/img/help/border-editor/border-editor.webp)

## Vista previa en vivo

Una caja de vista previa en la parte superior del editor muestra tus cambios de borde en tiempo real. La caja muestra la palabra "Vista previa" dentro de un rectángulo con borde que se actualiza instantáneamente a medida que ajustas los valores de estilo, color, ancho y radio.

## Modo básico vs. avanzado

El editor está organizado en dos pestañas:

| Pestaña | Qué contiene |
|--------|-------------|
| **Básico** | Estilo de borde, color, ancho (con controles por lado), y radio de borde (con controles por esquina) |
| **Avanzado** | Ajuste fino del radio de esquina individual y la propiedad experimental de forma de esquina |

La mayoría del trabajo con bordes se realiza completamente en la pestaña Básico. La pestaña Avanzada es útil cuando necesitas un control preciso sobre esquinas individuales o quieres experimentar con características CSS más nuevas.

## Estilo de borde

Un menú desplegable con nueve opciones que controlan la apariencia de la línea de borde:

| Estilo | Descripción |
|--------|-------------|
| **Ninguno** | Sin borde (elimina cualquier borde existente) |
| **Sólido** | Una línea continua (por defecto) |
| **Discontinuo** | Una serie de guiones cortos |
| **Punteado** | Una serie de puntos redondos |
| **Doble** | Dos líneas sólidas paralelas |
| **Grabado** | Un borde tallado con efecto 3D que parece incrustado en la superficie |
| **Relieve** | Un borde elevado con efecto 3D (opuesto a grabado) |
| **Insetado** | Hace que el elemento parezca incrustado o presionado |
| **Sobresaliente** | Hace que el elemento parezca elevado o saliente |

Establecer el estilo en Ninguno elimina completamente el borde, independientemente de los ajustes de ancho o color.

## Color de borde

Un campo de entrada de texto emparejado con un botón de selector de color. Introduzca un valor hexadecimal directamente (por ejemplo, `#3b82f6`) o haga clic en el cuadro de color para abrir el selector de color completo con modos de entrada hexadecimal, RGB y HSL, más un área visual de color. El color predeterminado es negro (`#000000`).

## Ancho de borde

Controla el grosor del borde en píxeles. La pestaña Básico muestra cuatro entradas individuales por lado:

| Lado | Entrada |
|------|--------|
| **Arriba** | Entrada numérica, mínimo 0 |
| **Derecha** | Entrada numérica, mínimo 0 |
| **Abajo** | Entrada numérica, mínimo 0 |
| **Izquierda** | Entrada numérica, mínimo 0 |

Un **botón de conmutación de enlace** (icono de cadena) junto al etiqueta controla si los cuatro lados están vinculados:

- **Vinculado** (por defecto) — al cambiar cualquier valor, se actualizan los cuatro lados a la vez
- **No vinculado** — cada lado puede tener un ancho diferente, útil para efectos como un borde solo en la parte inferior o bordes de acento en el lado izquierdo

## Radio de borde

Controla la redondez de cada esquina. La pestaña Básico muestra cuatro entradas de esquina:

| Esquina | Etiqueta |
|--------|--------|
| **Arriba a la izquierda** | TL |
| **Arriba a la derecha** | TR |
| **Abajo a la izquierda** | BL |
| **Abajo a la derecha** | BR |

Un **botón de conmutación de enlace** funciona de la misma manera que el ancho del borde:

- **Vinculado** (por defecto) — todas las cuatro esquinas comparten el mismo valor de radio
- **No vinculado** — cada esquina puede tener un radio diferente

Valores de radio comunes:

| Valor | Efecto |
|-------|--------|
| 0px | Esquinas cuadradas afiladas |
| 4-8px | Redondeo sutil, ideal para tarjetas y botones |
| 12-16px | Redondeo notorio, un aspecto moderno y suave |
| 50% | Círculo completo o forma de píldora (dependiendo de las dimensiones del elemento) |

El selector de unidades admite px, em, rem y % para los valores de ancho y radio.

## Forma de esquina (Avanzado)

La pestaña Avanzado incluye una propiedad experimental **Forma de esquina**. Esta característica de CSS controla si las esquinas redondeadas usan la forma redonda estándar o una forma más angular "scoop". El soporte del navegador es limitado, y el editor muestra una advertencia de compatibilidad cuando el navegador actual no admite esta propiedad.

## Acciones del pie de página

| Botón | Acción |
|--------|--------|
| **Restablecer** | Revierte todos los valores a su estado cuando se abrió el editor |
| **Cancelar** | Cierra el editor sin aplicar cambios |
| **Aplicar** | Guarda los ajustes del borde y cierra el editor |

## ¿Dónde aparece?

El Editor de bordes está disponible en varios editores:

- **Editor de páginas** — selecciona cualquier elemento, abre la pestaña Estilo y haz clic en la sección de Borde
- **Editor de encabezado/pie de página** — agrega bordes a secciones de encabezado, contenedores de navegación y áreas del pie de página
- **Editor de menú** — estila bordes en elementos del menú y contenedores de menús desplegables

El editor lee los estilos de borde calculados actuales del elemento en vivo en el lienzo, por lo que siempre se abre con los valores existentes correctos.

## Consejos

- **Usa bordes con moderación** — bordes sutiles de 1px en un gris claro crean una separación limpia entre secciones sin añadir peso visual.
- **Combina radio con sombra** — esquinas redondeadas combinadas con una sombra de caja suave (a través del Editor de sombras) producen un efecto de tarjeta pulido.
- **Prueba bordes por un solo lado** — desvincula los lados y establece solo un borde inferior o izquierdo para líneas de acento, divisores de sección o indicadores de barra lateral.
- **Usa radio en porcentaje para píldoras** — establece todas las esquinas en 50% en un botón o distintivo para crear una forma de píldora que se adapte a cualquier tamaño de contenido.
- **Verifica la vista previa** — la caja de vista previa en vivo se actualiza inmediatamente, así que experimenta libremente antes de aplicar.
