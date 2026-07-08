---
title: Sincronización de Configuración
---

La sincronización de configuración le permite copiar la configuración de la tienda entre dos instalaciones de Spwig. Esto es ideal para mantener entornos de pruebas y producción, donde configura y prueba cambios en el entorno de pruebas antes de implementarlos en su tienda en vivo.

## ¿Cuándo Usar la Sincronización de Configuración

- **De Pruebas a Producción**: Configure la configuración en su tienda de pruebas, luego envíela a producción
- **De Producción a Pruebas**: Extraiga la configuración de producción a pruebas para comenzar con un entorno coincidente
- **Copia de Seguridad de Configuración**: Extraiga la configuración de producción a una instancia de copia de seguridad como medida de protección

La sincronización de configuración maneja solo datos de configuración — no transfiere productos, clientes, pedidos ni archivos multimedia. Para una transferencia de datos completa, use la Migración del Sistema Completo en su lugar.

## ¿Qué Se Puede Sincronizar

La sincronización de configuración admite las siguientes categorías:

| Grupo | Categorías |
|-------|-----------|
| **Configuración** | Configuración del Sitio, Impuestos y Monedas, Tarifas de Impuestos, Idiomas, Configuración del Blog, Compartición Social, Regiones de Venta y Almacenes, Configuración de Búsqueda, Campos Personalizados, Roles del Personal, Análisis de Clientes |
| **Diseño** | Diseño y Tema, Encabezados/Pie de Página/Menús |
| **Proveedores** | Correo Electrónico, SMS/WhatsApp, Proveedores de Pago, Envío, Proveedores de SEO, Feeds de Productos, Conectores Sociales del Blog, Configuración de POS |
| **Contenido** | Páginas y Plantillas, Posts del Blog, Anuncios, Formularios, Colecciones de Productos |
| **Comercio** | Reglas de Comercio (Vales, Promociones, Lealtad, Suscripciones), Programa de Afiliados, Webhooks e Integraciones |

> **Nota:** Las categorías que contienen credenciales (proveedores de pago, cuentas de envío, etc.) se marcan con un icono de llave. Las claves API y secretos se transfieren de forma segura, pero pueden necesitar ser reingresadas para integraciones basadas en OAuth.

## Guía Paso a Paso

### Paso 1: Configurar una Conexión

1. Navegue hasta **Migración de Datos > Sincronización Spwig a Spwig** en el menú lateral de administración
2. Haga clic en **Iniciar Sincronización de Configuración**
3. Seleccione una conexión guardada o cree una nueva:
   - Ingrese la URL de la tienda remota (por ejemplo, `https://staging.yourstore.com`)
   - Pegue el token de sincronización generado en la tienda remota
   - Asigne un nombre descriptivo a la conexión
   - Establezca el rol (Pruebas, Producción, Copia de Seguridad o Otro)
4. Haga clic en **Probar Conexión** para verificar que funcione
5. Haga clic en **Siguiente** para continuar

### Paso 2: Elegir Categorías y Dirección

**Dirección:**
- **Extraer** — Copia la configuración de la tienda conectada a esta tienda
- **Enviar** — Copia la configuración de esta tienda a la tienda conectada

**Modo de Sincronización:**
- **Añadir y Actualizar** — Añade nuevos elementos y actualiza los existentes, pero nunca elimina nada. Esta es la opción más segura.
- **Copia Exacta** — Hace que el destino coincida exactamente con la fuente, incluyendo eliminar elementos que existen en el destino pero no en la fuente. Use con precaución.

Seleccione las categorías que desee incluir, luego haga clic en **Siguiente**.

### Paso 3: Previsualizar Cambios

Antes de aplicar cualquier cambio, verá una previsualización detallada que muestra exactamente qué elementos se agregarán, modificarán o eliminarán en cada categoría. Revíselo cuidadosamente.

Si está enviando a una conexión de producción, deberá confirmar que entiende que los cambios afectarán su tienda en vivo.

Haga clic en **Iniciar Sincronización** cuando esté listo.

### Paso 4: Supervisar el Progreso

La sincronización se ejecuta en segundo plano. Puede navegar libremente lejos de la página de progreso — la sincronización continuará ejecutándose.

La página de progreso muestra:
- Porcentaje de completitud general con tiempo estimado restante
- Progreso por categoría con conteos de éxito/error
- Un registro de actividad en vivo que puede expandir para ver salida detallada

## Retroceso

Después de que una sincronización se complete, tiene **24 horas** para retroceder los cambios. Un retroceso restaura el estado anterior de todas las configuraciones afectadas.

Para retroceder:
1. Vaya a **Panel de Sincronización**
2. Encuentre el trabajo completado
3. Haga clic en **Retroceder** y confirme

Después de 24 horas, la opción de retroceso expira y los cambios se vuelven permanentes.

## Consejos

Conservar todo el formato de markdown, rutas de imágenes, bloques de código y términos técnicos.

- **Prueba en entorno de pruebas primero**:

Siempre sincroniza primero con un entorno de pruebas para verificar los resultados antes de enviar a producción

- **Usa el modo Añadir y Actualizar**:

Este es el modo más seguro ya que nunca elimina datos existentes

- **Revisa cuidadosamente la vista previa**:

La vista previa de diferencias te muestra exactamente qué cambiará antes de que se aplique algo

- **Las conexiones de producción muestran advertencias**:

Cuando se envía a una conexión marcada como Producción, se requieren confirmaciones adicionales de seguridad