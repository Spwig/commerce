---
title: Añadir un Producto
---

Esta guía te explica paso a paso cómo crear un nuevo producto en tu tienda. Los productos están organizados en varias pestañas — Información Básica, Medios, Precios, Inventario y SEO — para que puedas completar todo de una sola vez o volver más tarde a rellenar las secciones pendientes.

## Primeros Pasos

Desde la barra lateral, navega a **Productos > Todos los Productos** para ver tu catálogo de productos. Haz clic en el botón **+ Añadir Producto** en la esquina superior derecha para abrir el formulario de creación de producto.

![Página de listado de productos](/static/core/admin/img/help/add-product/product-list-page.webp)

## Pestaña de Información Básica

La pestaña **Información Básica** es donde defines los datos principales de tu producto.

![Formulario de añadir producto](/static/core/admin/img/help/add-product/add-product-form.webp)

### Campos Obligatorios

- **Nombre** — El nombre del producto que verán los clientes. Haz clic en el icono del globo para añadir traducciones a otros idiomas.
- **Slug** — Versión del nombre adaptada para URLs (se genera automáticamente). Desactiva "Auto" para personalizarlo.
- **SKU** — Tu código interno de referencia de inventario.
- **Tipo de Producto** — Elige entre: Simple, Variable, Digital, Pack, Tarjeta Regalo, Personalizable o Configurable.
- **Estado** — Establécelo como Borrador mientras trabajas y cámbialo a Publicado cuando esté listo.

### Campos Opcionales

- **Categoría** — Asigna el producto a una categoría para organizarlo y facilitar la navegación en la tienda.
- **Marca** — Asocia el producto a una marca si corresponde.
- **Es Destacado** — Marca esta opción para resaltar este producto en tu tienda.
- **Es Producto Digital** — Marca esta opción si el producto incluye descargas digitales (archivos, licencias).
- **Ocultar de la Tienda** — Oculta el producto de los listados del catálogo, manteniéndolo disponible como opción de configurador o componente de pack.

### Descripciones del Producto

- **Descripción Corta** — Aparece en los listados y tarjetas de producto. Mantenla breve y atractiva.
- **Descripción Completa** — Descripción detallada del producto que se muestra en la página de detalle del producto. Utiliza el editor de texto enriquecido para añadir formato, imágenes, vídeos y tablas.

Ambos campos de descripción son compatibles con la función de traducción — haz clic en el icono del globo para proporcionar el contenido en otros idiomas.

## Pestaña de Medios

La pestaña **Medios** te permite gestionar las imágenes del producto mediante la Biblioteca de Medios integrada.

![Pestaña de medios](/static/core/admin/img/help/add-product/media-tab.webp)

1. Haz clic en **+ Añadir Imágenes desde la Biblioteca de Medios** para abrir el selector de medios.
2. Selecciona imágenes existentes o sube nuevas directamente.
3. Arrastra las imágenes para reordenarlas — la **primera imagen** se convierte en la imagen principal del producto, mostrada en los listados y tarjetas.
4. Elige un **Tipo de Galería** para controlar cómo se muestran las imágenes en la página del producto: Galería Estándar, Carrusel, Cuadrícula, Galería con Zoom o Vista 360°.

## Pestaña de Precios

Configura los precios de tu producto y las ofertas.

![Pestaña de precios](/static/core/admin/img/help/add-product/pricing-tab.webp)

### Precio Regular

- **Precio Regular** — El precio de venta estándar que verán los clientes.
- **Moneda** — Selecciona la moneda (la moneda predeterminada de tu tienda está preseleccionada).
- **Coste** — Tu coste de adquisición, utilizado para calcular beneficios. Nunca se muestra a los clientes.

### Configuración de Ofertas

Configura descuentos temporales:

- **Tipo de Oferta** — Elige entre: Sin Oferta, Precio de Oferta Fijo, Descuento por Cantidad o Descuento por Porcentaje.
- **Valor de la Oferta** — El importe o porcentaje del descuento.
- **Fechas de Inicio/Fin** — Programa cuándo se activa y cuándo expira la oferta. Déjalas vacías para que comience de inmediato o no tenga fecha de finalización.

## Pestaña de Inventario

Gestiona los niveles de stock y los atributos físicos del producto.

![Pestaña de inventario](/static/core/admin/img/help/add-product/inventory-tab.webp)

### Gestión de Stock

- **Seguimiento de Inventario** — Actívalo para controlar las cantidades en stock (activado por defecto).
- **Umbral de Stock Bajo** — Recibe alertas cuando el stock caiga por debajo de este número (por defecto: 5).
- **Cantidad en Stock** — Unidades totales disponibles.
- **Permitir Reservas** — Actívalo para aceptar pedidos incluso cuando no haya stock disponible.

### Atributos Físicos

Introduce el peso del producto (kg) y sus dimensiones (largo, ancho y alto en cm) para calcular correctamente los costes de envío.

### Identificadores del Producto

Códigos estándar del producto para listados en marketplaces y sistemas de inventario:

- **GTIN** — Número Global de Artículo Comercial
- **EAN** — Número de Artículo Europeo
- **UPC** — Código Universal de Producto (EE. UU.)
- **ISBN** — Para libros
- **ASIN** — Identificador de Amazon
- **MPN** — Número de Pieza del Fabricante

### Envío Internacional / Aduanas

Obligatorio para envíos internacionales:

- **Código HS** — Código de clasificación del Sistema Armonizado
- **País de Origen** — Dónde se fabrica el producto
- **Precio Unitario para Aduanas** — Valor declarado por unidad para aduanas

## Pestaña de SEO

Optimiza la visibilidad de tu producto en los motores de búsqueda.

![Pestaña de SEO](/static/core/admin/img/help/add-product/seo-tab.webp)

- **Meta Título** — El título que se muestra en los resultados de los motores de búsqueda. Haz clic en el icono del globo para traducirlo.
- **Meta Descripción** — Una breve descripción para los resultados de búsqueda (máximo 160 caracteres). Haz clic en el icono del globo para traducirla.
- **Generar SEO Automáticamente** — Marca esta opción para generar automáticamente el contenido SEO cuando se guarde el producto.

Una **Vista Previa del Resultado de Búsqueda** en tiempo real muestra exactamente cómo aparecerá tu producto en los resultados de Google.

## Guardar tu Producto

Cuando estés listo, utiliza los botones de guardado en la esquina superior derecha:

- **Guardar** (marca de verificación) — Guarda y permanece en la página del producto.
- **Guardar y continuar editando** — Guarda y permanece en el formulario para seguir trabajando.

Tu producto será visible en la tienda una vez que su estado esté configurado como **Publicado**.

## Consejos

- Comienza con el estado **Borrador** para que puedas perfeccionar el producto antes de que los clientes lo vean.
- Sube varias imágenes — los productos con varias fotos generan más conversiones.
- Rellena los campos de **SEO** para mejorar la visibilidad en los motores de búsqueda.
- Utiliza **Categorías** y **Marcas** para ayudar a los clientes a navegar por tu catálogo.
- Para productos variables (por ejemplo, diferentes tallas o colores), elige el tipo **Producto Variable** y añade las variantes después de guardar.
