---
title: Configuración de GeoIP
---

GeoIP permite que tu tienda detecte automáticamente de dónde proviene cada visitante según su dirección IP. Esto activa características basadas en la ubicación en toda tu tienda, desde mostrar la moneda correcta por defecto, hasta ejecutar reglas comerciales geográficas, hasta ver desgloses a nivel de país en tus análisis.

Tu tienda viene preconfigurada con el servicio de GeoIP de Spwig, por lo que la detección geográfica funciona de forma inmediata. También puedes conectar proveedores adicionales para una mayor precisión, usar una base de datos que descargues tú mismo, o depender de encabezados de un CDN para búsquedas sin latencia.

## Cómo funcionan los proveedores

Navega a **Clientes > Proveedores de GeoIP** para ver los proveedores configurados para tu tienda. Cada proveedor maneja las búsquedas de IP a ubicación usando un método diferente. Cuando un visitante llega, tu tienda consulta a los proveedores activos en orden de prioridad y usa el primer resultado exitoso.

Pueden estar activos varios proveedores a la vez — se intentan primero los de menor número de prioridad. Si el proveedor de mayor prioridad falla o devuelve ningún dato, se intenta automáticamente el siguiente.

### Tipos de proveedores disponibles

| Proveedor | Descripción |
|----------|-------------|
| **Spwig GeoIP** | Búsqueda basada en la nube por defecto a través del servicio de Spwig. No requiere configuración. |
| **MaxMind GeoLite2** | Base de datos offline de MaxMind. Alta precisión. Requiere una clave de licencia gratuita. |
| **DB-IP Lite** | Base de datos offline de DB-IP. Descargue desde su sitio web. |
| **IP2Location LITE** | Base de datos offline de IP2Location. Requiere una inscripción gratuita. |
| **Encabezados de borde de CDN** | Lee encabezados de ubicación inyectados por tu CDN (por ejemplo, Cloudflare). Sin latencia. |
| **Pistas del navegador** | Usa la zona horaria/idioma proporcionado por el navegador como señal de ubicación suave. |
| **Proveedor personalizado** | Un componente de proveedor instalado desde el mercado de componentes de Spwig. |

## Añadir un proveedor

### Usando el servicio Spwig GeoIP (por defecto)

El proveedor Spwig GeoIP se añade automáticamente en nuevas instalaciones. Verifica que aparezca en la lista y que **Está activo** esté marcado. No se requiere configuración adicional.

### Añadir una base de datos MaxMind GeoLite2

MaxMind ofrece una base de datos gratuita offline que da resultados precisos sin enviar búsquedas a un servicio externo.

1. Regístrate para una cuenta gratuita en maxmind.com y genera una clave de licencia
2. Navega a **Clientes > Proveedores de GeoIP** y haz clic en **+ Añadir Proveedor de GeoIP**
3. Llena el formulario:
   - **Nombre**: `MaxMind GeoLite2` (o cualquier nombre descriptivo)
   - **Tipo de proveedor**: MaxMind GeoLite2
   - **Está activo**: marcado
   - **Prioridad**: `1` (menor que la predeterminada de Spwig para probarla primero, o mayor para usarla como respaldo)
   - **Clave de licencia**: pega tu clave de licencia de MaxMind
   - **URL de la base de datos**: la URL de descarga desde tu panel de control de cuenta de MaxMind
4. Haz clic en **Guardar**

Después de guardar, selecciona el proveedor en la lista y usa la acción **Actualizar bases de datos del proveedor seleccionado** para verificar que la URL de la base de datos sea accesible.

### Añadir encabezados de borde de CDN

Si tu tienda se encuentra detrás de un CDN que inyecta encabezados de geolocalización (como el `CF-IPCountry` de Cloudflare), puedes usar esos encabezados para la detección inmediata de país sin latencia.

1. Navega a **Clientes > Proveedores de GeoIP** y haz clic en **+ Añadir Proveedor de GeoIP**
2. Establece **Tipo de proveedor** en **Encabezados de borde de CDN**
3. Establece **Prioridad** en `0` (mayor prioridad, ya que los encabezados son la fuente más rápida)
4. En el campo **Config**, especifica qué encabezado usa tu CDN:
   ```json
   {
     "header_name": "CF-IPCountry"
   }
   ```
5. Haz clic en **Guardar**

## Probar un proveedor

Después de añadir un proveedor, puedes verificar que funcione correctamente:

1. En la lista de Proveedores de GeoIP, selecciona el proveedor usando su casilla de verificación
2. Abre el menú desplegable **Acción** y elige **Probar proveedores seleccionados**
3. Haz clic en **Ir**

Spwig enviará una búsqueda de prueba para una dirección IP conocida (el DNS público de Google, `8.8.8.8`) y te mostrará el resultado. Una prueba exitosa muestra el país devuelto y el tiempo de respuesta en milisegundos.

## Establecer la prioridad del proveedor

Cuando hay múltiples proveedores activos, el campo **Prioridad** controla cuál se intenta primero.

Los números más bajos indican una prioridad más alta.

Por ejemplo, para usar primero los encabezados del borde del CDN (más rápido) y recurrir al Spwig GeoIP:

| Proveedor | Prioridad |
|----------|----------|
| CDN Edge Headers | 0 |
| Spwig GeoIP | 10 |

Puedes editar la prioridad directamente en la vista de lista — la columna **Prioridad** es editable en línea.

## Monitoreo del rendimiento del proveedor

Cada registro de proveedor rastrea sus propias estadísticas de precisión:

- **Total Lookups** — número total de búsquedas de IP intentadas
- **Successful Lookups** — búsquedas que devolvieron un resultado
- **Failed Lookups** — búsquedas que devolvieron ningún dato o un error
- **Average Response (ms)** — tiempo de respuesta promedio en milisegundos
- **Accuracy** — porcentaje de búsquedas exitosas

Si un proveedor muestra una tasa de precisión baja o tiempos de respuesta altos, considere ajustar su prioridad o deshabilitarlo en favor de una opción con mejor rendimiento.

## Mapeos de países

Navegue a **Customers > Country Mappings** para configurar los valores predeterminados por país para moneda, idioma, impuesto y envío. Cada entrada de país controla:

- **Default Currency** — la moneda predeterminada seleccionada para visitantes de ese país
- **Default Language** — el idioma mostrado a los visitantes de ese país
- **Tax Rate** — el porcentaje de impuesto predeterminado aplicado para ese país
- **Is EU Member** / **Requires VAT** — se usa para la lógica de cumplimiento fiscal de la UE
- **Shipping Zone** — vincula el país a una zona de envío
- **Supports COD** — habilita el pago en efectivo al entregar para ese país

Puedes editar los campos **Is Active**, **Default Currency** y **Default Language** directamente en la lista sin abrir cada registro.

## Consejos

- El proveedor Spwig GeoIP funciona inmediatamente sin configuración — solo agrega proveedores adicionales si necesitas una precisión más alta o operación fuera de línea
- Si usas Cloudflare, el proveedor CDN Edge Headers es la mejor opción: no agrega latencia y no cuenta contra ningún cupo de API
- Mantén solo los proveedores que realmente necesitas activos — tener muchos proveedores activos no mejora la precisión si el primero ya tiene éxito
- Revisa las estadísticas de precisión semanalmente y deshabilita cualquier proveedor con una tasa de éxito inferior al 80%
- Los mapeos de países se usan como valores predeterminados; los clientes siempre pueden cambiar su moneda e idioma manualmente en la tienda en línea