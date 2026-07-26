---
title: Tokens de API
---

Los tokens de API son claves seguras que permiten que los servicios externos e integraciones se comuniquen con tu tienda. Cuando un servicio de terceros o una herramienta necesita acceder a los datos de tu tienda o desencadenar acciones, envía un token de API con cada solicitud para que tu tienda pueda verificar que la solicitud esté autorizada. Creas y gestionas todos los tokens, incluyendo exactamente qué partes de tu tienda pueden alcanzar, desde la sección de Tokens de API de tu administrador.

## Cuando necesitas un token de API

Normalmente necesitarás crear un token de API cuando:

- Conectes un servicio externo o una herramienta de automatización que necesite leer o escribir en tu tienda
- Configures un receptor de webhooks que necesite autenticar llamadas entrantes
- Configures el Sistema de Ayuda de Spwig para tu instalación
- Construyas una integración personalizada usando la API de Spwig
- Sincronices datos entre tu tienda de Spwig y otro sistema

Cada integración debe tener su propio token para que puedas revocar el acceso para un servicio sin afectar a otros.

## Tipos de token

Al crear un token, eliges un tipo que describe su propósito. El tipo es para tu referencia y te ayuda a mantener el control de qué hace cada token.

| Tipo | Propósito |
|------|---------|
| **Sistema de Ayuda** | Utilizado por el sistema de documentación de ayuda de Spwig |
| **Integración Externa** | Servicios de terceros, herramientas de automatización (p. ej., Zapier) o herramientas de sincronización de datos |
| **Webhook** | Autenticación para receptores de webhooks o puntos finales |
| **Personalizado** | Cualquier otro propósito que no encaje en las categorías anteriores |
| **Sincronización de Instancia** | Sincronización entre instalaciones de Spwig o servicios externos de Spwig |

## Ámbitos de API: controlar qué puede alcanzar un token

Cada token también tiene una sección de **Ámbitos de API** que decide exactamente qué partes de tu tienda está permitido que llame. En lugar de que un token tenga acceso general a todo, otorgas acceso área por área — y al nivel que realmente necesite la integración.

**Un token sin ámbitos seleccionados no puede alcanzar ninguna API**, incluso si de otro modo está activo y válido. Esto es el valor predeterminado para un token nuevo, por lo que una integración no funcionará hasta que le otorgues explícitamente acceso.

Para cada ámbito, eliges uno de tres niveles de acceso:

| Nivel de Acceso | Qué permite |
|----------------|-------------|
| **Sin acceso** | El token no puede llamar a ningún punto final en este área |
| **Lectura** | El token puede recuperar datos de este área, pero no puede cambiar nada |
| **Lectura y Escritura** | El token puede recuperar datos y también crear, actualizar o eliminarlos |

Los ámbitos se agrupan para coincidir con las áreas de tu administrador:

| Grupo | Ámbito | ¿Disponible Lectura y Escritura? | Concede acceso a |
|-------|-------|:---:|-------------------|
| Análisis | **Análisis de Ventas** | Solo lectura | Dashboards de ventas, KPIs, análisis de productos/clientes/categorías, comparaciones y exportaciones |
| Análisis | **Análisis Web** | Solo lectura | Análisis de visitantes y tráfico: visión general, tendencias, páginas más visitadas, geografía y referidos |
| Catálogo | **Productos** | Sí | Productos, variantes, imágenes, ajustes de stock y asignación de atributos |
| Catálogo | **Categorías** | Sí | Categorías de productos, incluyendo imágenes y banners |
| Catálogo | **Marcas** | Sí | Marcas de productos |
| Catálogo | **Atributos** | Sí | Definiciones de atributos de productos |
| Catálogo | **Inventario** | Sí | Dashboards de inventario, velocidad de stock, movimientos, sugerencias de reorden y configuraciones de inventario |
| Pedidos | **Pedidos** | Sí | Pedidos, notas de pedido, actualizaciones de estado/seguimiento, cancelaciones, reembolsos y documentos de pedido |
| Clientes | **Mensajes de Cliente** | Sí | Mensajes de clientes desde formularios de contacto y notas de pedido, incluyendo actualizaciones de estado y respuestas |
| Tienda y Configuración | **Configuración de Tienda** | Sí | Configuración de tienda, idiomas disponibles y branding (nombre, colores, logotipo) |
| Usuarios y Acceso | **Personal y Roles** | Sí | Cuentas de personal, invitaciones, roles y catálogo de permisos |

Los dos ámbitos de **Análisis** siempre son de solo lectura — los datos de informes no tienen un concepto de "escritura", por lo que el selector solo ofrece **Sin acceso** o **Lectura** para ellos.

