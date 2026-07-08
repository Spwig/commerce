---
title: Procesamiento de pagos
---

El procesamiento de pagos le permite pagar a los afiliados por sus comisiones aprobadas. Esta guía le muestra cómo crear, administrar y procesar pagos a través de PayPal o proveedores de transferencia bancaria.

![Lista de pagos](/static/core/admin/img/help/payout-processing/payout-list.webp)

## Visión general del pago

Un pago es un lote de pagos que agrupa múltiples comisiones aprobadas para un solo afiliado. Piénselo como un cheque para todas las ganancias pendientes.

Características clave:
- **Incluye múltiples comisiones** — Un pago puede cubrir docenas de comisiones aprobadas
- **Requiere umbral mínimo** — La mayoría de los programas tienen montos mínimos de pago ($50-$100 típicos)
- **Procesado a través de proveedores** — PayPal o Airwallex manejan la transferencia real de dinero
- **Tiene ciclo de vida** — Pendiente → Procesando → Completado (o Fallido)

## Flujo de trabajo de pago

El proceso completo de pago sigue seis pasos:

1. **El afiliado gana comisiones** — Ventas atribuidas a enlaces de seguimiento del afiliado
2. **El comerciante aprueba comisiones** — Revisa y aprueba comisiones pendientes
3. **El saldo alcanza el mínimo** — El saldo aprobado del afiliado cumple con el umbral del programa
4. **El afiliado solicita un pago** — El afiliado presenta una solicitud de pago en su panel de control
5. **El comerciante procesa el pago** — Usted crea y procesa el pago
6. **Pago completado** — El proveedor envía los fondos, las comisiones se marcan como pagadas

## Ver pagos

Navegue a **Programa de afiliados > Pagos** para acceder al panel de control de administración de pagos.

El panel de estadísticas muestra:
- **Pendiente** — Pagos creados pero aún no procesados
- **Procesando** — Actualmente se envían al proveedor de pago
- **Completado** — Pagado con éxito
- **Fallido** — El pago falló (requiere atención)

La vista de lista muestra:
- Nombre y código del afiliado
- Monto del pago
- Método de pago (PayPal o Transferencia bancaria)
- Etiqueta de estado
- Fechas de creación y finalización
- Botones de acción

Use filtros para restringir por:
- Afiliado
- Método de pago
- Estado
- Rango de fechas

## Crear un pago

Siga estos pasos para crear un nuevo pago:

1. **Navegue** a **Programa de afiliados > Pagos**
2. **Haga clic** en el botón **+ Agregar pago**
3. **Seleccione afiliado** desde el menú desplegable
4. **Revise comisiones aprobadas** — El sistema muestra todas las comisiones no pagadas y aprobadas para este afiliado
5. **Seleccione comisiones para incluir** — Marque las casillas para las comisiones que desea pagar (normalmente todas)
6. **Verifique el monto total** — El sistema calcula la suma automáticamente
7. **Elija el método de pago** — PayPal o Transferencia bancaria (según la preferencia del afiliado)
8. **Seleccione la cuenta del proveedor** — Elija qué cuenta de PayPal/Airwallex usar
9. **Añada notas** (opcional) — Notas internas para el registro
10. **Haga clic en Guardar** — El pago se crea con el estado "Pendiente"

El pago ahora está listo para procesar.

## Procesamiento de pagos

Tiene dos opciones para procesar pagos: manual o basado en proveedor.

### Procesamiento manual

Use el procesamiento manual cuando maneje pagos fuera del sistema (cheques, transferencias bancarias, etc.):

1. Seleccione el pago en la lista
2. Haga clic en la acción **Marcar como en proceso**
3. Complete el pago mediante su método externo
4. Vuelva al pago
5. Haga clic en la acción **Marcar como completado**
6. Las comisiones se actualizan automáticamente a "Pagadas"

El procesamiento manual ofrece flexibilidad pero requiere más trabajo administrativo.

### Procesamiento por proveedor (Recomendado)

El procesamiento por proveedor automatiza los pagos a través de PayPal o Airwallex:

1. **Seleccione pago(s)** en la lista (puede procesar varios)
2. **Haga clic** en la acción **Procesar con proveedor**
3. **Confirme** en el cuadro de diálogo
4. **El sistema encola la tarea** — El trabajador Celery maneja la llamada a la API
5. **El proveedor procesa el pago**:
   - **PayPal**: Lotes de hasta 15,000 pagos por solicitud
   - **Airwallex**: Transferencias bancarias individuales
