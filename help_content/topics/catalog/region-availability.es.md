---
title: Disponibilidad por región
---

La disponibilidad por región controla qué zonas de ventas de su producto pueden venderse, y cómo experimentan su catálogo los compradores fuera de esas zonas. úselo cuando un producto esté licenciado solo para ciertos países, cuando el stock esté reservado para un mercado local o cuando esté lanzando un nuevo producto región por región.

Esto se basa en **Zonas de ventas**, que agrupan países en mercados con nombre (consulte la guía de Zonas de ventas para configurarlas). Una vez que existan sus zonas, puede restringir productos individuales a ellas y decidir cómo aparecen los productos restringidos a los compradores que no pueden comprarlos.

## Restringir un producto a zonas específicas

Cada producto tiene un ajuste de **Disponibilidad por región** en su página de edición. Abra **Productos > Todos los productos**, seleccione un producto y búsquelo en la sección **Estado** junto con **Estado**, **Destacado** y **Ocultar de la tienda**.

<!-- screenshots-needed:
- url: /en/admin/catalog/product/1/change/
  filename: product-region-availability-field.webp
  description: Página de edición del producto desplazada a la sección de Estado, con el campo de disponibilidad por región visible y seleccionado como "Solo en las zonas seleccionadas"
  save-to: core/static/core/admin/img/help/region-availability/
  viewport: 1440x900
  notes: Use un producto con al menos 2 zonas ya seleccionadas abajo, si es posible, para que en la segunda imagen la tabla tenga filas visibles.
-->

| Opción | Qué significa |
|--------|---------------|
| **Disponible en todas las zonas** | Sin restricción. El producto se vende en todas partes. Este es el valor predeterminado para cada producto. |
| **Solo en las zonas seleccionadas** | Una lista de permitidos. El producto solo se vende en las zonas que seleccione a continuación - en todas partes, se trata como no disponible. |
| **Todas las zonas excepto las seleccionadas** | Una lista de bloqueos. El producto se vende en todas partes *excepto* en las zonas que seleccione a continuación. |

### Elegir las zonas

Debajo de la sección Estado, una tabla titulada **Disponibilidad por región (zonas seleccionadas)** muestra las zonas a las que se aplica el modo anterior.

1. Establezca **Disponibilidad por región** en **Solo en las zonas seleccionadas** o **Todas las zonas excepto las seleccionadas**.
2. En la tabla **Disponibilidad por región (zonas seleccionadas)**, haga clic en **Añadir otra zona** y elija una Zona de ventas.
3. Repita para cada zona que desee agregar.
4. Haga clic en **Guardar**.

<!-- screenshots-needed:
- url: /en/admin/catalog/product/1/change/
  filename: product-region-availability-inline.webp
  description: La tabla "Disponibilidad por región (zonas seleccionadas)" con dos o tres filas de zonas añadidas
  save-to: core/static/core/admin/img/help/region-availability/
  viewport: 1440x900
-->

Si **Disponibilidad por región** está establecida en **Disponible en todas las zonas**, todo lo que haya en esta tabla se ignora: limpie primero el menú desplegable de modo si quiere eliminar una restricción sin borrar las filas.

Para ver una vista general del catálogo de las reglas de región de cada producto en una lista (útil al auditar muchos productos a la vez), vaya a **Visibilidad de región de producto** en `/admin/catalog/productregionvisibility/`.

## Mostrando a los compradores dónde no llega el producto

Cuando la región del comprador no coincide con las reglas de disponibilidad del producto, controla qué ven en **Configuración de visualización del stock**, en la sección **Disponibilidad por región**. Esta página aún no tiene un acceso directo en el menú lateral: ábrala directamente en `/admin/catalog/stockdisplaysettings/`.

<!-- screenshots-needed:
- url: /en/admin/catalog/stockdisplaysettings/1/change/
  filename: stock-display-region-availability.webp
  description: Formulario de cambio de Configuración de visualización del stock desplazado a la sección "Disponibilidad por región", mostrando el campo de visualización restringida por región
  save-to: core/static/core/admin/img/help/region-availability/
  viewport: 1440x900
-->

| Opción | Lo que ven los compradores |
|--------|-------------------|
| **Mostrar, marcado como no disponible** (predeterminado) | El producto sigue apareciendo en las listas, con un sello de "No disponible" y una notificación de "No se envía a [región]" en lugar del botón "Añadir al carrito". También aparece un banner en la parte superior de las páginas de lista ("Algunos productos no se envían a [destino]") con un enlace para filtrar y mostrar solo los artículos que sí se envían allí. |
| **Ocultar de las listas** | El producto se elimina por completo de las listas y resultados de búsqueda para los compradores de esa región. |

<!-- screenshots-needed:
- url: /en/products/
  filename: storefront-region-restricted-listing.webp
  description: Lista de productos de la tienda con el banner de región en la parte superior y al menos una tarjeta de producto que muestre el sello de "No disponible" y la notificación de "No se envía a [región]"
  save-to: core/static/core/admin/img/help/region-availability/
  viewport: 1440x900
  notes: Requiere una selección de envío a destino (o detección de GeoIP) que resuelva a una región a la que un producto de demostración esté restringido.
-->

Un producto restringido siempre muestra una notificación de "Este producto no se envía a [región]" cuando un comprador llega directamente a él (por ejemplo, desde un enlace compartido o resultado de motor de búsqueda) — esto se aplica independientemente de la opción de lista que elija, ya que un enlace directo evita por completo la lista.

## Permitir que los compradores elijan o descubran su región

Spwig puede detectar automáticamente la región de un comprador y ofrecer un cambio, y puede agregar un selector para que los compridores lo cambien ellos mismos en cualquier momento.

