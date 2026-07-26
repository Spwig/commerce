---
title: Migrar desde Magento
---

Spwig puede importar su catálogo, clientes, pedidos, cupones y páginas de CMS directamente desde una tienda Magento 2 o Adobe Commerce en vivo utilizando la API REST de Magento. Esta guía explica cómo generar las credenciales de integración que requiere Magento, ejecutar el asistente de migración y la única limitación significativa que los comerciantes que vienen de Magento deben planear: las reseñas de productos.

Solo se admite **Magento 2 y Adobe Commerce**. Magento 1 llegó al final de su vida útil hace años y no expone la API REST en la que esta migración depende — si aún está en Magento 1, use [Importar desde archivos CSV](csv-import) en su lugar.

## Antes de comenzar

Revise [Visión general de la migración de datos](migration-overview) para obtener orientación general sobre la planificación. Para Magento específicamente:

- **Categorías** — importadas con su jerarquía intacta.
- **Productos** — importados, incluyendo imágenes.
- **Clientes y direcciones** — importados.
- **Pedidos** — importados.
- **Cupones** — importados como cupones de Spwig, obtenidos de las reglas de ventas de Magento.
- **Páginas de CMS** — importadas como páginas de Spwig.
- **Reseñas** — normalmente **no** importadas. Vea la siguiente sección antes de depender de esto.
- Se admiten variantes para productos configurables.

> **Nota:** Las migraciones de Magento no transfieren programas de afiliados, comisiones o pagos — la integración del puente de afiliados de Spwig solo está disponible para tiendas WooCommerce.

### La limitación de las reseñas

La edición comunitaria de Magento no expone un punto final REST para reseñas de productos — la ruta `/reviews` simplemente no existe en una instalación comunitaria estándar. Spwig la verifica antes de la importación y, si no está presente, registra un mensaje y continúa con el resto de su migración en lugar de fallar todo el trabajo. Sus categorías, productos, clientes, pedidos, cupones y páginas aún se transfieren; solo se omiten las reseñas.

Las reseñas **sí** se importarán si su tienda ejecuta **Adobe Commerce** (que expone este punto final) o si su instalación de Magento tiene un módulo personalizado que agrega una ruta de reseñas compatible.

Si está en Magento Community y necesita que sus reseñas se transfieran a Spwig, exportelas por separado (la mayoría de las extensiones de reseñas ofrecen una exportación CSV) y luego introdúzcalas posteriormente usando el archivo de reseñas en [Importar desde archivos CSV](csv-import), vinculadas a sus productos mediante `product_id`.

## Paso 1: Elegir Magento

Desde el panel de migración en **Importación y exportación de datos**, haga clic en **Iniciar una nueva migración** y seleccione **Magento** como su plataforma.

## Paso 2: Conectarse a su tienda

Necesitará la URL de su tienda Magento y un token de acceso de integración. El administrador de Magento no distribuye un simple token de API como lo hacen algunas plataformas — crea una **Integración**, que es una credencial con ámbito que Magento trata como una aplicación conectada.

### Crear un token de acceso de integración

1. En su administrador de Magento, vaya a **Sistema > Integraciones**.
2. Haga clic en **Añadir nueva integración**.
3. Establezca el nombre en `Spwig Migration` para que sea fácil de identificar más tarde.
4. Abra la pestaña **API** y establezca **Acceso a recursos** en **Todo**.
5. Haga clic en **Guardar**, luego haga clic en **Activar**.
6. Confirme haciendo clic en **Permitir** en el cuadro de diálogo que enumera los permisos que se están otorgando.
7. Copie el token de acceso mostrado después de la activación — Magento solo lo muestra una vez.

> **Nota:** El acceso a recursos se establece en **Todo** porque el árbol de recursos de Magento es muy granular — cientos de permisos individuales cubriendo catálogo, ventas, clientes y CMS — sin un interruptor único para "leer todo" más allá de seleccionar todos ellos. La migración solo lee desde su tienda; nunca escribe de vuelta, y puede revocar la integración una vez que su migración esté verificada (se cubre al final de esta guía).

De vuelta en el asistente de Spwig, ingrese su **URL de tienda** y el **Token de Acceso** que copió. Deje marcada la opción **Probar conexión antes de continuar** (activada por defecto) para que Spwig verifique que puede alcanzar y autenticarse con su tienda antes de que continúe. Si la prueba falla, vuelva a revisar la URL y asegúrese de que la integración aún esté activa en Magento. Haga clic en **Siguiente**.

comment

<!-- screenshots-needed:
- url: /en/admin/migration/migrationjob/wizard/step2/
  filename: magento-connection-step.webp
  description: Step 2 of the wizard with Magento selected, showing the Store URL and Access Token fields and the Test connection checkbox
  save-to: core/static/core/admin/img/help/migrate-from-magento/
  viewport: 1440x900
