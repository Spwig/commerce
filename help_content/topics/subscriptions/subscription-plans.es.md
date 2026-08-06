---
title: Suscripciones
---

Los planes de suscripción le permiten ofrecer facturación recurrente para sus productos: ideal para artículos de consumo, servicios, cajas curadas o cualquier producto que los clientes compren repetidamente. Esta guía explica cómo crear y configurar planes, establecer niveles de precios, agregar períodos de prueba y adjuntar complementos opcionales.

## Comenzando

Navegue hasta **Suscripciones > Planes de suscripción** en la barra lateral de administración. La lista de planes muestra todos sus planes con su modelo de precios, cantidad de suscriptores activos y estado de visibilidad.

Para crear un nuevo plan, haga clic en el botón **+ Añadir plan de suscripción** - esto abre el asistente para crear el plan, que lo guía paso a paso.

![Lista de planes de suscripción](/static/core/admin/img/help/subscription-plans/plan-list.webp)

Un plan por sí solo no es comprable: es una plantilla. Una vez que lo haya construido aquí, ájelo a uno o más productos desde la pestaña **Suscripciones** del producto (únicamente para productos simples, variables y digitales), para que los clientes puedan suscribirse realmente. Vea [Vender productos como suscripciones](/help/selling-products-as-subscriptions) para ese paso.

## Información del plan

La primera sección captura la identidad principal de su plan.

- **Nombre del plan** - El nombre que ven los clientes al suscribirse. Haga clic en el icono del globo para agregar traducciones para otros idiomas de la tienda.
- **Slug** - Un identificador amigable para URL generado automáticamente a partir del nombre (por ejemplo, `plan-premium`). Se utiliza internamente y en integraciones.
- **Descripción** - Texto opcional que describe qué incluye el plan. Soporta traducciones.

## Modelo de precios

Elija cómo se estructura el precio para este plan:

| Modelo de precios | Ideal para |
|------------------|------------|
| **Precios por niveles** | Ofrecer opciones de compromiso mensual, trimestral y anual con descuentos para términos más largos |
| **Basado en cantidad** | Precios por asiento o usuario donde el total varía con la cantidad (por ejemplo, licencias para equipos) |
| **Tarifa fija** | Un precio fijo único sin variaciones |

Para planes **Basados en cantidad**, establezca la **Cantidad mínima** (número mínimo de asientos requeridos) y opcionalmente una **Cantidad máxima** para limitar cuántos asientos puede comprar un suscriptor.

## Niveles de precios

Los niveles de precios definen la frecuencia de facturación y las opciones de descuento disponibles para los clientes en este plan. Agregue los niveles en la sección **Niveles de precios** que aparece debajo del formulario principal.

Cada nivel tiene estos campos:

- **Nombre del nivel** - La etiqueta que se le muestra al cliente (por ejemplo, `Mensual`, `Anual - Ahorra 20%`). Soporta traducciones.
- **Ciclo de facturación** - Con qué frecuencia se cobra al cliente: Diario, Semanal, Mensual, Trimestral, Semestral o Anual.
- **Intervalo de facturación** - El multiplicador del ciclo de facturación. Establezca en `2` con Mensual para facturar cada 2 meses.
- **Porcentaje de descuento** - El descuento aplicado al precio del producto para este nivel. Establezca en `0` para el precio completo, o en `20` para dar un 20% de descuento. Este descuento se aplica sobre cualquier precio de venta que tenga el producto en sí mismo.
- **Nivel predeterminado** - Marque un nivel como predeterminado para seleccionarlo automáticamente para los clientes cuando vean las opciones de suscripción.

El descuento se aplica desde el primer ciclo de facturación del cliente, no solo en renovaciones: un nivel con un descuento del 20% cobra un 20% menos desde el primer día (o desde la primera factura después de una prueba, si el plan tiene una).

### Ejemplo: plan con tres opciones de niveles

Para un plan de suscripción "Club de Café":

| Nombre del nivel | Ciclo de facturación | Descuento |
|------------------|----------------------|-----------|
| Mensual | Mensual | 0% |
| Trimestral - Ahorra 10% | Trimestral | 10% |
| Anual - Ahorra 20% | Anual | 20% |

## Período de prueba

Un período de prueba le permite a los clientes probar su suscripción antes de su primer cargo completo. Configure esto en la sección **Período de prueba**:

