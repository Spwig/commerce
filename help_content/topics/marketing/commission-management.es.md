---
title: Gestión de comisiones
---

La gestión de comisiones es el proceso de revisar y aprobar los ingresos de afiliados para asegurar que solo se registren ventas legítimas. Esta guía le muestra cómo revisar comisiones pendientes, aprobar las válidas, rechazar las órdenes fraudulentas o devueltas, y gestionar eficientemente las comisiones mediante acciones en masa.

## Panel de comisiones

Navegue a **Marketing > Comisiones** para acceder al panel de gestión de comisiones.

El panel proporciona una visión general de la actividad de comisiones en todos los programas de afiliados:

| Estadística | Descripción |
|-------------|-------------|
| **Comisiones pendientes** | Número de comisiones que esperan su revisión |
| **Comisiones aprobadas** | Comisiones confirmadas y listas para el pago |
| **Comisiones pagadas** | Comisiones que se han pagado a los afiliados |
| **Comisiones rechazadas** | Comisiones rechazadas debido a fraude, devoluciones o violaciones de políticas |
| **Monto pendiente de pago** | Valor total de comisiones aprobadas pero no pagadas |

Estas estadísticas le ayudan a seguir su carga de trabajo de revisión y monitorear el impacto financiero de su programa de afiliados.

![Panel de comisiones](/static/core/admin/img/help/commission-management/commission-dashboard.webp)

## Ver comisiones

La lista de comisiones muestra todos los registros de comisiones en orden cronológico.

### Columnas de la lista

| Columna | Descripción |
|---------|-------------|
| **Afiliado** | Nombre y código único del afiliado |
| **Programa** | El programa de afiliados que generó esta comisión |
| **Orden** | Número de orden (haga clic para ver los detalles completos de la orden) |
| **Monto** | Valor de la comisión en la moneda de su tienda |
| **Estado** | Pendiente, Aprobada, Rechazada o Pagada |
| **Creada** | Cuando se generó la comisión |

### Filtros de comisiones

Use el panel lateral de filtros para reducir las comisiones:

- **Por estado** — Muestra solo comisiones pendientes, aprobadas, rechazadas o pagadas
- **Por afiliado** — Ver comisiones de un socio específico
- **Por programa** — Ver comisiones de un programa de afiliados específico
- **Por rango de fechas** — Filtrar por fecha de creación

### Búsqueda de comisiones

Use la barra de búsqueda para encontrar comisiones específicas:

- Ingrese un **número de orden** para encontrar una comisión para una venta específica
- Ingrese un **código de afiliado** para ver todas las comisiones de un socio

## Detalles de la comisión

Haga clic en cualquier comisión de la lista para ver sus detalles completos.

### Campos de detalles

La vista de detalles muestra:

- **Información de la orden** — Haga clic en el número de orden para ver la orden completa en una nueva pestaña, incluyendo artículos, dirección de envío, estado de pago y detalles del cliente
- **Información del afiliado** — Nombre, código, correo electrónico de pago y estado de membresía del programa del afiliado
- **Detalles del programa** — Nombre del programa, tipo de comisión (porcentaje o fijo) y tasa de comisión
- **Marcas de tiempo** — Fecha de creación, fecha de aprobación/rechazo y fecha de pago
- **Sección de notas** — Notas internas visibles solo para los vendedores (explicadas a continuación)

Esta información le ayuda a verificar la legitimidad de la comisión antes de aprobarla.

## Aprobar comisiones

Aprobar una comisión confirma que es válida y la agrega al saldo disponible del afiliado, haciéndola elegible para el pago.

### Cuándo aprobar

Aprobar comisiones cuando:

- **La orden se haya cumplido correctamente** — El producto se envió o los bienes digitales se entregaron
- **No haya devoluciones ni reembolsos** — El cliente no ha solicitado una devolución (considere esperar 14-30 días después del cumplimiento)
- **Se cumplan los estándares de calidad** — La venta cumple con los términos de su programa (por ejemplo, no es una auto-referencia, el cliente usó un método de pago auténtico)
- **No se detecte fraude** — La orden pasa por el análisis de fraude (verifique la IP, coincidencia de dirección de facturación/envío, patrones de orden inusuales)

### Cómo aprobar

**Aprobación de una sola comisión**:

1. Navegue a **Marketing > Comisiones**
2. Haga clic en la comisión que desea aprobar
3. Haga clic en el botón **Aprobar** en la parte superior de la página de detalles
4. Opcionalmente, agregue una nota (por ejemplo, "Aprobada después de la entrega exitosa")
5. El estado cambia a **Aprobada** y la comisión se agrega al saldo del afiliado

