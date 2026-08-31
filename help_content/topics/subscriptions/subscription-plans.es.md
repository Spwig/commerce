---
title: Planes de suscripción
---

Los planes de suscripción le permiten ofrecer facturación recurrente para sus productos: ideal para artículos de consumo, servicios, cajas curadas o cualquier producto que los clientes compren repetidamente. Esta guía explica cómo crear y configurar planes, establecer niveles de precios, agregar períodos de prueba y adjuntar complementos opcionales.

## Comenzando

Navegue hasta **Suscripciones > Planes de suscripción** en la barra lateral de administración. La lista de planes muestra todos sus planes con su modelo de precios, cantidad de suscriptores activos y estado de visibilidad.

![Lista de planes de suscripción](/static/core/admin/img/help/subscription-plans/plan-list.webp)

Para crear un nuevo plan, haga clic en el botón **Crear con asistente** - esto abre el asistente para crear el plan, que lo guía paso a paso. El botón **+ Añadir plan** junto a él abre un formulario en blanco para los comerciantes que prefieren configurar todo manualmente en su lugar.

Un plan por sí solo no es comprable: es una plantilla. Una vez que lo haya construido aquí, ájelo a uno o más productos desde la pestaña **Suscripciones** del producto (únicamente para productos simples, variables y digitales), para que los clientes puedan suscribirse realmente. Vea [Vender productos como suscripciones](/help/selling-products-as-subscriptions) para ese paso.

## El editor de planes

Abrir un plan existente (haciendo clic en su nombre o en el icono del lápiz, desde la lista) lo lleva al editor de planes. El encabezado muestra el nombre del plan, su modelo de precios, las etiquetas de estado **Activo**/**Inactivo** y **Público**/**Privado**, y la fecha en que fue creado. Los dos botones en la esquina superior derecha del encabezado guardan sus cambios: el icono de círculo verde guarda y regresa a la lista, el icono de verificación guarda y le permite continuar editando.

Debajo del encabezado, una cinta de estadísticas resume el plan a simple vista: **Suscripciones activas**, **Niveles de precios**, **Complementos** y **Ingresos totales**.

El resto del formulario está organizado en cinco pestañas:

| Pestaña | Qué contiene |
|-----|-------------------|
| **General** | Información del plan (nombre, slug, descripción) y Estado (activo/público) |
| **Precios** | Configuración de precios, período de prueba y límites y restricciones |
| **Niveles y complementos** | Editores de niveles de precios y complementos |
| **Ciclo de vida** | Política de cancelación y comportamiento de cambio de plan |
| **Avanzado** | Integración del proveedor y estadísticas |

Las secciones siguientes recorren la configuración de cada pestaña. Al crear un nuevo plan directamente desde **+ Añadir plan** (en lugar del asistente), los mismos campos aparecen en un solo formulario desplazable en lugar de pestañas: guarde el plan una vez y vuélvalo a abrir para obtener el editor con pestañas completo.

## Información del plan (pestaña General)

La tarjeta **Información del plan** captura la identidad principal de su plan.

- **Nombre del plan** - El nombre que ven los clientes al suscribirse. Haga clic en el icono del globo para agregar traducciones para otros idiomas de la tienda.
- **Slug** - Un identificador amigable para URL generado automáticamente a partir del nombre (por ejemplo, `plan-premium`). Se utiliza internamente y en integraciones.
- **Descripción** - Texto opcional describiendo qué incluye el plan. Soporta traducciones.

