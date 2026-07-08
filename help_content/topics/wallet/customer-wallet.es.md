---
title: Billetera del cliente
---

La billetera del cliente es un sistema de crédito para tienda que le da al cliente un saldo que puede gastar en pedidos futuros. El crédito de la tienda puede agregarse como resultado de reembolsos, recompensas por referidos, campañas promocionales o ajustes manuales realizados por su equipo. Los clientes pueden luego aplicar su saldo de billetera en el momento del pago para reducir la cantidad que pagan.

Navegue a **Clientes > Billeteras de clientes** para ver y administrar billeteras.

## Entendiendo los saldos de la billetera

Cada billetera del cliente muestra cuatro figuras de saldo:

| Balance | Descripción |
|---|---|
| **Saldo disponible** | La cantidad que el cliente puede gastar ahora en el momento del pago |
| **Saldo pendiente** | Créditos que aún no son gastables — por ejemplo, un reembolso que aún está dentro de su ventana de confirmación |
| **Crédito total en la vida** | La cantidad total que ha sido creditada en esta billetera, incluyendo todos los créditos anteriores |
| **Total utilizado en la vida** | La cantidad total que el cliente ha gastado de su billetera en todos los pedidos |

El saldo disponible es la única figura que importa en el momento del pago. Los créditos pendientes se vuelven disponibles una vez que expire el período pendiente.

## Ver la billetera de un cliente

1. Navegue a **Clientes > Billeteras de clientes**
2. Use el campo de búsqueda para encontrar al cliente por nombre o correo electrónico
3. Haga clic en la entrada de la billetera para abrir la vista detallada

La vista detallada muestra los saldos actuales en la parte superior y un historial completo de transacciones debajo. Las marcas de tiempo **Último crédito en** y **Último uso en** le indican cuándo la billetera estuvo activa por última vez.

### Filtros de la lista de billeteras

Use el filtro **Activo** para separar las billeteras activas de las congeladas. Una billetera marcada como inactiva no puede usarse en el momento del pago, incluso si tiene un saldo positivo.

## Leyendo el historial de transacciones

Cada cambio en el saldo de una billetera se registra como una transacción individual. El historial de transacciones es un libro contable completo y permanente — las transacciones nunca se editan ni eliminan. Si se necesita corregir un error, se agrega en su lugar una nueva transacción compensadora.

Cada transacción muestra:

| Campo | Descripción |
|---|---|
| **Tipo** | Crédito, Débito, Reembolso, Ajuste o Reversión |
| **Monto** | El valor de esta transacción (siempre mostrado como un número positivo) |
| **Saldo después** | El saldo de la billetera inmediatamente después de que se aplicó esta transacción |
| **Fuente** | Dónde se originó el crédito o débito |
| **Estado** | Completado, Pendiente o Revertido |
| **Descripción** | Una explicación breve de la transacción |
| **ID de referencia** | Un enlace al registro original (por ejemplo, un número de pedido o ID de recompensa) |
| **Creado en** | Cuando se registró la transacción |

### Explicación de los tipos de transacciones

- **Crédito** — fondos agregados a la billetera (de un reembolso, promoción o ajuste manual)
- **Débito** — fondos gastados en el momento del pago
- **Reembolso** — crédito agregado específicamente como resultado de un pedido devuelto o cancelado
- **Ajuste** — una corrección manual realizada por su equipo
- **Reversión** — una transacción que anula una entrada anterior

### Explicación de las fuentes de transacciones

- **Reembolso de pedido** — crédito otorgado cuando un pedido se reembolsó a la billetera
- **Recompensa por referido** — crédito ganado a través del programa de referidos
- **Promoción** — crédito otorgado como parte de una campaña de marketing
- **Ajuste manual** — crédito agregado o eliminado directamente por un miembro del personal
- **Pago de pedido** — fondos gastados en el momento del pago para pagar un pedido

## Ajustes manuales de billetera

No puede agregar ni eliminar fondos directamente desde la vista detallada de la billetera — las transacciones de billetera se crean a través de los procesos relevantes (reembolsos, recompensas, promociones). Sin embargo, los miembros del personal con los permisos adecuados pueden crear transacciones de ajuste manual a través de la sección **Transacciones de billetera**.

Navegue a **Clientes > Transacciones de billetera** y use **+ Agregar transacción de billetera** si necesita aplicar un crédito que no encaja en otra fuente — por ejemplo, un crédito de buena voluntad tras una queja de servicio.

Al crear un ajuste manual:

1.

Seleccione la **Billetera** que está ajustando (busque por correo electrónico del cliente)
2.



Establezca **Tipo de Transacción** en `Ajuste`
3.

Establezca **Fuente** en `Ajuste Manual`
4.

Introduzca el **Monto** — siempre un número positivo, independientemente de la dirección
5.

Establezca el **Estado** en `Completado` para un crédito inmediato
6.

Agregue una **Descripción** clara que explique la razón — esto es visible en el historial de transacciones
7.

Haga clic en **Guardar**

> **Nota:** Debido a que las transacciones de billetera son inmutables, verifique cuidadosamente el monto y la billetera antes de guardar. Si comete un error, deberá crear una transacción de reversión para corregirlo.

## Congelar una billetera

Si necesita evitar que un cliente utilice su saldo de billetera — por ejemplo, durante una investigación de fraude — puede desactivarla sin eliminarla ni quitar el saldo.

1. Abra la vista de detalles de la billetera del cliente
2. Desactive el interruptor **Activo**
3. Haga clic en **Guardar**

El saldo se conserva y la billetera puede reactivarse en cualquier momento. Mientras esté inactiva, el cliente no podrá aplicar el saldo de la billetera en el momento del pago.

## Ver todas las transacciones

Para obtener una vista general de toda la actividad de la billetera, vaya a **Clientes > Transacciones de Billetera**. Esta lista muestra todas las transacciones de todas las billeteras de los clientes, con filtros para:

- **Tipo de Transacción** — filtre por crédito, débito, ajuste, etc.
- **Fuente** — filtre por dónde originaron las transacciones
- **Estado** — filtre por completado, pendiente o revertido
- **Fecha** — use la jerarquía de fechas en la parte superior para explorar un día, mes o año específico

La lista de transacciones es de solo lectura — no se pueden editar ni eliminar transacciones desde esta vista.

## Consejos

- Revise **Crédito Vitalicio** versus **Usado Vitalicio** para comprender cuán activamente un cliente utiliza su crédito de tienda — un gran saldo no utilizado puede indicar que el cliente ha olvidado que existe
- Si un cliente reporta que su saldo parece incorrecto, revise el historial de transacciones completo para rastrear exactamente cómo cambió el saldo con el tiempo; la columna **Saldo Después** en cada entrada facilita esto
- Use créditos de billetera como herramienta de retención de clientes — un crédito de buena voluntad después de una experiencia difícil con un pedido puede costar menos que un reembolso, manteniendo al cliente gastando en su tienda
- Las billeteras congeladas conservan su saldo permanentemente; no hay vencimiento — si desactiva temporalmente una billetera, recuerde reactivarla cuando el problema se resuelva
- El **ID de Referencia** en cada transacción se vincula al registro de origen, lo que facilita verificar por qué se aplicó un crédito o débito sin tener que buscar en otro lugar