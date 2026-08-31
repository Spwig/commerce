---
title: Añadir un producto
---

Este tutorial le guiará a través de la creación de un nuevo producto en su tienda. El formulario de producto está organizado en secciones que cubren información básica, medios, precios, inventario, SEO y más, para que pueda completar todo de una vez o volver a completar secciones más tarde.

## Comenzando

Desde el menú lateral, navegue a **Productos > Todos los productos** para ver su catálogo de productos. Haga clic en el botón **+ Añadir producto** en la esquina superior derecha para abrir el formulario de creación de productos.

![Página de lista de productos](/static/core/admin/img/help/add-product/product-list-page.webp)

## Información básica

La sección **Información básica** es donde define la identidad principal de su producto.

![Formulario para añadir producto](/static/core/admin/img/help/add-product/add-product-form.webp)

### Campos obligatorios

- **Nombre** — El nombre del producto que se muestra a los clientes. Haga clic en el icono del globo para agregar traducciones para otros idiomas.
- **Slug** — Versión amigable para URL del nombre (generado automáticamente). Personalícelo si es necesario.
- **SKU** — Su código de unidad de control de existencias interno.
- **Tipo de producto** — Elija entre: Simple, Variable, Digital, Paquete, Tarjeta de regalo, Personalizable, Configurable o Reserva.
- **Categoría** — Asigne el producto a una categoría para organización y navegación en la tienda.

### Estado y visibilidad

En la sección **Estado** en la parte inferior del formulario:

- **Estado** — Establezca en **Borrador** mientras trabaja, **Publicado** cuando esté listo para vender, o **Cessación de venta** para productos que ya no ofrezca.
- **Destacado** — Marque para resaltar este producto en su tienda.
- **Producto digital** — Marque si este producto incluye descargas digitales (archivos, licencias). Puede combinarse con cualquier tipo de producto.
- **Ocultar de la tienda** — Oculta el producto de las listas del catálogo, manteniéndolo disponible como opción de configurador o componente de paquete.

### Campos opcionales

- **Marca** — Asócielo con una marca si aplica.
- **Etiquetas** — Asigne una o más etiquetas en la tarjeta **Etiquetas** más abajo en esta pestaña. Las etiquetas son diferentes de las Colecciones: son etiquetas rápidas y libres para organizar y filtrar productos, en lugar de un agrupamiento de mercancía. Comience a escribir para buscar una etiqueta existente, o escriba un nuevo nombre para crear una en el acto. Vea el tema de ayuda **Etiquetas de producto** para crear, renombrar y eliminar en masa etiquetas directamente.

![La tarjeta de Etiquetas en la pestaña de Información básica, con dos etiquetas aplicadas en el selector de etiquetas](/static/core/admin/img/help/add-product/tags-card.webp)

### Descripciones del producto

- **Descripción breve** — Aparece en listas de productos y tarjetas. Manténgala breve y convincente.
- **Descripción completa** — Descripción detallada del producto mostrada en la página de detalles del producto. Use el editor de texto rico para agregar formato, imágenes, videos y tablas.

Ambos campos de descripción admiten la función de traducción: haga clic en el icono del globo para proporcionar contenido en otros idiomas.

### Características y especificaciones

La sección **Detalles del producto** contiene dos campos de datos estructurados:

- **Características** — Pares clave-valor para resaltar el producto (por ejemplo, "Vida de la batería: 20 horas").
- **Especificaciones** — Detalles técnicos para la pestaña de especificaciones en la página del producto (por ejemplo, "Procesador: Intel i7").

## Medios

La sección **Medios** le permite gestionar imágenes de productos usando la Biblioteca de medios integrada.

![Pestaña de Medios](/static/core/admin/img/help/add-product/media-tab.webp)

1. Haga clic en **+ Añadir imágenes desde la Biblioteca de medios** para abrir el selector de medios.
2. Seleccione imágenes existentes o cargue nuevas directamente.
3. Arrastre las imágenes para reordenarlas — la **primera imagen** se convierte en la imagen principal del producto mostrada en listas y tarjetas.

El campo **Tipo de Galería**, en la tarjeta **Configuración de Galería** debajo de la lista de imágenes, controla cómo se muestran las imágenes en la tienda: Galería estándar, Carrusel, Diseño de cuadrícula, Galería de acercamiento o Vista de 360°.