El card **Estado** en la misma pestaña controla los interruptores **Activo** y **Público** - véase [Visibilidad y estado](#visibilidad-y-estado) a continuación.

![Pestaña General del editor de planes](/static/core/admin/img/help/subscription-plans/edit-form-general-tab.webp)

## Modelo de precios (pestaña Precios)

La tarjeta **Configuración de precios** controla cómo se estructura el precio para este plan:

| Modelo de precios | Lo mejor para |
|---------------|----------|
| **Precios por niveles** | Ofrecer opciones de compromiso mensuales, trimestrales y anuales con descuentos para términos más largos |
| **Basado en cantidad** | Precios por asiento o usuario donde el total varía con la cantidad (por ejemplo, licencias por equipo) |
| **Tarifa plana** | Un precio fijo único sin variaciones |

Para planes **Basados en cantidad**, marque **Permitir cantidad** y establezca la **Cantidad mínima** (número mínimo de asientos requeridos) y opcionalmente una **Cantidad máxima** para limitar cuántos asientos puede comprar un suscriptor.

Preserve all markdown formatting, image paths, code blocks, and technical terms.

[![](https://spwig.com/static/core/admin/img/help/subscription-plans/edit-form-pricing-tab.webp)](/static/core/admin/img/help/subscription-plans/edit-form-pricing-tab.webp)

## Tarifas de precios (pestaña Tarifas y complementos)

Las tarifas de precios definen la frecuencia de facturación y las opciones de descuento disponibles para los clientes en este plan. Agréguelas en la tarjeta **Tarifas de precios** de la pestaña **Tarifas y complementos**, junto con el editor de complementos.

Cada tarifa tiene estos campos:

- **Nombre de la tarifa** — La etiqueta que se le muestra al cliente (por ejemplo, `Mensual`, `Anual - Ahorra 20%`). Soporta traducciones.
- **Ciclo de facturación** — Con qué frecuencia se cobra al cliente: Diario, Semanal, Mensual, Trimestral, Semestral o Anual.
- **Intervalo de facturación** — El multiplicador del ciclo de facturación. Establezca en `2` con Mensual para facturar cada 2 meses.
- **Porcentaje de descuento** — El descuento aplicado al precio del producto para esta tarifa. Establezca en `0` para el precio completo, o en `20` para dar un 20% de descuento. Este descuento se aplica sobre cualquier precio de venta en el propio producto.
- **Tarifa predeterminada** — Marque una tarifa como predeterminada para seleccionarla automáticamente para los clientes cuando vean las opciones de suscripción.

El descuento se aplica desde el primer ciclo de facturación del cliente, no solo en renovaciones — una tarifa con un 20% de descuento cobra 20% menos desde el primer día (o desde la primera factura después de una prueba, si el plan tiene una).

### Ejemplo: plan con tres opciones

Para un plan de suscripción "Club de café":

| Nombre de la tarifa | Ciclo de facturación | Descuento |
|-----------|---------------|----------|
| Mensual | Mensual | 0% |
| Trimestral - Ahorra 10% | Trimestral | 10% |
| Anual - Ahorra 20% | Anual | 20% |

## Complementos del plan (pestaña Tarifas y complementos)

Los complementos son extras opcionales que los suscriptores pueden adjuntar a su plan. Agréguelos en la tarjeta **Complementos**, directamente debajo de las tarifas en la misma pestaña:

- **Nombre del complemento** — El nombre que se le muestra al cliente. Soporta traducciones.
- **Descripción** — Qué ofrece el complemento.
- **Precio** — Costo del complemento.
- **Frecuencia de facturación** — Si el complemento se cobra **Por ciclo de facturación** (recurrente) o **Una vez** al inicio de la suscripción.
- **Permitir cantidad** — Active para permitir que los clientes compren múltiples unidades del complemento.
- **Requerido** — Marque para incluir automáticamente el complemento en todas las nuevas suscripciones. Los complementos requeridos no se pueden eliminar por el cliente.

[![](https://spwig.com/static/core/admin/img/help/subscription-plans/edit-form-tiers-addons-tab.webp)](/static/core/admin/img/help/subscription-plans/edit-form-tiers-addons-tab.webp)

## Período de prueba (pestaña de precios)

Un período de prueba permite a los clientes probar su suscripción antes de su primera factura completa. Configure esto en la tarjeta **Período de prueba**, debajo de **Configuración de precios**:

- **Período de prueba (días)** — Número de días de prueba gratuitos. Establezca en `0` para deshabilitar las pruebas. El máximo es 365 días.
- **Precio de prueba** — Precio reducido opcional durante la prueba (por ejemplo, $1 por el primer mes). Deje en blanco para una prueba completamente gratuita.

## Límites y restricciones (pestaña de precios)

La tarjeta **Límites y restricciones**, también en la pestaña de precios, contiene:

- **Máximo de ciclos de facturación** — Número total de ciclos de facturación antes de que la suscripción finalice automáticamente. Deje en blanco para facturación recurrente ilimitada. Útil para planes de cuotas o suscripciones con plazo limitado.

**Tarifa de configuración** y **Orden de clasificación** no forman parte de esta tarjeta — se establecen una vez, cuando crea por primera vez el plan a través del flujo **Crear con asistente**, y no se pueden cambiar desde la pantalla de edición posteriormente. Si necesita ajustar alguno de estos valores, desactive el plan y créelo nuevamente con el asistente en lugar de editar el existente. Tenga en cuenta que las tarifas de configuración aún no se cobran automáticamente en el momento de la compra en esta versión — trátelo como un campo reservado para una actualización futura en lugar de un cargo funcional.

## Política de cancelación (pestaña de ciclo de vida)

Controle cómo los clientes pueden cancelar su suscripción en la tarjeta **Política de cancelación**.

{"| Policy | Description |\n|--------|-------------|\n| **Cancel Anytime** | Los clientes pueden cancelar inmediatamente en cualquier momento |\n| **Cancel at Period End** | La cancelación surtirá efecto al final del período pagado — los clientes tendrán acceso hasta la fecha de vencimiento |\n| **Minimum Commitment Required** | Los clientes deben completar un número mínimo de ciclos de facturación antes de cancelar |\n|\nAdditional settings:|\n|\n- **Minimum Commitment (Cycles)** — Al usar la política de compromiso, establezca el número requerido de ciclos de facturación (por ejemplo, `3` para un mínimo de 3 meses).|\n- **Grace Period (Days)** — Días de acceso continuo después de un fallo de pago antes de que la suscripción se suspenda. Establezca en `0` para suspensión inmediata.|\n- **Reactivation Period (Days)** — Días después de la cancelación durante los cuales un cliente puede reactivar su suscripción sin volver a suscribirse desde cero.|\n|\n## Plan change behavior (Lifecycle tab)|\n|\nLa tarjeta **Plan Change Behavior**, debajo de **Cancellation Policy**, controla qué ocurre cuando los clientes actualizan o reducen sus planes:|\n|\n- **Upgrade Behavior** — Establezca en **Immediate** (cobrar la cantidad proporcional ahora) o **At Renewal** (cambiar en la fecha de facturación siguiente).|\n- **Downgrade Behavior** — Establezca en **Immediate** (aplicar crédito a la próxima factura) o **At Renewal** (cambiar en la fecha de facturación siguiente).|\n|\n![Lifecycle tab of the plan editor](/static/core/admin/img/help/subscription-plans/edit-form-lifecycle-tab.webp)|\n|\n## Advanced tab|\n|\nLa pestaña **Advanced** contiene configuraciones que rara vez necesita día a día:|\n|\n- **Provider Integration** — Asigne este plan a identificadores de planes/precios de sus proveedores de pago (por ejemplo, `"stripe": "price_xxx", "paypal": "P-xxx"`), para tiendas que gestionen sus suscripciones directamente a través del proveedor en lugar del motor de facturación propio de Spwig.|\n- **Statistics** — Figuras de solo lectura: **Active Subscriptions**, **Total Revenue**, y las fechas de creación y actualización del plan. Estas figuras reflejan las estadísticas en la parte superior de la página.|\n|\n![Advanced tab of the plan editor](/static/core/admin/img/help/subscription-plans/edit-form-advanced-tab.webp)|\n|\n## Visibility and status (General tab)|\n|\n- **Active** — Desmarque para desactivar un plan para que no se puedan crear nuevas suscripciones. Las suscripciones existentes no se verán afectadas.|\n- **Public** — Desmarque para ocultar el plan de las páginas visibles para los clientes (útil para planes internos o legados que los suscriptores existentes mantengan).|\n|\n## Tips|\n|\n- Use un **periodo de prueba** para reducir la duda — incluso una prueba gratuita de 7 días puede mejorar significativamente las tasas de conversión en productos con suscripción.|\n- Configure **tres niveles de precios** (mensual, trimestral, anual) con descuentos crecientes para fomentar los compromisos anuales y mejorar su flujo de efectivo.|\n- Para suscripciones basadas en servicios, establezca **Cancellation Policy** en **Cancel at Period End** para que los clientes tengan acceso a través de su período pagado — esto parece justo y reduce los reembolsos.|\n- Mantenga el **Grace Period** entre 3-7 días para fallos en el pago. Esto da tiempo a los clientes para actualizar su método de pago antes de perder el acceso.|\n- Use la bandera **Required** en complementos con moderación — úselo solo para cosas que sean genuinamente obligatorias (por ejemplo, un acuerdo de servicio), no como forma de inflar los precios.|n- Desactive los planes sin suscriptores en lugar de eliminarlos — esto preserva los datos históricos para cualquier cliente que anteriormente se haya suscrito."}