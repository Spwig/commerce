---
title: Configuración de correo electrónico
---

La configuración de correo electrónico controla cómo su tienda envía correos electrónicos transaccionales: confirmaciones de pedidos, notificaciones de envío, restablecimientos de contraseña y más. Spwig incluye un servidor SMTP integrado y admite proveedores de correo electrónico externos para una mayor entrega.

![Cuentas de correo electrónico](/static/core/admin/img/help/email-configuration/email-accounts.webp)

## Proveedores disponibles

| Proveedor | Descripción |
|----------|-------------|
| **SMTP integrado** | Servidor de correo electrónico alojado por sí mismo gratuito incluido con Spwig. Firma DKIM automática. |
| **API de Gmail** | Envíe a través de su cuenta de Gmail o Google Workspace usando la autenticación OAuth. |
| **SMTP genérico** | Conéctese a cualquier servidor SMTP (SendGrid, Mailgun, Amazon SES, o su propio servidor de correo). |

## Configuración del correo electrónico

Navegue hasta **Configuración > Cuentas de correo electrónico** y haga clic en **Añadir cuenta de correo electrónico** para iniciar el asistente de configuración.

### Paso 1: Seleccionar proveedor

Elija su proveedor de correo electrónico. El servidor SMTP integrado es la opción más sencilla para comenzar, ya que no requiere cuentas externas.

### Paso 2: Configurar credenciales

Ingrese las credenciales para su proveedor elegido:

- **SMTP integrado** — No se necesitan credenciales. El servidor funciona en su instalación de Spwig.
- **API de Gmail** — Autenticación mediante Google OAuth. Será redirigido para iniciar sesión con su cuenta de Google.
- **SMTP genérico** — Ingrese la dirección del servidor SMTP, puerto, nombre de usuario y contraseña.

### Paso 3: Configuración del remitente

Establezca la identidad del remitente para los correos electrónicos salientes:

- **Correo electrónico desde** — La dirección de correo electrónico que aparece en el campo "De" (por ejemplo, pedidos@tutienda.com)
- **Nombre del remitente** — El nombre de visualización junto a la dirección de correo electrónico (por ejemplo, "Nombre de tu tienda")
- **Correo electrónico de respuesta** — A dónde se dirigen las respuestas de los clientes (puede diferir de la dirección de correo electrónico desde)

### Paso 4: Validación de DNS

Verifique los registros de autenticación de correo electrónico de su dominio. El asistente comprueba tres registros DNS:

| Registro | Propósito |
|--------|---------|
| **SPF** | Autoriza a su servidor para enviar correo electrónico en nombre de su dominio |
| **DKIM** | Firma digitalmente los correos electrónicos para demostrar que no han sido alterados |
| **DMARC** | Indica a los servidores receptores qué hacer con los correos electrónicos que no pasen las pruebas SPF/DKIM |

Para cada registro, el asistente muestra:
- **Estado actual** — Si el registro está configurado correctamente
- **Valor requerido** — El registro DNS exacto que agregar en su registrador de dominios
- **Estado de propagación** — Si los cambios recientes han tenido efecto (los cambios de DNS pueden tardar hasta 48 horas)

El servidor SMTP integrado genera automáticamente las claves DKIM para su dominio.

### Paso 5: Enviar correo de prueba

Envíe un correo de prueba para verificar que todo funcione:
1. Ingrese una dirección de correo electrónico del destinatario
2. Haga clic en **Enviar correo de prueba**
3. Verifique su bandeja de entrada para el mensaje de prueba
4. Verifique que el correo llegue sin advertencias de spam

### Paso 6: Guardar y activar

Guarde la configuración y marque la cuenta como activa. Márcalo como **Predeterminado** si debe ser la cuenta de correo electrónico principal.

## Plantillas de correo electrónico

Spwig incluye más de 30 plantillas de correo electrónico para cada evento transaccional. Navegue hasta **Configuración > Plantillas de correo electrónico** para gestionarlas.

### Tipos de plantilla

Las plantillas cubren todos los eventos de la tienda, incluyendo:
- **Ciclo de vida del pedido** — Confirmación, procesamiento, enviado, entregado, cancelado
- **Pago** — Recibo, confirmación de reembolso, pago fallido
- **Cuenta del cliente** — Bienvenida, restablecimiento de contraseña, verificación de correo electrónico
- **Tarjetas de regalo** — Entrega, notificación de saldo
- **Envío** — Actualizaciones de seguimiento, confirmación de entrega
- **Productos digitales** — Enlaces de descarga, claves de licencia
- **Marketing** — Recuperación de carrito abandonado, solicitudes de reseña

