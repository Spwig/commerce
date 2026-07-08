---
title: Ejemplos de cupones
---

Esta guía proporciona ejemplos concretos, campo por campo, para los tipos de cupones más comunes. Cada ejemplo muestra exactamente qué ingresar cuando se cree un cupón en **Marketing > Cupones** → **+ Agregar cupón**.

![Tarjeta de cupón](/static/core/admin/img/help/voucher-examples/voucher-card.webp)

## Ejemplo 1: Descuento porcentaje con límite máximo

**Escenario:** Ofrecer un 20% de descuento en todo el carrito, pero limitar el descuento a $50 para mantener las órdenes de alto valor rentables. Sin fecha de vencimiento.

| Campo | Valor |
|-------|-------|
| Código | `SAVE20` |
| Nombre | 20% de descuento — Máximo $50 |
| Tipo de descuento | Porcentaje |
| Valor del descuento | 20 |
| Monto máximo de descuento | 50 |
| Alcance de aplicación | Todo el carrito |
| Uso máximo total | *(vacío — ilimitado)* |
| Uso máximo por cliente | 1 |
| Valor mínimo de la orden | *(vacío — sin mínimo)* |

**Cómo funciona el límite:** En una orden de $200 el descuento es de $40. En una orden de $300 sería de $60, pero el límite lo reduce a $50. En una orden de $500 el descuento sigue siendo de $50. Esto le permite realizar una promoción que suene generosa, mientras mantiene el descuento real predecible.

## Ejemplo 2: Descuento fijo con mínimo

**Escenario:** Ofrecer $10 de descuento en cualquier orden superior a $75 para fomentar carritos más grandes.

| Campo | Valor |
|-------|-------|
| Código | `TAKE10` |
| Nombre | $10 de descuento en pedidos superiores a $75 |
| Tipo de descuento | Monto fijo |
| Valor del descuento | 10 |
| Alcance de aplicación | Todo el carrito |
| Valor mínimo de la orden | 75 |
| Uso máximo por cliente | 0 *(ilimitado)* |
| Fecha de finalización | *(vacío — sin vencimiento)* |

> **Nota:** Establecer un valor mínimo de orden protege tus márgenes. Sin él, un cliente podría usar este código en un pedido de $12 y eliminar tu beneficio. Siempre combina cupones con monto fijo con un mínimo razonable.

## Ejemplo 3: Envío gratis

**Escenario:** Ofrecer envío gratis en cualquier orden sin mínimo de gasto.

| Campo | Valor |
|-------|-------|
| Código | `FREESHIP` |
| Nombre | Envío gratis |
| Tipo de descuento | Envío gratis |
| Alcance de aplicación | Todo el carrito |
| Uso máximo total | *(vacío — ilimitado)* |
| Uso máximo por cliente | 1 |
| Valor mínimo de la orden | *(vacío — sin mínimo)* |

> **Nota:** Seleccione el tipo de descuento **Envío gratis**, que elimina automáticamente los cargos de envío del pedido. Este es el enfoque más limpio y funciona independientemente del método de envío que el cliente elija.

## Ejemplo 4: Código de bienvenida para clientes nuevos

**Escenario:** Ofrecer un 15% de descuento en su primer pedido a nuevos clientes para fomentar la conversión.

| Campo | Valor |
|-------|-------|
| Código | `WELCOME15` |
| Nombre | Bienvenido — 15% de descuento en primer pedido |
| Tipo de descuento | Porcentaje |
| Valor del descuento | 15 |
| Alcance de aplicación | Todo el carrito |
| Uso máximo por cliente | 1 |
| Solo para clientes nuevos | Marcado |

El sistema verifica el estado de cliente nuevo comprobando si el cliente tiene algún pedido anterior completado. Si un cliente con historial de pedidos intenta aplicar este código, verá un mensaje claro de error en la caja de pago.

## Ejemplo 5: Cupón específico del producto

**Escenario:** Ofrecer $5 de descuento en productos seleccionados — por ejemplo, para mover inventario de venta lenta.

| Campo | Valor |
|-------|-------|
| Código | `PICK5` |
| Nombre | $5 de descuento en artículos seleccionados |
| Tipo de descuento | Monto fijo |
| Valor del descuento | 5 |
| Alcance de aplicación | Productos específicos |
| Productos elegibles | *(seleccionar los productos objetivo)* |
| Uso máximo por cliente | 1 |

> **Nota:** Use el alcance de producto cuando desee descuentar SKU individuales. Use el alcance de categoría (ejemplo siguiente) cuando desee descuentar todo un departamento. El alcance de producto le da un control preciso; el alcance de categoría es más fácil de mantener cuando su catálogo cambia con frecuencia.

## Ejemplo 6: Cupón de categoría

**Escenario:** Realizar una promoción de 25% de descuento en todos los artículos de la categoría Electrónicos.

| Campo | Valor |
|-------|-------|
| Código | `ELEC25` |
| Nombre | 25% de descuento en electrónicos |
| Tipo de descuento | Porcentaje |
| Valor del descuento | 25 |
| Alcance de aplicación | Categorías específicas |
| Categorías elegibles | Electrónicos |
| Uso máximo total | *(vacío — ilimitado)* |
| Uso máximo por cliente | 1 |


Cuando se aplica a una categoría, el descuento solo se aplica a los artículos elegibles en el carrito.

Los artículos que no son electrónicos se cobran al precio completo.

## Comparación de tipos de descuento

| Tipo | Cómo funciona | Mejor para | Ejemplo |
|------|-------------|----------|---------|
| **Porcentaje** | Deduce un porcentaje del total elegible | Descuentos que se escalan según el tamaño del pedido | 20% de descuento en todo el carrito |
| **Monto fijo** | Deduce una cantidad fija en dólares | Promociones simples y predecibles | $10 de descuento en pedidos superiores a $75 |
| **Envío gratis** | Elimina los cargos de envío del pedido | Reducir la abandono de carrito en la caja de pago | Envío gratis, sin mínimo |

## Comparación de alcance

| Alcance | Cómo funciona | Mejor para |
|-------|-------------|----------|
| **Todo el carrito** | El descuento se aplica al total completo del pedido | Promociones a nivel de tienda y códigos de bienvenida |
| **Productos específicos** | El descuento se aplica solo a productos seleccionados en el carrito | Limpiar inventario específico o destacar ofertas |
| **Categorías específicas** | El descuento se aplica solo a artículos en categorías seleccionadas | Ventas por departamento y promociones estacionales |

## Consejos

- **Usa códigos memorables** — `SUMMER20` funciona mejor que `COUPONX1600406498`. Guarda los códigos generados automáticamente para campañas masivas.
- **Prueba antes de distribuir** — Realiza un pedido de prueba con el código de cupón para verificar que se aplique correctamente y respete todos los límites.
- **Monitorea el uso** — Revisa el recuento de redenciones en cada tarjeta de cupón para seguir el rendimiento de la campaña en tiempo real.
- **Combínalo con la barra de anuncio** — Promociona tu código de cupón en una notificación a nivel del sitio para que los clientes lo vean antes de comenzar a comprar.