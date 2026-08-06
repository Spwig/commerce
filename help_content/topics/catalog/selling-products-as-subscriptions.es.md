---
title: Vender productos como suscripciones
---

Cualquier producto Simple, Variable o Digital ahora se puede vender con un pago recurrente, junto con - o en lugar de - una compra única. Esta guía cubre cómo activar las suscripciones para un producto, elegir qué planes pueden elegir los clientes y qué ven realmente los clientes al comprar.

<!-- screenshots-needed:
- url: /admin/catalog/product/{id}/change/
  filename: subscriptions-tab.webp
  description: El formulario de edición del producto con la pestaña de Suscripciones activa, mostrando
    Habilitar Suscripción marcado, uno o más planes seleccionados en el campo de Planes de Suscripción, y las casillas de verificación Permitir Compra Única / Predeterminado a Suscripción visibles.
  save-to: core/static/core/admin/img/help/selling-products-as-subscriptions/
  viewport: 1440x900
- url: (tienda) página de detalles del producto para un producto con suscripción habilitada
  filename: subscribe-and-save-selector.webp
  description: El selector de tienda "Compra única" vs "Suscribirse y guardar" expandido, mostrando una lista de niveles de frecuencia de entrega con un rótulo de "Ahorra X%" en los niveles con descuento.
  save-to: core/static/core/admin/img/help/selling-products-as-subscriptions/
  viewport: 1440x900
  notes: Requiere un producto con suscripción habilitada con al menos un plan público activo y tarifas, visto desde la tienda (no desde el administrador).
-->

## Qué tipos de productos se pueden vender como suscripciones

Las suscripciones solo están disponibles para estos tipos de productos:

| Eligible | No elegible |
|----------|---------------|
| Producto Simple | Producto conjunto |
| Producto Variable | Tarjeta de regalo |
| Producto Digital | Producto personalizable |
| | Producto configurable |
| | Producto de reserva |

La razón es la entrega, no el precio: una suscripción recargará al cliente cada ciclo y reentregará el producto a través de un nuevo pedido cada vez. Spwig sabe cómo reenviar un producto Simple o Variable y reotorgar la descarga o licencia de un producto Digital en cada renovación - pero no puede reejecutar con seguridad la emisión de una tarjeta de regalo, un paquete de múltiples componentes, una personalización guardada del cliente, un armado de configurador o un horario de reserva en un calendario recurrente. Permitir que esos tipos se vendan como suscripciones conlleva el riesgo de tomar el dinero del cliente en el ciclo 2 sin poder entregarle nada.

La casilla **Habilitar Suscripción** no está oculta ni gris para los tipos no elegibles - puedes marcarla técnicamente en cualquier producto. Si intentas guardar un producto con suscripción habilitada, como una Tarjeta de regalo, Paquete, Personalizable, Configurable o de Reserva, Spwig rechazará el guardado con un error de validación explicando que este tipo de producto no se puede vender como suscripción. Cambia primero el **Tipo de producto** (pestaña Información Básica), o deja las suscripciones desactivadas para ese producto.

## Habilitar suscripciones en un producto

1. Navega a **Productos > Todos los productos** y abre el producto que quieres vender como suscripción (o crea uno nuevo).
2. Confirma que el **Tipo de producto** en la pestaña Información Básica sea Simple, Variable o Digital.
3. Haz clic en la pestaña **Suscripciones**.
4. Marca **Habilitar Suscripción**.
5. En el campo **Plan de Suscripción**, selecciona uno o más planes que este producto deba ofrecer. Solo puedes elegir planes que ya existan - si aún no has creado ninguno, consulta primero [Plan de Suscripción](/help/subscription-plans).
6. Configura las dos casillas de verificación de modo de compra (debajo).
7. Haz clic en **Guardar**.

## Adjuntar planes de suscripción

Un **Plan de Suscripción** es un modelo reutilizable - opciones de frecuencia de facturación, prueba, tarifa de configuración, reglas de cancelación - que construyes una vez y puedes adjuntar a cualquier número de productos elegibles. El campo **Plan de Suscripción** en la pestaña de Suscripciones del producto es donde conectas el producto a los planes que debe vender.

Puedes adjuntar más de un plan al mismo producto.

Esto es útil cuando, por ejemplo, quieres ofrecer una "tarifa estándar" y una "tarifa premium" recurrente para el mismo artículo - cada plan puede tener su propia tarifa, prueba y política de cancelación.


