---
title: Gestión de claves de licencia
---

La gestión de claves de licencia le permite controlar cómo se generan, almacenan y entregan las claves de licencia de software a los clientes cuando compran productos digitales. Spwig admite la generación de claves integrada, grupos de claves precargados y la integración con servicios externos de gestión de licencias.

## Visión general

Hay tres formas de gestionar claves de licencia en Spwig:

| Método | Mejor para |
|--------|---------|
| **Plantillas de licencia** | Generar automáticamente claves únicas en un formato personalizado en el momento de la compra |
| **Pools de licencias** | Generar previamente un lote de claves para su distribución masiva |
| **Proveedores externos** | Delegar la generación y gestión de claves a un servicio de terceros, como Keygen.sh |

Estos métodos se pueden combinar — por ejemplo, un pool puede usar una plantilla personalizada para definir el formato de la clave y, opcionalmente, sincronizar las claves generadas con un proveedor externo.

## Plantillas de claves de licencia

Una plantilla de clave de licencia define el *formato* de las claves generadas. Las plantillas usan un patrón con marcadores de posición que Spwig rellena en el momento de la generación.

### Crear una plantilla

1. Navegue a **Catálogo > Plantillas de claves de licencia**
2. Haga clic en **+ Agregar plantilla de clave de licencia**
3. Ingrese un **Nombre** (por ejemplo, `Licencia de aplicación estándar`)
4. Configure el **Patrón** usando marcadores de posición (ver más abajo)
5. Establezca el **Prefijo** y **Sufijo** si es necesario (por ejemplo, un prefijo de `MYAPP` agrega `MYAPP-` a cada clave)
6. Elija el **Caracter separador** (por defecto: `-`)
7. Establezca el **Conjunto de caracteres** — los caracteres utilizados para los segmentos aleatorios. El valor predeterminado excluye caracteres ambiguos como `0` y `O`, `1` y `I`
8. Establezca **Longitud mínima/máxima** para la validación
9. Haga clic en **Guardar**

### Marcadores de posición del patrón

| Marcador de posición | Descripción | Ejemplo de salida |
|-------------|-------------|---------------|
| `{RANDOM:N}` | N caracteres aleatorios del conjunto de caracteres | `{RANDOM:5}` → `K7JXQ` |
| `{CHECKSUM:N}` | N dígitos de checksum para la validación | `{CHECKSUM:2}` → `47` |
| `{PREFIX}` | El valor del prefijo de la plantilla | `MYAPP` |
| `{SUFFIX}` | El valor del sufijo de la plantilla | `PRO` |
| `{ORDER_ID}` | El número de pedido | `10045` |
| `{PRODUCT_SKU}` | El SKU del producto | `SOFTPRO` |
| `{DATE:FORMAT}` | Fecha formateada | `{DATE:YYMMDD}` → `260318` |

**Ejemplo de patrón**: `{PREFIX}-{RANDOM:5}-{RANDOM:5}-{RANDOM:5}-{CHECKSUM:2}`

Esto genera claves como: `MYAPP-K7JXQ-M3TPR-9BWKN-47`

### Previsualización de claves

Después de guardar una plantilla, en la lista de plantillas está disponible una acción **Generar clave de ejemplo**. Use esto para verificar que su patrón genere claves en el formato esperado antes de asignar la plantilla a un producto.

## Pools de licencias

Un pool de licencias es un lote de claves generadas previamente para un producto. Los pools son útiles cuando:
- Necesita claves para empaquetado físico (cajas de venta al por menor, tarjetas impresas)
- Trabaja con revendedores que necesitan lotes de claves
- Quiere generar claves con anticipación en lugar de a demanda

### Crear un pool de licencias

1. Navegue a **Catálogo > Pools de licencias**
2. Haga clic en **+ Agregar pool de licencias**
3. Rellene los detalles del pool:

| Campo | Descripción |
|-------|-------------|
| **Nombre** | Nombre descriptivo (por ejemplo, `Pack de venta al por menor Q1 2026`) |
| **Producto** | El producto para el cual estas claves son |
| **Plantilla de licencia** | Plantilla para el formato de la clave (por defecto, la plantilla del producto) |
| **Total de claves** | Cuántas claves generar |
| **Tipo de clave** | Perpetua, suscripción o prueba |
| **Máximo de activaciones** | Cuántos dispositivos puede activar cada clave |
| **Vence después de X días** | Días hasta que la licencia expire después de la primera activación (dejar en blanco para no tener vencimiento) |
| **Vence el pool el** | Fecha después de la cual las claves no utilizadas de este pool se vuelven inválidas |
| **Sincronizar con proveedor** | Opcionalmente sincronizar las claves generadas con un proveedor de licencias externo |

