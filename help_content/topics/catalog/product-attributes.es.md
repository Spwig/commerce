---
title: Atributos de producto
---

Los atributos de producto definen las dimensiones a lo largo de las cuales un producto puede variar — por ejemplo, Tamaño, Color o Material. Una vez que hayas creado un atributo y sus valores posibles, puedes asignarlo a cualquier producto variable y Spwig generará el selector de variaciones que los clientes usan al finalizar la compra.

Navega a **Catálogo > Atributos de producto** para gestionar los atributos y sus valores.

## Cómo funcionan los atributos

Los atributos son reutilizables en todo tu catálogo. Los creas una vez y los asignas a tantos productos como necesites. Cada atributo tiene:

- Un **nombre** que lo identifica (por ejemplo, "Tamaño")
- Un **tipo de visualización** que controla cómo aparece el selector en la página del producto
- Uno o más **valores** que representan las opciones disponibles (por ejemplo, "Pequeño", "Mediano", "Grande")

Cuando asignas un atributo a un producto, también especificas cuáles de sus valores están disponibles para ese producto en particular. Esto significa que un atributo de "Tamaño" podría tener valores de S a 3XL, pero una camiseta específica podría ofrecer solo S, M y L.

## Tipos de visualización de atributos

El campo **Tipo** en un atributo controla cómo aparece el widget de selección en la página del producto de tu tienda en línea:

| Tipo | Apariencia | Mejor para |
|---|---|---|
| **Selector de desplazamiento** | Un menú desplegable que el cliente abre para elegir un valor | Atributos con muchos valores (por ejemplo, un rango de tallas con 10+ tallas) |
| **Muestra de color** | Círculos o cuadrados de color que el cliente hace clic | Atributos de color donde la identificación visual ayuda |
| **Grupo de botones** | Botones en forma de píldora mostrados en línea | Atributos con un número pequeño de valores (por ejemplo, S, M, L, XL) |
| **Botones de opción** | Lista tradicional de botones de opción | Cualquier atributo donde desees un diseño de lista claro y accesible |

Elige el tipo de visualización que se ajuste a cómo tus clientes piensan sobre el atributo. Para el color, las muestras suelen ser mucho mejores que un selector de desplazamiento. Para el tamaño, los grupos de botones funcionan bien cuando hay menos de 8 opciones.

## Crear un atributo

1. Navega a **Catálogo > Atributos de producto**
2. Haz clic en **+ Añadir atributo de producto**
3. Introduce el **Nombre** (por ejemplo, `Tamaño`, `Color`, `Material`)
4. El **Slug** se llena automáticamente — puedes dejarlo así
5. Selecciona el **Tipo** (Selector de desplazamiento, Muestra de color, Grupo de botones o Botones de opción)
6. Marca **Es obligatorio** si los clientes deben seleccionar este atributo antes de poder añadir el producto a su carrito — esto es adecuado para la mayoría de los atributos de tamaño y color
7. Establece un **Orden de clasificación** — los atributos con números más bajos aparecen primero en el selector de variaciones en la página del producto
8. Añade valores de atributo directamente en la sección **Valores** (ver más abajo)
9. Haz clic en **Guardar**

## Añadir valores de atributo

Los valores de atributo son las opciones individuales dentro de un atributo. Puedes añadirlos directamente mientras creas o editas un atributo, usando el formulario de valores en línea en la parte inferior de la página de detalles del atributo.

Para cada valor:

- **Valor** — la etiqueta de visualización (por ejemplo, `Pequeño`, `Rojo`, `Algodón`)
- **Slug** — se llena automáticamente desde el valor; se usa en URLs e identificadores de variantes
- **Color en Hex** — solo relevante para los atributos de tipo **Muestra de color**. Introduce un código de color en hex (por ejemplo, `#FF0000` para rojo) para que la muestra muestre el color correcto.
- **Orden de clasificación** — controla el orden en que aparecen los valores en el selector. Asigna números más bajos a los valores que desees que aparezcan primero.

### Ordenar los valores lógicamente

Para atributos de tamaño, establece el orden de clasificación para que los tamaños vayan de pequeño a grande:

| Valor | Orden de clasificación |
|---|---|
| XS | 1 |
| S | 2 |
| M | 3 |
| L | 4 |
| XL | 5 |
| 2XL | 6 |

Para atributos de color, podrías ordenarlos alfabéticamente o agrupar colores similares — lo que más sentido tenga para tus clientes.

## Gestionar valores de atributo de forma independiente

También puedes gestionar los valores de atributo de forma independiente en **Catálogo > Valores de atributo**. Esta lista es útil cuando necesitas encontrar o actualizar un valor específico en tu catálogo sin abrir cada atributo individualmente. La lista se puede filtrar por nombre de atributo.

## Asignar atributos a productos

Los atributos se asignan a nivel de producto, no de forma global.

Para agregar un atributo a un producto:

1. Navegue a **Catálogo > Productos** y abra un producto variable
2. En la pestaña **Variaciones**, encuentre la sección **Atributos**
3. Seleccione el atributo que desea agregar
4. Elija cuáles de los valores del atributo están disponibles para este producto
5. Guarde el producto — Spwig generará las combinaciones de variantes correspondientes

Para una guía detallada sobre la configuración de variantes de producto, consulte el tema de ayuda **Product Variants**.

## Ejemplos prácticos

### Ejemplo: Atributo de tamaño de ropa

| Campo | Valor |
|---|---|
| Nombre | Tamaño |
| Tipo | Grupo de botones |
| Es obligatorio | Sí |
| Orden de clasificación | 1 |
| Valores | XS (1), S (2), M (3), L (4), XL (5), 2XL (6) |

### Ejemplo: Atributo de muestra de color

| Campo | Valor |
|---|---|
| Nombre | Color |
| Tipo | Muestra de color |
| Es obligatorio | Sí |
| Orden de clasificación | 2 |
| Valores | Negro (#000000), Blanco (#FFFFFF), Azul marino (#001F5B), Rojo (#CC0000) |

### Ejemplo: Atributo de material

| Campo | Valor |
|---|---|
| Nombre | Material |
| Tipo | Selección desplegable |
| Es obligatorio | No |
| Orden de clasificación | 3 |
| Valores | 100% Algodón, Mezcla de algodón/poliéster, Lana merino, Lino |

## Consejos

- Cree atributos que representen decisiones reales de compra que los clientes tomen — si los clientes no necesitan elegirlo, quizás no sea necesario que sea un atributo
- Use nombres consistentes en todo su catálogo: si algunos productos usan "Colour" y otros usan "Color", tanto los clientes como su equipo encontrarán la inconsistencia confusa
- El orden de clasificación en ambos atributos y valores importa — coloque el atributo más importante primero (normalmente Tamaño o Color) y ordene los valores en una secuencia lógica
- El tipo de muestra de color requiere códigos hexadecimales precisos; pruebe los colores en un selector de color del navegador antes de guardar para asegurarse de que la muestra coincida con el color real del producto
- Si necesita renombrar un atributo (por ejemplo, de "Color" a "Colour"), actualice el campo **Nombre** en lugar de crear un nuevo atributo — cambiar el nombre no afecta las asignaciones existentes de productos