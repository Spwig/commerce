---
title: Marcas de productos
---

Las marcas te permiten asociar productos con su fabricante o etiqueta y dar a los clientes una forma de navegar por tu tienda por marcas. Cada marca tiene su propia página en tu tienda en línea donde los clientes pueden descubrir todos los productos de esa marca, leer la historia de la marca y seguir un enlace a la página web de la marca.

Navega a **Catálogo > Marcas** para gestionar tus marcas.

## ¿Por qué usar marcas

Las marcas tienen dos propósitos en Spwig:

1. **Organización** — los productos se etiquetan con una marca, lo que facilita que los clientes leales a una etiqueta específica encuentren lo que buscan
2. **Merchandising** — las páginas de marca son un espacio dedicado para mostrar la historia de la marca, su logotipo y su gama completa de productos, lo que puede mejorar la conversión para compradores conscientes de la marca

Las marcas también funcionan con el sistema de promociones — puedes realizar una venta que se aplique a todos los productos de una marca específica sin tener que seleccionar los productos individualmente.

## Crear una marca

1. Navega a **Catálogo > Marcas**
2. Haz clic en **+ Añadir Marca**
3. Rellena la sección **Información Básica**:
   - **Nombre** — el nombre de la marca como aparecerá en tu tienda en línea (debe ser único)
   - **Slug** — la ruta URL de la página de la marca (rellenada automáticamente desde el nombre; puedes personalizarla)
   - **Descripción** — una breve descripción de la marca mostrada en la página de la marca
   - **Sitio web** — la URL del sitio web oficial de la marca (opcional — mostrada como un enlace en la página de la marca)
4. Añade activos de la marca:
   - **Logotipo** — la imagen del logotipo de la marca, utilizada en listados de marcas y en la página de la marca
   - **Imagen de banner** — una imagen ancha mostrada en la parte superior de la página de la marca
5. Escribe la **Historia de la marca** (opcional) — un artículo editorial más largo sobre la historia, valores o lo que hace especial a la marca. Esto aparece en la página de la marca en tu tienda en línea y puede ser una forma efectiva de contar la historia de la marca a los clientes interesados.
6. Configura los campos **SEO**:
   - **Título meta** — el título de la página mostrado en los resultados de los motores de búsqueda
   - **Descripción meta** — la breve descripción mostrada debajo del título en los resultados de búsqueda
7. Establece opciones de visualización:
   - **Mostrar página de marca** — controla si la marca tiene una página accesible públicamente. Desmarcar para ocultar una marca de la tienda en línea manteniéndola en el sistema.
   - **Activa** — controla si la marca está disponible para asignar a productos y visible en la tienda
   - **Destacada** — marca la marca para un lugar destacado en tu tema (por ejemplo, una fila de logotipos de marcas en la página de inicio)
8. Haz clic en **Guardar**

## Asignar productos a una marca

Las marcas se asignan en registros de productos individuales, no desde la página de gestión de marcas. Para asignar una marca a un producto:

1. Navega a **Catálogo > Productos** y abre el producto
2. En el formulario del producto, busca el campo **Marca**
3. Busca y selecciona la marca adecuada
4. Guarda el producto

Una vez que se asigna una marca, el producto aparecerá automáticamente en la página de la tienda en línea de esa marca.

## Páginas de marca en tu tienda en línea

Cada marca con **Mostrar página de marca** habilitado obtiene su propia página en `/brand/{slug}/`. La página muestra:

- El logotipo de la marca y la imagen de banner
- El nombre de la marca y la descripción
- La historia de la marca (si se proporciona)
- Un enlace al sitio web de la marca (si se proporciona)
- Todos los productos activos asignados a esa marca

Los clientes pueden llegar a las páginas de marca haciendo clic en el nombre de la marca en una página de producto, o a través de enlaces que crees en tu navegación o constructor de páginas.

## SEO para páginas de marca

Rellenar los campos **Título meta** y **Descripción meta** para cada marca ayuda a que tus páginas de marca aparezcan bien en los resultados de búsqueda. Los títulos de SEO efectivos para marcas suelen combinar el nombre de la marca con lo que vende la marca:

| Marca | Buen título meta |
|---|---|
| Levi's | "Levi's Jeans & Clothing — Official Store" |
| KitchenAid | "KitchenAid Stand Mixers & Kitchen Appliances" |
| Patagonia | "Patagonia Outdoor Clothing & Gear" |

Si dejas los campos de SEO en blanco, tu tema recurrirá al nombre de la marca.

### Generación automática de SEO

Si **SEO Auto Generado** está habilitado en una marca, Spwig generará automáticamente el contenido del título meta y la descripción cuando se guarde la marca.

Esto es conveniente para tiendas con muchas marcas, pero te da menos control sobre la redacción exacta.

Siempre puedes sobrescribir el contenido generado escribiendo directamente en los campos y desactivando el interruptor de generación automática.

## Marcas destacadas

La bandera **Is Featured** es utilizada por los temas para mostrar una fila o cuadrícula curada de logotipos de marcas — comúnmente en la página de inicio. Solo un pequeño número de marcas debe destacarse a la vez; consulta la documentación de tu tema para entender cuántas marcas destacadas se muestran de forma óptima.

## Consejos

- Sube un logotipo de marca como PNG o WebP con fondo transparente — se mostrará limpiamente en cualquier color de fondo de tu tema
- Escribe una historia atractiva de la marca incluso para marcas menos conocidas; los clientes que no están familiarizados con una marca valoran el contexto que les ayuda a decidir si los productos son adecuados para ellos
- Si realizas promociones dirigidas a marcas específicas, asegúrate de que el nombre de la marca en Spwig coincida exactamente — las promociones usan la relación de marca en los productos para determinar la elegibilidad
- Desactiva una marca en lugar de eliminarla cuando dejes de vender sus productos — la eliminación elimina la referencia de la marca de todos los productos asociados, mientras que la desactivación preserva la historia
- Usa la bandera **Is Featured** con moderación; una página de inicio que muestra 20 logotipos de marcas pierde impacto en comparación con 6–8 elegidos cuidadosamente