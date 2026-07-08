---
title: Programa de Afiliados
---

El programa de afiliados le permite reclutar socios que promuevan sus productos y ganen comisiones por las ventas que generen. Los afiliados comparten enlaces de referencia únicos, y Spwig rastrea automáticamente los clics, atribuye los pedidos y calcula las comisiones.

![Programas de afiliados](/static/core/admin/img/help/affiliate-program/program-list.webp)

## Cómo funciona

1. Usted crea uno o más **programas de afiliados** con tasas de comisión y reglas
2. Los afiliados **se inscriben** a través de un portal público o se agregan manualmente
3. Cada afiliado obtiene un **enlace de referencia único** con un código de seguimiento
4. Cuando un cliente hace clic en el enlace y realiza una compra, se registra una **comisión**
5. Usted revisa y aprueba las comisiones, luego procesa **pagos**

## Crear un Programa

Navegue a **Marketing > Programas de Afiliados** y haga clic en **Agregar Programa**.

### Configuración del Programa

| Configuración | Descripción |
|---------|-------------|
| **Nombre** | Nombre del programa visible para los afiliados (ej. "Programa de Socios") |
| **Tipo de Comisión** | **Porcentaje** del total del pedido o **Fijo** monto por venta |
| **Tasa de Comisión** | El porcentaje o monto fijo que ganan los afiliados |
| **Duración de la Cookie** | Cuántos días dura la cookie de seguimiento de referidos (por defecto: 30 días) |
| **Monto Mínimo de Pago** | Ganancias mínimas antes de que un afiliado pueda solicitar un pago |
| **Aprobar Automáticamente Afiliados** | Aceptar automáticamente nuevas solicitudes de afiliados, o requerir aprobación manual |
| **Estado** | Activo, pausado o cerrado |

### Tipos de Comisión

- **Porcentaje** — Los afiliados ganan un porcentaje del subtotal de cada pedido referido (ej. 10% de un pedido de $100 = $10 de comisión)
- **Fijo** — Los afiliados ganan un monto fijo por venta, independientemente del valor del pedido (ej. $5 por venta)

## Gestionar Afiliados

Navegue a **Marketing > Afiliados** para ver y gestionar cuentas de afiliados.

### Detalles del Afiliado

Cada afiliado tiene:
- **Código de Afiliado** — Un código único usado en los enlaces de referencia (generado automáticamente o personalizado)
- **Enlace de Referencia** — La URL completa de seguimiento que el afiliado comparte (ej., `yourstore.com/?ref=CODE`)
- **Estado** — Pendiente, aprobado o rechazado
- **Método de Pago** — Cómo el afiliado recibe los pagos (PayPal o transferencia bancaria)
- **Miembro del Programa** — A qué programas pertenece el afiliado

### Agregar Afiliados Manualmente

1. Haga clic en **Agregar Afiliado**
2. Seleccione una cuenta de cliente existente o cree una nueva
3. Asigne al afiliado a uno o más programas
4. Establezca el código de afiliado (o deje en blanco para generar automáticamente)

### Portal del Afiliado

Los afiliados acceden a un portal público donde pueden:
- Ver su panel de control con estadísticas de ganancias y clics
- Copiar sus enlaces de referencia
- Rastrear el historial de comisiones
- Solicitar pagos

La URL del portal está disponible automáticamente en `/affiliate/` en su tienda.

## Seguimiento y Comisiones

### Cómo funciona el seguimiento

1. Un cliente hace clic en el enlace de referencia de un afiliado
2. Se establece una cookie de seguimiento en el navegador del cliente (duración configurada de la cookie)
3. Si el cliente coloca un pedido dentro del período de vida de la cookie, el pedido se atribuye al afiliado
4. Se crea un registro de comisión con el estado **Pendiente**

### Estados de Comisión

| Estado | Descripción |
|--------|-------------|
| **Pendiente** | Comisión registrada, esperando revisión |
| **Aprobada** | Verificada y lista para pago |
| **Rechazada** | Comisión denegada (ej. pedido fraudulento o artículo devuelto) |
| **Pagada** | Comisión incluida en un pago completado |

### Revisar Comisiones

Navegue a **Marketing > Comisiones** para revisar comisiones pendientes:

1. Revise los detalles del pedido para verificar que la venta sea legítima
2. Haga clic en **Aprobar** para confirmar, o en **Rechazar** con una razón
3. Las comisiones aprobadas se acumulan hacia el saldo de pago del afiliado

## Pagos

Cuando el saldo de comisión aprobado de un afiliado alcanza el umbral mínimo de pago, puede procesar un pago.

### Procesar Pagos

1. Navegue a **Marketing > Pagos**
2. Seleccione afiliados con saldos disponibles
3. Elija el método de pago:
   - **PayPal** — Envíe fondos directamente al correo electrónico de PayPal del afiliado
   - **Transferencia Bancaria** — Registre una transferencia bancaria manual
4. Confirme y procese el pago
5. El estado del pago se actualiza a **Completado** y las comisiones se marcan como **Pagadas**

### Proveedores de Pagos

Spwig se integra con proveedores de pago para pagos automatizados:
- **PayPal** — Pagos masivos automatizados a través de la API de PayPal
- **Airwallex** — Pagos internacionales con tasas de cambio competitivas
- **Manual** — Registre pagos procesados fuera de Spwig

## Enlaces de Referencia

Cada enlace de referencia de un afiliado sigue este patrón:

```
https://yourstore.com/?ref=AFFILIATE_CODE
```

Los afiliados también pueden crear enlaces a productos o categorías específicos:

```
https://yourstore.com/products/shoe-name/?ref=AFFILIATE_CODE
```

El parámetro `ref` funciona en cualquier página — la cookie de seguimiento se establece independientemente de la página de llegada.

## Análisis del Programa

El panel de control del programa de afiliados muestra:
- **Total de Clics** — Cuántas veces se han hecho clics en los enlaces de referencia
- **Total de Pedidos** — Pedidos atribuidos a afiliados
- **Total de Comisiones** — Suma de todas las comisiones (pendientes, aprobadas y pagadas)
- **Afiliados Activos** — Número de afiliados aprobados que actualmente generan referidos

## Consejos

- Comience con una **comisión basada en porcentaje** (5–15%) — se escala naturalmente con el valor del pedido y es fácil de entender para los afiliados.
- Establezca una **duración de cookie de 30 días** como punto de partida — esto da a los clientes tiempo para regresar y completar su compra, aún atribuyendo la venta al afiliado.
- Active **aprobación automática** para programas públicos para reducir la fricción, o use aprobación manual para programas por invitación donde desee verificar cada afiliado.
- Establezca un **monto mínimo de pago** razonable (ej. $25–$50) para evitar procesar muchas transacciones pequeñas.
- Personalice el **portal del afiliado** para que coincida con su marca — los afiliados son más propensos a promover su tienda cuando la experiencia se sienta profesional.
- Supervise regularmente las comisiones en busca de **patrones fraudulentos** como referencias a sí mismos, tasas de devolución inusualmente altas o volúmenes de clics sospechosos.