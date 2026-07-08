---
title: Combinando descuentos
---

La plataforma ofrece cuatro tipos de descuentos que pueden funcionar juntos: ventas de productos, promociones, códigos de cupón y tarjetas regalo. Entender cómo interactúan ayuda a ejecutar campañas efectivas sin resultados inesperados o descuentos dobles no deseados.

## Las Cuatro Capas de Descuentos

Cada tipo de descuento opera en un nivel diferente y es visible para los clientes de maneras distintas.

| Capa | Dónde se Configura | Cómo se Aplica | Visible para el Cliente |
|-------|---------------|-----------------|-------------------|
| **Venta de Producto** | Formulario de edición del producto > Sección de Venta | Cambia automáticamente el precio mostrado | Sí — se muestra como el precio original tachado |
| **Promoción** | Marketing > Ventas y Promociones | Se aplica automáticamente a los productos coincidentes | Sí — se muestra como un precio de venta en las tarjetas del producto |
| **Código de Cupón** | Marketing > Cupones | El cliente ingresa un código en el checkout | Solo en el checkout después de ingresar el código |
| **Tarjeta Regalo** | Aplicado en el checkout desde el saldo de una tarjeta regalo | Reduce el total del pago | Solo en el checkout |

## Cómo Funciona la Prioridad

Las promociones tienen un campo **Prioridad** que acepta valores de 0 en adelante. Números más altos significan mayor prioridad.

Cuando múltiples promociones coinciden con el mismo producto, la que tiene **la prioridad más alta gana**. No se acumulan — solo se aplica una promoción por producto.

**Ejemplo:** "Venta Flash 50% de descuento" (prioridad 10) y "Venta de Verano 20% de descuento" (prioridad 5) ambas se dirigen a todos los productos. Un cliente ve el precio de la venta flash del 50%, no un 70% combinado.

Dentro del mismo nivel de prioridad, el sistema selecciona la promoción que ofrece el mayor descuento al cliente.

## Reglas de Apilamiento

La siguiente tabla muestra qué combinaciones de descuentos están permitidas y cómo controlarlas.

| Combinación | Permitido? | Cómo Controlarlo |
|-------------|----------|-------------------|
| Venta de Producto + Promoción | Solo si está habilitado | Marque **"Apilable con ventas de productos"** en la configuración avanzada de la promoción |
| Promoción + Promoción | No — la prioridad más alta gana | Establezca valores de prioridad para controlar cuál se aplica |
| Promoción + Código de Cupón | Sí | Las promociones descuentan el precio del producto, los cupones descuentan el total del carrito por separado |
| Cupón + Cupón | Configurable | La bandera **"No se puede combinar con otros cupones"** del cupón controla esto (habilitada por defecto) |
| Cupón + Artículos en Venta | Configurable | La bandera **"Excluir artículos en venta"** del cupón controla esto |
| Tarjeta Regalo + Cualquier Descuento | Sí — siempre | Las tarjetas regalo se aplican al final, reduciendo el monto final del pago después de todos los otros descuentos |

## Escenarios Comunes

### Escenario A: Promoción de todo el sitio + código de cupón

- **Configuración:** 20% de descuento en todo (promoción) + el cliente tiene un cupón de $10 de descuento
- **Resultado:** Un producto de $100 se convierte en $80 (promoción), luego el cupón de $10 se aplica al total del carrito. El cliente paga **$70**.

### Escenario B: Producto en venta + promoción de todo el sitio

- **Configuración:** El producto tiene una venta del 30% a nivel de producto + existe una promoción del 20% para todo el sitio
- **Resultado (apilamiento deshabilitado):** Solo se aplica la venta del producto. El cliente paga **$70**.
- **Resultado (apilamiento habilitado):** Ambas se aplican. 30% de descuento primero = $70, luego 20% de descuento = **$56**.

### Escenario C: Dos promociones en el mismo producto

- **Configuración:** "Venta Flash 40% de descuento" (prioridad 10) + "Venta de Verano 20% de descuento" (prioridad 5), ambas se dirigen a todos los productos
- **Resultado:** La Venta Flash gana porque tiene mayor prioridad. El cliente paga **$60** en un producto de $100.

### Escenario D: Cupón en un artículo en venta

- **Configuración:** El producto está en venta con un descuento del 25%. El cliente ingresa un código de cupón del 10% que tiene habilitada la opción "Excluir artículos en venta".
- **Resultado:** El cupón no se aplica a ese producto. Si el carrito tiene artículos no en venta, el cupón se aplica solo a esos.

## Qué Tipo de Descuento Usar

| Objetivo | Enfoque Recomendado | Por Qué |
|------|---------------------|-----|
| Mover inventario estacional | **Promoción** (destino por categoría o colección) | Automático, no se requiere acción del cliente, visible en las tarjetas del producto |
| Recompensar a un cliente específico | **Código de Cupón** (uso único, límite por cliente) | Dirigido, rastreable, se siente personalizado |
| Oferta rápida para un solo producto | **Venta de Producto** (en el formulario de edición del producto) | Más rápido de configurar, no se necesita asistente de promoción |
| Crédito de tienda o regalo | **Tarjeta Regalo** | Basado en saldo, el cliente gestiona su propio crédito |
| Evento de todo el sitio | **Promoción** (destino a todos los productos) | Máximo alcance, una configuración cubre todo |
| Campaña de recuperación | **Código de Cupón** (restricciones para clientes nuevos o regresados) | Puede dirigirse a segmentos específicos de clientes |

## Consejos

- **Pruebe con un carrito real** — después de configurar promociones y cupones, agregue productos a un carrito y pase por el checkout para verificar que los descuentos se apliquen como se espera.
- **Revise el recuento de productos afectados** — en el paso de revisión de la promoción, verifique que el número de productos afectados coincida con su intención.
- **Use la prioridad con intención** — si ejecuta múltiples promociones simultáneamente, siempre establezca valores de prioridad diferentes para controlar cuál gana.
- **Mantenga el apilamiento deshabilitado por defecto** — solo habilite "Apilable con ventas de productos" cuando específicamente desee descuentos dobles.
- **Documente su estrategia** — use el campo Descripción de la promoción para anotar por qué existe una promoción y cómo se relaciona con otras promociones activas.