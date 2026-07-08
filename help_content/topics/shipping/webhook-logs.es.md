---
title: Registros de Webhook
---

Los registros de webhook proporcionan un historial de auditoría permanente de todas las solicitudes de webhook entrantes de los transportistas—capturando el método de solicitud, la URL del punto final, los encabezados, la carga útil, el estado de procesamiento (pendiente/procesado/fallido) y la respuesta. Cada webhook se registra antes del procesamiento para asegurar que no se pierdan eventos si el procesamiento falla. Los registros permiten depurar problemas de integración de webhook, monitorear la fiabilidad de la API del transportista y reconstruir cronologías de entrega para el soporte al cliente.

Esta página de administración de solo lectura ayuda a solucionar problemas de fallos de webhook y verificar la salud de la integración del transportista.

## Estructura del Registro de Webhook

Cada entrada de registro registra:

**Detalles de la Solicitud**:
- **Clave del Proveedor**: ¿Cuál transportista envió el webhook (fedex, ups, dhl)
- **Endpoint**: Ruta del URL del webhook (ejemplo: `/webhooks/shipping/fedex/`)
- **Método**: Método HTTP (normalmente POST)
- **Encabezados**: Encabezados de solicitud (JSON)
- **Carga útil**: Cuerpo de la solicitud (JSON)

**Procesamiento**:
- **Estado de Procesamiento**: pendiente, procesado, fallido
- **Mensaje de Error**: Razón del fallo (si el estado=fallido)
- **Respuesta**: Respuesta HTTP enviada al transportista
- **Código de Estado de Respuesta**: 200, 400, 500, etc.

**Marcas de Tiempo**:
- **Recibido En**: Cuando llegó el webhook
- **Procesado En**: Cuando se completó el procesamiento

---

## Valores de Estado de Procesamiento

**pendiente**: Webhook recibido, esperando procesamiento
- Normal por un breve momento después de la recepción
- Si se atasca pendiente, indica un retraso en la cola de procesamiento

**procesado**: Webhook procesado con éxito
- Creado TrackingEvent
- Enviada notificación al cliente (si aplica)
- Enviada respuesta 200 al transportista

**fallido**: Fallo en el procesamiento del webhook
- Verifique el campo error_message para la razón
- Causas comunes: JSON inválido, envío desconocido, evento duplicado

---

## Flujo de Webhook

**Flujo Normal**:
```
1. El transportista escanea el paquete
   ↓
2. El transportista envía POST a endpoint de webhook de Spwig
   ↓
3. Spwig crea WebhookLog (status=pending)
   ↓
4. Trabajador en segundo plano procesa webhook
   ↓
5. Analizar carga útil JSON
   ↓
6. Encontrar envío coincidente (por número de seguimiento)
   ↓
7. Crear TrackingEvent
   ↓
8. Actualizar WebhookLog (status=processed)
   ↓
9. Enviar respuesta HTTP 200 al transportista
```

**Escenarios de Fallo**:
- **JSON inválido**: El transportista envió datos malformados → status=fallido, error="error de análisis de JSON"
- **Envío desconocido**: El número de seguimiento no coincide con ningún envío → status=fallido, error="Envío no encontrado"
- **Duplicado**: El evento ya existe → status=fallido, error="Evento duplicado"

---

## Depuración de Fallos de Webhook

**Paso a Paso**:

**1. Filtrar por Status=Fallido**
- Navegue a Envío > Registros de Webhook
- Filtro: Estado de procesamiento = "fallido"
- Revise los fallos recientes

**2. Verificar Mensaje de Error**
- Haga clic en la entrada del registro
- Lea el campo error_message
- Errores comunes:
  - "Envío no encontrado" → Mismatch en número de seguimiento
  - "error de decodificación de JSON" → El transportista envió JSON inválido
  - "Falta campo requerido" → Carga útil faltando datos esperados

**3. Inspeccionar Carga Útil**
- Ver la carga útil JSON cruda
- Verificar que la estructura coincida con el formato esperado
- Verificar campos faltantes (tracking_id, event_type, etc.)

**4. Verificar que el Envío Existe**
- Extraer el número de seguimiento de la carga útil
- Buscar Envíos por número de seguimiento
- Asegurarse de que el envío exista y use el transportista correcto

**5. Verificar Configuración del Proveedor**
- Verificar que la cuenta del proveedor esté activa
- Confirmar URL del punto final de webhook correcta
- Probar credenciales de API del proveedor

**6. Reintentar el Procesamiento** (si aplica)
- Algunos procesadores de webhook admiten reintentos manuales
- Arregle el problema subyacente primero
- Reintente el webhook fallido

---

## Problemas Comunes de Webhook

**Problema 1: "Envío no encontrado"**

