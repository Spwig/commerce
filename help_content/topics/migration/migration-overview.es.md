---
title: Visión general de la migración de datos
---

Si tus productos, clientes y pedidos actualmente residen en WooCommerce, Shopify o Magento, o simplemente en un puñado de archivos CSV, la herramienta de migración lleva esos datos a tu nuevo almacén de Spwig para que no tengas que reintroducirlos manualmente. Maneja categorías, productos, clientes, pedidos, reseñas y cupones, y para WooCommerce también puede transferir contenido de blog y, con un complemento puente, tu programa de afiliados.

Encuéntrala en el menú lateral de administración bajo **Panel de sistema > Importación/exportación de datos** (visible para superusuarios en instalaciones autoalojadas; si no la ves, pregunta a quien gestiona tu instalación). La página, titulada **Importación y exportación de datos**, enumera cada migración que has iniciado con tarjetas de estadísticas para Total de migraciones, Completadas, En progreso y Fallidas, además de los botones **Iniciar nueva migración**, **Ver registros** y **Asignación de campos**. Las migraciones solo se pueden crear a través del asistente.

## Plataformas compatibles

Spwig se conecta directamente a tres plataformas, además de archivos CSV simples:

- **WooCommerce** — la ruta más completa; los datos de extensiones (suscripciones, paquetes, tarjetas de regalo, reservas) y tu programa de afiliados también pueden transferirse.
- **Shopify** — se conecta a través de una aplicación personalizada que creas en tu panel de desarrollador de Shopify.
- **Magento 2** — se conecta a través de un token de integración desde tu administración de Magento.
- **Archivos CSV** — cinco archivos separados (productos, categorías, clientes, pedidos, reseñas), para otras plataformas o datos preparados manualmente.

> **Nota:** BigCommerce, PrestaShop, Squarespace y Wix no se admiten como conexiones directas. Si estás migrando desde una de estas, exporta tu catálogo y datos de clientes a CSV y usa la ruta CSV en su lugar — consulta [Importación desde archivos CSV](csv-import).

## ¿Qué se transfiere, por plataforma

La cobertura varía según la plataforma — verifica esta tabla contra tu propia tienda antes de comprometerte con una fecha de lanzamiento.

| Datos | WooCommerce | Shopify | Magento 2 | CSV |
|---|---|---|---|---|
| Categorías | Sí, con jerarquía | Sí, como Colecciones (planas) | Sí | Sí |
| Productos | Sí | Sí | Sí | Sí (archivo requerido) |
| Imágenes de productos | Sí | Sí | Sí | No |
| Variantes | Sí | Sí | Sí | No |
| Clientes + direcciones | Sí | Sí | Sí | Sí |
| Pedidos | Sí | Sí, solo los últimos 60 días a menos que se agregue el alcance `read_all_orders` | Sí | Sí |
| Reseñas | Sí | No admitido en absoluto | Normalmente no disponible — Magento Community no tiene un punto final REST para reseñas | Sí |
| Cupones / descuentos | Sí | Sí | Sí | No |
| Blog / contenido de CMS | Sí (publicaciones, categorías, etiquetas, imágenes) | Sí (artículos) | Sí (páginas de CMS) | No |
| Afiliados, comisiones, pagos | Sí, requiere el complemento Spwig Migration Bridge | No | No | No |
| Detección de campos personalizados | Sí | No — los metafields de Shopify no se leen | No | n/a |

Los comerciantes de Shopify deben planear reintroducir manualmente cualquier dato de metafield (especificaciones personalizadas de productos, campos adicionales de clientes) después de la importación, ya que no se detecta ni se transfiere. Para todo lo demás, consulta [Asignación de campos de migración](migration-field-mapping) para ver cómo se mapean los campos de origen en los campos de Spwig.

## Planificación de tu migración

- **Migra antes de lanzar**, contra una instalación de Spwig que aún no esté manejando tráfico real, antes de apuntar el DNS de tu dominio a ella — de esta manera puedes revisar y corregir cosas sin que los clientes vean un catálogo incompleto.
- **Mantén tu antigua tienda en funcionamiento, en modo solo lectura**, hasta que hayas verificado que la copia de Spwig sea correcta.
- **Reserva tiempo para la configuración de impuestos y envíos después** — las configuraciones del asistente para esto parecen importar tus tarifas y zonas, pero no se aplican (consulta [Asignación de campos de migración](migration-field-mapping)). Configura tú mismo **Configuración > Impuestos y moneda** y **Configuración > Envío**.
- **Revisa con atención en lugar de pasar por alto** — las importaciones de datos de extensiones se realizan en el mejor esfuerzo posible; un producto cuyos datos de extensión no pudieron leerse aún se crea, pero sin ellos. Consulta [Después de tu migración](after-migration-review) antes de anunciar nada a los clientes.

- **Acceso de administrador a tu plataforma de origen** para crear credenciales de API — una clave de API REST en WooCommerce, una aplicación personalizada en Shopify o un token de integración en Magento.

No es necesario para CSV.
- **Ámbitos de solo lectura** en los lugares donde la plataforma de origen los ofrezca — Spwig solo lee de tu antigua tienda, nunca escribe de vuelta en ella.
- **Un presupuesto de tiempo** — cada ejecución tiene un límite estricto de 4 horas.

