---
title: Ejemplos de Promociones
---

Este guía muestra ejemplos concretos de cómo configurar diferentes tipos de promociones. Cada ejemplo incluye los valores exactos de los campos que debe ingresar en el asistente de promociones para que pueda seguirlos o adaptarlos para su tienda.

![Tarjeta de Promoción](/static/core/admin/img/help/promotion-examples/promotion-card.webp)

## Ejemplo: Descuento porcentaje en una categoría

**Escenario:** 30% de descuento en todos los zapatos para la liquidación de invierno.

Navegue a **Marketing > Ventas y Promociones** y haga clic en **+ Crear Promoción**. Ingrese los siguientes valores en cada paso del asistente:

| Paso | Campo | Valor |
|------|-------|-------|
| Básicos | Nombre | Liquidación de Invierno — 30% de Descuento en Zapatos |
| Básicos | Descripción | Liquidación de fin de temporada para todos los calzados |
| Básicos | Activo | Marcado |
| Descuento | Tipo | Descuento por Porcentaje |
| Descuento | Valor | 30 |
| Programación | Fecha de Inicio | 15 de enero de 2026 |
| Programación | Fecha de Fin | 28 de febrero de 2026 |
| Productos | Aplicar a | Categorías |
| Productos | Seleccionado | Zapatos, Botas, Sandalias |

Esto crea una venta limitada por tiempo que descuenta automáticamente cada producto en las categorías seleccionadas. Un par de botas de $120 se convierte en $84, y un par de sandalias de $60 se convierte en $42.

## Ejemplo: Descuento fijo en una colección

**Escenario:** $15 de descuento en artículos de la colección Summer Essentials.

| Paso | Campo | Valor |
|------|-------|-------|
| Básicos | Nombre | Summer Essentials — $15 de Descuento |
| Básicos | Activo | Marcado |
| Descuento | Tipo | Descuento Fijo |
| Descuento | Valor | 15.00 |
| Programación | Fecha de Inicio | 1 de junio de 2026 |
| Programación | Fecha de Fin | (vacío — sin vencimiento) |
| Productos | Aplicar a | Colecciones |
| Productos | Seleccionado | Summer Essentials |

> **Nota:** El descuento de $15 se aplica a cada producto elegible individualmente. Un producto de $50 se convierte en $35, un producto de $30 se convierte en $15. Dejar la Fecha de Fin vacía significa que la promoción se ejecuta indefinidamente hasta que la desactive manualmente.

## Ejemplo: Precio de venta fijo para liquidación

**Escenario:** Establecer todos los artículos de liquidación en $9.99.

| Paso | Campo | Valor |
|------|-------|-------|
| Básicos | Nombre | Liquidación Final — Todo a $9.99 |
| Básicos | Activo | Marcado |
| Descuento | Tipo | Precio de Venta Fijo |
| Descuento | Valor | 9.99 |
| Programación | Fecha de Inicio | (hoy) |
| Productos | Aplicar a | Colecciones |
| Productos | Seleccionado | Liquidación Final |

> **Nota:** El Precio de Venta Fijo establece el precio exacto de venta, independientemente del precio original. Un artículo de $75 y un artículo de $25 se convierten ambos en $9.99. Use esto para estanterías de liquidación o precios uniformes donde desee que todos los artículos tengan el mismo punto de precio.

![Promoción de Categoría](/static/core/admin/img/help/promotion-examples/category-promotion.webp)

## Elegir el tipo de descuento adecuado

| Tipo | Cómo funciona | Mejor para | Ejemplo |
|------|-------------|----------|---------|
| **Descuento por Porcentaje** | Reduce el precio por un porcentaje | Ventas amplias donde los productos tienen precios variables | 20% de descuento — $100 se convierte en $80, $50 se convierte en $40 |
| **Descuento Fijo** | Resta una cantidad fija en dólares | Promociones con un mensaje específico de ahorro en dólares | $15 de descuento — $100 se convierte en $85, $50 se convierte en $35 |
| **Precio de Venta Fijo** | Establece el precio exacto de venta | Liquidaciones, precios uniformes, "todo a $X" | $9.99 — todos los artículos se convierten en $9.99 independientemente del precio original |

## Elegir el objetivo adecuado

| Objetivo | Cómo funciona | Mejor para |
|--------|-------------|----------|
| **Todos los productos** | Aplica a todos los productos de su tienda | Ventas sitewide, eventos de toda la tienda |
| **Categorías** | Aplica a todos los productos en categorías seleccionadas | Ventas por departamento, liquidaciones estacionales por tipo |
| **Marcas** | Aplica a todos los productos de marcas seleccionadas | Colaboraciones con marcas, eventos específicos de marca |
| **Colecciones** | Aplica a todos los productos en colecciones seleccionadas | Promociones curadas, ventas temáticas |
| **Productos** | Aplica a productos seleccionados individualmente | Ofertas seleccionadas a mano, selecciones limitadas |

## Patrones de programación

Tres patrones comunes para configurar horarios de promoción:

| Patrón | Fecha de Inicio | Fecha de Fin | Caso de uso |
|---------|-----------|----------|----------|
| **Inmediato, en curso** | Hoy | (vacío) | Reducciones de precios permanentes, ventas a largo plazo |
| **Rango de fechas** | Fecha futura | Fecha futura | Eventos estacionales, ventas de fin de año |
| **Inicio futuro, sin fin** | Fecha futura | (vacío) | Nuevos precios permanentes que comienzan en una fecha específica |

Establecer una Fecha de Inicio en el futuro crea una promoción programada. Aparecerá en la pestaña **Programada** en el panel de promociones y se activará automáticamente cuando llegue la fecha. Dejar la Fecha de Fin vacía significa que la promoción permanece activa hasta que la desactive manualmente.

## Consejos

- **Use nombres descriptivos** — Incluya el valor del descuento y el objetivo en el nombre (por ejemplo, "Verano 20% de descuento en zapatos") para que pueda identificar rápidamente las promociones en el panel.
- **Verifique la cantidad de productos afectados** — El paso de Revisión muestra cuántos productos se descuentarán. Si el número parece incorrecto, vuelva atrás y verifique su objetivo.
- **Empiece con lo pequeño** — Si no está seguro de un descuento, empiece con un porcentaje más pequeño y aumentelo si es necesario.
- **Use Descuento Fijo para marketing** — "$15 de descuento" es un ahorro concreto que es fácil de comunicar en anuncios y campañas de correo electrónico.
- **Use Descuento por Porcentaje para equidad** — Un descuento por porcentaje se escala con el precio, brindando ahorros proporcionales en diferentes puntos de precio.