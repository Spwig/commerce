---
title: Higiene de listas y supresiones
---

Cada dirección de correo electrónico que genera un rebote definitivo, marca tus correos como spam o falla repetidamente al recibir tus mensajes pone en riesgo el resto de tu lista — los proveedores de buzones de correo evalúan tu reputación como remitente según lo limpia que sea tu actividad de envío, y una lista sucia significa que más de *cada* campaña terminará en la carpeta de spam. Campaign Studio te protege de esto automáticamente mediante la **higiene de listas**: vigila las direcciones no entregables y las que presentan quejas, y deja de enviarles correos de marketing, sin que tengas que configurar nada.

Esto es diferente de las bajas de suscripción. Una dirección dada de baja ha retirado su consentimiento; una dirección **suprimida** es aquella que Spwig ha determinado que es insegura o imposible de seguir enviándole correos, independientemente del consentimiento.

## Cómo se suprimen las direcciones

Spwig añade una dirección a la **Lista de supresión** automáticamente cuando:

| Disparador | Qué significa |
|---------|---------------|
| **Rebote definitivo** | La dirección no existe, o el dominio se negó a aceptar correos para ella — no entregable de forma permanente. |
| **Queja de spam** | Un destinatario marcó tu correo como spam o correo no deseado. |
| **Rebotes blandos repetidos** | La dirección generó un rebote blando (buzón lleno, servidor temporalmente no disponible) 5 veces dentro de una ventana móvil de 30 días. Un solo rebote blando se trata como un contratiempo temporal y se ignora — solo un patrón de fallos repetidos activa la supresión. |
| **Bloqueo manual** | Tú mismo añadiste la dirección. |

Una vez que una dirección está suprimida, Spwig deja de enviarle inmediatamente cualquier **campaña** o correo de **journey** — no se requiere ninguna otra acción por tu parte.

## De dónde proviene la señal

Spwig puede enterarse de un rebote o queja desde varios lugares diferentes, mostrados como **Origen** en cada dirección suprimida:

- **Rechazado al enviar** — tu servidor de correo rechazó la dirección inmediatamente cuando Spwig intentó enviarle.
| **Webhook del proveedor** — si has conectado un proveedor de correo (como SendGrid, Amazon SES, Mailgun o Postmark), ese proveedor informa a Spwig sobre los rebotes y quejas a medida que ocurren.
- **Pasarela de correo** — si tu tienda envía a través de la pasarela de correo alojada por Spwig, Spwig obtiene los informes de rebotes de la pasarela en tu nombre.
- **Añadida manualmente** — tú ingresaste la dirección desde el panel de administración.

No necesitas configurar nada para beneficiarte de esto — sin importar cómo envíes tus correos, Spwig está vigilando los fallos y manteniendo tu lista limpia.

## El panel de Campaign Studio

Abre **Campaign Studio** y busca la tarjeta **Direcciones suprimidas**. Muestra el número total de direcciones actualmente suprimidas, además de cuántas son nuevas en los últimos 30 días. Haz clic en la tarjeta para abrir la lista completa de Supresiones.

![La tarjeta de estadísticas de direcciones suprimidas en el panel de Campaign Studio, mostrando un total y un recuento de "nuevas en los últimos 30 días"](/static/core/admin/img/help/list-hygiene/dashboard-suppressed-card.webp)

Un recuento que sube de manera constante es normal — cada lista acumula algunas direcciones malas con el tiempo a medida que las personas cambian de trabajo, cierran cuentas o abandonan sus buzones. Un aumento repentino merece una investigación; consulta [Bandeja de salida de correo](email-outbox) para verificar si un envío en particular tuvo un número inusual de fallos.

## La lista de Supresiones

Haz clic en **Supresiones** para ver cada dirección suprimida, por qué fue suprimida y de dónde provino la señal.

![La lista de Supresiones mostrando direcciones suprimidas con sus columnas de Motivo y Origen](/static/core/admin/img/help/list-hygiene/suppressions-list.webp)

Usa los filtros de la derecha para filtrar la lista por **Motivo** o **Origen** — por ejemplo, para revisar cada dirección bloqueada manualmente, o todo lo que llegó a través de un webhook de proveedor.

## Añadir una dirección manualmente

Para bloquear una dirección tú mismo — una dirección de abuso conocida, un competidor que está raspando tu boletín, o cualquier otra cosa que quieras mantener fuera de tu lista — haz clic en **+ Añadir dirección suprimida** y completa:

- **Email** — la dirección a bloquear
- **Reason** — elija **Manually blocked** para una entrada añadida manualmente
- **Source** — elija **Added manually**
- **Detail** — una nota opcional que explica el motivo (útil para sus propios registros y para cualquier personal que revise la lista más adelante)

Guarde la entrada y Spwig dejará de enviarle a esa dirección cualquier correo de campaña o journey de inmediato.

## ¿Cuándo debería liberar una dirección?

Liberar (des-suprimir) una dirección debe ser algo raro y deliberado. Solo hágalo cuando tenga la certeza de que el problema subyacente se ha resuelto realmente; por ejemplo:

- Un cliente le indica que su buzón estaba lleno y que ya lo ha vaciado.
- Una dirección fue suprimida por una racha de rebotes blandos que sabe que fue causada por una interrupción temporal en su proveedor de correo, no por un buzón inexistente.
- Bloqueó una dirección manualmente y más tarde decide que el bloqueo fue un error.

Para liberar una dirección, ábrala en la lista de Supresiones y elimine la entrada; esto levanta el bloqueo para que la dirección pueda recibir correos nuevamente. No libere una dirección con rebote duro solo porque sea inconveniente perder un suscriptor; la dirección no existe, y volver a enviarle solo causará otro rebote y le costará reputación una segunda vez. Del mismo modo, liberar una dirección con queja de spam rara vez ayuda: ese destinatario le dijo a su proveedor de correo que no desea recibir sus correos, y volver a enviarle correos corre el riesgo de generar otra queja.

## Qué no se ve afectado

La supresión solo se aplica a las **campañas de marketing y journeys** enviadas a través de Campaign Studio. No afecta al **correo transaccional**: las confirmaciones de pedido, actualizaciones de envío, restablecimientos de contraseña y otros correos que su tienda envía como parte de una acción de pedido o de cuenta siempre se envían, incluso a una dirección suprimida. La supresión existe para proteger la reputación de su remitente de marketing; no es una lista de bloqueo general de correo para su tienda.

## Consejos

- No luche contra el sistema liberando manualmente cada rebote duro que vea: un rebote duro significa que la dirección ha desaparecido, y volver a añadirla a sus envíos solo causará otro rebote.
- Revise la lista de Supresiones después de un envío masivo si su tasa de apertura parece inusualmente baja: una oleada de rebotes blandos en un dominio compartido (p. ej., un servidor de correo corporativo con problemas) puede ser una señal de un problema temporal de entrega que vale la pena investigar con su proveedor.
- Si está migrando a Spwig desde otra plataforma, no importe manualmente su antigua lista de bloqueo completa como supresiones; deje que Spwig aprenda de los rebotes y quejas reales en esta lista, para no bloquear accidentalmente direcciones que habrían sido entregadas sin problemas.
- Revise ocasionalmente la columna **Source**: muchas entradas de **Provider webhook** confirman que la notificación de rebotes de su proveedor de correo está conectada y funcionando.
- Mantenga el campo **Detail** con significado al añadir un bloqueo manual; es el único registro del motivo por el que se tomó esa decisión una vez que ha pasado el tiempo.