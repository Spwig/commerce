---
title: Biblioteca de medios
---

La Biblioteca de medios es el centro de gestión de todas las imágenes, videos, modelos 3D y archivos utilizados en su tienda. Cargue archivos arrastrándolos, organice con carpetas y etiquetas, y permita que el sistema optimice automáticamente las imágenes para una carga rápida.

![Galería de medios](/static/core/admin/img/help/media-library/media-gallery.webp)

## Interfaz de la Galería

Navegue hasta **Biblioteca de medios** en el menú lateral para abrir la galería. La interfaz tiene tres áreas:

| Área | Ubicación | Propósito |
|------|----------|---------|
| **Zona de carga** | Lado izquierdo, parte superior | Arrastrar y soltar archivos para cargar (imágenes, videos, modelos 3D hasta 100 MB) |
| **Carpetas y etiquetas** | Lado izquierdo, debajo | Explorar carpetas, filtrar por etiquetas, acceder al Reciclaje |
| **Cuadrícula de medios** | Área principal | Buscar, filtrar, explorar y gestionar todos sus activos |

### Controles de la Barra de Herramientas

La barra de herramientas encima de la cuadrícula de medios proporciona:

- **Búsqueda** — encontrar activos por título, texto alternativo, descripción o nombre de etiqueta
- **Filtro de tipo** — mostrar solo Imágenes, Videos o Modelos 3D
- **Filtro de tamaño** — filtrar por tamaño de archivo (Pequeño, Mediano, Grande)
- **Acciones en bloque** — Seleccionar elementos, Editar detalles, Eliminar seleccionados
- **Modos de visualización** — Cuadrícula (grande), Cuadrícula pequeña o Vista de lista (persistente en sesiones)

## Carga de Archivos

Arrastre uno o más archivos a la zona de **Carga** en el menú lateral izquierdo, o haga clic en la zona para abrir un selector de archivos.

### Formatos Soportados

| Tipo | Formatos |
|------|---------|
| **Imágenes** | JPEG, PNG, GIF, WebP, SVG, BMP, TIFF |
| **Videos** | MP4, WebM, MOV, MKV, AVI |
| **Modelos 3D** | GLB, glTF |

### Cola de Carga

Cuando carga varios archivos, aparece un administrador de cola que muestra:

- El nombre de cada archivo y la barra de progreso de carga
- Cargas concurrentes (hasta 2 a la vez para el rendimiento)
- Estado de procesamiento a medida que los archivos se optimizan después de la carga
- Opción para cancelar cargas individuales o limpiar los elementos completados

La cola es arrastrable y se puede minimizar para que pueda continuar trabajando mientras se completan las cargas.

## Optimización Automática de Imágenes

Toda imagen que carga se optimiza automáticamente:

- **Conversión a WebP** — se genera una versión en WebP junto con la original (calidad 85%) para una carga más rápida
- **Generación de miniaturas** — se crean varias versiones de tamaño basadas en sus configuraciones predeterminadas de imagen
- **Orientación EXIF** — las imágenes se rotan automáticamente a la orientación correcta

### Configuraciones Predeterminadas del Sistema

La plataforma incluye 21 configuraciones predeterminadas integradas que cubren casos de uso comunes:

