---
title: Gestionar suscripciones de clientes
---

La sección de suscripciones de clientes le da una visión completa de todas las suscripciones recurrentes activas, pausadas y canceladas en su tienda. Desde aquí puede supervisar la salud de las facturaciones, ver detalles de suscripciones individuales y tomar medidas cuando surjan problemas.

## Ver suscripciones de clientes

Navegue hasta **Suscripciones > Suscripciones de clientes** para ver la lista completa de suscripciones de todos los clientes.

![Lista de suscripciones de clientes](/static/core/admin/img/help/managing-subscriptions/subscription-list.webp)

La lista muestra el cliente de cada suscripción, el nombre del plan, el estado actual, la fecha de próxima facturación y el número de ciclos de facturación completados.

### Filtros y búcsqueda

Use el panel de filtros a la derecha para reducir las suscripciones según:

- **Estado** — Filtre por Activo, Prueba, Atrasado, Pausado, Cancelado o Vencido
- **Plan** — Ver suscripciones para un plan específico
- **Modo del proveedor** — Nativo (administrado por Stripe/PayPal) o de respaldo (facturación interna)

Use la barra de búcsqueda para encontrar suscripciones por dirección de correo electrónico del cliente.

## Estados de suscripción

Entender cada estado le ayuda a identificar suscripciones que requieren atención:

| Estado | Qué significa |
|--------|---------------|
| **Prueba** | El cliente está en el período de prueba gratuito o con precio reducido |
| **Activo** | La suscripción está en buen estado — la facturación está al día y el acceso está activo |
| **Atrasado** | Un intento de pago falló — el sistema está intentando nuevamente. El cliente sigue teniendo acceso durante el período de gracia |
| **Pausado** | La suscripción está temporalmente suspendida — sin facturación ni acceso |
| **Cancelado** | Se ha solicitado la cancelación. El cliente puede seguir teniendo acceso hasta la fecha de finalización del período |
| **Vencido** | La suscripción ha terminado completamente — vencimiento de prueba, máximo de ciclos de facturación alcanzado o vencimiento del período de cancelación |

Las suscripciones que están **Atrasadas** requieren la mayor atención — si los pagos continúan fallando y el período de gracia termina, la suscripción se suspenderá.

## Ver detalles de una suscripción

Haga clic en cualquier suscripción para abrir la vista de detalles. Esto muestra:

### Período de facturación actual

- **Inicio / Fin del Período Actual** — Las fechas del ventana de facturación activa
- **Fecha de próxima facturación** — Cuando se intentará la próxima carga
- **Fecha de última facturación** y **Estado de última facturación** — Resultado del último intento de facturación
- **Contador de ciclos de facturación** — Cuántos ciclos de facturación exitosos se han completado

### Información de la suscripción

- **Plan** y **Nivel de precios** — Cuál es el plan y la frecuencia de facturación del cliente
- **Producto / Variante** — El producto del catálogo vinculado a esta suscripción (si aplica)
- **Cantidad** — Número de asientos o unidades (para planes basados en cantidad)
- **Token de pago** — El método de pago almacenado que se utiliza para la facturación recurrente

### Detalles de prueba

Si la suscripción está en prueba, la **Fecha de finalización de la prueba** muestra cuándo expira la prueba del cliente y comienza la facturación completa.

### Detalles de cancelación

Para suscripciones canceladas, puede ver:

- **Tipo de cancelación** — Si la cancelación fue inmediata, al final del período o programada
- **Cancelado en** — Cuándo se solicitó la cancelación
- **Razón de cancelación** — Notas sobre por qué el cliente canceló (si se registró)
- **Fecha límite de reactivación** — La última fecha en la que el cliente puede reactivar sin volver a suscribirse desde el principio

### Período de gracia y compromisos

- **Fecha de finalización del período de gracia** — Si un pago ha fallado, muestra la fecha límite antes de que se suspenda el acceso
- **Fecha de finalización del compromiso mínimo** — Para planes con compromisos mínimos, la fecha más temprana de cancelación

