---
title: Migrar desde Shopify
---

Si tu tienda actualmente funciona en Shopify, el asistente de migración de Spwig puede importar tus productos, clientes, pedidos y contenido conectándose a una pequeña aplicación personalizada que crees en el panel de Shopify Partners. La plataforma de Shopify es más restringida que la mayoría, por lo que gran parte de esta guía se centra en crear esa aplicación correctamente — la conexión en sí misma es un paso de cinco minutos una vez que exista la aplicación.

## Antes de comenzar

Dos limitaciones específicas de Shopify son lo suficientemente importantes como para mencionarlas aquí, no solo más adelante en una tabla:

> **Importante:** Shopify no tiene una API de reseñas, por lo tanto, **las reseñas de los clientes no se migrarán en absoluto**, independientemente de qué alcances de la aplicación le concedas. Si necesitas tus reseñas, descárgalas por separado de la aplicación de reseñas que estés utilizando (Judge.me, Yotpo, Loox, etc.) e importa las reseñas a Spwig tú mismo.

> **Importante:** Por defecto, Spwig solo puede leer **pedidos de los últimos 60 días**. Para transferir tu historial completo de pedidos, debes agregar el alcance `read_all_orders` cuando crees tu aplicación — consulta la lista de alcances a continuación. Esto es fácil de pasar por alto, ya que la aplicación aún se conecta e importa con éxito sin él; simplemente limita silenciosamente cuán lejos atrás va tu historial de pedidos.

Todo lo demás se transfiere bien: categorías (como Colecciones — véase a continuación), productos, imágenes, variantes, clientes y direcciones, descuentos y contenido del blog. Los campos personalizados son otro hueco notable — véase **Metafields de Shopify** al final de esta guía.

También ten en cuenta:

- Las opciones **Importar configuraciones de impuestos** y **Importar zonas y métodos de envío** del asistente no se aplican a los datos importados. Configura las tasas de impuesto y el envío en Spwig tú mismo después — véase [Después de tu migración](after-migration-review).
- La opción **Ajuste de precio** en el mismo paso *sí* tiene efecto para las importaciones de Shopify, cambiando el precio base de cada producto al crearse. Deja que esté establecido en **Ninguno** a menos que quieras deliberadamente que cada precio se ajuste.
- Necesitarás acceso a una cuenta de Shopify Partners para crear la aplicación. Si no tienes una ya, Shopify te permite crear una de forma gratuita en partners.shopify.com.

## Crear la aplicación de Shopify

Spwig se conecta a Shopify a través de una aplicación personalizada que creas e instalas en tu propia tienda. Esto imita la guía **Shopify API Setup Guide** dentro del producto (abierta mediante **Open Setup Guide** en el paso 2 del asistente), por lo que los pasos a continuación coinciden exactamente con lo que verás allí — puedes seguir cualquiera de los dos.

### Paso 1: Crear la aplicación

