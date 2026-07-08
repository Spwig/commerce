---
title: Cuentas de Proveedores de Envío
---

Las cuentas de proveedores de envío conectan tu tienda con las APIs de transportistas (FedEx, UPS, DHL) para el cálculo de tarifas en tiempo real y la compra automática de etiquetas. Cada cuenta almacena credenciales de API encriptadas, monitorea la salud de la conexión y se vincula a métodos de envío en tiempo real. Los proveedores obtienen tarifas en vivo en el momento del pago basadas en las dimensiones del paquete, peso, origen y destino — eliminando la necesidad de mantener tablas de tarifas manuales y asegurando precios precisos del transportista.

Utiliza cuentas de proveedores cuando necesites tarifas de envío calculadas por el transportista o generación automática de etiquetas en lugar de la creación manual de envíos.

## Proveedores de Envío Soportados

Spwig soporta a los principales transportistas mediante componentes de proveedor instalables:

### FedEx

**Servicios**: Tierra, Expreso, Internacional
**API**: FedEx Web Services
**Funciones**: Tarifas en tiempo real, compra de etiquetas, seguimiento, documentos aduaneros internacionales

### UPS

**Servicios**: Tierra, Aéreo, Mundial
**API**: UPS Developer API
**Funciones**: Tarifas en tiempo real, generación de etiquetas, seguimiento, validación de direcciones

### DHL

**Servicios**: Expreso, eCommerce, Internacional
**API**: DHL Express API
**Funciones**: Tarifas internacionales, documentos aduaneros, seguimiento

### Proveedores Adicionales

Instale desde el mercado de componentes según sea necesario (USPS, Canada Post, Australia Post, etc.)

---

## Configuración de Cuentas de Proveedor

Cada cuenta de proveedor requiere:

### Información Básica

- **Nombre de Visualización**: Cómo aparece la cuenta en el administrador (ej. "Cuenta de Producción de FedEx")
- **Proveedor**: Seleccione el componente de proveedor instalado desde el menú desplegable
- **Activo**: Conmutador para habilitar/deshabilitar sin eliminar las credenciales
- **Es Predeterminado**: Establezca como cuenta predeterminada para este proveedor (solo una predeterminada por proveedor)

### Credenciales de API (Encriptadas)

**Varían según el proveedor**, normalmente incluyen:

**FedEx**:
- Número de Cuenta
- Número de Medidor
- Clave de API
- Secreto de API

**UPS**:
- Número de Licencia de Acceso
- ID de Usuario
- Contraseña
- Número de Cuenta

**DHL**:
- ID de Sitio
- Contraseña
- Número de Cuenta

**Todas las credenciales están encriptadas en reposo** y solo se desencriptan al realizar llamadas a la API.

### Dirección de Origen

- **Dirección de Envío por Defecto**: Dirección del almacén/origen para el cálculo de tarifas
- Algunos proveedores requieren una configuración específica de origen en su panel de control

### Configuración

Opciones específicas del proveedor (varían según el transportista):

- **Modo de Prueba**: Use los puntos finales de API de prueba/sandbox del transportista
- **Tarifas Negociadas**: Use sus tarifas negociadas con el transportista (si están disponibles)
- **Incluir Seguro**: Cotizar automáticamente el seguro en las tarifas
- **Recargo Residencial**: Aplicar tarifas de entrega residencial
- **Firma Requerida**: Requisitos de firma por defecto

---

## Crear una Cuenta de Proveedor

**Proceso de Configuración en 6 Pasos**:

**Paso 1: Obtener Acceso a la API del Transportista**
1. Cree una cuenta con el transportista (FedEx.com, UPS.com, DHL.com)
2. Solicite acceso a la API/Desarrollador
3. Complete el proceso de incorporación de la API del transportista (puede tomar 1-3 días hábiles)
4. Reciba las credenciales de la API por correo electrónico o a través del portal del desarrollador

