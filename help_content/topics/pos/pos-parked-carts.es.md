---
title: Aparcar y reanudar transacciones POS
---

<!-- screenshots-needed:
- url: /en/admin/pos_app/parkedcart/
  filename: parked-cart-list.webp
  description: Vista de lista de carritos aparcados (puede estar vacía en una instalación nueva — capturar de todos modos)
  save-to: core/static/core/admin/img/help/pos/
-->

Los carritos aparcados permiten a tus cajeros pausar una transacción y comenzar a atender al siguiente cliente de inmediato, sin perder ni un solo artículo ni descuento. Cuando estés listo, el carrito original se restaura exactamente como estaba y la venta continúa desde el punto en el que se detuvo.

## ¿Qué hace apresar un carrito?

Cuando un cajero toca **Aparcar** en el registrador POS, Spwig guarda una captura completa del carrito actual en el servidor. El registrador se limpia para que pueda comenzar una transacción nueva de inmediato. El carrito aparcado se almacena y se vincula al terminal en el que fue creado.

Nada se pierde en la captura. El carrito aparcado conserva:

- Cada artículo y su cantidad
- Cualquier cliente que se haya vinculado a la venta
- Descuentos manuales aplicados al carrito o a artículos individuales

El carrito aparcado permanece disponible en el mismo terminal durante un máximo de **24 horas**. Después de eso, Spwig lo elimina automáticamente. Los carritos que ya han sido restaurados se eliminan inmediatamente después de la restauración y no cuentan para el período de 24 horas.

## ¿Cómo apresar una transacción?

Debes tener al menos un artículo en el carrito antes de poder apresarlo. Un carrito vacío no puede ser aparcado.

1. Mientras una venta esté en curso, toca el botón **Aparcar** en el registrador POS.
2. Spwig guarda el carrito y limpia el registrador. Verás una confirmación y la cuenta de carritos aparcados en la sección de carritos aparcados se actualizará.
3. Comienza la transacción del siguiente cliente en el registrador ahora vacío.

Si el cliente ya estaba vinculado a la venta antes de apresarla, su nombre aparecerá en la lista de carritos aparcados para una identificación fácil.

## ¿Cómo reanudar una transacción aparcada?

1. Toca el área o icono **Carritos Aparcados** en el registrador POS. Verás una lista de todos los carritos actualmente aparcados en este terminal, mostrando el nombre del cliente (si se vinculó uno), la cantidad de artículos, el monto total, el cajero que lo aparcó y la hora en que se aparcó.
2. Toca el carrito que deseas reanudar.
3. Si tu registrador actual tiene artículos en él, el POS los limpiará antes de restaurar el carrito aparcado. Asegúrate de haber completado o aparcado la transacción actual antes de reanudar otra.
4. Los artículos del carrito aparcado, el vínculo al cliente y los descuentos manuales se restauran. La venta continúa normalmente.

## Visibilidad de carritos aparcados

Los carritos aparcados están **vinculados al terminal** en el que se crearon. Cualquier cajero que esté conectado al mismo terminal puede ver y reanudar cualquier carrito aparcado en ese terminal — no hay restricción por cajero sobre quién puede recoger un carrito aparcado.

Los carritos aparcados en un terminal diferente, incluso en la misma ubicación de tienda, no son visibles en tu terminal actual.

## Cancelar un carrito aparcado desde el POS

Un cajero puede eliminar un carrito aparcado directamente desde la lista de carritos aparcados en el terminal — toca el carrito y usa la opción de eliminar o descartar. Los carritos aparcados eliminados se eliminan permanentemente y no pueden recuperarse.

## Caducidad automática y limpieza

Cada carrito aparcado caduca **24 horas después de haber sido aparcado**. Spwig ejecuta una tarea en segundo plano que elimina los carritos caducados que nunca se reanudaron. No necesitas hacer nada — la limpieza ocurre automáticamente.

Si necesitas limpiar carritos aparcados antes del período de 24 horas, un cajero puede eliminarlos uno por uno desde la lista de carritos aparcados en el terminal.

## Turnos y carritos aparcados

No hay un vínculo estricto entre un carrito aparcado y el turno que estaba abierto cuando se aparcó. Cerrar un turno **no** elimina o cancela automáticamente ningún carrito aparcado en ese terminal. Los carritos aparcados sobreviven a los cambios de turno y permanecen disponibles durante el período completo de 24 horas.

Esto significa:

- Un carrito aparcado al final de un turno matutino puede ser reanudado por un cajero en un turno posterior.
- Si no deseas que los carritos aparcados se lleven entre turnos, pide a los cajeros que limpien la lista de carritos aparcados antes de cerrar su turno.

## Consejos

Mantén todo el formato de markdown, rutas de imágenes, bloques de código y términos técnicos.

- Parcha un carrito en el momento en que un cliente diga "Solo necesito conseguir una cosa más" — es más rápido que pedirles que esperen en fila nuevamente o agregar manualmente los artículos de nuevo.
- Si la lista de carritos parcheados se está volviendo larga, verifica si un cajero anterior dejó transacciones sin resolver al final de su turno y limpia cualquier carrito obsoleto.
- Asocia a un cliente a la venta antes de parchear cuando puedas — su nombre aparece en la lista, lo que hace mucho más fácil encontrar el carrito correcto cuando regrese.
- Los carritos parcheados expiran después de 24 horas, por lo que no son adecuados para mantener transacciones durante la noche a través de múltiples días laborales.
- Recuerda que reanudar un carrito parcheado limpiará lo que actualmente esté en el cajero.

Completa o parcha la transacción activa antes de tomar un carrito parcheado diferente.