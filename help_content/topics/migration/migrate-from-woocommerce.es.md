---
title: Migrando desde WooCommerce
---

Si tu tienda actualmente funciona con WooCommerce, el asistente de migración de Spwig puede importar tus productos, clientes, pedidos y contenido directamente a través de la API REST de WooCommerce. Esta guía cubre cómo obtener las credenciales de la API, ejecutar la importación y dos características específicas de WooCommerce que es importante conocer primero: el complemento opcional Migration Bridge para datos de afiliados, y el soporte integrado para varias extensiones populares de WooCommerce.

## Antes de comenzar

WooCommerce tiene el mayor soporte de cualquier plataforma de origen en el asistente de migración. La siguiente importación se realiza de forma limpia: categorías (con jerarquía), productos, imágenes y variantes, clientes y direcciones, pedidos, reseñas, cupones y entradas de blog con sus categorías, etiquetas e imágenes.

Los perfiles de afiliados, registros de comisiones y historial de pagos también pueden importarse, pero solo si instala primero el complemento Spwig Migration Bridge — véase a continuación. Sin él, esos datos simplemente se omiten.

También tenga en cuenta:

- Los productos de ciertas extensiones de WooCommerce (suscripciones, paquetes, reservas, tarjetas regalo) se colocan en la función correspondiente de Spwig, pero no todos los detalles se transfieren — véase **Soporte de extensiones de WooCommerce** a continuación.
- Los campos personalizados en tus productos, clientes y pedidos se detectan automáticamente y necesitan mapeo en un paso posterior. Véase [Mapeo de campos de migración](migration-field-mapping).
- Las opciones **Importar configuración de impuestos** y **Importar zonas y métodos de envío** del asistente no se aplican a los datos importados. Configure las tasas de impuestos y el envío en Spwig usted mismo después — véase [Después de su migración](after-migration-review).
- La opción **Ajuste de precios** en el mismo paso *sí* tiene efecto en las importaciones de WooCommerce, cambiando el precio base de cada producto al crearlo. Deje que esté configurado en **Ninguno** a menos que intencionalmente desee que cada precio se ajuste.

Tenga a mano su inicio de sesión de administrador de WordPress y conozca aproximadamente cuántos productos, clientes y pedidos está importando para que pueda verificar los conteos que muestra el asistente.

## Obteniendo credenciales de la API REST

Spwig se conecta a WooCommerce usando una clave de API REST generada desde su administrador de WordPress. Esta clave solo necesita **Lectura** — Spwig solo lee desde su tienda durante una migración, nunca escribe nada de vuelta.

1. En WordPress, vaya a **WooCommerce > Configuración > Avanzado > API REST**
2. Haga clic en **Agregar clave**
3. Asigne una descripción (por ejemplo, `Spwig Migration`) y establezca **Permisos** en **Lectura**
4. Haga clic en **Generar clave de API**
5. Copie la **Clave del consumidor** (`ck_...`) y el **Secreto del consumidor** (`cs_...`) a un lugar seguro

> **Importante:** WooCommerce muestra el Secreto del Consumidor solo una vez, en el momento en que lo genera. Si navega lejos antes de copiarlo, necesitará generar una nueva clave.

## Conectando tu tienda

Vaya a **Importación y exportación de datos > Iniciar nueva migración** en el administrador de Spwig y elija **WooCommerce** en el paso 1. En el paso 2, ingrese:

- **URL de la tienda** — la dirección web completa de su tienda, por ejemplo `https://mystore.com`
- **Clave del consumidor** y **Secreto del consumidor** — los valores que acaba de copiar

Deje marcada la opción **Probar conexión antes de continuar** (por defecto, activada) para que Spwig confirme que puede acceder a su tienda y autenticarse antes de que continúe — esto detecta errores de ortografía y problemas de permisos de inmediato en lugar de en medio de la importación. Haga clic en **Siguiente** una vez que tenga éxito.

## Revisando y seleccionando datos

El paso 3 obtiene conteos en vivo de su tienda — categorías, productos, clientes, pedidos, reseñas y cupones — más una muestra de los primeros cinco productos para que confirme que está leyendo el sitio correcto. Cada casilla de verificación de tipo de datos se marca automáticamente cuando su conteo es superior a cero y se deshabilita cuando es cero.

**Opciones de importación**:

- **Saltar elementos existentes** (activado) — coincide los registros entrantes con lo que ya está en Spwig (SKU para productos, correo electrónico para clientes) y salta los duplicados.

Dejalo encendido a menos que estés empezando desde una tienda vacía.
- **Importar imágenes de productos** (encendido) — más lento, pero vale la pena.
- **Conservar los IDs originales cuando sea posible** (apagado) — el asistente en sí mismo lo etiqueta como "no recomendado". Dejalo apagado a menos que tengas un motivo técnico específico para conservar los IDs numéricos de WooCommerce.
- **Tamaño de lote** — 10, 25 (por defecto), 50 o 100 registros a la vez.

Los lotes más pequeños son adecuados para conexiones inestables; los lotes más grandes terminan más rápido en una conexión estable.

## El complemento Spwig Migration Bridge

WooCommerce no tiene un concepto integrado de un programa de afiliados, por lo tanto, si ejecutas uno a través de una extensión de afiliados de WooCommerce, esos datos viven en tablas que la API REST estándar no puede ver. El **Spwig Migration Bridge** es un pequeño complemento complementario que installas en tu sitio de WordPress para exponerlo.