| Configuración | Dimensiones | Recorte | Usado para |
|--------|-----------|------|---------|
| **Miniatura** | 150 x 150 | Cubrir | Listas de administración, previzualizaciones rápidas |
| **Pequeño** | 300 x 300 | Cubrir | Tarjetas de productos pequeñas |
| **Mediano** | 600 x 600 | Contener | Tarjetas de productos, miniaturas de blogs |
| **Grande** | 1200 x 1200 | Contener | Páginas de detalles del producto |
| **Galería** | 800 x 800 | Contener | Galerías de imágenes |
| **Hero** | 1920 x 1080 | Cubrir | Secciones hero, banners de páginas |
| **Banner** | 1200 x 400 | Cubrir | Banners de promoción |
| **Tarjeta** | 400 x 300 | Cubrir | Tarjetas de características, tarjetas de contenido |
| **Avatar** | 200 x 200 | Recortar | Avatares de clientes y empleados |
| **Lista de productos** | 400 x 400 | Cubrir | Tarjetas de la cuadrícula de productos |
| **Detalle del producto** | 1200 x 1200 | Cubrir | Imágenes completas del producto |
| **Miniatura del producto** | 100 x 100 | Cubrir | Selectores de variantes, carritos mini |
| **Banner de categoría** | 1920 x 480 | Cubrir | Encabezados de páginas de categoría |
| **Miniatura de categoría** | 300 x 200 | Cubrir | Tarjetas de categoría |
| **Logo de encabezado** | 300 x 80 | Ajustar | Logo del encabezado del sitio |
| **Logo de pie de página** | 200 x 60 | Ajustar | Logo del pie de página del sitio |
| **Logo de correo electrónico** | 400 x 100 | Ajustar | Logos de plantillas de correo electrónico |
| **Logo cuadrado** | 160 x 160 | Ajustar | Ubicaciones de logos cuadrados |
| **Logo de marca** | 200 x 100 | Ajustar | Logos de marcas/patrocinadores |
| **Banner de anuncio** | 800 x 300 | Cubrir | Imágenes de anuncios |
| **Fondo de anuncio** | 1200 x 800 | Cubrir | Fondos de anuncios |

Las configuraciones predeterminadas del sistema no se pueden renombrar ni eliminar. Puede crear configuraciones personalizadas adicionales bajo **Biblioteca de medios > Configuraciones de tamaño de imagen** si necesita tamaños no cubiertos por las predeterminadas.

### Modos de Recorte

| Modo | Comportamiento |
|------|----------|
| **Cubrir** | Llena todo el área, recortando los bordes si es necesario — ideal para tarjetas y banners |
| **Contener** | Ajusta la imagen completa dentro del área, añadiendo espacio transparente si es necesario — ideal para imágenes de productos |
| **Recortar** | Recorta al centro exactamente a las dimensiones especificadas |
| **Ajustar** | Ajusta la imagen y añade relleno (transparente, blanco o negro) — ideal para logos |

## Organización de Archivos

### Carpetas

Cree carpetas para organizar sus medios en grupos lógicos. Las carpetas pueden anidarse a cualquier profundidad. Haga clic en una carpeta en el menú lateral izquierdo para mostrar solo los activos dentro de ella. El enlace **Todos los archivos** muestra todo.

### Etiquetas

Agregue etiquetas a los activos para una organización flexible entre carpetas. Las etiquetas aparecen en la nube en el menú lateral izquierdo. Haga clic en una etiqueta para filtrar activos por esa etiqueta. Los activos pueden tener múltiples etiquetas.

### Búsqueda

La barra de búsqueda encuentra activos por título, texto alternativo, descripción o nombre de etiqueta. Combine la búsqueda con filtros de tipo y tamaño para resultados precisos.

## Detalles del Activo

Haga clic en un activo para abrir su vista de detalles con una vista previa grande y metadatos completos.

![Detalles del Activo](/static/core/admin/img/help/media-library/media-detail.webp)

La vista de detalles muestra:

- **Vista previa** — vista previa de imagen grande con las dimensiones originales
- **Información del archivo** — tipo, dimensiones, tamaño del archivo, fecha de carga
- **Pestañas** para edición:

| Pestaña | Campos |
|-----|--------|
| **General** | Título, Texto alternativo, Descripción (todo traducible para tiendas multilingües) |
| **Técnica** | Tipo MIME, hash del archivo, nombre de archivo original, estado de la versión WebP |
| **Organización** | Asignación de carpeta, etiquetas, conmutador público/privado |
| **Avanzado** | Coordenadas del punto focal, ID externo, JSON de metadatos |

### Campos Traducibles