1. Ve a tu [dashboard de desarrollo de Shopify Partners](https://dev.shopify.com/dashboard) y abre **Apps**
2. Haz clic en **Crear app**
3. Elige **Empezar desde el dashboard de desarrollo**
4. Ingresa el nombre de la aplicación: `Spwig Migration`
5. Haz clic en **Crear**

![Creando la aplicación Spwig Migration en el dashboard de desarrollo de Shopify](/static/core/admin/img/help/migrate-from-shopify/shopify-create-app.webp)

### Paso 2: Establecer la URL de la aplicación y los alcances

En la página de configuración de la nueva aplicación, bajo **Versiones**, establece:

- **App URL**: `https://shopify.dev/apps/default-app-home`
- **Scopes**: `read_customers,read_discounts,read_files,read_orders,read_products,read_content`

![Estableciendo la URL de la aplicación y los alcances requeridos](/static/core/admin/img/help/migrate-from-shopify/shopify-app-url-scopes.webp)

| Alcance | Da a Spwig acceso a |
|---|---|
| `read_products` | Productos, variantes, imágenes, colecciones |
| `read_customers` | Nombres de clientes, correos electrónicos, direcciones |
| `read_orders` | Pedidos de los últimos 60 días |
| `read_content` | Posts de blog y páginas |
| `read_discounts` | Códigos de descuento y reglas |
| `read_files` | Archivos de medios cargados |

> **Nota:** ¿Quieres tu historial completo de pedidos en lugar de solo los últimos 60 días? Añade `read_all_orders` a la lista de alcances anterior.

### Paso 3: Copiar tu ID de cliente y secreto

Ve a **Configuración > Credenciales** y copia el **ID de cliente** y **Secreto** mostrados allí — pegarás estos en el asistente de Spwig en un momento.

![Copiando el ID de cliente y el secreto desde la página de configuración de la aplicación](/static/core/admin/img/help/migrate-from-shopify/shopify-credentials.webp)

### Paso 4: Generar un enlace de distribución personalizado

1.

Vaya a **Distribución** y seleccione **Distribución personalizada**
2.

Ingrese su dominio de tienda (por ejemplo, `yourstore.myshopify.com`)
3.

Haga clic en **Generar enlace**, luego **Copie** el enlace de instalación que genere

![Copiando el enlace de instalación de distribución personalizada generado](/static/core/admin/img/help/migrate-from-shopify/shopify-install-link.webp)

### Paso 5: Instale la aplicación en su tienda

Abra el enlace de instalación que acaba de copiar en su navegador (asegúrese de que esté conectado a su administrador de tienda Shopify), revise los permisos que solicita y haga clic en **Instalar**.

![Instalando la aplicación en la tienda Shopify](/static/core/admin/img/help/migrate-from-shopify/shopify-install-app.webp)

> **Importante:** Este último paso es fácil de pasar por alto. Generar el enlace de instalación no instala la aplicación — debe abrir realmente el enlace y hacer clic en Instalar, de lo contrario, Spwig no podrá conectarse. Si la prueba de conexión falla en la siguiente sección, esto es lo primero que debe verificar.

## Copiando sus credenciales en Spwig

En el administrador de Spwig, vaya a **Importación y exportación de datos > Iniciar nueva migración**, elija **Shopify** en el paso 1, y en el paso 2 ingrese:

- **Dominio de la tienda** — `yourstore.myshopify.com`
- **ID de cliente** — de Configuración > Credenciales
- **Secreto de cliente** — de Configuración > Credenciales

Si prefiere seguir la guía de configuración dentro del producto en lugar de esta guía, haga clic en **Abrir guía de configuración** en este paso — cubre los mismos cinco pasos anteriores con las mismas capturas de pantalla y toma aproximadamente 10 minutos en total.

Deje marcada **Probar conexión antes de continuar**. Si `read_products`, `read_customers` o `read_orders` falta en los alcances de su aplicación, Spwig le advierte antes de que continúe — vaya a la página de versiones de la aplicación en el panel de administración de Shopify, agregue el alcance faltante, guarde una nueva versión y vuelva a intentarlo.

## Revisando y seleccionando datos

El paso 3 extrae cuentas en vivo de su tienda y muestra una muestra de los primeros cinco productos. Algunas cosas se ven diferentes en comparación con otras plataformas:

- **Colecciones, no categorías** — Shopify organiza productos en Colecciones en lugar de categorías, y las Colecciones no admiten anidamiento, por lo que la jerarquía se importa como plana. Si su tienda Shopify usó colecciones para representar un árbol de categorías, planee reconstruir esa estructura en el administrador de categorías de Spwig después de la importación.
- **Descuentos, no cupones** — Los códigos de descuento y reglas de Shopify se importan como descuentos de Spwig.
- **No hay fila de reseñas** — ya que Shopify no tiene una API de reseñas, este tipo de datos no aparece en este paso en absoluto, a diferencia de WooCommerce o importaciones CSV.

Las **Opciones de importación** funcionan de la misma manera que en otras plataformas: **Saltar elementos existentes** (activado) coincide en SKU y correo electrónico para evitar duplicados; **Importar imágenes del producto** (activado) es más lento pero recomendado; **Mantener los IDs originales cuando sea posible** (deshabilitado) debe mantenerse deshabilitado a menos que tenga un motivo específico para cambiarlo; **Tamaño del lote** se establece de forma predeterminada en 25.

## Metafields de Shopify

Si usa metafields de Shopify para almacenar datos adicionales en productos, clientes u órdenes, tenga en cuenta que Spwig no los detecta ni los lee — a diferencia de WooCommerce, no hay un paso de mapeo de campos personalizados para importaciones de Shopify. Cualquier dato que haya almacenado en metafields deberá ingresarse manualmente en Spwig usando [campos personalizados](migration-field-mapping) después de la migración, por lo que es útil exportar una lista de sus metafields y sus valores de Shopify antes de comenzar.

## Ejecutando la importación

Una vez que haya revisado el paso 3, inicie la importación. Se ejecuta en segundo plano — puede cerrar la ventana del navegador y seguirá ejecutándose. El paso 5 muestra el progreso en vivo con una fila por tipo de datos y un registro de actividad expandible.

El paso 6 muestra los resultados: qué se importó, se saltó o falló, más una herramienta de **Reescritura de enlaces** si se encontraron enlaces internos a su antiguo dominio `myshopify.com` en el contenido importado.

Revisa cuidadosamente el resumen, luego trabaja en la lista de verificación en [Después de tu migración](after-migration-review) — cubre verificar tus datos, reconstruir cualquier jerarquía de colecciones, configurar tasas de impuesto y envío (lo cual el asistente no configura para ti), y volver a ingresar cualquier cosa que se almacenara en metafields.

## Elimina la aplicación de Shopify

Una vez que hayas confirmado que la migración se completó con éxito, vuelve a la página **Apps** del administrador de Shopify, o al panel de Partners, y elimina la aplicación de migración de Spwig (o al menos desinstálala de tu tienda). No hay razón para dejar activo el acceso de lectura a los datos de tu tienda una vez que la migración esté completa.

## Consejos

- **El historial de pedidos está limitado por defecto** — si necesitas más de los últimos 60 días de pedidos, agrega `read_all_orders` a la lista de alcance antes de generar tu enlace de instalación, no después.
- **Las reseñas necesitan una exportación separada** — planifica esto antes de migrar, ya que no hay forma de traer las reseñas a través del asistente en absoluto.
- **Generar el enlace no es lo mismo que instalar la aplicación** — siempre completa el Paso 5 y haz clic en Instalar, o la prueba de conexión en Spwig fallará.
- **Las colecciones vienen en forma plana** — si tu estructura de categorías importaba para la navegación o el SEO, presupuesta tiempo para reconstruir la jerarquía en Spwig después de la importación.
- **Exporta tus metafields primero** — Spwig no puede leerlos, así que captura esos datos de Shopify antes de comenzar si los necesitarás más tarde.
- **Elimina la aplicación una vez que estés verificado** — no dejes una integración activa apuntando a tu tienda antigua después de que hayas terminado.