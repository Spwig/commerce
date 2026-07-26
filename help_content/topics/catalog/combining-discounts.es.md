---
title: Combinando descuentos
---

La plataforma ofrece cuatro tipos de descuentos que pueden funcionar juntos: ventas de productos, promociones, códigos de cupón y tarjetas regalo. Entender cómo interactúan ayuda a ejecutar campañas efectivas sin resultados inesperados o descuentos dobles no deseados.

> **Las tarjetas regalo aún no pueden aplicarse en el checkout en línea.** El diseño descrito a continuación — tarjeta regalo aplicada al final, después de todos los demás descuentos — es cómo funcionará una vez que se lance esa característica. Actualmente, una tarjeta regalo solo puede canjearse en persona en el **Punto de Venta**, por lo que las interacciones descritas para la tienda en línea no se aplican aún específicamente a las tarjetas regalo. Consulte el tema de ayuda **Tarjetas Regalo** para conocer el estado actual.

## Las Cuatro Capas de Descuento

Cada tipo de descuento opera en un nivel diferente y es visible para los clientes de maneras distintas.

| Capa | Dónde se establece | Cómo se aplica | Visible para el cliente |
|-------|---------------|-----------------|-------------------|
| **Venta de producto** | Formulario de edición del producto > Sección de venta | Cambia automáticamente el precio mostrado | Sí — se muestra como el precio original tachado |
| **Promoción** | Marketing > Ventas y Promociones | Se aplica automáticamente a productos coincidentes | Sí — se muestra como un precio de venta en las tarjetas del producto |
| **Código de cupón** | Marketing > Cupones | El cliente ingresa un código en el checkout | Solo en el checkout después de ingresar el código |
| **Tarjeta regalo** | Canjeada contra el saldo de una tarjeta regalo | Reduce el total del pago | Solo en el Punto de Venta por ahora (ver nota anterior) |

## Cómo Funciona la Prioridad

Las promociones tienen un campo **Prioridad** que acepta valores de 0 en adelante. Los números más altos significan mayor prioridad.

Cuando múltiples promociones coinciden con el mismo producto, la que tiene la **mayor prioridad gana**. No se acumulan — solo se aplica una promoción por producto.

**Ejemplo:** "Venta flash 50% de descuento" (prioridad 10) y "Venta de verano 20% de descuento" (prioridad 5) ambas se dirigen a todos los productos. Un cliente ve el precio de la venta flash del 50%, no un 70% combinado.

Dentro del mismo nivel de prioridad, el sistema selecciona la promoción que ofrece el mayor descuento al cliente.

## Reglas de acumulación

La siguiente tabla muestra qué combinaciones de descuentos están permitidas y cómo controlarlas.

| Combinación | ¿Permitido? | Cómo controlarlo |
|-------------|----------|-------------------|
| Venta de producto + Promoción | Solo si está habilitado | Marque **"Acumular con ventas de productos"** en la configuración avanzada de la promoción |
| Promoción + Promoción | No — gana la de mayor prioridad | Establezca valores de prioridad para controlar cuál se aplica |
| Promoción + Código de cupón | Sí | La promoción descuenta el precio del producto, el código de cupón descuenta el total del carrito por separado |
| Cupón + Cupón | Configurable | La bandera **"No se puede combinar con otros cupones"** del cupón controla esto (habilitada por defecto) |
| Cupón + Artículos en venta | Configurable | La bandera **"Excluir artículos en venta"** del cupón controla esto |
| Tarjeta regalo + Cualquier descuento | Sí — siempre | Las tarjetas regalo se aplican al final, reduciendo el monto final del pago después de todos los demás descuentos. Actualmente solo posible en el Punto de Venta — ver nota anterior |

## Escenarios Comunes

### Escenario A: Promoción sitewide + código de cupón

- **Configuración:** 20% de descuento en todo (promoción) + el cliente tiene un cupón de $10 de descuento
- **Resultado:** Un producto de $100 se convierte en $80 (promoción), luego el cupón de $10 se aplica al total del carrito. El cliente paga **$70**.

### Escenario B: Producto en venta + promoción sitewide

- **Configuración:** El producto tiene una venta de nivel de producto del 30% + existe una promoción sitewide del 20%
- **Resultado (acumulación deshabilitada):** Solo se aplica la venta del producto. El cliente paga **$70**.
- **Resultado (acumulación habilitada):** Ambas se aplican. 30% de descuento primero = $70, luego 20% de descuento = **$56**.

### Escenario C: Dos promociones en el mismo producto

- **Configuración:** "Venta flash 40% de descuento" (prioridad 10) + "Venta de verano 20% de descuento" (prioridad 5), ambas se dirigen a todos los productos
- **Resultado:** Gana la venta flash porque tiene mayor prioridad. El cliente paga **$60** en un producto de $100.

### Escenario D: Cupón en un producto en venta

- **Configuración:** El producto está en venta con un descuento del 25%.

# Ejemplos de uso

El cliente introduce un código de cupón del 10% que tiene habilitada la opción "Excluir artículos en oferta".
- **Resultado:** El cupón no se aplica a ese producto.

Si el carrito contiene artículos que no son de oferta, el cupón solo se aplica a esos.

## ¿Qué tipo de descuento usar

| Objetivo | Enfoque recomendado | ¿Por qué? |
|---------|-------------------|---------|
| Mover inventario estacional | **Promoción** (destino por categoría o colección) | Automático, no se requiere acción del cliente, visible en las tarjetas de producto |
| Recompensar a un cliente específico | **Código de cupón** (uso único, límite por cliente) | Dirigido, rastreable, parece personal |
| Oferta rápida para un solo producto | **Venta del producto** (en el formulario de edición del producto) | Más rápido de configurar, no se necesita asistente de promoción |
| Crédito de tienda o regalo | **Tarjeta de regalo** | Basado en saldo; actualmente redimible solo en el punto de venta |
| Evento en toda la tienda | **Promoción** (destino a todos los productos) | Máximo alcance, una configuración cubre todo |
| Campaña de recuperación | **Código de cupón** (restricciones para clientes nuevos o regresados) | Puede dirigirse a segmentos específicos de clientes |

## Consejos

- **Prueba con un carrito real** — después de configurar promociones y cupones, añade productos a un carrito y pasa por el proceso de pago para verificar que los descuentos se apliquen como se espera.
- **Verifica el recuento de productos afectados** — en el paso de revisión de la promoción, verifica que el número de productos afectados coincida con tu intención.
- **Usa la prioridad con intención** — si ejecutas múltiples promociones simultáneamente, siempre establece valores de prioridad diferentes para controlar cuál gana.
- **Mantén el apilamiento deshabilitado por defecto** — solo habilite "Apilar con ventas de productos" cuando desee específicamente descuentos dobles.
- **Documenta tu estrategia** — usa el campo de descripción de la promoción para anotar por qué existe una promoción y cómo se relaciona con otras promociones activas.