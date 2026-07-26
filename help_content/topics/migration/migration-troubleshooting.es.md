---
title: Solución de problemas de migración
---

La mayoría de las migraciones se completan sin incidentes, pero las conexiones fallan, las importaciones se agotan, y ocasionalmente una ejecución se detiene a mitad de camino. Este tema cubre el diagnóstico de una conexión fallida, la lectura del registro de progreso mientras se ejecuta una importación, y — lo más importante — qué opciones realmente tienes una vez que algo salga mal, incluyendo qué hacen realmente Retry, Cancel y Rollback.

## Fallos de conexión en el paso 2

El cuadro de verificación **Test connection before proceeding** (Prueba la conexión antes de continuar) está activado de forma predeterminada y es tu primer diagnóstico — valida las credenciales contra la plataforma de origen antes de comprometerte con el resto del asistente. Si falla, el mensaje de error generalmente apunta a uno de estos:

- **WooCommerce** — URL de la tienda que falta `https://` o con un segmento de ruta final; una clave/secret incorrecta o regenerada; o una clave de API REST creada sin permiso **Read** en **WooCommerce > Settings > Advanced > REST API**.
- **Shopify** — Dominio de la tienda no en el formato `yourstore.myshopify.com`; ID/Secret del cliente de la aplicación equivocada; o, con mayor frecuencia, una aplicación creada en el Dashboard de desarrollo pero nunca realmente **instalada** — crear una versión de la aplicación no es suficiente, necesitas el enlace de distribución personalizado y un clic en **Install**. Spwig también advierte si `read_products`, `read_customers` o `read_orders` no se incluyeron en los permisos de la aplicación.
- **Magento 2** — URL de la tienda que apunta al tienda en lugar de la raíz de la API, o un token de integración que se creó pero nunca se activó (**Save > Activate > Allow**).
- **Problemas de SSL** — un certificado caducado, autogenerado o mal configurado falla la conexión antes de que se verifiquen las credenciales, mostrándose como un error general en lugar de uno de autenticación. Si las credenciales parecen correctas, verifica el certificado a continuación.

Vuelve a ejecutar la prueba de conexión después de cada corrección en lugar de cambiar varias credenciales a la vez — esto aísla cuál fue la incorrecta.

## Leer el registro en vivo en el paso 5

Mientras se ejecuta una importación, el paso 5 muestra un registro de la actividad a medida que ocurre. Haz clic en **Show Details** (Mostrar detalles) para expandirlo en entradas individuales — nivel y mensaje — en lugar de solo el resumen del paso actual. Este es el método más rápido para ver qué está sucediendo si el progreso parece detenerse: una pared de entradas "saltadas" para un tipo de datos suele significar que "Saltar elementos existentes" funciona como se espera, no que algo esté atascado.

La vista del registro muestra solo las **últimas 500 entradas**, por lo tanto, en una migración grande, las entradas más antiguas se desplazan fuera del campo de vista mientras la importación aún está en ejecución. Si necesitas el registro completo una vez que un tipo de datos haya terminado, usa **Download Logs** (Descargar registros) en la página de resultados en su lugar — no tiene este límite.

## ¿Qué significa realmente una migración fallida?

Este es el aspecto más importante de entender si una migración falla.

Cuando una migración falla, la página de finalización te lo dice claramente: los elementos importados antes del error aún están en tu tienda, nada se eliminó automáticamente, y corregir el problema y ejecutar la importación nuevamente saltará lo que ya se importó la primera vez. Toma esto a la cara. Ningún paso de la importación se ejecuta dentro de una transacción de base de datos que pueda revertirse como una unidad — lo que se importó con éxito antes del punto de falla, productos, categorías, clientes, pedidos, lo que el trabajo logró, permanece en tu tienda exactamente como se creó. Una migración fallida es una **migración parcial**, no una que se haya deshecho.

