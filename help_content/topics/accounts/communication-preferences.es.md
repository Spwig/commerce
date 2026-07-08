---
title: Preferencias de Comunicación
---

Las preferencias de comunicación permiten a los clientes controlar qué correos electrónicos y mensajes de SMS reciben de su tienda. Este sistema garantiza la conformidad con el GDPR y le ayuda a respetar las preferencias de comunicación del cliente en todos los canales.

Navegue a **Clientes > Preferencias de Comunicación** en el menú lateral de administración para administrar las preferencias de comunicación del cliente.

## Entendiendo las Preferencias de Comunicación

El sistema de preferencias de comunicación le da a los clientes un control detallado sobre los mensajes que reciben. Esto incluye:

- **Correos electrónicos transaccionales** — Confirmaciones esenciales de pedidos, actualizaciones de envío, correos de seguridad de la cuenta (siempre activado)
- **Correos electrónicos de marketing** — Boletines, promociones, recomendaciones de productos (requiere opt-in)
- **Notificaciones específicas de la aplicación** — Posts de blog, puntos de lealtad, recompensas de referidos, comisiones de afiliados
- **Notificaciones por SMS** — Notificaciones por mensaje de texto (requiere opt-in explícito según TCPA)

Todas las comunicaciones de marketing requieren el consentimiento del cliente y la verificación del correo electrónico para garantizar la conformidad con el GDPR.

## Explicación de Tipos de Preferencias

### Comunicaciones Transaccionales (Siempre Activadas)

Las comunicaciones transaccionales son esenciales para la cuenta y pedidos de sus clientes. Estas **no pueden desactivarse** por los clientes:

| Tipo | Descripción | Ejemplos |
|------|-------------|----------|
| **Confirmación de Pedido** | Confirmación cuando se coloca el pedido | El pedido #12345 ha sido recibido |
| **Actualizaciones de Envío** | Notificaciones cuando cambia el estado del pedido | Su pedido ha sido enviado |
| **Confirmación de Pago** | Pago recibido, reembolso procesado | Pago de $49.99 confirmado |
| **Seguridad de la Cuenta** | Restablecimiento de contraseña, verificación de correo electrónico | Restablezca su contraseña |

### Comunicaciones de Marketing (Requiere Opt-In)

Las comunicaciones de marketing requieren el consentimiento del cliente y la verificación del correo electrónico:

| Tipo | Descripción | Valor por Defecto |
|------|-------------|---------|
| **Boletín Informativo** | Boletines generales y actualizaciones | Opt-out |
| **Ofertas Promocionales** | Ventas, descuentos, ofertas especiales | Opt-out |
| **Recomendaciones de Productos** | Sugerencias personalizadas de productos | Opt-out |
| **Vuelta al Stock** | Notificaciones cuando los productos regresan | Opt-out |

Los clientes deben **verificar su dirección de correo electrónico** antes de recibir cualquier correo electrónico de marketing (requisito de doble opt-in del GDPR).

### Preferencias Específicas de la Aplicación

Los clientes pueden controlar las notificaciones de características específicas:

**Notificaciones del Blog**
- Nuevo post publicado (inmediato, resumen semanal o mensual)
- Suscripciones específicas de categorías
- Preferencias de frecuencia

**Programa de Lealtad**
- Notificaciones de puntos ganados
- Actualizaciones de nivel
- Recompensas desbloqueadas
- Puntos próximos a expirar
- Bonos de cumpleaños
- Ofertas de campaña

**Programa de Referidos**
- Recompensa emitida (referidor y referido)
- Registro exitoso de referido
- Recompensa próxima a expirar
- Invitaciones de referidos

**Programa de Afiliados**
- Comisión ganada
- Comisión aprobada o rechazada
- Pago procesado, completado o fallido
- Informes mensuales de rendimiento

### Notificaciones por SMS (Requiere Opt-In Explícito)

Todas las notificaciones por SMS requieren **opt-in explícito** según las regulaciones TCPA. Los clientes deben activamente marcar la casilla de opt-in para SMS:

- **SMS Transaccionales** — Pedido enviado, entregado (requiere opt-in)
- **SMS de Marketing** — Promociones, ofertas especiales (requiere opt-in separado)

Incluso los SMS transaccionales requieren opt-in porque enviar mensajes de texto no solicitados está regulado más estrictamente que el correo electrónico.

## Administración de Preferencias del Cliente en el Panel de Control

### Ver todas las Preferencias

Navegue a **Clientes > Preferencias de Comunicación** para ver todas las preferencias del cliente:

| Columna | Descripción |
|--------|-------------|
| **Correo Electrónico del Usuario** | Dirección de correo electrónico del cliente (enlace al panel de control del usuario) |
| **Estado del Correo Electrónico** | ✓ verde si el correo electrónico está activado, ○ gris si está desactivado |
| **Estado del SMS** | ✓ verde si el SMS está activado, ○ gris si está desactivado |
| **Estado del Marketing** | Etiqueta "Opted In" o "Opted Out" |
| **Estado de Verificación** | 📧✓ si el correo electrónico está verificado, 📱✓ si el SMS está verificado |
| **Fuente del Consentimiento** | Dónde el cliente dio su consentimiento (registro, pago, centro de preferencias) |
| **Actualizado en** | Última vez que se cambió una preferencia |

### Filtros de Preferencias

Use el panel lateral de filtros para encontrar clientes:

- **Correo Electrónico Activado** — Sí/No
- **SMS Activado** — Sí/No
- **Marketing por Correo Electrónico** — Sí/No (opt-in para marketing)
- **Marketing por SMS** — Sí/No (opt-in para marketing por SMS)
- **Correo Electrónico Verificado** — Sí/No (verificado su dirección de correo electrónico)
- **SMS Verificado** — Sí/No (verificado su número de teléfono)
- **Fuente del Consentimiento** — Registro, Pago, Centro de Preferencias, API, Migración
- **Código de Idioma** — Idioma preferido para las comunicaciones

### Búsqueda de Preferencias

Buscar clientes por:
- Correo electrónico del usuario
- Nombre de usuario
- Nombre
- Apellido
- Token de descuento

### Acciones por Lotes

Selecciona múltiples clientes y aplica acciones por lotes:

**✓ Marcar Correo Electrónico como Verificado**
- Verificar manualmente las direcciones de correo electrónico de los clientes
- Útil cuando se importan clientes desde otro sistema
- Invalida la caché de preferencias para aplicar cambios inmediatamente

**🚫 Darse de Baja de Todo el Marketing**
- Desactiva todas las comunicaciones de marketing (correo electrónico, SMS, todas las aplicaciones)
- Mantiene activadas las comunicaciones transaccionales
- Útil para clientes que soliciten darse de baja completamente
- Respeta el derecho del GDPR de retirar el consentimiento

**📥 Exportar Preferencias a CSV**
- Exportar las preferencias de los clientes a una hoja de cálculo
- Incluye todos los campos de preferencia y ajustes específicos de la aplicación
- Útil para auditorías de cumplimiento y análisis
- Formato: CSV con encabezados

## Centro de Preferencias de Auto-Servicio del Cliente

Los clientes pueden administrar sus propias preferencias en `/accounts/preferences/` cuando están conectados.

### Características del Centro de Preferencias

**Acciones Rápidas**
- **Suscribirse a Todo el Marketing** — Habilitar todas las comunicaciones de marketing con un solo clic
- **Darse de Baja de Todo** — Deshabilitar todas las comunicaciones de marketing (comunicaciones transaccionales aún habilitadas)

**Tarjetas de Preferencias**
- **Correos Electrónicos Transaccionales** — Solo lectura (siempre habilitados, marcados como "Requeridos")
- **Comunicaciones de Marketing** — Cambiar el estado de encendido/apagado con un distintivo de verificación
- **Preferencias del Blog** — Habilitar/deshabilitar, seleccionar frecuencia (inmediata, semanal, mensual)
- **Programa de Lealtad** — Habilitar/deshabilitar tipos específicos de notificaciones
- **Programa de Referidos** — Habilitar/deshabilitar notificaciones de recompensas
- **Programa de Afiliados** — Habilitar/deshabilitar notificaciones de comisiones y pagos
- **Notificaciones por SMS** — Optar por recibir o no recibir SMS (muestra el estado de verificación)

**Actualizaciones en Tiempo Real**
- Los cambios se guardan inmediatamente mediante AJAX
- No se requiere recarga de la página
- Feedback visual cuando se guardan los cambios

### Proceso de Verificación del Correo Electrónico

Cuando un cliente habilita correos electrónicos de marketing:

1. El cliente cambia "Correos Electrónicos de Marketing" a ON
2. El sistema envía un correo de verificación con un enlace único
3. El cliente hace clic en el enlace de verificación
4. El correo se marca como verificado (aparece el distintivo 📧✓)
5. Ahora los correos de marketing se enviarán

**Los clientes no verificados NO recibirán correos de marketing** incluso si el interruptor está en ON. Esto garantiza el cumplimiento del doble opt-in del GDPR.

## Darse de Baja con Un Solo Clic

Todos los correos de marketing incluyen un enlace de darse de baja en el pie de página. Al hacer clic en este enlace:

1. Lleva al cliente a `/accounts/unsubscribe/<token>/` (no se requiere iniciar sesión)
2. Muestra de qué se está dándose de baja
3. Permite retroalimentación opcional (razón de la baja)
4. Desactiva las comunicaciones de marketing
5. Mantiene activas las comunicaciones transaccionales
6. Proporciona un enlace al centro de preferencias completo

Los clientes pueden suscribirse nuevamente en cualquier momento a través del centro de preferencias.

## Cumplimiento y Requisitos Legales

### Cumplimiento con el Artículo 7 del GDPR

El sistema garantiza el cumplimiento completo con el Artículo 7 del GDPR:

**✅ Prueba del Consentimiento**
- Marca temporal cuando se dio el consentimiento
- Fuente del consentimiento (registro, pago, centro de preferencias)
- Dirección IP del consentimiento
- User agent (información del navegador)

**✅ Consentimiento Separado**
- Los correos electrónicos de marketing y transaccionales son interruptores separados
- Cada aplicación (blog, lealtad, etc.) requiere consentimiento individual

**✅ Retirada Fácil**
- Darse de baja con un solo clic en todos los correos de marketing
- Centro de preferencias disponible para todos los clientes conectados
- La baja toma efecto inmediatamente

**✅ Consentimiento Dado Libremente**
- El estado por defecto es opt-out para el marketing (mejor práctica del GDPR)
- No hay casillas preseleccionadas (los clientes deben optar activamente)

**✅ Consentimiento Específico e Informado**
- Descripciones claras de lo que cada preferencia controla
- Preferencias detalladas a nivel de aplicación (no todo o nada)

**✅ Consentimiento Verificable**
- Doble opt-in para correos electrónicos de marketing
- Rastro de auditoría a través del estado de seguimiento de EmailOutbox

### Cumplimiento con TCPA (Regulaciones de SMS en EE. UU.)

Todas las notificaciones por SMS requieren **opt-in explícito**:

- Los clientes deben activamente marcar la casilla de opt-in para SMS
- No se permiten casillas preseleccionadas
- Descripción clara de lo que están optando
- Darse de baja fácil a través del centro de preferencias
- Todos los envíos de SMS se registran para auditoría de cumplimiento

### Cumplimiento con CAN-SPAM (Regulaciones de Correo Electrónico en EE. UU.)

El sistema garantiza el cumplimiento con CAN-SPAM:

- Enlace de darse de baja en cada correo electrónico de marketing
- Procesar la darse de baja inmediatamente (se requiere dentro de 10 días hábiles, lo hacemos instantáneamente)
- Nombre claro en "From" (nombre de su tienda)
- Dirección física en el pie de página del correo electrónico
- No hay asuntos engañosos

## Entendiendo el Estado del Correo Electrónico en EmailOutbox

Cuando ve **Sistema de Correo Electrónico > Email Outbox**, verá cómo las preferencias afectan la entrega del correo:

| Estado | Significado | Razón |
|--------|---------|--------|
| **Pendiente** | Correo encolado para enviar | Las preferencias permiten este correo |
| **En cola** | En la cola de envío | Las preferencias permiten este correo |
| **Saltado** | Correo no enviado | Preferencia del cliente desactivada |
| **Enviado** | Entregado con éxito | Correo enviado normalmente |

Cuando un correo está **saltado**, el campo `skip_reason` muestra por qué:

- **user_preference_disabled** — El cliente desactivó este tipo de correo en las preferencias
- **email_not_verified** — El cliente no ha verificado su dirección de correo electrónico
- **email_disabled** — El cliente desactivó todos los correos (interruptor principal)

Este rastro de auditoría es importante para el cumplimiento del GDPR — puede probar que honró las preferencias del cliente.

## Configuración del Sitio para Preferencias

Navegue a **Configuración > Configuración del Sitio** para configurar los valores predeterminados globales de las preferencias:

**Habilitar Doble Opt-In para Correos Electrónicos de Marketing** (Predeterminado: Sí)
- Requiere verificación del correo electrónico antes de enviar correos de marketing
- Mejor práctica del GDPR
- Recomendado: Dejarlo habilitado

**Estado Predeterminado de Opt-In de Marketing** (Predeterminado: No - Opt-Out)
- Estado predeterminado cuando los nuevos clientes se registran
- El GDPR requiere opt-out por defecto
- Recomendado: Dejarlo como opt-out (Falso)

**Centro de Preferencias Habilitado** (Predeterminado: Sí)
- Permite a los clientes gestionar sus propias preferencias
- Requerido para el derecho del GDPR de retirar el consentimiento
- Recomendado: Dejarlo habilitado

**Requerir Verificación de SMS** (Predeterminado: No)
- Requerir verificación del número de teléfono para notificaciones de SMS
- Opcional pero recomendado para remitentes de SMS de alto volumen
- Puede habilitarse si desea doble opt-in para SMS