Cuando un producto tiene más de un plan adjunto, los clientes ven un selector de planes en la página del producto antes de elegir la frecuencia de facturación.

## Control de compras únicas frente a suscripciones

Dos casillas de verificación en la pestaña de Suscripciones controlan cómo los clientes pueden comprar el producto:

- **Permitir compra única** — Está activado por defecto. Al marcarlo, los clientes eligen entre una compra única regular y una suscripción. Desmarque para hacer que el producto sea solo de suscripción: cada compra se convierte en un pedido recurrente y no se muestra ninguna opción de compra única en absoluto.
- **Predeterminado a suscripción** — Selecciona la opción de suscripción (y su plan/tier predeterminado) cuando se carga la página del producto, en lugar de hacer que los clientes elijan activamente. Esto solo tiene efecto cuando **Permitir compra única** también está marcado — si la compra única está desactivada, el producto es solo de suscripción, independientemente de esta configuración.

Use **Predeterminado a suscripción** para productos donde la entrega recurrente es la expectativa natural (café, suplementos, productos de consumo) — elimina un clic y empuja a los clientes hacia la opción que los mantiene volviendo, sin quitarles la capacidad de comprar solo una vez.

## Lo que ven los clientes

### En la página del producto

Cuando un producto tiene suscripciones habilitadas y al menos un plan activo, público adjunto, aparece un selector de modo de compra en la página del producto:

- Si se permite la compra única, los clientes ven una elección de **"Compra única"** frente a **"Suscríbete y ahorra"** y predeterminado a cualquier modo que haya configurado.
- Si el producto tiene más de un plan adjunto, aparece un selector de planes una vez que se seleccione **"Suscríbete y ahorra"**.
- Para el plan elegido, los clientes ven una lista de **frecuencia de entrega** construida a partir de los niveles de precios de ese plan (por ejemplo, Mensual, Trimestral, Anual), cada uno mostrando su precio y un **rótulo de "Ahorra X%"** cuando el nivel tiene un descuento.
- La duración de la prueba, la tarifa de configuración y la política de cancelación del plan (por ejemplo, "Cancela en cualquier momento") se muestran junto con la lista de niveles, junto con una nota de que se agrega un método de pago en el momento de finalizar la compra.

### En el carrito y en el proceso de finalización

Los artículos de línea de suscripción en el carrito llevan un **rótulo de Suscripción**, la frecuencia de facturación (por ejemplo, "Cada mes") y una nota de prueba si aplica, para que el cliente sepa claramente cuáles líneas son recurrentes. En el proceso de finalización, el cliente elige un proveedor de pago como siempre — este es el método de pago que se cargará en las renovaciones futuras.

> **Limitación conocida:** Guardar automáticamente la tarjeta del cliente para renovaciones de suscripción futuras aún no está conectado para algunos proveedores de pago. Hasta que un proveedor específico lo soporte, las suscripciones realizadas a través de él pueden requerir un seguimiento adicional (por ejemplo, contactar al cliente para obtener detalles de pago actualizados antes de una renovación) en lugar de ser totalmente automáticas desde el primer día. Consulte la configuración de su proveedor de pago si nota que las renovaciones no se cobran automáticamente para una suscripción.

## Consejos

- Cree y pruebe primero el plan de suscripción (niveles de precios, prueba, política de cancelación), luego ájelo a productos — es más fácil obtener el plan correcto desde el principio que corregirlo en varios productos más adelante.
- Deje **Permitir compra única** marcado para la mayoría de los productos. Reserve los productos solo de suscripción para casos en los que una compra única realmente no tenga sentido para su negocio.
- Si está convirtiendo un producto de mayor venta existente en una opción de suscripción, deje **Predeterminado a suscripción** desactivado al principio para no molestar a los clientes acostumbrados a comprarlo una vez — ábralo más tarde una vez que haya visto cómo responden los suscriptores.
- Los productos digitales son un buen ejemplo para suscripciones (licencias de software, membresías de contenido) ya que la renovación restablece automáticamente el acceso sin necesidad de envío.
- Si necesita un tipo de producto que no es elegible (por ejemplo, un paquete o un artículo personalizable) para ser vendido de forma recurrente, considere si una versión simplificada equivalente Simple o Digital podría llevar la suscripción en su lugar.