---
title: Servicios alojados de Spwig
---

Spwig incluye tres servicios en la nube opcionales que tu tienda puede usar sin necesidad de que tú configure o aloje nada: **GeoIP** detecta dónde se encuentra ubicado tu visitante, **Geocoder** convierte las direcciones de los clientes en coordenadas de mapa, y **Push** envía notificaciones instantáneas a tu aplicación móvil de administración de Spwig. En la edición Comunitaria (gratuita), cada servicio viene con un límite mensual generoso. Cuando cualquier servicio se acerca a su límite, Spwig te advierte en la administración para que puedas decidir si deseas actualizar antes de que tus clientes noten algo.

## Los tres servicios alojados

### GeoIP — detección del país del visitante

GeoIP busca el país de cada visitante basándose en su dirección IP. Tu tienda utiliza esta información para mostrar automáticamente la moneda correcta cuando un cliente llega, y para rellenar previamente el campo del país durante el proceso de pago. Por ejemplo, un visitante de Alemania verá los precios en euros, y un visitante de Japón verá los precios en yenes — sin necesidad de elegir manualmente.

Cada carga de página donde GeoIP realiza una búsqueda cuenta contra tu cuota mensual. Las visitas repetidas desde la misma sesión de navegador no consumen cada una una búsqueda; el resultado se almacena en caché para la sesión. Las búsquedas de GeoIP solo ocurren en el sitio de venta, no en tu panel de administración.

### Geocoder — direcciones a coordenadas

Geocoder traduce las direcciones escritas por los clientes en coordenadas geográficas (latitud y longitud). Tu tienda utiliza estas coordenadas para dos propósitos: calcular costos de envío basados en la distancia cuando tengas puntos de recogida o reglas de envío basadas en radio, y alimentar las sugerencias de autocompletado de direcciones en la página de pago para que los clientes puedan encontrar su dirección rápidamente.

Una búsqueda del geocoder se activa cuando un cliente selecciona o confirma una dirección durante el proceso de pago. Al igual que GeoIP, los resultados se almacenan en caché para que la misma dirección solo se busque una vez por sesión.

### Push — notificaciones de la aplicación de administración

Push envía notificaciones en tiempo real a tu aplicación móvil de comerciante de Spwig. Cuando llega un nuevo pedido, cuando el stock baja por debajo de un umbral, o cuando un cliente envía un mensaje, Push envía una notificación inmediata a tu dispositivo para que puedas responder sin necesidad de tener abierta la interfaz de administración.

Cada notificación enviada a tu dispositivo cuenta como una solicitud de push contra tu cuota mensual.

## La edición gratuita de la comunidad

En la edición Comunitaria de Spwig, cada servicio se incluye sin costo alguno hasta un límite de solicitudes mensuales. Los límites exactos están establecidos por Spwig y pueden variar; tu panel de administración siempre muestra las cifras actuales para tu instalación. Los planes pagados (Starter, Growth, Pro, Pro Plus) e instalaciones autoalojadas con una licencia pagada tienen límites más altos para cada servicio.

Cuando un servicio alcanza el 100% de su cuota de la edición Comunitaria, las solicitudes a ese servicio se detienen hasta que el contador se reinicie al siguiente mes calendario. El impacto en tu tienda depende de qué servicio esté afectado:

| Servicio | ¿Qué ocurre al alcanzar el 100% |
|---------|----------------------|
| GeoIP | La detección automática de moneda se retrocede a la moneda predeterminada de tu tienda. Los clientes aún pueden cambiar la moneda manualmente. |
| Geocoder | El autocompletado de direcciones deja de ofrecer sugerencias. Los clientes aún pueden escribir manualmente su dirección. El cálculo del costo de envío continúa usando las coordenadas conocidas anteriormente. |
| Push | Las nuevas notificaciones de la aplicación de administración se filan pero no se entregan hasta el siguiente mes o una actualización. |

Tu tienda continúa operando normalmente en todos los casos — no se pierden pedidos y los clientes aún pueden pagar. Los efectos están limitados a características de conveniencia.

## Leyendo el mosaico del panel

El mosaico **Uso de servicios de Spwig** aparece en la página de inicio de tu panel de administración. Muestra una barra de progreso para cada uno de los tres servicios.

Cada fila en el mosaico sigue el mismo diseño:

- **Nombre del servicio** (izquierda) — GeoIP, búsqueda de direcciones (Geocoder) o notificaciones de push.
- **Barra de progreso** (centro) — se llena de izquierda a derecha a medida que aumenta el uso.

El color de la barra cambia a medida que se acercan los límites:
  - **Verde** — el uso es inferior al 80%.

Todo funciona normalmente.
  - **Amber** — el uso está entre el 80% y el 99%.

El servicio aún está en funcionamiento pero se está acercando al límite.
  - **Rojo** — el uso ha alcanzado el 100%.

El servicio ahora está limitado para este mes.
- **Conteo de uso** (derecha) — el número exacto de solicitudes utilizadas de las permitidas en total, por ejemplo `3,241 / 10,000`.

La etiqueta entre paréntesis muestra el período de tiempo, normalmente `(este mes)`.

Si el tile no puede conectarse al servidor de actualizaciones de Spwig para obtener su uso actual (por ejemplo, si su servidor no tiene acceso a internet saliente), la columna de conteo muestra un guion (`—`) para ese servicio. Esto no significa que el servicio esté roto; significa que la visualización del uso está temporalmente no disponible.

### El botón **Upgrade**

