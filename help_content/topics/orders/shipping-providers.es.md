---
title: Proveedores de Envío
---

Los proveedores de envío conectan tu tienda con las APIs de transportistas para obtener tarifas de envío en vivo, generación de etiquetas y seguimiento de paquetes. Spwig admite transportistas principales en todo el mundo y también te permite configurar tablas de tarifas manuales para transportistas sin integración de API.

![Proveedores de envío](/static/core/admin/img/help/shipping-providers/provider-list.webp)

## Proveedores Disponibles

| Proveedor | Regiones | Características Clave |
|---------|---------|-------------|
| **FedEx** | Global | Tarifas en vivo, impresión de etiquetas, seguimiento, múltiples paquetes |
| **UPS** | Global | Tarifas en vivo, impresión de etiquetas, seguimiento, validación de direcciones |
| **USPS** | Estados Unidos | Tarifas nacionales e internacionales, seguimiento |
| **NinjaVan** | Sudeste Asiático | Entrega de último milla, soporte de pago en efectivo |
| **Canada Post** | Canadá | Nacionales e internacionales, tarifas de paquetes y cartas |
| **Australia Post** | Australia | Nacionales e internacionales, paquetes y express |

## Conectar un Proveedor

Navega a **Configuración > Proveedores de Envío** y haz clic en **Conectar Proveedor** para iniciar el asistente de configuración.

### Paso 1: Seleccionar Proveedor

Elige entre los proveedores de envío disponibles. Cada tarjeta muestra las regiones y características admitidas por el proveedor.

### Paso 2: Instrucciones de Configuración

Revisa la guía de configuración específica del proveedor:
- Cómo crear una cuenta de desarrollador/empresa con el proveedor
- Dónde encontrar tus credenciales de API
- Configuraciones de cuenta requeridas (por ejemplo, número de remitente, número de medidor)

### Paso 3: Ingresar Credenciales

Ingresa las credenciales de API de tu cuenta del proveedor. Los campos requeridos varían según el proveedor:

- **Clave de API / Secreto** — Credenciales de autenticación
- **Número de Cuenta** — Tu número de cuenta o de remitente del proveedor
- **Número de Medidor** — Requerido por algunos proveedores (por ejemplo, FedEx)
- **Modo de Entorno de Prueba** — Actívalo para probar con la API de entorno de prueba del proveedor antes de ir en vivo

### Paso 4: Probar la Conexión

Haz clic en **Probar Conexión** para verificar tus credenciales. El asistente confirma:
- La autenticación de la API tiene éxito
- Las permisos de la cuenta son válidos
- Las consultas de tarifa devuelven resultados esperados

### Paso 5: Configurar y Guardar

Finaliza la configuración:
- **Activo** — Habilitar o deshabilitar el proveedor
- **Nombre de Visualización** — El nombre mostrado a los clientes en la caja de pago
- **Dirección de Origen** — La dirección del almacén o de cumplimiento para cálculos de tarifa

## Zonas de Envío

Las zonas de envío definen áreas geográficas para cálculos de tarifa. Navega a **Configuración > Zonas de Envío** para gestionarlas.

### Crear una Zona

1. Haz clic en **+ Agregar Zona**
2. Asigna un nombre a la zona (por ejemplo, "Nacional", "Europa", "Asia Pacífico")
3. Define la cobertura de la zona usando una o más de:
   - **Países** — Selecciona países específicos
   - **Estados/Provincias** — Limita a regiones específicas dentro de un país
   - **Patrones de Códigos Postales** — Coincide con códigos postales/ZIP usando patrones (por ejemplo, "90*" para el área de Los Ángeles)
4. Establece la **Prioridad** — Cuando las zonas se superponen, se usa la zona con mayor prioridad

### Coincidencia de Zonas

Cuando un cliente ingresa su dirección de envío en la caja de pago, el sistema:
1. Verifica primero los patrones de códigos postales (más específicos)
2. Luego coincidencias de estado/provincia
3. Luego coincidencias de país
4. Usa la zona con mayor prioridad coincidente

## Promociones de Envío

Las promociones de envío aplican modificadores condicionales a las tarifas de envío. Navega a **Configuración > Promociones de Envío** para configurarlas.

### Tipos de Promoción

| Tipo de Promoción | Descripción |
|-----------|-------------|
| **Descuento %** | Reduce la tarifa de envío en un porcentaje |
| **Descuento Fijo** | Reduce la tarifa de envío en una cantidad fija |
| **Sobrescribir Costo** | Sobrescribe la tarifa con una cantidad específica |
| **Envío Gratis** | Establece el costo de envío en cero |
| **Recargo %** | Añade un recargo en porcentaje a la tarifa |
| **Recargo Fijo** | Añade un recargo fijo a la tarifa |

