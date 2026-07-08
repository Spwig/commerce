---
title: Editor de Fondo
---

El editor de fondo te da un control completo sobre los fondos de los elementos con cuatro tipos: color sólido, degradado, imagen y video. También admite estados independientes de **Normal** y **Hover** para que puedas crear efectos visuales interactivos. Abre la pestaña **Estilo** de cualquier elemento y busca la sección **Fondo** para acceder al editor.

![Editor de Fondo](/static/core/admin/img/help/background-editor/background-editor.webp)

## Estados Normal y Hover

En la parte superior del editor de fondo, un interruptor cambia entre los estados **Normal** y **Hover**. Cada estado tiene su propia configuración de fondo independiente:

- **Normal** — El fondo predeterminado que se muestra cuando se carga la página
- **Hover** — El fondo aplicado cuando un visitante mueve el cursor sobre el elemento

Dos bloques de vista previa pequeños junto al interruptor muestran los fondos de **Normal** y **Hover** uno al lado del otro, para que puedas ver el contraste a simple vista. Configura el estado **Normal** primero, luego cambia a **Hover** para agregar un efecto interactivo si lo deseas.

## Tipos de Fondo

Selecciona un tipo de fondo desde la fila de iconos en la parte superior del panel del editor:

| Tipo | Descripción |
|------|-------------|
| **Color** | Un relleno sólido usando un solo valor de color. Fácil de aplicar y ligero. |
| **Degradado** | Una transición suave entre dos o más colores, ya sea lineal o radial. Incluye configuraciones predefinidas como Océano, Atardecer, Bosque y Baya. Para edición avanzada de degradados, consulta el tema [Creador de Degradados](gradient-creator). |
| **Imagen** | Una imagen subida o seleccionada de la biblioteca de medios. Admite control de posición, tamaño y repetición. |
| **Video** | Una URL de video de fondo con una imagen de presentación opcional que se muestra mientras se carga el video o en dispositivos móviles. |

Solo puede estar activo un tipo a la vez por estado. Cambiar de tipo no elimina tu configuración anterior — puedes volver a cambiar y tus ajustes se conservarán.

## Fondos de Color

Cuando se selecciona **Color**:

- **Entrada de Hex** — Escribe directamente un código hex (por ejemplo, `#1A1A2E`)
- **Muestras de Color** — Haz clic en una muestra predefinida para una selección rápida. Las muestras son conscientes del tema y reflejan el paleta del tema activo.
- **Botón de Edición** — Abre el selector de color completo con espectro, deslizadores y opciones de formato (ver el tema [Selector de Color](color-picker))

Los fondos de color se renderizan de inmediato y no tienen impacto en el rendimiento, lo que los hace ideales para secciones, tarjetas y contenedores.

## Fondos de Degradado

Cuando se selecciona **Degradado**:

- **Degradados Predefinidos** — Elige entre degradados integrados: Océano, Atardecer, Bosque, Baya y otros
- **Degradado Personalizado** — Haz clic en **Editar** para abrir el creador de degradados donde puedes establecer la dirección, el tipo (lineal o radial) y los puntos de color
- **Deslizador de Ángulo** — Ajusta la dirección del degradado para degradados lineales (0-360 grados)

Los degradados añaden profundidad visual sin requerir activos de imagen y se escalan perfectamente a cualquier tamaño de pantalla.

## Fondos de Imagen

Cuando se selecciona **Imagen**:

- **Subir o Biblioteca de Medios** — Haz clic en el marcador de posición de imagen para subir una nueva imagen o seleccionar una de tu biblioteca de medios
- **Tamaño** — Elige **Cubrir** (rellena el elemento, puede recortar), **Contener** (se ajusta dentro del elemento) o un tamaño personalizado
- **Posición** — Establece el punto focal usando una cuadrícula de 9 puntos (esquina superior izquierda, centro, esquina inferior derecha, etc.) o introduce porcentajes personalizados de X/Y
- **Repetir** — Activa o desactiva la repetición. Útil para patrones de teselado
- **Superposición** — Añade una superposición de color encima de la imagen con opacidad ajustable, útil para garantizar la legibilidad del texto

Optimiza siempre las imágenes antes de subirlas. Las imágenes grandes no comprimidas ralentizan los tiempos de carga de la página.

## Fondos de Video

Cuando se selecciona **Video**:

- **URL de Video** — Introduce una URL directa a un archivo de video MP4 o WebM
- **Imagen de Presentación** — Sube una imagen de respaldo que se muestra mientras se carga el video y en dispositivos que no reproducen automáticamente el video
- **Reproducción automática / Repetición / Silencio** — Los fondos de video se reproducen automáticamente, se repiten y están silenciados por defecto para cumplir con las políticas del navegador

Mantén los videos de fondo cortos (10-30 segundos), comprimidos y visualmente sutiles.

Deben mejorar la sección sin distraer del contenido.

## Where It Appears

El editor de fondo está disponible para cada elemento que admite fondos:

- **Page Builder** — Las secciones, contenedores, columnas e elementos individuales tienen una sección de Fondo en la pestaña Estilo
- **Header/Footer Builder** — Fondos de fila y fondos de widgets individuales
- **Menu Builder** — Fondos del contenedor de menú y paneles de despliegue

La misma interfaz del editor se usa en todos los lugares, por lo que tu flujo de trabajo permanece coherente en todos los constructores.

## Tips

- Usa un color semitransparente como capa superior en fondos de imágenes para asegurar que el texto siga siendo legible independientemente del contenido de la imagen.
- Los gradientes preestablecidos son una forma rápida de agregar interés visual — aplícalo, luego personaliza el ángulo o los colores para que coincidan con tu marca.
- Establece tanto el fondo Normal como el de Hover en tarjetas interactivas para dar a los visitantes una retroalimentación visual clara cuando exploren tu contenido.
- Para fondos de imágenes, siempre establece un punto focal para que la parte más importante de la imagen siga siendo visible en todos los tamaños de pantalla.
- Prefiere fondos de color o gradientes en lugar de imágenes para secciones donde la velocidad de carga es crítica, como el contenido por encima de la carpeta.
- Prueba fondos de video en dispositivos móviles — la mayoría de los navegadores móviles mostrarán la imagen de presentación en lugar de reproducir el video.