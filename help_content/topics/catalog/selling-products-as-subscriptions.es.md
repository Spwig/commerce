---
title: Vender productos como suscripciones
---

Cualquier producto Simple, Variable o Digital ahora se puede vender con un pago recurrente, junto con - o en lugar de - una compra única. Este manual cubre cómo activar las suscripciones para un producto, elegir qué planes pueden elegir los clientes y qué ven realmente los clientes al comprar.

## Qué tipos de productos se pueden vender como suscripciones

Las suscripciones solo están disponibles para estos tipos de productos:

| Eligible | No elegible |
|----------|---------------|
| Producto Simple | Producto conjunto |
| Producto Variable | Tarjeta de regalo |
| Producto Digital | Producto personalizable |
| | Producto configurable |
| | Producto de reserva |

La razón es la entrega, no el precio: una suscripción recargará al cliente cada ciclo y reentregará el producto a través de un nuevo pedido cada vez. Spwig sabe cómo reenviar un producto Simple o Variable y reotorgar la descarga o licencia de un producto Digital en cada renovación - pero no puede ejecutar con seguridad la emisión de una tarjeta de regalo, un paquete de múltiples componentes, una personalización guardada del cliente, un montaje de configurador o un horario de reserva en un calendario recurrente. Permitir que esos tipos se vendan como suscripciones conlleva el riesgo de tomar el dinero del cliente en el ciclo 2 sin poder entregar nada.

La casilla **Habilitar suscripción** en sí no está oculta o gris para los tipos no elegibles - puedes marcarla técnicamente en cualquier producto. Si intentas guardar un producto de Tarjeta de regalo, Paquete, Personalizable, Configurable o de Reserva con suscripciones habilitadas, Spwig rechazará el guardado con un error de validación que explica que este tipo de producto no se puede vender como suscripción. Cambia primero el **Tipo de producto** (pestaña Información básica), o deja las suscripciones desactivadas para ese producto.

## Habilitar suscripciones en un producto

1. Navega a **Productos > Todos los productos** y abre el producto que quieres vender como suscripción (o crea uno nuevo).
2. Confirma que el **Tipo de producto** en la pestaña Información básica sea Simple, Variable o Digital.
3. Haz clic en la pestaña **Suscripciones**.
4. Marca **Habilitar suscripción**.
5. En el campo **Plan de suscripción**, selecciona uno o más planes que este producto deba ofrecer. Solo puedes elegir planes que ya existan - si aún no has creado ninguno, consulta primero [Plan de suscripción](/help/subscription-plans).
6. Configura las dos casillas de verificación de modo de compra (debajo).
7. Haz clic en **Guardar**.

![La pestaña Suscripciones del formulario de edición de producto: Habilitar suscripción marcada, un plan seleccionado en la lista de Planes de suscripción, y las casillas Permitir compra única y Predeterminar a suscripción](/static/core/admin/img/help/selling-products-as-subscriptions/subscriptions-tab.webp)

## Adjuntar planes de suscripción

Un **Plan de suscripción** es un modelo reutilizable - opciones de frecuencia de facturación, prueba, tarifa de configuración, reglas de cancelación - que construyes una vez y puedes adjuntar a cualquier número de productos elegibles. El campo **Plan de suscripción** en la pestaña Suscripciones del producto es donde conectas el producto al plan (o planes) bajo los cuales se vende.

Puedes adjuntar más de un plan al mismo producto. Esto es útil cuando, por ejemplo, quieres ofrecer una "versión estándar" y una "versión premium" recurrente para el mismo artículo - cada plan puede tener sus propios niveles de precios, prueba y política de cancelación. Cuando un producto tiene más de un plan adjunto, los clientes ven un selector de plan en la página del producto antes de elegir la frecuencia de facturación.

## Controlar compras únicas vs. compras por suscripción

Dos casillas de verificación en la pestaña Suscripciones controlan cómo pueden comprar los clientes el producto:

- **Permitir compra única** - activado por defecto.

Al marcarla, los clientes eligen entre una compra única regular y una suscripción.

