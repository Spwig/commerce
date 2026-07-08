---
title: Planes de suscripción
---

Los planes de suscripción le permiten ofrecer facturación recurrente para sus productos — ideal para productos de consumo, servicios, cajas curadas o cualquier producto que los clientes compren repetidamente. Esta guía explica cómo crear y configurar planes, establecer niveles de precios, agregar períodos de prueba y adjuntar complementos opcionales.

## Comenzando

Navegue hasta **Suscripciones > Planes de suscripción** en el menú lateral de administración. La lista de planes muestra todos sus planes con su modelo de precios, cantidad de suscriptores activos y estado de visibilidad.

Para crear un nuevo plan, haga clic en el botón **+ Agregar plan de suscripción** — esto abre el asistente de creación de planes, que le guía paso a paso en la configuración.

![Lista de planes de suscripción](/static/core/admin/img/help/subscription-plans/plan-list.webp)

## Información del plan

La primera sección captura la identidad central de su plan.

- **Nombre del plan** — El nombre que ven los clientes al suscribirse. Haga clic en el icono de globo para agregar traducciones para otros idiomas del almacén.
- **Slug** — Un identificador amigable para URLs generado automáticamente a partir del nombre (por ejemplo, `premium-plan`). Se usa internamente y en integraciones.
- **Descripción** — Texto opcional que describe qué incluye el plan. Soporta traducciones.

## Modelo de precios

Elija cómo se estructura el precio para este plan:

| Modelo de precios | Mejor para |
|------------------|------------|
| **Precios por tramos** | Ofrecer opciones de compromiso mensual, trimestral y anual con descuentos por términos más largos |
| **Basado en cantidad** | Precios por plaza o por usuario donde el total escala con la cantidad (por ejemplo, licencias para equipos) |
| **Tarifa fija** | Un precio fijo único sin variaciones |

Para los planes **Basado en cantidad**, establezca la **Cantidad mínima** (número mínimo de plazas requerido) y opcionalmente una **Cantidad máxima** para limitar cuántas plazas puede comprar un suscriptor.

## Niveles de precios

Los niveles de precios definen la frecuencia de facturación y las opciones de descuento disponibles para los clientes en este plan. Agregue los niveles en la sección **Niveles de precios** debajo del formulario principal.

Cada nivel tiene estos campos:

- **Nombre del nivel** — La etiqueta mostrada a los clientes (por ejemplo, `Mensual`, `Anual — Ahorro del 20%`). Soporta traducciones.
- **Ciclo de facturación** — Con qué frecuencia se cobra al cliente: Diario, Semanal, Mensual, Trimestral, Semestral o Anual.
- **Intervalo de facturación** — El multiplicador del ciclo de facturación. Establezca en `2` con Mensual para facturar cada 2 meses.
- **Porcentaje de descuento** — El descuento aplicado al precio del producto para este nivel. Establezca en `0` para el precio completo, o `20` para un descuento del 20%. Este descuento se aplica encima de cualquier precio de venta del producto en sí.
- **Nivel predeterminado** — Marque un nivel como predeterminado para que se seleccione automáticamente para los clientes cuando vean las opciones de suscripción.

### Ejemplo: plan por tramos con tres opciones

Para un plan de suscripción "Club de café":

| Nombre del nivel | Ciclo de facturación | Descuento |
|------------------|----------------------|-----------|
| Mensual | Mensual | 0% |
| Trimestral — Ahorro del 10% | Trimestral | 10% |
| Anual — Ahorro del 20% | Anual | 20% |

## Período de prueba

Un período de prueba le permite a los clientes probar su suscripción antes de su primera carga completa. Configure esto en la sección **Período de prueba**:

- **Período de prueba (días)** — Número de días de prueba gratuitos. Establezca en `0` para deshabilitar los períodos de prueba. Máximo es 365 días.
- **Precio de prueba** — Precio reducido opcional durante el período de prueba (por ejemplo, $1 por el primer mes). Deje vacío para un período de prueba completamente gratuito.

## Política de cancelación

Controle cómo los clientes pueden cancelar su suscripción en la sección **Política de cancelación**:

| Política | Descripción |
|----------|-------------|
| **Cancelar en cualquier momento** | Los clientes pueden cancelar inmediatamente en cualquier momento |
| **Cancelar al final del período** | La cancelación se aplica al final del período pagado — los clientes mantienen el acceso hasta la expiración |
| **Requerimiento de compromiso mínimo** | Los clientes deben completar un número mínimo de ciclos de facturación antes de cancelar |

Configuraciones adicionales:

- **Commitimiento mínimo (Ciclos)** — Al usar la política de compromiso, establezca el número requerido de ciclos de facturación (por ejemplo, `3` para un compromiso mínimo de 3 meses).
- **Periodo de gracia (Días)** — Días de acceso continuo después de un fracaso en el pago antes de que se suspenda la suscripción.

Establezca en `0` para suspensión inmediata.
- **Periodo de reactivación (Días)** — Días después de la cancelación durante los cuales un cliente puede reactivar su suscripción sin volver a suscribirse desde el principio.

## Comportamiento al cambiar de plan

Cuando los clientes actualicen o degraden entre planes, puede controlar cuándo surta efecto el cambio:

- **Comportamiento de actualización** — Establezca en **Inmediato** (cargue el monto proporcional ahora) o **En la renovación** (cambie en la fecha de facturación siguiente).
- **Comportamiento de degradación** — Establezca en **Inmediato** (aplique el crédito en la próxima factura) o **En la renovación** (cambie en la fecha de facturación siguiente).

## Límites y restricciones

- **Ciclos de facturación máximos** — El número total de ciclos de facturación antes de que la suscripción termine automáticamente. Deje vacío para facturación recurrente ilimitada. Útil para planes de cuotas o suscripciones con límite de tiempo.
- **Tarifa de configuración** — Una tarifa única cobrada cuando se crea por primera vez la suscripción (por ejemplo, tarifa de onboarding o activación). Establezca en `0.00` para no tener tarifa de configuración.

## Complementos del plan

Los complementos son extras opcionales que los suscriptores pueden adjuntar a su plan. Agregue los complementos en la sección **Complementos del plan**:

- **Nombre del complemento** — El nombre mostrado a los clientes. Soporta traducciones.
- **Descripción** — Qué ofrece el complemento.
- **Precio** — Costo del complemento.
- **Frecuencia de facturación** — Si el complemento se cobra **Por ciclo de facturación** (recurrente) o **Una sola vez** al iniciar la suscripción.
- **Permitir cantidad** — Active para permitir que los clientes compren múltiples unidades del complemento.
- **Requerido** — Marque esto para incluir automáticamente el complemento en todas las nuevas suscripciones. Los complementos requeridos no pueden ser eliminados por el cliente.

## Visibilidad y estado

- **Activo** — Desactive para desactivar un plan, de modo que no se puedan crear nuevas suscripciones. Las suscripciones existentes no se ven afectadas.
- **Público** — Desactive para ocultar el plan de las páginas orientadas al cliente (útil para planes internos o heredados en los que los suscriptores existentes siguen estando inscritos).
- **Orden de clasificación** — Controla el orden de visualización en las páginas de selección de suscripción. Los números más bajos aparecen primero.

## Consejos

- Use un **periodo de prueba** para reducir la hesitación, incluso un corto periodo de prueba gratuito de 7 días puede mejorar significativamente las tasas de conversión en productos de suscripción.
- Establezca **tres niveles de precios** (mensual, trimestral, anual) con descuentos progresivos para fomentar compromisos anuales y mejorar su flujo de efectivo.
- Para suscripciones basadas en servicios, establezca **Política de cancelación** en **Cancelar al final del período** para que los clientes mantengan el acceso durante su período pagado — esto parece justo y reduce los cobros por incumplimiento.
- Mantenga el **periodo de gracia** entre 3 y 7 días para fracasos en el pago. Esto da a los clientes tiempo para actualizar su método de pago antes de perder el acceso.
- Use la bandera **Requerido** en los complementos con moderación — úsela solo para cosas que sean verdaderamente obligatorias (por ejemplo, un acuerdo de servicio), no como forma de inflar el precio.
- Desactive los planes sin suscriptores en lugar de eliminarlos — esto preserva los datos históricos para cualquier cliente que haya suscrito anteriormente.