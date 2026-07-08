---
title: Registros de Entrega de Webhook
---

Cada vez que tu tienda intenta enviar un webhook, se crea un registro de entrega. Estos registros te permiten ver exactamente qué se envió, si tuvo éxito y qué sucedió durante cualquier intento de reintento. Esta guía explica cómo leer los registros de entrega y depurar problemas cuando las entregas fallen.

## Ver registros de entrega

Navega a **Integraciones > Entregas de Webhook** para ver la historia completa de todos los intentos de entrega de webhook en todos tus puntos de conexión.

![Registros de entrega de webhook](/static/core/admin/img/help/webhook-deliveries/delivery-list.webp)

La lista muestra el nombre del punto de conexión, el tipo de evento, el estado, el código de respuesta HTTP, el tiempo de respuesta y cuántos intentos se realizaron.

Los registros de entrega son de solo lectura — se crean automáticamente cuando se disparan eventos y no pueden editarse.

## Estados de entrega

Cada entrega tiene uno de estos estados:

| Estado | Qué significa |
|--------|---------------|
| **Pendiente** | La entrega está en cola y aún no ha sido intentada |
| **Éxito** | El servidor receptor respondió con un código de estado HTTP 2xx — entrega confirmada |
| **Fallido** | Todos los intentos de entrega han sido agotados — la entrega no se reintentará |
| **Reintentando** | El último intento falló, pero el sistema intentará de nuevo en el tiempo de reintento programado |
| **Bloqueado en entorno de prueba** | La entrega fue bloqueada porque la URL del punto de conexión no es accesible en el entorno actual |

Una entrega se considera exitosa cuando el servidor receptor devuelve cualquier código de respuesta HTTP 2xx (200, 201, 202, etc.). Cualquier otro tipo de respuesta — incluyendo 3xx redirecciones o errores 4xx/5xx — se trata como un fracaso.

## Filtros de entregas

Usa el panel de filtros a la derecha para reducir la lista:

- **Estado** — Ver solo entregas fallidas, en reintento o exitosas
- **Tipo de evento** — Ver todas las entregas para un evento específico (por ejemplo, todas las entregas `order.created`)
- **Punto de conexión** — Ver entregas para un punto de conexión específico
- **Creado en** — Filtrar por rango de fechas

Usa la barra de búsqueda para buscar por tipo de evento o nombre del punto de conexión, o para encontrar una entrega específica por su ID.

## Leer detalles de una entrega

Haz clic en cualquier entrega para ver sus detalles completos. Los registros de entrega son de solo lectura.

### Resumen

- **ID** — El identificador único para este intento de entrega
- **Punto de conexión** — A qué punto de conexión de webhook se envió (enlaza al registro del punto de conexión)
- **Tipo de evento** — El evento que disparó esta entrega (por ejemplo, `order.paid`)
- **Estado** — Estado actual de la entrega

### Carga útil

La sección **Carga útil** muestra los datos exactos en formato JSON que se enviaron a tu punto de conexión. Esto incluye el tipo de evento, una marca de tiempo y los datos completos del evento. Usa esto para verificar que tu servidor receptor esté recibiendo la estructura de datos correcta.

### Respuesta

La sección **Respuesta** muestra lo que tu servidor respondió:

- **Código de estado de respuesta** — El código de estado HTTP devuelto por tu servidor. Codificado por colores: verde para 2xx (éxito), amarillo para 4xx (error del cliente), rojo para 5xx (error del servidor).
- **Tiempo de respuesta** — Cuánto tiempo tomó a tu servidor responder en milisegundos. Codificado por colores: verde bajo 500 ms, amarillo hasta 2 segundos, rojo por encima de 2 segundos.
- **Cuerpo de la respuesta** — El cuerpo de la respuesta de tu servidor (truncado a 1,000 caracteres). Esto puede ayudar a identificar por qué tu servidor rechazó el webhook.
- **Encabezados de respuesta** — Los encabezados devueltos por tu servidor.

