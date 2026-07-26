---
title: Mapeo de Campos de Migración
---

Cada plataforma nombra las cosas un poco de manera diferente — el `regular_price` de WooCommerce no es el `price` de Shopify, y una columna CSV llamada `barcode` podría ser exactamente lo mismo que Spwig espera ver etiquetado como `sku`. El paso 4 del asistente de migración, **Configurar Mapeo de Campos**, es donde verificas cómo tus datos de origen se ubicarán en Spwig antes de que realmente se realice la importación. Este tema cubre cada bloque de esa página y se aplica a las migraciones de WooCommerce, Shopify, Magento y CSV, con diferencias de plataforma señaladas donde sea relevante. Para credenciales y los pasos anteriores del asistente, consulta [Migrar desde WooCommerce](migrate-from-woocommerce) o la guía equivalente para tu plataforma.

## Mapeos Automáticos

Este bloque muestra, para cada tipo de datos que seleccionaste en el paso 3, una lista de solo lectura de campos de origen y el campo de Spwig en el que cada uno se ubica — por ejemplo, el `nombre` de un producto que se mapea al título del producto de Spwig, o el `correo electrónico` de un cliente que se mapea al correo electrónico de la cuenta. Solo aparecen los tipos de datos que estás realmente importando; si no seleccionaste Reseñas en el paso 3, no habrá una sección de Reseñas en esta página.

Dado que estas filas son de solo lectura, no hay nada que configurar — existen para que puedas verificar el mapeo antes de comprometerte con la importación. Si un mapeo parece incorrecto para tus datos, no hay forma de sobrescribirlo desde esta pantalla; tus opciones son corregir los datos de origen antes de la migración o corregir los registros afectados en Spwig después de que se complete la importación.

## Mapeo de Columnas CSV

Este bloque solo aparece para migraciones CSV, con una tabla por cada archivo que subiste. Spwig detecta automáticamente coincidencias probables desde los encabezados de tus columnas — por ejemplo, un mapeo `sku` también reconoce encabezados como `barcode`, `part_number` o `item_number` — por lo tanto, en la mayoría de los casos no necesitarás tocar nada aquí.

Cada columna CSV obtiene un menú desplegable que enumera los campos que Spwig espera para ese tipo de archivo:

- **productos** — `id, nombre, slug, descripción, precio, sku, stock_quantity, categoría`
- **categorías** — `id, nombre, slug, descripción, parent_id`
- **clientes** — `id, correo electrónico, nombre, apellido, teléfono`
- **pedidos** — `id, correo electrónico del cliente, fecha del pedido, estado, total, moneda`
- **reseñas** — `id, id del producto, correo electrónico del cliente, calificación, comentario, fecha`

Cada menú desplegable también incluye **— Saltar esta columna —**, lo cual excluye completamente esa columna de la importación. Sobrescribe el mapeo detectado automáticamente cuando tu encabezado utilice un convenio de nomenclatura que Spwig no reconoció, o cuando una columna realmente no corresponda a nada que Spwig importe (un campo de nota interna, por ejemplo) — elige Saltar en lugar de forzarla al campo disponible más cercano.

## Campos Personalizados

Este bloque es exclusivo de WooCommerce. Spwig toma 10 productos, clientes y pedidos de tu tienda y enumera cualquier campo de metadatos personalizado que encuentre más allá de los campos estándar de WooCommerce, junto con el tipo detectado y un valor de ejemplo.

Para cada campo, elige adónde debe ir:

- **Mapear a** — Campo Personalizado 1, 2 o 3 para productos (Campo Personalizado 1 o 2 para clientes y pedidos), o **Metadatos (JSON)** como un todo en caso de que tengas más campos personalizados de los que hay en los espacios numerados, o déjalo como **— Saltar este campo —**.
- **Transformar** — cómo debe convertirse el valor al entrar: Como Texto, Como Número (Entero), Como Decimal, Como Verdadero/Falso (Booleano), Como JSON, Como Fecha, Como URL o Como Correo Electrónico.

> **Nota:** Los metafields de Shopify no se detectan en absoluto con esta característica — las migraciones de Shopify nunca muestran un bloque de Campos Personalizados, sin importar cuántos datos de metafield tenga tu tienda. Si dependes de metafields de Shopify para especificaciones de productos, atributos de clientes o similares, planea reingresar esa información manualmente en Spwig después de la importación.

