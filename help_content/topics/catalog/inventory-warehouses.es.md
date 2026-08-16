---
title: Inventario y Almacenes
---

El sistema de almacenes le permite gestionar el inventario en múltiples ubicaciones, establecer prioridades de cumplimiento y seguir los niveles de stock en tiempo real. Navegue hasta **Productos > Almacenes** en la barra lateral de administración para gestionar sus ubicaciones de almacén.

![Lista de almacenes](/static/core/admin/img/help/inventory-warehouses/warehouse-list.webp)

## Almacenes

### Lista de Almacenes

La página de almacén muestra todas sus ubicaciones de inventario como tarjetas con:

- **Nombre y código** — Identificador del almacén (por ejemplo, "Almacén principal", código "MAIN-WH")
- **Región de ventas** — Asignación de región geográfica
- **Estados** — Activo/inactivo, ubicación de venta al por menor
- **Estadísticas** — Productos almacenados, prioridad de cumplimiento, porcentaje de reserva de stock
- **Ubicación** — Ciudad y país
- **Última actualización** — Cuándo se modificaron por última vez los niveles de stock

### Crear un almacén

1. Haga clic en **+ Añadir Almacén**
2. Complete la **Información Básica**:
   - **Nombre** — Etiqueta descriptiva (por ejemplo, "Almacén de EE.UU. Este")
   - **Código** — Identificador único corto (por ejemplo, "US-EAST") — debe ser único en todos los almacenes
   - **Región de ventas** — Asignar a una región geográfica para el enrutamiento de cumplimiento
   - **Activo** — Habilitar para incluirlo en el cumplimiento
3. Complete la sección **Dirección** con la dirección completa del almacén
4. Configure **Configuración de Cumplimiento**:
   - **Prioridad de Cumplimiento** — Números más altos = mayor prioridad para el cumplimiento de pedidos
   - **Porcentaje de Reserva de Stock** — Porcentaje de stock que se reserva como reserva de seguridad (0–100)
   - **Ubicación de Envío** — Opcionalmente, vincular a una ubicación de recogida si este almacén admite la recogida por parte del cliente
5. Configure **Visualización para el Cliente** (opcional):
   - **Nombre para Mostrar** — Etiqueta visible para el cliente (por ejemplo, "Envío desde Australia"). Deje en blanco para usar el nombre del almacén.
   - **Mostrar en la Página Principal** — Mostrar el origen de este almacén a los clientes en las páginas de productos
6. Configure **Punto de Venta / Tienda de Venta al por menor** (opcional):
   - **Ubicación de Venta al por Menos** — Marcar si este almacén también sirve como tienda física con terminales de Punto de Venta
   - **Nombre para Mostrar en Punto de Venta** — Nombre corto que se muestra en la interfaz de Punto de Venta
   - **Grupo de Tiendas** — Asignar a un grupo de tiendas de Punto de Venta para heredar configuraciones
7. Agregue **Información de Contacto** si es necesario (nombre, correo electrónico, teléfono)
8. Haga clic en **Guardar"

### Prioridad de Cumplimiento

Cuando llega un pedido, el sistema selecciona el mejor almacén según:

1. **Valor de prioridad** — Almacenes con mayor prioridad son preferidos
2. **Disponibilidad de stock** — Debe tener suficiente stock
3. **Coincidencia de región** — Los almacenes en la región del cliente son preferidos

Por ejemplo, si tiene un almacén de EE.UU. (prioridad 100) y un almacén de la UE (prioridad 60), los pedidos de EE.UU. se cumplirán desde el almacén de EE.UU. primero.

### Porcentaje de Reserva de Stock

El porcentaje de reserva de stock reserva un porcentaje de inventario que no se venderá en línea. Esto es útil para:

- Tiendas físicas de venta al por menor que necesitan stock en el mostrador
- Stock de seguridad para evitar la venta en exceso
- Inventario reservado para pedidos mayoristas

Un 10% de reserva en 100 unidades significa que solo 90 unidades están disponibles para pedidos en línea.

## Artículos de Stock

Los artículos de stock representan el inventario real de un producto específico en un almacén específico.

