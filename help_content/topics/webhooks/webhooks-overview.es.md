---
title: Visión general de webhooks
---

Los webhooks permiten que tu tienda notifique automáticamente a sistemas externos — como herramientas de inventario, ERPs, servicios de cumplimiento o aplicaciones personalizadas — cuando ocurra algo en tu tienda. En lugar de que esos sistemas pregunten repetidamente "¿ha cambiado algo?", tu tienda envía una notificación en el momento en que ocurre un evento.

## ¿Qué hacen los webhooks

Cuando ocurre un evento en tu tienda (se coloca un pedido, se recibe un pago, un producto se agota), Spwig envía una solicitud HTTP POST con los datos del evento a una URL que configures. El sistema receptor puede actuar inmediatamente sobre esos datos — por ejemplo, actualizar el inventario, generar una etiqueta de envío o enviar una notificación personalizada.

Usos comunes de los webhooks incluyen:

- Sincronizar pedidos en tiempo real con un socio de cumplimiento
- Actualizar el inventario en un ERP cuando cambie el stock
- Triggers de SMS o notificaciones push para cambios en el estado del pedido
- Registrar eventos en un almacén de datos para informes
- Conectar con herramientas de automatización como Zapier o Make

## Ver y gestionar endpoints

Navega a **Integrations > Webhooks** para ver todos tus endpoints de webhook configurados.

![Lista de endpoints de webhook](/static/core/admin/img/help/webhooks-overview/endpoint-list.webp)

La lista muestra el nombre de cada endpoint, su URL, su estado activo, cuántos eventos suscribe, su estado de salud y cuándo recibió por última vez una entrega.

### Indicadores de salud

La columna **Salud** muestra a simple vista cómo está funcionando cada endpoint:

- **Saludable** — Todas las entregas recientes han tenido éxito
- **Degradado** — Algunos fallos recientes, pero el endpoint sigue activo
- **No saludable / Deshabilitado** — El endpoint se deshabilitó automáticamente después de demasiados fallos consecutivos (10 por defecto). Debes habilitarlo manualmente una vez que se resuelva el problema subyacente.

## Crear un endpoint de webhook

Haz clic en **+ Añadir endpoint de webhook** para abrir el asistente de configuración. El asistente te guía a través de cuatro pasos.

### Paso 1: Información básica

- **Nombre** — Una etiqueta amigable para identificar este endpoint (por ejemplo, `Servicio de cumplimiento de pedidos` o `Sincronización de inventario`).
- **URL** — La URL completa del servidor que recibirá las solicitudes POST de webhook. Esto debe ser accesible públicamente (no una URL de localhost).
- **Descripción** — Notas opcionales sobre qué se usa este endpoint.
- **Activo** — Si este endpoint debe recibir entregas. Desmarcarlo para pausarlo temporalmente sin eliminar el endpoint.

### Paso 2: Suscripciones a eventos

Elige qué eventos deben desencadenar una entrega a este endpoint. Los eventos se agrupan por categoría:

### Eventos de pedido

| Evento | Cuando se dispara |
|-------|---------------|
| `order.created` | Se coloca un nuevo pedido |
| `order.paid` | Se confirma el pago de un pedido |
| `order.cancelled` | Se cancela un pedido |
| `order.fulfilled` | Todos los artículos de un pedido se envían |
| `order.partially_fulfilled` | Algunos artículos de un pedido se envían |
| `order.status_changed` | Cambia el estado del pedido |
| `order.note_added` | Se añade una nota a un pedido |

### Eventos de pago

| Evento | Cuando se dispara |
|-------|---------------|
| `payment.received` | Se recibe un pago |
| `payment.failed` | Un intento de pago falla |
| `payment.pending` | Un pago está esperando confirmación |

### Eventos de envío

| Evento | Cuando se dispara |
|-------|---------------|
| `shipment.created` | Se crea un envío |
| `shipment.shipped` | Se envía un envío |
| `shipment.delivered` | Se entrega un envío |
| `shipment.returned` | Se devuelve un envío |
| `shipment.tracking_updated` | Se actualiza la información de seguimiento |

