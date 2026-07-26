---
title: Importación desde archivos CSV
---

La importación desde CSV es la ruta de migración por defecto para cualquier tienda a la que Spwig no se conecte directamente. Si vienes de BigCommerce, PrestaShop, Squarespace, Wix, una hoja de cálculo que hayas mantenido a mano o un sistema personalizado sin una API que Spwig entienda, esta es la opción en la que aterrizas — exporta tus datos a archivos CSV y sube los archivos aquí en lugar de conectarte en vivo.

Esta guía cubre cuándo usar CSV en lugar de una conexión de API, qué no puede traer, los cinco archivos involucrados, cómo prepararlos y cómo funciona el mapeo de columnas.

## Cuándo usar CSV en lugar de una conexión de API

Spwig se conecta directamente a WooCommerce, Shopify y Magento 2/Adobe Commerce — consulta [Data Migration Overview](migration-overview) para esos. Para cualquier otra plataforma, CSV es tu única opción; no hay integración directa para BigCommerce, PrestaShop, Squarespace o Wix. También es la opción correcta si estás consolidando datos desde una hoja de cálculo, desechando una tienda personalizada o quieres controlar exactamente qué se importa curando los archivos tú mismo.

## Qué no puede hacer el CSV

Antes de preparar nada, conoce qué deja atrás esta ruta — este es el mayor origen de sorpresas para los comerciantes que usan la importación CSV:

- **Ninguna imagen de producto.** Los productos se importan sin imágenes adjuntas; sube las imágenes después.
- **Ninguna variante.** Cada producto se crea como un producto simple. Reconstruye las estructuras de tamaño/color/estilo en Spwig después de la importación.
- **Ningún cupón.** Los códigos de descuento y promociones no son parte del formato CSV.
- **Ningún contenido de blog.** No hay un archivo CSV para publicaciones o artículos.

Ninguna de estas cosas bloquea la importación — solo significa que los productos necesitan trabajo posterior una vez que estén en Spwig. Consulta [After Your Migration](after-migration-review) para la lista completa de verificación post-importación.

## Los cinco archivos

El paso CSV del asistente ofrece cinco entradas de archivo, cada una con un botón **Descargar plantilla**. Comienza con estas plantillas en lugar de construir los archivos desde cero — garantizan los nombres de columna correctos y permiten que la detección automática haga más del trabajo en el paso 4.

| Archivo | ¿Es obligatorio? |
|---|---|
| Productos | **Obligatorio** |
| Categorías | Opcional |
| Clientes | Opcional |
| Pedidos | Opcional |
| Reseñas | Opcional |

Productos es el único archivo en el que Spwig insiste — el resto puede dejarse vacío si aún no tienes esos datos.

<!-- screenshots-needed:
- url: /en/admin/migration/migrationjob/wizard/step2/
  filename: csv-file-upload-step.webp
  description: Paso 2 con CSV seleccionado, mostrando las cinco entradas de archivo y sus botones Descargar plantilla
  save-to: core/static/core/admin/img/help/csv-import/
  viewport: 1440x900
-->

### Productos (Obligatorio)

| Columna | Descripción |
|---|---|
| `id` | Identificador único en tus datos de origen; no se muestra a los clientes. |
| `name` | El título del producto. **Esencial.** |
| `slug` | Versión amigable para URLs del nombre; se genera automáticamente desde `name` si está vacío. |
| `description` | La descripción mostrada en el punto de venta. |
| `price` | El precio regular del producto. **Esencial.** |
| `sku` | Unidad de control de inventario — usada para coincidir cuando **Saltar elementos existentes** está habilitado. |
| `stock_quantity` | Unidades actualmente en stock. |
| `category` | Nombre de la categoría a la que pertenece este producto. Debe coincidir con un `name` en tu archivo de categorías. |

### Categorías

| Columna | Descripción |
|---|---|
| `id` | Identificador único en tus datos de origen. |
| `name` | El nombre de la categoría. **Esencial.** |
| `slug` | Versión amigable para URLs del nombre; se genera automáticamente si está vacío. |
| `description` | Texto de descripción de la categoría. |
| `parent_id` | El `id` de la categoría padre de esta categoría. Vacío significa nivel superior. |

### Clientes

| Columna | Descripción |
|---|---|
| `id` | Identificador único en tus datos de origen. |
| `email` | Dirección de correo electrónico del cliente. **Esencial** — vincula pedidos y reseñas al cliente correcto. |
| `first_name` | Nombre del cliente. |
| `last_name` | Apellido del cliente. |
| `phone` | Número de teléfono del cliente. |

### Pedidos

Preserve all markdown formatting, image paths, code blocks, and technical terms.

| Columna | Descripción |
|---|---|
| `id` | Identificador único en sus datos de origen. |
| `customer_email` | Correo electrónico del cliente que realizó el pedido. **Esencial** — vincula el pedido a un registro de cliente. |
| `order_date` | La fecha en que se realizó el pedido. |
| `status` | El estado del pedido (por ejemplo, completado, en proceso). |
| `total` | El total del pedido. **Esencial.** |
| `currency` | Código de moneda para el total del pedido. |

### Reseñas (Opcional)