6. **El webhook actualiza el estado** — El proveedor confirma la finalización
7. **Las comisiones se marcan como pagadas** — El sistema actualiza todas las comisiones incluidas

El procesamiento por proveedor es más rápido, más confiable y crea un registro de auditoría automático.

## Métodos de pago

Spwig admite dos métodos de pago con requisitos diferentes:

| Método | Proveedor | Requisitos | Tiempo de procesamiento | Tarifas | Mejor para |
|--------|----------|--------------|-----------------|------|----------|
| **PayPal** | PayPal Payouts | El afiliado debe tener un `payment_email` válido | 1-2 días hábiles | ~2% o $0.25-$1.00 por pago | La mayoría de los afiliados, alcance global |
| **Transferencia bancaria** | Airwallex | Detalles de la cuenta bancaria (número de cuenta, ruta, SWIFT) | 2-5 días hábiles | Varía según el país | Afiliados internacionales, montos grandes |

Los afiliados configuran su método de pago y detalles en su panel de control. El sistema selecciona automáticamente el proveedor adecuado según su preferencia.

### Lógica de selección del método de pago

Al procesar un pago, Spwig selecciona el proveedor de la siguiente manera:

1. Verifique el método de pago preferido del afiliado (PayPal o Transferencia bancaria)
2. Asigne a la cuenta del proveedor configurada (PayPal → PayPal, Banco → Airwallex)
3. Si no hay preferencia disponible, caiga en el primer proveedor disponible
4. Muestre un error si no hay proveedores configurados

## Flujo de estados de pago

Entender los estados de los pagos le ayuda a seguir el progreso del pago:

| Estado | Significado | Acción siguiente |
|--------|---------|-------------|
| **Pendiente** | Creado pero aún no enviado al proveedor | Procesar con proveedor o marcar como en proceso |
| **En proceso** | Enviado al proveedor de pago, esperando confirmación | Espere el webhook o revise el panel de control del proveedor |
| **Completado** | Pago exitoso, fondos enviados | Ninguna — las comisiones se marcan como pagadas |
| **Fallido** | El pago falló (ver detalles del error) | Revise el error, corrija el problema, reintente o cancele |
| **Cancelado** | Cancelado manualmente antes de la finalización | Ninguna — las comisiones permanecen sin pagar |

### Camino de éxito

Pendiente → En proceso → Completado

Este es el camino feliz. Los webhooks del proveedor actualizan automáticamente el estado a medida que se procesa el pago.

### Camino de falla

Pendiente → En proceso → Fallido

Cuando un pago falla, el estado del pago cambia a Fallido y debe investigar.

## Manejo de pagos fallidos

Los pagos fallidos requieren intervención manual. Razones comunes de falla:

| Causa | Error del proveedor | Solución |
|-------|----------------------------------|----------|
| Cuenta inválida | "Cuenta del destinatario no encontrada" | Verifique el correo electrónico de pago del afiliado o los detalles bancarios |
| Saldo insuficiente | "Fondos insuficientes" | Agregue fondos a su cuenta del proveedor |
| Error en los detalles bancarios | "Número de ruta inválido" | Pida al afiliado que actualice su información bancaria |
| Restricción de cuenta | "El destinatario no puede recibir pagos" | Póngase en contacto con el afiliado para resolver el estado de su cuenta |
| Problema del proveedor | "Servicio temporalmente no disponible" | Espere y reintente después de unas horas |

### Cómo reintentar un pago fallido

1. **Ver el pago fallido** — Haga clic en él en la lista
2. **Lea el mensaje de error** — Revise el campo **Respuesta del proveedor** para obtener detalles
3. **Corrija el problema subyacente** — Actualice los detalles del afiliado, agregue fondos al proveedor, etc.
4. **Restablezca el estado** — Cambie el estado de nuevo a Pendiente (formulario de edición)
5. **Procese nuevamente** — Use la acción **Procesar con proveedor**

### Cómo cancelar y recrear

Si reintentar no funciona:

1. **Abra el pago fallido**
2. **Cambie el estado a Cancelado**
3. **Guarde el pago**
4. **Cree un nuevo pago** — Siga los pasos de creación nuevamente
5. **Procese el nuevo pago**

Los pagos cancelados no marcan las comisiones como pagadas, por lo que permanecen elegibles para nuevos pagos.