También marca el trabajo como no reversible, por lo tanto, el botón **Rollback** (Revertir) no estará disponible en una **importación** fallida — solo aparece una vez que una migración se haya completado, o si un rollback de una migración completada falló parcialmente, en cuyo caso Spwig ofrece el botón nuevamente para que puedas intentarlo de nuevo. La única situación en la que más desearías un deshacer automático — una importación fallida — es exactamente la situación en la que el botón no se ofrece.

Entonces, cuando una migración falla:


1. **Revisa qué realmente se importó**, usando los recuentos de Importados/Rechazados/Fallidos y los registros descargados para construir una imagen de lo que está en tu tienda versus lo que no logró hacerlo.

2. **Decide cómo limpiar.** Para una cantidad pequeña de datos parciales, revísalos manualmente y elimina lo que no quieras a través de las vistas de lista normales del administrador.

Para una importación parcial más grande o desordenada, suele ser más rápido limpiar los datos importados tú mismo antes de comenzar de nuevo que reconciliarlos artículo por artículo.

3. **Vuelve a ejecutar con Skip existing items habilitado**, cualquiera que sea el camino de limpieza que elijas — es lo que evita que los datos que sobrevivieron se dupliquen en el siguiente intento.

## Reintentar

**Reintentar** reinicia por completo la importación desde el principio. Limpia los contadores y registros previos del trabajo e importa todo desde cero — **no** continúa desde donde se detuvo el intento fallido. Mantén **Skip existing items** habilitado para que los elementos que ya se importaron en la primera vez no se dupliquen en la segunda pasada.

Si una migración se detiene porque alcanzó el **límite de 4 horas**, el mensaje que verás es preciso: volver a ejecutar la importación comienza desde el principio y salta los elementos que ya se importaron, **no** es una reanudación desde donde se detuvo. Para una tienda lo suficientemente grande como para alcanzar el límite de tiempo, reintentar la totalidad repetidamente rara vez termina; en su lugar, reduce el alcance de cada ejecución seleccionando menos tipos de datos en el paso 3 (productos en una ejecución, pedidos en otra) y haz varias pasadas más pequeñas.

## Cancelar

**Cancelar** está disponible en una migración en curso, y marca el trabajo como fallido en el panel de control de inmediato. **No** detiene la tarea de importación en segundo plano, que sigue ejecutándose y escribiendo datos hasta que alcance un punto de parada natural. Espera a que los recuentos importados sigan aumentando un tiempo después de cancelar — deja que se estabilicen antes de decidir qué limpiar, en lugar de actuar sobre los recuentos capturados en el momento en que hiciste clic en Cancelar.

## No hay pausa ni reanudación

Spwig no admite pausar una migración en curso y reanudarla más tarde. El botón **Reanudar** en el panel de control es para un caso diferente: una migración configurada a través del asistente pero nunca iniciada. Reabre el asistente donde te quedaste configurándolo — no está relacionado con una ejecución ya en curso.

## Rollback

> **Advertencia:** El rollback es una acción permanente y destructiva. Lee esta sección completa antes de usarla.

El rollback se ofrece en una migración **completada**, y nuevamente en una cuya propia migración de rollback falló parcialmente (estado **Rollback Failed**), por lo que un rollback atascado puede reintentarse. Solo elimina lo que la importación misma creó, y mantiene cualquier cosa en la que ahora dependa tu tienda:

- Un cliente migrado que haya realizado un pedido real desde la importación **se mantiene** — su cuenta, direcciones, historial de lealtad y crédito de tienda permanecen con él, y ese pedido real permanece sin tocar. Solo se eliminan los pedidos que la importación creó.

- Un producto migrado que aún sea referenciado por cualquier pedido, conjunto, tarjeta de regalo o slot de configurador **se mantiene**. Los pedidos pertenecientes a otros clientes nunca se modifican — el rollback ya no puede eliminar elementos de línea de un pedido no relacionado o dejarlo con un total incorrecto.

