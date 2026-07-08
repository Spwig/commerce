---
title: Configuración del proveedor de SMS
---

Las notificaciones por SMS mantienen a tus clientes informados en cada paso de su pedido, desde la confirmación hasta la entrega. Para enviar mensajes de SMS o WhatsApp desde tu tienda, conecta una cuenta de un proveedor de SMS con tus credenciales. Una vez conectada, Spwig utilizará esa cuenta para enviar todos los mensajes de texto salientes.

Navega a **Sistema de SMS > Cuentas de Proveedores de SMS** para gestionar tus proveedores de SMS.

![Lista de cuentas de proveedores de SMS](/static/core/admin/img/help/sms-setup/provider-list.webp)

## Añadir un proveedor de SMS

Puedes añadir un proveedor utilizando ya sea el **Asistente de configuración** (recomendado para la primera configuración) o el formulario manual.

### Usando el asistente de configuración

1. Navega a **Sistema de SMS > Cuentas de Proveedores de SMS**
2. Haz clic en **Asistente de configuración** en la barra de herramientas
3. Sigue los pasos guiados:
   - **Paso 1**: Elige tu proveedor de la lista de proveedores disponibles
   - **Paso 2**: Introduce tus credenciales del proveedor (claves API, SID de cuenta, etc.)
   - **Paso 3**: Establece el nombre de visualización y las configuraciones predeterminadas, luego guárdalas
4. El asistente prueba automáticamente la conexión antes de guardar

### Añadir un proveedor manualmente

1. Navega a **Sistema de SMS > Cuentas de Proveedores de SMS**
2. Haz clic en **Explorar Proveedores** para explorar los proveedores de SMS disponibles, o haz clic en **+ Añadir cuenta de proveedor de SMS** directamente
3. En el campo **Proveedor**, selecciona tu proveedor de SMS de la lista desplegable
4. Una vez que selecciones un proveedor, los campos de credenciales aparecerán automáticamente según lo que requiera ese proveedor
5. Rellena los campos de credenciales requeridos (estos varían según el proveedor — consulta las secciones a continuación para proveedores comunes)
6. Introduce un **Nombre de visualización** para identificar esta cuenta (por ejemplo, `Twilio — Principal`)
7. Establece las **Configuraciones predeterminadas** (ver más abajo)
8. Haz clic en **Guardar**

## Credenciales del proveedor

### Twilio

| Campo | Dónde encontrarlo |
|-------|-----------------|
| Account SID | Consola de Twilio → Dashboard |
| Auth Token | Consola de Twilio → Dashboard |
| From Number | Tu número de teléfono de Twilio en formato E.164 (por ejemplo, `+15551234567`) |

### Otros proveedores

Otros componentes de proveedores de SMS instalados mostrarán sus propios campos de credenciales específicos al seleccionarlos. Consulta la documentación de tu proveedor para los valores exactos necesarios — normalmente una clave API o token de acceso y un identificador de remitente.

## Configuraciones predeterminadas

Después de introducir las credenciales, configura cómo se utilizará esta cuenta:

- **Activo** — habilita o deshabilita esta cuenta. Las cuentas inactivas no se utilizan para enviar mensajes, incluso si se establecen como predeterminadas
- **Cuenta de SMS predeterminada** — al marcarla, todas las notificaciones de SMS de tu tienda utilizarán esta cuenta. Solo puede haber una cuenta predeterminada de SMS a la vez
- **Cuenta de WhatsApp predeterminada** — si este proveedor admite WhatsApp (por ejemplo, Twilio a través de la API de WhatsApp Business), marca esta opción para utilizarla como predeterminada para los mensajes de WhatsApp

## Probar la conexión

Después de guardar una cuenta de proveedor, prueba que las credenciales funcionen:

1. Navega a **Sistema de SMS > Cuentas de Proveedores de SMS**
2. Haz clic en tu cuenta de proveedor para abrirla
3. Haz clic en el botón **Probar conexión**
4. Spwig envía una solicitud de prueba al proveedor y actualiza el campo **Estado de conexión**

| Estado | Significado |
|--------|---------|
| Conectado | Las credenciales son válidas y el proveedor es alcanzable |
| Fallo de conexión | Las credenciales son incorrectas o el proveedor no es alcanzable |
| No probado | La conexión aún no ha sido probada |

Si la prueba falla, vuelve a revisar tus credenciales y asegúrate de que tu cuenta tenga los permisos necesarios en el dashboard del proveedor.

## Columna de estado de conexión

La lista de Cuentas de Proveedores de SMS muestra un distintivo **Conexión** con código de color para cada cuenta:

- **Conectado** (verde) — la cuenta está funcionando
- **Fallo de conexión** (rojo) — las credenciales han fallado — actualízalas
- **No probado** (gris) — la cuenta aún no ha sido probada

## Consejos

- Usa el Asistente de configuración para tu primer proveedor — te guía a través de cada campo y prueba la conexión antes de guardar
- Solo puede haber una cuenta como Cuenta de SMS predeterminada a la vez.

Si agrega una segunda cuenta y la marca como predeterminada, la anterior predeterminada se desactiva automáticamente
- Guarde una nota con sus credenciales de API del proveedor en un lugar seguro.

Si las credenciales cambian, actualícelas aquí de inmediato para evitar notificaciones fallidas
- Las cuentas inactivas permanecen en la lista pero no se usan para enviar — útil para mantener credenciales de respaldo sin activarlas
- La mayoría de los proveedores cobran por mensaje enviado — supervise el uso en el panel de control de su proveedor para evitar facturas inesperadas