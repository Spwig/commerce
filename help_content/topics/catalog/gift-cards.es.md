---
title: Tarjetas regalo
---

Las tarjetas regalo son un crédito para la tienda que los clientes pueden comprar para alguien más — o para sí mismos — y se entregan por correo electrónico como un código único de redención. También puedes emitir una tarjeta regalo directamente desde el administrador sin una compra del cliente.

La venta de tarjetas regalo está activa. Cuando un cliente compra una, la tarjeta se crea y se envía por correo electrónico automáticamente una vez que se confirme su pago — nunca antes, por lo que nadie recibe un código por un pago que luego falle.

Algunas cosas importantes que debes saber antes de habilitar un producto de tarjeta regalo:

- **Una tarjeta regalo es dinero, no un descuento.** Se resta del total final después de impuestos y envío, y no reduce el impuesto que debes pagar. Esto es lo opuesto a un vale, que reduce el precio de los productos.
- **Las tarjetas son de un solo tipo de moneda.** Una tarjeta comprada en euros solo puede usarse en un pedido en euros. Si vendes en varias monedas, crea un producto de tarjeta regalo separado para cada una. Esto te protege de los movimientos de tipo de cambio en un saldo que podría no usarse durante un año.
- **Las tarjetas regalo no pueden ser descuentadas.** Un vale no se aplicará a una línea de tarjeta regalo, porque vender 100 libras de crédito por 80 pierde 20 libras cada vez.
- **Una tarjeta regalo no puede comprar otra tarjeta regalo.** Esto cierra una ruta que la gente usa para lavar detalles de tarjetas robadas.
- **Comprar una tarjeta regalo no genera puntos de fidelidad.** Los puntos se generan cuando la tarjeta se usa para comprar productos, por lo que nadie gana puntos dos veces por el mismo dinero.

![Gestión de tarjetas regalo](/static/core/admin/img/help/gift-cards/gift-card-list.webp)

## Tipos de denominaciones

Estas configuraciones controlan cómo un cliente elige la cantidad al comprar una tarjeta regalo:

| Tipo | Descripción |
|------|-------------|
| **Denominaciones fijas** | Los clientes eligen entre montos predeterminados (por ejemplo, $25, $50, $100) |
| **Monto personalizado** | Los clientes ingresan cualquier monto dentro de un rango mínimo/máximo |
| **Ambos** | Ofrece denominaciones predeterminadas más una opción de monto personalizado |

## Crear un producto de tarjeta regalo

Cada tarjeta regalo — ya sea que eventualmente se venda o se emita manualmente hoy — necesita tener detrás un producto de tipo Tarjeta Regalo.

### Paso 1: Configurar el producto

1. Navega a **Productos > Todos los productos** y haz clic en **+ Añadir producto**
2. Establece **Tipo de producto** en **Tarjeta regalo**
3. Llena el nombre del producto y la descripción
4. Configura las opciones de denominación:
   - Elige un **Tipo de denominación** (Fija, Personalizada o Ambos)
   - Para Fija: establece los montos de denominación disponibles
   - Para Personalizada: establece el **Mínimo** y el **Máximo** de montos permitidos
5. Establece **Días de vencimiento** (0 = nunca vence) — esto determina cuánto tiempo serán válidas las tarjetas regalo después de la compra
6. Guarda y publica el producto

### Paso 2: Publicar

Publica el producto cuando estés listo para venderlo. Los clientes pueden comprarlo desde tu tienda en línea de inmediato, y la tarjeta se enviará por correo electrónico automáticamente una vez que se confirme su pago.

El producto también es lo que seleccionarás cuando emitas una tarjeta manualmente — por lo tanto, vale la pena crear uno incluso si planeas dar tarjetas regalo solo como regalo.

## Crear una tarjeta regalo manualmente

Este es el único método disponible para crear una tarjeta regalo financiada actualmente, y funciona completamente hoy en día.

1. Navega a **Productos > Tarjetas regalo** y haz clic en **+ Añadir tarjeta regalo**
2. Elige el **Producto** — debe ser un producto existente de tipo Tarjeta Regalo (ver arriba)
3. Ingresa el **Valor inicial** — el saldo inicial, en cualquier monto que elijas. A diferencia de una compra del cliente, esto no está limitado a las configuraciones de denominación del producto
4. Opcionalmente establece una fecha de **Vencimiento en** y deja marcada **Activa** para que la tarjeta pueda canjearse
5. Llena la sección **Receptor**, más abajo en la misma página:
   - **Correo electrónico del receptor** — obligatorio; lugar donde se enviará el correo electrónico de entrega
   - **Nombre del receptor**, **Nombre del remitente** y **Mensaje personal** — todos son opcionales
   - **Enviar programado en** — opcional; deja en blanco y envía cuando estés listo, o establece una fecha/hora futura (por ejemplo, un cumpleaños)
6. Haz clic en **Guardar**

El código de redención se genera automáticamente y el saldo inicial se establece desde el Valor Inicial — tú no llenas ninguno de esos campos manualmente.

**Guardar la tarjeta no la envía por correo electrónico.** Para entregarla, regrese a la lista de tarjetas regalo, seleccione la casilla de la tarjeta, elija **Enviar correos electrónicos de tarjetas regalo** desde el menú desplegable de Acciones y haga clic en **Ir**.

La misma acción vuelve a enviar el correo electrónico si necesita reenviarlo más tarde.

## Administración de Tarjetas Regalo en el Panel de Control

