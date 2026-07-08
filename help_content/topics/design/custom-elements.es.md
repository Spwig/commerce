---
title: Elementos personalizados
---

Los elementos personalizados te permiten crear bloques reutilizables del constructor de páginas que se adapten a las necesidades de tu tienda. Diseñas un elemento visualmente usando las herramientas existentes del constructor de páginas, y luego, opcionalmente, lo conectas a datos en vivo de la tienda — como nombres de productos, precios o imágenes — para que el elemento se llene automáticamente con contenido real cuando se coloque en una página. Una vez creado, tus elementos personalizados aparecerán en la biblioteca de elementos del constructor de páginas junto a los bloques preinstalados.

![Biblioteca de elementos personalizados](/static/core/admin/img/help/custom-elements/custom-elements-list.webp)

## Cuándo usar elementos personalizados

Los elementos personalizados son más valiosos cuando te encuentras construyendo repetidamente la misma disposición. En lugar de recrear una "tarjeta de producto destacado" desde cero en cada página, la construyes una vez como un elemento personalizado y la colocas donde la necesites. Si el elemento está vinculado a datos, automáticamente obtiene información actual de productos — no se necesitan actualizaciones manuales cuando cambien los precios o los nombres.

Usos comunes:

- Tarjetas de resaltado de productos que muestran nombre, precio y imagen principal
- Bloques de promoción de categorías con banner, título y enlace
- Paneles de exhibición de marcas con logotipo y descripción
- Resúmenes de entradas de blog con imagen destacada, título y extracto

## Crear un nuevo elemento personalizado

1. Navega a **Diseño > Elementos personalizados**
2. Haz clic en **+ Agregar elemento personalizado**
3. Spwig crea inmediatamente un borrador del elemento y abre el **Constructor visual** — no es necesario completar un formulario primero
4. En el Constructor visual, construye el diseño del elemento usando las herramientas del constructor de páginas disponibles
5. Cuando estés satisfecho con el diseño, configura la configuración del elemento (nombre, vinculación de datos, icono) en el panel lateral
6. Activa **Activo** cuando estés listo para publicar el elemento en la biblioteca
7. Guarda el elemento

El elemento ahora está disponible en el panel de elementos del constructor de páginas bajo la categoría que asignaste.

## El constructor visual

El Constructor visual es un lienzo dedicado para diseñar tu elemento. Funciona como el constructor de páginas estándar, pero se centra en un solo elemento en lugar de toda una página. Puedes:

- Agregar y organizar elementos secundarios (bloques de texto, imágenes, contenedores, etc.)
- Establecer el estilo, el espaciado y el diseño de cada elemento secundario
- Previsualizar cómo se verá el elemento con datos de ejemplo

Los cambios en el Constructor visual se guardan directamente en la definición del elemento. No hay un paso de publicación separado — al guardar en el constructor, el elemento se actualiza inmediatamente para cualquier página que ya lo use.

## Configurar la configuración del elemento

Cada elemento personalizado tiene estas configuraciones:

| Campo | Descripción |
|-------|-------------|
| **Nombre** | Nombre que se muestra en la biblioteca de elementos |
| **Slug** | Identificador seguro para URL, generado automáticamente a partir del nombre |
| **Descripción** | Nota opcional sobre para qué sirve este elemento |
| **Modelo objetivo** | El modelo de tienda del cual se vincularán datos (ver más abajo) |
| **Icono** | Icono que se muestra en la biblioteca de elementos |
| **Categoría** | Agrupa elementos relacionados en la biblioteca |
| **Activo** | Si el elemento está disponible en el constructor de páginas |

## Vinculación de datos

La vinculación de datos conecta partes de la disposición de tu elemento a datos en vivo de la tienda. Cuando un editor de páginas coloca un elemento vinculado a datos en una página, elige un registro específico (por ejemplo, un producto), y todos los campos vinculados se llenan automáticamente desde ese registro.

### Elegir un modelo objetivo

La configuración **Modelo objetivo** determina qué tipo de datos de la tienda puede mostrar el elemento. Los modelos disponibles son:

| Modelo | Qué proporciona |
|-------|-----------------|
| **Producto** | Nombre, precio, estado de stock, imágenes, descripción, SKU, categoría, marca y más |
| **Categoría** | Nombre, descripción, imagen, banner, cantidad de productos y URL |
| **Marca** | Nombre, logotipo, descripción, historia de la marca y URL |
| **Entrada de blog** | Título, extracto, imagen destacada, autor, fecha de publicación y URL |

