---
title: Después de su migración
---

Una migración completada es el comienzo de su revisión, no el final. El paso 6 del asistente le da un resumen de lo que se transfirió, una herramienta para corregir enlaces que aún apuntan a su antiguo sitio y un informe que puede descargar para sus registros. Este tema le guiará sobre lo que debe verificar antes de considerar el traslado terminado, incluyendo el trabajo relacionado con impuestos, envíos y el lanzamiento que el asistente mismo no hace por usted.

## Leer sus resultados

En la parte superior de la página de finalización verá una fila de tarjetas de estadísticas — una por tipo de datos (Productos, Categorías, Clientes, Pedidos, etc.) — seguida de una tabla **Resumen de importación** con columnas de Importado, Saltado, Fallido y Total para cada paso que se ejecutó.

- **Importado** — elementos creados con éxito en Spwig.
- **Saltado** — elementos que tenía su plataforma de origen, pero Spwig no creó. Esto casi siempre es esperado: con **Saltar elementos existentes** activado en el paso 3, cualquier elemento que coincida con uno que ya existía en Spwig (por SKU, correo electrónico, etc.) se deja sin tocar en lugar de duplicarse. Un alto recuento de saltos después de un reintento suele significar simplemente que el primer intento ya creó esos registros.
- **Fallido** — elementos que Spwig intentó crear pero no pudo, debido a un problema de datos, una dependencia faltante o un error en el lado de la fuente. Un recuento de fallidos no nulo vale la pena investigarlo; consulte [Solución de problemas de migración](migration-troubleshooting) para ver cómo leer los registros y cuáles son sus opciones de limpieza.

> **Nota:** Si algún paso muestra fallidos, no asuma que la tienda devolvió algo para compensarlo — no lo hace. Cualquier cosa importada antes del fallo sigue en su tienda junto con todo lo que tuvo éxito. Revíselo de la misma manera que lo haría con un resultado parcial normal.

## Reescritura de enlaces

Los productos, páginas y publicaciones de blog importados desde su antigua plataforma suelen contener enlaces de regreso a su dominio original — una URL de imagen, un enlace a "producto relacionado", una referencia cruzada interna. Si Spwig detecta alguno de estos en el contenido que acaba de importar, aparecerá un panel **Reescritura de enlaces** en la página de finalización.

Cada enlace detectado se agrupa por la página o producto del que proviene y se muestra con:

- **URL original** — el enlace exactamente como apareció en el contenido importado.
- **URL sugerida** — la mejor suposición de Spwig sobre la página equivalente en su nueva tienda, si se encontró alguna.
- **Coincidencia** — un porcentaje de confianza para esa sugerencia. Los enlaces sin coincidencia razonable se muestran como **Ninguna** y no tienen ninguna URL sugerida para aprobar.

Para cada enlace puede **Aprobar** la sugerencia o **Saltar**la, uno a la vez. **Aprobar automáticamente las coincidencias altas** aprueba todas las sugerencias con un porcentaje de 85% o más con un solo clic — ahorra tiempo, pero aún vale la pena revisar algunos después. Las sugerencias por debajo de ese umbral son las que vale la pena abrir manualmente: una coincidencia del 50-70% podría ser el producto correcto con el nombre equivocado, o podría estar muy lejos, y solo una mirada humana puede determinarlo.

Aprobar o saltar solo marca un enlace — nada en su contenido cambia hasta que haga clic en **Aplicar enlaces aprobados**, lo que reescribe todos los enlaces aprobados a la vez. Eso significa que es seguro trabajar a través de la lista en más de una sesión antes de comprometerse.

> **Consejo:** Deje cualquier enlace en el que no esté seguro como **Saltar** en lugar de aprobar una suposición. Siempre puede corregir manualmente un enlace antiguo de dominio más tarde; una reescritura incorrecta aplicada a docenas de productos es más trabajo para deshacerse de ella.

## Verificando sus datos

Trate las tarjetas de estadísticas como un punto de partida, no como prueba de que todo esté correcto. Dedique unos minutos a revisar algunos elementos:

- **Productos** — Abra varios productos, especialmente aquellos con variantes (tamaño, color, etc.), y confirme que las opciones de variantes y precios se transfirieron correctamente, y que las imágenes adjuntas y se muestran en el almacén, no solo en el administrador.
- **Categorías** — Confirme que la jerarquía de categorías se vea bien, especialmente si migró desde Shopify, donde las colecciones se importan como una lista plana en lugar de un árbol anidado.
- **Cuentas de clientes** — Revisar algunos registros de correos electrónicos y direcciones.

Los clientes migrados no llevan su antigua contraseña — Spwig no tiene forma de leerla desde la plataforma de origen — por lo tanto, **los clientes deberán restablecer su contraseña** la primera vez que inicien sesión.

Considere enviar un correo de aviso una vez que esté en producción.
- **Pedidos** — Verifique que los totales, los estados y los artículos de una muestra de pedidos coincidan con lo que vio en la antigua plataforma.
- **Productos derivados de extensiones** — Si migró desde WooCommerce con extensiones como Subscriptions, Bundles, Gift Cards, Composite Products o Bookings, revise algunos productos que las usaran.

Los datos de la extensión que no se pueden leer no bloquean la importación del producto — aún se importa, solo sin esa configuración adicional — por lo tanto, estos productos son los más propensos a necesitar un ajuste manual.

## Configuración de impuestos y envío

