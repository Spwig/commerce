---
title: Bandeja de salida de correo electrónico
---

La bandeja de salida de correo electrónico es un registro completo de cada correo electrónico que tu tienda ha enviado o intentado enviar — confirmaciones de pedidos, actualizaciones de envío, informes de administración y todos los demás mensajes transaccionales. Úsala para confirmar entregas, investigar fallas y gestionar la cola de correos.

Navega a **Sistema de correo electrónico > Bandeja de salida de correo electrónico** para ver el registro de correos.

![Lista de bandeja de salida con insignias de estado](/static/core/admin/img/help/email-outbox/outbox-list.webp)

## Leer la bandeja de salida

La barra de resumen en la parte superior muestra conteos para cada categoría de estado. La lista de abajo muestra correos individuales con:

- **Asunto** — la línea de asunto del correo electrónico
- **Para** — la dirección de correo electrónico del destinatario
- **De** — la dirección del remitente utilizada
- **Estado** — el estado actual de entrega
- **En cola el** — cuando el correo electrónico entró en la cola
- **Enviado el** — cuando el correo electrónico fue enviado al proveedor
- **Conteo de reintentos** — cuántos intentos de envío se han realizado

## Estados de correo electrónico

| Estado | Significado |
|--------|---------|
| En cola | El correo electrónico está esperando en la cola para ser enviado |
| Enviando | El correo electrónico está siendo enviado actualmente al proveedor |
| Enviado | El proveedor aceptó el correo electrónico |
| Retenido | El correo electrónico está pausado y no se enviará hasta que se libere |
| Registrado | El correo electrónico fue registrado pero no enviado (modo de prueba o configuración de solo registro) |
| Fallido | El proveedor rechazó o no pudo entregar el correo electrónico |
| Rebotado | El correo electrónico fue enviado pero rebotó desde el servidor de correo del destinatario |
| Omitido | El envío fue omitido por una razón del sistema |

## Ver detalles del correo electrónico

Haz clic en cualquier correo electrónico de la lista para ver los detalles completos:

- El **cuerpo HTML completo** y **cuerpo de texto** del correo electrónico
- **ID de mensaje del proveedor** — la referencia de tu proveedor de correo electrónico (úsalo cuando contactes al soporte del proveedor)
- **Mensaje de error** — el error exacto para correos fallidos o rebotados
- **Conteo de reintentos** y **Máximo de reintentos** — cuántas veces se intentó enviar
- Todos los timestamps: creado, en cola, enviado y fallido

## Filtrar la bandeja de salida

Usa los filtros a la derecha para reducir tu vista:

- **Estado** — mostrar correos de un estado de entrega específico
- **Fecha** — filtrar por cuando los correos fueron creados o enviados
- **Tipo de plantilla** — mostrar solo correos de un tipo específico de notificación (por ejemplo, solo confirmaciones de pedidos)

La caja de búsqueda en la parte superior busca por asunto, dirección del destinatario, dirección del remitente o ID de mensaje del proveedor.

## Liberar correos retenidos

Los correos en estado **Retenido** están pausados — no se enviarán hasta que los liberes. Un correo puede estar retenido si tu tienda estaba en modo de mantenimiento cuando se generó, o si una acción de administrador lo puso en pausa.

Para liberar correos retenidos:
1. Selecciona los correos que deseas liberar (marca las casillas a la izquierda)
2. Elige **Liberar correos retenidos para entrega** desde el menú desplegable **Acciones**
3. Haz clic en **Ir**

Los correos liberados se mueven al estado **En cola** y se enviarán en el siguiente ciclo de procesamiento de la cola.

## Correos programados

Algunos correos están programados para enviarse en un momento futuro — por ejemplo, los informes de resumen semanal están programados para enviarse en un día y hora específicos. Navega a **Sistema de correo electrónico > Correos programados** para ver los envíos programados próximos.

La lista de correos programados muestra:

- **Tipo de plantilla** — el tipo de correo electrónico programado
- **Correo electrónico del destinatario** — la dirección a la que se enviará
- **Programado para** — la fecha y hora en que está programado para enviarse
- **Estado** — Pendiente (no enviado aún), Enviado o Fallido

Los correos programados se procesan automáticamente cuando llegue su hora programada — no se necesita ninguna acción manual.

## Solución de problemas de entregas fallidas

Si los correos muestran un estado **Fallido**, haz clic para ver el mensaje de error y sigue estos pasos:

### Causas comunes y soluciones

| Síntoma | Causa probable | Qué hacer |
|---------|-------------|------------|
| "Autenticación fallida" | Las credenciales del proveedor de correo electrónico son inválidas | Actualice las credenciales en **Sistema de Correo > Cuentas de Correo** |
| "Conexión rechazada" / "Tiempo de espera" | Su servidor de correo electrónico no es alcanzable | Revise la página de estado del proveedor de correo electrónico; pruebe la conexión en **Cuentas de Correo** |
| "Destinatario inválido" | La dirección de correo electrónico del cliente está malformada | Revise la cuenta del cliente y corrija su correo electrónico |
| Correos rechazados | El servidor de correo del destinatario rechazó el correo | La dirección podría no existir o su bandeja de entrada esté llena; no intente enviar demasiadas veces |
| Alto índice de fallos de repente | Problema del proveedor o credenciales expiradas | Revise el estado del proveedor; vuelva a probar la conexión en **Cuentas de Correo** |

### Comprobando la conexión de su cuenta de correo

Si muchos correos están fallando, pruebe su cuenta de correo:

1. Navegue a **Sistema de Correo > Cuentas de Correo**
2. Encuentre su cuenta activa y revise su estado de **Conexión**
3. Si la conexión muestra un error, haga clic en la cuenta y use la opción **Probar Conexión** para diagnosticar el problema

### Comportamiento de reintento

Spwig reintenta automáticamente los correos fallidos hasta el límite de **Máximo de Reintentos**. El recuento de reintentos mostrado en cada correo le indica cuántos intentos se han realizado. Una vez que se alcanza el límite de reintentos, el correo permanece en estado **Fallido** y no se realizarán más reintentos automáticos.

## Correos rechazados

Un correo **rechazado** fue enviado pero fue devuelto por el servidor de correo del destinatario. Hay dos tipos de rechazos:

- **Rechazo duro** — la dirección de correo electrónico no existe o el dominio no acepta correos. No intente reenviar rechazos duros; la dirección es inválida
- **Rechazo suave** — un problema temporal (bandeja de entrada llena, servidor temporalmente no disponible). Puede tener éxito al reintentar

Los rechazos repetidos a la misma dirección pueden dañar su reputación como remitente con los proveedores de correo electrónico. Si ve rechazos repetidos a la misma dirección del cliente, actualice o elimine esa dirección de la cuenta del cliente.

## Consejos

- Revise la bandeja de salida después de eventos importantes como una venta flash o un lanzamiento de producto grande para confirmar que todos los correos de confirmación de pedidos se hayan enviado correctamente
- Si un cliente dice que no recibió un correo, busque en la bandeja de salida por su dirección de correo electrónico para ver si fue enviado, fallido o omitido
- Un aumento repentino en los fallos suele indicar un problema de credenciales o cuenta — revise **Cuentas de Correo** inmediatamente
- El estado **Pendiente** no es un fallo — solo significa que el correo está esperando. Libere los correos pendientes cuando esté listo para enviarlos
- Use el filtro **Tipo de Plantilla** para auditar rápidamente todos los correos de un tipo — por ejemplo, revise que todos los confirmaciones de pedidos de los últimos 7 días tengan un estado **Enviado**
- La navegación de jerarquía de fechas (día / mes / año) en la parte superior de la lista es útil para revisar la bandeja de salida para un período específico