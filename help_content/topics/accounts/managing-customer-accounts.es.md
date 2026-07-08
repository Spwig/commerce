---
title: Gestión de Cuentas de Clientes
---

Las cuentas de clientes permiten a los comerciantes rastrear la información del cliente, el historial de pedidos y las preferencias. Navegue hasta **Clientes > Todos los Clientes** en el menú lateral de administración para gestionar cuentas de clientes.

![Añadir Cliente](/static/core/admin/img/help/managing-customer-accounts/add-customer.webp)

## Entendiendo Cuentas de Clientes vs Perfiles de Clientes

**Cuentas de Clientes** son las credenciales de inicio de sesión (correo electrónico/contraseña) almacenadas en el modelo de Usuario. **Perfiles de Clientes** almacenan información adicional del cliente como número de teléfono, fecha de nacimiento, preferencias y análisis. Cada cuenta de cliente tiene un perfil correspondiente que almacena este tipo de datos extendidos.

Cuando gestiona clientes en la administración, está trabajando con Perfiles de Clientes que se vinculan a cuentas de Usuario en segundo plano.

## Ver Todos los Clientes

La lista de clientes muestra a todos los clientes registrados con métricas clave:

| Columna | Descripción |
|--------|-------------|
| **Usuario** | Nombre y dirección de correo electrónico del cliente |
| **Estado de Afiliado** | Si el cliente también es un socio afiliado |
| **Valor del Cliente** | Cantidad total gastada por el cliente (codificada con colores) |
| **Segmento del Cliente** | Segmento RFM (Campeón, Leal, En Riesgo, etc.) |
| **Total de Pedidos** | Número de pedidos completados |
| **Días desde Último Pedido** | Recencia de la última compra |
| **Cliente VIP** | Etiqueta si el cliente se marcó como VIP |

### Filtrar Clientes

Use el menú lateral de filtrado para reducir la lista:

- **Estado de Afiliado** — Es Afiliado, No es Afiliado, Pendiente de Afiliado, Activo, Suspendido, Rechazado
- **Diseño del Panel de Control** — Diseño preferido del cliente en el panel de control
- **Suscripción al Boletín** — Si el cliente se inscribió en boletines
- **Correos de Marketing** — Si el cliente se inscribió en correos promocionales
- **Creado en** — Filtre por fecha de registro

### Buscar Clientes

Use la barra de búsqueda para encontrar clientes por:
- Nombre de usuario
- Dirección de correo electrónico
- Nombre
- Apellido
- Número de teléfono

## Ver Detalles del Cliente

Haga clic en el nombre del cliente para ver su perfil completo. La página de detalles del cliente muestra:

![Detalles del Cliente](/static/core/admin/img/help/managing-customer-accounts/customer-detail.webp)

### Sección de Información del Cliente

Detalles de contacto básicos y estado de la cuenta:
- **Usuario** — Enlace a la cuenta de Usuario subyacente
- **Teléfono** — Número de teléfono del cliente
- **Fecha de Nacimiento** — Para verificación de edad y promociones de cumpleaños

### Preferencias del Panel de Control

Cómo el cliente ha personalizado su panel de control de cuenta:
- **Diseño del Panel de Control** — Vista de cuadrícula, lista o compacta
- **Mostrar Historial de Pedidos** — Si el historial de pedidos aparece en el panel de control
- **Mostrar Lista de Deseos** — Si la lista de deseos aparece en el panel de control
- **Mostrar Productos Recientes** — Si los productos recientemente vistos aparecen
- **Mostrar Recomendaciones** — Si las recomendaciones de productos aparecen

### Preferencias de Comunicación

Estado de inscripción del cliente para varias comunicaciones:
- **Suscripción al Boletín** — Inscrito en boletines generales
- **Correos de Marketing** — Inscrito en correos promocionales
- **Notificaciones de Pedido** — Inscrito en actualizaciones del estado del pedido

### Análisis del Cliente

Resúmenes de comportamiento y valor del cliente en solo lectura:
- **Resumen de Análisis del Cliente** — Puntuaciones RFM, segmento, valor de vida útil
- **Resumen del Comportamiento de Compra** — Frecuencia de pedidos, valor promedio por pedido, categorías preferidas
- **Resumen de Engagement** — Último inicio de sesión, tasas de apertura de correos, actividad en el sitio

Estos campos de análisis se calculan automáticamente y no se pueden editar manualmente. Consulte [Entendiendo el Análisis del Cliente](customer-analytics.md) para más detalles.

## Crear una Cuenta de Cliente

Los comerciantes pueden crear manualmente cuentas de clientes para pedidos telefónicos, recogidas en tienda o para registrar clientes al por mayor de antemano.

1. Haga clic en **+ Añadir Perfil de Cliente** en la esquina superior derecha
2. Rellene los campos obligatorios y opcionales:

| Campo | Obligatorio | Descripción |
|-------|-------------|-------------|
| **Usuario** | Sí | Seleccione una cuenta de Usuario existente o cree una nueva |
| **Teléfono** | No | Número de teléfono del cliente |
| **Fecha de Nacimiento** | No | Para verificación de edad y campañas de cumpleaños |
| **Suscripción al Boletín** | No | Inscríbalo en boletines |
| **Correos de Marketing** | No | Inscríbalo en correos de marketing |

### Crear un Nuevo Usuario Mientras Añade un Perfil

Si el cliente aún no tiene una cuenta de Usuario:
1. Haga clic en el icono **+** junto al campo Usuario
2. Ingrese la **dirección de correo electrónico** del cliente (esto se convierte en su nombre de usuario)
3. Ingrese opcionalmente el **nombre** y **apellido**
4. Ingrese opcionalmente una **contraseña**
5. Marque **Enviar correo de restablecimiento de contraseña** si no estableció una contraseña
6. Guarde la cuenta de Usuario
7. Complete los campos del Perfil del Cliente
8. Haga clic en **Guardar**

### Correos de Bienvenida

Después de crear una cuenta de cliente:
- Si estableció una contraseña, el cliente puede iniciar sesión inmediatamente con esa contraseña
- Si no estableció una contraseña, el sistema enviará un correo de restablecimiento de contraseña para que el cliente establezca su propia contraseña
- Puede desencadenar manualmente un correo de bienvenida a través del sistema de correos en **Marketing > Campañas de Correo Electrónico**

## Editar Información del Cliente

Para actualizar los detalles del cliente:
1. Navegue hasta **Clientes > Todos los Clientes**
2. Haga clic en el nombre del cliente
3. Modifique los campos que desee actualizar
4. Haga clic en **Guardar**

### Lo que Puede Editar

**Detalles de Contacto:**
- Nombre (a través de la cuenta de Usuario)
- Dirección de correo electrónico (a través de la cuenta de Usuario)
- Número de teléfono
- Fecha de nacimiento

**Preferencias:**
- Estado de suscripción al boletín
- Inscripción a correos de marketing
- Preferencias de notificación de pedidos
- Diseño del panel de control y configuraciones de visibilidad

### Lo que No Puede Editar

Estos campos se calculan automáticamente basados en el comportamiento del cliente:
- Total gastado / Valor del cliente
- Cantidad de pedidos
- Segmento del cliente (Campeón, Leal, En Riesgo, etc.)
- Puntuaciones RFM
- Predicciones de valor de vida útil
- Fecha del último pedido
- Resúmenes de análisis

Si estos campos aparecen incorrectos, revise los datos subyacentes de pedidos o desencadene un cálculo manual en **Clientes > Análisis** → **Recalcular Métricas**.

## Notas de Cliente

Añada notas internas sobre clientes para rastrear problemas de soporte, solicitudes VIP o tareas de seguimiento.

### Añadir una Nota

1. Abra el perfil del cliente
2. Desplácese hasta la sección **Notas del Cliente** (puede ser una pestaña separada)
3. Haga clic en **+ Añadir Nota**
4. Rellene los detalles de la nota:

| Campo | Descripción |
|-------|-------------|
| **Tipo de Nota** | General, Problema de Soporte, Queja, Comentario Positivo, Servicio VIP, Requiere Seguimiento, Problema de Pago, Problema de Envío |
| **Título** | Resumen breve de la nota |
| **Contenido** | Contenido detallado de la nota |
| **Requiere Seguimiento** | Marque si esta nota requiere acción |
| **Fecha de Seguimiento** | Fecha para seguir el progreso |
| **Completado** | Marque cuando el seguimiento se complete |

### Tipos de Notas

| Tipo | Caso de Uso |
|------|----------|
| **Nota General** | Cualquier observación general sobre el cliente |
| **Problema de Soporte** | Registro de un ticket de soporte o problema |
| **Queja** | Queja del cliente para seguimiento y resolución |
| **Comentario Positivo** | Comentario positivo sobre el cliente o su feedback sobre usted |
| **Servicio VIP** | Solicitud de manejo especial para clientes VIP |
| **Requiere Seguimiento** | Tareas que requieren acción antes de una fecha específica |
| **Problema de Pago** | Notas sobre problemas de pago o disputas |
| **Problema de Envío** | Notas sobre problemas de envío o solicitudes de entrega especiales |

### Ver Historial de Notas

Todas las notas aparecen en orden cronológico en el perfil del cliente. Cada nota muestra:
- Fecha y hora de creación
- Creado por (nombre del miembro del personal)
- Etiqueta del tipo de nota
- Título y contenido
- Estado de seguimiento si aplica

### Notas Internas vs Notas Visibles para el Cliente

Todas las notas del cliente son **internas solamente** por defecto — los clientes nunca ven estas notas. Estas son para la comunicación del equipo de comerciantes solamente.