Las opciones del paso 4 del asistente para importar la configuración de impuestos y zonas de envío registran sus preferencias, pero no se aplican a la importación — no se crean tasas de impuesto ni zonas de envío a partir de ellas. Esto es esperado: **la configuración de impuestos y envío es un paso normal y separado que completa directamente en Spwig** después de que finalice la importación de datos, igual que lo haría al configurar una tienda nueva.

El control de **Ajuste de precio** en ese mismo paso es la excepción — sí tiene efecto para las importaciones de WooCommerce, CSV y Shopify, desplazando el precio base de cada producto al crearlo. Si establece uno y sus precios parecen incorrectos, ese es el lugar de donde proviene el cambio. Consulte [Mapeo de Campos de Migración](migration-field-mapping) para obtener más detalles.

Antes de ir en producción, configure:

- Sus tasas de impuesto — consulte [Configuración de Impuestos](tax-configuration) para configurar tasas por país, estado o región, incluyendo cualquier exención que sus productos necesiten.
- Sus zonas y métodos de envío — consulte [Configuración del Envío](setup-shipping) para recrear las opciones de envío que tenían sus clientes en su antigua plataforma.

Hágalo antes de probar el proceso de pago, para que su pedido de prueba refleje totales reales.

## Descargando su informe

La página de finalización ofrece tres descargas:

- **Descargar PDF** — un resumen formateado con metadatos del trabajo, conteos por paso y una lista de errores, limitado a los **primeros 20 errores**.
- **Descargar CSV** — el mismo resumen en formato de hoja de cálculo, limitado a los **primeros 50 errores**.
- **Descargar registros** — cada entrada de registro del trabajo, sin límite.

Si el recuento de errores es pequeño, el PDF o CSV es suficiente. Para una migración con un gran número de errores, descargue los registros en su lugar — es el único de los tres con el registro completo en lugar de una muestra truncada.

> **Consejo:** Los registros de trabajos de migración — incluyendo sus registros y reportes — permanecen en Spwig indefinidamente; nada los elimina en un horario. Descargue una copia de todos modos si desea tenerla para registros fuera de línea o para compartirla con alguien que no tenga acceso de administrador, pero no hay un conteo descendente que lo obligue a hacerlo hoy.

## Ir en producción

Una vez que esté satisfecho con su configuración de datos, impuestos y envío:

1. **Pruebe el proceso de pago de principio a fin.** Agregue un producto al carrito, complete el pago y confirme que los impuestos, el envío y el pago se calculen y procesen correctamente, idealmente con un método de pago real en modo de prueba.
2. **Actualice su DNS** para que su dominio apunte solo a Spwig una vez que esa prueba tenga éxito. No cambie el DNS primero y luego intente depurar — los clientes podrían encontrar un proceso de pago roto en el medio.
3. **Mantenga su antigua tienda disponible, en un estado de solo lectura o "cerrado"**, hasta que esté seguro de que la nueva maneja correctamente los pedidos. Esto le da un respaldo sin correr el riesgo de que se realicen pedidos en la antigua plataforma después del cambio.

## Revocando las credenciales de la plataforma de origen

Una vez que haya verificado que la migración está completa y no espera ejecutarla nuevamente, vuelva a su plataforma de origen y revóque o elimine la clave de API, la aplicación o la integración que creó para ella (consulte [Migración desde WooCommerce](migrate-from-woocommerce) o la guía equivalente de la plataforma para ver dónde se encuentra esa credencial).

Spwig no necesita acceso permanente a tu antiguo almacén después de que finalice la importación, por lo tanto, eliminarlo cierra una credencial que ya no usas.

## Consejos

- **Saltado suele estar bien, fallido no lo está** — un gran número de elementos saltados después de un reintento con Skip existing items activado es esperado; un recuento de fallidos distinto de cero merece una revisión de los registros.
- **No te apresures a aplicar los enlaces aprobados** — las aprobaciones y los saltos pueden cambiar fácilmente hasta que hagas clic en Aplicar, así que tómate tu tiempo con los de baja confianza.
- **Configura impuestos y envíos antes de tu primera venta en vivo**, no después — la importación no lo hace por ti, y una tasa impositiva no configurada es fácil de pasar por alto hasta que un cliente se queje.
- **Advierte a los clientes sobre restablecimientos de contraseña** si estás enviando un correo electrónico a tu lista de clientes sobre el cambio, para que el primer inicio de sesión no sea una sorpresa.
- **Descarga tu informe antes del plazo de 90 días** si lo necesitas para registros contables o de cumplimiento.
- **Mantén el antiguo almacén activo, de solo lectura, durante un tiempo** — cuesta poco y te da una red de seguridad durante tus primeros días en Spwig.

<!-- screenshots-needed:
- url: /admin/migration/migrationjob/wizard/step6/
  filename: step6-results-summary.webp
  description: Página de finalización de migración que muestra las tarjetas de estadísticas y la tabla de resumen de Importado/Saltado/Fallido/Total
  save-to: core/static/core/admin/img/help/after-migration-review/
  viewport: 1440x900
- url: /admin/migration/migrationjob/wizard/step6/
  filename: step6-link-rewriting.webp
  description: Panel de reescritura de enlaces con sugerencias agrupadas, porcentajes de confianza y los controles Aprobar/Saltar/Aplicar enlaces aprobados
  save-to: core/static/core/admin/img/help/after-migration-review/
  viewport: 1440x900
-->