**Paso 2: Instalar el Componente del Proveedor** (si no está preinstalado)
1. Vaya a Configuración > Componentes > Mercado
2. Busque el nombre del transportista (ej. "FedEx")
3. Instale el componente del proveedor de envío
4. Espere a que se complete la instalación

**Paso 3: Crear una Cuenta de Proveedor en Spwig**
1. Navegue a Configuración > Envío > Cuentas de Proveedor
2. Haga clic en "Añadir Cuenta de Proveedor"
3. Seleccione el proveedor desde el menú desplegable
4. Ingrese el nombre de visualización

**Paso 4: Ingresar Credenciales de API**
1. Rellene los campos de credenciales (varían según el proveedor)
2. Las credenciales se encriptan automáticamente al guardar
3. Opcional: Active el modo de prueba para pruebas iniciales

**Paso 5: Probar la Conexión**
1. Haga clic en el botón "Probar Conexión"
2. El sistema intenta realizar una llamada a la API del transportista
3. Verifique que aparezca el estado "Conectado"
4. Revise la marca de tiempo last_tested_at

**Paso 6: Vincular a un Método de Envío**
1. Cree o edite un método de envío (Configuración > Carrito > Métodos de Envío)
2. Establezca method_type = "En Tiempo Real"
3. Seleccione la cuenta del proveedor desde el menú desplegable
4. Guarde el método

---

## Monitoreo del Estado de la Conexión

Las cuentas de proveedores rastrean la salud de la conexión:

### Valores de Estado

**Desconocido** (gris): Nunca probado o aún no conectado

**Conectado** (verde): Última llamada a la API exitosa, credenciales válidas

**Error** (rojo): Última llamada a la API fallida, credenciales pueden ser inválidas

### Última Prueba

- **Marca de Tiempo**: Cuando se verificó la conexión por última vez
- **Actualización Automática**: Cada vez que se use el proveedor (obtención de tarifas, compra de etiquetas)
- **Prueba Manual**: Haga clic en el botón "Probar Conexión" en cualquier momento

### Solución de Problemas con Conexiones Fallidas

**Causas Comunes**:
- Credenciales de API incorrectas (error de escritura, copiadas con espacio adicional)
- Llave de API del transportista caducada o revocada
- Modo de prueba habilitado pero usando credenciales de producción (o viceversa)
- Dirección IP no blanqueada con el transportista
- Tiempo de inactividad de la API del transportista

**Pasos de Solución**:
1. Verifique que las credenciales coincidan exactamente con el panel de control del transportista
2. Revise que la configuración de modo de prueba coincida con el tipo de credencial
3. Revise la página de estado de la API del transportista para interrupciones
4. Póngase en contacto con el soporte del transportista para verificar la cuenta

---

## Flujo de Trabajo de Búsqueda de Tarifas

Cómo funcionan las tarifas en tiempo real en el momento del pago:

**1. Cliente Ingresa la Dirección**
- Se ingresa la dirección de envío
- El carrito calcula el peso total + dimensiones

**2. Sistema Prepara la Solicitud de Tarifa**
- Obtiene las credenciales de la cuenta del proveedor (descifradas)
- Calcula las dimensiones del paquete a partir de los artículos del carrito (usa paquetes de envío si se definen)
- Prepara la solicitud de API con origen, destino y paquetes

**3. API del Proveedor Llamada**
- La solicitud se envía a la API del transportista con las credenciales de autenticación
- El transportista calcula la tarifa basada en la zona, peso y dimensiones
- La respuesta incluye opciones de servicio (Tierra, Expreso, etc.)

**4. Tarifas Mostradas**
- El sistema analiza la respuesta del transportista
- Normaliza a un formato estándar
- Se aplica un margen de beneficio (si se configura)
- Las tarifas se muestran al cliente en el momento del pago

