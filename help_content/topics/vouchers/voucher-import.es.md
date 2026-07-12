---
title: Importar en批量 Voucher Codes
---

El asistente para importar cupones le permite crear cientos de códigos de cupón a la vez cargando una hoja de cálculo CSV o XLSX. Esto es ideal cuando tiene códigos ya impresos, códigos de programas de lealtad de un sistema de terceros, o simplemente necesita lanzar una campaña grande sin agregar cada código manualmente.

![Lista de cupones con botón de importación](/static/core/admin/img/help/voucher-import/voucher-list-import-button.webp)

## Comenzar una importación

Navegue hasta **Marketing > Vouchers** y haga clic en el botón **Importar** en el área superior derecha de la página. Esto abre el asistente de importación de tres pasos.

## Paso 1: Cargue su archivo y establezca las configuraciones de lote

![Formulario de carga de importación](/static/core/admin/img/help/voucher-import/import-upload.webp)

La primera página tiene dos partes: la carga de archivos y las configuraciones de descuento por lotes.

### Preparar su archivo

Cargue un archivo `.csv` o `.xlsx` de hasta 5 MB. El archivo debe tener una fila de encabezado como primera fila. El requisito mínimo es una columna que contenga los códigos de cupón — todas las demás columnas son opcionales.

El importador reconoce automáticamente nombres de columnas comunes. Si su archivo usa alguno de los nombres siguientes, Spwig seleccionará previamente la asignación correcta en la siguiente página sin necesidad de hacer clic adicional:

| Su nombre de columna | Se mapea a |
|---------------------|-----------|
| `code`, `voucher_code`, `coupon_code`, `promo_code` | Código de cupón |
| `name`, `title`, `campaign` | Nombre interno |
| `description`, `details`, `note` | Descripción orientada al cliente |
| `external_id`, `member_id`, `reference` | ID externo |

