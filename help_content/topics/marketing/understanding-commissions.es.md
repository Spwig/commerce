---
title: Comprensión de las comisiones
---

Las comisiones son registros de ingresos creados cuando un afiliado logra generar una venta en tu tienda. Cada comisión está vinculada a un pedido específico, un afiliado y un programa, y pasa por un ciclo de vida desde pendiente hasta pagada. Esta guía explica cómo funcionan las comisiones, cómo se calculan y cómo gestionarlas de manera efectiva.

## ¿Qué es una comisión?

Una comisión representa la cantidad que se debe a un afiliado por referir a un cliente que completó una compra. Cuando un cliente hace clic en el enlace de referencia de un afiliado y coloca un pedido dentro del período de vida de la cookie, Spwig crea automáticamente un registro de comisión.

Cada comisión contiene:
- **Afiliado** — El socio que refirió al cliente
- **Programa** — El programa de afiliados que define las reglas de la comisión
- **Pedido** — El pedido que generó la comisión
- **Monto** — El valor calculado de la comisión
- **Estado** — La etapa actual en el ciclo de vida de la comisión
- **Fechas** — Fecha de creación, fecha de aprobación/rechazo y fecha de pago

## Cálculo de comisiones

Las comisiones se calculan automáticamente según el tipo de comisión y la tasa del programa.

| Tipo de comisión | Cálculo | Ejemplo |
|------------------|---------|---------|
| **Porcentaje** | Total del pedido × porcentaje de comisión ÷ 100 | Pedido: $200, Tasa: 10% → **$20 de comisión** |
| **Fijo** | Monto fijo por pedido | Tasa: $15 → **$15 de comisión** (independientemente del valor del pedido) |

### Ejemplos de cálculo

**Comisión por porcentaje (10%)**:
- Cliente coloca un pedido de $50 → $5 de comisión
- Cliente coloca un pedido de $150 → $15 de comisión
- Cliente coloca un pedido de $300 → $30 de comisión

**Comisión fija ($20)**:
- Cliente coloca un pedido de $50 → $20 de comisión
- Cliente coloca un pedido de $150 → $20 de comisión
- Cliente coloca un pedido de $300 → $20 de comisión

La comisión se calcula en el **subtotal del pedido** (antes de envío y impuestos) y se crea inmediatamente cuando se coloca el pedido.

## Ciclo de vida de la comisión

Toda comisión pasa por una serie de estados desde su creación hasta el pago:

```
Pending → Approved → Paid
   ↓
Rejected
```

### Definiciones de estado

| Estado | Descripción | ¿Qué ocurre? |
|--------|-------------|--------------|
| **Pending** | Pedido realizado, comisión en espera de revisión | La comisión se crea pero aún no está confirmada. El afiliado puede verla pero no puede retirar fondos. |
| **Approved** | El comerciante confirma que la venta es válida | La comisión se verifica y se agrega al saldo disponible del afiliado. Es elegible para pago. |
| **Rejected** | El comerciante rechaza la comisión | La comisión se niega (por ejemplo, el pedido fue reembolsado, fraudulento o violó términos). No es elegible para pago. |
| **Paid** | La comisión se incluyó en un pago completado | El afiliado ha sido pagado. La comisión se finaliza y no se puede modificar. |

![Lista de comisiones](/static/core/admin/img/help/commission-management/commission-list.webp)

## Cuándo se crean las comisiones

Las comisiones se crean automáticamente siguiendo esta secuencia:

1. **El cliente hace clic en el enlace del afiliado** — La URL de referencia contiene el código de seguimiento único del afiliado (por ejemplo, `?ref=JOHNSMITH`)
2. **Se establece la cookie** — Se almacena una cookie de seguimiento en el navegador del cliente con el código del afiliado
3. **Compra dentro del período de vida de la cookie** — El cliente completa un pedido antes de que expire la cookie (por defecto: 30 días)
4. **El sistema atribuye el pedido** — Spwig verifica una cookie de seguimiento activa e identifica al afiliado que refirió al cliente
5. **Creación automática de comisión** — Se genera un registro de comisión con el estado **Pending**

La comisión se crea **inmediatamente** cuando se coloca el pedido, incluso antes de que se confirme el pago. Esto permite a los comerciantes revisar las comisiones mientras se procesan los pedidos.

