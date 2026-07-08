---
title: Gestion de solicitudes de afiliados
---

Cuando posibles socios solicitan unirse a su programa de afiliados, aparecen en su cola de solicitudes esperando revisión. Esta guía le muestra cómo evaluar, aprobar y rechazar solicitudes de afiliados para construir una red de socios de calidad que se alineen con su marca.

Gestionar las solicitudes con cuidado asegura que trabaje con afiliados confiables que representarán profesionalmente su tienda y generarán ventas reales.

![Vista de lista de solicitudes](/static/core/admin/img/help/managing-affiliate-applications/applications-list.webp)

## Fuentes de solicitudes

Las solicitudes de afiliados llegan a su cola a través de varios canales:

### Aplicaciones del portal público

La mayoría de las solicitudes provienen del portal de afiliados público en `/affiliate/` de su tienda. Cuando los posibles afiliados hacen clic en **Convertirse en Afiliado**, completan un formulario de registro que crea un registro de solicitud.

### Invitados vs. usuarios registrados

Si ha habilitado **Permitir registro de invitados** en la configuración de afiliados, los no clientes pueden aplicar directamente. De lo contrario, los usuarios deben crear primero una cuenta de cliente en su tienda antes de poder aplicar para convertirse en afiliados.

### Revisión manual requerida

Cuando **Requerir aprobación** está habilitado en la configuración de afiliados (recomendado), todas las solicitudes entran en un estado **Pendiente** esperando su revisión. Si está deshabilitado, las solicitudes se aprueban automáticamente y los afiliados obtienen acceso inmediato a su panel de control.

## Ver solicitudes

Navegue a **Programa de Afiliados > Solicitudes** (o **Marketing > Miembros de Afiliados** en el administrador) para ver todas las solicitudes del programa.

La vista de lista muestra:

| Columna | Descripción |
|--------|-------------|
| **Afiliado** | El nombre y correo electrónico del solicitante |
| **Programa** | El programa de afiliados al que se están aplicando |
| **Estado** | Pendiente, aprobado o rechazado |
| **Fecha de aplicación** | Cuando presentaron la solicitud |
| **Método de pago** | Su método preferido de pago (PayPal o transferencia bancaria) |

### Filtros de solicitudes

Use los filtros del administrador para reducir las solicitudes:

- **Estado**: Ver solo solicitudes pendientes que requieren revisión
- **Programa**: Filtre por programa específico si tiene múltiples programas de afiliados
- **Rango de fechas**: Encuentre solicitudes de un período de tiempo específico

### Badge de solicitudes pendientes

El panel lateral del administrador muestra un recuento de badge junto a **Afiliados** cuando tiene solicitudes pendientes que requieren acción.

## Revisar una solicitud

Haga clic en cualquier solicitud para ver el perfil completo del solicitante. Esta vista de detalles muestra toda la información que necesita para tomar una decisión de aprobación informada.

![Tarjeta de detalles de la solicitud](/static/core/admin/img/help/managing-affiliate-applications/application-detail-card.webp)

### Información del perfil del afiliado

Revise estos detalles clave sobre el solicitante:

**Información básica**
- **Dirección de correo electrónico**: Se usa para iniciar sesión y comunicación
- **Nombre de la empresa/empresa**: Su organización (si aplica)
- **URL del sitio web**: Su plataforma de promoción principal
- **Número de teléfono**: Información de contacto

**Información de pago**
- **Método de pago**: PayPal o transferencia bancaria
- **Correo electrónico de PayPal**: Requerido si seleccionaron pagos por PayPal
- **Detalles bancarios**: Requerido si seleccionaron transferencia bancaria (número de cuenta, número de ruta, código SWIFT)

**Canales de promoción**
Muchas solicitudes incluyen notas sobre dónde el afiliado planea promocionar sus productos — cuentas de redes sociales, canales de YouTube, listas de correo electrónico o blogs.

### Detalles del programa

Revise a qué programa se aplicaron y revise su tasa de comisión, tiempo de vida de la cookie y umbral de pago mínimo. Asegúrese de que el solicitante sea una buena opción para el público objetivo del programa.

### Historial de solicitudes

Si un solicitante ha sido rechazado anteriormente o ha aplicado a múltiples programas, este historial aparece en la vista de detalles.

