---
title: Acciones en masa de productos
---

La lista de **Productos** le permite actuar en muchos productos a la vez en lugar de abrir cada uno por separado. Desde el menú desplegable de **Acciones en masa** en la barra de herramientas sobre la cuadrícula de productos, puede publicar o no publicar productos, destacarlos o no, exportar datos a CSV, verificar si los productos están listos para envíos internacionales o eliminarlos, todo en un solo paso.

Navegue hasta **Productos > Todos los productos** para usar estas acciones.

![La barra de herramientas de la lista de productos con tres tarjetas de producto seleccionadas y el menú desplegable de Acciones en masa que muestra cada opción, incluyendo Exportar datos aduaneros (CSV) y Verificar la preparación para envíos internacionales](/static/core/admin/img/help/product-bulk-actions/bulk-actions-dropdown.webp)

## Ejecutar una acción en masa

1. Use el panel de filtros o la caja de **Búsqueda** para reducir los productos que desee, si es necesario
2. Marque la casilla en la esquina superior izquierda de cada tarjeta de producto que desee incluir: la barra de **Acciones en masa** muestra un recuento en tiempo real de cuántos productos están seleccionados
3. Elija una acción del menú desplegable de **Acciones en masa**
4. Haga clic en **Aplicar**

Las acciones que cambian o exportan datos se ejecutan inmediatamente; **Eliminar seleccionados** solicita una confirmación primero, ya que es la única acción aquí que no se puede deshacer fácilmente desde la lista en sí misma.

## Acciones disponibles

| Acción | Qué hace |
|--------|---------------|
| **Marcar como Publicado** | Establece el estado de los productos seleccionados como Publicado para que aparezcan en la tienda. |
| **Marcar como Borrador** | Establece el estado de los productos seleccionados como Borrador, ocultándolos de la tienda mientras los edita. |
| **Marcar como Destacado** | Habilita **Es Destacado** en los productos seleccionados. |
| **Eliminar Destacado** | Deshabilita **Es Destacado** en los productos seleccionados. |
| **Exportar a CSV** | Descarga un CSV de los ID, nombre, SKU, estado, bandera destacada y precio de los productos seleccionados. |
| **Exportar datos aduaneros (CSV)** | Descarga un CSV de la información aduanera para los productos seleccionados. Vea a continuación. |
| **Verificar preparación para envíos internacionales** | Muestra un resumen de cuáles de los productos seleccionados tienen los datos aduaneros necesarios para envíos internacionales. Vea a continuación. |
| **Eliminar seleccionados** | Mueve los productos seleccionados a la papelera, tras un aviso de confirmación. |

## Exportar datos aduaneros (CSV)

Úselo cuando necesite una hoja de declaración aduanera para entregarle a un transportista, mensajero o corredor aduanero: por ejemplo, antes de un gran envío internacional, o al configurar un nuevo transportista que pida códigos HS y datos de origen de antemano.

Seleccione los productos, elija **Exportar datos aduaneros (CSV)** desde el menú desplegable y haga clic en **Aplicar**. Spwig descarga un archivo llamado `product_customs_data.csv` con una fila por producto y estas columnas:

| Columna | Origen |
|--------|--------|
| **SKU** | El SKU del producto |
| **Nombre** | El nombre del producto |
| **Código HS** | El código de clasificación del Sistema Armonizado |
| **País de origen** | Dónde se fabrica el producto |
| **Precio unitario aduanero** | El valor declarado por unidad para aduanas |
| **Licencia de exportación** | El número de licencia de exportación, si el producto lo requiere |
| **Fecha de vencimiento de la licencia** | La fecha de vencimiento de la licencia de exportación, si se establece |
| **Listo para envío internacional** | `Sí` o `No` — si el producto tiene los datos mínimos necesarios para envío internacional (véase a continuación) |

Estos campos provienen de la sección **Envío internacional / Aduanas** del formulario de producto. Si un producto falta uno, su columna queda en blanco en la exportación: complete los datos que falten en el producto antes de confiar en este archivo para un envío real.

## Verificar preparación para envíos internacionales

Úselo para auditar un lote de productos antes de comenzar a enviarlos internacionalmente, sin abrir cada producto individualmente o esperar a una exportación completa en CSV.

Seleccione los productos, elija **Verificar preparación para envíos internacionales** y haga clic en **Aplicar**. Spwig comprueba cada producto seleccionado contra tres campos requeridos: **Código HS**, **País de origen** y **Precio unitario aduanero**, y muestra una notificación que resume el resultado:

- Si cada producto seleccionado tiene los tres campos completos, verá una confirmación de que todos están listos.
- Si algunos tienen datos faltantes, la notificación informa cuántos están listos y cuántos no, y enumera cada producto que no esté listo junto con los campos que le faltan (por ejemplo, "Taza de cerámica azul (faltante: código HS, país de origen)").

Si más de 10 productos tienen datos faltantes, la notificación lista los primeros 10 y le indica cuántos más hay.

Esta acción solo lee datos: no cambia nada en los productos, por lo que es seguro ejecutarla tanto como desee mientras complete la información de aduanas en su catálogo.

**Número de licencia de exportación** y **Fecha de vencimiento de la licencia de exportación** no forman parte de la verificación de listado. Solo aplican a artículos controlados o restringidos, por lo que un producto puede estar "listo" para envío internacional sin ellos.

## Consejos

- Ejecute **Verificar la preparación para envío internacional** en todo su catálogo (o por categoría a la vez) antes de su primer pedido internacional: es mucho más rápido que descubrir un código HS faltante cuando un envío ya está en la frontera.
- Mantenga **Datos de aduanía de exportación (CSV)** para entregárselo a agentes y transportistas, y **Verificar la preparación para envío internacional** para su propia lista de verificación interna: el CSV es un registro, la verificación de preparación es una lista de tareas.
- Complete **Código HS**, **País de origen** y **Precio unitario de aduanía** en el formulario del producto (debajo de **Envío internacional / Aduanas**) a medida que agrega nuevos productos, para que no termine haciendo esto en masa más tarde.
- La cuadrícula de productos carga más productos automáticamente a medida que desplaza (desplazamiento infinito), y sus selecciones de casilla de verificación se mantienen a medida que se cargan nuevos productos: así que puede desplazar para construir una selección grande antes de aplicar una acción. Sin embargo, cambiar un filtro o recargar la página borra su selección, así que aplique la acción antes de ajustar los filtros.
- **Marcar como borrador** es una forma rápida de retirar varios productos del catálogo de inmediato: por ejemplo, antes de un recuento de existencias - sin cambiar nada más sobre ellos.