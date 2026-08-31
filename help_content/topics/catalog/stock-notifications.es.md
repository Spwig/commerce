---
title: Notificaciones de existencias
---

Las notificaciones de existencias permiten a los clientes suscribirse para recibir un correo electrónico cuando un producto agotado vuelve a estar disponible. La configuración de visualización de existencias controla lo que los clientes ven en las páginas de producto, como etiquetas de estado de existencias, advertencias de stock bajo y qué ocurre cuando un producto se agota.

## Configuración de visualización de existencias

La configuración de visualización de existencias son valores predeterminados a nivel de tienda que se aplican a todos los productos, a menos que se anulen a nivel de categoría o producto.

Vaya a **Catálogo > Configuración de visualización de existencias** para configurar estas opciones. Hay un registro de configuración para su tienda; haga clic en él para editarlo.

### Visualización del estado de existencias

| Configuración | Descripción |
|---------|-------------|
| **Mostrar estado de existencias** | Mostrar etiquetas de "En stock" o "Agotado" en las páginas de producto |
| **Mostrar advertencia de stock bajo** | Mostrar un mensaje de "Solo quedan X" cuando el stock está bajo |
| **Umbral de stock bajo** | La cantidad en o por debajo de la cual aparece la advertencia de stock bajo (predeterminado: 5) |
| **Mostrar cantidad exacta** | Mostrar el número exacto restante (p. ej., "¡Solo quedan 3!") en lugar de una advertencia genérica |

### Comportamiento cuando no hay existencias

La configuración **Acción cuando no hay existencias** determina lo que ven los clientes cuando un producto no tiene stock disponible:

| Acción | Lo que ven los clientes |
|--------|-------------------|
| **Ocultar de las listas** | El producto se elimina de las páginas de categoría y de los resultados de búsqueda |
| **Mostrar como no disponible** | El producto es visible pero no se puede añadir al carrito |
| **Mostrar botón "Avísame"** | Los clientes pueden registrar su correo electrónico para ser notificados cuando el stock vuelva |
| **Permitir pedidos anticipados** | Los clientes pueden comprar el producto incluso cuando el stock es cero |

Establezca **Mensaje de no disponibilidad** para personalizar el texto mostrado cuando un producto no está disponible (predeterminado: `Agotado`).

Establezca **Mensaje de pedido anticipado** para personalizar el texto mostrado para productos con pedido anticipado (predeterminado: `Disponible en pedido anticipado`).

### Visualización de envío y entrega

| Configuración | Descripción |
|---------|-------------|
| **Mostrar ubicación de "Envía desde"** | Mostrar el nombre del almacén en la página del producto |
| **Mostrar entrega estimada** | Mostrar fechas de entrega estimadas calculadas desde la ubicación del almacén |

### Permitir pedidos anticipados (a nivel de sitio)

Marque **Permitir pedidos anticipados** para permitir que los clientes compren cualquier producto agotado por defecto. Los productos y categorías individuales pueden anular esta configuración.

## Notificaciones de reposición

Cuando establece la acción de no disponibilidad en **Mostrar botón "Avísame"**, los clientes pueden ingresar su dirección de correo electrónico en la página del producto para recibir un correo electrónico cuando el producto se reponga.

### Ver solicitudes de notificación

Vaya a **Catálogo > Notificaciones de existencias** para ver todas las solicitudes de notificación de los clientes. Cada registro muestra:
- Dirección de correo electrónico del cliente
- Producto y variante (si aplica)
- Almacén preferido (si el cliente seleccionó una preferencia regional)
- Cuándo se creó la solicitud
- Cuándo se envió la notificación (vacío si aún no se ha enviado)

### Cuándo se envían las notificaciones

Spwig envía correos electrónicos de reposición automáticamente cuando el nivel de existencias de un producto sube por encima de cero. El campo **Notificado el** registra cuándo se envió el correo electrónico.

Los clientes reciben un correo electrónico de notificación. Una vez notificados, deben suscribirse nuevamente si el producto se agota una segunda vez.

Si prefiere enviar más que una simple alerta — por ejemplo, mostrando el producto reabastecido con un bloque de contenido de **Producto destacado**, o haciendo seguimiento un día después — cree un viaje de **Producto de nuevo en stock** en **Estudio de campañas > Viajes** y establézcalo como **Activo**. Una vez que ese viaje existe, los clientes en espera se inscriben en él en lugar de recibir el correo electrónico único simple; sin un viaje activo, este correo electrónico único sigue enviándose exactamente como se describe arriba. Consulte [Viajes activados](/help/triggered-journeys) para saber cómo funciona el disparador.

### Filtrar solicitudes de notificación

Use los filtros de administración para encontrar:
- Solicitudes para un producto específico
- Solicitudes que ya han sido notificadas (para ver a quién se ha contactado)
- Solicitudes que aún están pendientes (clientes esperando una reposición)

## Sobreescrituras a nivel de producto

La configuración predeterminada de visualización del stock del sitio puede sobrescribirse por producto o categoría. En el formulario de edición del producto, busque la sección **Stock** donde puede configurar un **Acción de Agotado** específico del producto que difiera del predeterminado global.

Esto es útil cuando desea que la mayoría de los productos permitan pedidos de devolución, pero mantenga algunos productos configurados como "Notificarme" - o cuando un producto específico deba ocultarse cuando esté agotado.

## Consejos

- Establezca **Umbral de Stock Bajo** en el punto de reposición que normalmente utiliza, para que los clientes reciban una alerta sobre la disponibilidad limitada antes de que se acabe por completo.
- Utilice la opción **Mostrar botón "Notificarme"** en lugar de ocultar los productos agotados: los clientes que se registren representan una demanda real que puede justificar un pedido de reposición.
- Active **Mostrar Cantidad Exacta** con moderación. Para la mayoría de las tiendas, mostrar "Solo quedan 3!" funciona mejor que mostrar el número exacto, ya que crea urgencia sin revelar la imagen completa de su inventario.
- Revise la lista de notificaciones de stock antes de realizar un nuevo pedido: el número de solicitudes pendientes de notificación le indica cuánta demanda existe para ese producto.
- Si utiliza pedidos de devolución, actualice su **Mensaje de Devolución** para fijar expectativas precisas (por ejemplo, "Se envía en 2-3 semanas - ordene ahora para reservar su lugar").
- Combine las notificaciones de agotamiento con el marketing por correo electrónico: cuando se abastezca un producto popular, envíe una campaña a todos los que se registraron, no solo al correo electrónico de notificación automática.