Deja **Modelo objetivo** vacío para crear un elemento estático sin datos dinámicos. Los elementos estáticos son útiles para componentes de diseño fijos, como banners decorativos o espaciadores de diseño.

### Cómo funcionan los vinculos


Dentro del Visual Builder, puedes marcar elementos secundarios individuales como enlazados a datos seleccionando el campo del modelo que deben mostrar.

Por ejemplo:
- Un elemento secundario de **texto** puede vincularse a **Nombre del producto**, para mostrar el nombre del producto seleccionado
- Un elemento secundario de **imagen** puede vincularse a **Imagen principal**, para mostrar la foto principal del producto
- Un elemento secundario de **texto** puede vincularse a **Precio**, para reflejar siempre el precio actual

Cada vinculación mapea un campo de contenido de un elemento a un campo del modelo. Puedes agregar múltiples vinculaciones a un solo elemento personalizado — por ejemplo, vincular un bloque de texto a **Nombre del producto** y un bloque de imagen separado a **Imagen principal** al mismo tiempo.

### Preset de miniaturas de imagen

Para los vinculados de imagen, puedes especificar opcionalmente un **Preset de miniatura** (como `thumbnail` o `medium`). Esto controla el tamaño de la imagen que se carga, ayudando a que las páginas se carguen más rápido al servir la imagen del tamaño adecuado para el diseño del elemento.

## Desactivar y reactivar elementos

Desactivar un elemento lo elimina de la biblioteca de elementos, por lo que no puede agregarse a nuevas páginas. Las páginas existentes que ya usan el elemento no se ven afectadas — el elemento sigue siendo renderizado en esas páginas.

Para desactivar:
1. Navega a **Diseño > Elementos personalizados**
2. Haz clic en el nombre del elemento
3. Desmarca **Activo**
4. Guarda

Para reactivar, sigue los mismos pasos y vuelve a marcar **Activo**.

## Filtros de la biblioteca de elementos

La lista de elementos admite filtrado por:
- **Activo / Inactivo** — mostrar solo elementos publicados o solo elementos en borrador
- **Modelo objetivo** — filtrar por el modelo al que un elemento está vinculado
- **Categoría** — filtrar por categoría de elemento
- **Buscar** — buscar por nombre, slug o descripción

Esto ayuda cuando tienes muchos elementos personalizados y necesitas encontrar uno específico rápidamente.

## Ejemplo: tarjeta de resaltado de producto

**Objetivo:** Un elemento de tarjeta que muestre la imagen principal, el nombre y el precio de un producto.

| Configuración | Valor |
|---------|-------|
| Nombre | Tarjeta de resaltado de producto |
| Modelo objetivo | Producto |
| Categoría | Productos |
| Icono | fas fa-box |

En el Visual Builder, agrega:
- Un elemento de **Imagen** vinculado a **Imagen principal** con el preset de miniatura `medium`
- Un elemento de **Texto** vinculado a **Nombre del producto**
- Un elemento de **Texto** vinculado a **Precio**

Una vez guardado y activado, el elemento aparece en el constructor de páginas en la categoría Productos. Cuando un editor de páginas lo agrega a una página, elige qué producto destacar y la tarjeta se rellena automáticamente.

## Consejos

- Dales a los elementos nombres descriptivos que incluyan su propósito y el tipo de datos — por ejemplo, "Tarjeta de resaltado de producto" en lugar de "Tarjeta 1" — para que la biblioteca siga siendo fácil de navegar a medida que crece
- Usa el campo **Categoría** para agrupar elementos relacionados (Productos, Blog, Promociones) — esto mantiene la biblioteca de elementos organizada para tus editores de páginas
- Prueba elementos enlazados a datos agregándolos a una página en borrador y seleccionando un registro real antes de publicar, para confirmar que el vinculado esté obteniendo la información correcta
- Desactiva elementos obsoletos en lugar de eliminarlos — esto preserva cualquier página que aún los haga referencia y te da la opción de reactivarlos más tarde
- Los elementos estáticos (sin modelo objetivo) son ideales para patrones de diseño que reutilizas en toda la web, como divisores, paneles de llamado a la acción o espacios con marca