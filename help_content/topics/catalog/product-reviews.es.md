---
title: Reseñas de productos
---

Las reseñas de productos permiten a los clientes calificar y escribir sobre su experiencia con un producto. Las reseñas que apruebes aparecerán en la página del producto en tu tienda, donde ayudarán a otros compradores a decidir qué comprar. Spwig te da total control sobre qué reseñas se publican: nada se publica hasta que las apruebes.

Las reseñas están ubicadas bajo **Productos > Reseñas** en la barra lateral, que se abre como un grupo: el primer enlace te lleva al **Panel de control de reseñas**, y **Moderar reseñas** te lleva directamente a la lista de reseñas.

## El panel de control de reseñas

Navega a **Productos > Reseñas** para abrir el panel de control: una vista general de una sola pantalla de cómo están funcionando las reseñas en toda tu tienda.

![Panel de control de reseñas](/static/core/admin/img/help/product-reviews/reviews-dashboard.webp)

En la parte superior, seis tarjetas de KPI resumen tu actividad de reseñas:

| Tarjeta | Lo que muestra |
|---|---|
| **Total de reseñas** | Todas las reseñas alguna vez enviadas, aprobadas o no |
| **Calificación promedio** | La calificación promedio de estrellas en cada reseña |
| **Pendiente de moderación** | Reseñas esperando tu aprobación o rechazo |
| **Tasa de aprobación** | La proporción de todas las reseñas que has aprobado |
| **Compras verificadas** | La proporción de reseñas dejadas por clientes con un pedido confirmado para ese producto |
| **Nuevas (30 días)** | Reseñas enviadas en los últimos 30 días |

Debajo de los KPI, tres gráficos dan más detalles:

- **Distribución de calificaciones** — un gráfico de barras de cuántas reseñas caen en cada calificación de estrellas (1-5). Un grupo de reseñas de 1 estrella aquí merece investigarse de inmediato.
- **Volumen de reseñas (12 semanas)** — un gráfico de líneas de la cantidad de reseñas por semana, para que puedas detectar picos después de una promoción o una caída que requiera atención.
- **Canal de compra de los reseñistas** — un gráfico de rosquilla del canal de marketing (directo, correo electrónico, búsqueda pagada, redes sociales orgánicas, etc.) que impulsó la *compra* detrás de cada reseña. Esto reutiliza tus datos de atribución y es genuinamente útil para ver qué canales traen a clientes que luego dejan reseñas — pero no es un registro de cómo el cliente encontró el formulario de reseña en sí mismo. Spwig no rastrea eso por separado; consulta "Lo que hace y no hace el recorrido" más adelante en este manual.

Dos listas completan el panel de control:

- **Productos más reseñados** — tus productos más reseñados, cada uno con su cantidad de reseñas y calificación promedio, vinculados directamente al producto.
- **Pendiente de moderación** — tus reseñas más recientes pendientes, para que puedas saltar directamente a cualquier cosa que necesite una decisión sin salirte del panel de control.

## La lista de reseñas

Haz clic en **Moderar reseñas** (o **Productos > Reseñas > Moderar reseñas**) para ver cada reseña como una tarjeta, con filtros sobre la lista.

![Lista de reseñas de productos con filtros y tarjetas de reseña pendiente](/static/core/admin/img/help/product-reviews/review-list.webp)

Cada tarjeta muestra la miniatura del producto, el título de la reseña, la calificación de estrellas, un sello de **Aprobada**/**Pendiente**, un sello de **Compra verificada** cuando corresponda, una vista previa del comentario, y quién lo escribió y cuándo.

### Filtros de reseñas

Usa el panel de filtros para reducir la lista:

- **Búsqueda** — coincide con el nombre del producto, el nombre de usuario del cliente o el título de la reseña
- **Calificación** — muestra solo reseñas con una calificación de estrellas específica (útil para investigar quejas de 1 estrella)
- **Aprobación** — separa rápidamente reseñas aprobadas de pendientes
- **Verificado** — filtra reseñas de clientes con un pedido confirmado para ese producto

La filtración ocurre de inmediato sin recargar la página.

## Aprobar y rechazar reseñas

Las reseñas no son visibles en tu tienda hasta que las apruebes. Puedes aprobar o rechazar reseñas individualmente o en masa.

### Acciones por lotes

1. En la lista de reseñas, marca las casillas al lado de las reseñas que desees actuar
2. Selecciona **Aprobar reseñas seleccionadas** o **Rechazar reseñas seleccionadas** del menú desplegable de acciones
3. Haz clic en **Ir**

Este es el camino más rápido para trabajar a través de un lote de nuevas reseñas.

### Revisión individual

1.

Haz clic en el icono de edición en una tarjeta de reseña, o en su título, para abrir la reseña
2.

Preserva todos los formatos de markdown, las rutas de imágenes, los bloques de código y los términos técnicos.

En la pestaña **Revisión**, marque o desmarque **¿Aprobado?**
3.

Haga clic en el botón de marca de verificación en el encabezado para guardar

## La página de edición de revisión

Abrir una revisión le brinda una vista con estilo de tablero centrada en esa revisión única: un encabezado con el nombre del producto, la calificación con estrellas, un sello de **Aprobado**/**Pendiente**, un sello de **Compra verificada** cuando corresponda, quién escribió la revisión y cuándo, y una fila de estadísticas (**Calificación**, **Votos útiles**, **Pedidos del cliente**, **Gasto total**) . Debajo de eso, los detalles están organizados en cuatro pestañas.

