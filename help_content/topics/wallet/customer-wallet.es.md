---
title: Billetera del cliente
---

La billetera del cliente es un registro de crédito de tienda que lleva un balance en curso para cada cliente. El crédito de tienda puede agregarse como resultado de reembolsos, recompensas por referidos, campañas promocionales o ajustes manuales realizados por tu equipo.

> **Los saldos de la billetera se pueden utilizar en el proceso de pago.** Un cliente registrado con crédito de tienda lo ve en el paso de pago y puede aplicarlo con un solo clic. El crédito se deduce del monto final de la factura — después de impuestos y envío — y cualquier resto se cobra normalmente a su tarjeta. Si el crédito cubre completamente el pedido, no se necesita ninguna tarjeta. El crédito se reserva al aplicarlo y solo se deduce realmente una vez que se confirme el pago, por lo tanto, un proceso de pago abandonado nunca cuesta nada al cliente.

Navega a **Clientes > Billeteras de clientes** para ver y gestionar las billeteras.

## Entendiendo los saldos de la billetera

Cada billetera del cliente muestra cuatro figuras de saldo:

| Balance | Descripción |
|---|---|
| **Saldo disponible** | El crédito actual y utilizable del cliente — esto será lo que se pueda utilizar en el proceso de pago una vez que esa función esté disponible |
| **Saldo pendiente** | Créditos que aún no están en el saldo disponible — por ejemplo, un reembolso que aún está dentro de su período de confirmación |
| **Crédito total en la vida** | La cantidad total que ha sido creditada en esta billetera, incluyendo todos los créditos pasados |
| **Uso total en la vida** | La cantidad total que ha sido debitada de esta billetera |

El saldo disponible es la figura que importará una vez que el gasto en el proceso de pago esté activo. Los créditos pendientes se mueven a este una vez que expire el período pendiente.

## Ver la billetera de un cliente

1. Navega a **Clientes > Billeteras de clientes**
2. Usa el campo de búsqueda para encontrar al cliente por nombre o correo electrónico
3. Haz clic en la entrada de la billetera para abrir la vista detallada

La vista detallada muestra los saldos actuales en la parte superior y un historial completo de transacciones debajo. Las marcas de tiempo **Último crédito en** y **Último uso en** te indican cuándo la billetera estuvo activa por última vez.

### Filtros de la lista de billeteras

Usa el filtro **Activo** para separar las billeteras activas de las congeladas. Una billetera marcada como inactiva está congelada — no se pueden registrar créditos ni débitos contra ella, aunque mantenga su saldo.

## Leyendo el historial de transacciones

Cada cambio en el saldo de una billetera se registra como una transacción individual. El historial de transacciones es un libro contable completo y permanente — las transacciones nunca se editan ni eliminan. Si se necesita corregir un error, se agrega una nueva transacción compensadora en su lugar.

Cada transacción muestra:

| Campo | Descripción |
|---|---|
| **Tipo** | Crédito, Débito, Reembolso, Ajuste o Reversión |
| **Monto** | El valor de esta transacción (siempre mostrado como un número positivo) |
| **Saldo después** | El saldo de la billetera inmediatamente después de que se aplicara esta transacción |
| **Fuente** | Dónde se originó el crédito o débito |
| **Estado** | Completado, Pendiente o Revertido |
| **Descripción** | Una breve explicación de la transacción |
| **ID de referencia** | Un enlace al registro original (por ejemplo, un número de pedido o ID de recompensa) |
| **Creado en** | Cuando se registró la transacción |

### Explicación de los tipos de transacciones

- **Crédito** — fondos agregados a la billetera (de un reembolso, promoción o ajuste manual)
- **Débito** — fondos retirados de la billetera. Una vez que el gasto en el proceso de pago esté disponible, esto significará "gastado en un pedido" — por ahora, la única manera en que ocurre un débito es mediante un ajuste manual
- **Reembolso** — crédito agregado específicamente como resultado de un pedido devuelto o cancelado
- **Ajuste** — una corrección manual realizada por tu equipo
- **Reversión** — una transacción que anula una entrada anterior

### Explicación de las fuentes de transacciones

- **Reembolso de pedido** — crédito otorgado cuando un pedido se reembolsó a la billetera
- **Recompensa por referido** — crédito ganado a través del programa de referidos
- **Promoción** — crédito otorgado como parte de una campaña de marketing
- **Ajuste manual** — crédito agregado o retirado directamente por un miembro del personal
- **Pago de pedido** — fondos gastados en el proceso de pago para pagar un pedido. No se usa aún — reservado para cuando el gasto en la billetera en el proceso de pago esté disponible

## Ajustes manuales de billetera

No puedes agregar ni restar fondos desde el panel de administración — las transacciones de la billetera se crean solo mediante los procesos que las poseen: reembolsos de pedidos, recompensas de lealtad y recompensas de referidos. Esto es intencional. Cada movimiento lleva una referencia a lo que lo causó, y una verificación nocturna verifica el saldo de cada billetera contra su propia historia; las filas ingresadas a mano son lo que rompe esa cadena.

Para un crédito de buena voluntad — una queja de servicio, un gesto después de un problema — emite una **tarjeta regalo** a mano en su lugar (consulte el tema de ayuda **Tarjetas Regalo**). Una tarjeta regalo está diseñada exactamente para esto: tú controlas el valor, el cliente recibe un código por correo electrónico, y se gasta en el momento del pago de la misma manera que la tarjeta de crédito del almacén.

## Congelar una billetera

Si necesitas evitar que un cliente utilice su saldo de billetera — por ejemplo, durante una investigación de fraude — puedes desactivarla sin eliminarla ni quitar el saldo.

1. Abre la vista de detalles de la billetera del cliente
2. Desmarca el interruptor **Activa**
3. Haz clic en **Guardar**

El saldo se conserva y la billetera puede reactivarse en cualquier momento. Mientras esté inactiva, no se pueden registrar nuevos créditos o débitos — manuales o de otro tipo — contra la billetera.

## Ver todas las transacciones

Para una vista general de la actividad de la billetera, navega a **Clientes > Transacciones de Billetera**. Esta lista muestra todas las transacciones en todas las billeteras de los clientes, con filtros para:

- **Tipo de transacción** — filtra por crédito, débito, ajuste, etc.
- **Fuente** — filtra por donde originaron las transacciones
- **Estado** — filtra por completado, pendiente o revertido
- **Fecha** — usa la jerarquía de fechas en la parte superior para explorar un día, mes o año específico

La lista de transacciones es de solo lectura — no se pueden editar ni eliminar transacciones desde esta vista.

## Consejos

- Revisa **Crédito Vitalicio** versus **Usado Vitalicio** para entender cuán activamente un cliente utiliza su crédito de tienda — un gran saldo no utilizado puede indicar que el cliente ha olvidado que existe
- Si un cliente reporta que su saldo parece incorrecto, revisa la historia completa de transacciones para rastrear exactamente cómo cambió el saldo con el tiempo; la columna **Saldo Después** en cada entrada facilita esto
- Un gran saldo no gastado vale la pena un recordatorio — los clientes ven su crédito de tienda en el panel de control de la cuenta y en el paso de pago en el momento del pago, pero un breve correo electrónico que lo señale a menudo lo convierte en un pedido
- Las billeteras congeladas conservan su saldo permanentemente; no hay vencimiento — si desactivas temporalmente una billetera, recuerda reactivarla cuando el problema se resuelva
- El **ID de referencia** en cada transacción vincula de vuelta al registro original, lo que facilita verificar por qué se aplicó un crédito o débito sin tener que buscar en otro lugar