### Ver Niveles de Stock

1. Haga clic en el **icono de stock** en cualquier tarjeta de almacén para ver sus artículos de stock
2. O navegue hasta la pestaña **Inventario** de un producto para ver el stock en todos los almacenes

Cada artículo de stock muestra:

- **Nombre del producto** y variante (si aplica)
- **En mano** — Inventario físico total
- **Asignado** — Cantidad reservada para pedidos pendientes
- **Disponible** — En mano menos asignado (lo que se puede vender)

### Añadir stock

1. Navegue hasta **Productos > Artículos de Stock** y haga clic en **+ Añadir Artículo de Stock**, o
2. Abra el formulario de edición de un producto y use la sección **Artículos de Stock** en el fondo
3. Seleccione el **producto** y el **almacén** (y opcionalmente una **variante** para productos variables)
4. Ingrese la cantidad **en mano**
5. Establezca el **umbral de bajo stock** — este umbral por artículo activa una alerta de bajo stock
6. Guarde

### Movimientos de Stock

Cada cambio en el inventario se registra como un **movimiento de stock**:

| Tipo de movimiento | Descripción |
|--------------|-------------|
| **Entrada** | Nuevo stock recibido del proveedor |
| **Venta** | Stock deducido por un pedido cumplido |
| **Devolución** | Stock devuelto por un cliente |
| **Ajuste** | Corrección manual (diferencia en el conteo) |
| **Transferencia** | Movido entre almacenes |
| **Reserva** | Mantenido temporalmente para un carrito activo |
| **Daño** | Cancelado como dañado o perdido |
| **Reconteo** | Corregido para coincidir con un conteo físico del inventario |

Los movimientos de inventario proporcionan un registro completo de los cambios en el inventario. Más allá de la acción **Ajustar los niveles de stock**, Spwig también ofrece acciones en masa en la lista de artículos de stock para transferir, escribir fuera y recount stock en muchos artículos a la vez — véase [Acciones de stock en masa](/help/stock-bulk-actions).

## Seguimiento del inventario en productos

### Habilitar el seguimiento del inventario

En la sección **Inventario** de un producto:

1. Active **Seguimiento del inventario** para habilitar la gestión de stock para este producto
2. Establezca el **Umbral de bajo stock** — activa alertas en el tablero cuando el stock en cualquier almacén caiga por debajo de este nivel
3. Configure **Permitir devoluciones** si quiere aceptar pedidos cuando esté agotado
4. Opcionalmente, establezca una **Acción de agotado** para reemplazar el comportamiento del sitio o categoría para este producto específico

Después de habilitar el seguimiento, gestione las cantidades reales de stock usando la sección **Artículos de stock** integrada en la parte inferior del formulario del producto, o a través de **Productos > Artículos de stock**.

### Stock en múltiples almacenes

Cuando el seguimiento del inventario está habilitado, la pestaña de inventario muestra los niveles de stock en todos los almacenes en una tabla resumen:

- Total en mano en todas las ubicaciones
- Desglose por almacén
- Cantidad disponible después de reservas y asignaciones

## Alertas de bajo stock

El sistema monitorea automáticamente los niveles de stock y alerta cuando:
- Un producto cae por debajo de su **límite de bajo stock**
- Un producto alcanza **cero stock disponible**

Las alertas de bajo stock aparecen en:
- El **Tablero de tienda** en la sección Acciones Pendientes
- La lista de productos con un indicador visual

## Consejos

- Comience con un solo almacén y agregue más a medida que crezca su negocio.
- Establezca prioridades de cumplimiento según la velocidad y el costo del envío a cada región.
- Use buffers de stock para ubicaciones de venta minorista para garantizar la disponibilidad de stock en el piso.
- Revise regularmente los movimientos de stock para identificar pérdidas o discrepancias.
- Establezca umbrales de bajo stock basados en su tiempo de reorden — si toma 2 semanas restablecer el stock, establezca el umbral para cubrir 2 semanas de ventas.
- Habilite el seguimiento del inventario antes de lanzar para evitar ventas excesivas.