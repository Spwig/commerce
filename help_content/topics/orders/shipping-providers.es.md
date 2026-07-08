---
title: Proveedores de Envío
---

Los proveedores de envío conectan tu tienda con las API de los transportistas para obtener tarifas de envío en tiempo real, generación de etiquetas y seguimiento de paquetes. Spwig admite los principales transportistas a nivel mundial y también permite configurar tablas de tarifas manuales para transportistas sin integración API.

![Shipping providers](/static/core/admin/img/help/shipping-providers/provider-list.webp)

## Transportistas Disponibles

| Transportista | Regiones | Características Principales |
|---------------|----------|----------------------------|
| **FedEx** | Global | Tarifas en tiempo real, impresión de etiquetas, seguimiento, multipaquete |
| **UPS** | Global | Tarifas en tiempo real, impresión de etiquetas, seguimiento, validación de direcciones |
| **USPS** | Estados Unidos | Tarifas nacionales e internacionales, seguimiento |
| **NinjaVan** | Sudeste Asiático | Entrega de última milla, soporte de contra reembolso |
| **Canada Post** | Canadá | Nacional e internacional, tarifas de paquetes y cartas |
| **Australia Post** | Australia | Nacional e internacional, paquetes y express |

## Conectar un Transportista

Navega a **Configuración > Proveedores de Envío** y haz clic en **Conectar Proveedor** para iniciar el asistente de configuración.

### Paso 1: Seleccionar Proveedor
Elige entre los transportistas disponibles. Cada tarjeta muestra las regiones y funcionalidades admitidas por el transportista.

### Paso 2: Instrucciones de Configuración
Revisa la guía de configuración específica del transportista:
- Cómo crear una cuenta de desarrollador/empresa con el transportista
- Dónde encontrar tus credenciales de API
- Configuraciones de cuenta requeridas (p. ej., número de remitente, número de medidor)

### Paso 3: Introducir Credenciales
Introduce las credenciales de API de tu cuenta de transportista. Los campos requeridos varían según el transportista:
- **Clave API / Secreto** — Credenciales de autenticación
- **Número de Cuenta** — Tu número de cuenta o de remitente del transportista
- **Número de Medidor** — Requerido por algunos transportistas (p. ej., FedEx)
- **Modo Sandbox** — Actívalo para probar con la API de pruebas del transportista antes de pasar a producción

### Paso 4: Probar Conexión
Haz clic en **Probar Conexión** para verificar tus credenciales. El asistente confirma:
- La autenticación de la API es exitosa
- Los permisos de la cuenta son válidos
- Las consultas de tarifas devuelven resultados esperados

### Paso 5: Configurar y Guardar
Finaliza la configuración:
- **Activo** — Activar o desactivar el transportista
- **Nombre para Mostrar** — El nombre que se muestra a los clientes en el proceso de compra
- **Dirección de Origen** — La dirección del almacén o centro de distribución para el cálculo de tarifas

## Zonas de Envío

Las zonas de envío definen áreas geográficas para el cálculo de tarifas. Navega a **Configuración > Zonas de Envío** para gestionarlas.

### Crear una Zona
1. Haz clic en **+ Añadir Zona**
2. Dale un nombre a la zona (p. ej., "Nacional", "Europa", "Asia Pacífico")
3. Define la cobertura de la zona usando una o más de:
   - **Países** — Selecciona países específicos
   - **Estados/Provincias** — Limita a regiones específicas dentro de un país
   - **Patrones de Código Postal** — Coincide códigos postales usando patrones (p. ej., "90*" para el área de Los Ángeles)
4. Establece la **Prioridad** — Cuando las zonas se superponen, se usa la zona de mayor prioridad

### Coincidencia de Zonas
Cuando un cliente introduce su dirección de envío en el proceso de compra, el sistema:
1. Verifica primero los patrones de código postal (más específico)
2. Luego las coincidencias de estado/provincia
3. Luego las coincidencias de país
4. Usa la zona coincidente de mayor prioridad

## Reglas de Envío

Las reglas de envío aplican modificadores condicionales a las tarifas de envío. Navega a **Configuración > Reglas de Envío** para configurarlas.

### Tipos de Reglas

| Tipo de Regla | Descripción |
|---------------|-------------|
| **Descuento %** | Reduce la tarifa de envío en un porcentaje |
| **Descuento Fijo** | Reduce la tarifa de envío en una cantidad fija |
| **Establecer Costo** | Reemplaza la tarifa con una cantidad específica |
| **Envío Gratuito** | Establece el costo de envío en cero |
| **Recargo %** | Añade un recargo porcentual a la tarifa |
| **Recargo Fijo** | Añade un recargo fijo a la tarifa |

### Condiciones
Cada regla puede tener una o más condiciones que deben cumplirse:

| Condición | Ejemplo |
|-----------|---------|
| **Valor del Carrito** | Envío gratuito en pedidos superiores a $100 |
| **Peso Total** | Recargo para pedidos de más de 30 kg |
| **Cantidad de Artículos** | Descuento para pedidos con más de 5 artículos |
| **Zona de Envío** | Aplicar regla solo a envíos nacionales |
| **Método de Envío** | Aplicar a métodos específicos del transportista |
| **Productos** | Tarifas especiales para productos específicos |
| **Grupo de Clientes** | Los clientes VIP obtienen envío gratuito |
| **Rango de Fechas** | Promociones de envío en temporada de fiestas |

### Prioridad de Reglas
- Las reglas se evalúan en orden de prioridad (el número más bajo primero)
- **Detener Reglas Adicionales** — Cuando está activado, si esta regla coincide, no se verifican más reglas
- Múltiples reglas pueden acumularse (p. ej., una regla de descuento del 10% más una regla de umbral de envío gratuito)

## Tablas de Tarifas

Las tablas de tarifas proporcionan precios escalonados basados en atributos del pedido. Navega a **Configuración > Tablas de Tarifas de Envío** para configurarlas.

### Tipos de Tablas
Crea niveles de tarifa basados en:
- **Peso** — Niveles de precio por peso total del pedido (p. ej., 0-1 kg = $5, 1-5 kg = $10)
- **Valor del Pedido** — Niveles de precio por subtotal del carrito
- **Cantidad** — Niveles de precio por número de artículos

### Crear una Tabla de Tarifas
1. Haz clic en **+ Añadir Tabla de Tarifas**
2. Nombra la tabla y selecciona el tipo de nivel
3. Añade niveles con rangos mínimo/máximo y precios
4. Asigna la tabla de tarifas a una zona de envío

Las tablas de tarifas son útiles cuando no utilizas tarifas de API del transportista y deseas definir tu propia estructura de precios.

## Paquetes de Envío

Define tamaños de empaque estándar para cálculos de tarifas precisos. Navega a **Configuración > Paquetes de Envío**.

Para cada tipo de paquete, establece:
- **Nombre** — Descripción (p. ej., "Caja Pequeña", "Tarifa Plana Grande")
- **Dimensiones** — Largo, ancho, alto
- **Peso Máximo** — Peso máximo que puede contener el paquete
- **Predeterminado** — Usar este paquete cuando no se asigna un empaque específico

Los transportistas utilizan las dimensiones del paquete para cálculos de peso dimensional, lo que puede afectar las tarifas de envío.

## Transportistas Manuales (Preajustes de Transportista)

Para transportistas sin integración API, crea preajustes de transportista manuales:
1. Navega a **Configuración > Preajustes de Transportista**
2. Haz clic en **+ Añadir Preajuste**
3. Configura:
   - **Nombre del Transportista** — Nombre para mostrar en el proceso de compra
   - **Plantilla de URL de Seguimiento** — Patrón de URL con un marcador `{tracking_number}` (p. ej., `https://track.transportista.com/?id={tracking_number}`)
   - **Entrega Estimada** — Rango de tiempo de entrega para mostrar a los clientes
4. Combina con una tabla de tarifas para los precios

Los transportistas manuales proporcionan enlaces de seguimiento y estimaciones de entrega sin integración API en tiempo real.

## Envío Multi-Almacén

Si tienes múltiples almacenes, el envío puede calcularse desde diferentes orígenes:
- **Almacén por País** — Asigna almacenes a países específicos para distancias de envío más cortas
- **Cadena de Respaldo** — Define qué almacén envía cuando el almacén principal no tiene stock
- **Asignación por Producto** — Algunos productos pueden enviarse solo desde almacenes específicos

El sistema selecciona automáticamente el mejor almacén según la ubicación del cliente y la disponibilidad del producto.

## Consejos

- Conecta las API de los transportistas para obtener **tarifas en tiempo real** siempre que sea posible — son más precisas que las tablas de tarifas planas y se ajustan según peso, dimensiones y destino.
- Crea una zona de envío **"Resto del Mundo"** como opción general para países no cubiertos por zonas específicas.
- Usa el tipo de regla **Envío Gratuito** con una condición de valor del carrito como incentivo de ventas (p. ej., "Envío gratuito en pedidos superiores a $75").
- Prueba los cálculos de tarifas de envío con diferentes direcciones y contenidos del carrito antes de pasar a producción.
- Configura **Preajustes de Transportista** con plantillas de URL de seguimiento para los transportistas locales que no tengan integraciones API — los clientes seguirán recibiendo enlaces de seguimiento.
- Usa **Paquetes de Envío** para obtener precios precisos de peso dimensional de transportistas como FedEx y UPS.
