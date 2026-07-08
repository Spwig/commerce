---
title: Regiones de ventas
---

Las regiones de ventas te permiten definir mercados geográficos para tu tienda y controlar qué productos están disponibles en cada región. Esto es útil cuando vendes en múltiples países o territorios y necesitas catálogos de productos diferentes, monedas regionales o disponibilidad de stock por ubicación.

## ¿Qué es una región de ventas?

Una región de ventas es un área geográfica con nombre compuesta por uno o más países. Cada región tiene una moneda predeterminada, una prioridad y puede vincularse a uno o más almacenes. Cuando un cliente navega por tu tienda, Spwig determina su región basándose en su ubicación y aplica las reglas de moneda y visibilidad de productos adecuadas.

Casos de uso comunes:
- Mostrar solo productos disponibles localmente a los clientes de cada país
- Asignar monedas predeterminadas específicas de la región (por ejemplo, NZD para clientes de Nueva Zelanda)
- Controlar qué almacenes cumplen pedidos para cada región
- Ocultar productos que aún no estén disponibles en ciertos mercados

## Crear una región de ventas

1. Navega a **Catálogo > Regiones de ventas**
2. Haz clic en **+ Agregar región de ventas**
3. Llena los detalles de la región:

| Campo | Descripción | Ejemplo |
|-------|-------------|---------|
| **Nombre de la región** | Nombre de visualización para esta región | `Asia-Pacifico` |
| **Código de región** | Identificador único corto | `APAC` |
| **Países** | Códigos de país ISO incluidos en esta región | `["NZ", "AU", "SG", "FJ"]` |
| **Moneda predeterminada** | Código de moneda ISO para esta región | `NZD` |
| **Prioridad** | Las regiones con mayor prioridad se coinciden primero | `10` |
| **Activo** | Si esta región está actualmente en uso | Marcado |

4. Haz clic en **Guardar**

### Códigos de país

Ingresa países como una lista JSON de códigos ISO de dos letras. Por ejemplo:
- Nueva Zelanda y Australia: `["NZ", "AU"]`
- Solo Singapur: `["SG"]`
- Todo Europa: `["DE", "FR", "IT", "ES", "NL", "BE", "AT", "CH", "SE", "NO", "DK", "FI", "PL"]`

### Prioridad

Si el país del cliente coincide con más de una región, se usa la región con el número de prioridad más alto. Establece una prioridad más alta para regiones más específicas (por ejemplo, asigna a `NZ` una prioridad de 20 y a `APAC` una prioridad de 10 para que los clientes de Nueva Zelanda se coincidan primero con la región de Nueva Zelanda).

## Controlar la visibilidad de los productos por región

Por defecto, cada producto es visible en todas las regiones. Para restringir un producto a regiones específicas, usa registros de **Visibilidad de la región del producto**.

### Restringir un producto a regiones específicas

1. Navega a **Catálogo > Visibilidad de la región del producto**
2. Haz clic en **+ Agregar visibilidad de la región del producto**
3. Selecciona el **Producto**
4. Selecciona la **Región**
5. Establece **Visible** en on o off según sea necesario
6. Haz clic en **Guardar**

Una vez que exista cualquier registro de visibilidad para un producto, Spwig aplica las reglas. Los productos sin registros de visibilidad permanecen visibles en todas partes.

### Patrones comunes

**Limitar a una sola región**

Agrega un registro de visibilidad por región que desees admitir, estableciendo **Visible** en `Sí` para las regiones permitidas. Los clientes en otras regiones no verán el producto.

**Excluir de una región**

Agrega un solo registro de visibilidad para la región que deseas excluir y establece **Visible** en `No`. El producto permanece visible en todas las otras regiones.

### Editar la visibilidad desde la página del producto

También puedes gestionar la visibilidad por región directamente desde el formulario de edición del producto. En la sección **Visibilidad de la región** del producto, encontrarás una tabla en línea que muestra todas las regiones y su configuración de visibilidad para ese producto.

## Moneda regional

Cada región tiene una moneda predeterminada. Los clientes que navegan desde esa región ven los precios mostrados en la moneda de la región. La moneda utilizada se determina en el momento del pago.

Para configurar precios en múltiples monedas, configura las tasas de cambio bajo **Configuración > Tasas de cambio**. Los precios pueden convertirse automáticamente o establecerse manualmente por moneda.

## Vincular almacenes a regiones

Los almacenes se vinculan a regiones cuando creas o editas un almacén bajo **Catálogo > Almacenes**. Cada almacén pertenece a una región, lo que controla qué stock de la región se usa para cumplir pedidos.

Para obtener más detalles sobre los almacenes, consulte el tema de ayuda **Inventario y Almacenes**.

## Consejos

- Mantenga los códigos de región cortos y descriptivos (`NZ`, `APAC`, `EU`, `US`) — se utilizan internamente y en los registros.
- Use números de prioridad más altos para regiones más pequeñas y específicas para que tengan prioridad sobre regiones más amplias y genéricas.
- Si solo vende a un país, no es necesario configurar regiones en absoluto — Spwig funciona correctamente con un catálogo global único.
- Pruebe la visibilidad basada en la región previsualizando su tienda mientras filtra por una región específica en el administrador.
- Los registros de visibilidad de productos solo necesitan crearse cuando desee restringir productos. Dejar un producto sin registros de visibilidad lo hace disponible universalmente.
- Revise sus reglas de visibilidad siempre que agregue una nueva región para asegurarse de que las restricciones de productos existentes sean correctas.