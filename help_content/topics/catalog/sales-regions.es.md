---
title: Regiones de ventas
---

Las regiones de ventas le permiten definir mercados geográficos para su tienda y controlar qué productos están disponibles en cada región. Esto es útil cuando vende en varios países o territorios y necesita catálogos de productos diferentes, divisas regionales o disponibilidad de stock por ubicación.

## ¿Qué es una región de ventas?

Una región de ventas es un área geográfica con nombre compuesta por uno o más países. Cada región tiene una moneda predeterminada, una prioridad y puede estar vinculada a uno o más almacenes. Cuando un cliente navega por su tienda, Spwig determina su región según su ubicación y aplica la moneda y las reglas de visibilidad de productos adecuadas.

Casos de uso comunes:
- Mostrar solo productos disponibles localmente a los clientes de cada país
- Asignar divisas predeterminadas específicas de la región (por ejemplo, NZD para clientes de Nueva Zelanda)
- Controlar qué almacenes cumplen órdenes para cada región
- Ocultar productos que aún no están disponibles en ciertos mercados

## Crear una región de ventas

1. Navegue a **Inventario > Regiones de ventas**. Si no lo ve, active **Habilitar múltiples almacenes** en **Configuración > Configuración de la tienda > E-commerce** para revelar el elemento del menú — no necesita usar realmente múltiples almacenes para esto, solo desbloquea el vínculo. También puede ir directamente a `/admin/catalog/salesregion/`.
2. Haga clic en **+ Añadir región de ventas**
3. Complete los detalles de la región:

| Campo | Descripción | Ejemplo |
|-------|-------------|---------|
| **Nombre de la región** | Nombre de visualización de esta región | `Pacífico-Ásia` |
| **Código de región** | Identificador único corto | `APAC` |
| **Países** | Códigos ISO de países incluidos en esta región | `["NZ", "AU", "SG", "FJ"]` |
| **Moneda predeterminada** | Código ISO de moneda para esta región | `NZD` |
| **Prioridad** | Las regiones con mayor prioridad se coinciden primero | `10` |
| **Activo** | Si esta región está en uso actualmente | Marcado |

4. Haga clic en **Guardar**

### Códigos de país

Ingrese los países como una lista JSON de códigos de dos caracteres ISO. Por ejemplo:
- Nueva Zelanda y Australia: `["NZ", "AU"]`
- Solo Singapur: `["SG"]`
- Todo Europa: `["DE", "FR", "IT", "ES", "NL", "BE", "AT", "CH", "SE", "NO", "DK", "FI", "PL"]`

### Prioridad

Si el país de un cliente coincide con más de una región, se utiliza la región con el número de prioridad más alto. Establezca una prioridad más alta para regiones más específicas (por ejemplo, otorgarle a `NZ` una prioridad de 20 y a `APAC` una prioridad de 10 para que los clientes de Nueva Zelanda se asignen primero a la región `NZ`).

## Controlar la visibilidad de los productos por región

Por defecto, cada producto es visible en todas las regiones. Para restringir un producto, ábralo en **Productos > Todos los productos** y establezca el campo **Disponibilidad por región** (en la sección de estado) para permitirlo solo en regiones específicas o en todas las regiones excepto específicas, luego elija las regiones en la tabla debajo de este campo.

Esto también determina qué ven los compradores fuera de las regiones disponibles del producto — si el producto se oculta por completo de las listas, o se muestra con una notificación de "No se envía a [región]". Consulte la guía **Disponibilidad por región** para el recorrido completo, incluida esta configuración de visualización y el selector de envío al cliente final.

## Divisas regionales

Cada región tiene una moneda predeterminada. Si su tienda admite explícitamente más de una moneda (**Configuración > Múltiples divisas**), la moneda mostrada por el cliente cambia a la moneda predeterminada de su región cada vez que su región cambia — ya sea desde el aviso automático de región o desde el selector de envío. Las tiendas con solo una moneda, o que no han activado deliberadamente múltiples divisas, siempre muestran esa única moneda independientemente de la región.

Para configurar precios en múltiples divisas, configure las tasas de cambio bajo **Configuración > Tasas de cambio**. Los precios se pueden convertir automáticamente o establecerse manualmente por moneda.

Para más detalles sobre almacenes, consulte el tema de ayuda **Inventario y almacenes**.

## Consejos

- Mantenga los códigos de región cortos y descriptivos (``NZ``, ``APAC``, ``EU``, ``US``) — se utilizan internamente y en registros.
- Use números de prioridad más altos para regiones más pequeñas y específicas para que tengan prioridad sobre regiones más amplias.
- Si solo vende a un país, no necesita configurar regiones en absoluto — Spwig funciona perfectamente con un catálogo global único.
- Solo establezca la **Disponibilidad por región** de un producto lejos de **Disponible en todas las regiones** cuando realmente necesite restringirla — el valor predeterminado mantiene los productos universalmente disponibles sin necesidad de mantenimiento.
- Revise las reglas de región de cada producto cada vez que agregue una nueva región de ventas, para que las restricciones coincidan con lo que intente.
- Agregue el selector de destino a su encabezado (consulte la guía **Disponibilidad por región**) para que pueda cambiar de región y verificar que los productos restringidos funcionen según lo esperado.