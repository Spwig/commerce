---
title: Gestión de Pedidos
---

Esta guía cubre todo lo que necesita para gestionar los pedidos de sus clientes, desde la revisión de nuevos pedidos hasta el procesamiento de envíos y la gestión de reembolsos.

## Lista de Pedidos

Navegue a **Pedidos > Todos los Pedidos** en la barra lateral para ver todos los pedidos. La lista muestra el número, estado, cliente, total y fecha de cada pedido.

![Order list](/static/core/admin/img/help/manage-orders/order-list.webp)

Utilice los filtros en la parte superior para acotar pedidos por estado, rango de fechas, o busque por número de pedido o nombre del cliente.

## Detalle del Pedido

Haga clic en cualquier pedido para abrir su página de detalle. Aquí encontrará toda la información sobre el pedido organizada en secciones claras.

![Order detail](/static/core/admin/img/help/manage-orders/order-detail.webp)

### Información del Pedido

La sección superior muestra:

- **Número de Pedido** — El identificador único de este pedido
- **Estado** — Estado actual del pedido (Pendiente, En Proceso, Enviado, Entregado, Completado, Cancelado)
- **Cliente** — Nombre y correo electrónico del cliente que realizó el pedido
- **Creado** — Cuándo se realizó el pedido

### Artículos del Pedido

La sección de artículos enumera todo lo que el cliente pidió:

- Nombre del producto y SKU
- Cantidad pedida
- Precio unitario y total de la línea
- Cualquier descuento aplicado

### Detalles de Pago

Muestra el método de pago utilizado, el ID de transacción y el estado del pago. Para pedidos pendientes de pago, puede rastrear el estado de la pasarela de pago aquí.

### Dirección de Envío

La dirección de entrega del cliente. Si la dirección de facturación es diferente, se muestran ambas.

## Ciclo de Vida del Pedido

Los pedidos normalmente pasan por estos estados:

1. **Pendiente** — Nuevo pedido recibido, esperando confirmación de pago
2. **En Proceso** — Pago confirmado, preparando para envío
3. **Enviado** — Pedido despachado con información de seguimiento
4. **Entregado** — El cliente recibió el pedido
5. **Completado** — Pedido finalizado

## Procesamiento de un Pedido

### 1. Revisar el Pedido

Verifique que:

- Los artículos y cantidades son correctos
- La dirección de envío está completa
- Se ha recibido el pago
- Cualquier nota del cliente ha sido atendida

### 2. Crear un Envío

Para enviar el pedido:

1. Haga clic en **Crear Envío** en la página de detalle del pedido
2. Seleccione qué artículos incluir (para envíos parciales, seleccione solo algunos artículos)
3. Elija el transportista y el servicio de envío
4. Introduzca el número de seguimiento
5. Haga clic en **Guardar Envío**

El estado del pedido se actualiza automáticamente a **Enviado** y el cliente recibe un correo electrónico de notificación de envío con la información de seguimiento.

### 3. Marcar como Entregado

Una vez que el cliente confirma la entrega o el seguimiento muestra que fue entregado, actualice el estado a **Entregado** y luego a **Completado**.

## Acciones del Pedido

### Agregar Notas

Añada notas internas o mensajes visibles para el cliente:

1. Desplácese hasta la sección **Notas** en la página de detalle del pedido
2. Escriba su mensaje
3. Elija si es una nota interna (solo personal) o una notificación al cliente
4. Haga clic en **Agregar Nota**

Las notas visibles para el cliente generan una notificación por correo electrónico.

### Procesar un Reembolso

Para emitir un reembolso:

1. Haga clic en **Reembolso** en la página de detalle del pedido
2. Seleccione los artículos a reembolsar (o introduzca un monto personalizado)
3. Elija un motivo de reembolso
4. Confirme el reembolso

Los reembolsos se procesan a través de la pasarela de pago original. El cliente recibe una confirmación por correo electrónico.

### Cancelar un Pedido

Para cancelar:

1. Haga clic en **Cancelar Pedido**
2. Seleccione un motivo de cancelación
3. Elija si desea reponer el inventario de los artículos
4. Confirme

El cliente es notificado automáticamente y se inicia un reembolso si el pago ya fue realizado.

## Acciones Masivas

Desde la lista de pedidos, puede seleccionar múltiples pedidos y aplicar acciones masivas:

- **Actualizar estado** — Mover varios pedidos al mismo estado
- **Exportar** — Descargar los pedidos seleccionados como CSV
- **Imprimir** — Generar albaranes o facturas

## Notificaciones de Pedidos

Los clientes reciben automáticamente correos electrónicos en las etapas clave:

- **Confirmación de pedido** — Inmediatamente después de realizar el pedido
- **Pago recibido** — Cuando se confirma el pago
- **Notificación de envío** — Cuando se crea un envío (incluye enlace de seguimiento)
- **Confirmación de entrega** — Cuando se marca como entregado

Configure las plantillas de correo electrónico en **Configuración > Configuración de Correo Electrónico**.

## Consejos

- Procese los pedidos diariamente para mantener tiempos de envío rápidos.
- Utilice los filtros de estado para centrarse en los pedidos que necesitan atención (Pendiente y En Proceso).
- Añada notas internas para rastrear cualquier requisito de manejo especial.
- Para períodos de alto volumen, utilice acciones masivas para actualizar múltiples pedidos a la vez.
- Configure reglas de envío para automatizar la selección del transportista según el peso del pedido y el destino.
