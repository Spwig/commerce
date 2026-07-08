---
title: Notificaciones de stock
---

Las notificaciones de stock permiten a los clientes registrarse para recibir un correo electrónico cuando un producto agotado vuelva a estar disponible. La configuración de visualización del stock controla lo que ven los clientes en las páginas de productos, como etiquetas de estado del stock, advertencias de bajo stock y lo que ocurre cuando un producto se agota.

## Configuración de visualización del stock

La configuración de visualización del stock son valores predeterminados para toda la tienda que se aplican a todos los productos, a menos que se anulen a nivel de categoría o producto.

Navegue hasta **Catálogo > Configuración de Visualización del Stock** para configurar estas opciones. Hay un registro de configuración para su tienda — haga clic en él para editar.

### Visualización del estado del stock

| Configuración | Descripción |
|---------|-------------|
| **Mostrar estado del stock** | Mostrar las etiquetas "En stock" o "Agotado" en las páginas de productos |
| **Mostrar advertencia de bajo stock** | Mostrar un mensaje "Solo quedan X" cuando el stock esté por agotarse |
| **Umbral de bajo stock** | La cantidad a la que o por debajo de la cual aparece la advertencia de bajo stock (por defecto: 5) |
| **Mostrar cantidad exacta** | Mostrar el número exacto restante (por ejemplo, "Solo quedan 3!") en lugar de una advertencia genérica |

### Comportamiento cuando el producto está agotado

La configuración **Acción cuando el producto está agotado** determina lo que ven los clientes cuando un producto no tiene stock disponible:

| Acción | Lo que ven los clientes |
|--------|-------------------|
| **Ocultar en listados** | El producto se elimina de las páginas de categorías y resultados de búsqueda |
| **Mostrar como no disponible** | El producto es visible pero no se puede agregar al carrito |
| **Mostrar botón "Notificarme"** | Los clientes pueden registrar su correo electrónico para recibir una notificación cuando el stock vuelva a estar disponible |
| **Permitir pedidos anticipados** | Los clientes pueden comprar el producto incluso cuando el stock esté en cero |

Establezca **Mensaje cuando el producto está agotado** para personalizar el texto mostrado cuando un producto no está disponible (por defecto: `Agotado`).

Establezca **Mensaje de pedidos anticipados** para personalizar el texto mostrado para productos con pedidos anticipados (por defecto: `Disponible con pedido anticipado`).

### Visualización de envío y entrega

| Configuración | Descripción |
|---------|-------------|
| **Mostrar ubicación "Envío desde"** | Mostrar el nombre del almacén en la página del producto |
| **Mostrar fecha estimada de entrega** | Mostrar fechas estimadas de entrega calculadas desde la ubicación del almacén |

### Permitir pedidos anticipados (a nivel de toda la tienda)

Marque **Permitir pedidos anticipados** para permitir que los clientes compren cualquier producto agotado por defecto. Los productos individuales y categorías pueden anular esta configuración.

## Notificaciones de regreso al stock

Cuando establezca la acción de stock agotado en **Mostrar botón "Notificarme"**, los clientes pueden ingresar su dirección de correo electrónico en la página del producto para recibir un correo electrónico cuando el producto vuelva a estar disponible.

### Ver solicitudes de notificación

Navegue hasta **Catálogo > Notificaciones de Stock** para ver todas las solicitudes de notificación de los clientes. Cada registro muestra:
- Dirección de correo electrónico del cliente
- Producto y variante (si aplica)
- Almacén preferido (si el cliente seleccionó una preferencia regional)
- Cuándo se creó la solicitud
- Cuándo se envió la notificación (en blanco si aún no se ha enviado)

### Cuándo se envían las notificaciones

Spwig envía automáticamente correos electrónicos de regreso al stock cuando el nivel de stock de un producto sube por encima de cero. El campo **Notificado en** registra cuándo se envió el correo electrónico.

Los clientes reciben un solo correo electrónico de notificación. Una vez notificados, deben registrarse nuevamente si el producto se agota una segunda vez.

### Filtros de solicitudes de notificación

Use los filtros del administrador para encontrar:
- Solicitudes para un producto específico
- Solicitudes que ya han sido notificadas (para ver a quién se ha contactado)
- Solicitudes que aún están pendientes (clientes esperando una reposición)

## Anulaciones a nivel de producto

Las configuraciones de visualización del stock a nivel de toda la tienda pueden anularse por producto o categoría. En el formulario de edición del producto, busque la sección **Stock** donde puede establecer una **Acción cuando el producto está agotado** específica del producto que difiere del valor predeterminado global.

Esto es útil cuando desea que la mayoría de los productos permitan pedidos anticipados, pero mantener algunos productos configurados en "Notificarme" — o cuando un producto específico debe ocultarse cuando esté agotado.

## Consejos

Conservar todo el formato de markdown, rutas de imágenes, bloques de código y términos técnicos.

- Establece **Umbral de Stock Bajo** en el punto de reorden que sueles utilizar, para que los clientes sean advertidos sobre la disponibilidad limitada antes de que se agote por completo.
- Usa la opción **Mostrar botón "Notifícame"** en lugar de ocultar los productos agotados — los clientes que se registren representan una demanda real que puede justificar un nuevo pedido.
- Habilita **Mostrar cantidad exacta** con moderación.

Para la mayoría de tiendas, mostrar "Solo quedan 3!" funciona mejor que mostrar el número exacto, ya que genera urgencia sin revelar tu situación completa de inventario.
- Revisa la lista de notificaciones de stock antes de realizar un nuevo pedido — la cantidad de solicitudes pendientes te indica cuánta demanda existe para ese producto.
- Si utilizas pedidos por anticipado, actualiza tu **Mensaje de Pedido por Anticipado** para establecer expectativas precisas (p. ej., "Envío en 2-3 semanas — ordena ahora para reservar tu lugar").
- Combina las notificaciones de productos agotados con el marketing por correo electrónico: cuando restockees un producto popular, envía una campaña a todos los que se hayan registrado, no solo al correo electrónico de notificación automática.