- Lo que se mantiene se informa de vuelta a ti por nombre y cantidad, con la razón — por ejemplo, "1 Producto mantenido, aún referenciado por un elemento de pedido" — para que sepas exactamente qué sigue allí y por qué.

- Afiliados, comisiones y pagos creados por la importación **se eliminan**, junto con cualquier cuenta de afiliado que la importación haya creado. Un afiliado adjunto a un cliente que ya existía mantiene su cuenta; solo el registro del afiliado se elimina.

- El historial de lealtad y el crédito de tienda siguen al cliente: se eliminan si el cliente se elimina, se mantienen si el cliente se mantiene.

Todavía **no** elimina planes de suscripción, niveles de precios o recursos de reservación creados por extensiones de la tienda — estos sobreviven un rollback y necesitan limpieza manual si no quieres que permanezcan.

Preserva todo el formato de markdown, rutas de imágenes, bloques de código y términos técnicos.

Antes de confirmar, la página de confirmación muestra una vista previa de exactamente qué se eliminará y qué se mantendrá, calculado contra tus datos en vivo — léelo antes de hacer clic en **Sí, Revertir Migración**.

El revertir se ejecuta en segundo plano en lugar de en tu navegador, por lo que es seguro cerrar la pestaña; verifica el estado de la migración para obtener el informe de lo que realmente se eliminó y se mantuvo una vez que finalice.

Dado que el revertir ya no alcanza más allá de lo que la importación creó, ya no es una herramienta solo para el mismo día — las órdenes reales de un cliente migrado y las ventas reales de un producto migrado están protegidas tanto tiempo como haya transcurrido desde la migración. Aún así, sigue siendo una acción permanente y destructiva en las filas que elimina, por lo que úsala deliberadamente en lugar de de forma casual, y limpia manualmente cualquier cosa que Spwig mantenga que no desees realmente.

En cuanto a la disponibilidad: el botón de Revertir permanece en la resumen de una migración completada tanto tiempo como exista el registro del trabajo — para la mayoría de las plataformas no hay un plazo fijo. Magento es la excepción y pierde la disponibilidad de revertir después de una ventana establecida, por lo que decide rápidamente si estás en Magento. Los registros de trabajo no se eliminan según ningún horario, por lo que una migración permanece revertible indefinidamente a menos que elimines su registro tú mismo.

## Estrategia para tiendas grandes y importaciones lentas

Para una tienda lo suficientemente grande que un solo proceso arriesgue el límite de 4 horas:

- **Aumenta el tamaño del lote** en el paso 3 (hasta 100) — los lotes más grandes suelen significar menos viajes de ida y vuelta y un mayor throughput.
- **Divide la migración en múltiples ejecuciones según el tipo de datos** — categorías y productos en una ejecución, clientes y órdenes en una ejecución posterior, en lugar de todo a la vez.
- **Mantén activa la opción Saltar elementos existentes** para cada ejecución después de la primera, para que las ejecuciones repetidas no dupliquen lo que ya tuvo éxito.
- **Deshabilita Importar imágenes de productos.** Descargar y procesar cada imagen suele ser el factor más grande en una ejecución lenta. Puedes agregar imágenes a los productos individualmente, o a través de una importación CSV separada, una vez que el resto de los datos esté en su lugar.

## Consejos

- **Prueba la conexión después de cada cambio de credencial**, no solo una vez al final — aísla qué valor está incorrecto.
- **Nunca asumas que un trabajo fallido limpió después de sí mismo** — verifica qué realmente está en tu tienda antes de decidir sobre una limpieza o un reintento.
- **Mantén activa la opción Saltar elementos existentes para cada reintento** — es la única cosa que evita duplicados en una segunda pasada.
- **No luches contra el límite de 4 horas con más reintentos** — divide por tipo de datos en su lugar.
- **Lee la vista previa de revertir antes de confirmar** — nombra exactamente qué se eliminará y qué se mantendrá, calculado contra tus datos en vivo, por lo que no hay sorpresas.