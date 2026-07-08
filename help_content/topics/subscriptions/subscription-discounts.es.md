---
title: Descuentos de suscripción
---

Los descuentos de suscripción le permiten aplicar reducciones de precio a suscripciones individuales de clientes — por ejemplo, recompensar a suscriptores leales, honrar un cupón promocional o resolver un desacuerdo de facturación con un crédito de buena voluntad. A diferencia de los niveles de precios a nivel de plan, estos descuentos se aplican directamente a una suscripción específica.

## Ver descuentos de suscripción

Navegue hasta **Suscripciones > Descuentos de Suscripción** para ver todos los descuentos actualmente aplicados a sus suscripciones.

Cada entrada muestra la suscripción a la que pertenece, el tipo y valor del descuento, cuánto tiempo dura el descuento y si aún está activo.

También puede encontrar descuentos adjuntos a una suscripción específica abriendo **Suscripciones > Suscripciones de Cliente**, haciendo clic en una suscripción y desplazándose hasta la sección **Descuentos** en la parte inferior de la página de detalles.

## Añadir un descuento a una suscripción

Para añadir un nuevo descuento:

1. Navegue hasta **Suscripciones > Descuentos de Suscripción**
2. Haga clic en **+ Añadir Descuento de Suscripción**
3. Seleccione la **Suscripción** a la que desea aplicar el descuento
4. Configure la configuración del descuento (descrito a continuación)
5. Haga clic en **Guardar**

El descuento tomará efecto en el próximo ciclo de facturación.

## Tipos de descuento

Elija cómo se calcula el descuento:

| Tipo de Descuento | Cómo funciona | Ejemplo |
|------------------|----------------|---------|
| **Porcentaje de descuento** | Reduce la factura en un porcentaje | `20` reduce una factura de $50 a $40 |
| **Monto fijo de descuento** | Resta un monto fijo de la factura | `10` reduce una factura de $50 a $40 |
| **Precio fijo de reemplazo** | Establece la suscripción a un precio específico, independientemente del precio normal del plan | `29` establece la factura en $29/ciclo |

Establezca el campo **Valor del Descuento** en el número correspondiente al tipo de descuento elegido (porcentaje, monto en dólares o precio fijo).

### Ejemplo: oferta de retención

Un cliente se contacta con usted deseando cancelar. Le ofrece 3 meses con un descuento del 25% para que se quede:

| Campo | Valor |
|-------|-------|
| Tipo de Descuento | Porcentaje de descuento |
| Valor del Descuento | `25` |
| Tipo de Duración | Repetitivo |
| Duración (Meses) | `3` |

## Duración del descuento

Controla cuánto tiempo el descuento se aplica a los ciclos de facturación futuros:

| Tipo de Duración | Cuándo se aplica |
|------------------|------------------|
| **Aplicar una vez** | Reduce solo el cargo del próximo ciclo de facturación, luego expira automáticamente |
| **Para siempre** | Se aplica a cada ciclo de facturación futuro hasta que se desactive manualmente |
| **Repetitivo** | Se aplica durante un número establecido de meses, luego expira |

Para descuentos **Repetitivos**, establezca el campo **Duración (Meses)** en el número de meses que debe durar el descuento. El campo **Ciclos Restantes** registra cuántos ciclos quedan — se cuenta hacia abajo con cada ciclo de facturación.

## Códigos de cupón

Si el descuento fue desencadenado por un código promocional, ingréselo en el campo **Código de Cupón**. Esto es informativo — registra de dónde provino el descuento para su propio seguimiento.

## Desactivar un descuento

Para detener un descuento antes de que expire naturalmente, abra el registro del descuento y desmarque la casilla **Activo**, luego guárdelo. El descuento ya no se aplicará a los ciclos de facturación futuros. La suscripción regresará a su precio normal del plan en el próximo ciclo de facturación.

También puede establecer una fecha **Vence en** al crear el descuento — el sistema desactivará automáticamente el descuento después de esa fecha.

## Consejos

- Use descuentos **Aplicar una vez** para gestos de buena voluntad puntuales (por ejemplo, compensar a un suscriptor por un corte de servicio).

Son limpios y se expiran solos.
- Los descuentos **Porcentaje de descuento** son más seguros que los **Monto fijo de descuento** para suscripciones con precios variables, ya que el descuento se ajusta según el monto real de la factura.
- Cuando ofrezca una oferta de retención, use **Repetitivo** con una duración de 3 meses — le da a los clientes una razón para quedarse sin reducir permanentemente sus ingresos.
- Mantenga el campo **Código de Cupón** consistente con el código que usaron los clientes.

# Facilita la auditoría de qué promociones generaron qué descuentos al revisar tus ingresos por suscripciones.
- Los descuentos se aplican a suscripciones individuales, no a planes.

Si deseas reducir el precio de un plan para todos los nuevos suscriptores, actualiza los niveles de precios del plan en su lugar.