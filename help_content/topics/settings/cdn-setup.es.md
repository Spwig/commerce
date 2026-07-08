---
title: Configuración de CDN
---

Una Red de Entrega de Contenido (CDN) almacena copias de las imágenes, hojas de estilo y scripts de tu tienda en servidores alrededor del mundo. Cuando un cliente visita tu tienda, estos archivos se sirven desde el servidor más cercano a ellos en lugar de desde tu servidor de alojamiento principal. Esto reduce los tiempos de carga de la página, especialmente para clientes ubicados lejos del lugar donde se aloja tu tienda.

Spwig ya optimiza la entrega de activos estáticos de forma predeterminada con compresión previa con Brotli y gzip, almacenamiento en caché de activos con huella digital y encabezados inmutables de 1 año, y negociación de contenido adecuada. Agregar un CDN es opcional, pero puede mejorar aún más la velocidad para tiendas con una base de clientes internacional.

## ¿Necesita su tienda un CDN?

No todas las tiendas se benefician por igual de un CDN. Use estas pautas para decidir:

**Se recomienda un CDN si**:
- Sus clientes están distribuidos en múltiples países o continentes
- Su tienda tiene muchas imágenes de productos o páginas con mucho contenido multimedia
- Quiere los tiempos de carga de página más rápidos posibles a nivel mundial
- Vende a regiones lejos de su servidor de alojamiento (por ejemplo, servidor en Europa, clientes en Asia)

**Probablemente no es necesario un CDN si**:
- Sus clientes son principalmente locales o están en el mismo país que su servidor
- Su tienda tiene un catálogo pequeño con pocas imágenes
- Su proveedor de alojamiento ya incluye un CDN integrado

Cuando tenga dudas, un CDN no afecta el rendimiento. Servicios como Cloudflare ofrecen niveles gratuitos, por lo que no hay costo para probarlo.

## ¿Cómo funciona Spwig con CDNs

Spwig está listo para CDN de forma predeterminada. No necesita cambiar ningún código o configuración dentro del panel de administración de Spwig. Aquí es lo que Spwig ya hace por usted:

- **Archivos estáticos con huella digital** -- Cada archivo de CSS, JavaScript e imagen incluye un hash de versión única en su nombre de archivo. Esto significa que los CDNs pueden almacenar en caché estos archivos durante mucho tiempo sin servir contenido obsoleto.
- **Encabezados de caché de larga duración** -- Los activos estáticos se sirven con encabezados de caché inmutables de 1 año, indicando a los CDNs y navegadores que los almacenen de forma agresiva.
- **Archivos precompresos** -- Spwig precompresiona los activos usando Brotli y gzip, por lo que su CDN puede entregar archivos más pequeños sin procesamiento adicional.
- **Negociación de contenido adecuada** -- Spwig envía los encabezados de tipo de contenido y codificación correctos en los que los CDNs dependen para un almacenamiento en caché adecuado.

Todo lo que necesita hacer es apuntar los DNS de su dominio al proveedor de CDN, y todo funciona automáticamente.

## Configuración de Cloudflare

Cloudflare es la CDN más popular y ofrece un nivel gratuito que funciona bien para la mayoría de las tiendas. Siga estos pasos:

**Paso 1: Crear una cuenta de Cloudflare**
- Visite cloudflare.com y regístrese para una cuenta gratuita

**Paso 2: Agregar su dominio**
- Haga clic en **Agregar un sitio** y escriba el nombre de dominio de su tienda
- Seleccione el plan **Gratuito** (suficiente para la mayoría de las tiendas)

**Paso 3: Actualizar los servidores DNS**
- Cloudflare le mostrará dos servidores DNS (por ejemplo, `anna.ns.cloudflare.com`)
- Inicie sesión en su registrador de dominios (donde compró su dominio)
- Reemplace sus servidores DNS actuales con los servidores DNS de Cloudflare
- Los cambios de DNS pueden tardar hasta 24 horas en hacer efecto

**Paso 4: Configurar SSL/TLS**
- En el panel de Cloudflare, vaya a **SSL/TLS**
- Establezca el modo de encriptación en **Completo (estricto)**
- Esto asegura que todo el tráfico entre Cloudflare y su servidor permanezca encriptado

**Paso 5: Verificar que funcione**
- Una vez que los cambios de DNS se propaguen, visite su tienda y revise el encabezado `cf-cache-status` en su navegador (consulte Verificando su CDN a continuación)

## Configuración de AWS CloudFront

Si ya utiliza Amazon Web Services, CloudFront se integra naturalmente con su infraestructura:

1. Abra el **console de CloudFront** en su cuenta de AWS
2. Cree una nueva **Distribución** con el dominio de su tienda como origen
3. Establezca la **Política de protocolo de origen** en "HTTPS Only"
4. Bajo **Comportamiento de caché**, establezca **Política de caché** en "CachingOptimized" para activos estáticos
5. Agregue el dominio de su tienda como **Nombre de dominio alternativo (CNAME)**
6. Adjunte un certificado SSL de AWS Certificate Manager
7. Actualice los DNS de su dominio para apuntar al URL de la distribución de CloudFront

El precio de CloudFront es basado en el uso.

Para la mayoría de las tiendas, los costos son mínimos ya que los activos con huella de Spwig se cachean durante períodos largos.

## Configuración Recomendada de CDN

Para obtener los mejores resultados, configure su CDN para cachear el contenido correcto y omitir el resto.

**¿Qué cachear** (activos estáticos):
- `/static/` -- Todos los estilos, scripts, fuentes y activos del tema
- `/media/` -- Imágenes de productos y archivos de medios subidos
- Archivos de imagen (`.jpg`, `.png`, `.webp`, `.svg`, `.gif`)
- Archivos de fuente (`.woff`, `.woff2`)

