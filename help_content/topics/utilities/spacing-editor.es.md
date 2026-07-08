---
title: Editor de Espaciado
---

El editor visual de espaciado le permite configurar márgenes y relleno utilizando un diagrama del modelo de caja intuitivo. El control preciso del espaciado asegura diseños consistentes y experiencias de lectura cómodas en toda su tienda en línea. Abra la **pestaña de Estilo** de cualquier elemento y busque la sección **Espaciado** para acceder al editor.

![Editor de Espaciado](/static/core/admin/img/help/spacing-editor/spacing-editor.webp)

## El Diagrama del Modelo de Caja

El editor muestra un diagrama visual del modelo de caja con tres capas anidadas:

- **Márgen** (anillo exterior, normalmente mostrado en naranja) — El espacio fuera del borde del elemento, que lo separa de los elementos vecinos
- **Relleno** (anillo interior, normalmente mostrado en verde) — El espacio entre el borde del elemento y su contenido
- **Contenido** (área central) — El contenido real del elemento, como texto o una imagen

Cada lado del diagrama (arriba, derecha, abajo, izquierda) tiene un control deslizante y una entrada numérica. Arrastre un control hacia afuera para aumentar el valor, o hacia adentro para disminuirlo. También puede hacer clic directamente en el valor de un lado para escribir un número preciso.

## Pestañas de Márgen y Relleno

Dos pestañas en la parte superior del editor alternan entre las vistas de **Márgen** y **Relleno**. Cuando se selecciona Márgen, el anillo exterior se resalta y se puede editar. Cuando se selecciona Relleno, el anillo interior se resalta y se puede editar. El anillo inactivo sigue visible para referencia, pero se atenúa.

Ambas pestañas comparten los mismos controles y opciones de unidad, por lo que el flujo de trabajo es idéntico para la configuración de márgen y relleno.

## Controles por Lado

Cada lado tiene una entrada de valor independiente y un selector de unidad:

| Lado | Descripción |
|------|-------------|
| **Arriba** | Espacio encima del elemento (márgen) o encima del contenido (relleno) |
| **Derecha** | Espacio a la derecha del elemento o del contenido |
| **Abajo** | Espacio debajo del elemento o del contenido |
| **Izquierda** | Espacio a la izquierda del elemento o del contenido |

Haga clic en el valor de cualquier lado en el diagrama para seleccionarlo, luego escriba un número o use las teclas de flecha hacia arriba/abajo para incrementar en 1. Mantenga presionada la tecla Shift mientras presiona las teclas de flecha para incrementar en 10.

## Unidades

El selector de unidades junto a cada entrada de valor le permite elegir la unidad de medida:

| Unidad | Descripción |
|------|-------------|
| **px** | Píxeles. Tamaño fijo, consistente en todos los dispositivos. Ideal para valores de espaciado precisos y pequeños. |
| **em** | Relativo al tamaño de fuente del elemento. Escala con cambios en el tipografía. |
| **rem** | Relativo al tamaño de fuente raíz. Proporciona una escala consistente en toda la página. |
| **%** | Porcentaje del ancho del elemento padre. Útil para diseños fluidos y responsivos. |
| **auto** | Permite que el navegador calcule el valor automáticamente. Comúnmente usado para centrar horizontalmente elementos con márgenes izquierdo/derecho. |

Elija una unidad que se alinee con su intención — use `px` para espacios fijos, `rem` para espaciado escalable que respete los tokens de tipografía del tema y `%` para diseños que deben adaptarse al ancho del contenedor.

## Vincular Lados

Un **icono de enlace** en el centro del diagrama conmuta el modo de enlace:

- **Vinculado** (icono de cadena conectado) — Cambiar el valor de cualquier lado actualiza los cuatro lados al mismo valor. Útil para espaciado uniforme.
- **No vinculado** (icono de cadena roto) — Cada lado se controla de forma independiente. Use esto cuando necesite valores diferentes para arriba/abajo y izquierda/derecha.

Haga clic en el icono de enlace para alternar entre los modos. Cuando cambie de no vinculado a vinculado, los cuatro lados se establecen al valor del lado editado más recientemente.

## Preset Rápidos

Una fila de botones de configuración predeterminada debajo del diagrama proporciona configuraciones de espaciado con un solo clic:

| Preset | Valores |
|--------|--------|
| **Ninguno** | 0 en todos los lados |
| **Pequeño** | Espaciado compacto adecuado para diseños ajustados y elementos en línea |
| **Mediano** | Espaciado equilibrado para uso general en tarjetas y secciones |
| **Grande** | Espaciado generoso para áreas de héroe y secciones de alto énfasis |
| **XL** | Espaciado extra ancho para banners de ancho completo y secciones principales de la página |

Los presets se aplican a la pestaña activa (Márgen o Relleno) y establecen los cuatro lados a la vez. Después de aplicar un preset, puede ajustar los lados individuales según sea necesario.

## ¿Dónde aparece?

El editor de espaciado está disponible para cada elemento que admite el espaciado de diseño:

- **Constructor de Páginas** — Pestaña de Estilo, sección de Espaciado en secciones, contenedores, columnas y elementos individuales
- **Constructor de Encabezado/Pie de Página** — Controles de espaciado de fila y widget para espaciado vertical y horizontal
- **Constructor de Menú** — Configuración de relleno de elementos del menú y márgen del contenedor

La misma interfaz del editor se usa en todos los lugares, asegurando una experiencia consistente en todos los constructores.

## Consejos

- Use valores de espaciado consistentes en todas sus páginas — elija 2-3 tamaños estándar y manténgase con ellos para un diseño limpio y profesional.
- Establezca el márgen en **auto** en izquierda y derecha para centrar horizontalmente un elemento de ancho fijo dentro de su elemento padre.
- Prefiera unidades `rem` para el espaciado si su tema usa tipografía responsiva, para que el espaciado se escale proporcionalmente con el tamaño del texto.
- Use el modo vinculado para establecer rápidamente un relleno uniforme, luego desvincule y ajuste los lados individuales si el contenido requiere espaciado asimétrico.
- Evite un relleno excesivo en dispositivos móviles — pruebe su espaciado en anchos de ventana estrechos para asegurarse de que el contenido no se comprima ni esté excesivamente relleno.