Desmarca la casilla para hacer que el producto sea exclusivo de suscripción - cada compra se convierte en un pedido recurrente, y no se muestra ninguna opción de compra única en absoluto.
- **Predeterminar a suscripción** - selecciona la opción de suscripción (y su plan/tier predeterminado) cuando se carga la página del producto, en lugar de que los clientes elijan activamente la opción.

Esto solo tiene efecto cuando **Permitir compra única** también está marcado — si la compra única está desactivada, el producto es solo de suscripción, sin importar esta configuración.

Use **Predeterminar a suscripción** para productos donde la entrega recurrente sea la expectativa natural (café, suplementos, productos de consumo) — esto elimina un clic y orienta a los clientes hacia la opción que los mantiene volviendo, sin quitarles la capacidad de comprar una vez.

## Lo que ven los clientes

### En la página del producto

Cuando un producto tiene suscripciones activas y al menos un plan activo y público adjunto, aparece un selector de modo de compra en la página del producto:

![El selector de compra de la tienda con "Suscríbete y ahorra" seleccionado: un modo de compra única frente a un interruptor de Suscríbete y ahorra sobre una lista de frecuencia de entrega que muestra los niveles Anual (Ahorra 20%), Mensual y Trimestral (Ahorra 10%) con precios, además de notas de prueba, cancelación y pago](/static/core/admin/img/help/selling-products-as-subscriptions/subscribe-and-save-selector.webp)

- Si se permite la compra única, los clientes ven una elección de **"Compra única"** vs **"Suscríbete y ahorra"** y por defecto, se selecciona el modo que configuró.
- Si el producto tiene más de un plan adjunto, aparece un selector de plan una vez que se seleccione "Suscríbete y ahorra".
- Para el plan seleccionado, los clientes ven una lista de **frecuencia de entrega** construida a partir de los niveles de precios de ese plan (por ejemplo, Mensual, Trimestral, Anual), cada uno mostrando su precio y un **rótulo de "Ahorra X%"** cuando el nivel tenga un descuento.
- La duración de la prueba, tarifa de configuración y la política de cancelación del plan (por ejemplo, "Cancela en cualquier momento") se muestran junto con la lista de niveles, además de una nota que indica que se agrega un método de pago en el momento del pago.

### En el carrito y en el pago

Los artículos de suscripción en el carrito llevan un **rótulo de Suscripción**, la frecuencia de facturación (por ejemplo, "Cada mes") y una nota de prueba si aplica, para que el cliente sepa cuáles líneas son recurrentes. En el pago, el cliente elige un proveedor de pago como siempre — este es el método de pago que se cargará en las renovaciones futuras.

> **Limitación conocida:** Guardar automáticamente la tarjeta del cliente para renovaciones de suscripción en el momento del pago aún no está conectado para algunos proveedores de pago. Hasta que un proveedor específico lo soporte, las suscripciones colocadas a través de él pueden requerir un seguimiento adicional (por ejemplo, contactar al cliente para obtener detalles de pago actualizados antes de una renovación) en lugar de ser totalmente automáticas desde el primer día. Consulte la configuración de su proveedor de pago si nota que las renovaciones no se cargan automáticamente en una suscripción.

## Consejos

- Cree y pruebe primero el plan de suscripción (niveles de precios, prueba, política de cancelación), luego ájelo a los productos — es más fácil obtener el plan correcto desde el principio que corregirlo en varios productos posteriormente.
- Deje **Permitir compra única** marcado para la mayoría de los productos. Reserve los productos solo de suscripción para casos en los que la compra única realmente no tenga sentido para su negocio.
- Si está convirtiendo un producto de mayor venta existente en una opción de suscripción, deje **Predeterminar a suscripción** desactivado al principio para no molestar a los clientes acostumbrados a comprarlo una vez — ábralo más tarde una vez que haya visto cómo responden los suscriptores.
- Los productos digitales son un buen ejemplo para suscripciones (licencias de software, membresías de contenido) ya que la renovación restablece automáticamente el acceso sin necesidad de envío.
- Si necesita un tipo de producto que no es elegible (por ejemplo, un paquete o un artículo personalizable) para ser vendido de forma recurrente, considere si podría llevar la suscripción un equivalente simplificado o digital en su lugar.