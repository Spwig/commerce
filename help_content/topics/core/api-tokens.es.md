---
title: Tokens de API
---

Los tokens de API son claves seguras que permiten que los servicios externos e integraciones se comuniquen con tu tienda. Cuando un servicio de terceros o una herramienta necesita acceder a los datos de tu tienda o desencadenar acciones, envía un token de API con cada solicitud para que tu tienda pueda verificar que la solicitud esté autorizada. Crea y gestiona todos los tokens desde la sección Tokens de API de tu administrador.

## Cuando necesitas un token de API

Normalmente necesitarás crear un token de API cuando:

- Conectes un servicio externo o una herramienta de automatización que necesite leer o escribir en tu tienda
- Configures un receptor de webhooks que necesite autenticar llamadas entrantes
- Configure el Sistema de Ayuda de Spwig para tu instalación
- Construyas una integración personalizada usando la API de Spwig
- Sincronices datos entre tu tienda de Spwig y otro sistema

Cada integración debe tener su propio token para que puedas revocar el acceso para un servicio sin afectar a otros.

## Tipos de token

Al crear un token, elige un tipo que describa su propósito. El tipo es para tu referencia y te ayuda a mantener el control de qué hace cada token.

| Tipo | Propósito |
|------|---------|
| **Sistema de Ayuda** | Utilizado por el sistema de documentación de ayuda de Spwig |
| **Integración Externa** | Servicios de terceros, herramientas de automatización (p. ej., Zapier) o herramientas de sincronización de datos |
| **Webhook** | Autenticación para receptores de webhooks o puntos de conexión |
| **Personalizado** | Cualquier otro propósito que no encaje en las categorías anteriores |
| **Sincronización de Instancia** | Sincronización entre instalaciones de Spwig o servicios externos de Spwig |

## Crear un token de API

1. Navega a **Configuración > Tokens de API**
2. Haz clic en **+ Agregar Token de API**
3. Ingresa un **Nombre** que describa claramente para qué se usa el token (p. ej., `Sincronización de Productos con Zapier` o `API del Sistema de Ayuda`)
4. Selecciona el tipo de token adecuado
5. Opcionalmente, agrega una **Descripción** con más detalles sobre la integración
6. Configura el estado **Activo**, la **Fecha de Vencimiento** y las **IPs Permitidas** según sea necesario (ver más abajo)
7. Haz clic en **Guardar**

Después de guardar, el valor completo del token se muestra en la página de detalles. **Cópialo inmediatamente** — el token se muestra enmascarado en la vista de lista por razones de seguridad y no se puede recuperar en su totalidad después de que dejes esta página.

![Detalles del Token de API](/static/core/admin/img/help/api-tokens/api-token-detail.webp)

## Seguridad del valor del token

Spwig muestra el valor completo del token solo una vez: inmediatamente después de que guardes un nuevo token. Después de eso, la vista de lista muestra solo una versión enmascarada (p. ej., `spw_••••••••••••••••••••3f8a`).

Si pierdes el valor de un token, no puedes recuperarlo. Deberás eliminar el token antiguo y crear uno nuevo, luego actualizar la integración que lo utilizaba.

**Nunca compartas valores de tokens en correos electrónicos, mensajes de chat o código fuente.** Trátalos como contraseñas.

## Establecer una fecha de vencimiento

El campo **Vence en** establece una fecha y hora después de las cuales el token dejará de funcionar automáticamente. Deja este campo vacío para tokens que no deben vencer.

Las fechas de vencimiento son útiles para:

- Integraciones temporales con una fecha de finalización fija
- Tokens dados a terceros donde deseas eliminar automáticamente el acceso
- Agregar una capa adicional de seguridad a integraciones con altos privilegios

Cuando un token vence, las solicitudes que lo usan se rechazan. Puedes extender el acceso actualizando la fecha **Vence en** o creando un token de reemplazo.

## Restringir a direcciones IP específicas

El campo **IPs Permitidas** acepta una lista de direcciones IP. Cuando la lista no está vacía, el token solo funciona cuando la solicitud proviene de una de esas direcciones.

Por ejemplo, si tu herramienta de análisis funciona en un servidor en `203.0.113.42`, agregar esa IP significa que el token no puede ser mal utilizado desde cualquier otro lugar, incluso si se filtra.

Deja **IPs Permitidas** vacío para permitir solicitudes desde cualquier dirección IP.

## Monitorear el uso del token

La lista de tokens muestra:

- **Conteo de Uso** — número total de veces que el token ha sido utilizado
- **Último Uso** — cuándo el token fue utilizado por última vez para hacer una solicitud

Estos campos te ayudan a identificar tokens no utilizados (candidatos para revocación) y detectar actividad inesperada.

Un aumento repentino en el recuento de uso puede indicar que un token está siendo utilizado por alguien distinto de la integración prevista.

## Revocar un token

Para detener inmediatamente el funcionamiento de un token sin eliminarlo:

1. Haz clic en el nombre del token
2. Desmarcar **Activo**
3. Guardar

El token sigue en tu lista para referencia, pero se rechazará en cualquier solicitud posterior. Esto es útil cuando necesitas suspender temporalmente una integración mientras investigas un problema.

Para eliminar permanentemente un token:

1. Selecciona su casilla de verificación en la lista
2. Elige **Eliminar los tokens de API seleccionados** del menú de acciones
3. Confirma la eliminación

Una vez eliminado, un token no puede recuperarse. Si la integración aún necesita acceso, crea un nuevo token y actualiza la configuración de la integración.

## Ejemplo: configurar una integración de Zapier

**Escenario:** Quieres conectar tu tienda con Zapier para automatizar las notificaciones de pedidos.

| Campo | Valor |
|-------|-------|
| Nombre | `Zapier Order Automation` |
| Tipo de token | Integración externa |
| Descripción | Utilizado por Zapier para leer nuevos pedidos y disparar notificaciones |
| Activo | Sí |
| Vence en | *(dejar en blanco)* |
| IPs permitidas | *(dejar en blanco — Zapier utiliza IPs dinámicas)* |

Después de guardar, copia el valor completo del token y pégalo en la configuración de la integración de Spwig en Zapier.

## Consejos

- Dales a cada token un nombre claro y específico — `Shopify Sync v2` es mucho más útil que `Token 3` cuando estés solucionando problemas meses después
- Crea un token por integración — si una integración se ve comprometida, puedes revocar solo ese token sin afectar a otros
- Establece una fecha de vencimiento para tokens utilizados en proyectos puntuales o integraciones temporales — esto reduce el riesgo de que tokens olvidados permanezcan activos indefinidamente
- Revisa tu lista de tokens cada pocos meses y desactiva cualquier token con una fecha de **Último uso** que sea inesperadamente antigua, ya que pueden pertenecer a integraciones que ya no estén en funcionamiento
- Si sospechas de que un token ha sido expuesto, desactívalo inmediatamente, crea un reemplazo y actualiza la integración afectada antes de reactivar el acceso