---
title: Preferencias de comunicación
---

Las preferencias de comunicación permiten a los clientes controlar qué correos electrónicos y mensajes SMS reciben de su tienda. Este sistema garantiza el cumplimiento del RGPD y le ayuda a respetar las preferencias de comunicación de los clientes en todos los canales.

Vaya a **Clientes > Preferencias de comunicación** en la barra lateral de administración para gestionar las preferencias de comunicación de los clientes.

## Comprensión de las preferencias de comunicación

El sistema de preferencias de comunicación otorga a los clientes un control detallado sobre los mensajes que reciben. Esto incluye:

- **Correos transaccionales** — Confirmaciones esenciales de pedidos, actualizaciones de envío, correos de seguridad de la cuenta (siempre activados)
- **Correos de marketing** — Boletines, promociones, recomendaciones de productos (requiere aceptación previa)
- **Notificaciones específicas de la aplicación** — Publicaciones de blog, puntos de fidelidad, recompensas por referidos, comisiones de afiliados
- **Notificaciones SMS** — Notificaciones por mensaje de texto (requiere aceptación explícita según TCPA)

Todas las comunicaciones de marketing requieren el consentimiento del cliente y la verificación del correo electrónico para garantizar el cumplimiento del RGPD.

## Tipos de preferencias explicados

### Comunicaciones transaccionales (Siempre activadas)

Los mensajes transaccionales son esenciales para la cuenta y los pedidos de su cliente. Estos **no pueden desactivarse** por parte de los clientes:

| Tipo | Descripción | Ejemplos |
|------|-------------|----------|
| **Confirmaciones de pedido** | Confirmación cuando se realiza un pedido | Se ha recibido el pedido #12345 |
| **Actualizaciones de envío** | Notificaciones cuando cambia el estado del pedido | Su pedido ha sido enviado |
| **Confirmaciones de pago** | Pago recibido, reembolso procesado | Pago de $49.99 confirmado |
| **Seguridad de la cuenta** | Restablecimiento de contraseña, verificación de correo electrónico | Restablezca su contraseña |

### Comunicaciones de marketing (Requiere aceptación previa)

Los mensajes de marketing requieren el consentimiento del cliente y la verificación del correo electrónico:

| Tipo | Descripción | Predeterminado |
|------|-------------|---------|
| **Boletín** | Boletines y actualizaciones generales | Rechazo previo |
| **Ofertas promocionales** | Ventas, descuentos, ofertas especiales | Rechazo previo |
| **Recomendaciones de productos** | Sugerencias personalizadas de productos | Rechazo previo |
| **De vuelta en stock** | Notificaciones cuando los productos vuelven | Rechazo previo |

Los clientes deben **verificar su dirección de correo electrónico** antes de recibir cualquier correo de marketing (requisito de doble aceptación del RGPD).

### Preferencias específicas de la aplicación

Los clientes pueden controlar las notificaciones de funciones específicas:

**Notificaciones de blog**
- Nueva publicación de blog publicada (inmediata, resumen semanal o resumen mensual)
- Suscripciones específicas por categoría
- Preferencias de frecuencia

**Programa de fidelidad**
- Notificaciones de puntos ganados
- Mejoras de nivel
- Recompensas desbloqueadas
- Puntos por vencer pronto
- Bonificaciones de cumpleaños
- Ofertas de campañas

**Programa de referidos**
- Recompensa emitida (referente y referido)
- Registro exitoso de referido
- Recompensa por vencer pronto
- Invitaciones de referidos

**Programa de afiliados**
- Comisión ganada
- Comisión aprobada o rechazada
- Pago procesado, completado o fallido
- Informes de rendimiento mensuales

### Notificaciones SMS (Requiere aceptación explícita)

Todas las notificaciones SMS requieren **aceptación explícita** según las regulaciones TCPA. Los clientes deben marcar activamente la casilla de aceptación de SMS:

- **SMS transaccional** — Pedido enviado, entregado (requiere aceptación previa)
- **SMS de marketing** — Promociones, ofertas especiales (requiere aceptación previa separada)

Incluso los SMS transaccionales requieren aceptación previa porque el envío de mensajes de texto no solicitados está regulado de manera más estricta que el correo electrónico.

## Gestión de preferencias de clientes en la administración

### Visualización de todas las preferencias

Vaya a **Clientes > Preferencias de comunicación** para ver todas las preferencias de los clientes:

| Columna | Descripción |
|--------|-------------|
| **Correo del usuario** | Dirección de correo del cliente (enlaza al admin de usuarios) |
| **Estado del correo** | Verde ✓ si los correos están habilitados, gris ○ si están deshabilitados |
| **Estado de SMS** | Verde ✓ si los SMS están habilitados, gris ○ si están deshabilitados |
| **Estado de marketing** | Insignia de "Optó por participar" o "Optó por no participar" |
| **Estado de verificación** | 📧✓ si el correo está verificado, 📱✓ si el SMS está verificado |
| **Origen del consentimiento** | Dónde el cliente dio su consentimiento (registro, pago, centro de preferencias) |
| **Actualizado el** | Última vez que se cambiaron las preferencias |

### Filtrar preferencias

Use la barra lateral de filtros para encontrar clientes:

- **Correo habilitado** — Sí/No
- **SMS habilitado** — Sí/No
- **Marketing por correo** — Sí/No (optó por participar en marketing)
- **Marketing por SMS** — Sí/No (optó por participar en marketing por SMS)
- **Correo verificado** — Sí/No (verificó su dirección de correo)
- **SMS verificado** — Sí/No (verificó su número de teléfono)
- **Origen del consentimiento** — Registro, Pago, Centro de preferencias, API, Migración
- **Código de idioma** — Idioma preferido para las comunicaciones

### Buscar preferencias

Busque clientes por:
- Correo del usuario
- Nombre de usuario
- Nombre
- Apellido
- Token de baja

### Acciones masivas

Seleccione varios clientes y aplique acciones masivas:

**✓ Marcar correo como verificado**
- Verifique manualmente las direcciones de correo de los clientes
- Útil al importar clientes desde otro sistema
- Invalida la caché de preferencias para aplicar los cambios de inmediato

**🚫 Dar de baja de todo el marketing**
- Deshabilita todas las comunicaciones de marketing (correo, SMS, todas las aplicaciones)
- Mantiene habilitados los correos transaccionales
- Use esto para clientes que solicitan darse de baja por completo
- Respeta el derecho del RGPD a retirar el consentimiento

**📥 Exportar preferencias a CSV**
- Exporte las preferencias de los clientes a una hoja de cálculo
- Incluye todos los campos de preferencias y configuraciones específicas de la aplicación
- Útil para auditorías de cumplimiento y análisis
- Formato: CSV con encabezados

## Centro de preferencias de autoservicio para clientes

Los clientes pueden gestionar sus propias preferencias en `/accounts/preferences/` cuando están iniciados en la sesión.

### Funciones del centro de preferencias

**Acciones rápidas**
- **Suscribirse a todo el marketing** — Habilite todas las comunicaciones de marketing con un solo clic
- **Darse de baja de todo** — Deshabilite todas las comunicaciones de marketing (los transaccionales siguen habilitados)

**Tarjetas de preferencias**
- **Correos transaccionales** — Solo lectura (siempre habilitados, marcados como "Obligatorio")
- **Comunicaciones de marketing** — Activar/desactivar con insignia de verificación
- **Preferencias del blog** — Habilitar/deshabilitar, seleccionar frecuencia (inmediata, semanal, mensual)
- **Programa de lealtad** — Habilitar/deshabilitar tipos de notificación individuales
- **Programa de referidos** — Habilitar/deshabilitar notificaciones de recompensas
- **Programa de afiliados** — Habilitar/deshabilitar notificaciones de comisiones y pagos
- **Notificaciones por SMS** — Optar por participar o no en SMS (muestra el estado de verificación)

**Actualizaciones en tiempo real**
- Los cambios se guardan de inmediato mediante AJAX
- No se requiere recargar la página
- Retroalimentación visual al guardar

### Proceso de verificación de correo

Cuando un cliente habilita los correos de marketing:

1. El cliente activa "Correos de marketing" a ON
2. El sistema envía un correo de verificación con un enlace único
3. El cliente hace clic en el enlace de verificación
4. El correo se marca como verificado (aparece la insignia 📧✓)
5. Ahora se enviarán correos de marketing

**Los clientes no verificados NO recibirán correos de marketing** incluso si el interruptor está en ON. Esto garantiza el cumplimiento del doble opt-in del RGPD.

## Baja con un solo clic

Todos los correos de marketing incluyen un enlace de baja en el pie de página. Al hacer clic en este enlace:

1. Lleva al cliente a `/accounts/unsubscribe/<token>/` (no se requiere inicio de sesión)
2. Muestra de qué se está dando de baja
3. Permite retroalimentación opcional (motivo de la baja)
4. Deshabilita las comunicaciones de marketing
5. Mantiene habilitados los correos transaccionales
6. Proporciona un enlace al centro de preferencias completo

Los clientes pueden volver a suscribirse en cualquier momento a través del centro de preferencias.

## Cumplimiento y requisitos legales

### Cumplimiento del Artículo 7 del RGPD

El sistema garantiza el cumplimiento completo del Artículo 7 del RGPD:


**✅ Prueba del Consentimiento**
- Marca de tiempo cuando se otorgó el consentimiento
- Origen del consentimiento (registro, pago, centro de preferencias)
- Dirección IP del consentimiento
- Agente de usuario (información del navegador)

**✅ Consentimiento Separado**
- Los correos electrónicos de marketing y transaccionales son interruptores separados
- Cada aplicación (blog, lealtad, etc.) requiere consentimiento individual

**✅ Retiro Fácil**
- Cancelación de suscripción con un clic en todos los correos de marketing
- Centro de preferencias disponible para todos los clientes iniciados
- La cancelación de suscripción tiene efecto inmediato

**✅ Consentimiento Libremente Otorgado**
- El valor predeterminado es no suscrito para marketing (mejor práctica de GDPR)
- Sin casillas premarcadas (los clientes deben suscribirse activamente)

**✅ Consentimiento Específico e Informado**
- Descripciones claras de lo que controla cada preferencia
- Preferencias a nivel de aplicación granulares (no todo o nada)

**✅ Consentimiento Verificable**
- Doble suscripción para correos electrónicos de marketing
- Rastro de auditoría mediante el seguimiento del estado de EmailOutbox

### Cumplimiento de TCPA (Regulaciones de SMS de EE. UU.)

Todas las notificaciones por SMS requieren **opt-in explícito**:

- Los clientes deben marcar activamente la casilla de opt-in de SMS
- No se permiten casillas premarcadas
- Descripción clara de lo en lo que se están suscribiendo
- Cancelación fácil a través del centro de preferencias
- Todos los envíos de SMS se registran para la auditoría de cumplimiento

### Cumplimiento de CAN-SPAM (Regulaciones de Correo Electrónico de EE. UU.)

El sistema garantiza el cumplimiento de CAN-SPAM:

- Enlace de cancelación de suscripción en cada correo de marketing
- La cancelación de suscripción se procesa inmediatamente (se requieren 10 días hábiles, lo hacemos al instante)
- Nombre "De" claro (el nombre de su tienda)
- Dirección física en el pie del correo
- Sin líneas de asunto engañosas

## Comprensión del Estado del Correo en EmailOutbox

Al ver **Sistema de Correo > Bandeja de Salida**, verá cómo las preferencias afectan la entrega de correos:

| Estado | Significado | Razón |
|--------|---------|--------|
| **Pendiente** | Correo en cola para envío | Las preferencias permiten este correo |
| **En cola** | En la cola de envío | Las preferencias permiten este correo |
| **Omitido** | Correo no enviado | Preferencia del cliente deshabilitada |
| **Enviado** | Entregado con éxito | Correo enviado normalmente |

Cuando un correo es **omitido**, el campo `skip_reason` muestra la razón:

- **user_preference_disabled** — El cliente deshabilitó este tipo de correo en las preferencias
- **email_not_verified** — El cliente no ha verificado su dirección de correo electrónico
- **email_disabled** — El cliente deshabilitó todos los correos (interruptor maestro)

Este rastro de auditoría es importante para el cumplimiento de GDPR — puede demostrar que respetó las preferencias de los clientes.

## Configuración del Sitio para Preferencias

Navegue a **Configuración > Configuración del Sitio** para configurar los valores predeterminados globales de preferencias:

**Habilitar Doble Suscripción para Correos de Marketing** (Predeterminado: Sí)
- Requiere verificación de correo antes de enviar correos de marketing
- Mejor práctica de GDPR
- Recomendado: Dejar habilitado

**Estado Predeterminado de Suscripción a Marketing** (Predeterminado: No - No suscrito)
- Estado predeterminado cuando se registran nuevos clientes
- GDPR requiere no suscrito por defecto
- Recomendado: Dejar como no suscrito (False)

**Centro de Preferencias Habilitado** (Predeterminado: Sí)
- Permite a los clientes gestionar sus propias preferencias
- Requerido para el derecho de GDPR a retirar el consentimiento
- Recomendado: Dejar habilitado

**Requerir Verificación de SMS** (Predeterminado: No)
- Requiere verificación del número de teléfono para notificaciones por SMS
- Opcional pero recomendado para remitentes de SMS de alto volumen
- Se puede habilitar si desea doble suscripción para SMS

**Mostrar Razones de Cancelación de Suscripción** (Predeterminado: Sí)
- Recopilar comentarios opcionales cuando los clientes cancelan la suscripción
- Ayuda a entender por qué los clientes se están desuscribiendo
- Recomendado: Dejar habilitado para obtener información

## Mejores Prácticas

### 1. Predeterminar a No Suscrito para Marketing