**Aprobación en masa**:

1. Navegue a **Marketing > Comisiones**
2. Marque las casillas junto a las comisiones que desea aprobar
3. Seleccione **Aprobar seleccionadas** del menú desplegable **Acciones**
4. Haga clic en **Ir**
5. Todas las comisiones seleccionadas cambian al estado **Aprobada**

Las comisiones aprobadas aparecen en el panel del afiliado como saldo disponible y pueden incluirse en el próximo lote de pagos.

## Rechazar comisiones

Rechazar una comisión la elimina del saldo del afiliado y la marca como no elegible para el pago.

### Cuándo rechazar

Rechazar comisiones cuando:

- **Orden fraudulenta** — La orden muestra signos de fraude (método de pago robado, coincidencia de IP, afiliado usando su propio enlace)
- **El cliente devolvió el producto** — El cliente devolvió los artículos para un reembolso total
- **Problemas de calidad** — La venta no cumple con los términos del programa (por ejemplo, el afiliado violó las directrices de publicidad)
- **Violación de términos** — El afiliado usó métodos de promoción prohibidos (correo no deseado, pujas de marcas, relleno de cookies)
- **Orden cancelada** — El cliente canceló antes del cumplimiento

### Cómo rechazar

**Rechazo de una sola comisión**:

1. Navegue a **Marketing > Commissions**
2. Haga clic en la comisión que desea rechazar
3. Haga clic en el botón **Reject** en la parte superior de la página de detalles
4. **Agregue una nota** explicando la razón (altamente recomendado para la resolución de disputas)
5. El estado cambia a **Rejected**

**Rechazo en masa**:

1. Navegue a **Marketing > Commissions**
2. Marque las casillas junto a las comisiones que desea rechazar
3. Seleccione **Reject Selected** del menú desplegable **Actions**
4. Haga clic en **Go**
5. Todas las comisiones seleccionadas cambian al estado **Rejected**

Las comisiones rechazadas se eliminan del saldo del afiliado y no pueden pagarse. Quedan visibles en el historial de comisiones para fines de registro.

## Acciones en masa

Las acciones en masa le permiten aprobar o rechazar múltiples comisiones a la vez, ahorrando tiempo al procesar lotes grandes.

### Usando acciones en masa

1. Navegue a **Marketing > Commissions**
2. Filtre la lista para mostrar solo las comisiones que desea procesar (por ejemplo, filtre por estado **Pending**)
3. Marque la casilla junto a cada comisión, o haga clic en la casilla del encabezado para seleccionar todas en la página actual
4. Elija una acción del menú desplegable **Actions**:
   - **Approve Selected** — Marque todas las comisiones seleccionadas como aprobadas
   - **Reject Selected** — Marque todas las comisiones seleccionadas como rechazadas
5. Haga clic en **Go**
6. Revise el mensaje de confirmación que muestra cuántas comisiones se actualizaron

### Procesamiento en masa eficiente

- **Filtrar por programa** — Aprobar todas las comisiones de un afiliado de confianza de alto rendimiento a la vez
- **Filtrar por rango de fechas** — Procesar comisiones anteriores a 14 días (fuera del período de devolución)
- **Revisar las de alto valor por separado** — Use acciones en masa para comisiones pequeñas, revise manualmente las de alto valor

## Notas de comisión

El campo de notas le permite documentar sus decisiones y comunicarse con su equipo.

### Agregar notas

Las notas se pueden agregar:

- **Durante la aprobación** — Haga clic en la comisión, agregue una nota en el campo de notas, luego haga clic en **Aprobar**
- **Durante el rechazo** — Agregue una nota explicando la razón del rechazo
- **Cualquier momento** — Haga clic en la comisión, agregue o edite la nota en el campo de notas y guárdela

### Cuándo usar notas

- **Comisiones rechazadas** — Documente siempre la razón ("El cliente devolvió el pedido #12345 el 2/10/26")
- **Comisiones de alto valor** — Nota los pasos de verificación tomados ("Verificado el envío mediante el número de seguimiento #ABC123")
- **Comisiones disputadas** — Documente la comunicación con el afiliado
- **Patrones de fraude** — Nota actividades sospechosas para referencia futura

Las notas son **solo internas** — los afiliados no pueden verlas. Sirven como su herramienta de registro.

