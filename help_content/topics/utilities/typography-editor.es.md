---
title: Editor de Tipografía
---

El Editor de Tipografía es una herramienta de estilo compartida que le da un control total sobre la apariencia del texto. Se abre como un panel flotante siempre que edite propiedades de tipografía en cualquier elemento dentro del Page Builder, Header/Footer Builder o Menu Builder.

![Editor de Tipografía](/static/core/admin/img/help/typography-editor/typography-editor.webp)

## Vista previa en vivo

El editor muestra una comparación lado a lado en la parte superior del panel:

| Caja | Propósito |
|-----|---------|
| **Actual** | Muestra "The quick brown fox..." en el estilo de tipografía existente |
| **Nueva** | Se actualiza en tiempo real a medida que ajusta los ajustes, mostrando el resultado antes de aplicar |

Esto le permite comparar antes y después sin comprometerse con ningún cambio.

## Pestaña Fuente

La pestaña Fuente es la vista predeterminada cuando el editor se abre.

**Familia de Fuente** — Un menú desplegable buscable con 70+ fuentes organizadas por categoría. Cada fuente se previsualiza en su propia tipografía para que pueda ver cómo se ve antes de seleccionarla. Las fuentes se cargan según sea necesario desde Google Fonts cuando sea necesario.

**Tamaño de Fuente** — Entrada numérica con un selector de unidad que admite px, em, rem y %. El valor predeterminado es 16px.

**Peso de Fuente** — Un deslizador desde 100 (Delgado) hasta 900 (Negro):

| Valor | Nombre |
|-------|------|
| 100 | Delgado |
| 200 | Extra Delgado |
| 300 | Delgado |
| 400 | Regular |
| 500 | Medio |
| 600 | Semi Negrita |
| 700 | Negrita |
| 800 | Extra Negrita |
| 900 | Negro |

No todas las fuentes admiten los nueve pesos. El editor muestra cuáles pesos están disponibles para la familia de fuentes seleccionada.

**Estilo de Fuente** — Botones de conmutación para Normal, Itálico y Oblicuo.

## Pestaña Espaciado

Ajuste finamente el espacio alrededor y entre los caracteres:

| Control | Qué hace | Valor predeterminado |
|---------|-------------|---------|
| **Altura de línea** | Espacio vertical entre líneas de texto | normal |
| **Espaciado de letras** | Espacio horizontal entre caracteres individuales | normal |
| **Espaciado de palabras** | Espacio horizontal entre palabras | normal |
| **Sangría de texto** | Sangría de la primera línea en un párrafo | 0 |

Cada control de espaciado incluye un selector de unidad (px, em, rem, %).

## Pestaña Estilo

Controlar decoración del texto y efectos visuales:

- **Decoración de texto** — Ninguna, Subrayado, Línea superior o Línea a través
- **Estilo de decoración** — Sólido, Rayado, Punteado, Doble o Ondulado (se aplica cuando una decoración está activa)
- **Color de decoración** — Selector de color para la línea de decoración, por defecto es el color del texto
- **Sombra de texto** — Efecto de sombra opcional con controles de desplazamiento, desenfoque y color

## Pestaña Transformar

Cambie la capitalización del texto sin editar el contenido:

| Opción | Resultado |
|--------|--------|
| **Ninguna** | El texto aparece como está escrito |
| **Mayúsculas** | TODAS LAS LETRAS ESTÁN MAYÚSCULAS |
| **Minúsculas** | todas las letras son minúsculas |
| **Capitalizar** | La primera letra de cada palabra está capitalizada |

Controles adicionales en esta pestaña incluyen **Alineación de texto** (izquierda, centrada, derecha, justificada), **Alineación vertical** y **Dirección del texto** (LTR o RTL).

## Familias de Fuente Disponibles

El editor incluye una biblioteca curada de fuentes del sistema y Google Fonts, agrupadas por categoría:

| Categoría | Tipografías
|----------|-------
| **Sistema** | Predeterminado del sistema, Arial, Helvetica Neue, Helvetica, Segoe UI, Roboto, Ubuntu, Verdana, Tahoma, Trebuchet MS
| **Sin serifa (Moderno)** | Inter, Montserrat, Poppins, DM Sans, Space Grotesk, Plus Jakarta Sans, Outfit, Manrope, Figtree, Josefin Sans
| **Sin serifa (Clásico)** | Open Sans, Lato, Nunito, Nunito Sans, Source Sans 3, Raleway, Rubik, Work Sans, Mulish, Cabin, Karla, Barlow, Lexend
| **Con serifa** | Playfair Display, Merriweather, Lora, Libre Baskerville, Cormorant Garamond, Source Serif 4, EB Garamond, Crimson Pro, Bitter, Fraunces, Spectral, Cardo, Alegreya
| **Con serifa (Sistema)** | Georgia, Times New Roman, Palatino, Book Antiqua, Garamond, Cambria
| **Monoespaciado** | Source Code Pro, Fira Code, JetBrains Mono, Roboto Mono, IBM Plex Mono, Space Mono, Inconsolata, Consolas, Monaco, Menlo, Courier New, SF Mono
| **Visual** | Oswald, Bebas Neue, Anton, Archivo Black, Rajdhani, Righteous, Abril Fatface, Archivo, Impact, Arial Black

Las fuentes de Google se cargan automáticamente al seleccionarlas. Las fuentes del sistema utilizan cadenas de retroceso CSS adecuadas para un renderizado confiable en diferentes plataformas.

## ¿Dónde aparece

El Editor de Tipografía está disponible en todos los lugares donde se necesite el estilo del texto:

- **Constructor de páginas** — Seleccione cualquier elemento, abra la pestaña Estilo y haga clic en la sección Tipografía
- **Constructor de encabezado/pie de página** — Estilice el texto en enlaces de navegación, texto del logotipo, elementos del menú y contenido del pie de página
- **Constructor de menú** — Controlar la tipografía para etiquetas de menú y elementos de submenú
- **Administración del catálogo** — Se usa en descripciones de productos y editores de contenido donde se exponen los controles de tipografía

El editor siempre se accede a través de la misma interfaz consistente, independientemente del contexto.

## Consejos

- **Combine fuentes intencionalmente** — use una fuente visual o con serifa para títulos y una sin serifa limpia para el texto principal. Combinaciones clásicas como Playfair Display + Inter o Montserrat + Merriweather funcionan bien.
- **Límite las familias de fuentes por página** — dos o tres familias de fuentes por página suelen ser suficientes. Más de eso puede ralentizar los tiempos de carga y crear un desorden visual.
- **Use unidades relativas para texto responsivo** — em y rem se escalan con el tamaño de fuente base, lo que hace que su tipografía se adapte automáticamente a diferentes tamaños de pantalla.
- **Verifique la disponibilidad de peso** — si el texto parece lo mismo en 400 y 500, la fuente seleccionada puede no admitir ese peso. El editor indica qué pesos proporciona cada fuente.
- **Pruebe en todos los dispositivos** — el texto que parece bueno en tamaños de escritorio puede ser demasiado pequeño o demasiado grande en móviles. Use la vista previa de dispositivos del Constructor de páginas para verificar.
- **Use la vista previa en vivo** — siempre compare Current vs New en las cajas de vista previa antes de aplicar para evitar cambios inesperados.