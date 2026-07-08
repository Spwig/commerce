---
title: Tarjetas regalo de múltiples monedas
---

Si vende a clientes en múltiples países, puede emitir tarjetas regalo en monedas específicas. Por ejemplo, un cliente de Nueva Zelanda puede comprar una tarjeta regalo de $50 NZD y el destinatario la canjea en NZD — el valor nominal permanece igual independientemente de las fluctuaciones de las tasas de cambio.

Esta función requiere que la multi-moneda esté habilitada con al menos un proveedor de tasas de cambio configurado.

## Cómo funciona

Cuando establece una **Moneda de Tarjeta Regalo** en un producto de tarjeta regalo, el sistema convierte el precio del producto en la moneda objetivo en el momento de la compra utilizando la tasa de cambio actual. La tarjeta regalo resultante se denomina en esa moneda y solo puede canjearse por clientes que estén comprando en la misma moneda.

| Paso | ¿Qué ocurre? |
|------|-------------|
| **Configuración del producto** | Establece el precio del producto de tarjeta regalo en su moneda base y elige una moneda objetivo (por ejemplo, NZD) |
| **Compra** | Un cliente compra la tarjeta regalo. El precio base se convierte en NZD utilizando la tasa de cambio actual |
| **Tarjeta regalo creada** | La tarjeta regalo se emite con su valor en NZD (por ejemplo, NZ$78.50) |
| **Canje** | El destinatario aplica el código en la caja de pago mientras compra en NZD. Se deduce el saldo en NZD |

## Requisitos previos

Antes de configurar tarjetas regalo de múltiples monedas, asegúrese de tener:

1. **Multi-moneda habilitada** — Vaya a **Configuración > Configuración del almacén** y habilite el soporte de multi-moneda
2. **Monedas admitidas configuradas** — Añada las monedas que desea ofrecer (por ejemplo, NZD, SGD, EUR)
3. **Proveedor de tasas de cambio conectado** — Vaya a **Configuración > Tasas de cambio** y configure un proveedor para que las tasas en vivo estén disponibles

## Configuración de un producto de tarjeta regalo de múltiples monedas

### Paso 1: Crear o editar un producto de tarjeta regalo

1. Navegue a **Productos > Todos los Productos**
2. Haga clic en **+ Añadir Producto** o abra un producto de tarjeta regalo existente
3. Establezca **Tipo de Producto** en **Tarjeta Regalo**

### Paso 2: Establecer la moneda de la tarjeta regalo

1. Haga clic en la pestaña **Tarjeta Regalo**
2. Configure sus ajustes de denominación como de costumbre (cantidades fijas, cantidades personalizadas o ambas)
3. En la parte inferior de la pestaña Tarjeta Regalo, encuentre el menú desplegable **Moneda de Tarjeta Regalo**
4. Seleccione la moneda objetivo (por ejemplo, **NZD - Dólar de Nueva Zelanda**)
5. Guarde el producto

El menú desplegable muestra todas las monedas habilitadas en la configuración de su tienda. Seleccionar **Moneda base de la tienda (por defecto)** significa que las tarjetas regalo se emitirán en su moneda base — este es el comportamiento estándar.

### Paso 3: Establecer el precio

Establezca el precio del producto en su moneda base como lo haría normalmente. Cuando un cliente compre esta tarjeta regalo, el precio se convertirá automáticamente a la moneda objetivo utilizando la tasa de cambio actual.

**Ejemplo:** Su moneda base es USD. Crea un producto de tarjeta regalo con un precio de $50 USD y la moneda de la tarjeta regalo establecida en NZD. Si la tasa de cambio es 1 USD = 1.57 NZD, la tarjeta regalo resultante tendrá un valor de NZ$78.50.

## Coincidencia de monedas y canje

Las tarjetas regalo de múltiples monedas utilizan **canje en la misma moneda** — la moneda activa de compra del cliente debe coincidir con la moneda de la tarjeta regalo.

### Experiencia del cliente

- Un cliente que compra en **NZD** puede aplicar una tarjeta regalo en NZD en el momento del pago
- Un cliente que compra en **USD** no puede aplicar una tarjeta regalo en NZD — verán un mensaje explicando la discrepancia de monedas
- Los clientes pueden cambiar su moneda de compra utilizando el selector de monedas en su tienda en línea antes de aplicar la tarjeta regalo

### Cómo funciona el saldo

El saldo de la tarjeta regalo siempre se rastrea en su moneda nativa:

- Una tarjeta regalo de NZ$78.50 comienza con un saldo de NZ$78.50
- Si un cliente realiza una compra de NZ$30, el saldo restante es NZ$48.50
- El saldo no fluctúa con las tasas de cambio — el valor nominal es fijo

Cuando se aplica la tarjeta regalo en el momento del pago, el sistema convierte el descuento a su moneda base internamente para los cálculos del pedido, pero el saldo de la tarjeta regalo siempre se deduce en su moneda nativa.

## Gestionar tarjetas regalo de múltiples monedas

Navegue a **Productos > Tarjetas Regalo** para ver todas las tarjetas regalo emitidas. Las tarjetas regalo de múltiples monedas se muestran con su moneda nativa:

- **Saldo** se muestra en la moneda de la tarjeta regalo (por ejemplo, NZ$48.50)
- **Transacciones** registran montos en la moneda de la tarjeta regalo
- **Valor inicial** muestra el monto convertido en el momento de la compra

### Ver detalles de la tasa de cambio

Cada transacción de tarjeta regalo registra la tasa de cambio utilizada en el momento de la transacción. Esto proporciona un registro de auditoría completo para fines contables.

## Ejemplos

### Ejemplo 1: Tarjeta regalo regional para Nueva Zelanda

**Escenario:** Opera desde EE. UU. pero tienes clientes en Nueva Zelanda. Quieres vender tarjetas regalo en moneda NZD.

| Configuración | Valor |
|---------|-------|
| Nombre del producto | Tarjeta Regalo de NZ |
| Tipo de producto | Tarjeta Regalo |
| Precio | $50.00 (USD — su moneda base) |
| Tipo de denominación | Denominaciones Fijas |
| Denominaciones fijas | 25, 50, 100, 200 |
| Moneda de la tarjeta regalo | NZD - Dólar de Nueva Zelanda |
| Vencimiento | 365 días |

Cuando un cliente selecciona la denominación de $50:
- El sistema convierte $50 USD a NZD utilizando la tasa actual
- Se crea una tarjeta regalo con el equivalente en NZD (por ejemplo, NZ$78.50)
- El destinatario puede canjearla mientras compra en NZD

### Ejemplo 2: Tarjetas regalo en múltiples monedas

**Escenario:** Vende a clientes en Singapur, Australia y el Reino Unido. Crea tres productos de tarjeta regalo:

1. **Tarjeta Regalo de SG** — Moneda de la tarjeta regalo: SGD
2. **Tarjeta Regalo de AU** — Moneda de la tarjeta regalo: AUD
3. **Tarjeta Regalo de UK** — Moneda de la tarjeta regalo: GBP

Cada producto convierte su precio base en la moneda objetivo en el momento de la compra. Los clientes en cada región pueden canjear la tarjeta regalo en su moneda local.

### Ejemplo 3: Oferta de tarjetas regalo mixta

**Escenario:** Quiere ofrecer tanto tarjetas regalo en moneda base como tarjetas regalo regionales.

- **Tarjeta Regalo de Tienda** — Moneda de la tarjeta regalo: *Moneda base de la tienda (por defecto)* — canjear en su moneda base
- **Tarjeta Regalo de NZ** — Moneda de la tarjeta regalo: NZD — canjear solo en NZD

Ambos productos pueden coexistir en su catálogo. Los clientes ven en qué moneda está denominada una tarjeta regalo cuando consultan el saldo.

## Consejos

- Comience con una moneda regional y pruebe el flujo completo (compra, entrega, canje) antes de agregar más monedas.
- La tasa de cambio en el momento de la compra determina el valor de la tarjeta regalo. Si las tasas cambian significativamente, el valor de la tarjeta regalo permanece fijo — esto protege tanto a usted como a sus clientes.
- Haga clara la moneda en el nombre del producto (por ejemplo, "Tarjeta Regalo de NZ" o "Tarjeta Regalo (NZD)") para que los clientes sepan qué están comprando.
- Las tarjetas regalo sin una moneda establecida continúan funcionando exactamente como antes en su moneda base — los productos existentes no se ven afectados.
- Supervise su proveedor de tasas de cambio para asegurarse de que las tasas estén actualizadas. Tasas antiguas podrían llevar a tarjetas regalo sobrevaloradas o subvaloradas.
- Considere cuidadosamente sus denominaciones. Una denominación de $25 USD se convierte aproximadamente en NZ$39 — las denominaciones redondas en la moneda objetivo pueden verse mejor. Puede crear productos separados con denominaciones que sean números redondos en la moneda objetivo.