## Precios

Establezca el precio de su producto y configure ventas.

![Pestaña de Precios](/static/core/admin/img/help/add-product/pricing-tab.webp)

### Precio regular

- **Precio regular** — El precio de venta al por menor estándar que verán los clientes.

La moneda se establece junto con la cantidad del precio.
- **Costo** — Su costo de mercancía, utilizado para cálculos de ganancia.

Esto nunca se muestra a los clientes.

### Configuración de venta

Configure descuentos temporales:

- **Tipo de venta** — Elija entre: Sin venta, Precio de venta fijo, Monto restante, o Porcentaje restante.
- **Valor de venta** — La cantidad del descuento o porcentaje.
- **Fecha de inicio de venta / Fecha de finalización de venta** — Programar cuándo se activa y expira la venta. Deje en blanco para iniciar inmediatamente o no tener fecha de finalización.

### Precios multi-moneda

Si se habilita la multi-moneda en su tienda, aparece un campo **Estrategia de precios**:

- **Precios dinámicos** — Los precios en otras monedas se calculan automáticamente utilizando las tasas de cambio configuradas.
- **Precios fijos** — Establezca un precio específico para cada moneda independientemente utilizando la sección **Precios multi-moneda** que aparece debajo.

## Inventario

Administre los niveles de stock, el comportamiento de envío y las características físicas del producto.

![Pestaña de inventario](/static/core/admin/img/help/add-product/inventory-tab.webp)

### Gestión de stock

- **Seguimiento de inventario** — Active para seguir los niveles de stock (habilitado por defecto).
- **Límite de stock bajo** — Reciba alertas cuando el stock caiga por debajo de este número (valor predeterminado: 5).
- **Permitir pedidos de devolución** — Active para aceptar órdenes incluso cuando no haya stock. Los nuevos productos comienzan con el valor **Permitir pedidos de devolución por defecto** desde **Configuración > Configuración de tienda > Comercio**, pero puede anularlo por producto aquí en cualquier momento.
- **Acción al agotar stock** — Anule el comportamiento del sitio o de la categoría cuando este producto se agote: márquelo, muestre como no disponible, muestre un botón de "Notificarme", o permita pedidos de devolución.

Los niveles de stock se gestionan por almacén. Después de guardar el producto, use la sección **Artículos de stock** en la parte inferior del formulario (o navegue a **Productos > Artículos de stock**) para establecer cantidades en cada ubicación de almacén.

### Atributos físicos

Ingrese el peso del producto (kg) y las dimensiones (largo, ancho, altura en cm) para cálculos precisos de envío.

### Envío

- **Requiere envío** — Si este producto debe ser enviado al cliente. Está activado por defecto para productos físicos; su tienda en línea y proceso de pago lo usan para decidir si se recoge una dirección de envío y se cotiza el costo del correo para el pedido. Spwig lo apaga automáticamente para productos Digitales, de Reserva y de Tarjeta de Regalo, ya que nunca se envían — no necesita (y no puede) volver a activarlo para esos tipos de productos. Deje marcado para un producto físico que parezca cercano a digital, como una tarjeta de regalo impresa que se envía en una caja.
- **Paquete de envío preferido** — Opcionalmente, elija uno de sus paquetes de envío configurados. Al establecerlo, las dimensiones propias del paquete se usan para calcular las tarifas de envío en lugar del peso y las dimensiones del producto anterior — útil cuando un producto siempre se envía en la misma caja estándar o sobre. Deje en blanco para usar las características físicas del producto. Administre los paquetes disponibles bajo **Envío > Paquetes**.

### Venta anticipada

Use la tarjeta **Venta anticipada** para vender un producto antes de que tenga stock — útil para lanzamientos futuros que desee comenzar a tomar órdenes con anticipación:

- **¿Es venta anticipada?** — Active para permitir que los clientes compren este producto incluso mientras está agotado.
- **Fecha de lanzamiento de venta anticipada** — La fecha de disponibilidad esperada, mostrada a los clientes.
- **Mensaje de venta anticipada** — Un mensaje personalizado corto mostrado a los clientes, de hasta 200 caracteres (por ejemplo: "Se envía en marzo de 2026").

### Identificadores de producto

Códigos estándar de producto para listados de mercados y sistemas de inventario:

- **GTIN** — Número de artículo de comercio global
- **EAN** — Número de artículo europeo
- **UPC** — Código de producto universal (EE.UU.)
- **ISBN** — Para libros
- **ASIN** — Identificador de Amazon
- **MPN** — Número de pieza del fabricante

### Envío internacional / aduanas

Requerido para envíos internacionales (expanda la sección **Envío internacional / Aduanas**):

- **Código HS** — Código de clasificación del Sistema Armonizado
- **País de Origen** — Lugar donde se fabrica el producto
- **Precio Unitario Aduanero** — Valor declarado por unidad para aduanas
- **Número de Licencia de Exportación** — Requerido solo para artículos controlados o restringidos
- **Vencimiento de la Licencia de Exportación** — Fecha de expiración de la licencia de exportación

## SEO

Optimice la visibilidad de su producto en los motores de búsqueda.

![Pestaña SEO](/static/core/admin/img/help/add-product/seo-tab.webp)

- **Meta Title** — El título que se muestra en los resultados del motor de búsqueda. Haga clic en el icono del globo para traducir.
- **Meta Description** — Una breve descripción para los resultados de búsqueda (máximo 160 caracteres). Haga clic en el icono del globo para traducir.
- **Generar SEO automáticamente** — Marque para generar automáticamente el contenido de SEO cuando se guarde el producto.

Una vista previa en vivo de **Search Result Preview** muestra exactamente cómo aparecerá su producto en los resultados de búsqueda de Google.

## Configuración de la página del producto

En la pestaña **Advanced**, la tarjeta **Product Page Settings** le permite controlar cómo se ve la página de la tienda de este producto:

- **Page Template** — Anule el diseño predeterminado de la página de producto del sitio para este único producto: Classic, Full Width, Gallery Focus o Digital. Déjelo configurado en **Use Site Default** para heredar el diseño que especifique su configuración de Diseño; la mayoría de los productos deben permanecer en el predeterminado para que los cambios de plantilla allí se apliquen automáticamente.
- **Show Related Products** — Muestra productos relacionados en la parte inferior de la página.
- **Show Reviews** — Muestra las reseñas de los clientes.
- **Show Specifications** — Muestra la pestaña de especificaciones.

El campo **Gallery Type** — que controla cómo se muestran las imágenes del producto (Standard Gallery, Carousel, Grid Layout, Zoom Gallery o 360° View) — se configura por separado, en la pestaña **Media**.

![Pestaña Advanced mostrando la tarjeta Product Page Settings con un menú desplegable de Page Template, y la tarjeta Technical Details debajo](/static/core/admin/img/help/add-product/advanced-tab.webp)

## Canal de ventas

El campo **Sales Channel** (en la sección Status) controla dónde se puede vender el producto:

- **All Channels** — Disponible en línea y en la tienda (POS).
- **Online Only** — No disponible a través de terminales POS.
- **In-Store Only** — No se lista en línea; solo disponible en su tienda física.

También está disponible un campo **Barcode** para el escaneo de códigos de barras POS.

## Guardar su producto

Cuando esté listo, use los botones de guardar en la esquina superior derecha. Su producto será visible en la tienda una vez que su estado se establezca en **Published**.

## Consejos

- Comience con el estado **Draft** para que pueda perfeccionar el producto antes de que los clientes lo vean.
- Suba varias imágenes; los productos con varias fotos tienen una mejor tasa de conversión.
- Complete los campos de **SEO** para mejorar la detectabilidad en los motores de búsqueda.
- Use **Categories**, **Brands** y **Tags** para ayudar a los clientes a navegar por su catálogo.
- Para productos variables (por ejemplo, diferentes tamaños o colores), elija el tipo **Variable Product** y agregue variantes después de guardar.
- Use **Features** y **Specifications** para agregar datos estructurados del producto que se muestran en pestañas dedicadas en la página del producto.
- Si **Requires Shipping** no se mantiene marcado, revise el **Product Type** — Spwig desactiva el envío automáticamente para productos Digitales, de Reserva y Tarjetas de Regalo, ya que ninguno de esos se envía físicamente.
- Establezca un **Preferred Shipping Package** para productos que siempre se envían en la misma caja; esto le ahorra tener que mantener el peso y las dimensiones de ese producto en sincronía con la caja que realmente usa.