- **Período de prueba (días)** - Número de días de prueba gratuitos. Establezca en `0` para desactivar las pruebas. El máximo es 365 días.
- **Precio de prueba** - Precio reducido opcional durante la prueba (por ejemplo, $1 por el primer mes). Deje en blanco para una prueba completamente gratuita.

## Política de cancelación

Controle cómo los clientes pueden cancelar su suscripción en la sección **Política de cancelación**:

| Política | Descripción |
|--------|-------------|
| **Cancelar en cualquier momento** | Los clientes pueden cancelar inmediatamente en cualquier momento |
| **Cancelar al final del período** | La cancelación surte efecto al final del período pagado — los clientes mantienen el acceso hasta la fecha de vencimiento |
| **Se requiere compromiso mínimo** | Los clientes deben completar un número mínimo de ciclos de facturación antes de cancelar |

Ajustes adicionales:

- **Compromiso mínimo (ciclos)** — Al usar la política de compromiso, establezca el número requerido de ciclos de facturación (por ejemplo, `3` para un mínimo de 3 meses).
- **Período de gracia (días)** — Días de acceso continuo después de un fallo en el pago antes de que la suscripción se suspenda. Establezca en `0` para suspensión inmediata.
- **Período de reactivación (días)** — Días después de la cancelación durante los cuales un cliente puede reactivar su suscripción sin volver a suscribirse desde cero.

## Comportamiento de cambio de plan

Cuando los clientes actualizan o reducen sus planes, puede controlar cuándo se produce el cambio:

- **Comportamiento de actualización** — Establezca en **Inmediato** (cobrar una cantidad proporcional ahora) o **En la renovación** (cambiar en la fecha de facturación siguiente).
- **Comportamiento de reducción** — Establezca en **Inmediato** (aplicar crédito en la siguiente factura) o **En la renovación** (cambiar en la fecha de facturación siguiente).

## Límites y restricciones

- **Máximo de ciclos de facturación** — Número total de ciclos de facturación antes de que la suscripción finalice automáticamente. Deje en blanco para facturación recurrente ilimitada. Útil para planes de cuotas o suscripciones con plazo limitado.
- **Tarifa de configuración** — Un cargo único que se recoge cuando se crea por primera vez la suscripción (por ejemplo, tarifa de puesta en marcha o activación). Establezca en `0.00` para no tener tarifa de configuración.

## Complementos de plan

Los complementos son extras opcionales que los suscriptores pueden adjuntar a su plan. Agréguelos en la sección **Complementos de plan**:

- **Nombre del complemento** — El nombre que se muestra a los clientes. Soporta traducciones.
- **Descripción** — Qué proporciona el complemento.
- **Precio** — Costo del complemento.
- **Frecuencia de facturación** — Si el complemento se cobra **Por ciclo de facturación** (recurrente) o **Una vez** al inicio de la suscripción.
- **Permitir cantidad** — Active para permitir que los clientes compren múltiples unidades del complemento.
- **Requerido** — Marque esta opción para incluir automáticamente el complemento en todas las suscripciones nuevas. Los complementos requeridos no se pueden eliminar por el cliente.

## Visibilidad y estado

- **Activo** — Desmarque para desactivar un plan para que no se puedan crear nuevas suscripciones. Las suscripciones existentes no se ven afectadas.
- **Público** — Desmarque para ocultar el plan de las páginas visibles para los clientes (útil para planes internos o antiguos que los suscriptores existentes permanezcan en ellos).
- **Orden de clasificación** — Controla el orden de visualización en las páginas de selección de suscripción. Los números más bajos aparecen primero.

## Consejos

- Use un **período de prueba** para reducir la duda — incluso una prueba gratuita de 7 días puede mejorar significativamente las tasas de conversión en productos de suscripción.
- Configure **tres niveles de precios** (mensual, trimestral, anual) con descuentos crecientes para fomentar los compromisos anuales y mejorar su flujo de efectivo.
- Para suscripciones basadas en servicios, establezca **Política de cancelación** en **Cancelar al final del período** para que los clientes conserven el acceso durante su período pagado — esto parece justo y reduce los reembolsos.
- Mantenga el **Período de gracia** entre 3-7 días para fallos en el pago. Esto da tiempo a los clientes para actualizar su método de pago antes de perder el acceso.
- Use la **bandera Requerido** en complementos con moderación — úselo solo para cosas que sean genuinamente obligatorias (por ejemplo, un acuerdo de servicio), no como forma de inflar los precios.
- Desactive los planes sin suscriptores en lugar de eliminarlos — esto preserva los datos históricos para cualquier cliente que anteriormente se haya suscrito.