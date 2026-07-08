---
title: Eventos de Seguimiento
---

Los eventos de seguimiento registran puntos de control del estado del envío durante el ciclo de vida de la entrega—cada evento captura el estado (en tránsito, en camino de entrega, entregado), marca de tiempo, ubicación, descripción y datos brutos del transportista. Los eventos se crean automáticamente a través de notificaciones de webhook del transportista o manualmente por los comerciantes. Los clientes ven el historial de eventos de seguimiento en su cuenta y en los correos electrónicos de confirmación de pedido, proporcionando visibilidad en tiempo real sobre el estado de la entrega.

Esta página de administración muestra un historial de eventos de solo lectura para fines de auditoría y soporte al cliente.

## Estructura del Evento de Seguimiento

Cada evento contiene:

**Información de Estado**:
- **Estado**: en_tránsito, en_camino_de_entrega, entregado, excepción, fallido, devuelto
- **Descripción**: Estado legible para humanos (ej. "Paquete llegó a la instalación de clasificación")
- **Código de Estado del Transportista**: Estado original del transportista (ej. "DEP" para salido)

**Datos de Ubicación**:
- **Ciudad**: Ciudad de la ubicación del evento
- **Estado**: Estado/provincia de la ubicación del evento
- **País**: País de la ubicación del evento
- **Código Postal**: Código postal/ZIP de la ubicación del evento

**Marcas de Tiempo**:
- **Ocurrió en**: Cuándo ocurrió el evento (hora del transportista)
- **Creado en**: Cuándo se registró el evento en Spwig (hora del sistema)

**Metadatos**:
- **Datos Brutos**: Respuesta JSON completa de la API del transportista
- **Envío**: ID de envío vinculado

---

## Tipos de Estado del Evento

**en_tránsito**: Paquete en movimiento a través de la red del transportista
- Ejemplos: "Salida de la instalación", "Llegada al centro", "En tránsito hacia la próxima instalación"

**en_camino_de_entrega**: Paquete en el vehículo de entrega
- Ejemplos: "En camino de entrega", "En el vehículo de entrega"

**entregado**: Paquete entregado con éxito
- Ejemplos: "Entregado a la puerta principal", "Dejado en recepción", "Entregado al destinatario"

**excepción**: Problema de entrega que requiere atención
- Ejemplos: "Retraso por clima", "Dirección incorrecta", "Intento de entrega fallido"

**fallido**: Entrega fallida permanentemente
- Ejemplos: "No se puede entregar según la dirección", "Rechazado por el destinatario"

**devuelto**: Paquete siendo devuelto al remitente
- Ejemplos: "Iniciada la devolución al remitente", "Paquete devolviéndose"

---

## Cómo Se Crean los Eventos de Seguimiento

### Automático (Webhook del Transportista)

**Flujo de Trabajo**:
1. El transportista escanea el paquete (salida, llegada, entrega)
2. El transportista envía un webhook a un punto final de webhook de Spwig
3. El webhook se registra en la tabla WebhookLog
4. El sistema analiza la carga útil del webhook
5. Se crea el TrackingEvent con los datos extraídos
6. Se envía una notificación por correo electrónico al cliente (si está configurado)

**Beneficios**:
- Actualizaciones en tiempo real (no se requiere encuestar)
- Marcas de tiempo precisas del transportista
- Historial de eventos completo mantenido automáticamente

### Manual (Entrada del Comerciante)

**Flujo de Trabajo**:
1. Navegue a los detalles del envío
2. Haga clic en "Añadir Evento de Seguimiento"
3. Seleccione el estado desde el menú desplegable
4. Ingrese la descripción
5. Opcional: Ingrese datos de ubicación
6. Establezca la marca de tiempo occurred_at
7. Guarde

**Casos de Uso**:
- Transportistas sin soporte de webhook
- Correcciones manuales de envío
- Entregas locales (no transportista)
- Actualizaciones de estado internas

---

## Orden de Visualización de Eventos

Los eventos se muestran en **orden cronológico inverso** (más recientes primero):