## Integración del proveedor de pagos

El procesamiento de pagos requiere una cuenta de proveedor de pagos configurada. Spwig se integra con:

- **API de pagos de PayPal** — Para pagos con PayPal
- **Airwallex** — Para transferencias bancarias internacionales

### Requisitos de configuración

Antes de procesar pagos:
1. Configure al menos un proveedor en **Configuración > Proveedores de pagos**
2. Agregue credenciales de API (ID de cliente, secreto, clave de API)
3. Establezca el modo de producción (sandbox para pruebas)
4. Configure la URL del webhook en el panel de control del proveedor
5. Verifique la conectividad con un pago de prueba

Vea la guía [Configuración del proveedor de pagos](#) para instrucciones detalladas de configuración.

### Selección del proveedor por el afiliado

Los afiliados eligen su método de pago preferido en su panel de control:
- PayPal: Ingrese `payment_email`
- Transferencia bancaria: Ingrese los detalles de la cuenta bancaria

El sistema enruta automáticamente los pagos al proveedor correspondiente.

## Mejores prácticas para el calendario de pagos

Establezca un calendario regular de pagos para construir confianza con los afiliados:

| Calendario | Frecuencia | Carga de trabajo | Satisfacción del afiliado | Recomendado para |
|----------|-----------|----------|------------------------|-----------------|
| Semanal | Cada viernes | Alta | Excelente | Programas nuevos, alto volumen |
| Cada dos semanas | 1° y 15° | Media | Buena | Programas de volumen medio |
| Mensual | 1° del mes | Baja | Aceptable | Programas establecidos |
| Trimestral | Cada 3 meses | Muy baja | Mala | No recomendado |

Considere el tamaño de su programa y la capacidad administrativa al elegir un calendario.

## Mejores prácticas para el procesamiento

Siga estas pautas para operaciones de pago fluidas:

- **Agrupe los pagos por calendario** — Procese todos los pagos elegibles el mismo día cada semana/mes
- **Verifique los detalles antes de procesar** — Revise dos veces la información de pago del afiliado, especialmente para montos grandes
- **Supervise el saldo del proveedor** — Asegúrese de que haya suficientes fondos en su cuenta de PayPal/Airwallex
- **Establezca umbrales mínimos claros** — Comunique los mínimos de pago en los términos del programa ($50-$100 típicos)
- **Documente su calendario** — Agregue el calendario de pagos a los términos del afiliado y a la configuración del portal
- **Use el procesamiento del proveedor** — Evite el procesamiento manual a menos que sea absolutamente necesario
- **Revise los pagos fallidos inmediatamente** — Aborde los fallos dentro de las 24 horas
- **Mantenga configurados los webhooks del proveedor** — Los webhooks permiten actualizaciones de estado automáticas
- **Descargue informes de pagos regularmente** — Descargue informes mensuales para contabilidad

## Registros de pagos y reportes

Cada pago crea un registro inmutable con:
- Información del afiliado
- IDs de comisión incluidos
- Monto total
- Método de pago y proveedor
- Marcas de tiempo de creación y finalización
- ID de transacción del proveedor (después del procesamiento)
- Datos de respuesta del proveedor (para depuración)
- Notas internas

Acceda a estos datos haciendo clic en cualquier pago en la lista. Use la función de exportación de la interfaz de administración para descargar informes de pagos para fines de contabilidad o impuestos.

## Consejos

- Procese los pagos en un horario fijo (por ejemplo, todos los viernes a las 2:00 p.m.) para que los afiliados sepan cuándo esperar el pago.
- Siempre use el procesamiento del proveedor en lugar del procesamiento manual — es más rápido, más confiable y crea mejores registros de auditoría.
- Establezca umbrales mínimos de pago en sus programas para reducir la carga administrativa — $50 o $100 es estándar.
- Supervise el saldo de su cuenta del proveedor antes de procesar lotes grandes para evitar fallos.
- Pruebe su integración de pagos en modo sandbox antes de usar pagos reales.
- Añada una nota a cada pago explicando el período que cubre (por ejemplo, "Comisiones de enero de 2026").
- Revise los pagos fallidos inmediatamente — los retrasos frustran a los afiliados y dañan la confianza.
- Comunique proactivamente los retrasos — si no puede procesar en el horario acordado, notifique a los afectados con anticipación.

Recuerde: preserve all markdown formatting, image paths, code blocks, and technical terms exactly as shown in the preservation rules.