## Pausar una suscripción

Una suscripción pausada detiene temporalmente la facturación mientras también suspende el acceso. Esto es ótil para clientes que desean tomar un descanso sin cancelar completamente.

Para ver suscripciones pausadas, filtre por **Estado: Pausado**. La vista de detalles muestra:

- **Pausado en** — Cuándo comenzó la pausa
- **Razón de pausa** — Notas sobre por qué se pausó
- **Fecha de reanudación automática** — Si se establece, la fecha en la que la suscripción se reanudará automáticamente la facturación y el acceso

Las suscripciones se reanudan ya sea en la fecha de reanudación automática o cuando el cliente reactive manualmente la suscripción.

## Registros del ciclo de facturación

Cada intento de facturación — exitoso o fallido — se registra en el log del ciclo de facturación. Navegue hasta **Suscripciones > Registros del Ciclo de Facturación** para ver este historial.

![Lista de registros del ciclo de facturación](/static/core/admin/img/help/managing-subscriptions/billing-cycle-log.webp)

### Leer una entrada del registro del ciclo de facturación

Cada entrada del registro registra:

- **Suscripción** — ¿A qué suscripción del cliente pertenece este intento de facturación?
- **Número de ciclo** — Ciclo de facturación secuencial (Ciclo 1 = primer cobro después del período de prueba)
- **Fecha de facturación** — Cuando se intentó el cobro
- **Estado** — Pendiente, En proceso, Exitoso, Fallido o Reintentando
- **Desglose del monto**:
  - **Monto base** — El precio del plan antes de cualquier ajuste
  - **Monto de cantidad** — Cargo adicional por la cantidad de asientos/unidades
  - **Monto de complementos** — Costo total de complementos activos
  - **Monto de descuento** — Total de descuentos aplicados
  - **Monto total** — El monto final cobrado (o intentado)
- **Método de pago** — La tarjeta o método de pago utilizado
- **ID de transacción del proveedor** — El número de referencia del proveedor de pago (útil para buscar reembolsos)
- **Razón de falla** — Si la facturación falló, explica por qué falló (por ejemplo, tarjeta rechazada, fondos insuficientes)

### Diagnóstico de fallos de pago

Si un cliente se contacta con usted sobre un problema de facturación, encuentre su suscripción y revise los registros del ciclo de facturación. El campo **Razón de falla** explica qué salió mal. Las razones comunes de falla incluyen:

- **Tarjeta rechazada** — La tarjeta del cliente fue rechazada por su banco
- **Fondos insuficientes** — El saldo de la cuenta era demasiado bajo en el momento de la facturación
- **Tarjeta caducada** — El método de pago guardado ha caducado
- **Error de red** — Un problema temporal de conexión con el proveedor de pago — generalmente se resuelve al reintentar

Para fallos persistentes, dirija al cliente a actualizar su método de pago en la configuración de su cuenta.

## Consejos

- Revise el filtro **Atrasado** semanalmente para detectar suscripciones en riesgo de cancelación. Un correo electrónico rápido al cliente suele resolver problemas de pago antes de que expire el período de gracia.
- Los registros del ciclo de facturación son de solo lectura — se crean automáticamente y no pueden modificarse. Esto garantiza un historial de auditoría confiable.
- Si una suscripción del cliente muestra **Atrasado** pero ya actualizó su método de pago, el siguiente reintento automático tomará la nueva tarjeta. Los reintentos siguen el horario de período de gracia configurado en el plan.
- Las suscripciones **Caducadas** no se eliminan — permanecen visibles para informes. Use los filtros de fecha para enfocarse en suscripciones activas actualmente.
- Para suscripciones en **Prueba**, revise la **Fecha de fin del período de prueba** para anticipar los primeros cobros próximos y abordar proactivamente cualquier problema con el método de pago.