Navegue hasta **Productos > Tarjetas Regalo** para administrar todas las tarjetas regalo:

### Panel de Estadísticas

En la parte superior de la página, cuatro tarjetas muestran métricas clave:

- **Total de Tarjetas Regalo** — Número total de tarjetas regalo emitidas
- **Activa** — Tarjetas actualmente activas con saldo disponible
- **Total de Saldo** — Saldo restante combinado en todas las tarjetas
- **Parcialmente Usada** — Tarjetas que han sido parcialmente canjeadas

### Filtros

Filtre tarjetas regalo por:

- **Buscar** — Buscar por código, correo electrónico o nombre del destinatario
- **Estado** — Activa, Inactiva, Vencida, Totalmente Canjeadas o Parcialmente Usada
- **Saldo** — Con Saldo o Sin Saldo
- **Creada** — Período de tiempo (Hoy, Esta Semana, Este Mes, Este Año)

### Detalles de la Tarjeta Regalo

Cada tarjeta regalo muestra:

- **Código** — El código único de canje (ej. GC-XXXX-XXXX-XXXX)
- **Destinatario** — Correo electrónico y nombre
- **Etiquetas de estado** — Estado actual con codificación de colores
- **Saldo / Inicial / Canjeados** — Resumen financiero con porcentaje usado
- **Fechas clave** — Creada, emitida, primera vez usada
- **Remitente** — Quién compró (o quién emitió) la tarjeta regalo

### Acciones

- Haga clic en una tarjeta regalo para **editar** sus detalles y ver su **historial de transacciones** completo, que se muestra en línea en la misma página
- Seleccione una o más tarjetas y use el menú desplegable **Acciones** para **Enviar correos electrónicos de tarjetas regalo** (entrega o vuelve a enviar el correo de entrega) o **Marcar las tarjetas regalo seleccionadas como inactivas** (desactiva — el saldo se mantiene pero la tarjeta ya no puede canjearse)

## Canje Hoy

**En tienda**, en su terminal de Punto de Venta:

1. El cajero recibe el código en el paso de pago
2. El código se valida — activo, no vencido, con saldo y en la misma moneda que la venta
3. El saldo se aplica al monto total adeudado, incluyendo impuestos y envío
4. Si el saldo no cubre toda la venta, el cliente paga el resto de otra manera
5. El saldo se deduce y la transacción se registra

Tenga en cuenta que el cajero recibe el código en **pago**, no cuando se construye el carrito. Una tarjeta regalo es dinero que el cliente ya ha entregado, por lo que salda la cuenta en lugar de descuentar los productos.

**En línea**, en el proceso de pago hay un campo para tarjetas regalo en el paso de pago. El cliente ingresa su código, el saldo se deduce del monto adeudado — después de impuestos y envío — y cualquier resto se cobra a su tarjeta como de costumbre. Si la tarjeta cubre todo el pedido, no se necesita otro pago. El saldo solo se deduce realmente una vez que se confirma el pago, por lo tanto, un carrito abandonado nunca afecta la tarjeta.

Los destinatarios también pueden verificar su saldo restante en cualquier momento en el enlace de su correo de entrega.

## Manejo de Reembolsos

Cuando se devuelven pedidos o ventas que usaron una tarjeta regalo:

- **Una tarjeta regalo comprada por el cliente, aún no usada** — la tarjeta se desactiva y su saldo se pone en cero, por lo que el crédito desaparece junto con el reembolso.
- **Una tarjeta regalo comprada por el cliente y parcialmente gastada** — esto requiere su juicio. Desactivarla tomaría el crédito que el cliente ya ha usado, por lo que el saldo se deja sin tocar y se marca para que usted lo ajuste manualmente.
- **Una tarjeta regalo usada para pagar el pedido que se devuelve** — el reembolso se devuelve primero a la tarjeta, antes de cualquier pago con tarjeta o banco. Devolver dinero a un banco del que el comerciante nunca realmente recibió es el peor error, y devolver el valor donde vino también cierra una ruta conocida de fraude. Si la tarjeta original ha vencido o ha sido desactivada, se emite una tarjeta de reemplazo al mismo destinatario sin fecha de vencimiento.
- **Reembolso total** — Crédito la cantidad de vuelta al saldo de la tarjeta regalo a través de una transacción de reembolso

## Consejos

Conservar todo el formato de markdown, rutas de imágenes, bloques de código y términos técnicos.

- Usa la emisión manual para créditos de buena voluntad, resoluciones de servicio al cliente o cualquier caso en el que desees otorgar a un cliente un crédito de tienda sin una compra en el sitio web.
- Establece períodos de vencimiento razonables (por ejemplo, 365 días) para cumplir con las regulaciones locales sobre tarjetas regalo — algunas jurisdicciones requieren períodos mínimos de validez.
- Usa el tipo de denominación "Ambos" para ofrecer comodidad (montos predeterminados) y flexibilidad (un monto personalizado).
- Monitorea regularmente la métrica Total Balance — representa una obligación pendiente en tus registros contables.
- Una tarjeta se gasta de la misma manera en línea y en persona — en el paso de pago durante el checkout en la web, o en el mostrador.

El correo electrónico de entrega incluye un enlace para verificar el saldo que los destinatarios pueden usar en cualquier momento.
- Si vendes a clientes en múltiples países, puedes emitir tarjetas regalo en monedas específicas — consulta el tema de ayuda **Tarjetas Regalo Multimoneda** para obtener más detalles.