-->

heading

## Paso 3: Revisa lo que se importará

paragraph

Spwig consulta tu tienda Magento y muestra conteos en vivo para cada tipo de datos que encontró: categorías, productos, clientes, pedidos, cupones (obtenidos de reglas de ventas) y páginas CMS. Cada tipo tiene un cuadro de verificación, que se marca automáticamente cuando Spwig encuentra elementos para importar y se deshabilita cuando el conteo es cero.

paragraph

También verás una muestra de los primeros cinco productos para que puedas verificar que los títulos, precios e imágenes parezcan correctos antes de comprometerte con la importación completa.

paragraph

Debajo de los conteos, **Opciones de importación** te permiten controlar cómo se comportará la importación:

list

paragraph

Si necesitas cambiar cómo se mapean campos específicos — atributos personalizados, coincidencia de categorías, manejo de impuestos o envíos — eso ocurre en el paso 4, cubierto en [Mapeo de Campos de Migración](migration-field-mapping). Haz clic en **Siguiente** para proceder al mapeo, luego en **Iniciar Migración** una vez que lo hayas revisado.

heading

## Ejecutar la importación

paragraph

La importación se ejecuta en segundo plano — puedes cerrar la ventana y seguirá ejecutándose. La página de progreso muestra el estado en vivo para cada tipo de datos (categorías, productos, clientes, pedidos, reseñas, cupones) con un registro que puedes expandir para obtener detalles.

paragraph

Una vez que finalice, llegarás a la página de resumen de resultados. Revisa [Después de tu migración](after-migration-review) para verificar qué se transfirió, manejar cualquier reescritura de enlaces para contenido que se refería a tus antiguos URLs de Magento y atender la configuración de impuestos y envíos que el asistente recopila pero no aplica automáticamente.

comment

<!-- screenshots-needed:
- url: /en/admin/migration/migrationjob/wizard/step5/
  filename: magento-import-progress.webp
  description: Import progress page showing per-step status rows during a Magento migration
  save-to: core/static/core/admin/img/help/migrate-from-magento/
  viewport: 1440x900
-->

heading

## Fecha límite de reversión

paragraph

Magento es la única plataforma donde la reversión tiene un límite de tiempo. Una vez que tu migración se complete, el botón **Reversión** aparecerá en la página de resumen del trabajo — pero para Magento específicamente, ese botón puede dejar de ofrecerse después de un período tras la finalización. Otros tipos de migración (WooCommerce, Shopify, CSV) no tienen este plazo, pero Magento sí, así que no dejes la verificación para más tarde.

block_quote

> **Advertencia:** La reversión elimina más de lo que la migración creó — incluyendo pedidos realizados por clientes migrados *después* de la migración, y elementos de pedido que se refieren a productos migrados, incluso en pedidos de clientes que no migraste. Solo es seguro usarlo inmediatamente después de una migración, antes de que ocurra cualquier comercio real en la tienda. Consulta [Solución de problemas de migración](migration-troubleshooting) para obtener una visión completa de lo que la reversión sí y no revierte.

paragraph

Verifica tus datos importados con prontitud, mientras aún esté disponible la reversión, en caso de que la necesites.

heading

## Revocar la integración

paragraph

Una vez que hayas verificado tus datos en Spwig — productos, precios, imágenes, clientes, pedidos, cupones y páginas todo parece correcto — regresa a **Sistema > Integraciones** en Magento, busca `Spwig Migration` y desactívala o elimínala.

El token no es necesario nuevamente a menos que planees volver a ejecutar la migración, y eliminarlo cierra una credencial de lectura activa que ya no necesitas.

## Consejos

- **Las reseñas son la mayor sorpresa para los comerciantes de Magento** — planifica una exportación/importación separada si estás en la edición Comunitaria y las reseñas son importantes para tu tienda.
- **Copia el token de acceso inmediatamente** — Magento solo lo muestra una vez cuando activas la integración; si lo pierdes, tendrás que desactivar y recrear la integración.
- **No retrases la verificación** — el botón de Rollback está disponible solo durante un tiempo limitado en Magento, a diferencia de otras plataformas.
- **Usa la vista previa de ejemplo en el paso 3** para detectar problemas obvios de mapeo (precios incorrectos, imágenes faltantes) antes de ejecutar la importación completa.
- **Los cupones provienen de reglas de ventas** — si un cupón de Magento depende de condiciones complejas, verifica en Spwig después, ya que no todos los tipos de regla tienen un equivalente directo.
- **Configura las tasas de impuestos y zonas de envío en Spwig después de la importación** — las opciones de impuestos y envío del asistente se guardan, pero no se aplican automáticamente a tu tienda.