**5. Cliente Selecciona el Servicio**
- El cliente elige la opción preferida
- La tarifa seleccionada se guarda en el pedido

**Ejemplo de Flujo de API**:
```
Solicitud a la API de FedEx:
{
  "origin": {"postal_code": "90210", "country": "US"},
  "destination": {"postal_code": "10001", "country": "US"},
  "parcels": [{
    "weight": 2500,  // gramos
    "dimensions": {"length": 30, "width": 20, "height": 15}  // cm
  }]
}

Respuesta de FedEx:
[
  {"service": "FEDEX_GROUND", "rate": 12.50, "delivery_days": 5},
  {"service": "FEDEX_EXPRESS", "rate": 28.75, "delivery_days": 2}
]
```

---

## Compra de Etiqueta (Opcional)

Si el proveedor admite la generación de etiquetas:

**Flujo de Trabajo**:
1. El cliente completa el pedido
2. El comerciante crea el envío (Pedidos > Detalle del Pedido > Crear Envío)
3. Seleccione la cuenta del proveedor + servicio
4. El sistema llama a la API de etiquetas del proveedor
5. Se genera el PDF de la etiqueta y se adjunta al envío
6. El número de seguimiento se completa automáticamente
7. La etiqueta está lista para imprimir

**Beneficios**:
- No es necesario iniciar sesión en el sitio web del transportista manualmente
- El seguimiento se sincroniza automáticamente
- Formularios aduaneros generados automáticamente (internacionales)
- Posibilidad de generar etiquetas en lotes

---

## Markup de Tarifas

Añade un margen de beneficio a las tarifas del transportista:

**Configuración** (en el método de envío, no en la cuenta del proveedor):
- **Tipo de Markup**: Porcentaje o Fijo
- **Monto de Markup**: ej. 15% o $2.50

**Ejemplo**:
```
Tarifa del Transportista: $12.50
Markup: 15%
Cliente Paga: $14.38

O

Tarifa del Transportista: $12.50
Markup: $2.50 (fijo)
Cliente Paga: $15.00
```

**Casos de Uso**:
- Cubrir costos de empaque/manejo
- Añadir margen de beneficio al envío
- Compensar tarifas de tarjetas de crédito en envíos

---

## Cuentas de Proveedor Múltiples

Puedes crear múltiples cuentas para el mismo proveedor:

**Casos de Uso**:
1. **Prueba vs Producción**
   - Cuenta de Prueba: Credenciales de sandbox del transportista
   - Cuenta de Producción: Credenciales en vivo

2. **Múltiples Almacenes**
   - Cuenta del Almacén A: Origen = Los Ángeles
   - Cuenta del Almacén B: Origen = Nueva York

3. **Diferentes Tarifas Negociadas**
   - Cuenta A: Tarifas estándar
   - Cuenta B: Tarifas de descuento por volumen

**Cada cuenta puede vincularse a diferentes métodos de envío** para una configuración flexible.

---

## Consejos

- **Pruebe en sandbox primero** - Use credenciales de prueba del transportista antes de ir en vivo
- **Monitorea el estado de la conexión** - Revise regularmente el panel de control para estados de error
- **Defina paquetes de envío** - Dimensiones precisas mejoran las cotizaciones de tarifas
- **Use tarifas negociadas** - Actívelas si tiene descuentos por volumen con el transportista
- **Establezca un origen realista** - Use la dirección real de envío para zonas precisas
- **Mantenga las credenciales seguras** - Nunca comparta claves de API, rote periódicamente
- **Tenga un método de respaldo** - Mantenga un método de tarifa plana activo si falla la API del transportista
- **Monitorea los límites de la API del transportista** - Algunos transportistas limitan las llamadas a la API por día
- **Actualice las credenciales de inmediato** - Cuando el transportista rote las claves, actualícelas inmediatamente
- **Use nombres descriptivos** - "Cuenta de FedEx en Los Ángeles" es mejor que "FedEx 1"