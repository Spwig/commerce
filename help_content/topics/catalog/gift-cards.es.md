---
title: Tarjetas de Regalo
---

Las tarjetas de regalo permiten a tus clientes comprar créditos para la tienda que pueden enviar a alguien como regalo o guardarlo para uso personal. Los destinatarios reciben un código único por correo electrónico que pueden canjear en el momento del pago.

![Gestión de tarjetas de regalo](/static/core/admin/img/help/gift-cards/gift-card-list.webp)

## Tipos de Denominaciones

Controla cómo los clientes eligen la cantidad de la tarjeta de regalo:

| Tipo | Descripción |
|------|-------------|
| **Denominaciones Fijas** | Los clientes eligen entre montos preestablecidos (por ejemplo, $25, $50, $100) |
| **Monto Personalizado** | Los clientes ingresan cualquier monto dentro de un rango mínimo/máximo |
| **Ambos** | Ofrece denominaciones preestablecidas más una opción de monto personalizado |

## Crear un Producto de Tarjeta de Regalo

### Paso 1: Configurar el Producto

1. Navegue a **Productos > Todos los Productos** y haga clic en **+ Agregar Producto**
2. Establezca **Tipo de Producto** en **Tarjeta de Regalo**
3. Llene el nombre del producto y la descripción
4. Configure la configuración de denominación:
   - Elija un **Tipo de Denominación** (Fija, Personalizada o Ambas)
   - Para Fija: establezca las denominaciones disponibles
   - Para Personalizada: establezca el **Mínimo** y el **Máximo** de montos permitidos
5. Establezca **Días de Vencimiento** (0 = nunca vence) — esto determina cuánto tiempo serán válidas las tarjetas de regalo después de la compra
6. Guarde y publique el producto

### Paso 2: Publicar y Vender

Una vez publicado, la tarjeta de regalo aparece en tu tienda en línea como cualquier otro producto. Los clientes pueden navegar hasta ella, seleccionar un monto y agregarla a su carrito.

## Ciclo de Vida de la Tarjeta de Regalo

Una tarjeta de regalo sigue este ciclo de vida:

1. **Compra** — El cliente compra el producto de tarjeta de regalo y proporciona los detalles del destinatario
2. **Entrega** — Se envía automáticamente un correo electrónico con el código de la tarjeta de regalo al destinatario
3. **Canje** — El destinatario ingresa el código en el momento del pago para aplicar el saldo
4. **Seguimiento del Saldo** — Cada uso deduce del saldo hasta que alcance cero

## Flujo de Compra del Cliente

Cuando un cliente compra una tarjeta de regalo:

1. **Seleccionar Monto** — Elija una denominación o ingrese un monto personalizado
2. **Detalles del Destinatario** — Ingrese la dirección de correo electrónico y el nombre del destinatario
3. **Mensaje Personal** — Agregue un mensaje opcional para incluirlo en el correo de entrega
4. **Nombre del Remitente** — Proporcione el nombre del remitente para el correo
5. **Entrega Programada** — Opcionalmente, programe el correo para una fecha futura (por ejemplo, un cumpleaños)
6. **Paso de Pago** — Complete la compra como cualquier otro producto

## Entrega Automática

Después de la compra, la tarjeta de regalo se entrega automáticamente:

- Se envía un correo electrónico con estilo al destinatario que incluye:
  - El código único de la tarjeta de regalo
  - El valor de la tarjeta de regalo
  - El mensaje personal del remitente
  - Un enlace para verificar el saldo restante
- Si se estableció una entrega programada, el correo se enviará en la fecha y hora especificadas
- El remitente recibe una confirmación de pedido con los detalles de la tarjeta de regalo

## Gestión de Tarjetas de Regalo en el Panel de Administración

Navegue a **Productos > Tarjetas de Regalo** para gestionar todas las tarjetas de regalo:

### Panel de Estadísticas

En la parte superior de la página, cuatro tarjetas muestran métricas clave:

- **Total de Tarjetas de Regalo** — Número total de tarjetas de regalo emitidas
- **Activas** — Tarjetas activas con saldo disponible
- **Total de Saldo** — Saldo restante combinado de todas las tarjetas
- **Parcialmente Usadas** — Tarjetas que han sido canjeadas parcialmente

### Filtros

Filtre tarjetas de regalo por:

- **Buscar** — Buscar por código, correo electrónico o nombre del destinatario
- **Estado** — Activo, Inactivo, Vencido, Totalmente Canjeadas o Parcialmente Usadas
- **Saldo** — Tiene Saldo o Saldo Cero
- **Creado** — Período de tiempo (Hoy, Esta Semana, Este Mes, Este Año)

### Detalles de la Tarjeta de Regalo

Cada tarjeta de regalo muestra:

- **Código** — El código único de canje (por ejemplo, GC-XXXX-XXXX-XXXX)
- **Destinatario** — Correo electrónico y nombre
- **Etiquetas de Estado** — Estado actual con codificación de colores
- **Saldo / Inicial / Canjeadas** — Resumen financiero con porcentaje usado
- **Fechas clave** — Creada, emitida, primera vez usada
- **Remitente** — Quién compró la tarjeta de regalo

### Acciones

Para cada tarjeta de regalo, puede:

- **Editar** — Ver y modificar los detalles de la tarjeta de regalo
- **Ver Transacciones** — Ver el historial completo de transacciones
- **Reenviar Correo** — Reenviar el correo de entrega al destinatario
- **Deshabilitar** — Deshabilitar la tarjeta (el saldo se mantiene pero no puede usarse)

## Canje en el Momento del Pago

Cuando un cliente ingresa un código de tarjeta de regalo en el momento del pago:

1. El código se valida (activa, no vencida, con saldo)
2. Se muestra el saldo disponible
3. El saldo se aplica al total del pedido
4. Si el saldo cubre el total del pedido, no se necesita un pago adicional
5. Si el saldo es menor que el total del pedido, el cliente paga el resto
6. La transacción se registra y el saldo se actualiza

## Manejo de Devoluciones

Cuando se devuelven pedidos que usaron una tarjeta de regalo:

- **Tarjetas de regalo no usadas** — Deshabilitar completamente la tarjeta de regalo
- **Tarjetas parcialmente usadas** — El saldo debe ajustarse manualmente a través de una transacción
- **Devolución total** — Crédito la cantidad de vuelta a la tarjeta de regalo a través de una transacción de devolución

## Consejos

- Establezca períodos de vencimiento razonables (por ejemplo, 365 días) para cumplir con las regulaciones locales de tarjetas de regalo — algunas jurisdicciones requieren períodos mínimos de validez.
- Use el tipo de denominación "Ambos" para ofrecer comodidad (montos preestablecidos) y flexibilidad (montos personalizados).
- Monitorea regularmente la métrica de Total de Saldo — representa una obligación pendiente en tus libros.
- Usa la entrega programada para promociones estacionales — los clientes pueden comprar tarjetas de regalo con anticipación y tenerlas entregadas en la fecha exacta.
- Prueba el flujo completo (compra, entrega por correo, canje) con un pedido de prueba antes de lanzar.
- Si vendes a clientes en múltiples países, puedes emitir tarjetas de regalo en monedas específicas — consulte el tema de ayuda **Tarjetas de Regalo Multimoneda** para obtener detalles.