**¿Qué NO cachear** (páginas dinámicas):
- `/admin/` -- El panel de administración debe siempre servir contenido fresco
- `/cart/` -- Las páginas del carrito de compras contienen datos específicos de sesión
- `/checkout/` -- Las páginas de pago nunca deben cachearse por razones de seguridad
- `/accounts/` -- Las páginas de cuentas de clientes contienen datos privados
- Cualquier página que requiera inicio de sesión o muestre contenido personalizado

**Reglas generales de caché**:
- **Respetar los encabezados de caché del origen** -- Spwig envía los encabezados correctos de control de caché para cada tipo de contenido. Configure su CDN para respetar estos encabezados en lugar de sobrescribirlos.
- **Habilitar la compresión Brotli** -- Tanto Cloudflare como CloudFront admiten Brotli. Hágalo para aprovechar los activos precompresos de Spwig.
- **Establecer el TTL de caché del navegador a "Respetar los Encabezados Existentes"** -- Esto permite que la política de caché integrada de Spwig determine el comportamiento.

## Verificando su CDN

Después de la configuración, confirme que el CDN está sirviendo correctamente su contenido:

**Paso 1: Abrir las Herramientas de Desarrollador del Navegador**
- En Chrome o Firefox, presione **F12** para abrir las herramientas de desarrollador
- Haga clic en la pestaña **Red** (Network)

**Paso 2: Cargar su Tienda**
- Visite la página de inicio de su tienda con las herramientas de desarrollador abiertas
- Haga clic en cualquier solicitud de archivo estático (por ejemplo, un archivo `.css` o `.js`)

**Paso 3: Verificar los Encabezados de Respuesta**
- **Cloudflare**: Busque el encabezado `cf-cache-status`. Un valor de `HIT` significa que el archivo se sirvió desde la caché del CDN. `MISS` significa que se obtuvo desde su servidor (solo en la primera solicitud).
- **CloudFront**: Busque el encabezado `x-cache`. Un valor de `Hit from cloudfront` confirma la entrega del CDN.

**Paso 4: Probar desde Otra Ubicación**
- Use una herramienta gratuita como gtmetrix.com o webpagetest.org para probar su tienda desde diferentes ubicaciones geográficas
- Compare los tiempos de carga antes y después de la configuración del CDN

## Problemas Comunes

### Contenido Obsoleto Después de Cambios en el Tema

**Problema**: Después de actualizar su tema o hacer cambios de diseño, los clientes aún ven la versión antigua.

**Solución**: Limpiar la caché del CDN. En Cloudflare, vaya a **Caching > Configuration > Purge Everything**. En CloudFront, cree una **Invalidación** para `/*`. Tenga en cuenta que los activos con huella de Spwig normalmente previenen este problema ya que los archivos actualizados reciben automáticamente nuevos nombres de archivos. Este problema afecta principalmente activos sin huella, como subidas personalizadas.

---

### Advertencias de Contenido Mezclado

**Problema**: Su navegador muestra una advertencia de seguridad sobre "contenido mezclado" después de habilitar el CDN.

**Solución**: Asegúrese de que el modo SSL de su CDN esté configurado en **Full (strict)**, no en "Flexible". El modo Flexible puede hacer que su servidor reciba solicitudes HTTP en lugar de HTTPS, lo que lleva a advertencias de contenido mezclado. En Cloudflare, revise **SSL/TLS > Overview** y verifique el modo.

---

### Panel de Administración Funcionando Lento

**Problema**: El panel de administración se siente más lento después de agregar un CDN.

**Solución**: Los CDNs no deben cachear páginas de administración. Cree una **Regla de Página** (Cloudflare) o **Comportamiento de Caché** (CloudFront) que establezca la caché en "Bypass" para cualquier URL que coincida con `/admin/*`. Esto asegura que las solicitudes de administración vayan directamente a su servidor sin sobrecarga del CDN.

---

### Imágenes que No Se Cargan

**Problema**: Las imágenes de productos o archivos de medios devuelven errores después de la configuración del CDN.

**Solución**: Verifique que la configuración del origen de su CDN tenga el protocolo correcto (HTTPS) y el puerto. También revise que su servidor permita conexiones desde las direcciones IP del CDN.

## Consejos

Conservar todo el formato markdown, rutas de imágenes, bloques de código y términos técnicos.

- **Comience con la versión gratuita de Cloudflare** -- Cubre las necesidades de la mayoría de las tiendas y solo toma minutos configurarla
- **Siempre use el modo SSL completo (estricto)** -- El modo flexible crea vulnerabilidades de seguridad y puede romper los flujos de pago
- **Limpie su caché de CDN después de actualizaciones importantes del tema** -- Aunque los archivos con huella dactilar de Spwig manejan la mayoría de los casos, una limpieza completa del caché asegura que no quede contenido obsoleto
- **No almacene en caché las páginas de pago o carrito** -- Almacenar en caché estas páginas puede exponer los datos de un cliente a otro
- **Pruebe desde las ubicaciones de sus clientes** -- Use herramientas gratuitas como webpagetest.org para medir el rendimiento real desde las regiones donde sus clientes compran
- **Monitorea las analíticas de tu CDN** -- Tanto Cloudflare como CloudFront ofrecen dashboards que muestran las tasas de aciertos en el caché, el ancho de banda ahorrado y el tráfico por país
- **Mantén el TTL de DNS bajo durante la configuración** -- Establece el TTL de DNS en 300 segundos (5 minutos) mientras te cambias a una CDN, luego aumenta el valor una vez que todo esté confirmado funcionando
- **Una CDN no reemplaza un buen alojamiento** -- Tu servidor de origen sigue siendo importante para páginas dinámicas como pago, carrito y administración.

Elige un alojamiento de calidad junto con una CDN