### Condiciones

Cada promoción puede tener una o más condiciones que deben cumplirse:

| Condición | Ejemplo |
|-----------|---------|
| **Valor del carrito** | Envío gratis en pedidos superiores a $100 |
| **Peso total** | Recargo para pedidos superiores a 30 kg |
| **Cantidad de artículos** | Descuento para pedidos con 5 o más artículos |
| **Zona de envío** | Aplicar promoción solo a envíos nacionales |
| **Método de envío** | Aplicar a métodos específicos de transportista |
| **Productos** | Tarifas especiales para productos específicos |
| **Grupo de clientes** | Los clientes VIP obtienen envío gratis |
| **Rango de fechas** | Promociones de envío de temporada |

### Prioridad de promoción

- Las promociones se evalúan en orden de prioridad (el número más bajo primero)
- **Detener promociones adicionales** — Cuando está habilitado, si esta promoción coincide, no se verificarán más promociones
- Se pueden aplicar múltiples promociones (por ejemplo, una promoción de descuento del 10% más una promoción de umbral de envío gratis)

## Tablas de tarifas

Las tablas de tarifas ofrecen precios escalonados basados en atributos del pedido. Navegue a **Configuración > Tablas de tarifas de envío** para configurarlas.

### Tipos de tabla

Cree niveles de tarifas basados en:
- **Peso** — Niveles de precios según el peso total del pedido (por ejemplo, 0-1 kg = $5, 1-5 kg = $10)
- **Valor del pedido** — Niveles de precios según el subtotal del carrito
- **Cantidad** — Niveles de precios según la cantidad de artículos

### Crear una tabla de tarifas

1. Haga clic en **+ Agregar tabla de tarifas**
2. Nombre la tabla y seleccione el tipo de nivel
3. Agregue niveles con rangos mínimos/máximos y precios
4. Asigne la tabla de tarifas a una zona de envío

Las tablas de tarifas son útiles cuando no utiliza tarifas de API de transportistas y desea definir su propia estructura de precios.

## Paquetes de envío

Defina tamaños estándar de empaque para cálculos precisos de tarifas. Navegue a **Configuración > Paquetes de envío**.

Para cada tipo de paquete, establezca:
- **Nombre** — Descripción (por ejemplo, "Caja pequeña", "Gran tarifa plana")
- **Dimensiones** — Longitud, ancho, altura
- **Peso máximo** — Peso máximo que puede contener el paquete
- **Predeterminado** — Use este paquete cuando no se asigne empaque específico

Los transportistas usan las dimensiones del paquete para calcular el peso dimensional, lo cual puede afectar las tarifas de envío.

## Transportistas manuales (presets de transportista)

Para transportistas sin integración de API, cree presets de transportista manuales:

1. Navegue a **Configuración > Presets de transportista**
2. Haga clic en **+ Agregar preset**
3. Configure:
   - **Nombre del transportista** — Nombre de visualización en el proceso de pago
   - **Plantilla de URL de seguimiento** — Patrón de URL con un marcador de posición {número de seguimiento} (por ejemplo, `https://track.carrier.com/?id={tracking_number}`)
   - **Tiempo estimado de entrega** — Rango de tiempo de entrega a mostrar a los clientes
4. Asocie una tabla de tarifas para el precio

Los transportistas manuales proporcionan enlaces de seguimiento y estimaciones de entrega sin integración de API en vivo.

## Envío de múltiples almacenes

Si tiene múltiples almacenes, el envío puede calcularse desde diferentes orígenes:

- **Almacén específico por país** — Asigne almacenes a países específicos para distancias de envío más cortas
- **Cadena de respaldo** — Defina qué almacén envía cuando el almacén principal esté agotado
- **Asignación por producto** — Algunos productos solo se envían desde almacenes específicos

El sistema selecciona automáticamente el mejor almacén según la ubicación del cliente y la disponibilidad del producto.

## Consejos

- Conecte APIs de transportistas para **tarifas en vivo** siempre que sea posible — son más precisas que tablas de tarifas planas y ajustan según el peso, dimensiones y destino.
- Cree una **zona de envío "Resto del mundo"** como un contenedor para países no cubiertos por zonas específicas.
- Use el tipo de promoción **Envío gratis** con una condición de valor del carrito como incentivo de ventas (por ejemplo, "Envío gratis en pedidos superiores a $75").
- Pruebe los cálculos de tarifas de envío con diferentes direcciones y contenidos de carrito antes de lanzar.
- Configure **Presets de transportista** con plantillas de URL de seguimiento para cualquier transportista local que no tenga integraciones de API — los clientes aún obtienen enlaces de seguimiento.
- Use **Paquetes de envío** para obtener precios de peso dimensional precisos de transportistas como FedEx y UPS.