Para una tienda grande, planifica un enfoque en etapas (categorías y productos primero, pedidos después) en lugar de un solo paso.

> **Importante:** Spwig no encripta las credenciales de API que ingresas en el asistente. Una vez que la migración se verifica como completa, revoca o elimina la credencial en la plataforma de origen.

## El asistente de migración, paso a paso

El asistente tiene seis pasos, con el progreso guardado entre ellos:

1. **Plataforma** — elige WooCommerce, Shopify, Magento o Importación CSV.
2. **Conexión** — ingresa las credenciales, con la opción (activada por defecto) de probar la conexión primero. Las guías específicas de la plataforma cubren exactamente qué generar.
3. **Vista previa** — conteos en vivo de tu tienda de origen, una muestra de los primeros 5 productos, y casillas para seleccionar qué tipos de datos incluir, más opciones como el tamaño de lote.
4. **Mapeo** — cómo los campos de origen se mapean a los campos de Spwig, cualquier campo personalizado de WooCommerce y categorías sin un coincidencia obvia. Detalles completos en [Migration Field Mapping](migration-field-mapping).
5. **Importar** — se ejecuta en segundo plano; puedes cerrar la pestaña y seguirá ejecutándose, con un registro en vivo.
6. **Completado** — un resumen de los resultados, una herramienta para reescribir enlaces que hagan referencia a tu antiguo dominio, y descargas de informes en PDF/CSV.

## Después de tu migración

Una importación exitosa no es la línea de meta — consulta [After Your Migration](after-migration-review) para obtener una lista completa de verificación que cubre la verificación de datos, la corrección de enlaces internos que aún apuntan a tu antiguo dominio, y la configuración de impuestos y envíos que el asistente no maneja por ti.

## El rollback no es una red de seguridad

Entiende esto antes de comenzar, no después de que algo salga mal. El rollback existe, pero no es el botón de deshacer que pueda parecer:

- No hay rollback automático si una importación falla a mitad de proceso. Lo que se importó antes del fallo permanece en tu tienda, y una importación fallida no puede revertirse desde el administrador — tendrás que revisar y limpiar los datos parciales manualmente.
- Una migración completada puede revertirse, y el rollback elimina solo lo que la importación misma creó — nunca más. Un cliente migrado que haya realizado un pedido real desde la importación mantiene su cuenta, direcciones, historial de fidelidad y crédito de tienda, y ese pedido real permanece intacto; solo se eliminan los pedidos que la importación creó. Un producto migrado que aún sea referenciado por cualquier pedido, paquete, tarjeta de regalo o slot de configurador también se mantiene, y los pedidos de otros clientes nunca se modifican.
- Los afiliados, comisiones y pagos creados por la importación se eliminan, junto con cualquier cuenta de afiliado que la importación haya creado — un afiliado vinculado a un cliente que ya existía mantiene su cuenta, y solo se elimina el registro de afiliado. Los planes de suscripción, niveles de precios y recursos de reserva creados por extensiones de la tienda todavía no se eliminan — límpialos manualmente.
- Antes de confirmar, Spwig muestra una vista previa exacta de lo que se eliminará y lo que se mantendrá, por nombre y cantidad, con la razón — calculada contra tus datos en vivo. Léela antes de confirmar. Luego el rollback se ejecuta en segundo plano, por lo que es seguro cerrar la pestaña; consulta el resumen de la migración para ver el informe una vez que finalice.
- El rollback sigue siendo una acción permanente y destructiva sobre las filas que elimina, así que úsalo con criterio — y limpia manualmente cualquier cosa que Spwig mantenga que en realidad no quieras. Pero como ya no va más allá de lo que la importación creó, ya no es una herramienta limitada al mismo día, como lo era antes.
- El botón de Rollback permanece disponible en el resumen de una migración completada mientras exista el registro de la tarea, y se ofrece de nuevo si un intento de rollback falla a mitad de proceso, para que puedas reintentarlo. Los registros no se eliminan según ningún calendario, por lo que esto no caduca por sí solo.

Si te encuentras con una migración fallida o atascada, [Migration Troubleshooting](migration-troubleshooting) cubre el reintento, la cancelación y la lectura de los registros.

## Consejos

- **Empieza con una prueba pequeña** — las categorías más un par de productos confirman que el mapeo de campos parece correcto antes del catálogo completo.
- **Lee primero la guía específica de la plataforma** — [Migrating from WooCommerce](migrate-from-woocommerce), [Migrating from Shopify](migrate-from-shopify) y [Migrating from Magento](migrate-from-magento) cubren exactamente qué credenciales y alcances necesitas.
- **No te saltees la matriz de capacidades anterior** — conocer las revisiones de Shopify o variantes CSV evitará una sorpresa después de que hayas cambiado DNS.
- **Mantén abierto el panel de administración de tu plataforma de origen en otra pestaña** para generar o copiar credenciales a medida que avances.
- **Trata literalmente las casillas de verificación del asistente** — si un ajuste no se describe como funcionando aquí, configúralo directamente en Spwig en lugar de confiar en el asistente.