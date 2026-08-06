---
title: Gestión de suscripciones de clientes
---

La sección de suscripciones de clientes le brinda una vista completa de todas las suscripciones recurrentes activas, pausadas y canceladas en su tienda. Desde aquí puede supervisar la salud de la facturación, ver los detalles individuales de la suscripción y tomar acciones cuando surjan problemas.

## Visualización de suscripciones de clientes

Navegue hasta **Suscripciones > Suscripciones de clientes** para ver la lista completa de suscripciones de todos los clientes.

![Lista de suscripciones de clientes](/static/core/admin/img/help/managing-subscriptions/subscription-list.webp)

La lista muestra el cliente, el nombre del plan, el estado actual, la fecha de próxima facturación y la cantidad de ciclos de facturación completados de cada suscripción.

### Filtros y búsqueda

Use el panel de filtros en el lado derecho para reducir las suscripciones por:

- **Estado** — Filtrar por Activo, Prueba, Vencido, Pausado, Cancelado o Expirado
- **Plan** — Ver las suscripciones para un plan específico
- **Modo del proveedor** — Nativo (gestionado por Stripe/PayPal) o Respaldo (facturación interna)

Use la barra de búsqueda para encontrar suscripciones por dirección de correo electrónico del cliente.

## Estados de las suscripciones

Entender cada estado le ayuda a identificar las suscripciones que requieren atención:

| Estado | Qué significa |
|--------|----------------|
| **Prueba** | El cliente se encuentra en el período de prueba gratuito o con precio reducido |
| **Activo** | La suscripción está saludable — la facturación está al día y el acceso está activo |
| **Vencido** | Un intento de pago falló — el sistema está reintentando. El cliente mantiene el acceso durante el período de gracia |
| **Pausado** | La suscripción está suspendida temporalmente — no hay facturación, no hay acceso |
| **Cancelado** | Se ha solicitado la cancelación. El cliente puede que aún tenga acceso hasta la fecha de finalización del período |
| **Expirado** | La suscripción ha finalizado por completo — la prueba expiró, se alcanzó el número máximo de ciclos de facturación o se agotó el período de cancelación |

Las suscripciones que estén en **Vencido** requieren más atención — si la facturación continúa fallando y el período de gracia se agota, la suscripción será suspendida.

## Visualización de los detalles de una suscripción

Haga clic en cualquier suscripción para abrir la vista de detalles. Esto muestra:

### Período de facturación actual

- **Inicio / Fin del período actual** — Las fechas de la ventana de facturación activa
- **Fecha de próxima facturación** — Cuándo se intentará la próxima carga
- **Fecha de última facturación** y **Estado de última facturación** — El resultado del último intento de facturación
- **Cantidad de ciclos de facturación** — Cuántos ciclos de facturación exitosos se han completado

### Información de la suscripción

- **Plan** y **Nivel de precios** — Qué plan y frecuencia de facturación tiene el cliente
- **Producto / Variante** — El producto del catálogo vinculado a esta suscripción (si aplica)
- **Cantidad** — Número de asientos o unidades (para planes basados en cantidad)
- **Token de pago** — El método de pago almacenado que se utiliza para la facturación recurrente

### Detalles de la prueba

Si la suscripción está en prueba, la **Fecha de finalización de la prueba** muestra cuándo expira la prueba del cliente y comienza la facturación completa.

### Detalles de la cancelación

Para suscripciones canceladas, puede ver:

- **Tipo de cancelación** — Si la cancelación fue inmediata, al final del período o programada
- **Cancelado a las** — Cuándo se solicitó la cancelación
- **Motivo de la cancelación** — Notas sobre por qué el cliente se canceló (si se registró)
- **Fecha límite de reactivación** — La última fecha en que el cliente puede reactivar sin volver a suscribirse desde cero

### Período de gracia y compromisos

- **Fecha de finalización del período de gracia** — Si un pago falló, esto muestra la fecha límite antes de que se suspenda el acceso
- **Fecha de finalización del compromiso mínimo** — Para planes con compromisos mínimos, la fecha más temprana para cancelar

## Pausar una suscripción

Una suscripción pausada detiene temporalmente la facturación y también suspende el acceso. Esto es útil para clientes que desean tomar un descanso sin cancelar por completo.

Para ver suscripciones pausadas, filtre por **Estado: Pausado**. La vista de detalle muestra:

- **Pausado a las** — Cuándo comenzó la pausa
- **Motivo de la pausa** — Notas sobre por qué se pausó
- **Fecha de reanudación automática** — Si se establece, la fecha en que la suscripción se reanudará automáticamente con facturación y acceso

Las suscripciones se reanudan en la fecha de reanudación automática o cuando el cliente active manualmente la suscripción.

## Registros del ciclo de facturación

Cada intento de facturación - ya sea exitoso o fallido - se registra en el historial del ciclo de facturación. Navegue a **Suscripciones > Registros del ciclo de facturación** para ver este historial.

![Lista de registros del ciclo de facturación](/static/core/admin/img/help/managing-subscriptions/billing-cycle-log.webp)

### Leer una entrada del registro del ciclo de facturación

Cada entrada del registro registra:

- **Suscripción** - A qué suscripción del cliente pertenece este intento de facturación
- **Número de ciclo** - Ciclo de facturación secuencial (Ciclo 1 = primer cargo después de la prueba)
- **Fecha de facturación** - Cuándo se intentó el cargo
- **Estado** - Pendiente, Procesando, Exitoso, Fallido o Reintentando
- **Desglose de monto**:
  - **Monto base** - El precio del plan antes de cualquier ajuste
  - **Monto de cantidad** - Cargo adicional por la cantidad de asientos/unidades
  - **Monto de complementos** - Costo total de complementos activos
  - **Monto de descuento** - Descuentos aplicados totales
  - **Monto total** - El monto final cobrado (o intentado)
- **Método de pago** - La tarjeta o método de pago utilizado
- **ID de transacción del proveedor** - El número de referencia del proveedor de pago (útil para búsquedas de reembolso)
- **Razón del fallo** - Si la facturación falló, por qué falló (por ejemplo, tarjeta rechazada, fondos insuficientes)

### Diagnosticar fallos en el pago

Si un cliente se pone en contacto con usted sobre un problema de facturación, encuentre su suscripción y revise los registros del ciclo de facturación. El campo **Razón del fallo** explica qué salió mal. Las razones comunes de fallo incluyen:

- **Tarjeta rechazada** - La tarjeta del cliente fue rechazada por su banco
- **Fondos insuficientes** - El saldo de la cuenta era demasiado bajo en el momento de la facturación
- **Tarjeta caducada** - El método de pago guardado ha caducado
- **Error de red** - Un problema de conexión temporal con el proveedor de pago - generalmente se resuelve al reintentar

Para fallos persistentes, dirija al cliente a actualizar su método de pago en la configuración de su cuenta.

## Cómo se cumplen las renovaciones

Cada cargo exitoso de renovación crea un nuevo pedido pagado para ese ciclo de facturación - no es solo un registro de pago. Ese pedido pasa por su proceso normal de cumplimiento exactamente como lo haría un pedido realizado en el checkout:

- **Productos físicos** - El pedido de renovación entra en la cola regular de cumplimiento para recoger, empaquetar y enviar. No se asigna automáticamente stock al instante en que se cobra la tarjeta, por lo que un déficit temporal de stock nunca bloquea un cargo que ya tuvo éxito - aún verá el pedido y podrá cumplirlo según el stock disponible.
- **Productos digitales** - El acceso (enlaces de descarga, claves de licencia) se vuelve a otorgar automáticamente en el momento en que se crea el pedido de renovación, de la misma manera que lo haría para una compra por primera vez.

Los pedidos de renovación copian los datos de envío y facturación del pedido que inició la suscripción, por lo que no necesita volver a ingresar nada. No llevan un sello especial en la lista de **Pedidos**, pero siempre puede rastrear un ciclo específico hacia su pedido: abra **Suscripciones > Registros del ciclo de facturación**, haga clic en la entrada del registro de ese ciclo y el campo **Pedido** lo lleva directamente a él.

## Correos electrónicos de suscripción automática

Spwig envía correos electrónicos de ciclo de vida de suscripción automáticamente, no necesita dispararlos manualmente. Los que más preguntan los comerciantes son:

| Correo electrónico | Cuándo se envía |
|-------|----------------|
| **Recordatorio de renovación** | Antes de un cargo de renovación próximo |
| **Finalización de prueba** | Antes de que un período de prueba gratuito o con descuento se convierta en facturación completa |
| **Pago fallido** | Inmediatamente después de que un cargo de renovación falle, y nuevamente como notificación final si el período de gracia está a punto de agotarse (dunning) |
| **Confirmación de cancelación** | Cuando se cancela una suscripción |

Spwig también envía correos electrónicos de bienvenida, pago exitoso, pausa/retomada, vencimiento, reactivación, cambio de plan y vencimiento de método de pago en los puntos relevantes en el ciclo de vida de una suscripción.

Todos estos son plantillas de correo electrónico comunes — consulte [Plantillas de correo electrónico](/help/email-templates) para revisar o personalizar su contenido y asegurarse de que estén activas.

## Autoatención del cliente

Los clientes no necesitan contactar con usted para cambios de suscripción rutinarios — pueden gestionar sus propias suscripciones desde su cuenta: ver detalles y historial de facturación, pausar, reanudar, cancelar y actualizar el método de pago registrado. Esto cubre la mayor parte de lo que de otro modo llegaría a su cola de soporte, por lo que, cuando un cliente se pone en contacto sobre su suscripción, vale la pena comprobar primero si han probado la página de su cuenta antes de realizar el cambio por ellos en el administrador.

## Consejos

- Revise la opción de **Vencidas** semanalmente para detectar suscripciones en riesgo de cancelación. Un correo electrónico rápido al cliente suele resolver problemas de pago antes de que expire el período de gracia.
- Los registros de ciclos de facturación son de solo lectura — se crean automáticamente y no se pueden modificar. Esto garantiza un registro de auditoría confiable.
- Si la suscripción de un cliente muestra **Vencida** pero ya ha actualizado su método de pago, el siguiente intento automático recogerá la nueva tarjeta. Los intentos siguen el horario configurado en el plan.
- Las suscripciones **Expiradas** no se eliminan — permanecen visibles para informes. Use los filtros de fecha para centrarse en suscripciones actualmente activas.
- Para suscripciones en **Prueba**, consulte la **Fecha de finalización de la prueba** para anticipar cargos futuros y abordar proactivamente cualquier problema con el método de pago.
- Si un cliente dice que un renovación física "no ha sido enviada", revise su cola regular de envío en lugar de la tarjeta de suscripción — los pedidos de renovación se envían de la misma manera que cualquier otro pedido y no saltan la cola.