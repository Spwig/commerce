---
title: Acciones en masa para el stock
---

Más allá de ajustes puntuales, Spwig le brinda tres acciones en masa en la lista de **Artículos de stock** para el trabajo de inventario que ocurre en muchos productos a la vez: mover el stock entre almacenes, anular unidades dañadas o perdidas, y reconciliar el stock después de un recuento físico. Las tres funciones se ejecutan desde el mismo menú desplegable **Acciones**, aplican la misma cantidad a cada artículo de stock que seleccione y se registran completamente en el registro de movimiento de stock.

Navegue hasta **Productos > Artículos de stock** para usarlos.

## Ejecutar una acción de stock en masa

1. En la lista de **Artículos de stock**, use los filtros o la búsqueda para encontrar los artículos que desee actualizar
2. Marque la casilla junto a cada artículo de stock para incluirlo (o use la casilla de encabezado para seleccionar todos los artículos de la página)
3. Elija una de las tres acciones del menú desplegable **Acciones**:
   - **Transferir stock a almacén**
   - **Registrar stock dañado/perdido**
   - **Recontar stock (recuento físico)**
4. Haga clic en **Ir**
5. Revise la página de confirmación — muestra cada artículo de stock seleccionado con sus cantidades **en mano**, **asignadas** y **disponibles** actuales para que pueda verificar que haya seleccionado los artículos correctos
6. Complete los campos de la acción (ver a continuación) y haga clic en el botón de envío para aplicarla

![Lista de artículos de stock con el menú desplegable de acciones en masa abierto, mostrando Transferir stock a almacén, Registrar stock dañado/perdido y Recount stock (recuento físico) junto con otras acciones](/static/core/admin/img/help/stock-bulk-actions/stock-items-actions-dropdown.webp)

La misma cantidad que ingrese se aplica a **todos** los artículos seleccionados — esto está diseñado para mover, anular o recountar la misma cantidad de unidades en muchos códigos de productos a la vez (por ejemplo, transferir 10 unidades de varios productos a una nueva ubicación de tienda). Para un solo artículo con una cantidad diferente, ejecute la acción nuevamente con solo ese artículo seleccionado, o use **Ajustar los niveles de stock** en su lugar.

## Transferir stock a almacén

Úselo para mover el stock disponible de cada artículo seleccionado de su almacén a otro almacén — por ejemplo, reabastecer una nueva ubicación de retail desde su almacén principal, o redistribuir el inventario entre centros de cumplimiento regionales.

En la página de confirmación, complete:

| Campo | Descripción |
|-------|-------------|
| **Almacén de destino** | Adónde debe moverse el stock. Solo los almacenes activos aparecen en esta lista. |
| **Cantidad por artículo** | Unidades a mover de cada artículo seleccionado de su almacén actual. |
| **Motivo** | Nota opcional, por ejemplo, "Reabastecimiento de nueva tienda de Auckland". |

Haga clic en **Transferir stock** para aplicar.

![Página de confirmación de Transferir stock: un card de Artículos de stock seleccionados que muestra tres artículos con sus figuras de en mano/atribuidas/disponibles, y un formulario de Detalles de transferencia con un almacén de destino, cantidad y motivo completados](/static/core/admin/img/help/stock-bulk-actions/transfer-stock-confirmation.webp)

**Solo el stock no reservado puede moverse.** Spwig transfiere desde el stock *disponible* (en mano menos unidades asignadas a órdenes abiertas) — las unidades ya comprometidas a un pedido de cliente permanecen en el almacén de origen para que se pueda cumplir el pedido. Si un artículo seleccionado no tiene suficiente stock disponible para cubrir la cantidad que ingresó, ese artículo se omite y se explica el motivo con un error; el resto de la selección aún se transfiere.

Si un artículo seleccionado ya está almacenado en el almacén de destino que eligió, se omite automáticamente (no hay nada que transferir a sí mismo), y verá un mensaje que le indicará cuántos artículos se omitieron por este motivo.

Cada transferencia escribe un conjunto de movimientos emparejados en el registro de auditoría — una entrada negativa **Transferencia de almacén** en el origen y una positiva coincidente en el destino — por lo tanto, el registro completo muestra exactamente de dónde vino el stock y a dónde fue.

## Registrar stock dañado/perdido

Úselo para anular unidades que estén rotas, dañadas o perdidas — por ejemplo, después de encontrar mercancía dañada en un envío o investigar una discrepancia.

