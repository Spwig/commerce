---
title: Carritos abandonados
---

Un carrito abandonado se crea cuando un cliente registrado agrega artículos a su carrito pero no completa el proceso de pago dentro de 24 horas. Spwig rastrea automáticamente estos carritos para que puedas entender la pérdida de ingresos, identificar patrones por los que los clientes dejan de comprar y tomar medidas para recuperar ventas.

Navega a **Clientes > Carritos abandonados** para ver todas las abandonaciones registradas.

## Lo que puedes ver en la lista de carritos abandonados

La vista de lista muestra cada carrito abandonado con la siguiente información a primera vista:

| Columna | Descripción |
|---|---|
| **Cliente** | El nombre y correo electrónico del cliente |
| **Abandonado en** | Fecha y hora en que el carrito fue marcado como abandonado |
| **Valor total** | El valor monetario de los artículos en el carrito en el momento del abandono |
| **Número total de artículos** | Cantidad de artículos en el carrito |
| **Razón estimada** | Mejor suposición de Spwig sobre la razón del abandono |
| **Estado de recuperación** | Si este carrito ha sido recuperado (convertido en un pedido completado) |
| **Días desde el abandono** | Cuánto tiempo ha pasado desde que el carrito fue abandonado |

### Filtros de carritos abandonados

Utiliza los filtros del lado derecho para restringir la lista:

- **Razón estimada** — filtra por la razón del abandono (por ejemplo, mostrar solo carritos donde la razón estimada fue un costo de envío alto)
- **Recuperado** — filtra para mostrar solo carritos recuperados o no recuperados
- **Abandonado en** — filtra por rango de fechas para enfocarte en abandonos recientes o un período de campaña específico

## Entendiendo las razones de abandono

Spwig registra una razón estimada para cada abandono. Estas razones se basan en señales capturadas durante el proceso de pago y no están garantizadas para ser exactas, pero ofrecen un punto de partida útil para diagnosticar patrones de abandono.

| Razón | Lo que podría indicar |
|---|---|
| **Desconocido** | No se capturó una señal específica — la razón más común |
| **Costo de envío alto** | El cliente podría haber estado desalentado por el costo de envío mostrado durante el pago |
| **Total demasiado alto** | El total general del pedido podría haber sido más alto de lo esperado |
| **Problemas en el pago** | El cliente encontró un problema durante el proceso de pago |
| **Pago fallido** | Se realizó un intento de pago pero falló |
| **Comparación de precios** | El cliente probablemente visitó para comparar precios |
| **Guardado para más tarde** | El cliente guardó intencionalmente los artículos para una visita futura |

Si ves una proporción grande de carritos con la misma razón — por ejemplo, un grupo significativo de abandonos por "Costo de envío alto" — es una señal que vale la pena investigar en tus configuraciones de envío o presentación del proceso de pago.

## Ver un carrito abandonado individual

Haz clic en cualquier fila de la lista para abrir la vista de detalles. Verás:

- **Detalles del abandono** — el cliente, la referencia del carrito, cuándo fue abandonado y la razón estimada
- **Resumen del carrito** — el número de artículos y el valor total en el momento del abandono
- **Seguimiento de recuperación** — si el carrito fue recuperado, cuándo fue recuperado y qué pedido se convirtió

El campo **Carrito** enlaza directamente al registro del carrito subyacente, por lo que puedes ver exactamente qué productos estaban en el carrito.

## Flujo de trabajo de recuperación

Spwig rastrea si cada carrito abandonado eventualmente se convierte en un pedido completado. Cuando un cliente regresa y completa una compra desde un carrito abandonado, el registro se marca automáticamente como **Recuperado** y el pedido resultante se vincula.

El contador **Correos de recuperación enviados** muestra cuántos correos de recuperación automatizados se han enviado al cliente para este carrito. Esto te ayuda a entender si tus campañas de correo electrónico están motivando a los clientes a regresar.

### Acciones de recuperación manual

La vista de carritos abandonados es de solo lectura — es un registro de lo que sucedió, no una herramienta para editar el contenido del carrito. Para actuar sobre carritos abandonados:

1.

Nota la dirección de correo electrónico del cliente desde el registro del carrito abandonado
2.

Utiliza tu sistema de correo o herramientas de marketing para enviar un mensaje personalizado
3.

Considera adjuntar un código de cupón para dar al cliente un incentivo para completar la compra
4.



Monitorea el estado **Recovered** durante los siguientes días para ver si la campaña de outreach tuvo éxito

## Analizando tendencias de abandono de carritos

Revisa la lista de carritos abandonados con frecuencia como una revisión de salud de tu proceso de pago:

- Un pico repentino en los abandons puede indicar un problema técnico con el checkout o el pago
- Valores de carrito consistentemente altos en carritos no recuperados representan tu segmento de recuperación de mayor oportunidad
- Compara la proporción de carritos recuperados frente a los no recuperados con el tiempo para medir la efectividad de tus correos de recuperación

La sección **Customer Analytics** de cada perfil de cliente también muestra su tasa personal de abandono de carritos, por lo que puedes identificar clientes que frecuentemente añaden al carrito pero rara vez completan una compra.

## Consejos

- Ordena por **Total Value** (de mayor a menor) para identificar los carritos de mayor valor que merecen prioridad para el outreach personalizado
- Usa el filtro **Abandoned At** para revisar abandons de una campaña o período promocional específico — un pico durante una venta flash puede significar que tu promoción atrajo navegadores en lugar de compradores
- Combina los datos de carritos abandonados con campañas de cupones: envía un código de descuento con límite de tiempo a clientes con carritos de alto valor no recuperados para crear urgencia
- Un carrito abandonado por más de 7 días es poco probable que se recupere por sí solo — si los correos de recuperación están habilitados, estos son los carritos que necesitan más atención
- Los clientes invitados no aparecen en carritos abandonados — este seguimiento se aplica solo a clientes con cuentas registradas