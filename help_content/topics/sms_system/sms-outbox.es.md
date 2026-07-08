---
title: Bandeja de salida de SMS
---

La bandeja de salida de SMS es un registro completo de cada mensaje de texto que ha intentado enviar su tienda. Úselo para confirmar que las notificaciones llegaron a los clientes, investigar fallas en la entrega y comprender su actividad general de mensajes.

Navegue hasta **Sistema de SMS > Bandeja de salida de SMS** para ver el registro de mensajes.

![Lista de bandeja de salida de SMS con insignias de estado](/static/core/admin/img/help/sms-outbox/outbox-list.webp)

## Leer la bandeja de salida

Cada fila en la bandeja de salida representa un intento de mensaje y muestra:

- **Teléfono** — el número de teléfono del destinatario
- **Tipo de mensaje** — SMS o WhatsApp
- **Estado** — el estado actual de entrega (ver más abajo)
- **Creado** — cuándo se creó el mensaje
- **Enviado en** — cuándo se envió el mensaje al proveedor

La barra de resumen en la parte superior muestra conteos agregados para los estados más importantes a primera vista.

## Estados de mensajes

| Estado | Significado |
|--------|-------------|
| Pendiente | El mensaje está esperando para ser recogido por la cola de envío |
| En cola | El mensaje ha sido encolado y se enviará pronto |
| Enviado | El proveedor aceptó el mensaje para su entrega |
| Entregado | El proveedor confirmó que el mensaje llegó al dispositivo del destinatario |
| Fallido | El proveedor rechazó o no pudo entregar el mensaje |
| Saltado | El envío se saltó intencionalmente (ver razones de salto a continuación) |
| Registrado en entorno de prueba | El mensaje se registró solo (la tienda está en modo de prueba/entorno de prueba) |

> **Enviado vs. Entregado:** Un estado **Enviado** significa que el mensaje salió de su tienda y fue aceptado por el proveedor. Un estado **Entregado** significa que el proveedor recibió un recibo de entrega del operador. No todos los proveedores admiten recibos de entrega — si su proveedor no lo hace, los mensajes pueden mostrar **Enviado** pero nunca avanzar a **Entregado**, lo cual es normal.

## Ver detalles del mensaje

Haga clic en cualquier fila de la bandeja de salida para ver los detalles completos de ese mensaje:

- El texto completo del **Mensaje** que se envió
- El **ID del mensaje del proveedor** — el número de referencia del proveedor de SMS (útil al contactar al soporte del proveedor)
- El **Mensaje de error** (para mensajes fallidos) — el error exacto devuelto por el proveedor
- El **Contador de reintentos** — cuántas veces Spwig ha intentado enviar el mensaje
- Todos los timestamps (creado, encolado, enviado, entregado)

## Filtrar la bandeja de salida

Use los filtros en el lado derecho para reducir la lista:

- **Estado** — mostrar solo mensajes con un estado particular
- **Tipo de mensaje** — mostrar solo SMS o solo mensajes de WhatsApp
- **Fecha** — filtrar por el día en que se creó el mensaje

La caja de búsqueda en la parte superior le permite buscar por número de teléfono, contenido del mensaje o ID del mensaje del proveedor.

## Entender las razones de salto

Los mensajes saltados no se enviaron porque Spwig determinó que el envío era inapropiado o innecesario. Razones comunes de salto:

| Razón de salto | Qué significa |
|----------------|-------------|
| `user_preference_disabled` | El cliente desactivó las notificaciones por SMS en sus ajustes de cuenta |
| `unsubscribed` | El cliente se ha dado de baja de los mensajes por SMS |
| `no_provider` | No hay cuenta activa de proveedor de SMS predeterminada configurada |
| `template_inactive` | La plantilla para este tipo de notificación está inactiva |

Un mensaje saltado no es un fallo — significa que el sistema funcionó como se esperaba. Sin embargo, un alto conteo de saltos de `no_provider` indica que necesita configurar y activar una cuenta de proveedor de SMS.

## Solución de problemas de entregas fallidas

Si los mensajes muestran un estado **Fallido**, siga estos pasos:

1. Haga clic en el mensaje fallido para ver su **Mensaje de error**
2. Causas comunes de error:

   | Error | Causa probable |
   |-------|-------------|
   | Número de teléfono inválido | El número de teléfono del cliente está ausente o no está en formato E.164 |
   | Autenticación fallida | Sus credenciales del proveedor son inválidas o han expirado — actualícelas en **Cuentas de Proveedores de SMS** |
   | Cuenta suspendida | Su cuenta del proveedor ha sido suspendida — inicie sesión en el panel de control del proveedor |
   | Fondos insuficientes | El saldo de su cuenta del proveedor es demasiado bajo — recárguelo |
   | Rechazo del operador | El operador de destino bloqueó el mensaje (a menudo debido a la filtración de contenido) |

3. Después de resolver el problema subyacente, los mensajes futuros se enviarán normalmente — el buzón de salida es un registro de solo lectura y los mensajes individuales no pueden reenviarse manualmente

## El buzón de salida es de solo lectura

El buzón de salida de SMS es un registro solo. No puede agregar mensajes al buzón de salida manualmente, ni puede reenviar mensajes individuales desde aquí. Los mensajes se envían automáticamente por Spwig cuando ocurren los eventos relevantes (por ejemplo, se coloca un pedido).

## Consejos

- Revise el buzón de salida después de un período ocupado para confirmar que todos los mensajes de confirmación de pedidos se entregaron con éxito
- Si un cliente dice que no recibió un SMS, busque en el buzón de salida por su número de teléfono para ver si el mensaje se envió, falló o se omitió
- Un pico repentino en los mensajes **Fallidos** suele indicar un problema con sus credenciales del proveedor o su saldo de cuenta — revise estos inmediatamente
- Si ve muchos mensajes **Omitidos** con la razón `no_provider`, vaya a **Sistema de SMS > Cuentas de Proveedores de SMS** y asegúrese de que una cuenta activa predeterminada esté configurada
- La jerarquía de fechas en la parte superior de la lista le permite navegar rápidamente por día, mes o año para revisar mensajes históricos