**Ejemplo de Visualización**:
```
13 de febrero de 2026 10:30 AM - Entregado (Brooklyn, NY)
13 de febrero de 2026 08:15 AM - En camino de entrega (Brooklyn, NY)
12 de febrero de 2026 11:45 PM - Llegó a la instalación local (Brooklyn, NY)
12 de febrero de 2026 06:30 PM - En tránsito (Newark, NJ)
12 de febrero de 2026 02:15 PM - Salida del origen (Filadelfia, PA)
12 de febrero de 2026 09:00 AM - Recogido (Filadelfia, PA)
```

---

## Visibilidad del Cliente

Los eventos de seguimiento se muestran a los clientes en:

**Correo Electrónico de Confirmación de Pedido**:
- Estado del evento más reciente
- Fecha estimada de entrega
- Enlace de seguimiento

**Cuenta del Cliente > Detalles del Pedido**:
- Línea de tiempo completa del evento
- Descripciones del evento
- Historial de ubicaciones
- Marcas de tiempo

**Página de Seguimiento** (si está habilitada):
- URL de seguimiento dedicada
- Línea de tiempo visual
- Logotipo del transportista
- Mapa de entrega (si están disponibles datos de ubicación)

---

## Filtros de Eventos de Seguimiento

**Filtros Útiles**:
- **Envío**: Ver eventos para un envío específico
- **Estado**: Filtrar por tipo de evento (entregado, en_tránsito, etc.)
- **Rango de Fechas**: Eventos dentro de un período de tiempo
- **Ubicación**: Eventos en una ciudad/estado específico

**Casos de Uso**:
- "Mostrar todos los envíos entregados hoy"
- "Encontrar todas las excepciones de la semana pasada"
- "Seguir envíos actualmente en tránsito"

---

## Datos Brutos (Depuración)

**Campo de Datos Brutos**:
- Almacena la respuesta completa de la API del transportista como JSON
- Útil para depurar problemas de webhook
- Contiene metadatos específicos del transportista

**Ejemplo de Datos Brutos** (FedEx):
```json
{
  "event_type": "OD",
  "event_description": "Out for delivery",
  "timestamp": "2026-02-13T08:15:00Z",
  "location": {
    "city": "Brooklyn",
    "state": "NY",
    "postal_code": "11201",
    "country": "US"
  },
  "delivery_signature": null,
  "estimated_delivery": "2026-02-13T17:00:00Z"
}
```

**Cuándo Revisar los Datos Brutos**:
- La descripción del evento es confusa
- Faltan datos de ubicación
- Errores de procesamiento de webhook
- Escalado a soporte del transportista

---

## Tiempo de Evento

**Ocurrió en** vs **Creado en**:

**Ocurrió en**: Cuándo ocurrió el evento del transportista
- Ejemplo: Paquete escaneado a las 10:30 AM

**Creado en**: Cuándo Spwig recibió el webhook
- Ejemplo: Webhook recibido a las 10:32 AM (retraso de 2 minutos)

**¿Por Qué Son Diferentes?**:
- Latencia de red
- Procesamiento por lotes del transportista
- Retrasos de reintentos de webhook

**Use Ocurrió en para la visualización del cliente** - reflejo más preciso del progreso real de la entrega.

---

## Consejos

- **Los eventos son de solo lectura** - No se pueden editar después de su creación (integridad de auditoría)
- **Revise los datos brutos para detalles** - Más información que los campos mostrados
- **Monitorea el retraso de webhook** - Un gran retraso entre occurred_at y created_at indica problemas con el webhook
- **Úsalo para soporte al cliente** - La línea de tiempo del evento ayuda a diagnosticar problemas de entrega
- **Seguimiento de patrones de entrega** - Analiza el tiempo de eventos para evaluar el desempeño del transportista
- **Configura notificaciones** - Enviar automáticamente correos electrónicos a los clientes en eventos clave (en_camino_de_entrega, entregado)
- **No elimines eventos** - Conserva el historial completo de auditoría
- **Revisa WebhookLog para errores** - Eventos faltantes pueden indicar errores en el procesamiento del webhook
- **Los datos de ubicación varían según el transportista** - Algunos transportistas proporcionan ubicación detallada, otros mínima
- **Los eventos de excepción requieren atención** - Monitorea y sigue los problemas de entrega