[![El selector de alcances de la API, con una nota de acceso encima de los grupos de alcances de Análisis y Catálogo](/static/core/admin/img/help/api-tokens/api-token-scope-picker.webp)]

Debajo del selector de alcances, un resumen de solo lectura **"Este token puede acceder a:"** enumera cada alcance que has concedido y su nivel, para que puedas revisar rápidamente el acceso del token sin necesidad de decodificar el selector.

![El resumen "Este token puede acceder a" que enumera cada alcance concedido y su nivel de Lectura o Lectura y Escritura](/static/core/admin/img/help/api-tokens/api-token-scope-summary.webp)

### ¿Qué permisos realmente usa un token

Los alcances de un token describen el *techo* de lo que puede hacer — pero el token también hereda los permisos reales del miembro del personal que lo creó:

- El token nunca puede actuar con poderes de **superusuario**, incluso si el miembro del personal que lo creó es un superusuario.
- **Lectura y Escritura** en un alcance solo funciona si el rol del miembro del personal que lo creó también permite el acceso de escritura a esa área. Si su rol es solo de visualización, por ejemplo, en Productos, un token que creen con "Productos: Lectura y Escritura" aún solo podrá leer — el rol actúa como una segunda puerta encima del alcance.
- Si el miembro del personal que creó un token es eliminado o su cuenta se desactiva, el token pierde inmediatamente el acceso a la API, independientemente de sus alcances — ya no hay un usuario permitido para que actúe como él.

Esto significa que la manera más segura de limitar los alcances de un token es crearlo mientras estés conectado como un miembro del personal cuyo rol ya coincida con el acceso que deseas que tenga el token.

## Crear un token de API

1. Navega a **Configuración > Tokens de API**
2. Haz clic en **+ Agregar Token de API**
3. Ingresa un **Nombre** que describa claramente para qué se usa el token (por ejemplo, `Sincronización de Productos con Zapier` o `API del Sistema de Ayuda`)
4. Selecciona el tipo de **Token adecuado**
5. Opcionalmente, agrega una **Descripción** con más detalles sobre la integración
6. En **Alcances de API**, elige **Sin acceso**, **Lectura** o **Lectura y Escritura** para cada área que la integración necesite — deja todos los demás alcances en **Sin acceso**
7. Configura el estado **Activo**, la **Fecha de vencimiento** y las **IPs permitidas** según sea necesario (ver más abajo)
8. Haz clic en **Guardar**

Después de guardar, el valor completo del token se muestra en la página de detalles. **Cópialo inmediatamente** — el token se muestra enmascarado en la vista de lista por razones de seguridad y no se puede recuperar en su totalidad después de que dejes esta página.

![Detalles del Token de API](/static/core/admin/img/help/api-tokens/api-token-detail.webp)

## Seguridad del valor del token

Spwig muestra el valor completo del token solo una vez: inmediatamente después de que guardes un nuevo token. Después de eso, la vista de lista muestra solo una versión enmascarada (por ejemplo, `spw_••••••••••••••••••••3f8a`).

Si pierdes el valor de un token, no puedes recuperarlo. Tendrás que eliminar el token antiguo y crear uno nuevo, luego actualizar la integración que lo utilizaba.

**Nunca compartas valores de tokens en correos electrónicos, mensajes de chat o código fuente.** Trátalos como contraseñas.

## Establecer una fecha de vencimiento

El campo **Vence en** establece una fecha y hora después de las cuales el token dejará de funcionar automáticamente. Dejalo en blanco para tokens que no deben vencer.

Las fechas de vencimiento son útiles para:

- Integraciones temporales con una fecha de finalización fija
- Tokens dados a terceros donde deseas la eliminación automática del acceso
- Agregar una capa adicional de seguridad a integraciones con altos privilegios

Cuando un token vence, las solicitudes que lo usen se rechazan. Puedes extender el acceso actualizando la fecha **Vence en** o creando un token de reemplazo.

## Restringir a direcciones IP específicas

El campo **IPs permitidas** acepta una lista de direcciones IP. Cuando la lista no está vacía, el token solo funciona cuando la solicitud proviene de una de esas direcciones.

Por ejemplo, si tu herramienta de análisis funciona en un servidor en `203.0.113.42`, agregar esa IP significa que el token no puede ser mal utilizado desde cualquier otro lugar, incluso si se filtra.

Deja **IPs permitidas** vacío para permitir solicitudes desde cualquier dirección IP.

**La expiración y las restricciones de IP se verifican de forma independiente de los alcances.** Un token expirado o no incluido en la lista de IPs permitidas se rechaza antes de que se consideren incluso sus alcances, y un token con alcances generosos sigue siendo rechazado en el momento en que expira o se llama desde una IP no registrada.

## Llamando a la API con un token

Las integraciones se autentican en la API de administración de Spwig enviando el token en un encabezado `Authorization`:

```
Authorization: Bearer <your-token-value>
```

Cada punto final de la API de administración vive bajo `/api/admin/...`. El desarrollador que construye su integración decide qué puntos finales llamar — su trabajo como comerciante es asegurarse de que el **alcance de la API** del token cubra esos puntos finales. Si una solicitud se rechaza con un error de permisos, la primera cosa que debe verificar es si el token ha sido otorgado el alcance correcto en el nivel de acceso correcto.

### Ejemplo: leer el análisis de tráfico web

Spwig expone un punto final `GET /api/admin/analytics/traffic/` que devuelve el análisis de visitas y tráfico para su tienda — una visión general de las visitas y visitantes únicos, tendencias con el tiempo, páginas más populares, geografía de los visitantes y fuentes de referidos. Para permitir que una herramienta de informes o panel de control lea estos datos:

1. Cree un token (o edite uno existente) para esa integración
2. En **Alcances de la API**, establezca **Análisis web** en **Lectura**
3. Guarde el token y píntelo a la integración

Dado que **Análisis web** es un alcance de solo lectura, no hay una opción "Lectura y escritura" para elegir — la integración solo puede recuperar datos de análisis, nunca cambiar la configuración de su tienda.

## Monitoreo del uso del token

La lista de tokens muestra:

- **Conteo de uso** — número total de veces que se ha utilizado el token
- **Último uso** — cuándo se utilizó el token por última vez para hacer una solicitud

Estos campos le ayudan a identificar tokens no utilizados (candidatos para revocación) y detectar actividad inesperada. Un pico repentino en el conteo de uso podría indicar que un token está siendo utilizado por alguien distinto de la integración prevista.

## Revocar un token

Para detener inmediatamente el funcionamiento de un token sin eliminarlo:

1. Haga clic en el nombre del token
2. Desmarque **Activo**
3. Guarde

El token sigue en su lista para referencia, pero se rechaza en cualquier solicitud posterior. Esto es útil cuando necesita suspender temporalmente una integración mientras investiga un problema.

Para eliminar permanentemente un token:

1. Seleccione su casilla en la lista
2. Elija **Eliminar los tokens de API seleccionados** del menú de acciones
3. Confirme la eliminación

Una vez eliminado, un token no puede recuperarse. Si la integración aún necesita acceso, cree un nuevo token y actualice la configuración de la integración.

## Ejemplo: configurar una integración con Zapier

**Escenario:** Desea conectar su tienda con Zapier para automatizar las notificaciones de pedidos.

| Campo | Valor |
|-------|-------|
| Nombre | `Zapier Order Automation` |
| Tipo de token | Integración externa |
| Descripción | Utilizado por Zapier para leer nuevos pedidos y activar notificaciones |
| Alcances de la API | **Pedidos**: Lectura y escritura |
| Activo | Sí |
| Expira en | *(dejar en blanco)* |
| IPs permitidas | *(dejar en blanco — Zapier utiliza IPs dinámicas)* |

Solo se otorga el alcance **Pedidos**, por lo tanto, incluso si este token alguna vez se expusiera, no podría acceder a productos, mensajes de clientes, cuentas de personal o cualquier otra parte de su tienda. Después de guardar, copie el valor completo del token y péguelo en la configuración de la integración de Spwig en Zapier.

- Asigne a cada token un nombre claro y específico — `Shopify Sync v2` es mucho más útil que `Token 3` cuando estés solucionando problemas meses después
- Crea un token por integración — si una integración se ve comprometida, puedes revocar solo ese token sin afectar a otros
- **Conceda solo los alcances que una integración realmente necesite** — una herramienta de informes solo necesita acceso de Lectura a Análisis de Ventas o Análisis Web, no Lectura y Escritura en Productos o Empleados y Roles
- Revisa la **"Este token puede acceder a:"** en el formulario de cambio antes de entregar un token a una tercera parte — es la forma más rápida de confirmar que no has concedido más de lo planeado
- Recuerda que el acceso de escritura también depende del rol del miembro del personal que lo creó — si un alcance muestra Lectura y Escritura pero los escritos aún están fallando, verifica también los permisos del rol de ese usuario
- Establece una fecha de vencimiento para los tokens utilizados en proyectos puntuales o integraciones temporales — esto reduce el riesgo de que tokens olvidados permanezcan activos indefinidamente
- Revisa tu lista de tokens cada pocos meses y desactiva cualquier token con una fecha **Último Uso** que sea inesperadamente antigua, ya que podrían pertenecer a integraciones que ya no estén en funcionamiento
- Si sospechas de que un token ha sido expuesto, desáctivalo inmediatamente, crea un reemplazo y actualiza la integración afectada antes de reactivar el acceso