## Flujo de comisión

Aquí está el flujo de trabajo completo de gestión de comisiones:

```
Orden Placed → Commission Created (Pending)
                      ↓
              Merchant Reviews
                      ↓
                ┌─────┴─────┐
                ↓           ↓
            Approved     Rejected
                ↓           ↓
        Ready for Payout  Not Payable
                ↓
        Included in Payout
                ↓
              Paid
```

**Ejemplo de cronograma**:

- **Día 1:** El cliente coloca un pedido de $100 a través de un enlace de afiliado → se crea una comisión de $10 (pendiente)
- **Día 15:** La orden se cumple y el período de devolución ha terminado → el vendedor aprueba la comisión
- **Día 20:** El vendedor procesa el lote mensual de pagos → el estado de la comisión cambia a Pagada
- **Día 21:** El afiliado recibe el pago a través de PayPal

## Mejores prácticas

### Ventana de revisión

Establezca un horario de revisión consistente:

- **Revisión diaria** — Procese las comisiones pendientes cada mañana (recomendado para programas de alto volumen)
- **Revisión semanal** — Reserve tiempo cada lunes para aprobar las comisiones de la semana anterior
- **Revisión quincenal** — Alinee con su horario de pagos (apruebe comisiones a mediados del mes, procese pagos al final del mes)

### Verificaciones de calidad

Antes de aprobar comisiones, verifique:

1. **La orden se ha cumplido** — Revise el estado de la orden en el panel de administración
2. **El pago se ha confirmado** — Verifique que el método de pago se haya procesado correctamente
3. **El período de devolución ha terminado** — Espere 14-30 días después de la entrega para tener en cuenta las devoluciones
4. **No hay banderas de fraude** — Revise la orden en busca de patrones sospechosos (direcciones no coincidentes, países de alto riesgo, múltiples órdenes desde la misma IP)
5. **El afiliado está en buen estado** — Revise el historial del afiliado para antecedentes de fraude o violaciones

### Prevención de fraude

Vigile estas banderas rojas:

- **Auto-referencias** — El afiliado colocando órdenes usando su propio enlace de seguimiento
- **Relleno de cookies** — Relación de clics a conversión anormalmente alta con valores de orden bajos
- **Órdenes duplicadas** — Múltiples órdenes desde el mismo cliente/IP a través del mismo enlace de afiliado
- **Mismatches de geolocalización** — Afiliado en el país A impulsando ventas exclusivamente en el país B
- **Cobros devueltos** — Tasa alta de cobros devueltos en órdenes referidas por afiliados

Si detecta fraude, **rechace las comisiones** y considere terminar la membresía del programa del afiliado.

### Comunicación con afiliados

- **Establezca expectativas** — Documente claramente su política de aprobación de comisiones en los términos del programa
- **Sé transparente** — Si rechaza comisiones, considere enviar un correo electrónico al afiliado explicando por qué (use las notas como referencia)
- **Responda a las disputas** — Si un afiliado cuestiona un rechazo, revise las notas y los detalles de la orden
- **Publique directrices** — Cree una página "Política de Aprobación de Comisiones" en su portal de afiliados para evitar confusiones

## Consejos

- Aprobar comisiones **después de que cierre el período de devolución** (normalmente 14-30 días) para evitar aprobar órdenes que los clientes devuelvan más tarde
- Use **acciones en masa con filtros** para procesar eficientemente comisiones de afiliados de confianza, mientras revisa manualmente nuevos o afiliados de alto riesgo
- Documente las razones de rechazo en el **campo de notas** — esto le protege si un afiliado discute la decisión y le ayuda a identificar patrones
- Vela por **auto-referencias** — es una violación común donde los afiliados usan sus propios enlaces para ganar comisiones en compras personales
- Establezca un **umbral mínimo de aprobación** — por ejemplo, aprobación automática de comisiones por debajo de $10 pero revisación manual de cualquier monto superior a $50 para equilibrar eficiencia con riesgo
- Cree una **lista de banderas de fraude** — estandarice su proceso de revisión con una lista de banderas rojas (mismatches de IP, patrones de órdenes sospechosos, métodos de pago de alto riesgo)
- Monitorea **tasas de rechazo por afiliado** — si un afiliado tiene muchas rechazos, puede indicar fraude o la necesidad de capacitación adicional sobre los términos del programa

Recuerde: Preserve all markdown formatting, image paths, code blocks, and technical terms exactly as shown in the preservation rules.