Siempre predetermine las comunicaciones de marketing a **no suscrito** (desmarcado):
- Cumple con GDPR
- Genera confianza con los clientes
- Reduce las quejas de spam
- Solo enviar a clientes comprometidos

### 2. Requerir Verificación de Correo

Mantener **Doble Suscripción** habilitada:
- Asegura que las direcciones de correo sean válidas
- Confirma que el cliente realmente desea correos de marketing
- Reduce la tasa de rebote
- Requerido para el cumplimiento de GDPR

### 3. Respetar las Preferencias Inmediatamente



Cuando un cliente cambia sus preferencias:
- Los cambios surten efecto inmediatamente
- La caché de preferencias se invalida
- El próximo envío de correos electrónicos revisará las preferencias actualizadas
- No hay demora en cumplir con las solicitudes de cancelación de suscripción

### 4. Supervisar correos electrónicos omitidos

Revisar con regularidad **Buzón de correos salientes** en busca de correos electrónicos omitidos:
- Un alto porcentaje de omisiones indica que los clientes se están optando out
- Puede indicar que el contenido del correo electrónico necesita mejorarse
- Ayuda a identificar problemas de preferencia

### 5. Revisiones de cumplimiento periódicas

Exportar las preferencias periódicamente para cumplir con los requisitos de cumplimiento:
1. Navegar a **Preferencias de comunicación**
2. Seleccionar a todos los clientes
3. Elegir **Exportar preferencias a CSV**
4. Guardar para el registro de auditoría de GDPR

Almacenar las exportaciones durante **al menos 3 años** para cumplir con los requisitos de retención de datos de GDPR.

### 6. Comunicación clara

Al recopilar el consentimiento:
- Usar lenguaje claro, no jerga legal
- Explicar qué recibirán los clientes
- Mostrar la frecuencia (diaria, semanal, mensual)
- Hacer que las casillas de opt-in sean visibles pero no marcadas de forma predeterminada

### 7. Segmentar por preferencia

Al enviar campañas de marketing:
- Enviar solo a clientes verificados y con opt-in
- Respetar las preferencias específicas de la aplicación (no enviar correos electrónicos de blog a clientes que desactivaron el blog)
- Usar las preferencias de frecuencia (no enviar correos electrónicos inmediatos a suscriptores de resumen semanal)

## Consejos

**💡 Verificar las preferencias antes de enviar**

El sistema comprueba automáticamente las preferencias cuando envía correos electrónicos usando `EmailSendingService.send_template_email()`. Asegúrese de que todos los envíos de correos electrónicos usen este servicio, en lugar de llamadas directas a SMTP.

**💡 El estado de omisión es normal**

No se alarme por los correos electrónicos omitidos en el buzón: esto significa que el sistema funciona correctamente y respeta las preferencias de los clientes. Es mejor omitir correos electrónicos no deseados que arriesgarse a multas por GDPR o quejas de spam.

**💡 La caché de preferencias tiene 5 minutos**

Las comprobaciones de preferencias se almacenan en caché durante 5 minutos para rendimiento. Cuando los clientes cambian sus preferencias a través del centro de preferencias o acciones de administración, la caché se invalida inmediatamente para que los cambios surtan efecto de inmediato.

**💡 Los clientes invitados evitan las comprobaciones**

Los clientes que compran como invitado (sin cuenta) recibirán todos los correos electrónicos normalmente, ya que no tienen registro de preferencias. Esto es intencional: optaron por suscribirse al proporcionar su correo electrónico durante el pago.

**💡 Los correos electrónicos transaccionales siempre se envían**

Los correos electrónicos de confirmación de pedido, actualizaciones de envío y correos electrónicos de seguridad de la cuenta **siempre se envían**, independientemente de las preferencias. Esto garantiza que los clientes reciban información crítica sobre sus pedidos y cuentas.

**💡 Usar con cuidado las acciones en masa**

La acción de "Darse de baja de todos los correos electrónicos de marketing" afecta a **todos los aplicaciones** (blog, lealtad, referidos, afiliados). Úsela solo para clientes que solicitaron explícitamente darse de baja completamente. Para preferencias específicas, edite los registros individuales de los clientes.

**💡 Registro de auditoría para cumplimiento**

El sistema registra:
- La hora y el origen del consentimiento
- La dirección IP y el agente de usuario
- La hora de verificación del correo electrónico
- Todos los cambios de preferencia a través del estado de omisión de EmailOutbox

Este registro de auditoría demuestra el cumplimiento de GDPR si las autoridades solicitan evidencia de consentimiento.

## Temas relacionados

- [Gestión de cuentas de clientes](/help/managing-customer-accounts) — Gestión del perfil del cliente
- [Configuración de correo electrónico](/help/email-configuration) — Configuración de SMTP y plantillas de correo electrónico