## Criterios de aprobación

Use esta lista de verificación para evaluar cada solicitud de forma consistente:

### Legitimidad del negocio

- [ ] **Sitio web o redes sociales activas**: ¿El solicitante tiene una plataforma en vivo con contenido real?
- [ ] **Público relevante**: ¿Su audiencia coincide con su demografía de clientes objetivo?
- [ ] **Contenido de calidad**: ¿Su contenido es profesional, bien escrito y alineado con los valores de su marca?
- [ ] **Plataforma establecida**: ¿Tienen una audiencia comprometida o tráfico significativo?

### Información de pago

- [ ] **Detalles de pago válidos**: ¿Han proporcionado un correo electrónico de PayPal funcional o información completa de cuenta bancaria?
- [ ] **Identidad coincidente**: ¿Los detalles de pago coinciden con su nombre de empresa o información personal?

### Alineación de marca

- [ ] **Ajuste adecuado**: ¿Su contenido, tono y estilo coinciden con la imagen de su marca?
- [ ] **Ningún conflicto**: ¿Ya están promocionando competidores directos?
- [ ] **Estándares profesionales**: ¿Mantienen estándares de calidad con los que se sienta cómodo asociarse?

### Prevención de fraude

- [ ] **Ningún indicador rojo**: Revise señales como direcciones de correo electrónico genéricas, perfiles incompletos o patrones de sitio web sospechosos
- [ ] **Ningún incumplimiento anterior**: ¿Han sido rechazados antes por fraude o incumplimiento de términos?
- [ ] **Expectativas razonables**: ¿Sus planes de promoción declarados son realistas y alcanzables?

Si una solicitud cumple con todos los criterios, apróblela. Si falla en alguna verificación crítica (riesgo de fraude, desalineación de marca, información de pago inválida), rechácela con una razón clara.

## Aprobar solicitudes

Siga estos pasos para aprobar una o más solicitudes:

### Aprobación de una sola solicitud

1. Abra la página de detalles de la solicitud
2. Revise cuidadosamente toda la información del perfil
3. Verifique que los detalles de pago estén completos y válidos
4. Haga clic en el botón **Guardar y continuar editando** si necesita hacer notas
5. Seleccione **Aprobar** en el menú desplegable de estado
6. Haga clic en **Guardar**

### Aprobación en批量

Para múltiples solicitudes calificadas:

1. Navegue a la lista de solicitudes en **Programa de Afiliados > Solicitudes**
2. Marque las casillas junto a las solicitudes que desea aprobar
3. Seleccione **Aprobar las solicitudes seleccionadas** en el menú desplegable **Acciones**
4. Haga clic en **Ir**
5. Confirme la acción en批量 cuando se le solicite

### ¿Qué ocurre después de la aprobación?

Cuando aprueba una solicitud:

- El estado del afiliado cambia a **Aprobado**
- Reciben una notificación por correo electrónico (si se han configurado plantillas de correo electrónico)
- Ganan acceso al panel de control del afiliado para generar enlaces de seguimiento
- Pueden comenzar a promocionar sus productos y ganar comisiones

Los afiliados aprobados aparecen en la lista de afiliados con un estado **Activo** y pueden comenzar inmediatamente a promocionar su programa.

## Rechazar solicitudes

Rechace las solicitudes que no cumplan con sus criterios para proteger su marca y prevenir fraudes.

### ¿Cuándo rechazar?

Razones comunes para rechazar:

- **Sin plataforma activa**: El solicitante no tiene sitio web, blog o presencia en redes sociales
- **Conflictos con competidores**: Principalmente promueven competidores directos
- **Desalineación de marca**: Su estilo de contenido, idioma o valores chocan con su marca
- **Información de pago inválida**: Falta o claramente falsa información de pago
- **Actividad sospechosa**: Correo electrónico genérico, perfil incompleto o indicadores de fraude
- **Incumplimiento de términos**: Afiliado anterior que violó términos del programa

### ¿Cómo rechazar?

1. Abra la página de detalles de la solicitud
2. Revise la información del solicitante para confirmar que el rechazo es apropiado
3. Agregue una nota en el campo **Notas** explicando la razón (solo para referencia interna)
4. Cambie el menú desplegable **Estado** a **Rechazado**
5. Haga clic en **Guardar**