El título, el texto alternativo y la descripción admiten traducciones. Haga clic en el icono de traducción junto a cada campo para agregar traducciones para los idiomas habilitados. Esto asegura que las imágenes tengan texto alternativo y descripciones localizadas correctamente para SEO y accesibilidad.

### Seguimiento de Uso

El sistema registra dónde se usa cada activo en toda la plataforma. La sección **Usos de medios** en la parte inferior muestra cada modelo y campo que hace referencia a este activo, lo que le ayuda a comprender el impacto antes de realizar cambios o eliminarlo.

## Soporte de Video

Los videos cargados en la biblioteca de medios se analizan automáticamente:

- **Extracción de metadatos** — se capturan la duración, resolución, tasa de fotogramas, bitrate y códigos de códec
- **Imagen de portada** — se genera una miniatura del video para la vista previa
- **Transmisión** — los videos admiten solicitudes de rango para buscar sin descargar el archivo completo
- **Conversión opcional** — los videos pueden convertirse a formatos optimizados WebM/AV1 para una entrega más rápida

## Papelera de Reciclaje

Eliminar un activo lo mueve a la **Papelera de Reciclaje** en lugar de eliminarlo permanentemente. Esto protege contra eliminaciones accidentales.

| Acción | Qué hace |
|--------|-------------|
| **Eliminar** | Mueve el activo a la Papelera de Reciclaje (eliminación suave) |
| **Restaurar** | Devuelve un activo eliminado a su ubicación original |
| **Eliminar permanentemente** | Elimina el activo y todas sus miniaturas del almacenamiento de forma permanente |
| **Vaciar la Papelera de Reciclaje** | Elimina permanentemente todos los elementos en la Papelera de Reciclaje |

Haga clic en **Papelera de Reciclaje** en el menú lateral izquierdo para ver y gestionar los activos eliminados.

## Dónde se Utiliza la Biblioteca de Medios

La biblioteca de medios está integrada en toda la plataforma:

| Función | Cómo utiliza los medios |
|---------|------------------|
| **Catálogo de productos** | Imágenes de productos, imágenes de variantes, banners de categorías |
| **Blog** | Imágenes destacadas, imágenes en contenido a través de CKEditor |
| **Constructor de páginas** | Elementos de imagen, fondos de hero, componentes de galería |
| **Constructor de encabezado/pie de página** | Imágenes de logotipo, imágenes de fondo |
| **Configuraciones del sitio** | Logotipo del sitio y favicon |
| **Anuncios** | Imágenes de anuncios y fondos de anuncios |
| **CKEditor** | Todas las subidas de imágenes en texto enriquecido pasan por la biblioteca de medios |
| **Programa de fidelidad** | Imágenes de recompensas y niveles |

Cuando selecciona una imagen en cualquiera de estas funciones, la galería de la biblioteca de medios se abre como un modal para una navegación y selección fáciles.

## Consejos

- **Use títulos y texto alternativo descriptivos** — una buena metadatos mejora el SEO y la accesibilidad. El sistema usa el texto alternativo en las etiquetas de imagen en toda la tienda.
- **Organice con carpetas desde el principio** — cree una estructura de carpetas (por ejemplo, Productos, Blog, Banners, Logos) antes de cargar muchos archivos. Es mucho más fácil organizar mientras va cargando que reorganizar más tarde.
- **Use etiquetas para categorías transversales** — etiquetas como "estacional", "venta" o "estilo de vida" le ayudan a encontrar activos que abarcan múltiples carpetas.
- **Revise el uso antes de eliminar** — la sección de seguimiento de uso muestra dónde se referencia un activo. Eliminar un activo usado puede dejar imágenes rotas en su tienda.
- **Deje que WebP haga el trabajo** — la conversión automática a WebP reduce normalmente el tamaño de los archivos en un 25-35% en comparación con JPEG sin pérdida visible de calidad. No necesita convertir manualmente las imágenes antes de cargar.
- **Cree configuraciones personalizadas** — si tiene un diseño único que requiere un tamaño de imagen específico, cree una configuración personalizada en lugar de redimensionar manualmente las imágenes.