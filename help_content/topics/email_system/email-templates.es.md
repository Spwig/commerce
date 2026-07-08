---
title: Plantillas de correo electrónico
---

Las plantillas de correo electrónico controlan el diseño y el contenido de cada correo electrónico automático que su tienda envía a los clientes y a usted — confirmaciones de pedido, actualizaciones de envío, restablecimientos de contraseña, notificaciones de reembolso y muchas más. Editar una plantilla cambia todos los correos electrónicos futuros de ese tipo; los correos electrónicos anteriores ya en la bandeja de salida no se ven afectados.

Navegue hasta **Sistema de correo electrónico > Plantillas de correo electrónico** para ver y administrar sus plantillas.

![Lista de plantillas de correo electrónico](/static/core/admin/img/help/email-templates/templates-list.webp)

## Tipos de plantilla

Su tienda incluye plantillas para una amplia gama de eventos. Están agrupadas por categoría:

### Correos electrónicos orientados al cliente
| Plantilla | Enviado cuando |
|----------|-----------|
| Confirmación de pedido | Un cliente completa una compra |
| Confirmación de pago | Un pago se procesa con éxito |
| Pedido enviado | Un pedido se marca como enviado |
| Confirmación de envío | Se agrega un número de seguimiento del envío |
| Confirmación de entrega | Un pedido se marca como entregado |
| Pedido cancelado | Un pedido se cancela |
| Notificación de retraso | Se registra un retraso en un pedido |
| Notificación de reembolso | Se emite un reembolso |

### Correos electrónicos de cuenta
| Plantilla | Enviado cuando |
|----------|-----------|
| Bienvenida a la cuenta | Un cliente crea una cuenta |
| Invitación a la cuenta | Usted invita a un cliente a crear una cuenta |
| Verificación de correo electrónico | Un cliente verifica su dirección de correo electrónico |
| Restablecimiento de contraseña | Un cliente solicita un restablecimiento de contraseña |

### Devoluciones
| Plantilla | Enviado cuando |
|----------|-----------|
| Devoluciones: Solicitud recibida | Un cliente presenta una solicitud de devolución |
| Devoluciones: Aprobada | Una solicitud de devolución se aprueba |
| Devoluciones: Rechazada | Una solicitud de devolución se rechaza |
| Devoluciones: Paquete recibido | El artículo devuelto llega a su ubicación |
| Devoluciones: Reembolso procesado | El reembolso por una devolución se emite |

### Notificaciones de administrador (enviadas a usted)
| Plantilla | Enviado cuando |
|----------|-----------|
| Administrador: Nuevo pedido | Se coloca un nuevo pedido |
| Administrador: Pago fallido | Un intento de pago falla |
| Administrador: Informe de ventas diario | Se genera el resumen de ventas diario |
| Administrador: Alerta de stock bajo | Un producto cae por debajo de su umbral de stock |
| Administrador: Resumen semanal | Se genera el resumen semanal de la tienda |

Plantillas adicionales cubren hitos de seguimiento de envío, actividad del programa de afiliados, confirmaciones de reservas (si la función de reservas está habilitada) y eventos del programa de lealtad.

## Editar una plantilla

1. Navegue hasta **Sistema de correo electrónico > Plantillas de correo electrónico**
2. Encuentre la plantilla que desea editar. Puede filtrar por **Tipo de plantilla**, **Idioma** o **Estado** usando los filtros a la derecha
3. Haga clic en la plantilla para abrirla
4. Edite la **Línea de asunto** (el asunto del correo electrónico mostrado en la bandeja de entrada del cliente)
5. Edite el **Contenido HTML** para la versión de diseño completo del correo electrónico
6. Opcionalmente, edite el **Contenido de texto** — una versión de texto plano para clientes de correo electrónico que no admiten HTML
7. Haga clic en **Guardar**

> **Correos electrónicos HTML:** El campo de contenido HTML acepta HTML estándar, incluyendo CSS en línea. Spwig lo renderiza en un correo electrónico correctamente formateado. Si usa marcado MJML, se compila automáticamente al guardar.

## Previsualizar una plantilla

Antes de guardar, puede previsualizar cómo se verá la plantilla en un cliente de correo electrónico:

1. Abra la plantilla que desea previsualizar
2. Haga clic en el botón **Previsualizar** (visible en la lista de plantillas o en la página de detalles de la plantilla)
3. Se abre una previsualización en una nueva pestaña del navegador mostrando el correo electrónico renderizado

Esto le permite verificar el diseño, el formato y la apariencia de las variables de marcador de posición antes de que la plantilla se active.

## Variables de plantilla

Las variables son marcadores de posición en su plantilla que Spwig reemplaza con datos reales al enviar el correo electrónico. Se escriben como `{{ variable_name }}`.

Variables comunes disponibles en la mayoría de las plantillas:

| Variable | Reemplazado con |
|----------|---------------|
| `{{ customer_name }}` | El nombre completo del cliente |
| `{{ order_number }}` | El número de referencia del pedido |
| `{{ order_total }}` | El monto total del pedido |
| `{{ store_name }}` | El nombre de tu tienda |
| `{{ store_url }}` | La dirección web de tu tienda |
| `{{ tracking_number }}` | El número de seguimiento del envío |
| `{{ tracking_url }}` | Un enlace clickeable para seguir el envío |

Las variables exactas disponibles dependen del tipo de plantilla. Las variables relevantes para una plantilla relacionada con un pedido (como `{{ order_number }}`) no están disponibles en una plantilla de cuenta (como Restablecer contraseña). Si incluyes una variable que no sea aplicable, aparecerá en blanco o sin reemplazar.

## Soporte de idioma

Cada tipo de plantilla puede tener una versión para cada idioma que tu tienda soporte. El campo **Idioma** en cada plantilla controla qué versión de idioma está activa.

Spwig selecciona automáticamente la versión correcta del idioma según la preferencia de idioma del cliente al enviar. Si no existe una plantilla para el idioma del cliente, Spwig recurre a la versión en inglés.

Para agregar una plantilla para un nuevo idioma:
1. Abre una plantilla existente
2. Haz clic en **Clonar plantilla** desde el menú **Acciones**
3. Establece el **Código de idioma** en la clonación al nuevo idioma
4. Traduce el contenido
5. Activa la plantilla clonada

## Clonar, activar y desactivar plantillas

### Clonar una plantilla

Clonar crea una copia exacta de una plantilla — útil para crear variantes de idioma o probar versiones diferentes sin afectar la plantilla en vivo.

1. Selecciona una o más plantillas en la lista
2. Elige **Clonar plantillas seleccionadas** desde el menú desplegable **Acciones**
3. La clonación se crea como inactiva — edita y actívala cuando estés listo

### Activar y desactivar plantillas

Una plantilla debe estar **activa** para ser usada para enviar. Solo se usa una plantilla activa por tipo y combinación de idioma en un momento dado.

Para activar o desactivar en masa:
1. Selecciona las plantillas
2. Elige **Activar plantillas seleccionadas** o **Desactivar plantillas seleccionadas** desde el menú desplegable **Acciones**

O abre una plantilla individual y activa/desactiva el cuadro de verificación **Activo**.

## Plantillas del sistema

Las plantillas marcadas con un distintivo **Sistema** son las plantillas predeterminadas sembradas por Spwig. No se pueden eliminar. Puedes editelas directamente o clonarlas para crear una versión personalizada.

## Consejos

- Siempre previamente visualiza una plantilla después de editarla para detectar problemas de formato antes de que los clientes las vean
- Mantén los asuntos cortos y específicos — `Tu pedido #10045 ha sido enviado` funciona mejor que asuntos genéricos como `Actualización de nuestra tienda`
- Edita también el contenido en texto plano — algunos clientes de correo electrónico solo muestran la versión en texto plano, y algunos clientes lo prefieren
- Clona la versión en inglés de una plantilla como punto de partida antes de crear una versión traducida
- Si deseas probar un cambio sin afectar los correos electrónicos en vivo, clona la plantilla, edita la clonación y deja ambas activas brevemente mientras verificas la vista previa — luego desactiva la original
- Las plantillas de notificación del administrador (como **Administrador: Nuevo pedido**) se envían a la dirección de correo electrónico del administrador de tu tienda — asegúrate de que esa dirección de correo electrónico esté correcta en la configuración de tu tienda