### Después del rechazo

Cuando rechaza una solicitud:

- El estado del afiliado cambia a **Rechazado**
- Pierden el acceso al panel de control del afiliado (si tenían alguno)
- No pueden crear enlaces de seguimiento ni ganar comisiones
- No se envía ninguna notificación automática (puede personalizar esto en plantillas de correo electrónico)

Los afiliados rechazados permanecen en su base de datos para fines de registro. Puede cambiar su estado a **Aprobado** más tarde si las circunstancias cambian.

## Configuración de aprobación automática

Controla si las solicitudes requieren revisión manual en la configuración de su programa de afiliados:

### Revisión manual (recomendado)

Navegue a su programa en **Marketing > Programas de Afiliados** y asegúrese de que **Aprobación automática** esté **desmarcado**. Esta configuración significa:

- Todas las solicitudes comienzan como **Pendientes**
- Usted revisa a cada solicitante antes de que obtengan acceso
- Mejor control de calidad y prevención de fraude
- Más trabajo para usted, pero más seguro para su marca

Use la revisión manual cuando desee evaluar cuidadosamente a los socios, trabajar con influenciadores seleccionados o mantener estándares estrictos de marca.

### Modo de aprobación automática

Marque **Aprobación automática** en la configuración de su programa para aceptar automáticamente todas las solicitudes. Esto significa:

- Las solicitudes saltan el estado pendiente y van directamente a **Aprobado**
- Los afiliados obtienen acceso inmediato a su panel de control
- Menos trabajo para usted, pero mayor riesgo de fraude
- Ideal para programas de referidos abiertos con muchos socios

Use la aprobación automática para programas de referidos generales donde desee maximizar la participación y aceptar algunas variaciones de calidad.

## Acciones en批量

Procese múltiples solicitudes de forma eficiente usando las acciones en批量 de la interfaz de administración:

### Aprobar múltiples solicitudes

1. Navegue a **Programa de Afiliados > Solicitudes**
2. Use filtros para mostrar solo solicitudes **Pendientes**
3. Marque las casillas para todas las solicitudes que desea aprobar
4. Seleccione **Aprobar las solicitudes seleccionadas** en el menú desplegable **Acciones**
5. Haga clic en **Ir** y confirme

### Filtros para eficiencia

Combine filtros para procesar solicitudes en lotes:

- **Programa + Estado**: Aprobar todas las solicitudes pendientes para su programa de influencers
- **Fecha + Estado**: Revisar solicitudes de la semana pasada
- **Método de pago + Estado**: Procesar todas las solicitudes de PayPal juntas

Este enfoque de lotes le ayuda a revisar solicitudes similares juntas, lo que facilita aplicar estándares consistentes.

## Consejos

- **Revise dentro de 24-48 horas** — Los tiempos de respuesta rápidos crean una primera impresión positiva y previenen que los solicitantes pierdan interés o se registren en competidores
- **Verifique los detalles de pago temprano** — Detectar correos electrónicos de PayPal inválidos o información bancaria incompleta en la etapa de solicitud previene problemas de pago más tarde
- **Revise su contenido primero** — Visite el sitio web o perfiles de redes sociales del solicitante antes de aprobar para verificar que tengan contenido real y una audiencia comprometida
- **Documente las razones del rechazo** — Use el campo de notas para registrar por qué rechazó una solicitud. Esto ayuda a mantener la consistencia y le protege si el solicitante vuelve a aplicar más tarde
- **Establezca requisitos claros del programa** — Actualice la página de destino de su portal de afiliados para indicar claramente qué busca en socios (tamaño mínimo de audiencia, tipo de contenido, etc.) para reducir aplicaciones no calificadas
- **Vigile a los solicitantes repetidos** — Algunos afiliados rechazados se registran nuevamente con diferentes direcciones de correo electrónico. Revise la URL del sitio web, el nombre de la empresa y los detalles de pago para detectar duplicados
- **Empiece estricto** — Es más fácil aprobar más liberalmente con el tiempo que eliminar afiliados problemáticos más tarde. Comience con criterios estrictos de aprobación y relájelos si necesita más socios

Recuerde: Preserve all markdown formatting, image paths, code blocks, and technical terms exactly as shown in the preservation rules.