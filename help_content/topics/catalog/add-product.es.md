---
title: Agregar un producto
---

<!-- screenshots-needed:
- url: /admin/catalog/product/<id>/change/
  filename: inventory-tab.webp
  description: pestaña de inventario, desplazada para mostrar las tarjetas de atributos físicos, envío,
    y pre-venta juntas (con la casilla de "Requiere envío" marcada, un paquete de envío preferido
    seleccionado y la casilla de "Pre-venta" marcada con una fecha y mensaje de lanzamiento
    completados, de modo que todos los nuevos campos sean visibles de un vistazo).
  save-to: core/static/core/admin/img/help/add-product/
  viewport: 1440x900
  notes: Reemplaza a la imagen inventory-tab.webp existente, que data de antes de las tarjetas
    de envío y pre-venta y ya no coincide con el formulario en vivo.
- url: /admin/catalog/product/<id>/change/
  filename: tags-card.webp
  description: pestaña de Información básica, desplazada hacia la tarjeta de Etiquetas, con un par de etiquetas
    ya aplicadas al producto en el selector de etiquetas.
  save-to: core/static/core/admin/img/help/add-product/
  viewport: 1440x900
- url: /admin/catalog/product/<id>/change/
  filename: advanced-tab.webp
  description: pestaña avanzada que muestra la tarjeta de Configuración de página de producto (desplegable de Plantilla de página con una opción no predeterminada seleccionada) y la tarjeta de Detalles técnicos
    debajo de ella.
  save-to: core/static/core/admin/img/help/add-product/
  viewport: 1440x900
-->

Este tutorial lo guiará a través de la creación de un nuevo producto en su tienda. El formulario de producto está organizado en secciones que cubren información básica, medios, precios, inventario, SEO y más: así que puede completar todo de una vez o volver a completar secciones más tarde.

## Comenzando

Desde el menú lateral, navegue a **Productos > Todos los productos** para ver su catálogo de productos. Haga clic en el botón **+ Añadir producto** en la esquina superior derecha para abrir el formulario de creación de productos.

![Página de lista de productos](/static/core/admin/img/help/add-product/product-list-page.webp)

## Información básica

La sección de **Información básica** es donde define la identidad principal de su producto.

![Formulario para agregar producto](/static/core/admin/img/help/add-product/add-product-form.webp)

### Campos obligatorios

- **Nombre** — El nombre del producto que se muestra a los clientes. Haga clic en el icono del globo para agregar traducciones para otros idiomas.
- **Slug** — Versión amigable para URL del nombre (generada automáticamente). Cópiela si es necesario.
- **SKU** — Su código de unidad de control de inventario interno.
- **Tipo de producto** — Elija entre: Simple, Variable, Digital, Paquete, Tarjeta de regalo, Personalizable, Configurable o Reserva.
- **Categoría** — Asigne el producto a una categoría para organización y navegación en la tienda.

### Estado y visibilidad

En la sección de **Estado** en la parte inferior del formulario:

- **Estado** — Establezca en **Borrador** mientras trabaja, **Publicado** cuando esté listo para vender, o **Cessación** para productos que ya no ofrezca.
- **Destacado** — Marque para resaltar este producto en su tienda.
- **Producto digital** — Marque si este producto incluye descargas digitales (archivos, licencias). Puede combinarse con cualquier tipo de producto.
- **Ocultar de la tienda** — Oculta el producto de las listas del catálogo, manteniéndolo disponible como opción de configurador o componente de paquete.

### Campos opcionales

- **Marca** — Asócielo con una marca si aplica.
- **Etiquetas** — Asigne una o más etiquetas en la tarjeta de **Etiquetas** más adelante en este pestaña. Las etiquetas son diferentes de las Colecciones: son etiquetas rápidas y libres para organizar y filtrar productos, en lugar de un agrupamiento de mercancía. Comience a escribir para buscar una etiqueta existente, o escriba un nombre nuevo para crear una en el acto. Vea el tema de ayuda **Etiquetas de producto** para crear, renombrar y eliminar en masa etiquetas directamente.

### Descripciones del producto

- **Descripción breve** — Aparece en listas de productos y tarjetas. Manténgala breve y convincente.
- **Descripción completa** — Descripción detallada del producto mostrada en la página de detalles del producto. Use el editor de texto rico para agregar formato, imágenes, videos y tablas.