## Seguimiento y atribución

Spwig utiliza **atribución por último clic** para determinar qué afiliado debe recibir crédito por una venta.

### Cómo funciona la atribución

- **Modelo de último clic** — El enlace del afiliado más reciente hace clic y obtiene el crédito (incluso si múltiples afiliados refirieron al cliente)
- **Seguimiento basado en cookies** — Una cookie almacena el código del afiliado en el navegador del cliente
- **Duración de la cookie** — Determina el período durante el cual una venta puede atribuirse (configurado por programa, normalmente 30 días)
- **Seguimiento de IP y sesión** — Datos adicionales ayudan a identificar patrones fraudulentos

### Ejemplo de atribución

- Día 1: El cliente hace clic en el enlace del afiliado A → Cookie establecida para el afiliado A
- Día 5: El cliente hace clic en el enlace del afiliado B → Cookie **actualizada** al afiliado B (el último clic gana)
- Día 7: El cliente coloca un pedido → La comisión va a **afiliado B**

Si el cliente vuelve el día 35 (después de que expire la cookie de 30 días) y coloca un pedido, **no se crea comisión** porque la ventana de seguimiento se cerró.

## Detalles de la comisión

Navegue a **Marketing > Comisiones** para ver todos los registros de comisión.

### Campos de la comisión

Cada comisión muestra:

| Campo | Descripción |
|-------|-------------|
| **Afiliado** | El nombre y código del afiliado |
| **Programa** | El nombre del programa de afiliados |
| **Pedido** | Número de pedido (enlace clickeable para ver los detalles del pedido completo) |
| **Monto** | Valor calculado de la comisión |
| **Estado** | Etapa actual (Pendiente, Aprobada, Rechazada, Pagada) |
| **Creada** | Cuando se generó la comisión |
| **Fecha de aprobación/rechazo** | Cuando se actualizó el estado |
| **Fecha de pago** | Cuando se procesó el pago |
| **Notas** | Notas internas sobre la comisión |

### Ver detalles del pedido

Haga clic en el **número de pedido** en el registro de comisión para ver el pedido original. Esto le permite verificar:
- Total del pedido y artículos comprados
- Información del cliente
- Estado del pago
- Estado del envío
- Cualquier reembolso o devolución

Este contexto le ayuda a decidir si aprobar o rechazar la comisión.

## Gestionar comisiones

Aunque esta guía se centra en comprender las comisiones, los pasos prácticos para aprobar, rechazar y pagar comisiones se cubren con detalle en el tema de ayuda **Gestión de comisiones**.

### Visión general rápida

- **Aprobar** — Verifique que el pedido sea legítimo y confirme que la comisión es válida
- **Rechazar** — Rechace comisiones por pedidos fraudulentos, reembolsos o violaciones de políticas
- **Añadir notas** — Documente las razones de la aprobación o rechazo para referencia futura
- **Procesar pagos** — Agrupe comisiones aprobadas en pagos por lotes

Consulte los temas de ayuda relacionados para obtener instrucciones paso a paso sobre cada tarea de gestión.

## Consejos

- Revise las comisiones pendientes **diariamente** durante su primer mes para establecer un ritmo y detectar cualquier problema de seguimiento temprano
- Configure **notificaciones por correo electrónico** para alertarle cuando se creen nuevas comisiones, para que pueda revisarlas mientras los detalles del pedido estén frescos
- Aprobar comisiones **después de la entrega del pedido** (no inmediatamente al colocar el pedido) para tener en cuenta las cancelaciones y devoluciones
- Use el **campo de notas** para documentar decisiones, especialmente para comisiones rechazadas, para que tenga un registro si los afiliados hacen preguntas
- Busque **patrones de rechazo** — si un afiliado tiene muchas comisiones rechazadas, podría indicar fraude o malentendidos sobre los términos del programa
- Considere crear una **política de aprobación de comisiones** (por ejemplo, "aprobadas después del período de devolución de 14 días") y comuníquela a los afiliados para establecer expectativas claras

Recuerde: preserve todos los formatos de markdown, rutas de imágenes, bloques de código y términos técnicos exactamente como se muestran en las reglas de preservación.