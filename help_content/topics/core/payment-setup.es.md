---
title: Configuración de pagos
---

Los proveedores de pago conectan tu tienda a pasarelas de pago para que puedas aceptar tarjetas de crédito, billeteras digitales y otros métodos de pago en el momento del pago. Spwig admite múltiples proveedores simultáneamente, ofreciendo a tus clientes opciones flexibles de pago.

![Proveedores de pago](/static/core/admin/img/help/payment-setup/payment-dashboard.webp)

## Proveedores disponibles

| Proveedor | Descripción |
|----------|-------------|
| **Stripe** | Tarjetas de crédito, Apple Pay, Google Pay y 135+ monedas |
| **PayPal** | Saldo de PayPal, tarjetas de crédito/débito y opciones de pago posterior |
| **Airwallex** | Pagos multimoneda optimizados para el comercio transfronterizo |
| **Square** | Pagos presenciales y en línea con soporte integrado de POS |
| **Revolut** | Pagos rápidos europeos con tipos de cambio competitivos |

## Conectar un proveedor

Navega a **Configuración > Proveedores de pago** y haz clic en **Conectar proveedor** para iniciar el asistente de configuración.

### Paso 1: Seleccionar proveedor

Elige entre los proveedores de pago disponibles. Cada tarjeta muestra las características y regiones compatibles con el proveedor.

### Paso 2: Instrucciones de configuración

Revisa la guía de configuración específica del proveedor. Esto incluye:
- Cómo crear una cuenta con el proveedor (si no tienes una)
- Dónde encontrar tus credenciales de API en el panel de control del proveedor
- Cualquier requisito previo (por ejemplo, verificación empresarial)

### Paso 3: Ingresar credenciales

Ingresa tus credenciales de API:
- **Clave API / Clave secreta** — Tus credenciales de autenticación del panel de control del proveedor
- **Modo de pago** — Elige cómo los clientes interactúan con el formulario de pago:

| Modo | Descripción |
|------|-------------|
| **Anfitrión** | Los clientes se redirigen a la página de pago del proveedor (por ejemplo, Stripe Checkout). Configuración más sencilla, la conformidad con PCI es manejada por el proveedor. |
| **Integrado** | El formulario de pago se incrusta directamente en tu página de pago. Experiencia sin interrupciones, pero requiere el SDK de JavaScript del proveedor. |

- **Modo de prueba / modo en vivo** — Comienza en modo de prueba para probar, luego cambia a modo en vivo cuando estés listo

### Paso 4: Probar conexión

Haz clic en **Probar conexión** para verificar que tus credenciales sean válidas. El asistente verifica:
- Autenticación de la clave API
- Permisos de cuenta
- Accesibilidad del punto final de webhook

### Paso 5: Configurar y guardar

Finaliza la configuración del proveedor:
- **Activo** — Habilitar o deshabilitar el proveedor
- **Proveedor predeterminado** — Establecer como el método de pago principal en el momento del pago
- **Nombre de visualización** — El nombre mostrado a los clientes durante el pago
- **Orden de clasificación** — Controla el orden en que aparecen los proveedores en el momento del pago (los números más bajos aparecen primero)

## Panel de pagos

Navega a **Configuración > Panel de pagos** para obtener una visión general de tu actividad de pago:

### Acciones necesarias

Las tarjetas de alerta en la parte superior resaltan problemas que requieren atención:
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

## Administrar métodos de pago

Cada proveedor admite diferentes métodos de pago. Puedes habilitar o deshabilitar métodos específicos por país:

1. Navega a la página de configuración del proveedor
2. Desplázate hasta la sección **Métodos de pago**
3. Activa o desactiva métodos individuales
4. Usa controles a nivel de país para restringir métodos a mercados específicos

Esto es útil cuando un método de pago es popular en una región pero no en otra (por ejemplo, iDEAL en los Países Bajos, Bancontact en Bélgica).

Los webhooks mantienen tu tienda sincronizada con el proveedor de pagos en tiempo real.

Manejan eventos como:
- Pago completado o fallido
- Reembolsos procesados
- Disputas y cobros retroactivos abiertos
- Renovaciones de suscripciones

### Configuración Automática

Cuando conectas un proveedor, Spwig registra automáticamente un punto final de webhook con el proveedor. La URL del webhook se muestra en la página de configuración del proveedor para referencia.

### Monitoreo de Webhooks

Cada webhook entrante se registra con:
- **Tipo de evento** (p. ej., payment_intent.succeeded)
- **Marca de tiempo** y estado de procesamiento
- **Carga útil** para depuración

Si un webhook falla al procesarse, se registra como un error para que puedas investigar.

## Usar múltiples proveedores

Puedes conectar múltiples proveedores de pago al mismo tiempo:

- **Proveedor predeterminado** — El proveedor seleccionado por defecto en el proceso de pago. Marca un proveedor como predeterminado en su configuración.
- **Orden de clasificación** — Controla el orden de visualización en el proceso de pago. Los clientes ven todos los proveedores activos y pueden elegir el que prefieran.
- **Fallo de respaldo** — Si un proveedor experimenta un tiempo de inactividad, los clientes aún pueden pagar usando un proveedor alternativo.

## Consejos

- Comienza con **Stripe** o **PayPal** — cubren el rango más amplio de métodos de pago y regiones.
- Usa el **modo de prueba/sandbox** para procesar transacciones de prueba antes de ir en vivo. Cada proveedor tiene números de tarjetas de prueba en su documentación.
- Habilita **múltiples proveedores** para que los clientes tengan una opción de pago alternativa si uno de los proveedores tiene problemas.
- Establece un **orden de clasificación bajo** para tu proveedor preferido para que aparezca primero en el proceso de pago.
- Monitorea el Panel de pago semanalmente para detectar transacciones fallidas y problemas de conexión a tiempo.
- Mantén tus credenciales de API seguras — se almacenan encriptadas en la base de datos, pero nunca deben compartirse.