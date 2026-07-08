---
title: Transacciones de pago
---

Las transacciones de pago son el registro completo de cada evento de pago procesado a través de su tienda — cobros, reembolsos, autorizaciones y más. Esta sección también incluye registros de webhooks de sus proveedores de pago y transacciones de pago creadas durante el proceso de pago.

## Transacciones de pago

Navegue a **Pagos > Transacciones de pago** para ver cada transacción que su tienda ha procesado.

### Tipos de transacción

| Tipo | Qué significa |
|------|--------------|
| **Cobro** | Un pago inmediato — los fondos se recogen en el momento de la transacción |
| **Autorización** | Los fondos se retienen en la tarjeta del cliente pero aún no se han recogido |
| **Captura** | Recoge los fondos de una autorización anterior |
| **Anular** | Cancela una autorización antes de que se capture |
| **Reembolso** | Devuelve el pago al cliente |

### Estados de transacción

| Estado | Qué significa |
|--------|--------------|
| **Pendiente** | La transacción ha sido iniciada pero aún no se ha procesado |
| **En proceso** | Se está procesando por el proveedor de pago |
| **Autorizado** | Los fondos se retienen — esperando captura |
| **Completado** | El pago fue exitoso |
| **Fallido** | El pago fue rechazado o ocurrió un error |
| **Anulado** | La autorización se canceló antes de la captura |
| **Reembolsado** | Se ha emitido un reembolso completo |
| **Reembolsado parcialmente** | Parte del pago ha sido devuelta |

### Qué puede ver en un registro de transacción

Cada transacción muestra:
- **ID de transacción** — referencia interna de Spwig
- **ID de transacción del proveedor** — la referencia de su proveedor de pago (por ejemplo, ID de cobro de Stripe)
- **Monto** — el monto de la transacción y la moneda
- **Estado** y **Tipo**
- **Correo electrónico del cliente** y **Nombre del cliente**
- **Método de pago** — tipo (tarjeta de crédito, transferencia bancaria, etc.) y últimos 4 dígitos
- **Orden** — la orden a la que pertenece esta transacción
- **Cuenta del proveedor** — qué proveedor de pago la procesó
- **Respuesta del proveedor** — la respuesta técnica bruta del proveedor de pago
- **Mensaje de error** — si la transacción falló, la razón dada por el proveedor
- Marcas de tiempo para creación, última actualización y finalización

### Filtros de transacciones

Use los filtros del administrador para reducir las transacciones según:
- Estado (por ejemplo, mostrar solo transacciones fallidas)
- Tipo (por ejemplo, mostrar solo reembolsos)
- Cuenta del proveedor
- Rango de fechas

Esto es útil para la conciliación al final del día o para investigar el historial de pagos de un cliente específico.

### ¿Cuándo puede reembolsarse una transacción?

Una transacción puede reembolsarse cuando:
- Su estado es **Completado**
- Su tipo es **Cobro** o **Captura**

Para emitir un reembolso, use la acción **Reembolso** desde la página de detalles de la orden. Los reembolsos procesados a través de la orden crean un nuevo registro de transacción de tipo **Reembolso**.

### Flujo de autorización y captura

Algunos métodos de pago (y algunos proveedores de pago) admiten autorización y captura por separado. Esto es útil si desea verificar el pago antes de enviar el producto:

1. **Autorizar** — Los fondos se retienen en la tarjeta del cliente (estado: `Autorizado`)
2. **Capturar** — Se activa cuando se envía la orden o se cumple
3. Si no se captura dentro del período de autorización, el retención **vence** automáticamente

El campo **Vence en** en la transacción muestra cuándo una autorización dejará de ser válida.

## Webhooks de pago

Los proveedores de pago envían eventos de webhook para notificar a su tienda sobre cambios en el estado del pago — por ejemplo, cuando un pago tiene éxito, falla o se presenta una disputa. Spwig registra todos los webhooks entrantes.

Navegue a **Pagos > Webhooks de pago** para ver el registro.

### Qué muestran los registros de webhook

