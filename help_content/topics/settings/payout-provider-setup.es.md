---
title: Configuración del Proveedor de Pagos
---

La configuración del proveedor de pagos le permite configurar PayPal y Airwallex para pagos de afiliados automatizados. Esta guía le muestra cómo conectar sus cuentas de proveedor de pagos, configurar webhooks y probar su integración.

## Proveedores de Pagos Soportados

Spwig se integra con dos proveedores de pagos para automatizar los pagos de afiliados:

| Proveedor | Método de Pago | Procesamiento | Soporte de Lotes | Mejor Para |
|----------|----------------|------------|---------------|----------|
| **PayPal** | Transferencias desde cuentas de PayPal | Basado en API | Sí (hasta 15,000) | La mayoría de los afiliados, alcance global |
| **Airwallex** | Transferencias bancarias internacionales | Basado en API | No (individual) | Transferencias bancarias, pagos internacionales |

### Diferencias Clave

**Pagos de PayPal**:
- Requiere que el afiliado tenga una cuenta de PayPal (correo electrónico de pago)
- Procesa lotes de hasta 15,000 pagos a la vez
- Procesamiento más rápido (1-2 días hábiles)
- Menor complejidad de configuración
- Tarifas: ~2% o $0.25-$1.00 por pago
- Un solo webhook para todo el lote

**Airwallex**:
- Soporta transferencias bancarias directas
- Procesa pagos individuales uno a la vez
- Procesamiento más largo (2-5 días hábiles)
- Soporta múltiples monedas y países
- Las tarifas varían según el país de destino
- Webhook individual por pago

Puede configurar ambos proveedores y permitir que los afiliados elijan su método de pago preferido.

## ¿Por Qué Usar Proveedores de Pagos?

Integrar proveedores de pagos ofrece beneficios significativos frente a los pagos manuales:

- **Procesamiento automático** — No hay entrada de datos manual ni ejecución de pagos
- **Eficiencia de lotes** — Procese docenas o cientos de pagos con un solo clic
- **Confirmaciones de webhook** — Actualizaciones de estado automáticas cuando se completen los pagos
- **Menor número de errores** — El sistema valida los detalles de la cuenta antes del procesamiento
- **Registro de auditoría** — Registro completo de transacciones y respuestas del proveedor
- **Pagos más rápidos** — Los afiliados reciben los fondos más rápidamente
- **Escalabilidad** — Maneje programas de afiliados en crecimiento sin un trabajo administrativo proporcional

Sin la integración del proveedor, debe procesar cada pago manualmente a través de su banco o panel de PayPal, luego regresar a Spwig para marcar los pagos como completados.

## Configuración de PayPal

Siga estos pasos para configurar los pagos de PayPal para pagos de afiliados automatizados.

### Requisitos previos