Ambos campos de descripción admiten la función de traducción: haga clic en el icono del globo para proporcionar contenido en otros idiomas.

La sección **Detalles del Producto** contiene dos campos de datos estructurados:

- **Características** — Pares clave-valor para resaltar el producto (por ejemplo, "Vida de la batería: 20 horas").
- **Especificaciones** — Detalles técnicos para la pestaña de especificaciones en la página del producto (por ejemplo, "Procesador: Intel i7").

## Medios de comunicación

La sección **Medios de comunicación** le permite gestionar imágenes de productos utilizando la Biblioteca de Medios integrada.

![Pestaña de medios](/static/core/admin/img/help/add-product/media-tab.webp)

1. Haga clic en **+ Añadir imágenes desde la Biblioteca de Medios** para abrir el selector de medios.
2. Seleccione imágenes existentes o cargue nuevas directamente.
3. Arrastre las imágenes para reordenarlas — la **primera imagen** se convierte en la imagen principal del producto que se muestra en listas y tarjetas.

El campo **Tipo de Galería**, en la tarjeta **Configuración de Galería** debajo de la lista de imágenes, controla cómo se muestran las imágenes en la tienda: Galería estándar, Carrusel, Diseño de cuadrícula, Galería de acercamiento o Vista de 360°.

## Precios

Establezca el precio de su producto y configure ventas.

![Pestaña de precios](/static/core/admin/img/help/add-product/pricing-tab.webp)

### Precio regular

- **Precio regular** — El precio de venta al por menor estándar que verán los clientes. La moneda se establece junto con la cantidad del precio.
- **Costo** — Su costo de mercancía, utilizado para cálculos de ganancia. Esto nunca se muestra a los clientes.

### Configuración de venta

Configure descuentos temporales:

- **Tipo de venta** — Elija entre: Sin venta, Precio de venta fijo, Monto restante, o Porcentaje restante.
- **Valor de venta** — La cantidad del descuento o porcentaje.
- **Fecha de inicio de venta / Fecha de finalización de venta** — Programar cuándo se activa y expira la venta. Deje en blanco para iniciar inmediatamente o sin fecha de finalización.

### Precios multimoneda

Si se habilita la multimoneda en su tienda, aparece un campo **Estrategia de precios**:

- **Precios dinámicos** — Los precios en otros idiomas se calculan automáticamente utilizando las tasas de cambio configuradas.
- **Precios fijos** — Establezca un precio específico para cada moneda independientemente usando la sección **Precios multimoneda** que aparece debajo.

## Inventario

Gestione los niveles de stock, el comportamiento de envío y las características físicas del producto.

![Pestaña de inventario](/static/core/admin/img/help/add-product/inventory-tab.webp)

### Gestión de stock

- **Seguimiento de inventario** — Active para seguir los niveles de stock (activado por defecto).
- **Límite de stock bajo** — Reciba alertas cuando el stock caiga por debajo de este número (por defecto: 5).
- **Permitir pedidos de reserva** — Active para aceptar pedidos incluso cuando no haya stock.
- **Acción al agotar stock** — Sobrescriba el comportamiento del sitio o categoría cuando este producto se agote: ocultarlo, mostrarlo como no disponible, mostrar un botón "Notificarme", o permitir pedidos de reserva.

Los niveles de stock se gestionan por almacén. Después de guardar el producto, use la sección **Artículos de inventario** en la parte inferior del formulario (o navegue a **Productos > Artículos de inventario**) para configurar las cantidades en cada ubicación de almacén.

### Atributos físicos

Ingrese el peso del producto (kg) y las dimensiones (largo, ancho, altura en cm) para cálculos precisos de envío.

### Envío

- **Requiere envío** — Si este producto necesita ser enviado al cliente. Está activado por defecto para productos físicos; su tienda y proceso de pago lo usan para decidir si se recopila una dirección de envío y se cotiza el costo del envío para el pedido. Spwig lo desactiva automáticamente para productos Digitales, de Reserva y de Tarjeta de Regalo, ya que nunca se envían — no necesita (y no puede) volver a activarlo para esos tipos de productos. Deje marcado para un producto físico que parezca cercano a digital, como una tarjeta de regalo impresa que se envía en una caja.
- **Paquete de envío preferido** — Opcionalmente, elija uno de sus paquetes de envío configurados. Al establecerlo, las dimensiones propias del paquete se usan para calcular las tarifas de envío en lugar del peso y dimensiones del producto anterior — útil cuando un producto siempre se envía en la misma caja estándar o sobre. Deje en blanco para usar las características físicas del producto. Administre paquetes disponibles bajo **Envío > Paquetes**.