**Causa**: El número de seguimiento en el webhook no coincide con ningún envío
- Error al crear el envío
- Webhook para una cuenta diferente
- Envío eliminado antes de recibir el webhook

**Solución**:
- Verificar ortografía del número de seguimiento
- Verificar que el transportista del envío coincida con el proveedor del webhook
- Reconstruir el envío si es necesario

---

**Problema 2: "error de decodificación de JSON"**

**Causa**: El transportista envió JSON malformado
- Raro, normalmente un error en la API del transportista
- Problemas de codificación de caracteres

**Solución**:
- Contactar al soporte del transportista con la carga útil cruda
- Verificar encabezados para codificación de charset
- Verificar URL del punto final en el panel de control del transportista

---

**Problema 3: Webhooks duplicados**

**Causa**: El transportista envía el mismo evento múltiples veces
- Lógica de reintento (el transportista no recibió 200)
- Error del transportista

**Solución**:
- El sistema rechaza automáticamente duplicados (comportamiento normal)
- Verificar que el código de estado de respuesta sea 200
- Si persiste, contactar al soporte del transportista

---

**Problema 4: Webhooks faltantes**

**Causa**: El webhook esperado nunca se recibió
- El transportista no lo envió (escaneo perdido)
- Punto final de webhook mal configurado en el panel del transportista
- Firewall bloqueando solicitudes

**Solución**:
- Verificar configuración de webhook en el panel del transportista
- Verificar que la URL del punto final sea pública y alcanzable
- Probar el punto final con curl/Postman
- Verificar reglas de firewall del servidor

---

## Configuración del Punto Final de Webhook

**URLs de Webhook Típicas**:
```
FedEx: https://yourdomain.com/webhooks/shipping/fedex/
UPS: https://yourdomain.com/webhooks/shipping/ups/
DHL: https://yourdomain.com/webhooks/shipping/dhl/
```

**Configuración en el Panel del Transportista**:
1. Iniciar sesión en el portal de desarrollo del transportista
2. Navegar a la configuración de webhook
3. Ingresar la URL de webhook de Spwig
4. Seleccionar eventos a suscribir (actualizaciones de seguimiento, entrega, excepciones)
5. Guardar la configuración
6. Probar webhook con la herramienta de prueba del transportista

**Seguridad**:
- Los webhooks requieren HTTPS (no HTTP)
- Algunos transportistas firman solicitudes (verificar firma)
- Lista blanca de IPs (si el transportista proporciona rangos de IP estáticos)

---

## Monitoreo de la Salud de Webhook

**Métricas Clave**:

**Tasa de Éxito**:
```
Tasa de Éxito = (Procesado / Total) × 100%

Meta: >98%
```

**Tiempo de Procesamiento**:
```
Tiempo Promedio = Procesado En - Recibido En

Meta: <2 segundos
```

**Patrones de Fallo**:
- Aumento repentino en fallos → Cambio o interrupción en la API del transportista
- Fallos consistentes "envío no encontrado" → Problema de sincronización del número de seguimiento
- Todos los webhooks fallidos → Problema de configuración del punto final

**Estrategia de Monitoreo**:
- Verificar tasa de fallo diariamente
- Alertar si la tasa de fallo >5%
- Revisar mensajes de error semanalmente
- Comparar con la página de estado del transportista

---

## Retención de Webhook

**Los registros son permanentes** - nunca se eliminan automáticamente

**¿Por Qué Permanentes**:
- Cumplimiento de auditoría
- Soporte al cliente (reconstruir cronología de entrega)
- Resolución de disputas
- Depuración de webhook

**Almacenamiento**: Los registros se almacenan de manera eficiente (JSON comprimido)

---

## Consejos

- **Los webhooks son un registro de auditoría permanente** - Nunca elimine, incluso si se procesan con éxito
- **Verifique webhooks fallidos diariamente** - Detecte problemas de integración temprano
- **Monitoree el retraso de procesamiento** - Retraso largo indica un problema de rendimiento
- **Guarde las cargas útiles crudas** - Esencial para depurar cambios en la API del transportista
- **Pruebe la configuración del punto final** - Use herramientas de prueba del transportista para verificar la configuración
- **Habilite la firma de webhook** - Verificar que las solicitudes realmente provengan del transportista
- **Agregue IPs del transportista a la lista blanca** - Si el transportista proporciona rangos de IP estáticos
- **Establezca alertas** - Notificar cuando la tasa de fallo exceda el umbral
- **Compare con el estado del transportista** - Brechas en webhooks pueden indicar una interrupción del transportista
- **Documente los formatos de carga útil del transportista** - Ayuda cuando el transportista actualiza la API
- **Mantenga URLs de webhook estables** - Cambiar URLs requiere actualización en el panel del transportista