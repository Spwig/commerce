---
title: Productos Digitales
---

Los productos digitales le permiten vender archivos descargables, licencias de software y otros bienes no físicos. Spwig admite productos digitales independientes, así como productos híbridos que combinan entrega física y digital.

![Proveedores de licencias](/static/core/admin/img/help/digital-products/license-providers.webp)

## Tipos de Productos Digitales

### Producto Digital Independiente

Establezca el **Tipo de Producto** como **Producto Digital** para artículos puramente digitales:
- Aplicaciones de software
- Libros electrónicos y PDFs
- Música y archivos de audio
- Arte digital y plantillas

### Productos Híbridos

Cualquier tipo de producto puede incluir entrega digital marcando **Es Producto Digital** en la pestaña de Información Básica. Esto es útil para:
- **Productos digitales variables** — Software con ediciones Básica/Profesional/Empresarial
- **Productos digitales personalizables** — Activos digitales diseñados a medida
- **Paquetes físicos + digitales** — Un libro que incluye una descarga digital

## Configurar un Producto Digital

### Paso 1: Crear el Producto

1. Navegue a **Productos > Todos los Productos** y haga clic en **+ Añadir Producto**
2. Establezca el **Tipo de Producto** como **Producto Digital** (o marque **Es Producto Digital** en otro tipo de producto)
3. Complete los detalles del producto (nombre, descripción, precio)
4. Guarde el producto

### Paso 2: Añadir Archivos Descargables

1. Vaya a la pestaña **Inventario** del producto
2. En la sección **Archivos Digitales**, suba los archivos que recibirán los clientes después de la compra
3. Para cada archivo, puede configurar:
   - **Nombre del archivo** — Nombre visible que se muestra a los clientes
   - **Límite de descargas** — Número máximo de veces que se puede descargar el archivo (0 = ilimitado)
   - **Días de expiración** — Número de días que el enlace de descarga permanece activo

### Paso 3: Configurar la Entrega de Licencias (Opcional)

Si su producto digital requiere claves de licencia:

1. Navegue a **Configuración > Gestión de Licencias**
2. Conecte un proveedor de licencias (ver más abajo)
3. En el formulario de edición del producto, asigne el proveedor de licencias

## Proveedores de Licencias

Los proveedores de licencias son servicios externos que generan y gestionan claves de licencia de software automáticamente cuando un cliente compra su producto.

### Tipos de Proveedores Disponibles

| Proveedor | Descripción |
|-----------|-------------|
| **Servidor de Licencias Integrado de Spwig** | Generación simple de claves de licencia integrada en la plataforma |
| **Keygen.sh** | API de gestión de licencias con funciones completas |
| **LicenseSpring** | Gestión de licencias empresarial |
| **Cryptlex** | Licenciamiento de software con soporte sin conexión |
| **API Personalizada** | Conecte cualquier sistema de licencias mediante REST API |

### Conectar un Proveedor de Licencias

1. Navegue a **Configuración > Gestión de Licencias**
2. Haga clic en **Conectar Proveedor**
3. Siga el asistente de configuración:
   - **Paso 1** — Seleccione el tipo de proveedor
   - **Paso 2** — Configure los ajustes generales
   - **Paso 3** — Introduzca las credenciales de la API
4. Pruebe la conexión para verificar que funciona
5. Guarde la configuración

### Tarjeta del Proveedor

Cada proveedor conectado muestra:
- **Insignias de estado** — Activo/Inactivo y estado de la conexión
- **Endpoint de la API** — La URL del servidor configurada
- **Capacidades de sincronización** — Soporte de sincronización de Pedidos, Activación y Desactivación
- **Botones de acción** — Configurar, Probar y Sincronizar Ahora

### Capacidades de Sincronización

Los proveedores de licencias pueden sincronizarse en tres eventos:

- **Pedido** — Generar automáticamente una clave de licencia cuando un cliente completa una compra
- **Activación** — Registrar cuándo un cliente activa su licencia
- **Desactivación** — Gestionar la desactivación de licencias para reembolsos o transferencias

## Experiencia del Cliente

### Después de la Compra

Cuando un cliente compra un producto digital:

1. **Confirmación del pedido** — Muestra que la entrega digital está incluida
2. **Entrega por correo electrónico** — Los enlaces de descarga y/o las claves de licencia se envían automáticamente
3. **Página de la cuenta** — Los clientes pueden acceder a sus descargas desde el panel de su cuenta
4. **Página de descarga** — Enlaces de descarga seguros y con tiempo limitado

### Seguridad de las Descargas

Las descargas de archivos digitales están protegidas por:
- Tokens de descarga únicos y con tiempo limitado
- Límites opcionales de cantidad de descargas
- Fechas de expiración después de las cuales los enlaces se desactivan
- Requisito de inicio de sesión (para clientes registrados)

## Consejos

- Establezca límites de descarga razonables (3-5 descargas) para prevenir abusos mientras permite re-descargas.
- Use días de expiración que coincidan con su período de soporte (ej., 365 días para un año de acceso).
- Pruebe el flujo completo de compra con un pedido de prueba para asegurar que los enlaces de descarga y las claves de licencia se entregan correctamente.
- Para productos de software, conecte un proveedor de licencias para automatizar la generación de claves en lugar de gestionar las claves manualmente.
- Use la función de producto híbrido cuando venda bienes físicos que incluyen extras digitales (ej., libro impreso + PDF).