### Pre-venta

Preserve all markdown formatting, image paths, code blocks, and technical terms.

Use the **Pre-order** card to sell a product before it has any stock — useful for upcoming releases you want to start taking orders for ahead of launch:

- **Is Pre-order** — Enable to let customers purchase this product even while it's out of stock.
- **Pre-order Release Date** — The expected availability date, shown to customers.
- **Pre-order Message** — A short custom message shown to customers, up to 200 characters (e.g., "Ships March 2026").

### Product identifiers

Standard product codes for marketplace listings and inventory systems:

- **GTIN** — Global Trade Item Number
- **EAN** — European Article Number
- **UPC** — Universal Product Code (US)
- **ISBN** — For books
- **ASIN** — Amazon identifier
- **MPN** — Manufacturer Part Number

### International shipping / customs

Required for international shipments (expand the **International Shipping / Customs** section):

- **HS Code** — Harmonized System classification code
- **Country of Origin** — Where the product is manufactured
- **Customs Unit Price** — Declared value per unit for customs
- **Export License Number** — Required only for controlled or restricted items
- **Export License Expiry** — Expiration date of the export license

## SEO

Optimize your product's search engine visibility.

![SEO tab](/static/core/admin/img/help/add-product/seo-tab.webp)

- **Meta Title** — The title shown in search engine results. Click the globe icon to translate.
- **Meta Description** — A brief description for search results (max 160 characters). Click the globe icon to translate.
- **Auto-generate SEO** — Check to automatically generate SEO content when the product is saved.

A live **Search Result Preview** shows exactly how your product will appear in Google search results.

## Product page settings

On the **Advanced** tab, the **Product Page Settings** card lets you control how this product's storefront page looks:

- **Page Template** — Override the site default product page layout for this one product: Classic, Full Width, Gallery Focus, or Digital. Leave it set to **Use Site Default** to inherit whatever layout your Design settings specify — most products should stay on the default so template changes there apply automatically.
- **Show Related Products** — Display related products at the bottom of the page.
- **Show Reviews** — Display customer reviews.
- **Show Specifications** — Display the specifications tab.

The **Gallery Type** field — which controls how product images display (Standard Gallery, Carousel, Grid Layout, Zoom Gallery, or 360° View) — is set separately, on the **Media** tab.

## Sales channel

The **Sales Channel** field (in the Status section) controls where the product can be sold:

- **All Channels** — Available online and in-store (POS).
- **Online Only** — Not available through POS terminals.
- **In-Store Only** — Not listed online; only available at your physical store.

A **Barcode** field is also available for POS barcode scanning.

## Saving your product

When you're ready, use the save buttons in the top-right corner. Your product will be visible on the storefront once its status is set to **Published**.

## Tips

Preserve all markdown formatting, image paths, code blocks, and technical terms.

- Comience con el estado **Borrador** para que pueda perfeccionar el producto antes de que los clientes lo vean.
- Suba múltiples imágenes: los productos con varias fotos tienen mejor conversión.
- Complete los campos de **SEO** para mejorar la visibilidad en los motores de búsqueda.
- Use **Categorías**, **Marcas** y **Etiquetas** para ayudar a los clientes a navegar por su catálogo.
- Para productos variables (por ejemplo, tallas o colores diferentes), elija el tipo de **Producto variable** y agregue variantes después de guardar.
- Use **Características** y **Especificaciones** para agregar datos estructurados del producto que se muestren en pestañas dedicadas en la página del producto.
- Si **Requiere envío** no se queda marcado, consulte **Tipo de producto** - Spwig desactiva el envío automáticamente para productos Digitales, Reservas y Tarjetas de regalo, ya que ninguno de ellos se envía físicamente.
- Establezca un **Paquete de envío preferido** para productos que siempre se envíen en la misma caja: esto le ahorrará la molestia de mantener sincronizados el peso y las dimensiones de ese producto con la caja que realmente utilice.