### Detalles del error

Si la entrega falló, la sección **Detalles del error** muestra el mensaje de error — por ejemplo, `Conexión rechazada`, `Tiempo de espera después de 30s` o el error HTTP de tu servidor.

### Información de reintento

- **Contador de intentos** — Cuántos intentos de entrega se han realizado (incluyendo el primer intento)
- **Próximo reintento en** — Cuándo se realizará el próximo reintento (solo se muestra para entregas en estado **Reintentando**)

Los reintentos siguen un horario de retroceso exponencial — el intervalo entre reintentos aumenta con cada intento para evitar sobrecargar un servidor que esté temporalmente inaccesible. Con un máximo de 5 reintentos (el valor predeterminado), el horario de reintento abarca varias horas.

## Reintentar entregas fallidas manualmente

Si deseas reintentar una entrega de inmediato sin esperar al horario automático:

1. Selecciona las casillas de verificación junto a las entregas que deseas reintentar
2. Desde el menú desplegable **Acción**, elige **Reintentar entregas seleccionadas**
3. Haz clic en **Ir**

Solo se encolarán para reintentar las entregas que no estén ya en estado **Éxito**. Las entregas exitosas se omiten.

Esto es útil cuando hayas corregido un problema con tu servidor receptor y desees reprocesar los eventos fallidos sin esperar.

## Diagnosticar fallos comunes

### Códigos de respuesta HTTP 4xx

Una respuesta 4xx de tu servidor generalmente significa que hay un problema con la solicitud — la autenticación falló, la URL del punto final cambió o tu servidor rechazó el formato de carga útil. Verifica:

- ¿La URL del punto final es correcta?
- ¿Tu servidor está verificando correctamente la firma HMAC? Una discrepancia hace que muchos servidores devuelvan 401 o 403.
- ¿Ha cambiado la estructura de la carga útil? Compara la carga útil en el registro de entrega con lo que espera tu servidor.

### Códigos de respuesta HTTP 5xx

Una respuesta 5xx significa que tu servidor encontró un error interno al procesar el webhook. Revisa los registros de error de tu propio servidor para diagnosticar el problema.

### Conexión rechazada / Tiempo de espera

Estos errores significan que Spwig no pudo llegar a tu servidor en absoluto:

- ¿El servidor está en ejecución y accesible públicamente?
- ¿La URL es correcta (incluyendo el protocolo correcto — http o https)?
- ¿Un firewall está bloqueando las solicitudes entrantes?
- ¿El tiempo de respuesta del servidor excede el tiempo de espera configurado? Si es así, aumenta la configuración de **Tiempo de espera** en el punto final o optimiza el controlador de webhook de tu servidor para responder rápidamente (idealmente dentro de 5 segundos).

### Bloqueo de entorno de prueba

Las entregas se bloquean para URLs de localhost o direcciones de red interna. Los puntos finales de webhook deben ser accesibles públicamente. Usa una herramienta como ngrok durante el desarrollo para exponer públicamente un servidor local.

## Consejos

- Aborda las entregas **Fallidas** con prontitud — los datos del evento aún están en la carga útil, y puedes reintentar manualmente una vez que se haya resuelto el problema.
- Si ves muchas entregas **Reintentando** para un solo punto final, abre el registro del punto final y verifica la sección **Salud** — el punto final podría estar a punto de desactivarse automáticamente.
- El tiempo de respuesta importa: configura tu controlador de webhook para responder rápidamente (dentro de unos segundos) y procesa la carga útil de forma asincrónica en segundo plano. Un controlador lento causa fallos por tiempo de espera incluso si tu lógica es correcta.
- Usa el filtro **Tipo de evento** para revisar el historial de entregas para un tipo de evento específico cuando investigues si tu integración está recibiendo los eventos correctos.
- Los registros de entrega se acumulan con el tiempo. Usa el filtro de fecha para enfocarte en entregas recientes y evita navegar por un historial antiguo.