**Mostrar Razones de Darse de Baja** (Predeterminado: Sí)
- Recopilar retroalimentación opcional cuando los clientes se den de baja
- Ayuda a entender por qué los clientes se están dándose de baja
- Recomendado: Dejarlo habilitado para obtener información

## Mejores Prácticas

### 1. Por Defecto, Opt-Out para Marketing

Siempre configure las comunicaciones de marketing para **opt-out** (no marcado):
- Cumple con el GDPR
- Construye confianza con los clientes
- Reduce las quejas por spam
- Solo envíe a clientes interesados

### 2. Requerir Verificación del Correo Electrónico

Mantenga **Doble Opt-In** habilitado:
- Garantiza que las direcciones de correo electrónico sean válidas
- Confirma que el cliente realmente quiere recibir correos de marketing
- Reduce la tasa de rebote
- Requerido para el cumplimiento del GDPR

### 3. Respetar Preferencias Inmediatamente

Cuando un cliente cambia sus preferencias:
- Los cambios toman efecto inmediatamente
- Se invalida la caché de preferencias
- El siguiente envío de correo verificará las preferencias actualizadas
- No hay retraso en el procesamiento de las solicitudes de darse de baja

### 4. Supervisar Correos Saltados

Revise regularmente el **Email Outbox** para correos saltados:
- Una alta tasa de salto indica que los clientes se están dándose de baja
- Puede señalar que el contenido del correo necesita mejora
- Ayuda a identificar problemas de preferencia

### 5. Auditorías de Cumplimiento Periódicas

Exportar preferencias periódicamente para cumplimiento:
1. Navegue a **Preferencias de Comunicación**
2. Seleccione todos los clientes
3. Elija **Exportar Preferencias a CSV**
4. Guarde para el rastro de auditoría del GDPR

Almacene las exportaciones durante **al menos 3 años** para cumplir con los requisitos de retención de datos del GDPR.

### 6. Comunicación Clara

Cuando se recolecta el consentimiento:
- Use lenguaje claro, no jerga legal
- Explique qué recibirán los clientes
- Muestre la frecuencia (diario, semanal, mensual)
- Haga prominentes las casillas de opt-in pero no preseleccionadas

### 7. Segmentar por Preferencia

Cuando se envían campañas de marketing:
- Solo envíe a clientes verificados y optados en
- Respete las preferencias específicas de la aplicación (no envíe correos de blog a clientes que deshabilitaron el blog)
- Use preferencias de frecuencia (no envíe correos inmediatos a suscriptores de resumen semanal)

## Consejos

**💡 Verificar Preferencias Antes de Enviar**

El sistema verifica automáticamente las preferencias cuando envía correos usando `EmailSendingService.send_template_email()`. Asegúrese de que todos los envíos de correo usen este servicio, no llamadas directas a SMTP.

**💡 El Estado de Salto es Normal**

No se preocupe por los correos saltados en el outbox — esto significa que el sistema está funcionando correctamente y respetando las preferencias del cliente. Es mejor saltar correos no deseados que correr el riesgo de multas del GDPR o quejas por spam.

**💡 La Caché de Preferencias es de 5 Minutos**

Las verificaciones de preferencias se almacenan en caché durante 5 minutos para el rendimiento. Cuando los clientes cambian las preferencias a través del centro de preferencias o acciones del administrador, la caché se invalida inmediatamente para que los cambios tengan efecto de inmediato.

**💡 Los Clientes Invitados Bypassan las Verificaciones**

Los clientes de pago invitado (sin cuenta) recibirán todos los correos normalmente porque no tienen registro de preferencias. Esto es intencional — optaron por recibirlos al proporcionar su correo electrónico en el pago.

**💡 Los Correos Electrónicos Transaccionales Siempre Se Envían**

Las confirmaciones de pedidos, actualizaciones de envío y correos de seguridad de la cuenta **siempre se envían** independientemente de las preferencias. Esto asegura que los clientes reciban información crítica sobre sus pedidos y cuentas.

**💡 Use Acciones por Lotes con Cuidado**

La acción por lotes "Darse de Baja de Todo el Marketing" afecta **todas las aplicaciones** (blog, lealtad, referidos, afiliados). Solo úsela para clientes que solicitaron específicamente darse de baja completamente. Para preferencias específicas, edite los registros de clientes individuales.

**💡 Rastro de Auditoría para Cumplimiento**

El sistema rastrea:
- Marca temporal y fuente del consentimiento
- Dirección IP y user agent
- Marca temporal de verificación del correo electrónico
- Cada cambio de preferencia a través del estado de salto de EmailOutbox

Este rastro de auditoría prueba el cumplimiento del GDPR si las autoridades solicitan evidencia del consentimiento.