### Eventos de inventario

| Evento | Cuando se dispara |
|-------|---------------|
| `inventory.low_stock` | El stock cae por debajo del umbral |
| `inventory.out_of_stock` | Un producto se agota |
| `inventory.restocked` | Un producto se reabastece |
| `inventory.adjusted` | El inventario se ajusta manualmente |

### Eventos de producto

`product.created`, `product.updated`, `product.deleted`, `product.published`, `product.unpublished`

### Eventos de cliente


customer.created`, `customer.updated`, `customer.deleted`

#### Eventos de suscripción

`subscription.created`, `subscription.activated`, `subscription.renewed`, `subscription.cancelled`, `subscription.expired`, `subscription.paused`, `subscription.resumed`, `subscription.payment_failed`

#### Otros eventos

`refund.created`, `refund.completed`, `refund.failed`, `cart.abandoned`, `cart.recovered`, `translation.job_completed`, `translation.job_failed`

Para recibir todos los eventos, suscríbase a `*` (comodín). Esto es útil para puntos de conexión de registro de propósito general, pero genera más tráfico — suscríbase solo a los eventos que realmente necesite para integraciones de producción.

### Paso 3: Configuración

- **Máximo de reintentos** — Cuántas veces Spwig debe intentar enviar un mensaje fallido antes de abandonar (por defecto: 5). Cada reintento utiliza un espaciado de retroceso exponencial.
- **Tiempo de espera (segundos)** — Cuánto tiempo esperar a que el servidor receptor responda antes de marcar la entrega como fallida (por defecto: 30 segundos). Aumente este valor solo si su servidor es conocido por ser lento.

### Paso 4: Seguridad

Cada punto de conexión de webhook obtiene una **clave de firma generada automáticamente** — una clave aleatoria de 64 caracteres. Spwig utiliza esta clave para firmar cada carga útil de webhook con una firma HMAC-SHA256.

La firma se incluye en el encabezado de solicitud `X-Webhook-Signature`. Su servidor receptor debe verificar esta firma para confirmar que la solicitud realmente provino de su tienda y no fue manipulada.

La clave se muestra enmascarada en la administración. Para ver o rotar la clave, use la API de Spwig. Rotar su clave inmediatamente si sospecha que ha sido comprometida.

## Habilitar y deshabilitar puntos de conexión

Para habilitar o deshabilitar uno o más puntos de conexión rápidamente sin abrir cada uno:

1. Seleccione las casillas junto a los puntos de conexión que desee cambiar
2. Use el menú desplegable **Acción** para elegir **Habilitar puntos de conexión seleccionados** o **Deshabilitar puntos de conexión seleccionados**
3. Haga clic en **Ir**

Para reactivar un punto de conexión que se haya deshabilitado automáticamente debido a errores, selecciónelo y use la acción **Restablecer contador de errores**, luego habilítelo. Arregle lo que causó los errores primero, de lo contrario se deshabilitará nuevamente rápidamente.

## Consejos

- Suscríbase solo a los eventos que realmente necesite — eventos innecesarios generan ruido en sus registros y aumentan la carga de entrega.
- Siempre verifique la firma del webhook en su servidor receptor antes de procesar la carga útil. Esto lo protege contra solicitudes falsificadas.
- Use el campo **Descripción** para registrar qué sistema o integración conecta este punto de conexión. Esto ayuda al depurar meses más tarde.
- Establezca un **Tiempo de espera** ligeramente por encima del tiempo de respuesta típico de su servidor. Un tiempo de espera de 10–15 segundos es suficiente para la mayoría de las integraciones.
- Si un punto de conexión se vuelve **Inestable**, revise primero los registros de entrega (vea **Entregas de webhook**) para comprender el patrón de falla antes de reactivarlo.
- Para pruebas, dirija los webhooks a una herramienta como [webhook.site](https://webhook.site) para inspeccionar las cargas útiles crudas sin necesidad de un servidor en vivo.