### Antes de comenzar

Necesita dos cosas configuradas para que la detección y el cambio de región funcionen correctamente:

1. **Regiones de ventas** — los países en cada región y la moneda predeterminada de cada región. Si no ve **Regiones de ventas** bajo **Inventario** en el menú lateral, active **Habilitar múltiples almacenes** en **Configuración > Configuración de la tienda > Comercio electrónico** para revelar el enlace del menú (no necesita usar realmente múltiples almacenes — este ajuste solo desbloquea el elemento del menú). También puede ir directamente a `/admin/catalog/salesregion/`.
2. **Países de envío** — los países a los que su tienda realmente envía. Normalmente ya están en vigor: cada país que agregue a una zona de envío se agrega automáticamente aquí. Para revisar o ajustar manualmente la lista, abra directamente `/admin/shipping/shippingcountry/` (también no tiene un enlace del menú lateral).

### La confirmación automática de región

Spwig detecta la región de un comprador desde su ubicación y la aplica automáticamente. Cuando esto los coloca en una región *diferente* a la región principal (predeterminada) de su tienda — y tiene dos o más Regiones de ventas activas — Spwig muestra una confirmación en su primera visita para que sepan en qué región están y puedan cambiarla:

> **Hemos establecido su región en [Región]**
> Elegimos esta región desde su ubicación para que vea los productos y precios correctos. ¿No es correcto? Elija su país.
> Enviar a: [selector de país]  **[Seguir navegando]**

<!-- screenshots-needed:
- url: /en/
  filename: region-confirmation-modal.webp
  description: El modal de confirmación "Hemos establecido su región en [Región]" en la página principal de la tienda, con el selector de país y el botón Seguir navegando
  save-to: core/static/core/admin/img/help/region-availability/
  viewport: 1440x900
  notes: Requiere GeoIP resolviendo a una región no predeterminada y al menos 2 Regiones de ventas activas para desencadenarlo. Localmente, establezca una cookie "geo_country" a un país no predeterminado para simulararlo.
-->

Elegir un país diferente en el selector los cambia inmediatamente. Si se cierra o se hace clic en **Seguir navegando**, se mantiene su región actual, y no se les preguntará nuevamente en ese navegador. Los visitantes que ya están en su región predeterminada no reciben la confirmación en absoluto.

### Agregar un selector de envío a su encabezado o pie de página

Si prefiere que los compradores cambien de región ellos mismos en cualquier momento (en lugar de depender solo del aviso automático), agregue el widget **Selector de envío** a su encabezado o pie de página.

1.

Navegue a **Diseño > Constructor de encabezados** (o **Constructor de pies de página**).
2.

Arrastre el widget **Selector de dirección de envío** desde la biblioteca de widgets a una fila.
3.

Haga clic en **Guardar**.

<!-- screenshots-needed:
- url: /en/theme/header/builder/
  filename: ship-to-selector-widget-library.webp
  description: Constructor de encabezados con la barra lateral de la biblioteca de widgets abierta y el widget Selector de dirección de envío visible/resaltado
  save-to: core/static/core/admin/img/help/region-availability/
  viewport: 1440x900
-->

El widget no requiere configuración: lista automáticamente sus países de envío activos y muestra la selección actual del comprador (o el país detectado por GeoIP, si aún no ha elegido uno). Al elegir un país diferente, actualiza inmediatamente su región y vuelve a cargar la disponibilidad y los precios de los productos de la página.

El Selector de dirección de envío aún no tiene un formulario de configuración dedicado. Si quiere cambiar el estilo del botón (contorno, sólido o fantasma) o ocultar la etiqueta "Enviar a", abra la configuración del widget en el constructor y edite directamente el campo **Configuración personalizada (JSON)**, utilizando `button_style` y `show_label`.

### Moneda según región

Si su tienda admite más de una moneda (configurado bajo **Configuración > Múltiples monedas**), al cambiar de región - ya sea a través del menú desplegable o del Selector de dirección de envío - también cambia la moneda mostrada a la moneda predeterminada de esa región. Si su tienda solo tiene una moneda, o no ha habilitado explícitamente una segunda, la moneda permanece igual cuando un comprador cambia de región.

## Consejos

- Deje **Disponibilidad por región** en **Disponible en todas las regiones**, a menos que tenga una razón específica para restringir un producto: es la opción más sencilla y no requiere mantenimiento al agregar regiones posteriormente.
- Use **Solo en regiones seleccionadas** para un listado de permitidos pequeño (por ejemplo, un producto que se lanza en un país primero) y **Todas las regiones excepto seleccionadas** para un listado de prohibidos pequeño (por ejemplo, en todas partes excepto en un país donde el artículo no tenga licencia) - elija el que necesite menos filas para configurar.
- Si los compradores informan que un producto falta y debería estar visible, revise tanto la configuración **Disponibilidad por región** del producto como si su país está cubierto por un **Área de ventas** activa y un **País de envío** activo.
- **Ocultar de listas** mantiene limpia su catálogo para los compradores que no pueden comprar ciertos artículos, pero también significa que el merchandising y la búsqueda lucirán más delgados en esas regiones: **Mostrar, marcado como no disponible** suele ser mejor si aún quiere que los compradores naveguen por todo su catálogo, incluso en regiones donde no puedan realizar la compra.
- Pruebe el comportamiento de región agregando el Selector de dirección de envío a su encabezado y cambiando entre países usted mismo antes de depender de la detección de GeoIP durante un lanzamiento.
- Establezca los valores de prioridad de sus regiones de manera deliberada: la región activa con mayor prioridad es el respaldo para los compradores cuyo país no se puede detectar o no coincide con ninguna región.