En la página de confirmación, complete:

| Campo | Descripción |
|-------|-------------|
| **Cantidad a escribir (por artículo)** | Unidades a eliminar del stock disponible para cada artículo seleccionado. |
| **Motivo** | Nota opcional, por ejemplo: "Daño por agua durante el almacenamiento". |

Haga clic en **Registrar escritura** para aplicarla.

**El stock reservado no se puede escribir.** El stock disponible nunca puede caer por debajo de la cantidad actualmente asignada a pedidos abiertos: Spwig bloquea la escritura para cualquier artículo donde la cantidad que ingresó afecte el stock reservado, por lo que no puede dejar accidentalmente un pedido pagado sin el stock necesario para cumplirlo. Si ocurre esto con un artículo, verá un error que menciona el artículo y cuántas unidades no reservadas tiene realmente disponibles para escribir.

Cada escritura se registra como un movimiento de **Dañado/Perdido** en ese artículo de stock, con una cantidad negativa.

## Recontar el stock (cuenta física)

Úselo después de una cuenta física del stock para corregir las cantidades disponibles para que coincidan con las que realmente contó: la forma más rápida de reconciliar muchos artículos después de una auditoría del almacén o un conteo cíclico.

En la página de confirmación, complete:

| Campo | Descripción |
|-------|-------------|
| **Cantidad disponible contada (por artículo)** | La cantidad que contó físicamente. El stock disponible se establece en este número exacto para cada artículo seleccionado: no se agrega ni se resta. |
| **Motivo** | Nota opcional, por ejemplo: "Cuenta de stock del almacén del tercer trimestre". |

Haga clic en **Aplicar reconteo** para aplicarlo.

![Página de confirmación de Recontar stock: el card de Artículos de stock seleccionados y un formulario de Detalles de reconteo con la cantidad disponible contada y un motivo rellenados](/static/core/admin/img/help/stock-bulk-actions/recount-stock-confirmation.webp)

A diferencia de las otras dos acciones, el reconteo puede mover el stock en cualquier dirección: hacia arriba si contó más de lo que el sistema esperaba, hacia abajo si contó menos. Si el recuento que ingresa es menor que la cantidad actualmente asignada a pedidos abiertos, Spwig aún lo aplica (un recuento es un hecho, no algo con lo que discutir), pero la figura **Disponible** de ese artículo mostrará como `0` en la lista de stock y su icono de estado cambiará a Agotado: tómelo como una señal de revisar si los pedidos afectados aún se pueden cumplir.

Cada reconteo se registra como un movimiento de **Reconteo físico**, con la cantidad que muestra la corrección (positiva o negativa) entre las figuras antiguas y nuevas de stock disponible.

## Revisar lo que cambió

Cada transferencia, escritura y reconteo se registra de la misma manera que cualquier otro cambio de stock:

- Abra un artículo de stock y desplácese hasta la sección **Movimientos de stock** para ver su historial completo
- O navegue hasta **Productos > Movimientos de stock** para revisar movimientos en todos los artículos, filtrables por tipo

Cada entrada registra el tipo de movimiento, el cambio de cantidad, las figuras antiguas y nuevas de stock disponible, quién realizó el cambio y el motivo que ingresó (si lo hubiera): por lo tanto, una transferencia o escritura en masa es tan rastreable como un ajuste manual individual.

## Consejos

- Ejecute **Recontar stock** inmediatamente después de una cuenta física del stock, mientras los números contados estén frescos: es más fácil detectar un error de escritura en la página de confirmación que desentrañarlo más tarde del historial de movimientos.
- Siempre complete **Motivo** para escrituras y reconteos. dentro de seis meses, "Daño por agua durante el almacenamiento" es mucho más útil en el registro de auditoría que un campo vacío.
- Antes de transferir stock, revise la columna **Disponible** en la página de confirmación: ya tiene en cuenta las unidades asignadas, por lo que podrá saber de inmediato si una cantidad es demasiado alta para uno de los artículos que seleccionó.
- Estas acciones aplican la misma cantidad a cada artículo seleccionado. Agrupe su selección por artículos que realmente necesiten la misma cantidad movida, escrita o recontada, y maneje las excepciones uno por uno.
- Si utiliza un POS en una ubicación de venta al por menor, recuerde que el stock del almacén no forma parte de "disponible" para pedidos en línea: pero las transferencias en masa y las escrituras aún funcionan contra el total real de stock disponible del almacén.