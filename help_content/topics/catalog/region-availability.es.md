---
title: Disponibilidad por región
---

La disponibilidad por región controla qué zonas de ventas de su producto pueden venderse, y cómo experimentan su catálogo los compradores fuera de esas zonas. úselo cuando un producto esté licenciado solo para ciertos países, cuando el stock esté reservado para un mercado local o cuando esté lanzando un nuevo producto región por región.

Esto se basa en **Zonas de ventas**, que agrupan países en mercados con nombre (consulte la guía de Zonas de ventas para configurarlas). Una vez que existan sus zonas, puede restringir productos individuales a ellas y decidir cómo aparecen los productos restringidos ante los compradores que no pueden comprarlos.

## Restringir un producto a zonas específicas

Cada producto tiene una configuración de **Disponibilidad por región** en su página de edición. Abra **Productos > Todos los productos**, seleccione un producto y búsquelo en la sección **Estado** junto con **Estado**, **Destacado** y **Ocultar de la tienda**.

![La sección de estado del formulario de edición del producto, con el menú desplegable de disponibilidad por región establecido en "Solo en las regiones seleccionadas" junto con Destacado y Ocultar de la tienda](/static/core/admin/img/help/region-availability/product-region-availability-field.webp)

| Opción | Qué significa |
|--------|----------------|
| **Disponible en todas las regiones** | Sin restricción. El producto se vende en todas partes. Este es el valor predeterminado para cada producto. |
| **Solo en las regiones seleccionadas** | Una lista de permitidos. El producto solo se vende en las regiones que seleccione a continuación — en todas partes más allá, se considera que no está disponible. |
| **Todas las regiones excepto las seleccionadas** | Una lista de bloqueos. El producto se vende en todas partes *excepto* las regiones que seleccione a continuación. |

### Elegir las regiones

Debajo de la sección de estado, una tabla titulada **Disponibilidad por región (regiones seleccionadas)** muestra las regiones a las que se aplica el modo anterior.

1. Establezca **Disponibilidad por región** en **Solo en las regiones seleccionadas** o **Todas las regiones excepto las seleccionadas**.
2. En la tabla **Disponibilidad por región (regiones seleccionadas)**, haga clic en **Añadir otra región** y elija una Zona de ventas.
3. Repita para cada región que desee agregar.
4. Haga clic en **Guardar**.

![La tabla integrada "Disponibilidad por región (regiones seleccionadas)" con las filas de América del Norte y Europa añadidas](/static/core/admin/img/help/region-availability/product-region-availability-inline.webp)

Si **Disponibilidad por región** está establecida en **Disponible en todas las regiones**, todo lo que haya en esta tabla se ignora: limpie primero el menú desplegable de modo si quiere eliminar una restricción sin borrar las filas.

Para una vista del catálogo general de las reglas de región de cada producto en una sola lista (útil al auditar muchos productos a la vez), vaya a **Visibilidad de región de producto** en `/admin/catalog/productregionvisibility/`.

## Mostrar a los compradores dónde no llega un producto

Cuando la región de un comprador no coincida con las reglas de disponibilidad del producto, controla qué ven en **Configuración de visualización del stock**, en la sección **Disponibilidad por región**. Esta página aún no tiene un acceso directo en el menú lateral: hágalos directamente en `/admin/catalog/stockdisplaysettings/`.

![Configuración de visualización del stock, sección de disponibilidad por región — el menú desplegable de visualización por región, establecido en "Mostrar, marcado como no disponible"](/static/core/admin/img/help/region-availability/stock-display-region-availability.webp)

| Opción | Qué ven los compradores |
|--------|------------------------|
| **Mostrar, marcado como no disponible** (predeterminado) | El producto aún aparece en las listas, con un sello de "No disponible" y una noticia de "No se envía a [región]" en lugar del botón "Añadir al carrito". También aparece un banner en la parte superior de las páginas de listado ("Algunos productos no se envían a [destino]") con un enlace para filtrar solo los artículos que sí se envían allí. |
| **Ocultar de las listas** | El producto se elimina por completo de las listas y resultados de búsqueda para los compradores de esa región. |

![Lista de productos de la tienda que se envían a Europa — el banner "Algunos productos no se envían a Europa" encima de la cuadrícula, y una tarjeta de producto marcada como "No disponible" con una noticia de "No se envía a Europa"](/static/core/admin/img/help/region-availability/storefront-region-restricted-listing.webp)

La página de un producto restringido siempre muestra un aviso de 'Este producto no se envía a [región]' cuando un comprador llega directamente a ella (por ejemplo, desde un enlace compartido o un resultado de motor de búsqueda) — esto se aplica independientemente de la opción de lista que elija arriba, ya que un enlace directo evita por completo la lista.

## Permitir que los compradores elijan o descubran su región

Spwig puede detectar la región de un comprador automáticamente y ofrecer un cambio, y puede agregar un selector para que los compradores lo cambien ellos mismos en cualquier momento.

### Antes de comenzar

Necesitas configurar dos cosas para que la detección y el cambio de región funcionen correctamente:

1. **Regiones de ventas** — los países en cada región y la moneda predeterminada de cada región. Si no ves **Regiones de ventas** bajo **Inventario** en el menú lateral, activa **Habilitar múltiples almacenes** en **Configuración > Configuración de tienda > Comercio electrónico** para revelar el enlace del menú (no necesitas usar realmente múltiples almacenes — este ajuste solo desbloquea el elemento del menú). También puedes ir directamente a `/admin/catalog/salesregion/`.
2. **Países de envío** — los países a los que tu tienda realmente envía. Estos suelen estar ya en vigor: cada país que agregues a una zona de envío se agrega automáticamente aquí también. Para revisar o ajustar manualmente la lista, abre `/admin/shipping/shippingcountry/` directamente (también no tiene un enlace del menú lateral aún).

### La confirmación automática de región

Spwig detecta la región de un comprador a partir de su ubicación y la aplica automáticamente. Cuando esto los coloca en una región *diferente* de la región principal (predeterminada) de tu tienda — y tienes dos o más Regiones de ventas activas — Spwig muestra una confirmación en su primera visita para que sepan en qué región están y puedan cambiarla:

> **Hemos establecido su región en [Región]**
> Elegimos esta región desde su ubicación para que vea los productos y precios correctos. ¿No es correcto? Elija su país.
> Enviar a: [selector de país]  **[Continuar navegando]**

![El mensaje de confirmación 'Hemos establecido su región en Norteamérica' en la tienda, con un selector de país 'Enviar a' y un botón 'Continuar navegando'](/static/core/admin/img/help/region-availability/region-confirmation-modal.webp)

Elegir un país diferente en el selector los cambia inmediatamente. Si se cierra o se hace clic en **Continuar navegando**, se mantiene su región actual, y no se les preguntará de nuevo en ese navegador. Los visitantes que ya están en su región predeterminada no reciben la confirmación en absoluto.

### Añadir un selector de envío a su encabezado o pie de página

Si prefiere que los compradores cambien de región ellos mismos en cualquier momento (en lugar de depender solo del aviso automático), añade el widget **Selector de envío** a tu encabezado o pie de página.

1. Navega a **Diseño > Constructor de encabezados** (o **Constructor de pies de página**).
2. Arrastra el widget **Selector de envío** de la biblioteca de widgets a una fila.
3. Haz clic en **Guardar**.

![La biblioteca de widgets del constructor de encabezados con el grupo 'Tienda' resaltado, mostrando el widget Selector de envío junto con el carrito de compras, el menú de cuenta y el selector de idioma](/static/core/admin/img/help/region-availability/ship-to-selector-widget-library.webp)

El widget no requiere configuración — lista automáticamente tus países de envío activos, y muestra la selección actual del comprador (o el país detectado por GeoIP, si aún no ha elegido uno). Elegir un país diferente actualiza inmediatamente su región y recarga la disponibilidad y los precios de los productos de la página.

El Selector de envío aún no tiene un formulario de configuración dedicado. Si quieres cambiar el estilo del botón (borde, sólido o fantasma) o ocultar la etiqueta 'Enviar a', abre la configuración del widget en el constructor y edita directamente el campo **Configuración personalizada (JSON)**, usando `button_style` y `show_label`.

### La moneda sigue la región

Si tu tienda admite más de una moneda (configurada bajo **Configuración > Multi-moneda**), cambiar de región — ya sea a través del aviso o del Selector de envío — también cambia la moneda mostrada a la moneda predeterminada de esa región.

Si su tienda solo tiene una moneda, o no ha habilitado explícitamente una segunda, la moneda se deja como está cuando un comprador cambia de región.

## Consejos

- Deje **Disponibilidad por región** en **Disponible en todas las regiones** a menos que tenga una razón específica para restringir un producto: es la opción más sencilla y no requiere mantenimiento a medida que agregue más regiones posteriormente.
- Use **Solo en regiones seleccionadas** para un listado de permitidos pequeño (por ejemplo, un producto que se lanza en un solo país primero) y **Todas las regiones excepto las seleccionadas** para un listado de prohibidos pequeño (por ejemplo, en todas partes excepto en un país donde el artículo no tenga licencia) - elija el que necesite menos filas para configurar.
- Si los compradores informan que un producto falta pero debería estar visible, verifique tanto la configuración **Disponibilidad por región** del producto como si su país está cubierto por un **Región de ventas** activa y un **País de envío** activo.
- **Ocultar de las listas** mantiene su catálogo con aspecto limpio para los compradores que no pueden comprar ciertos artículos, pero también significa que el merchandising y la búsqueda parecerán más escasos en esas regiones: **Mostrar, marcado como no disponible** suele ser mejor si aún quiere que los compradores naveguen por todo su catálogo incluso en aquellos lugares donde no puedan realizar la compra.
- Pruebe el comportamiento de las regiones agregando el selector de envío a su encabezado y cambiando entre países usted mismo antes de depender de la detección de GeoIP durante un lanzamiento.
- Establezca los valores de prioridad de sus regiones de manera deliberada: la región activa con mayor prioridad es el respaldo para los compradores cuyo país no se pueda detectar o no coincida con ninguna región.