| Campo | Descripción |
|-------|-------------|
| **Proveedor** | ¿Cuál proveedor de pago envió el webhook? |
| **ID del evento** | El identificador único del evento del proveedor |
| **Tipo de evento** | El tipo de evento (por ejemplo, `payment_intent.succeeded`, `charge.refunded`) |
| **Procesado** | Si Spwig ha actuado sobre este webhook |
| **Firma verificada** | Si la firma de seguridad del webhook era válida |
| **Carga útil** | Los datos completos enviados por el proveedor |
| **Resultado del procesamiento** | Lo que hizo Spwig en respuesta |
| **Error de procesamiento** | Cualquier error que ocurriera durante el procesamiento |
| **Recibido en** | Cuando llegó el webhook |

### Usando registros de webhooks para solucionar problemas

Si un pago parece estar atascado o el estado del pedido no se actualizó después del pago:

1. Navegue a **Pagos > Webhooks de pago**
2. Filtre por el proveedor y busque eventos recientes
3. Revise la columna **Procesado** — un webhook no procesado puede indicar un problema de entrega
4. Revise **Firma verificada** — una firma fallida puede significar que su secreto de webhook está mal configurado
5. Revise **Error de procesamiento** para cualquier mensaje de error

Los eventos duplicados se manejan automáticamente — el `ID del evento` y la combinación del proveedor son únicos, por lo tanto, el mismo webhook no puede procesarse dos veces.

## Intenciones de pago

Una intención de pago rastrea el ciclo de vida de un pago de checkout desde el momento en que un cliente comienza el proceso de pago hasta el resultado final. Las intenciones de pago se crean automáticamente cuando un cliente llega al paso de pago en el checkout.

Navegue a **Pagos > Intenciones de pago** para ver la lista.

### Estados de intención de pago

| Estado | Significado |
|--------|---------|
| **Creado** | La intención ha sido creada, esperando el método de pago |
| **Requiere método de pago** | Esperando que el cliente ingrese sus datos de tarjeta |
| **Requiere confirmación** | Detalles del pago ingresados, esperando confirmación |
| **Requiere acción** | El cliente necesita completar una acción (por ejemplo, autenticación 3D Secure) |
| **En proceso** | El pago está siendo procesado |
| **Exitoso** | El pago se completó con éxito |
| **Cancelado** | El pago fue abandonado o cancelado |
| **Fallido** | El intento de pago falló |

### Flujo de intención de pago a pedido

1. El cliente llega al paso de pago del checkout → Spwig crea una **Intención de pago** y un **Pedido** en borrador (no pagado)
2. El cliente ingresa los detalles de pago y confirma
3. El proveedor de pago procesa el pago
4. En caso de éxito, el Pedido se actualiza a **Pagado** y la Intención de pago se mueve a **Exitoso**
5. Se crea un registro de **Transacción de pago** con los detalles finales de la carga

La intención de pago vincula la sesión de checkout, la cuenta del proveedor y el pedido — le da una imagen completa del viaje de checkout del cliente.

### Usando intenciones de pago para soporte

Si un cliente reporta que pagó pero su pedido muestra como no pagado:

1. Encuentre el pedido del cliente en **Pedidos**
2. Navegue a **Pagos > Intenciones de pago** y busque intenciones vinculadas a ese pedido
3. Revise el estado de la intención — si es **Exitoso**, revise la transacción vinculada
4. Si la intención es **Requiere acción**, el cliente puede no haber completado la autenticación 3D Secure
5. Si la intención es **Fallida**, los detalles del error explican por qué el pago fue rechazado

## Consejos

- Revise las transacciones fallidas diariamente — patrones de fallas (por ejemplo, un método de pago o país específico) pueden indicar un problema de configuración o un intento de fraude.
- Los registros de webhooks son valiosos al investigar discrepancias de pago.

Si un pedido fue pagado pero no confirmado, el registro de webhook generalmente le dirá qué salió mal.
- Las retenciones de autorización expiran automáticamente — si usa autorizar-entonces-capturar, asegúrese de que su proceso de cumplimiento capture los fondos antes de que el período de vencimiento cierre (normalmente 7 días para la mayoría de los proveedores).
- El campo **Respuesta del proveedor** en las transacciones contiene los datos crudos del proveedor de pago.

Comparte esto con el equipo de soporte de tu proveedor si necesitas ayuda para resolver un problema específico de transacción.
- Los fallos en la verificación de la firma en los webhooks deben investigarse inmediatamente — pueden indicar un secreto de webhook mal configurado o un intento de enviar eventos de webhook fraudulentos a tu tienda.