Si Spwig no detecta ningún campo personalizado en tu muestra, verás un mensaje de confirmación en lugar de este bloque, y no hay nada más que configurar.

Cuando algunas de tus categorías de origen no tienen una coincidencia obvia en Spwig, este bloque ofrece tres opciones: **Crear nuevas categorías**, **Asignar a la categoría por defecto** (una categoría de captura general llamada "Sin categorizar"), o **Saltar los elementos con categorías no mapeadas**.

> **Nota:** Cualquier opción que elijas aquí, Spwig actualmente crea automáticamente una categoría coincidente para cualquier producto que tenga datos de categoría de origen, y solo recurre a "Sin categorizar" para productos que no tengan información de categoría en absoluto. No necesitas preocuparte demasiado por esta elección — si terminas con categorías que no deseas, es más rápido fusionarlas o eliminarlas en **Catálogo > Categorías** después de la importación que depender de esta configuración.

## Configuración de impuestos, envío y precios

El último bloque, **Configuración de impuestos y envío**, tiene tres controles: **Importar configuración de impuestos**, **Importar zonas y métodos de envío**, y un tipo y valor de **Ajuste de precio**.

Los dos casilleros de verificación actualmente no afectan la importación — ningún tipo de impuesto o zona de envío se transfiere desde tu antigua plataforma, independientemente de cómo se establezcan. Configúralos directamente en Spwig una vez que finalice la importación: los tipos de impuesto bajo **Configuración > Impuestos y Moneda**, y las zonas y métodos de envío bajo **Configuración > Envío**.

**Ajuste de precio** se comporta de manera diferente según tu plataforma de origen:

- **Migraciones de WooCommerce, CSV y Shopify** — este control funciona como se describe. Elige **Porcentaje** o **Monto Fijo**, ingresa un valor (por ejemplo, `10` para un aumento del 10%, o `-5` para una disminución de $5), y el precio base de cada producto se ajusta por ese monto al importarse. Se aplica solo al precio base — los precios de venta o de comparación se transfieren sin ajustes.
- **Migraciones de Magento** — el mismo control aparece en la página, pero no tiene efecto; los precios de Magento se importan sin cambios, independientemente de lo que ingrese. Si necesita un cambio general de precios en una migración de Magento, aplíquelo después usando las herramientas de precios en masa del catálogo de Spwig, en lugar de este campo.

> **Advertencia:** Si estás migrando desde WooCommerce, CSV o Shopify y no deseas que los precios cambien, deja **Ajuste de precio** establecido en **Ninguno**. Es el único control en esta página que realmente modifica tus datos, y es fácil asumir — incorrectamente — que se comporta de la misma manera que los casilleros de verificación de impuestos y envío que están justo encima.

## Las asignaciones se guardan para la próxima vez

Cualquier configuración que realices en esta página se guarda con el trabajo de migración, y Spwig la reutiliza como punto de partida para futuras migraciones desde la misma plataforma — útil si realizas una migración en fases (categorías y productos primero, pedidos después) o si necesitas reimportar después de corregir un problema de datos. También puedes revisar y ajustar las asignaciones guardadas después de que finalice una migración desde el botón **Asignaciones de Campos** en el panel de control de la migración, sin necesidad de ejecutar nuevamente todo el asistente.

## Consejos

- **Revisa el bloque de asignaciones automáticas incluso aunque no puedas editarlo** — detectar una asignación incorrecta antes de hacer clic en Iniciar Importación es mucho más barato que corregir cientos de registros importados después.
- **Renombra los encabezados CSV ambiguos antes de subirlos** si la detección automática no los reconoció, en lugar de intentar forzar un campo no coincidente a través del menú desplegable.
- **Usa Metadatos (JSON) como tu salida para campos personalizados** — es el único objetivo de asignación que no se agota después de dos o tres campos.
- **No dependas de esta página para impuestos, envío o (en Magento) precios** — trátalos como una tarea de configuración manual que debes realizar inmediatamente después de la importación, no algo que maneje el asistente por ti.
- **Deja el ajuste de precio en Ninguno en tu primera ejecución de una nueva migración**, luego usa un lote de prueba pequeño para confirmar los cálculos antes de aplicarlo a tu catálogo completo.