Si necesita comunicarse con el cliente, use el sistema de correos en **Marketing > Campañas de Correo Electrónico** o agregue un comentario al pedido específico.

## Convertir un Cliente Invitado en Cliente Registrado

Los clientes invitados se crean automáticamente cuando alguien completa el pago sin crear una cuenta. Su nombre de usuario sigue el patrón `guest_10374` donde el número es un ID único.

Para convertir a un invitado en un cliente registrado:

1. Navegue hasta **Clientes > Todos los Clientes**
2. Busque al invitado por su dirección de correo electrónico de pedido
3. Haga clic en el perfil del cliente invitado
4. Haga clic en el enlace **Usuario** para editar la cuenta de Usuario subyacente
5. Cambie el **nombre de usuario** de `guest_10374` a la dirección de correo electrónico real del cliente
6. Cambie el **correo electrónico** para coincidir
7. Agregue opcionalmente el **nombre** y **apellido**
8. Marque **Enviar correo de restablecimiento de contraseña** para que el cliente establezca una contraseña
9. Haga clic en **Guardar**

El cliente ahora puede iniciar sesión con su dirección de correo electrónico y verá sus pedidos anteriores como cliente invitado en su historial de pedidos.

### ¿Por Qué Convertir a Clientes Invitados?

- Los pedidos de invitados no cuentan hacia el análisis o segmentación de clientes
- Los invitados no pueden rastrear pedidos ni acceder al historial de pedidos
- Convertir invitados aumenta la cantidad de clientes registrados y mejora la precisión del análisis
- Los clientes registrados son más propensos a realizar compras repetidas

## Desactivar vs Eliminar Cuentas

### Desactivar una Cuenta de Cliente

La desactivación impide el inicio de sesión mientras se preserva todos los datos:

1. Abra el perfil del cliente
2. Haga clic en el enlace **Usuario** para editar la cuenta de Usuario
3. **Desmarque "Activo"**
4. Haga clic en **Guardar**

**¿Qué ocurre:**
- El cliente no puede iniciar sesión
- El historial de pedidos se preserva
- El cliente puede reactivarse más tarde marcando "Activo" nuevamente
- Los análisis y métricas permanecen intactos

**Use la desactivación para:**
- Suspender temporalmente cuentas debido a disputas de pago
- Bloquear clientes abusivos
- Clientes que solicitaron dejar de recibir acceso pero no eliminar los datos

### Eliminar una Cuenta de Cliente

La eliminación elimina la cuenta y puede dejar el historial de pedidos sin vincular:

1. Abra el perfil del cliente
2. Desplácese hasta el final y haga clic en **Eliminar**
3. Confirme la eliminación

**¿Qué ocurre:**
- La cuenta del cliente se elimina permanentemente
- El perfil del cliente se elimina
- El historial de pedidos puede quedar sin vincular (los pedidos existen pero no están vinculados a un cliente)
- No se puede deshacer

**Use la eliminación para:**
- Solicitudes de eliminación de datos GDPR/CCPA (exporte los datos primero)
- Cuentas de prueba que nunca deberían haber existido
- Cuentas duplicadas creadas por error

### Cumplimiento con GDPR

Antes de eliminar una cuenta de cliente en respuesta a una solicitud GDPR:

1. Navegue hasta **Clientes > Todos los Clientes**
2. Seleccione al cliente
3. Use la acción **Exportar Datos** para generar una exportación completa de datos
4. Envíe la exportación al cliente si lo solicitó
5. Luego proceda con la eliminación

La exportación incluye: perfil del cliente, historial de pedidos, direcciones, notas y datos de análisis.

## Consejos

- **Use filtros para identificar clientes de alto valor** — Filtre por Valor del Cliente para encontrar sus Campeones y VIP
- **Revise las notas de clientes regularmente** — Revise al menos semanalmente las tareas de seguimiento pendientes
- **No edite manualmente los análisis** — Deje que el sistema calcule las puntuaciones RFM y los segmentos automáticamente
- **Convierta a invitados proactivamente** — Después de que un invitado realice una segunda compra, contacte y ofrezca crear una cuenta adecuada
- **Use la desactivación en lugar de la eliminación** — La desactivación preserva los datos y puede revertirse si es necesario
- **Añada notas durante las llamadas de soporte** — Documente las interacciones de soporte para que otros miembros del equipo tengan contexto
- **Establezca fechas de seguimiento** — Use el sistema de tareas de seguimiento en las notas para asegurarse de que nada se pierda
- **Respete las preferencias de comunicación** — Nunca envíe correos de marketing a clientes que hayan optado por no recibirlos

Recuerde: Devuelva SOLO el objeto JSON con los campos "title" y "content". Preserve todo el formato markdown, rutas de imágenes, bloques de código y términos técnicos exactamente como se muestran arriba.