Antes de comenzar, necesita:
- Una cuenta de PayPal Business (las cuentas personales no pueden usar la API de Pagos)
- Acceso al [Panel de Desarrollador de PayPal](https://developer.paypal.com/dashboard/)
- Aprobación para la API de Pagos (después de las pruebas en el entorno de sandbox)

### Paso 1: Crear una Aplicación de PayPal

1. **Navegue** a [Panel de Desarrollador de PayPal](https://developer.paypal.com/dashboard/)
2. **Inicie sesión** con su cuenta de PayPal Business
3. **Haga clic** en **Mis Aplicaciones y Credenciales** en el menú lateral izquierdo
4. **Seleccione** la pestaña **Vivo** (o Sandbox para pruebas)
5. **Haga clic** en **Crear Aplicación**
6. **Ingrese el nombre de la aplicación** (por ejemplo, "Pagos de Afiliados de Spwig")
7. **Seleccione el tipo de aplicación**: Comerciante
8. **Haga clic** en **Crear Aplicación**

PayPal genera sus credenciales.

### Paso 2: Obtener Credenciales de API

Después de crear la aplicación:

1. **Copia el ID de Cliente** — Cadena alfanumérica larga
2. **Haga clic** en **Mostrar** bajo Secreto
3. **Copia el Secreto del Cliente** — Manténgalo confidencial
4. **Nota el modo** — Sandbox o Vivo

### Paso 3: Habilitar la Función de Pagos

Las aplicaciones de PayPal requieren permiso explícito para usar Pagos:

1. **Desplácese** hasta la sección **Funciones** de su aplicación
2. **Encuentre** la función **Pagos**
3. **Haga clic** en **Añadir** si no está habilitada
4. **Presente para aprobación** si está usando el modo Vivo (la aprobación toma 1-2 días hábiles)

### Paso 4: Añadir Proveedor en Spwig

Ahora, añada la cuenta de PayPal a Spwig:

1. **Navegue** a **Configuración > Proveedores de Pagos**
2. **Haga clic** en **+ Añadir Cuenta de PayPal**
3. **Rellene el formulario**:
   - **Nombre de la Cuenta**: Etiqueta descriptiva (por ejemplo, "Cuenta Principal de PayPal")
   - **ID de Cliente**: Pegue desde el Panel de Desarrollador de PayPal
   - **Secreto del Cliente**: Pegue desde el Panel de Desarrollador de PayPal
   - **Modo**: Seleccione Sandbox (pruebas) o Producción (vivo)
   - **Está activo**: Marque para habilitar
4. **Haga clic en Guardar**

Spwig valida las credenciales solicitando un token de acceso. Si la validación falla, vuelva a verificar su ID de Cliente y Secreto.

### Paso 5: Probar la Conexión

Verifique su integración de PayPal:

1. Cree un pago de prueba en **Programa de Afiliados > Pagos**
2. Use su propio correo electrónico de PayPal como destinatario
3. Establezca el monto en $0.01 (si está en modo Producción) o cualquier monto (si es Sandbox)
4. Procese con el proveedor
5. Revise la cuenta de PayPal para ver el pago entrante
6. Verifique que el webhook actualice el estado del pago en Spwig

Si está usando el modo Sandbox, cree una cuenta de prueba de PayPal en [PayPal Sandbox](https://developer.paypal.com/dashboard/accounts) para recibir pagos de prueba.

## Configuración de Airwallex

Airwallex soporta transferencias bancarias internacionales para afiliados que prefieren depósitos directos.

### Requisitos previos

Antes de comenzar, necesita:
- Una cuenta de Airwallex (creada en [airwallex.com](https://www.airwallex.com))
- Estado de cuenta empresarial verificado
- Acceso a la API habilitado (póngase en contacto con el soporte de Airwallex si es necesario)
- Saldo suficiente en su cuenta de Airwallex

### Paso 1: Generar Credenciales de API

1. **Inicie sesión** en [Panel de Airwallex](https://www.airwallex.com/app/)
2. **Navegue** a **Configuración > Claves de API**
3. **Haga clic** en **Crear Clave de API**
4. **Ingrese una descripción**: "Pagos de Afiliados de Spwig"
5. **Seleccione permisos**: Active **Pagos** (lectura y escritura)
6. **Haga clic** en **Generar**
7. **Copia la Clave de API** — Mostrada solo una vez
8. **Copia el ID de Cliente** — Mostrado junto con la clave

### Paso 2: Nota su Entorno

Airwallex proporciona dos entornos:

- **Demo**: Para pruebas con transacciones falsas
- **Producción**: Para transferencias de dinero real

Asegúrese de conocer qué entorno pertenece su clave de API.

### Paso 3: Añadir Proveedor en Spwig

Añada la cuenta de Airwallex a Spwig:

1. **Navegue** a **Configuración > Proveedores de Pagos**
2. **Haga clic** en **+ Añadir Cuenta de Airwallex**
3. **Rellene el formulario**:
   - **Nombre de la Cuenta**: Etiqueta descriptiva (por ejemplo, "Cuenta de Airwallex en EUR")
   - **Clave de API**: Pegue desde el panel de Airwallex
   - **ID de Cliente**: Pegue desde el panel de Airwallex
   - **Entorno**: Seleccione Demo o Producción
   - **Está activo**: Marque para habilitar
4. **Haga clic en Guardar**

Spwig valida las credenciales consultando el saldo de su cuenta.

### Paso 4: Verificar Países Soportados

Airwallex soporta transferencias a muchos países, pero no todos. Revise la página de [cobertura de Airwallex](https://www.airwallex.com/global-business-account/global-transfers) para confirmar que los países de sus afiliados estén soportados.

Países comunes soportados incluyen:
- Estados Unidos
- Reino Unido
- Países de la Unión Europea
- Australia
- Canadá
- Singapur
- Hong Kong

### Paso 5: Probar Transferencia Bancaria

Pruebe su integración de Airwallex:

1. Cree un pago de prueba para un afiliado con detalles bancarios
2. Use una cantidad pequeña ($1-$5) si está en modo Producción
3. Procese con el proveedor
4. Revise el panel de Airwallex para la transacción
5. Espere la confirmación del webhook
6. Verifique que el pago se complete en Spwig

El modo Demo procesa instantáneamente. El modo Producción toma 2-5 días hábiles.

## Lógica de Selección del Proveedor

Cuando procesa un pago, Spwig selecciona automáticamente el proveedor adecuado según el método de pago del afiliado.

### Flujo de Selección

1. **Verificar el método de pago del afiliado**:
   - Si `payment_email` está establecido → El afiliado prefiere PayPal
   - Si están establecidos los detalles bancarios → El afiliado prefiere transferencia bancaria
2. **Asociar al proveedor**:
   - Correo electrónico de PayPal → Use la cuenta activa de PayPal
   - Detalles bancarios → Use la cuenta activa de Airwallex
3. **Recurrir al primero disponible** si el proveedor preferido no está configurado
4. **Mostrar error** si no existe proveedor coincidente

### Múltiples Cuentas de Proveedor

Puede configurar múltiples cuentas para el mismo proveedor (por ejemplo, dos cuentas de PayPal para diferentes regiones). Spwig selecciona la primera cuenta activa que coincida con el método de pago. Para controlar qué cuenta se usa, reordene las cuentas en la lista del administrador o establezca solo una como activa.

## Pruebas de Integración de Pagos

Siempre pruebe su integración del proveedor antes de procesar pagos reales a afiliados.

### Pruebas en Modo Sandbox/Demo

1. **Establezca el proveedor en modo sandbox** (PayPal Sandbox o Airwallex Demo)
2. **Cree un afiliado de prueba** con detalles de pago de prueba
3. **Cree comisiones de prueba** y apróbelas
4. **Cree un pago de prueba** que incluya esas comisiones
5. **Procese con el proveedor** usando el menú de acciones
6. **Monitoree los registros de Celery** para solicitudes de API
7. **Revise el panel del proveedor** para la transacción
8. **Espere la confirmación del webhook** para actualizar el estado del pago
9. **Verifique que las comisiones se marquen como pagadas**

### Pruebas en Modo Producción

Antes de ir en vivo:

1. **Cambie al modo producción** en la configuración del proveedor
2. **Cree un pago de prueba pequeño** a usted mismo ($0.01-$1.00)
3. **Procese** y espere a que se complete
4. **Verifique que los fondos hayan llegado** a su propia cuenta
5. **Revise que se haya disparado el webhook** y se haya actualizado el estado
6. **Revise las tarifas de transacción del proveedor**

### Problemas Comunes de Prueba

| Problema | Causa | Solución |
|-------|-------|----------|
| "Credenciales inválidas" | Clave de API incorrecta o desacuerdo de modo | Vuelva a verificar las credenciales, verifique sandbox vs producción |
| Webhook nunca se dispara | URL no configurada en el proveedor | Añada la URL del webhook en el panel del proveedor |
| El pago permanece en Procesamiento | Firma del webhook fallida | Verifique que la firma del webhook coincida |
| No hay proveedor disponible | No hay proveedor activo para el método de pago | Active al menos una cuenta de proveedor |

## Procesamiento por Lotes (PayPal)

PayPal soporta el procesamiento por lotes para eficiencia y ahorro de costos.

### Cómo Funciona el Procesamiento por Lotes

Cuando selecciona múltiples pagos y hace clic en **Procesar con el Proveedor**:

1. Spwig agrupa todos los pagos de PayPal en un solo lote
2. El sistema envía una sola solicitud de API con todos los detalles de pago (hasta 15,000)
3. PayPal procesa todo el lote como una sola transacción
4. El webhook devuelve con los resultados del lote
5. Spwig actualiza todos los pagos según la respuesta del lote

### Ventajas del Procesamiento por Lotes

- **Menos llamadas a la API** — Una solicitud para cientos de pagos
- **Menores tarifas** — Algunas estructuras de tarifas de PayPal favorecen el procesamiento por lotes
- **Procesamiento más rápido** — Ejecución paralela para todo el lote
- **Un solo webhook** — Más fácil de monitorear y registrar

### Límites de Lotes

PayPal impone estos límites:
- Máximo 15,000 destinatarios por lote
- Máximo $100,000 total por lote
- El procesamiento generalmente se completa en minutos

Si supera los 15,000 pagos, Spwig divide automáticamente en múltiples lotes.

## Procesamiento Individual (Airwallex)

Airwallex procesa pagos uno a la vez, lo que ofrece diferentes tradeoffs.

### Cómo Funciona el Procesamiento Individual

Cuando procesa pagos de Airwallex:

1. El sistema envía una solicitud de API separada para cada pago
2. Airwallex encola las transferencias individualmente
3. Cada transferencia se completa de forma independiente (2-5 días)
4. Un webhook individual se dispara cuando cada transferencia se complete
5. Spwig actualiza los pagos a medida que llegan los webhooks

### Ventajas del Procesamiento Individual

- **Mejor aislamiento de errores** — Un fallo no bloquea otros
- **Seguimiento por pago** — Identificadores de transacción individuales
- **Más detalles de pago** — Información específica del banco por transferencia
- **Tiempo flexible** — Las transferencias se completan a diferentes velocidades

### Tiempo de Procesamiento

A diferencia del procesamiento por lotes instantáneo de PayPal, las transferencias de Airwallex toman más tiempo:
- Transferencias nacionales: 1-2 días hábiles
- Transferencias internacionales: 3-5 días hábiles
- Algunos países: Hasta 7 días hábiles

Establezca las expectativas de los afiliados según corresponda en los términos de su programa.

## Configuración de Webhooks

Los webhooks permiten actualizaciones automáticas del estado del pago cuando los proveedores completan las transacciones.

### Formato de URL de Webhook

Configure esta URL en el panel del proveedor:

```
https://yourdomain.com/api/payout-providers/{provider}/webhook/
```

Reemplace `{provider}` con:
- `paypal` para webhooks de PayPal
- `airwallex` para webhooks de Airwallex

Ejemplos:
- `https://shop.example.com/api/payout-providers/paypal/webhook/`
- `https://shop.example.com/api/payout-providers/airwallex/webhook/`

### Configuración de Webhook de PayPal

1. **Navegue** a [Panel de Desarrollador de PayPal](https://developer.paypal.com/dashboard/)
2. **Haga clic** en el nombre de su aplicación
3. **Desplácese** hasta la sección **Webhooks**
4. **Haga clic** en **Añadir Webhook**
5. **Ingrese la URL del webhook** (formato anterior)
6. **Selecione eventos**:
   - `PAYMENT.PAYOUTSBATCH.SUCCESS`
   - `PAYMENT.PAYOUTSBATCH.DENIED`
   - `PAYMENT.PAYOUTS-ITEM.SUCCEEDED`
   - `PAYMENT.PAYOUTS-ITEM.FAILED`
7. **Haga clic en Guardar**

PayPal proporciona una clave de firma del webhook. Spwig usa esta para verificar la autenticidad del webhook.

### Configuración de Webhook de Airwallex

1. **Navegue** a [Panel de Airwallex](https://www.airwallex.com/app/)
2. **Vaya a** **Configuración > Webhooks**
3. **Haga clic** en **Crear Webhook**
4. **Ingrese la URL del webhook** (formato anterior)
5. **Selecione eventos**:
   - `transfer.created`
   - `transfer.completed`
   - `transfer.failed`
6. **Haga clic en Crear**

Airwallex firma los webhooks con su secreto de API.

### Seguridad de Webhooks

Los webhooks se validan mediante estos mecanismos:

- **Verificación de firma** — El proveedor firma el payload del webhook con una clave secreta
- **Verificación de marca de tiempo** — Rechaza webhooks antiguos (previene ataques de repetición)
- **Lista blanca de IPs (opcional)** — Restringe a rangos de IPs del proveedor
- **HTTPS obligatorio** — Los webhooks solo funcionan sobre SSL

Nunca desactive la verificación de firma en producción.

### Pruebas de Webhooks

La mayoría de los proveedores ofrecen herramientas de prueba de webhooks:

**PayPal**: Use el "Simulador" en el Panel de Desarrollador para disparar webhooks de prueba

**Airwallex**: Cree una transferencia de prueba en modo Demo y observe el webhook

También puede revisar los registros de webhooks en Spwig en **Configuración > Registros del Sistema** (si el registro está habilitado).

## Solución de Problemas

### Error de Credenciales Inválidas

**Síntoma**: "Autenticación fallida" al guardar la cuenta del proveedor

**Causas**:
- ID de Cliente o Secreto incorrecto
- Credenciales de sandbox usadas en modo producción (o viceversa)
- Clave de API expirada o revocada
- Cuenta no verificada

**Soluciones**:
- Vuelva a copiar las credenciales desde el panel del proveedor
- Verifique que el modo coincida (sandbox vs producción)
- Regenere las claves de API
- Póngase en contacto con el soporte del proveedor para verificar el estado de la cuenta

### Webhook No Recibido

**Síntoma**: El pago se queda en estado "Procesando" indefinidamente

**Causas**:
- URL del webhook no configurada en el panel del proveedor
- Certificado SSL inválido
- Firewall bloqueando IPs del proveedor
- Validación de firma del webhook fallida

**Soluciones**:
- Verifique la URL del webhook en la configuración del proveedor
- Verifique que el certificado SSL sea válido
- Permita las IPs del proveedor en el firewall
- Revise los registros de Celery para errores de firma
- Pruebe el webhook con la herramienta de simulación del proveedor

### Pago Fallido

**Síntoma**: El estado del pago cambia a "Fallido" con un mensaje de error

**Causas**:
- Detalles de pago del afiliado inválidos (correo electrónico o cuenta bancaria incorrecta)
- Saldo insuficiente en la cuenta del proveedor
- Cuenta del destinatario no puede recibir pagos
- País no soportado (Airwallex)
- Pago excede los límites del proveedor

**Soluciones**:
- Revise el error en el campo **Respuesta del Proveedor**
- Verifique que los detalles de pago del afiliado sean correctos
- Añada fondos a la cuenta del proveedor
- Pida al afiliado que revise el estado de su cuenta
- Revise el soporte de país y moneda del proveedor
- Divida los pagos grandes si exceden los límites

### Mismatch de Modo

**Síntoma**: Los pagos de prueba funcionan pero los pagos en producción fallan

**Causas**:
- El proveedor está en modo Sandbox pero se usan cuentas de afiliados en producción
- Claves de API de un entorno incorrecto

**Soluciones**:
- Cambie el modo del proveedor a Producción
- Regenere las claves de API de producción
- Verifique que la URL del webhook apunte al dominio de producción

## Mejores Prácticas de Seguridad

Proteja su integración de pagos con estas medidas de seguridad:

### Almacenamiento de Credenciales

- **Nunca comprometa credenciales en el control de versiones** — Use variables de entorno o almacenamiento seguro
- **Rotar claves de API cada trimestre** — Genere nuevas claves cada 3 meses
- **Use claves separadas para sandbox y producción** — Nunca mezcle entornos
- **Limite los permisos de API** — Otorgue solo acceso a Pagos, no control completo de la cuenta

Spwig almacena las credenciales del proveedor encriptadas en la base de datos. Mantenga sus copias de seguridad de la base de datos seguras.

### Seguridad de Webhooks

- **Siempre verifique las firmas** — Nunca omita la validación de firma
- **Use HTTPS exclusivamente** — Los webhooks HTTP no son compatibles
- **Implemente lista blanca de IPs** — Restrinja los webhooks a rangos de IPs del proveedor
- **Registre todos los webhooks** — Monitoree para actividad sospechosa
- **Límite la tasa de endpoints de webhook** — Prevenga el abuso

### Control de Acceso

- **Limite el acceso del personal** — Solo el personal de confianza debe procesar pagos
- **Use autenticación de dos factores** — Requiera 2FA para cuentas de personal
- **Revise las acciones de pagos** — Revise quién procesó qué pagos
- **Separe responsabilidades** — Personal diferente para aprobación vs procesamiento

### Monitoreo

- **Revise los pagos fallidos diariamente** — Aborde los problemas de inmediato
- **Monitoree los saldos de la cuenta del proveedor** — Asegúrese de tener fondos suficientes
- **Revise los registros de transacciones semanalmente** — Detecte anomalías temprano
- **Establezca alertas** — Notificaciones por correo electrónico para pagos grandes o fallidos

## Consejos

- Pruebe su integración exhaustivamente en modo sandbox antes de cambiar a producción — detecte problemas con dinero falso.
- Configure tanto PayPal como Airwallex para dar a los afiliados la opción de pago — diferentes afiliados prefieren métodos diferentes.
- Establezca URLs de webhook durante la configuración inicial y verifique que se disparen correctamente — los webhooks son críticos para la automatización.
- Mantenga los saldos de la cuenta del proveedor actualizados para evitar pagos fallidos durante el procesamiento por lotes.
- Use nombres de cuenta descriptivos si configura múltiples proveedores (por ejemplo, "Cuenta de PayPal en USD", "Cuenta de PayPal en EUR").
- Rotar las credenciales de API cada trimestre como una práctica de seguridad.
- Documente sus URLs de webhook y credenciales en un gestor de contraseñas seguro compartido con su equipo.
- Revise los pagos fallidos inmediatamente — los retrasos frustran a los afiliados y dañan la reputación del programa.
- Siempre use HTTPS para su instalación de Spwig — los webhooks requieren certificados SSL.
- Póngase en contacto con el soporte del proveedor si encuentra errores persistentes — pueden verificar el estado de su cuenta y permisos.