4. Haga clic en **Guardar** — Spwig comienza a generar las claves en segundo plano

### Estado del pool


| Estado | Significado |
|--------|---------|
| **Generando** | Se están creando las claves en segundo plano |
| **Listo** | Todas las claves generadas y disponibles para su distribución |
| **Agotado** | Todas las claves han sido asignadas a pedidos |
| **Caducado** | La fecha de caducidad del grupo ha pasado |

### Monitorear un grupo

La lista de grupos muestra cuántas claves han sido distribuidas versus el total de claves generadas. Abra un grupo para ver la lista completa de claves y sus estados individuales.

## Proveedores de licencias externos

Los proveedores externos son servicios de gestión de licencias de terceros que manejan la generación de claves y el seguimiento de su activación. Cuando un cliente completa una compra, Spwig se comunica con el proveedor para generar y registrar la clave.

### Proveedores compatibles

| Proveedor | Tipo |
|----------|------|
| **Servidor de licencias integrado de Spwig** | Integrado — no se requiere cuenta externa |
| **Keygen.sh** | API de gestión de licencias basada en la nube |
| **LicenseSpring** | Gestión de licencias empresarial |
| **Cryptlex** | Gestión de licencias con soporte para uso sin conexión |
| **API personalizado** | Cualquier sistema de licencias basado en REST |

### Conectar un proveedor

1. Navegue a **Catálogo > Proveedores de licencias**
2. Haga clic en **+ Agregar Proveedor de Licencias**
3. Rellene los detalles del proveedor:

| Campo | Descripción |
|-------|-------------|
| **Nombre** | Una etiqueta para esta conexión (ej. `Keygen Producción`) |
| **Tipo de Proveedor** | Seleccione entre los proveedores compatibles |
| **Punto Final de API** | URL base de la API del proveedor |
| **Clave de API** | Clave de autenticación para el proveedor |
| **Clave secreta de API** | Si es requerida por el proveedor |

4. Configure el comportamiento de sincronización:
   - **Sincronizar al completar el pedido** — Sincronizar automáticamente cuando un cliente complete una compra
   - **Sincronizar al activar** — Informar las activaciones de dispositivos al proveedor
   - **Sincronizar al desactivar** — Informar desactivaciones (útil para transferencias de licencias y reembolsos)
   - **Sincronización bidireccional** — Permitir que el proveedor actualice los registros de Spwig a través de webhooks

5. Haga clic en **Guardar**, luego haga clic en **Probar Conexión** para verificar que las credenciales funcionen

### Estado de la conexión

Cada proveedor muestra uno de tres estados de conexión:

| Estado | Significado |
|--------|---------|
| **No probado** | La conexión aún no ha sido verificada |
| **Conectado** | La última prueba fue exitosa |
| **Error** | La prueba de conexión falló — revise el mensaje de error |

### Sincronización de licencias existentes

Para enviar manualmente claves de licencia existentes a un proveedor (para la configuración inicial o después de una sincronización fallida), use la acción **Sincronizar ahora** desde la lista de proveedores.

## Monitorear la actividad de sincronización

Navegue a **Catálogo > Sincronización de licencias externas** para revisar el registro de sincronización. Cada registro muestra:
- La clave de licencia que se sincronizó
- El proveedor al que se envió
- Dirección (Spwig → Proveedor o Proveedor → Spwig)
- Estado (Pendiente, Éxito, Fallido)
- Detalles del error para las sincronizaciones fallidas

Las sincronizaciones fallidas se reintentan automáticamente. También puede forzar un reintento editando el registro y limpiando el error.

## Consejos

- Use el conjunto de caracteres predeterminado (`ABCDEFGHJKLMNPQRSTUVWXYZ23456789`) para evitar caracteres ambiguos que los clientes suelen malinterpretar — excluye `0`, `O`, `1` y `I`.
- Agregue un segmento `{CHECKSUM}` a su patrón de plantilla para que los clientes y su equipo de soporte puedan detectar rápidamente claves mal escritas.
- Para productos de alto volumen, use un grupo en lugar de la generación a demanda para garantizar que las claves se entreguen de inmediato en el momento del pago.
- Establezca **Caducar en** en grupos de claves estacionales o con fecha límite para que las claves antiguas no utilizadas se invaliden automáticamente.
- Siempre pruebe la conexión del proveedor después de la configuración y después de cualquier cambio en las credenciales — una conexión rota significa que los clientes no reciben sus claves.
- Si usa sincronización bidireccional, configure la URL del webhook de su proveedor para que apunte al punto final de webhook de licencias de su tienda.