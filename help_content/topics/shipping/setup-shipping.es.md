---
title: Configuración de Envíos
---

Esta guía explica cómo configurar el envío para su tienda, desde la creación de métodos de envío básicos hasta la conexión de integraciones con transportistas para obtener tarifas en tiempo real.

## Resumen de Envío

Spwig ofrece dos enfoques para el envío:

- **Métodos de Envío Manuales** — Métodos de tarifa fija que usted define (por ejemplo, "Envío Estándar — 5,99 $")
- **Integraciones con Transportistas** — Tarifas en tiempo real de proveedores como FedEx, UPS y DHL

Puede utilizar cualquiera de los dos enfoques o combinar ambos.

## Métodos de Envío

Los métodos de envío son las opciones que sus clientes ven en el proceso de pago. Navegue a **Pedidos > Envíos** en la barra lateral para gestionarlos.

![Shipping methods](/static/core/admin/img/help/setup-shipping/shipping-methods.webp)

### Crear un Método de Envío

1. Haga clic en **Agregar Método de Envío**
2. Complete los datos:
   - **Nombre** — Nombre visible para los clientes (por ejemplo, "Entrega Exprés")
   - **Descripción** — Breve descripción del servicio
   - **Precio** — Costo de envío fijo
   - **Entrega Estimada** — Estimación del tiempo de entrega (por ejemplo, "3-5 días hábiles")
3. Haga clic en **Guardar**

## Zonas de Envío

Las zonas de envío definen las regiones geográficas donde se aplican sus métodos de envío. Navegue a la sección **Zonas de Envío** para gestionarlas.

![Shipping zones](/static/core/admin/img/help/setup-shipping/shipping-zones.webp)

### Crear una Zona

1. Haga clic en **Agregar Zona de Envío**
2. Configure la zona:
   - **Nombre de la Zona** — Nombre interno (por ejemplo, "Nacional", "Europa")
   - **Países** — Seleccione qué países pertenecen a esta zona
   - **Estados/Regiones** — Opcionalmente reduzca a estados específicos
   - **Patrones de Código Postal** — Use patrones como "9*" para apuntar a áreas específicas
3. Asigne métodos de envío a esta zona
4. Haga clic en **Guardar**

### Prioridad de Zona

Cuando la dirección de un cliente coincide con múltiples zonas, la zona más específica tiene prioridad. Una zona con orientación a nivel estatal tiene precedencia sobre una zona a nivel de país.

## Integraciones con Transportistas

Conéctese con transportistas para ofrecer tarifas calculadas en tiempo real en el proceso de pago.

![Shipping carriers](/static/core/admin/img/help/setup-shipping/shipping-carriers.webp)

### Proveedores Disponibles

Explore e instale proveedores de envío desde el marketplace.

![Shipping providers](/static/core/admin/img/help/setup-shipping/shipping-providers.webp)

Los transportistas compatibles incluyen:

- **FedEx** — Terrestre, Exprés, Internacional
- **UPS** — Terrestre, 2 Días, Nocturno, Mundial
- **DHL** — Exprés, eCommerce
- **USPS** — Priority, First Class, Media Mail
- Y más disponibles a través del Marketplace

### Configurar un Transportista

1. Vaya a la página de proveedores de envío y haga clic en **Instalar** en el transportista que prefiera
2. Siga el asistente de configuración:
   - **Paso 1** — Revisar los detalles del proveedor
   - **Paso 2** — Configurar los ajustes generales
   - **Paso 3** — Introducir sus credenciales de API (número de cuenta, clave API, etc.)
   - **Paso 4** — Activar servicios específicos (Terrestre, Exprés, etc.)
   - **Paso 5** — Probar la conexión
3. Una vez conectado, las tarifas del transportista aparecen automáticamente en el proceso de pago

### Credenciales de API

Cada transportista requiere una cuenta de API:

- **FedEx** — Regístrese en el Portal de Desarrolladores de FedEx, cree una aplicación y copie su clave API y secreto
- **UPS** — Regístrese en el Kit de Desarrolladores de UPS, solicite una clave de acceso
- **DHL** — Contacte a DHL para obtener credenciales de API a través de su portal empresarial

## Reglas de Envío

Cree reglas avanzadas para controlar cuándo y cómo se ofrecen los métodos de envío.

### Reglas Comunes

- **Envío gratuito a partir de 50 $** — Establezca un mínimo de carrito para envío gratuito
- **Tarifa fija para pedidos ligeros** — Tarifa fija cuando el peso del pedido está por debajo de un umbral
- **Desactivar exprés para áreas remotas** — Ocultar opciones exprés según códigos postales
- **Recargo porcentual** — Agregar una tarifa de manejo como porcentaje de las tarifas del transportista

### Crear una Regla

1. Navegue a la sección de reglas de envío
2. Haga clic en **Agregar Regla**
3. Establezca las condiciones (total del carrito, peso, zona, etc.)
4. Defina la acción (ajustar tarifa, ocultar método, activar envío gratuito)
5. Guarde la regla

Las reglas se evalúan en orden; la primera regla que coincida se aplica.

## Envío Gratuito

### Envío Gratuito en Toda la Tienda

Active el envío gratuito globalmente en **Configuración > Ajustes de la Tienda**:

- Active **Envío Gratuito**
- Opcionalmente establezca un monto mínimo de pedido
- Elija qué regiones califican

### Envío Gratuito Promocional

Cree ofertas de envío gratuito por tiempo limitado:

1. Vaya a **Marketing > Ventas y Promociones**
2. Cree una nueva promoción
3. Establezca la condición: "Total del carrito superior a X"
4. Establezca la acción: "Envío gratuito"
5. Configure las fechas de inicio y fin

## Envío Internacional

Para pedidos internacionales, asegúrese de que sus productos tengan:

- **Código HS** — Clasificación arancelaria del Sistema Armonizado
- **País de Origen** — País de fabricación
- **Valor Aduanero** — Valor declarado para aduanas

Estos campos se encuentran en la pestaña **Inventario** de cada producto. Los transportistas utilizan esta información para generar automáticamente la documentación aduanera.

## Consejos

- Comience con métodos de envío manuales para poner su tienda en marcha rápidamente y luego agregue integraciones con transportistas.
- Cree zonas de envío primero para sus destinos más comunes.
- Siempre pruebe su configuración de envío realizando pedidos de prueba con diferentes direcciones.
- Utilice la función de recargo de tarifas para cubrir los costos de manipulación y embalaje.
- Establezca umbrales de envío gratuito para aumentar el valor promedio de los pedidos.
