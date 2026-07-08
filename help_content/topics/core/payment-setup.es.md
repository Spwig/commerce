---
title: Configuración de pagos
---

Los proveedores de pago conectan tu tienda con pasarelas de pago para que puedas aceptar tarjetas de crédito, billeteras digitales y otros métodos de pago en el momento del pago. Spwig admite múltiples proveedores simultáneamente, brindando a tus clientes opciones de pago flexibles.

![Proveedores de pago](/static/core/admin/img/help/payment-setup/payment-dashboard.webp)

## Proveedores disponibles

| Proveedor | Descripción |
|----------|-------------|
| **Stripe** | Tarjetas de crédito, Apple Pay, Google Pay y 135+ monedas |
| **PayPal** | Saldo de PayPal, tarjetas de crédito/débito y opciones de pago posterior |
| **Airwallex** | Pagos en múltiples monedas optimizados para el comercio transfronterizo |
| **Adyen** | Pagos de nivel empresarial con 250+ métodos de pago en todo el mundo |
| **Square** | Pagos presenciales y en línea con soporte integrado de POS |
| **Revolut** | Pagos europeos rápidos con tipos de cambio competitivos |

## Conectar un proveedor

Navegue a **Configuración > Proveedores de pago** y haga clic en **Conectar proveedor** para iniciar el asistente de configuración.

### Paso 1: Seleccionar proveedor

Elija entre los proveedores de pago disponibles. Cada tarjeta muestra las características y regiones admitidas por el proveedor.

### Paso 2: Instrucciones de configuración

Revise la guía de configuración específica del proveedor. Esto incluye:
- Cómo crear una cuenta con el proveedor (si no tiene una)
- Dónde encontrar sus credenciales de API en el panel de control del proveedor
- Cualquier requisito previo (por ejemplo, verificación empresarial)

### Paso 3: Ingresar credenciales

Ingrese sus credenciales de API:
- **Clave API / Clave secreta** — Sus credenciales de autenticación del panel de control del proveedor
- **Modo de pago** — Elija cómo los clientes interactúan con el formulario de pago:

| Modo | Descripción |
|------|-------------|
| **Anfitrión** | Los clientes se redirigen a la página de pago del proveedor (por ejemplo, Stripe Checkout). Configuración más sencilla, la conformidad con PCI es manejada por el proveedor. |
| **Integrado** | El formulario de pago se incrusta directamente en su página de pago. Experiencia fluida, pero requiere el SDK de JavaScript del proveedor. |

- **Modo de prueba / modo en vivo** — Comience en modo de prueba para probar, luego cambie a modo en vivo cuando esté listo

### Paso 4: Probar conexión

Haga clic en **Probar conexión** para verificar que sus credenciales sean válidas. El asistente verifica:
- Autenticación de la clave API
- Permisos de cuenta
- Accesibilidad del punto final de webhook

### Paso 5: Configurar y guardar

Finalice la configuración del proveedor:
- **Activo** — Habilitar o deshabilitar el proveedor
- **Proveedor predeterminado** — Establecer como el método de pago principal en el momento del pago
- **Nombre de visualización** — El nombre mostrado a los clientes durante el pago
- **Orden de clasificación** — Controla el orden en que aparecen los proveedores en el momento del pago (los números más bajos aparecen primero)

## Panel de control de pagos

Navegue a **Configuración > Panel de control de pagos** para obtener una visión general de su actividad de pago:

### Acciones necesarias

Las tarjetas de alerta en la parte superior resaltan problemas que necesitan atención:
- **Transacciones fallidas** — Pagos que no pudieron procesarse
- **Capturas pendientes** — Pagos autorizados que esperan captura
- **Errores de conexión** — Proveedores con problemas de conectividad

### Análisis de ingresos

- **Gráfico de ingresos** — Desglose visual del volumen de pagos a lo largo del tiempo, agrupado por día, semana o mes
- **Métricas de rendimiento** — Ingresos totales, tasa de éxito, valor promedio de transacción y tasa de reembolso
- **Comparación de proveedores** — Tarjetas de rendimiento lado a lado para cada proveedor conectado

### Desglose de transacciones

- **Distribución de estado** — Cuentas de transacciones completadas, pendientes, fallidas y reembolsadas
- **Mezcla de métodos de pago** — Qué métodos de pago usan más los clientes (tarjetas de crédito, PayPal, billeteras digitales)

## Administración de métodos de pago

Cada proveedor admite diferentes métodos de pago. Puede habilitar o deshabilitar métodos específicos por país:

1. Navegue a la página de configuración del proveedor
2. Desplácese hasta la sección **Métodos de pago**
3. Active o desactive métodos individuales
4. Use controles a nivel de país para restringir métodos a mercados específicos

Esto es útil cuando un método de pago es popular en una región pero no en otra (por ejemplo, iDEAL en los Países Bajos, Bancontact en Bélgica).

## Webhooks

Los webhooks mantienen su tienda sincronizada con el proveedor de pago en tiempo real. Manejan eventos como:
- Pago completado o fallido
- Reembolsos procesados
- Disputas y cargos devueltos abiertos
- Renovaciones de suscripción

### Configuración automática

Cuando conecta un proveedor, Spwig registra automáticamente un punto final de webhook con el proveedor. La URL del webhook se muestra en la página de configuración del proveedor para referencia.

### Monitoreo de webhooks

Cada webhook entrante se registra con:
- **Tipo de evento** (por ejemplo, payment_intent.succeeded)
- **Marca de tiempo** y estado de procesamiento
- **Carga útil** para depuración

Si un webhook falla al procesarse, se registra como un error para que pueda investigar.

## Usando múltiples proveedores

Puede conectar múltiples proveedores de pago simultáneamente:

- **Proveedor predeterminado** — El proveedor seleccionado por defecto en el momento del pago. Marque un proveedor como predeterminado en su configuración.
- **Orden de clasificación** — Controla el orden de visualización en el momento del pago. Los clientes ven todos los proveedores activos y pueden elegir su preferido.
- **Fallo de respaldo** — Si un proveedor experimenta un tiempo de inactividad, los clientes aún pueden pagar usando un proveedor alternativo.

## Consejos

- Comience con **Stripe** o **PayPal** — cubren el rango más amplio de métodos de pago y regiones.
- Use **modo de prueba/modo de prueba** para procesar transacciones de prueba antes de ir en vivo. Cada proveedor tiene números de tarjetas de prueba en su documentación.
- Habilite **múltiples proveedores** para que los clientes tengan una opción de pago alternativa si un proveedor tiene problemas.
- Establezca un **orden de clasificación bajo** para su proveedor preferido para que aparezca primero en el momento del pago.
- Monitorea el Panel de control de pagos semanalmente para detectar transacciones fallidas y problemas de conexión temprano.
- Mantenga sus credenciales de API seguras — se almacenan encriptadas en la base de datos, pero nunca deben compartirse.

