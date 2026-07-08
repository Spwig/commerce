---
title: Configuración de correo electrónico
---

La configuración de correo electrónico controla cómo tu tienda envía correos electrónicos transaccionales — confirmaciones de pedido, notificaciones de envío, restablecimiento de contraseña y más. Spwig incluye un servidor SMTP integrado y admite proveedores de correo electrónico externos para una mayor entrega.

![Cuentas de correo electrónico](/static/core/admin/img/help/email-configuration/email-accounts.webp)

## Proveedores disponibles

| Proveedor | Descripción |
|----------|-------------|
| **Servidor SMTP integrado** | Servidor de correo electrónico gratuito y autoalojado incluido con Spwig. Firma automática DKIM. |
| **Gmail API** | Envía mediante tu cuenta de Gmail o Google Workspace usando la autenticación OAuth. |
| **SMTP genérico** | Conecta cualquier servidor SMTP (SendGrid, Mailgun, Amazon SES o tu propio servidor de correo). |

## Configuración de correo electrónico

Navega a **Configuración > Cuentas de correo electrónico** y haz clic en **Añadir cuenta de correo electrónico** para iniciar el asistente de configuración.

### Paso 1: Seleccionar proveedor

Elige tu proveedor de correo electrónico. El servidor SMTP integrado es la opción más sencilla para comenzar — no requiere cuentas externas.

### Paso 2: Configurar credenciales

Introduce las credenciales para tu proveedor elegido:

- **Servidor SMTP integrado** — No se necesitan credenciales. El servidor funciona en tu instalación de Spwig.
- **Gmail API** — Autenticación mediante OAuth de Google. Te redirigirán a iniciar sesión con tu cuenta de Google.
- **SMTP genérico** — Introduce la dirección del servidor SMTP, el puerto, el nombre de usuario y la contraseña.

### Paso 3: Configuración del remitente

Establece la identidad del remitente para los correos electrónicos salientes:

- **Correo electrónico de remitente** — La dirección de correo electrónico que aparece en el campo "De" (por ejemplo, orders@yourstore.com)
- **Nombre del remitente** — El nombre que se muestra junto a la dirección de correo electrónico (por ejemplo, "Nombre de tu tienda")
- **Correo electrónico de respuesta** — Dónde se dirigen las respuestas del cliente (puede diferir de la dirección de remitente)

### Paso 4: Validación DNS

Verifica los registros de autenticación de correo electrónico de tu dominio. El asistente comprueba tres registros DNS:

| Registro | Propósito |
|--------|---------|
| **SPF** | Autoriza tu servidor para enviar correo electrónico en nombre de tu dominio |
| **DKIM** | Firma digitalmente los correos electrónicos para probar que no han sido manipulados |
| **DMARC** | Indica a los servidores receptores qué hacer con los correos electrónicos que no pasan las pruebas SPF/DKIM |

Para cada registro, el asistente muestra:
- **Estado actual** — Si el registro está correctamente configurado
- **Valor requerido** — El registro DNS exacto que debe añadirse en tu registrador de dominio
- **Estado de propagación** — Si los cambios recientes han surtido efecto (los cambios DNS pueden tardar hasta 48 horas)

El servidor SMTP integrado genera automáticamente claves DKIM para tu dominio.

### Paso 5: Enviar correo electrónico de prueba

Envía un correo electrónico de prueba para verificar que todo funcione:
1. Introduce una dirección de correo electrónico del destinatario
2. Haz clic en **Enviar prueba**
3. Revisa tu bandeja de entrada para el mensaje de prueba
4. Verifica que el correo llegue sin advertencias de spam

### Paso 6: Guardar y activar

Guarda la configuración y establece la cuenta como activa. Marca como **Predeterminada** si debe ser la cuenta de correo electrónico principal.

## Plantillas de correo electrónico

Spwig incluye más de 30 plantillas de correo electrónico para cada evento transaccional. Navega a **Configuración > Plantillas de correo electrónico** para gestionarlas.

### Tipos de plantillas

