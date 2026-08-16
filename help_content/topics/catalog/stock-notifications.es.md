---
title: Notificaciones de existencia
---

Las notificaciones de existencia permiten a los clientes registrarse para recibir un correo electrónico cuando un producto agotado vuelva a estar disponible. La configuración de visualización de existencias controla lo que ven los clientes en las páginas de productos: como las etiquetas de estado de existencias, las alertas de existencias bajas y lo que ocurre cuando un producto se agota.

## Configuración de visualización de existencias

La configuración de visualización de existencias son valores predeterminados para toda la tienda que se aplican a todos los productos, a menos que se modifiquen a nivel de categoría o producto.

Navegue hasta **Catálogo > Configuración de visualización de existencias** para configurar estas opciones. Hay un registro de configuración para su tienda: haga clic en él para editar.

### Visualización del estado de existencias

| Configuración | Descripción |
|---------|-------------|
| **Mostrar estado de existencias** | Mostrar etiquetas "En stock" o "Agotado" en las páginas de productos |
| **Mostrar alerta de existencias bajas** | Mostrar un mensaje "Solo hay X disponibles" cuando las existencias estén bajando |
| **Límite de existencias bajas** | La cantidad a partir de la cual aparece la alerta de existencias bajas (predeterminado: 5) |
| **Mostrar cantidad exacta** | Mostrar el número exacto restante (por ejemplo, "Solo hay 3 disponibles!") en lugar de una alerta genérica |

### Comportamiento cuando el producto está agotado

La configuración **Acción cuando el producto está agotado** determina lo que ven los clientes cuando un producto no tiene existencias:

| Acción | Lo que ven los clientes |
|--------|-------------------|
| **Ocultar de las listas** | El producto se elimina de las páginas de categoría y los resultados de búsqueda |
| **Mostrar como no disponible** | El producto es visible, pero no se puede agregar al carrito |
| **Mostrar botón "Notificarme"** | Los clientes pueden registrarse para recibir un correo electrónico cuando vuelva a estar disponible |
| **Permitir pedidos de devolución** | Los clientes pueden comprar el producto incluso cuando las existencias sean cero |

Establezca **Mensaje cuando el producto está agotado** para personalizar el texto mostrado cuando un producto no esté disponible (predeterminado: `Agotado`).

Establezca **Mensaje de pedido de devolución** para personalizar el texto mostrado para productos que permitan pedidos de devolución (predeterminado: `Disponible para pedido de devolución`).

### Visualización del envío y entrega

| Configuración | Descripción |
|---------|-------------|
| **Mostrar ubicación "Envío desde"** | Mostrar el nombre del almacén en la página del producto |
| **Mostrar entrega estimada** | Mostrar fechas de entrega estimadas calculadas desde la ubicación del almacén |

### Permitir pedidos de devolución (a nivel de sitio)

Marque **Permitir pedidos de devolución** para permitir a los clientes comprar cualquier producto agotado por defecto. Los productos y categorías individuales pueden anular esta configuración.

## Notificaciones de reposición de existencias

Al configurar la acción de producto agotado en **Mostrar botón "Notificarme"**, los clientes pueden ingresar su dirección de correo electrónico en la página del producto para recibir un correo electrónico cuando el producto vuelva a estar disponible.

### Ver solicitudes de notificación

Navegue hasta **Catálogo > Notificaciones de existencias** para ver todas las solicitudes de notificación de los clientes. Cada registro muestra:
- Dirección de correo electrónico del cliente
- Producto y variante (si aplica)
- Almacén preferido (si el cliente seleccionó una preferencia regional)
- Cuándo se creó la solicitud
- Cuándo se envió la notificación (en blanco si aún no se ha enviado)

### Cuándo se envían las notificaciones

Spwig envía correos electrónicos de reposición de existencias automáticamente cuando el nivel de existencias de un producto supera cero. El campo **Notificado a las** registra cuándo se envió el correo electrónico.

Los clientes reciben un correo electrónico de notificación. Una vez notificados, necesitan registrarse nuevamente si el producto vuelve a agotarse por segunda vez.

### Filtros para solicitudes de notificación

Use los filtros del administrador para encontrar:
- Solicitud para un producto específico
- Solicitud que ya se notificó (para ver quién se contactó)
- Solicitud pendiente (clientes esperando reposición)

## Anulaciones a nivel de producto

La configuración de visualización de existencias predeterminada para toda la tienda se puede anular a nivel de producto o categoría. En el formulario de edición del producto, busque la sección **Existencias** donde puede configurar una **Acción cuando el producto está agotado** específica del producto que difiera del valor predeterminado global.

Esto es útil cuando desea que la mayoría de los productos permitan pedidos de devolución, pero mantenga algunos productos configurados como "Notificarme"; o cuando un producto específico debe ocultarse cuando esté agotado.

## Consejos

Preserve all markdown formatting, image paths, code blocks, and technical terms.

- Establezca **Límite de Existencias Bajas** en el punto de reposición que normalmente utiliza, para que los clientes reciban una alerta sobre la disponibilidad limitada antes de que se acaben por completo.
- Utilice la opción **Mostrar botón "Notificarme"** en lugar de ocultar los productos agotados: los clientes que se registren representan una demanda real que puede justificar un pedido de reposición.
- Active **Mostrar Cantidad Exacta** con moderación.

Para la mayoría de las tiendas, mostrar "¡Solo quedan 3!" funciona mejor que mostrar el número exacto, ya que crea urgencia sin revelar la imagen completa de su inventario.
- Revise la lista de notificaciones de existencias antes de realizar un nuevo pedido: el número de solicitudes pendientes de notificación le indica cuánta demanda existe para ese producto.
- Si utiliza pedidos de devolución, actualice su **Mensaje de Pedido de Devolución** para fijar expectativas precisas (por ejemplo: "Se enviará en 2-3 semanas: ¡ordene ahora para reservar su lugar").
- Combine las notificaciones de agotamiento con el marketing por correo electrónico: cuando se reabastezca un producto popular, envíe una campaña a todos los que se registraron, no solo al correo electrónico de notificación automática.