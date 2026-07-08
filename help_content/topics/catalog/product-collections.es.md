---
title: Colecciones de productos
---

Las colecciones te permiten agrupar productos para mostrarlos en tu tienda en línea. A diferencia de las categorías — que organizan tu catálogo completo en una jerarquía permanente — las colecciones son agrupaciones flexibles y cuidadosamente seleccionadas que creas para un propósito específico. Una colección podría destacar nuevos productos, mostrar artículos para una campaña estacional o presentar una selección cuidadosamente elegida de bestsellers.

Navega a **Catálogo > Colecciones** para gestionar tus colecciones.

## Colecciones vs categorías

Tanto las categorías como las colecciones agrupan productos, pero tienen propósitos diferentes:

| | Categorías | Colecciones |
|---|---|---|
| **Propósito** | Estructura permanente del catálogo | Agrupaciones flexibles y cuidadosamente seleccionadas |
| **Jerarquía** | Sí — estructura anidada de padre/hijo | No — agrupaciones planas |
| **Productos por grupo** | Cada producto pertenece a una categoría | Un producto puede aparecer en muchas colecciones |
| **Uso típico** | Menú de navegación de la tienda, buscar por departamento | Páginas de inicio, campañas, conjuntos destacados |

Usa categorías para "cómo está organizada tu tienda" y colecciones para "lo que quieres destacar ahora".

## Tipos de colecciones

Al crear una colección, elige un tipo que se ajuste a cómo deseas gestionar la lista de productos:

| Tipo | Cómo se añaden los productos |
|---|---|
| **Selección manual** | Tú eliges exactamente qué productos aparecerán, uno por uno |
| **Reglas automáticas** | Los productos se añaden automáticamente según criterios que defines |
| **Productos destacados** | Una selección editorial cuidadosamente seleccionada, gestionada manualmente |
| **Estacionales** | Una selección basada en el tiempo, normalmente gestionada manualmente para campañas |

Los tipos de selección manual y productos destacados te dan un control preciso. Las colecciones automáticas pueden crecer con tu catálogo sin mantenimiento continuo.

## Crear una colección

1. Navega a **Catálogo > Colecciones**
2. Haz clic en **+ Añadir Colección**
3. Rellena la sección **Información básica**:
   - **Nombre** — el nombre de la colección tal y como aparecerá en tu tienda en línea
   - **Slug** — la ruta URL de la página de la colección (rellenada automáticamente desde el nombre; puedes personalizarla)
   - **Descripción** — una descripción mostrada en la página de la colección en tu tienda en línea
4. Selecciona un **Tipo de Colección**
5. Añade productos:
   - Para los tipos **Selección manual** y **Productos destacados**: usa el campo **Productos** para buscar y añadir productos
   - Para el tipo **Automático**: define los criterios en el campo **Criterios automáticos**
6. Sube imágenes:
   - **Imagen** — la imagen principal de la colección usada en las páginas de listado y miniaturas
   - **Imagen de banner** — una imagen de banner más ancha mostrada en la parte superior de la página de la colección
7. Configura los campos **SEO** (opcional pero recomendado):
   - **Título meta** — el título de la página mostrado en los resultados de búsqueda
   - **Descripción meta** — la descripción mostrada debajo del título en los resultados de búsqueda
8. Establece **Opciones de visualización**:
   - **Activo** — controla si la colección es visible en tu tienda en línea
   - **Destacado** — marca la colección para su ubicación destacada en tu tema
   - **Orden de clasificación** — controla el orden en el que aparecen las colecciones en las páginas de listado (los números más bajos aparecen primero)
9. Haz clic en **Guardar**

## Añadir productos a una colección

Para colecciones manuales, usa el campo de autocompletar **Productos** para buscar en tu catálogo y seleccionar artículos. Puedes añadir tantos productos como necesites — no hay límite.

Los productos pueden pertenecer a múltiples colecciones al mismo tiempo. Por ejemplo, un producto podría estar en tu colección "Venta de verano" y en tu colección "Bestsellers" sin conflicto alguno.

## Mostrar colecciones en tu tienda en línea

Cada colección obtiene automáticamente su propia página en `/collection/{slug}/`. Puedes enlazar a las páginas de las colecciones desde tu menú de navegación, el constructor de páginas o banners promocionales.

La bandera **Destacado** se usa por tu tema para determinar qué colecciones aparecen en lugares destacados — por ejemplo, una cuadrícula de colecciones destacadas en la página de inicio. Consulta la documentación de tu tema para entender exactamente cómo se muestran las colecciones destacadas.

## Gestionar la visibilidad de las colecciones

- **Está activo** controla si la página de colección está accesible públicamente.

Una colección inactiva se oculta a los clientes, pero se conserva en el administrador para que puedas reactivarla más tarde.
- **Orden de clasificación** determina el orden en el que aparecen las colecciones en las páginas de listado.

Asigna números más bajos a las colecciones que desees que aparezcan primero.

## SEO para colecciones

Cada colección tiene sus propios campos **Título meta** y **Descripción meta**. Estos controlan lo que aparece en los resultados de los motores de búsqueda cuando alguien encuentre tu página de colección. Si dejas estos campos en blanco, tu tema normalmente recurrirá al nombre y descripción de la colección.

Los buenos títulos de SEO para colecciones son descriptivos y específicos:
- "Vestidos de verano 2026 — Estilos florales y ligeros" funciona mejor que "Colección de verano"
- "Zapatos de running para hombres — Ligeros y transpirables" funciona mejor que "Zapatos de running"

## Consejos

- Mantén los nombres de las colecciones cortos y claros — aparecen como títulos de página y texto de enlace en la navegación de tu tienda en línea
- Usa colecciones estacionales o de campañas con un plan de inicio y fin: crea la colección, actívala cuando comience la campaña y desactívala (en lugar de eliminarla) cuando termine, para que puedas referirte a ella más tarde
- El campo **Orden de clasificación** vale la pena establecerlo deliberadamente — el valor predeterminado es 0 para todas las colecciones, lo que significa que se ordenan alfabéticamente. Asigna números específicos para controlar qué colecciones aparecen con más prominencia
- Una colección sin productos mostrará una página vacía a los clientes — ya sea que agregues productos antes de activarla, o dejes la colección inactiva hasta que esté lista
- Verifica la bandera **Es destacada** solo para las colecciones que realmente desees destacar; la mayoría de los temas reservan espacios destacados para un pequeño número de colecciones y la visualización puede verse abrumadora si demasiadas están marcadas