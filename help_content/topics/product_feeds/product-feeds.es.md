---
title: Feeds de productos
---

Los feeds de productos le permiten exportar su catálogo a plataformas de compras como Google Shopping y Facebook Catalog. Una vez conectado, los datos de sus productos se sincronizan automáticamente según un horario, por lo que sus anuncios siempre reflejarán sus precios actuales, existencias y detalles del producto.

Su tienda utiliza un sistema de componentes de proveedores para los feeds. Cada proveedor de feeds (Google, Facebook u otros) se instala como un componente y luego se conecta a través de una cuenta del proveedor. Puede ejecutar varios proveedores de feeds al mismo tiempo, por ejemplo, un feed para Google Shopping y otro separado para Facebook.

## Conectar un proveedor de feeds

Antes de poder sincronizar su catálogo, debe instalar y conectar al menos un componente de proveedor de feeds.

### Instalando un componente de proveedor

Los componentes de proveedor están disponibles en el mercado de componentes de Spwig. Su administrador de tienda los instala a través del sistema de actualización de componentes. Una vez instalado un componente de proveedor, aparece como una opción al crear una cuenta de proveedor de feeds.

### Crear una cuenta de proveedor de feeds

1. Navegue a **Marketing > Proveedores de Feeds**
2. Haga clic en **+ Agregar Cuenta de Proveedor de Feeds**
3. Complete el formulario:

**Sección de información del proveedor:**
- **Sitio** — seleccione su tienda (solo hay una)
- **Componente del proveedor** — elija el proveedor de feeds instalado (por ejemplo, Google Shopping, Facebook Catalog)
- **Nombre de cuenta** — un nombre descriptivo como `Google Shopping — Principal` o `Facebook Catalog — EE.UU.`

**Sección de configuración:**
- **Activo** — marque para habilitar la generación de feeds y la sincronización
- **Principal** — marque si este es su proveedor de feeds principal para este tipo de plataforma
- **Prioridad** — controla el orden de clasificación en la lista (los números más bajos aparecen primero)
- **Config** — configuraciones específicas del proveedor (ver más abajo)

4. Haga clic en **Guardar**

### Opciones de configuración del feed

El campo **Config** acepta un objeto JSON con las siguientes opciones:

| Opción | Valores | Descripción |
|--------|--------|-------------|
| `sync_interval` | `hourly`, `daily`, `weekly`, `manual` | Con qué frecuencia se regenera automáticamente el feed |
| `format_preference` | `xml`, `csv`, `json` | Formato de salida (la mayoría de las plataformas prefieren XML) |
| `include_variants` | `true` / `false` | Incluir variantes de productos como entradas de feed separadas |
| `target_country` | Código de país, por ejemplo, `"US"` | País objetivo para el feed |
| `content_language` | Código de idioma, por ejemplo, `"en"` | Idioma de los datos del producto |

#### Ejemplo de configuración para un feed XML diario dirigido a EE.UU.:

```json
{
  "sync_interval": "daily",
  "format_preference": "xml",
  "include_variants": true,
  "target_country": "US",
  "content_language": "en"
}
```

## Filtrar qué productos aparecen en el feed

Puede controlar exactamente qué productos se incluyen agregando una sección `product_filter` a la configuración:

```json
{
  "product_filter": {
    "status": ["published"],
    "in_stock_only": true,
    "categories": [1, 5, 12]
  }
}
```

| Opción de filtro | Descripción |
|---------------|-------------|
| `status` | Solo incluir productos con estos estados. Use `["published"]` para productos activos solo. |
| `in_stock_only` | Establezca en `true` para excluir productos agotados |
| `categories` | Limitar a IDs de categorías específicas |
| `brands` | Limitar a IDs de marcas específicas |

También puede excluir productos específicos por sus IDs usando `exclude_products`:

```json
{
  "exclude_products": [42, 87, 103]
}
```

## Monitorear el estado de la sincronización

La lista de cuentas de proveedores de feeds muestra el estado de sincronización de cada feed conectado a primera vista:

- **PENDIENTE** — no se ha ejecutado ninguna sincronización aún, o el feed está esperando para ser generado
- **SINCRONIZANDO** — una sincronización está en curso
- **ÉXITO** — la última sincronización se completó sin errores
- **ERROR** — la última sincronización falló; el mensaje de error se muestra en la página de detalles de la cuenta

La lista también muestra la cantidad de productos en el feed actual y cuándo se ejecutó la última sincronización.

## Ver feeds generados

Navegue a **Marketing > Feeds de Productos** para ver los archivos de feeds generados. Cada entrada representa una captura de pantalla de un feed generado y muestra:

- **Cuenta del proveedor** — a la cual pertenece este feed
- **Formato** — XML, CSV o JSON
- **Cantidad de productos** — número de productos incluidos
- **Tamaño** — tamaño del archivo del feed generado
- **Generado en** — cuando se creó
- **Vence en** — cuando expira esta versión almacenada en caché
- **Estado** — si el feed sigue siendo válido o ha expirado
- **Cantidad de descargas** — cuántas veces se ha descargado este feed

Los feeds son de solo lectura en el administrador — se generan automáticamente por el proceso de sincronización.

## Ver historial de sincronización

Navegue hasta **Marketing > Registro de sincronización de feeds** para ver un historial completo de cada intento de sincronización para todas sus cuentas de feed. Cada entrada del registro registra:

- La cuenta del proveedor que se sincronizó
- El tipo de sincronización (Completa, Incremental, Manual o Programada)
- Estado (Éxito, Éxito parcial, Fallido, etc.)
- Productos sincronizados, fallidos y omitidos
- Duración de la sincronización
- Cualquier mensaje de error

El panel de registro de sincronización en la parte superior de la página muestra estadísticas generales: total de sincronizaciones, tasa de éxito y duración promedio de la sincronización. Use los filtros **Cuenta** y **Tipo de sincronización** para acotarse a un feed específico.

### Qué hacer cuando una sincronización falla

1. Navegue hasta **Marketing > Registro de sincronización de feeds** y encuentre la entrada fallida
2. Haga clic en la entrada del registro para ver el mensaje de error completo y los detalles del error
3. Causas comunes incluyen:
   - Campos de productos requeridos faltantes (título, precio, imagen)
   - Credenciales de API inválidas o expiradas — reinstale el componente del proveedor para refrescar las credenciales
   - Errores de red al conectarse a la API del proveedor
4. Una vez que se resuelva el problema, la próxima sincronización programada se ejecutará automáticamente, o puede desencadenar una sincronización manual desde la cuenta del proveedor

## Consejos

- Establezca `"sync_interval": "daily"` para la mayoría de los casos de uso — Google y Facebook no requieren actualizaciones más frecuentes a menos que tenga una alta volatilidad de precios
- Incluya siempre `"in_stock_only": true` en su filtro de productos para evitar anunciar productos que los clientes no pueden comprar
- Use un nombre descriptivo para la cuenta que incluya la plataforma y el mercado objetivo (por ejemplo, `Google Shopping — UK`) para facilitar la gestión de múltiples feeds
- La cantidad de **Productos en el feed** en la cuenta del proveedor le indica inmediatamente si se están incluyendo menos productos de los esperados — revise la configuración de su filtro de productos si la cantidad parece baja
- Marque una cuenta como **Feed principal** para cada tipo de proveedor; algunas herramientas de informes usan esto para identificar su feed principal
- Revise el registro de sincronización después de cualquier cambio masivo en su catálogo de productos para confirmar que los datos actualizados se capturaron correctamente