El complemento Bridge desbloquea:

- **Perfiles de afiliados** — los detalles de tus afiliados y códigos de referencia
- **Registros de comisión** — historial de comisiones vinculado a cada afiliado
- **Historial de pagos** — pagos anteriores realizados a afiliados

Es completamente opcional — salta si no ejecutas un programa de afiliados o no necesitas ese historial en Spwig.

> **Nota:** Solo se puede importar datos de afiliados si también se importan pedidos y clientes en la misma migración, ya que las comisiones y los pagos están vinculados a pedidos y clientes específicos.

Para instalarlo:

1. En el paso 3, si el complemento aún no se ha detectado en tu sitio, verás un botón **Descargar complemento Bridge** con instrucciones de instalación
2. Descarga el archivo ZIP del complemento
3. En WordPress, ve a **Complementos > Añadir nuevo > Cargar complemento**, elige el ZIP, haz clic en **Instalar ahora**, luego en **Activar**
4. Vuelve al asistente de Spwig y recarga la página — aparecerá un cuadro de verificación **Afiliados** y un bloque **Datos del programa de afiliados**, mostrando las cuentas encontradas

Puedes desactivar y eliminar el complemento Bridge de WordPress una vez que tu migración esté completa.

## Soporte para extensiones de WooCommerce

Si tu tienda utiliza ciertas extensiones populares, los productos que crean se reconocen durante la importación y se mapean a la característica correspondiente de Spwig en lugar de importarse como productos normales:

| Extensión de WooCommerce | Llega a |
|---|---|
| Suscripciones | planes de suscripción de Spwig |
| Add-Ons de productos | add-ons de productos de Spwig |
| Paquetes de productos | paquetes de productos de Spwig |
| Tarjetas regalo (variantes de WooCommerce, YITH y PW) | tarjetas regalo de Spwig |
| Productos compuestos | productos compuestos de Spwig |
| Reservas y Reservas de alojamiento | reservas de Spwig |

> **Nota:** La importación de datos de extensiones nunca bloquea la creación del producto subyacente. Si los datos específicos de la extensión de un producto no pueden leerse, el producto aún se importa — simplemente como un producto normal, sin su configuración de suscripción, paquete, reserva o tarjeta regalo.

Revisa algunos de tus productos de suscripción, paquete, reserva y tarjeta regalo después de la importación para confirmar que sus configuraciones específicas de la extensión se hayan transferido, en lugar de asumir que una importación exitosa llevó todos los detalles.

## Campos personalizados

Si has agregado campos de metadatos personalizados a tus productos, clientes o pedidos de WooCommerce, Spwig toma muestras de aproximadamente diez registros de cada tipo para detectar qué campos existen. Mapearás cada uno a un slot de campo personalizado de Spwig o a un campo de metadatos general en el paso 4. Consulta [Mapeo de campos de migración](migration-field-mapping) para el recorrido completo, incluyendo cómo se guardan los mapeos para futuras migraciones.

## Ejecutar la importación

Una vez que hayas revisado el paso 3 y confirmado tus mapeos en el paso 4, inicia la importación. Se ejecuta en segundo plano — puedes cerrar la ventana del navegador y seguirá ejecutándose. El paso 5 muestra el progreso en vivo con una fila por tipo de datos (categorías, productos, clientes, pedidos, reseñas, cupones, entradas de blog y afiliados/comisiones/pagos si se usó el complemento Bridge) más un registro de actividad expandible.

El paso 6 muestra tus resultados: qué se importó, se saltó o falló, más una herramienta de **Reescritura de enlaces** si se encontraron enlaces internos a tu antiguo dominio de WooCommerce en el contenido importado.

Revise cuidadosamente el resumen, luego siga la lista de verificación en [Después de su migración](after-migration-review) — cubre verificar sus datos, configurar tasas impositivas y envío (lo cual el asistente no configura para usted) y reescribir enlaces internos.

## Revocar su clave de API

Una vez que haya confirmado que la migración se completó con éxito, regrese a **WooCommerce > Configuración > Avanzado > API REST** en WordPress y revocar o eliminar la clave que creó para Spwig. No hay razón para dejar una clave de API activa en su tienda antigua una vez que haya terminado con ella.

## Consejos

- **Genere la clave de API justo antes de necesitarla** — ya que el Secreto del Consumidor se muestra solo una vez, créela inmediatamente antes de comenzar el paso 2 en lugar de hacerlo con anticipación.
- **Solo de lectura realmente es suficiente** — nunca otorgue permisos de Escritura o Lectura/Escritura; Spwig solo lee de su tienda WooCommerce.
- **Instale el plugin Bridge antes de comenzar la importación** — necesitará agregarlo y recargar el asistente antes de importar, así que verifíquelo de antemano en lugar de hacerlo a mitad del proceso.
- **Revise parcialmente los productos respaldados por extensiones** — las suscripciones, paquetes, reservas y tarjetas regalo son los productos más propensos a necesitar una verificación manual después de la importación.
- **Una importación parcial no se limpia automáticamente** — consulte [Solución de problemas de migración](migration-troubleshooting) antes de intentar nuevamente una importación fallida.
- **Revocar la clave de API cuando termine** — no deje activas integraciones antiguas en una tienda de la que se ha migrado.