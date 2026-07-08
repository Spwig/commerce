---
title: Plantillas de SMS
---

Las plantillas de SMS controlan el texto de cada notificación que su tienda envía a los clientes a través de mensajes de texto. Cada plantilla corresponde a un evento específico, como una confirmación de pedido o una actualización de envío, y utiliza variables de marcador de posición que Spwig reemplaza con los detalles reales del pedido cuando se envía el mensaje.

Navegue hasta **Sistema de SMS > Plantillas de SMS** para ver y editar sus plantillas.

![Lista de plantillas de SMS](/static/core/admin/img/help/sms-templates/templates-list.webp)

## Tipos de plantilla disponibles

Spwig incluye los siguientes tipos de plantilla preinstalados:

| Tipo de plantilla | Cuándo se envía |
|------------------|----------------|
| Confirmación de pedido | Cuando un cliente coloca un pedido |
| Actualización de envío | Cuando el estado de seguimiento de un pedido cambia |
| Notificación de entrega | Cuando un pedido se marca como entregado |
| Restablecimiento de contraseña | Cuando un cliente solicita un restablecimiento de contraseña |
| Código de verificación | Cuando se necesita un código de uso único para la verificación de cuenta |
| Recibo de POS | Cuando se procesa una venta en una terminal de punto de venta |
| Marketing | Para campañas promocionales (requiere opt-in separado) |
| Personalizado | Para cualquier otra notificación que cree |

## Edición de una plantilla

1. Navegue hasta **Sistema de SMS > Plantillas de SMS**
2. Haga clic en la plantilla que desee editar
3. Actualice el campo **Mensaje** con su texto deseado
4. Use marcadores de posición `{variable}` para incluir información específica del pedido (consulte las variables a continuación)
5. Marque **Activo** para habilitar la plantilla — las plantillas inactivas no se envían
6. Haga clic en **Guardar**

![Edición de una plantilla de SMS](/static/core/admin/img/help/sms-templates/template-edit.webp)

## Uso de variables

Las variables son marcadores de posición escritos entre llaves curvas — por ejemplo, `{nombre}` o `{número_de_pedido}`. Cuando Spwig envía el mensaje, reemplaza cada marcador de posición con el valor real para ese cliente o pedido.

### Variables comunes

| Variable | Reemplazado con |
|----------|------------------|
| `{nombre}` | El nombre propio del cliente |
| `{número_de_pedido}` | El número de referencia del pedido |
| `{total}` | El monto total del pedido |
| `{número_de_seguimiento}` | El número de seguimiento del envío |
| `{nombre_de_tienda}` | El nombre de su tienda |
| `{código}` | Un código de verificación o restablecimiento |

**Ejemplo de mensaje:**

```
Hola {nombre}, su pedido #{número_de_pedido} ha sido confirmado. Total: {total}. Le actualizaremos cuando se envíe. - {nombre_de_tienda}
```

Cuando se envía, esto se convierte en:

```
Hola Sarah, su pedido #10045 ha sido confirmado. Total: $89.00. Le actualizaremos cuando se envíe. - The Garden Shop
```

> Solo incluya variables que estén disponibles para un tipo de plantilla dado. Por ejemplo, `{número_de_seguimiento}` está disponible en una plantilla de Actualización de envío, pero no en una plantilla de Restablecimiento de contraseña. Si usa una variable no disponible, aparecerá tal cual (sin reemplazar) en el mensaje.

## Límites de caracteres y longitud del mensaje

Los mensajes de SMS estándar tienen un límite de **160 caracteres** para un solo segmento. Los mensajes más largos se dividen en varios segmentos y se envían como uno (SMS concatenado), pero los operadores cuentan cada segmento por separado para fines de facturación.

**Consejos para mantenerse dentro del límite:**
- Mantenga los mensajes concisos — un propósito por mensaje
- Abrevie frases comunes donde sea natural (por ejemplo, "Ord" en lugar de "Order")
- Evite palabras de relleno innecesarias

Spwig no impone un límite de caracteres estricto en el editor, por lo tanto, cuente sus caracteres (incluyendo los valores de las variables) antes de guardar.

## Activar y desactivar plantillas

El interruptor **Activo** en cada plantilla controla si se envía ese tipo de notificación. Si una plantilla está inactiva, Spwig omitirá completamente el envío de esa notificación — el mensaje aparecerá como **Saltado** en la bandeja de salida de SMS con la razón `template_inactive`.

Para activar una plantilla:
1. Abra la plantilla
2. Marque la casilla **Activo**
3. Guarde

Para desactivar (detener el envío de un tipo de notificación sin eliminar la plantilla):
1. Abra la plantilla
2. Desmarque **Activo**
3. Guarde

## Consejos

Conservar todo el formato de markdown, rutas de imágenes, bloques de código y términos técnicos.

- Escribe mensajes en el mismo tono que tu marca — el SMS es un canal directo y personal, por lo que un tono amigable funciona bien
- Siempre incluye el nombre de tu tienda en el mensaje para que los clientes sepan quién los está contactando
- Mantén los mensajes de confirmación de pedidos breves: el número de pedido, el total y una nota sobre los pasos siguientes es suficiente
- Prueba los mensajes colocando un pedido de prueba en tu propia tienda (usando un número de teléfono que controle) para ver exactamente lo que reciben los clientes
- Si una notificación está generando confusión o quejas, desactiva la plantilla y revísala en lugar de eliminarla — de esa manera podrás reactivarla una vez que esté actualizada
- Las plantillas de marketing solo deben enviarse a clientes que hayan optado explícitamente por recibir marketing por SMS, según lo requieren las regulaciones de telecomunicaciones en la mayoría de los países