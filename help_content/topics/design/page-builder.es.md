---
title: Page Builder
---

El Page Builder es un editor visual de arrastrar y soltar para crear páginas ricas y responsivas sin necesidad de escribir código. Añade elementos de una biblioteca de 39 componentes, dale estilo con poderosas utilidades, establece animaciones y reglas de visibilidad, y publica con un historial completo de versiones.

![Page Builder](/static/core/admin/img/help/page-builder/builder-overview.webp)

## La Interfaz del Editor

El editor tiene cuatro áreas principales:

| Área | Ubicación | Propósito |
|------|----------|---------|
| **Barra de herramientas** | Barra superior | Vista previa del dispositivo (escritorio/tableta/móvil), deshacer/rehacer, ajustes de la página, guardar borrador, publicar |
| **Biblioteca de elementos** | Barra lateral izquierda | Explorar y arrastrar 39 elementos organizados en 9 categorías |
| **Canvas** | Centro | Área de edición WYSIWYG en vivo — ve los cambios mientras los haces |
| **Panel de propiedades** | Barra lateral derecha | Editar el contenido, estilo, animaciones y ajustes avanzados del elemento seleccionado |

## Biblioteca de Elementos

Los elementos están organizados en categorías. Arrastra cualquier elemento de la biblioteca al canvas para añadirlo a tu página.

| Categoría | Elementos |
|----------|----------|
| **Diseño** | Contenedor, Divisor, Sección Hero, Pop-up de Modal, Menú de Navegación, Espaciador |
| **Básico** | Encabezado, Texto, Botón, Icono |
| **Contenido** | Carrusel de Entradas de Blog, Cuadrícula de Entradas de Blog, Acordion de Preguntas Frecuentes, Entradas Relacionadas, Testimonios |
| **Multimedia** | Imagen, Galería de Imágenes, Acordion de Imágenes, Incrustación de Video |
| **Formularios** | Formulario de Contacto, Formulario, Suscripción al Boletín |
| **Marketing** | Cronómetro de Conteo, Banderín de CTA, Banderín de Entrada Destacada, Banderín de Lealtad, Banderín de Promoción, Sellos de Confianza, Visualización de Códigos de Cupón |
| **E-commerce** | Muestra de Categoría, Promoción de Tarjeta Regalo, Carrusel de Productos, Cuadrícula de Productos, Lista de Productos, Visualización de Reseñas, Productos en Oferta, Localizador de Tienda |
| **Social** | Enlaces Sociales |
| **Navegación** | Barra de Búsqueda |

### Contenedores y Anidación

El elemento **Contenedor** es la base para diseños complejos. Los contenedores pueden contener otros elementos — incluyendo otros contenedores — lo que te permite construir cuadrículas de múltiples columnas y estructuras anidadas. Usa los ajustes de diseño del contenedor para configurar rápidamente disposiciones de columnas comunes (50/50, 33/33/33, 25/75, etc.).

## Añadiendo Elementos

1. Encuentra el elemento que deseas en la barra lateral izquierda
2. **Arrástralo** al canvas y suéltilo donde lo desees
3. Los elementos pueden colocarse entre elementos existentes o dentro de contenedores
4. La línea de inserción azul muestra dónde caerá el elemento
5. Después de soltar, el elemento se selecciona automáticamente y se abre el panel de propiedades

También puedes reordenar elementos arrastrándolos hacia arriba o hacia abajo en el canvas.

## Editando Contenido

Selecciona cualquier elemento en el canvas para abrir sus propiedades en el panel derecho. La pestaña **Contenido** muestra campos específicos para ese tipo de elemento.

![Panel de Propiedades](/static/core/admin/img/help/page-builder/properties-panel.webp)

Por ejemplo:
- **Encabezado** — texto, etiqueta HTML (H1–H6), alineación, ID de anclaje
- **Imagen** — fuente de imagen (biblioteca de medios), texto alternativo, enlace, tamaño
- **Botón** — etiqueta, URL, variante de estilo, icono
- **Cuadrícula de Productos** — fuente de datos, número de columnas, productos por página, orden de clasificación
- **Sección Hero** — título, subtítulo, descripción, fondo, botones de llamada a la acción

Los campos de contenido traducibles muestran un icono de traducción — haz clic en él para agregar traducciones para tiendas multilingües.

## Estilizando Elementos

La pestaña **Estilo** proporciona controles visuales para cada elemento. Cada sección abre un editor de utilidades dedicado.

![Pestaña de Estilo](/static/core/admin/img/help/page-builder/style-tab.webp)

| Sección | Qué Controla | Utilidad |
|---------|-----------------|---------|
| **Tipografía** | Familia de fuentes, tamaño, peso, altura de línea, espaciado entre letras, estilo del texto | Editor de Tipografía |
| **Colores** | Color del texto con entrada de hex/RGB/HSL y tokens de tema | Selector de Color |
| **Fondo** | Color sólido, degradado, imagen o video con estados de hover | Editor de Fondo |
| **Borde** | Ancho, estilo, color y radio del borde por lado | Editor de Borde |
| **Espaciado** | Márgenes y relleno con editor de modelo de caja visual | Editor de Espaciado |
| **Efectos** | Sombra de caja con ajustes preestablecidos y soporte de capas múltiples, deslizador de opacidad | Editor de Sombra |

Cada utilidad está documentada en su propio tema de ayuda — busca "selector de color", "editor de fondo", etc. para obtener más información.

## Animaciones

La pestaña **Animaciones** te permite agregar movimiento a los elementos.

### Animaciones de Entrada

Se activan cuando el elemento entra en vista al desplazarse:

| Animación | Descripción |
|-----------|-------------|
| Fade In | Aparece gradualmente |
| Slide In (Up/Down/Left/Right) | Se desliza desde una dirección |
| Zoom In | Se expande desde un tamaño pequeño hasta el tamaño completo |
| Bounce In | Se mueve hacia su lugar con un rebote |
| Pulse / Shake / Bounce / Flash / Spin | Efectos para llamar la atención |

Configura **duración** (0.3s–1.5s), **retraso** (0–1s), **función de temporización** (ease, ease-in, ease-out, linear) y **repetición** (una vez o infinita).

### Animaciones de Hover

Se activan cuando un visitante pasa el ratón sobre el elemento:

| Efecto | Descripción |
|--------|-------------|
| Escalar hacia arriba / Escalar hacia abajo | Se expande o se reduce |
| Levantar | Flota hacia arriba |
| Rotar (en sentido horario / antihorario) | Gira en sentido horario o antihorario |
| Aumentar brillo / Desvanecer | Cambia el brillo o la opacidad |
| Sombra creciente | La sombra se expande |
| Levantar con sombra | Se eleva con una sombra creciente |
| Escalar de pulso / Inclinación / Brillo de borde | Efectos especiales |

Configura **duración**, **temporización** y **intensidad** (sutil, normal, fuerte).

## Ajustes Avanzados

La pestaña **Avanzado** proporciona un control detallado:

### Reglas de Visibilidad

Controla cuándo se muestra o oculta un elemento según condiciones:

- **Estado del usuario** — iniciado sesión, no iniciado sesión, nuevo cliente, cliente recurrente
- **Dispositivo** — escritorio, tableta, móvil
- **Tiempo** — rango de fechas, hora del día, día de la semana
- **Grupo de clientes** — VIP, mayorista, etc.
- **Valor del carrito** — total mínimo o máximo del carrito
- **Geografía** — país, región
- Y más de 20 tipos de reglas

Las reglas se pueden combinar con lógica AND/OR para un objetivo de targeting complejo.

### CSS Personalizado

| Campo | Propósito |
|-------|---------|
| **ID del elemento** | ID único para enlaces de anclaje o targeting CSS |
| **Clases CSS personalizadas** | Clases adicionales para aplicar |
| **Estilos CSS personalizados** | CSS en línea para sobrescribires específicas |
| **Atributos de datos** | Atributos de datos personalizados como pares clave-valor |
| **Z-Index** | Orden de superposición para elementos superpuestos |

## Flujo de Trabajo de Publicación

Las páginas utilizan un sistema de borrador/publicación con historial completo de versiones:

| Estado | Significado |
|--------|---------|
| **Borrador** | Trabajo en progreso — no visible para los visitantes |
| **Publicado** | Activo en tu tienda |
| **Archivado** | Eliminado del sitio pero conservado |

### Cómo Funciona

1. Haz cambios en el editor — se guardan como un **borrador**
2. Haz clic en **Guardar Borrador** para guardar sin publicar
3. Haz clic en **Publicar** para hacer el borrador actual activo
4. Cada publicación crea una **instantánea de versión**
5. Puedes **restaurar** cualquier versión anterior desde el historial de versiones (icono del reloj en la barra de herramientas)

Esto significa que puedes experimentar libremente — tu página activa permanece sin cambios hasta que publiques explícitamente.

## Plantillas de Página

Ahorra tiempo trabajando con plantillas:

- **Guardar como plantilla** — guarda el diseño de cualquier página como una plantilla reutilizable
- **Crear desde plantilla** — inicia una nueva página desde una plantilla existente
- **Categorías de plantillas** — organiza las plantillas según su propósito (página de aterrizaje, sobre nosotros, exhibición de productos, etc.)

Las plantillas capturan la estructura completa de la página, incluyendo todos los elementos, contenido y estilos.

## Diseño Responsivo

Usa los botones de vista previa del dispositivo en la barra de herramientas para ver cómo se ve tu página en diferentes tamaños de pantalla:

- **Escritorio** — diseño de ancho completo
- **Tablet** — vista previa de mediana
- **Móvil** — vista previa de ancho estrecho

Los elementos se reorganizan automáticamente según la configuración de su contenedor. También puedes usar reglas de visibilidad para mostrar o ocultar elementos específicos en ciertos dispositivos.

## Consejos

- **Empieza con un Contenedor** — la mayoría de los diseños comienzan con un contenedor para crear columnas y estructuras. Usa ajustes de diseño preestablecidos para disposiciones comunes.
- **Usa secciones Hero para encabezados de página** — el elemento Hero proporciona título, subtítulo, imagen de fondo y botones de llamada a la acción en un solo componente.
- **Vista previa antes de publicar** — haz clic en Vista previa para ver exactamente lo que verán los visitantes, luego publica cuando estés satisfecho.
- **Usa reglas de visibilidad para personalización** — muestra contenido diferente a visitantes iniciados o no iniciados, o dirige a grupos de clientes específicos.
- **Mantén las animaciones sutiles** — una o dos animaciones de entrada por sección de página parecen profesionales. Demasiadas animaciones pueden resultar abrumadoras.
- **Nombra tus contenedores** — usa el campo ID del elemento para etiquetar contenedores (por ejemplo, "hero-section", "features") para que sean fáciles de encontrar en páginas complejas.
- **Prueba en todos los dispositivos** — usa la vista previa del dispositivo para verificar tu diseño en escritorio, tableta y móvil antes de publicar.
- **Aprovecha las plantillas** — guarda tus mejores diseños de página como plantillas para acelerar la creación de páginas futuras.