![Página de edición de revisión — pestaña de revisión con galería de imágenes](/static/core/admin/img/help/product-reviews/review-edit-review-tab.webp)

### Pestaña de revisión

Esta es la parte donde modera la revisión en sí misma:

- **Imágenes de revisión** — si el cliente adjuntó fotos, aparecen aquí como una galería de miniaturas; haga clic en cualquier miniatura para abrir la imagen en tamaño completo en una nueva pestaña. Las revisiones con imágenes son una señal de confianza fuerte para los compradores, por lo que vale la pena echarle un vistazo antes de aprobarla.
- **Calificación**, **Título**, **Comentario** — el contenido que el cliente envió
- **¿Aprobado?** — controla si la revisión es visible en su tienda
- **¿Compra verificada?** — marca la revisión como proveniente de un comprador confirmado; Spwig lo establece automáticamente cuando existe un pedido completado del producto (ver la pestaña **Compra**), pero puede anularlo aquí si es necesario
- **Imágenes** — la lista subyacente de URLs de imagen detrás de la galería anterior; normalmente no necesita tocarla, pero permanece editable para casos extremos (por ejemplo, eliminar una foto de una revisión con múltiples imágenes)

No puede editar el texto de la revisión — aprobar o rechazar, y gestionar las imágenes, es todo lo que controla aquí.

### Pestaña de Cliente y Trayectoria

![Página de edición de revisión — pestaña de Cliente y Trayectoria](/static/core/admin/img/help/product-reviews/review-edit-customer-tab.webp)

Esta pestaña le brinda contexto sobre quién dejó la revisión: órdenes totales, cuántas revisiones ha escrito, su calificación promedio dada, cuánto tiempo ha sido cliente y sus datos de contacto, con un enlace para abrir su registro completo de cliente.

Debajo de eso está la **trayectoria de tráfico** — los canales, campañas y referidores que trajeron a este cliente a su tienda, extraídos de sus datos de atribución y mostrados como una cronología.

#### Qué hace y qué no hace la "trayectoria"

Lea esta cronología como la **trayectoria de llegada y compra** del cliente — cómo originalmente encontró su tienda y luego compró. No es un registro de la visita en la que escribió esta revisión. Spwig no registra dónde estaba el cliente, o qué dispositivo o sesión usó, en el momento en que envió la revisión. Si la cronología muestra "Email > skincare-de-verano" tres semanas antes de la fecha de la revisión, eso le indica que la campaña de correo electrónico probablemente impulsó la *compra* — no dice nada sobre si el cliente volvió desde un resultado de búsqueda, un marcador, o un correo electrónico de seguimiento para dejar realmente la revisión. Trate esta pestaña como contexto de marketing útil, no como un registro literal de la presentación de la revisión.

### Pestaña de Compra

![Página de edición de revisión — pestaña de Compra](/static/core/admin/img/help/product-reviews/review-edit-purchase-tab.webp)

Esta pestaña lista cada pedido en el que el cliente compró el producto revisado: número de pedido, fecha, total, estado y el canal de compra para ese pedido. Si alguno de esos pedidos ha alcanzado un estado completado (enviado o entregado), verá una nota de confirmación de que se trata de una compra verificada — la misma señal que establece automáticamente **¿Compra verificada?** en la pestaña de Revisión.

Si no aparece ningún pedido coincidente aquí, el revisor compró el producto antes de que su tienda registrara pedidos en Spwig, o nunca compró realmente el producto — algo que vale la pena conocer antes de decidir cuánto peso darle a la revisión.

### Pestaña Avanzada

Metadatos que rara vez necesita tocar: **Cantidad de ayuda** (cuántos clientes marcaron la revisión como útil), el origen de la importación si la revisión fue migrada desde otra plataforma, y las horas de creación/actualización.

## Consejos

Preserve all markdown formatting, image paths, code blocks, and technical terms.

- Verifica primero la lista **Pendiente de moderación** en el panel de control, es la forma más rápida de ver qué necesita una decisión sin abrir la lista completa de revisiones
- Un grupo de revisiones con 1 estrella en el mismo producto en el gráfico **Distribución de calificaciones** es una señal clara de investigar el embalaje, la calidad del producto o su descripción
- Usa el filtro **Verificado** al decidir cómo manejar revisiones dudosas: los comentarios de clientes con un pedido confirmado tienen más peso en cualquier disputa
- Aprueba las revisiones rápidamente, incluidas las críticas: una revisión negativa visible junto con ninguna respuesta puede verse peor que una queja manejada, y las revisiones que tardan en aparecer disuaden a los clientes de dejar comentarios futuros
- No leas en exceso el **Viaje de origen del tráfico** o el gráfico **Canal de compra de los revisores** del panel de control: ambos describen cómo llegó el cliente y compró, no cómo llegó para escribir la revisión
- Las revisiones con fotos merecen una revisión más detallada antes de aprobarlas; las fotos del producto de clientes reales son algunos de los contenidos más persuasivos en tu tienda