Las plantillas cubren todos los eventos de la tienda, incluyendo:
- **Ciclo de vida del pedido** — Confirmación, procesamiento, enviado, entregado, cancelado
- **Pago** — Recibo, confirmación de reembolso, pago fallido
- **Cuenta del cliente** — Bienvenida, restablecimiento de contraseña, verificación de correo electrónico
- **Tarjetas regalo** — Entrega, notificación de saldo
- **Envío** — Actualizaciones de seguimiento, confirmación de entrega
- **Productos digitales** — Enlaces de descarga, claves de licencia
- **Marketing** — Recuperación de carritos abandonados, solicitudes de reseñas

### Personalización de plantillas

1. Navega a la lista de plantillas
2. Haz clic en una plantilla para editarla
3. Modifica la línea de asunto, encabezado, contenido del cuerpo y pie de página
4. Usa variables de plantilla (por ejemplo, `{{ order.number }}`, `{{ customer.name }}`) para contenido dinámico
5. Previsualiza el correo electrónico antes de guardar

### Soporte multilingüe

Las plantillas de correo electrónico admiten múltiples idiomas:
- Cada plantilla puede tener traducciones para todos los idiomas activos de tu tienda
- El sistema envía correos electrónicos en el idioma preferido del cliente
- **Cadena de retroceso de idioma** — Si no hay una traducción disponible, el sistema retrocede al idioma predeterminado de la tienda
- Usa la función **Traducción con IA** para traducir automáticamente las plantillas a otros idiomas

### Clonar plantillas

Para crear una versión personalizada de una plantilla del sistema:
1. Abre la plantilla que deseas modificar
2. Haz clic en **Clonar plantilla**
3. Edita la versión clonada
4. La clonación tiene prioridad sobre la plantilla original del sistema

## Cola de correos electrónicos

Supervisa los correos electrónicos salientes en **Configuración > Cola de correos electrónicos**:

- **En cola** — Correos electrónicos esperando para ser enviados
- **Enviando** — Actualmente en transmisión
- **Enviados** — Entregados con éxito
- **Fallidos** — No se pudieron entregar (con detalles del error)
- **Rechazados** — Rechazados por el servidor de correo del destinatario

Haz clic en cualquier correo electrónico para ver sus detalles completos, incluyendo destinatario, asunto, hora de envío y estado de entrega.

## Seguimiento de entrega

Rastrea la participación en correos electrónicos:
- **Abridos** — Cuántos destinatarios abrieron el correo electrónico
- **Clics** — Clics en enlaces dentro del correo electrónico
- **Rechazos** — Seguimiento de rechazos duros y suaves
- **Reclamos** — Informes de spam de los destinatarios

## Múltiples cuentas

Puedes configurar múltiples cuentas de correo electrónico:
- **Cuenta predeterminada** — Se usa para todos los correos electrónicos salientes a menos que se anule
- **Cuenta de respaldo** — Si la cuenta predeterminada falla, los correos electrónicos se colocan en cola para reintentar
- Usa cuentas diferentes para diferentes propósitos (por ejemplo, una para correos electrónicos transaccionales, otra para marketing)

## Consejos

- Comienza con el **servidor SMTP integrado** para una configuración rápida, luego cambia a un proveedor externo si necesitas mayores volúmenes de envío o mejor entrega.
- Siempre configura los registros **SPF, DKIM y DMARC** — sin ellos, los correos electrónicos tienen mucha más probabilidad de terminar en carpetas de spam.
- Envía un **correo electrónico de prueba** después de cualquier cambio de configuración para verificar que la entrega funcione.
- Supervisa regularmente la cola de correos electrónicos para **fallidos** o **rechazados** — indican problemas de entrega.
- Usa una **dirección de remitente profesional** (por ejemplo, orders@yourstore.com) en lugar de una dirección de correo electrónico gratuita para una mayor confianza y entrega.
- Mantén tus plantillas concisas — los correos electrónicos transaccionales deben entregar información rápidamente, no ser boletines de marketing.