Cuando cualquier servicio alcanza el 80% o más, aparece un botón **Upgrade** en la esquina superior derecha del tile. Al hacer clic en él, se abre la página de actualización de Spwig, donde puede comparar planes y aumentar los límites de su servicio. El botón desaparece una vez que el uso disminuya nuevamente por debajo del 80% al inicio del siguiente mes.

## El banner de advertencia de cuota

Además del tile del panel, un banner aparece en la parte superior de cada página de administración cuando cualquier servicio supera el umbral del 80%. El banner solo aparece en instalaciones de la comunidad.

**Banner amarillo — acercándose al límite (80–99%)**

> **Acercándose al límite de servicios hospedados:** Uno de tus servicios de Spwig supera el 80% de su cuota de la versión Comunitaria. Actualiza para aumentar el límite antes de que se alcance.

Este banner es una advertencia temprana. Tus servicios aún están en funcionamiento y tienes tiempo para decidir si deseas actualizar antes de que termine el mes.

**Banner rojo — límite alcanzado (100%)**

> **Límite de servicios de Spwig alcanzado:** Uno de tus servicios hospedados ha alcanzado su cuota de la versión Comunitaria. Actualiza para mantenerlos en funcionamiento sin interrupciones.

Este banner aparece cuando al menos un servicio ha alcanzado el 100% y ahora está limitado. Hacer clic en **Upgrade** en cualquiera de los banners abre la misma página de actualización que el botón del tile.

El banner desaparece automáticamente al inicio del siguiente mes calendario cuando los contadores se reinician, o inmediatamente después de que actualices a un plan de pago.

## Alerta por correo electrónico al alcanzar el 90%

Cuando cualquier servicio supera el 90% de su cuota, Spwig también envía un aviso por correo electrónico una vez al correo electrónico configurado en la configuración de tu tienda (**Configuración > Configuración de la tienda > Contacto > Correo electrónico de administrador**). El correo se envía como máximo una vez por servicio por mes calendario, por lo que no recibirás mensajes en exceso. No se envía ningún correo al alcanzar el 100%, ya que en ese momento el banner dentro de la administración ya hace clara la situación.

Si no recibes el correo, verifica que tu dirección de correo electrónico de administrador esté configurada correctamente en **Configuración > Configuración de la tienda**.

## Actualizar tu plan

Cuando actualices de la versión Comunitaria a cualquier plan de pago, los límites más altos se aplican de inmediato — no se requiere reiniciar la tienda ni realizar cambios de configuración. El tile del panel mostrará el nuevo límite más alto la próxima vez que se actualice (dentro de cinco minutos).

Para actualizar, haz clic en el botón **Upgrade** en el tile del panel o en el banner de cuota, o visita directamente la página de actualización de Spwig. Los planes de pago incluyen los mismos tres servicios hospedados (GeoIP, Geocoder, Push) con límites mensuales elevados, además del acceso a la entrega de correos electrónicos hospedados por Spwig y soporte prioritario.

## Instalación autónoma y licencias Pro

Si ejecutas una instalación autónoma de Spwig con una licencia de pago, tu nivel de licencia determina tus límites de servicio, igual que el plan hospedado equivalente. Tu tienda aún necesita acceso a internet saliente para alcanzar `updates.spwig.com` para que la plataforma obtenga y verifique tu configuración de nivel. Los contadores de uso mostrados en el tile del panel se obtienen de los puntos finales de los servicios hospedados en `geoip.spwig.com`, `geocoder.spwig.com` y `push.spwig.com`.

Actualmente no hay opción para reemplazar GeoIP, Geocoder o Push con alternativas autónomas — estos servicios se proporcionan exclusivamente por la infraestructura de Spwig y están incluidos en todas las ediciones.

## Consejos

Mantén todo el formato markdown, rutas de imágenes, bloques de código y términos técnicos.

- **Revise regularmente el tile al final de los meses ocupados** — un evento de ventas o promoción puede aumentar significativamente las consultas de GeoIP y Geocoder.

El tile te avisa con anticipación antes de que los clientes se vean afectados.
- **El cambio de moneda es invisible para la mayoría de los clientes** — si GeoIP alcanza su límite, los clientes verán la moneda predeterminada de tu tienda.

Esto rara vez es un problema grave para tiendas que principalmente sirven un solo mercado; es más relevante para tiendas verdaderamente internacionales.
- **El autocompletado de direcciones es una comodidad, no un obstáculo** — cuando Geocoder se limita, los clientes aún pueden escribir y enviar su dirección normalmente.

Si realizas promociones frecuentes que generan un alto tráfico en el checkout, considera actualizarte antes de los períodos ocupados.
- **El control de flujo no pierde notificaciones permanentemente** — las notificaciones en cola del período de control de flujo no se entregan retroactivamente cuando el mes se reinicia o después de una actualización.

Si dependes mucho del push para alertas de pedidos con plazos ajustados, actualizarte antes de alcanzar el límite asegura que no te pierdas nada.
- **El caché de 5 minutos significa que el tile no es perfectamente en tiempo real** — las cifras de uso se actualizan aproximadamente cada cinco minutos en segundo plano.

Durante períodos de tráfico inusualmente alto, el uso real puede estar ligeramente por delante de lo que muestra el tile.
- **Establece tu dirección de correo electrónico de administrador** — el correo electrónico del 90% solo funciona si **Configuración > Configuración de la tienda > Correo electrónico del administrador** está completado.

Es útil confirmar que esté configurado correctamente para que recibas la alerta antes de que surjan problemas.