**Consejo:** Descargue primero la plantilla XLSX (vea [Exportar cupones como plantilla](#exporting-vouchers-as-a-template) a continuación) — utiliza exactamente los nombres de columna que el importador espera, por lo que la asignación de columnas es automática.

### Límites de archivo

- Tamaño máximo de archivo: **5 MB**
- Máximo de filas por importación: **5,000 códigos**

### Establecer configuraciones de descuento por lotes

Cada cupón en el lote compartirá las mismas configuraciones de descuento que configure en esta página. Rellene los campos como lo haría al crear un cupón individual:

**Sección de descuento**

| Campo | Descripción |
|-------|-------------|
| **Tipo de descuento** | Porcentaje, monto fijo o envío gratuito |
| **Valor del descuento** | El porcentaje (0–100) o monto fijo a deducir |
| **Monto máximo de descuento** | Límite opcional en descuentos por porcentaje (por ejemplo, limitar un descuento del 20% a $50) |
| **Ámbito de aplicación** | Carrito completo, productos específicos o categorías específicas |

**Sección de validez**

| Campo | Descripción |
|-------|-------------|
| **Fecha de inicio** | Cuando los códigos se activan (por defecto es ahora si se deja en blanco) |
| **Fecha de finalización** | Cuando los códigos expiran (dejar en blanco para no tener fecha de expiración) |
| **Días válidos** | Alternativa a la fecha de finalización — los códigos expiran este número de días después de su creación |

**Sección de límites de uso**

| Campo | Descripción |
|-------|-------------|
| **Máximo de usos totales** | Número total de redenciones permitidas para todos los clientes (en blanco = ilimitado) |
| **Máximo de usos por cliente** | Cuántas veces un cliente puede usar cualquier código de este lote |
| **Valor mínimo del pedido** | Valor mínimo del carrito requerido antes de que se aplique el código |

**Restricciones**

Marque cualquier combinación de:
- **No se puede aplicar a artículos en oferta** — impide que el código se acumule con productos ya descuentados
- **No se puede combinar con otros cupones** — impide que los clientes usen dos códigos en el mismo pedido
- **No se puede combinar con artículos en oferta** — similar al anterior pero enfocado en artículos con precios de oferta
- **Solo para clientes nuevos** — restringe el código a clientes sin pedidos anteriores completados
- **Activo inmediatamente** — deje marcado para hacer los códigos activos en el momento en que se importen

Cuando esté satisfecho con las configuraciones, haga clic en **Continuar a vista previa**.

## Paso 2: Mapear columnas y revisar

![Página de mapeo de columnas y vista previa](/static/core/admin/img/help/voucher-import/import-preview.webp)

La página de vista previa muestra cuatro contadores de resumen en la parte superior:

- **Filas analizadas** — total de filas de datos encontradas en tu archivo

- **Se importarán** — nuevos códigos que se crearán

- **Duplicados** — códigos que ya existen en tu catálogo

- **Se omitirán (inválidos)** — filas rechazadas debido a errores de validación (código vacío, código demasiado largo, etc.)

### Mapeo de columnas

La **tabla de mapeo de columnas** te permite indicarle a Spwig qué columna de tu archivo corresponde a cada campo del cupón. Spwig detecta automáticamente nombres de encabezado comunes (ver la tabla anterior), pero puedes cambiar cualquier mapeo usando el menú desplegable de cada fila.

Solo la columna **Código del cupón** es obligatoria. Los otros campos — **Nombre interno**, **Descripción para el cliente** y **ID externo** — son opcionales. Si los omites, Spwig usa valores predeterminados sensibles (el nombre interno por defecto es "Cupón importado {code}").

### Estrategia de código duplicado

Si hay algún código en tu archivo que ya exista en tu catálogo, debes elegir cómo manejarlos:

| Estrategia | Qué ocurre |

|----------|-------------|

| **Saltar duplicados** | Los códigos existentes se dejan exactamente como están. Solo se crean nuevos códigos. |

| **Sobrescribir ajustes** | Los códigos existentes se actualizan con los ajustes de descuento de este lote. Sus códigos, conteos de uso y fechas de creación se mantienen. |

| **Fallar la importación** | La importación completa se cancela si se encuentra incluso un duplicado. Usa esto cuando necesites una garantía de que ningún código existente se ve afectado. |

Cualquier código duplicado encontrado se muestra en un panel expandible para que puedas revisarlo antes de decidir.

### Tabla de vista previa de datos

La parte inferior de la página muestra las primeras 20 filas de tu archivo para que puedas confirmar que el mapeo de columnas parece correcto antes de comprometerte. Las filas que coinciden con códigos existentes se resaltan.

Cuando todo parezca correcto, haz clic en **Importar N cupones** para comprometerte con el lote.

## Paso 3: Revisar el resultado

![Página de resultados de importación](/static/core/admin/img/help/voucher-import/import-result.webp)

Después de que la importación se complete, verás un resumen que muestra:

- **Importados** — códigos creados con éxito

- **Omitidos** — códigos que no se crearon (duplicados o filas inválidas)

- **Filas procesadas** — total de filas de tu archivo que se evaluaron

- **Fallidos** — filas que encontraron un error inesperado

Haz clic en **Ver cupones importados** para abrir la lista de cupones filtrada solo para los códigos de este lote, lo que facilita revisar el resultado o activar en masa los nuevos códigos.

Si algo parece incorrecto — por ejemplo, se aplicó el tipo de descuento equivocado — puedes usar la estrategia **Sobrescribir ajustes** en una nueva importación para corregir el lote sin tener que eliminar y recrear los códigos.

Haz clic en **Importar otro lote** para iniciar una subida nueva, o en **Volver a la lista de cupones** para regresar a tu catálogo completo.

## Exportar cupones como plantilla

La lista de cupones admite una acción de exportación en formato XLSX que genera un archivo en el mismo orden de columnas que el importador espera. Este es la forma más sencilla de obtener una plantilla correctamente formateada:

1. Navega a **Marketing > Cupones**

2. Selecciona los cupones que deseas exportar (o selecciona todos)

3. Elige **Exportar cupones seleccionados a XLSX** desde el menú desplegable **Acción**

4. Haz clic en **Ir**

El archivo descargado contiene todas las 21 columnas que el importador entiende, incluyendo campos que son de nivel de lote en el asistente de importación (tipo de descuento, fechas, límites de uso, etc.). Puedes usar este archivo como referencia o hacer un ciclo de edición → reimportación de tus códigos existentes usando la estrategia **Sobrescribir ajustes**.

## Consejos

Mantén todo el formato de markdown, rutas de imágenes, bloques de código y términos técnicos.

- Descargue primero una exportación XLSX para usarla como plantilla — los nombres de las columnas están pre-formateados para que el mapeo automático los detecte sin necesidad de ajustes en la página de vista previa.
- Ejecute un lote de prueba pequeño de 5 a 10 códigos antes de importar cientos para verificar que su mapeo de columnas y configuraciones del lote sean correctas.
- Use **Días válidos** en lugar de una **Fecha de finalización** fija cuando los códigos se distribuyan con el tiempo — la caducidad de cada código se contará desde la fecha en que se importó, en lugar de una fecha del calendario única.
- Si recibe códigos de un sistema de lealtad de terceros, asocie la referencia de miembro o cliente del proveedor a la columna **ID externo** para poder reconciliar las redenciones más tarde.
- Después de una importación grande, haga clic en **Ver cupones importados** en la página de resultados para filtrar la lista solo al nuevo lote — luego puede editar en masa, activar o desactivarlos como grupo.
- Una importación fallida (usando la estrategia de duplicado **Fallar**) deja su catálogo sin cambios, por lo que es seguro corregir el archivo y volver a intentarlo tantas veces como sea necesario.