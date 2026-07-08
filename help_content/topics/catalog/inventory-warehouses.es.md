---
title: Inventario y Almacenes
---

El sistema de almacenes le permite gestionar el inventario en múltiples ubicaciones, establecer prioridades de cumplimiento y realizar un seguimiento de los niveles de stock en tiempo real. Navegue a **Configuración > Gestión de Licencias** en la barra lateral, o acceda a los almacenes desde la pestaña de inventario del producto.

![Lista de almacenes](/static/core/admin/img/help/inventory-warehouses/warehouse-list.webp)

## Almacenes

### Lista de Almacenes

La página de almacenes muestra todas sus ubicaciones de inventario como tarjetas con:

- **Nombre y código** — Identificador del almacén (ej., "Almacén Principal", código "MAIN-WH")
- **Región de ventas** — Asignación de región geográfica
- **Insignias de estado** — Activo/inactivo, ubicación de venta al público
- **Estadísticas** — Productos almacenados, prioridad de cumplimiento, porcentaje de reserva de stock
- **Ubicación** — Ciudad y país
- **Última actualización** — Cuándo se modificaron por última vez los niveles de stock

### Crear un Almacén

1. Haga clic en **+ Añadir Almacén**
2. Complete los detalles del almacén:
   - **Nombre** — Etiqueta descriptiva (ej., "Almacén Este de EE.UU.")
   - **Código** — Identificador único corto (ej., "US-EAST")
   - **Región de Ventas** — Asignar a una región geográfica para el enrutamiento de cumplimiento
   - **Dirección** — Dirección completa del almacén para cálculos de envío
3. Configure los ajustes:
   - **Activo** — Habilitar para incluir en el cumplimiento
   - **Ubicación de Venta al Público** — Marcar si este almacén también funciona como tienda física
   - **Prioridad de Cumplimiento** — Los números más altos significan mayor prioridad para el cumplimiento de pedidos
   - **Reserva de Stock** — Porcentaje de stock que se reserva como margen de seguridad
4. Haga clic en **Guardar**

### Prioridad de Cumplimiento

Cuando llega un pedido, el sistema selecciona el mejor almacén basándose en:

1. **Valor de prioridad** — Los almacenes con mayor prioridad son preferidos
2. **Disponibilidad de stock** — Debe tener stock suficiente
3. **Coincidencia de región** — Se prefieren los almacenes en la región del cliente

Por ejemplo, si tiene un almacén en EE.UU. (prioridad 100) y un almacén en la UE (prioridad 60), los pedidos de EE.UU. se cumplirán primero desde el almacén de EE.UU.

### Reserva de Stock

La reserva de stock reserva un porcentaje del inventario que no se venderá en línea. Esto es útil para:
- Tiendas físicas que necesitan stock de exposición
- Stock de seguridad para prevenir la sobreventa
- Inventario reservado para pedidos mayoristas

Una reserva del 10% sobre 100 unidades significa que solo 90 unidades están disponibles para pedidos en línea.

## Artículos de Stock

Los artículos de stock representan el inventario real de un producto específico en un almacén específico.

### Ver Niveles de Stock

1. Haga clic en el **icono de stock** en cualquier tarjeta de almacén para ver sus artículos de stock
2. O navegue a la pestaña **Inventario** de un producto para ver el stock en todos los almacenes

Cada artículo de stock muestra:
- **Nombre del producto** y variante (si corresponde)
- **Disponible** — Inventario físico total
- **Asignado** — Cantidad reservada para pedidos pendientes
- **Disponible para venta** — Disponible menos asignado (lo que se puede vender)

### Añadir Stock

1. Desde la vista de stock del almacén, haga clic en **Añadir Artículo de Stock**
2. Seleccione el producto y la variante
3. Introduzca la cantidad **disponible**
4. Guarde

### Movimientos de Stock

Cada cambio en el inventario se registra como un **movimiento de stock**:

| Tipo de Movimiento | Descripción |
|--------------------|-------------|
| **Recepción** | Nuevo stock recibido del proveedor |
| **Venta** | Stock deducido para un pedido cumplido |
| **Devolución** | Stock devuelto por un cliente |
| **Ajuste** | Corrección manual (discrepancia en el conteo) |
| **Transferencia** | Trasladado entre almacenes |
| **Reserva** | Retenido temporalmente para un carrito activo |

Los movimientos de stock proporcionan un registro de auditoría completo de los cambios en el inventario.

## Seguimiento de Inventario en Productos

### Habilitar el Seguimiento de Inventario

En la pestaña **Inventario** de un producto:

1. Active **Seguimiento de Inventario** para habilitar la gestión de stock
2. Establezca el **Umbral de Stock Bajo** — activa alertas cuando el stock cae por debajo de este nivel
3. Configure **Permitir Pedidos Pendientes** si desea aceptar pedidos cuando no hay stock

### Stock en Múltiples Almacenes

Cuando el seguimiento de inventario está habilitado, la pestaña Inventario muestra los niveles de stock en todos los almacenes en una tabla resumen:

- Total disponible en todas las ubicaciones
- Desglose por almacén
- Cantidades disponibles después de reservas y asignaciones

## Alertas de Stock Bajo

El sistema monitorea automáticamente los niveles de stock y le alerta cuando:
- Un producto cae por debajo de su **umbral de stock bajo**
- Un producto alcanza **stock disponible cero**

Las alertas de stock bajo aparecen en:
- El **Panel de Control de la Tienda** en la sección de Acciones Requeridas
- La lista de productos con un indicador visual

## Consejos

- Comience con un solo almacén y añada más a medida que su negocio crezca.
- Establezca las prioridades de cumplimiento basándose en la velocidad de envío y el coste a cada región.
- Use reservas de stock para ubicaciones de venta al público para asegurar la disponibilidad de stock de exposición.
- Revise los movimientos de stock regularmente para identificar pérdidas o discrepancias.
- Establezca umbrales de stock bajo basándose en su tiempo de reabastecimiento — si tarda 2 semanas en reponer, establezca el umbral para cubrir 2 semanas de ventas.
- Habilite el seguimiento de inventario antes de lanzar la tienda para evitar la sobreventa.