| Columna | Descripción |
|---|---|
| `id` | Identificador único en sus datos de origen. |
| `product_id` | El `id` del producto que se está reseñando, coincidiendo con su archivo de productos. **Esencial** — vincula la reseña al producto correcto. |
| `customer_email` | Dirección de correo electrónico del revisor. |
| `rating` | La calificación en estrellas otorgada. |
| `comment` | El texto de la reseña. |
| `date` | La fecha en que se publicó la reseña. |

## Preparando sus archivos

- **Guarde como UTF-8** para evitar caracteres acentuados dañados, especialmente desde una codificación de origen diferente.
- **Cite campos que contengan comas** — envuelva una descripción o nombre que contenga una coma en comillas dobles para que no se lea incorrectamente como un salto de columna.
- **Incluya una fila de encabezado.** La primera fila debe contener los nombres de sus columnas — un archivo sin fila de encabezado se rechaza.
- **Construya la jerarquía de categorías con `parent_id`.** Dado que cada categoría tiene un `id` único, establezca el `parent_id` de una subcategoría en el `id` de su categoría principal. En blanco significa nivel superior.
- **Vincule pedidos a clientes con `customer_email`**, coincidiendo con la columna `email` de su archivo de clientes (o se creará un registro de invitado), en lugar de depender de números de identificación internos, que rara vez coinciden entre plataformas.
- **Vincule reseñas a productos con `product_id`**, coincidiendo con un valor en la columna `id` de su archivo de productos, o esa reseña se omitirá.

## Mapeo de columnas en el paso 4

El paso 4 muestra un panel de mapeo de columnas de CSV. Spwig escanea sus encabezados y detecta automáticamente coincidencias probables contra una lista de alias comunes — por ejemplo, un campo `sku` también coincide con `barcode`, `part_number` o `item_number`. Los encabezados exportados directamente de otra plataforma suelen mapearse correctamente sin trabajo manual alguno.

Para cada columna, puede aceptar la suposición detectada automáticamente, sobrescribirla eligiendo un campo de destino diferente o elegir "— Saltar esta columna —" para excluirlo. Los mapeos se guardan y se reutilizan en futuras migraciones CSV. Consulte [Mapeo de Campos de Migración](migration-field-mapping) para obtener una visión completa del paso 4, incluyendo mapeos de campos automáticos, mapeo de categorías y las opciones de impuestos/envío.

<!-- screenshots-needed:
- url: /en/admin/migration/migrationjob/wizard/step4/
  filename: csv-column-mapping.webp
  description: Panel de mapeo de columnas de CSV del paso 4 mostrando mapeos detectados automáticamente con menús desplegables para sobrescribir
  save-to: core/static/core/admin/img/help/csv-import/
  viewport: 1440x900
-->

## Errores comunes y qué significan

| Error | Significado |
|---|---|
| `Products CSV is required.` | Intentó continuar sin cargar un archivo de productos. Es el único archivo que requiere Spwig — cargue uno para continuar. |
| `{Type} CSV has no headers.` | La primera fila del archivo mencionado está vacía o faltante. Agregue una fila de encabezado con los nombres de las columnas y vuelva a cargarlo. |
| `{Type} CSV could not be read: ...` | Spwig no pudo analizar el archivo mencionado — generalmente un archivo dañado, codificación incorrecta o un archivo que no es realmente CSV a pesar de su extensión. Vuelva a exportarlo y confirme que se abre limpiamente antes de cargarlo nuevamente. |

## Ejecutando la importación

Una vez confirmado el mapeo, inicie la migración desde el paso 5. Se ejecuta en segundo plano, por lo que puede cerrar la ventana — el progreso y un registro en vivo están disponibles si vuelve a revisarlo antes de que finalice. Consulte [Después de su migración](after-migration-review) para verificar los resultados.

Recuerde que la importación de CSV deja específicamente **imágenes de productos** y **variantes** para que las complete usted manualmente — ninguna de ellas se transfiere automáticamente, independientemente de lo completa que haya sido su archivo.

## Consejos

Conservar todo el formato de markdown, rutas de imágenes, bloques de código y términos técnicos.

- **Comience desde el botón Descargar plantilla para cada archivo** — le ahorra el trabajo de corregir errores de nombres de columnas que de otro modo pasarían desapercibidos hasta la asignación manual.
- **Corrija los desajustes de `product_id` antes de subir reseñas** — una reseña cuyo `product_id` no coincide con ningún `id` de producto no tiene a nada que adherirse y se omite.
- **No cambie los encabezados de una exportación de otro plataforma** — la detección automática suele reconocerlos tal cual mediante alias, por lo que podría no necesitar ningún trabajo manual de asignación.
- **Reserve tiempo para imágenes y variantes justo después de la importación** — estas son las dos cosas que el CSV nunca trae consigo, y es fácil olvidarlas hasta que un cliente note una página de producto sin contenido.
- **Use `parent_id` para modelar categorías de múltiples niveles** — haga que el `parent_id` de una subcategoría apunte al `id` de su categoría principal para anidarla; deje este campo en blanco para categorías de nivel superior.
- **Reexportar y volver a verificar ante un error de "no se pudo leer"** — casi siempre es un problema de codificación o corrupción en el archivo fuente, no algo que deba corregirse en Spwig.