### Personalizar plantillas

1. Navegue hasta la lista de plantillas
2. Haga clic en una plantilla para editarla
3. Modifique la línea de asunto, el encabezado, el contenido del cuerpo y el pie de página
4. Use variables de plantilla (por ejemplo, `{{ order.number }}`, `{{ customer.name }}`) para contenido dinámico
5. Vaya a la vista previa del correo electrónico antes de guardar

### Soporte multilingüe

Preserve all markdown formatting, image paths, code blocks, and technical terms.

Las plantillas de correo electrónico admiten varios idiomas:
- Cada plantilla puede tener traducciones para todos los idiomas activos de su tienda
- El sistema envía correos electrónicos en el idioma preferido del cliente
- **Cadena de respaldo de idioma** — Si no está disponible una traducción, el sistema recurre al idioma predeterminado de la tienda
- Utilice la función **Traducción con IA** para traducir automáticamente las plantillas a otros idiomas

### Clonar plantillas

Para crear una versión personalizada de una plantilla del sistema:
1. Abra la plantilla que desea modificar
2. Haga clic en **Clonar plantilla**
3. Edite la versión clonada
4. El clon tiene prioridad sobre la plantilla del sistema original

## Cola de correos electrónicos

Monitoree los correos salientes en **Configuración > Cola de correos**:

- **En cola** — Correos esperando ser enviados
- **Enviando** — Actualmente en transmisión
- **Enviado** — Entregado con éxito
- **Fallido** — No se pudo entregar (con detalles del error)
- **Rebotado** — Rechazado por el servidor de correo del destinatario

Haga clic en cualquier correo para ver todos sus detalles, incluidos el destinatario, el asunto, la hora de envío y el estado de entrega.

## Seguimiento de entrega

Realice un seguimiento de la interacción con los correos:
- **Aperturas** — Cuántos destinatarios abrieron el correo
- **Clics** — Clics en los enlaces dentro del correo
- **Rebotes** — Seguimiento de rebotes duros y suaves
- **Quejas** — Informes de spam de los destinatarios

## Múltiples cuentas

Puede configurar varias cuentas de correo electrónico:
- **Cuenta predeterminada** — Se utiliza para todos los correos salientes a menos que se anule
- **Respaldo** — Si la cuenta predeterminada falla, los correos se ponen en cola para reintentar
- Use cuentas diferentes para diferentes propósitos (por ejemplo, una para correos transaccionales y otra para marketing)

## Modo de entrega de correo

Vaya a **Configuración > Configuración de la tienda** para controlar cómo su tienda maneja los correos salientes. Estos ajustes son útiles durante el desarrollo y las pruebas.

| Modo | Descripción |
|------|-------------|
| **En vivo** | Los correos se entregan normalmente a destinatarios reales |
| **Pausado** | Los correos se retienen en la cola y no se envían hasta que vuelva a cambiar a En vivo |
| **Solo registro** | Los correos se registran en la bandeja de salida pero nunca se entregan |

### Redirección de prueba de correo

Establezca una dirección de **Correo de redirección de prueba** para interceptar todos los correos salientes y redirigirlos a una única dirección. Cuando se establece, cada correo, independientemente del destinatario real, va a esa dirección en su lugar. Esto es útil para probar plantillas de correo sin enviar accidentalmente a clientes reales. Deje en blanco para enviar correos a destinatarios reales.

### Lista blanca de correo en modo sandbox

En modo sandbox o de desarrollo, puede restringir la entrega de correos a una lista blanca de direcciones aprobadas. Solo se entregarán los correos a direcciones en la lista blanca. Todos los demás correos se registran pero nunca se envían. El correo del administrador siempre se incluye automáticamente. Puede agregar hasta 10 direcciones.

## Consejos

- Comience con el servidor **SMTP integrado** para una configuración rápida, luego cambie a un proveedor externo si necesita volúmenes de envío más altos o una mejor entregabilidad.
- Configure siempre los registros **SPF, DKIM y DMARC** — sin ellos, es mucho más probable que los correos terminen en las carpetas de spam.
- Envíe un **correo de prueba** después de cualquier cambio de configuración para verificar que la entrega funcione.
- Monitoree la cola de correos regularmente en busca de correos **fallidos** o **rebotados** — estos indican problemas de entregabilidad.
- Use una **dirección de remitente profesional** (por ejemplo, orders@yourstore.com) en lugar de una dirección de correo gratuita para una mejor confianza y entregabilidad.
- Mantenga sus plantillas concisas — los correos transaccionales deben entregar información rápidamente, no ser boletines de marketing.
