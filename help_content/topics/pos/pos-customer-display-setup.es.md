---
title: Configuración de la pantalla del cliente POS
---

Una pantalla del cliente es una segunda pantalla que se enfrenta a su cliente durante una venta. Mientras procesa la transacción, el cliente ve cada artículo a medida que se escanea, el subtotal acumulado, el desglose de precios y impuestos, y — cuando no haya una venta en curso — una presentación en slideshow de su contenido promocional."
    },
    {
      "type": "paragraph",
      "content": "Esta guía cubre el lado del hardware y el emparejamiento de la configuración de su pantalla del cliente: habilitar la función en un terminal, emparejar un dispositivo separado como pantalla, y manejar escenarios comunes de configuración. Para información sobre las diapositivas promocionales mostradas durante los períodos de inactividad, consulte [Diapositivas promocionales de la pantalla del cliente](customer-display-promo-slides)."
    },
    {
      "type": "heading",
      "content": "¿Qué muestra la pantalla del cliente?"
    },
    {
      "type": "paragraph",
      "content": "Cuando una venta está activa, la pantalla del cliente muestra:"
    },
    {
      "type": "list",
      "content": [
        "Cada artículo a medida que se agrega o elimina, con cantidad y precio",
        "El subtotal del carrito, cualquier descuento aplicado y el desglose de impuestos",
        "El total debido y, durante el pago, la cantidad entregada y el cambio"
      ]
    },
    {
      "type": "paragraph",
      "content": "Cuando el terminal está inactivo (sin transacción activa), la pantalla cambia a una presentación promocional. Usted controla el contenido de esa presentación por separado — consulte [Diapositivas promocionales de la pantalla del cliente](customer-display-promo-slides)."
    },
    {
      "type": "heading",
      "content": "Configuraciones de hardware comunes"
    },
    {
      "type": "paragraph",
      "content": "Hay tres formas prácticas de configurar una pantalla orientada al cliente:"
    },
    {
      "type": "list",
      "content": [
        "**Tablet o monitor separado en un soporte** — la configuración más común para ventas en mostrador. Una pequeña tablet colocada en un soporte se enfrenta al cliente mientras su terminal principal se enfrenta a usted. Usted empareja los dos dispositivos usando un código de corta duración (descrito a continuación).",
        "**Segundo monitor en modo escritorio extendido** — si su terminal principal es una laptop o un escritorio, conecte un segundo monitor, extienda su escritorio a él, luego arrastre la ventana de la pantalla al segundo monitor y maximícela. Ambas pantallas funcionan en el mismo dispositivo; no se necesita un código de emparejamiento.",
        "**Pantalla dedicada en poste** — una unidad de pantalla de hardware montada en un poste, normalmente conectada al terminal del mostrador a través de USB o colocada en el mostrador. Abra `/pos/display/` en el navegador del dispositivo del poste y empareje usando el código del terminal principal."
      ]
    },
    {
      "type": "heading",
      "content": "Habilitar la pantalla del cliente en un terminal"
    },
    {
      "type": "paragraph",
      "content": "La función de la pantalla del cliente se habilita por terminal a través de la configuración del hardware del terminal."
    },
    {
      "type": "list",
      "content": [
        "Navegue a **POS > Terminales** y abra el terminal que desea configurar (o haga clic en **+ Agregar terminal POS** para uno nuevo).",
        "Haga clic en la pestaña **Dispositivo**.",
        "Desplácese hasta la tarjeta **Configuración del hardware**. Verá un campo JSON.",
        "Agregue `"customer_display": true` al objeto JSON. Por ejemplo:"
      ]
    },
    {
      "type": "code-block",
      "content": "{'customer_display': true}"
    },
    {
      "type": "paragraph",
      "content": "Si el campo ya contiene otras configuraciones de hardware (como la configuración de impresora o escáner), agregue `"customer_display": true` junto con ellas:"
    },
    {
      "type": "code-block",
      "content": "{'printer': 'HP LaserJet', 'scanner': 'Datalogic', 'customer_display': true}"
    },
    {
      "type": "list",
      "content": [
        "Haga clic en **Guardar**."
      ]
    },
    {
      "type": "image",
      "content": "![Configuración del hardware del terminal con customer_display habilitado](/static/core/admin/img/help/pos-customer-display-setup/terminal-capabilities-toggle.webp)"
    },
    {
      "type": "paragraph",
      "content": "Una vez habilitada, la aplicación POS en ese terminal abrirá la vista de la pantalla del cliente en una segunda ventana o pestaña del navegador cuando comience una sesión."
    },
    {
      "type": "heading",
      "content": "Emparejar un dispositivo separado como la pantalla"
    },
    {
      "type": "paragraph",
      "content": "Si está usando un dispositivo físico separado para la pantalla del cliente (una tablet, teléfono o segundo computador), lo empareja con el terminal usando un código de 6 dígitos de corta duración."
    },
    {
      "type": "heading",
      "content": "Paso 1: Generar un código de emparejamiento en el terminal principal

Abre la aplicación POS en tu terminal principal y ve a la configuración de visualización o a la sección de emparejamiento de la interfaz del terminal.

Solicita un nuevo código de emparejamiento de visualización.

El código es un número de 6 dígitos y es válido durante **5 minutos**.

Cuando generes un nuevo código, cualquier código anterior no utilizado para este terminal se cancelará automáticamente.

### Paso 2: Abre la URL de la visualización en el dispositivo del cliente

En el dispositivo orientado al cliente, abre un navegador web y ve a:

```
https://your-store-domain.com/pos/display/
```

No se requiere iniciar sesión — la página de visualización está públicamente accesible. Esto es intencional: el dispositivo de visualización no necesita credenciales de personal, y el código de emparejamiento proporciona el enlace entre la visualización y el terminal correcto.

![Vista de visualización del cliente en estado inactivo](/static/core/admin/img/help/pos-customer-display-setup/customer-display-view.webp)

### Paso 3: Ingresa el código de emparejamiento

En el dispositivo del cliente, ingresa el código de 6 dígitos del terminal principal. La visualización se emparejará con ese terminal y comenzará a mostrar datos del carrito en vivo.

Una vez que se utilice el código, se invalidará de inmediato y no podrá reutilizarse.

## Regenerar un código de emparejamiento

Si el código de emparejamiento expira antes de que puedas ingresarlo, o si necesitas reemparejar el dispositivo de visualización (por ejemplo, si se reemplaza o restablece un dispositivo de visualización), genera un nuevo código desde la aplicación POS en el terminal principal.

Generar un nuevo código cancela automáticamente cualquier código existente no utilizado para ese terminal. El nuevo código es válido durante 5 minutos.

No es necesario cambiar nada en el administrador para regenerar un código — esto se hace completamente dentro de la aplicación POS.

## Configuración de múltiples monitores en un solo dispositivo

Si tu terminal principal es una laptop o un escritorio con dos monitores:

1. Conecta el segundo monitor y configúralo en modo **escritorio extendido** en la configuración de visualización de tu sistema operativo (no en modo espejo).
2. Abre la aplicación POS en la pantalla principal como de costumbre.
3. La aplicación POS abrirá la visualización del cliente en una segunda ventana. Arrastra esa ventana hacia el segundo monitor.
4. Maximiza o pasa a pantalla completa en el segundo monitor.

No se requiere un código de emparejamiento porque ambas ventanas se ejecutan en el mismo dispositivo y se comunican directamente.

## Comportamiento en estado inactivo

Cuando no hay una venta activa, la visualización del cliente muestra una diapositiva rotativa de imágenes promocionales. Creas y gestionas esas diapositivas por separado bajo **POS > Diapositivas promocionales**.

Para obtener detalles sobre la creación de diapositivas, su objetivo a tiendas específicas y la gestión de contenido estacional, consulta [Diapositivas promocionales de la visualización del cliente](customer-display-promo-slides).

Si no se han configurado diapositivas, la visualización muestra una pantalla de bienvenida simple con el nombre de tu tienda.

## Solución de problemas

**La visualización se quedó en blanco o dejó de actualizar**

La visualización se comunica en tiempo real con el terminal principal. Si la conexión se interrumpe, la visualización puede quedar en blanco o mostrar datos antiguos. Refresca el navegador en el dispositivo del cliente. Si eso no funciona, genera un nuevo código de emparejamiento y vuelve a emparejar.

**La visualización muestra el carrito del terminal equivocado**

Cada visualización está emparejada con un terminal específico. Si tienes múltiples terminales, asegúrate de haber generado el código de emparejamiento en el terminal correcto y de haberlo ingresado en la visualización. Para corregir un desajuste, genera un nuevo código en el terminal correcto y vuelve a emparejar el dispositivo de visualización.

**El código de emparejamiento expiró antes de que pudiera ingresarlo**

Los códigos son válidos durante 5 minutos. Genera un nuevo código desde la aplicación POS y ingrésalo en el dispositivo de visualización con prontitud. Mantén los dos dispositivos cerca durante el proceso de emparejamiento.

**Se ingresó el código de emparejamiento, pero la visualización no se conectó**

Verifica que el dispositivo del cliente pueda acceder a tu dominio de tienda (necesita acceso a la red). También verifica que `"customer_display": true` esté configurado en la configuración de hardware del terminal y que el terminal haya sido guardado.

**La URL de la visualización devuelve un error**

Asegúrate de que estés navegando a `/pos/display/` en tu dominio de tienda, no en la URL de administración. La vista de la visualización no requiere iniciar sesión — si se te pide que inicies sesión, verifica nuevamente la URL.

## Consejos

Mantén todo el formato de markdown, rutas de imágenes, bloques de código y términos técnicos.

- **Mantén la sesión de emparejamiento breve** — ten el dispositivo del cliente listo y el navegador abierto en `/pos/display/` antes de generar el código de emparejamiento.

Tienes 5 minutos, pero completarlo en menos de un minuto evita el tiempo de expiración.
- **Prueba antes de abrir** — completa una venta de prueba con el display conectado para verificar que los clientes verán los artículos y totales correctos antes de tu primera transacción real.
- **Guarda el URL del display como favorito** — configura el navegador del dispositivo del cliente para que abra `/pos/display/` al iniciar, para que siempre esté listo.
- **Usa escritorio extendido para simplicidad** — si tu terminal tiene un puerto HDMI adicional y un monitor disponible, el enfoque de escritorio extendido no requiere emparejamiento continuo y nunca expira.
- **Agrega diapositivas promocionales antes de abrir** — un display inactivo que muestra solo una pantalla de bienvenida en blanco es una oportunidad perdida.

Configura al menos un par de diapositivas promocionales para que el display sea útil incluso cuando no haya una venta en curso.

Consulta [Diapositivas promocionales del display del cliente](customer-display-promo-slides).
- **Protege el dispositivo del display** — el URL del display está diseñado para ser públicamente accesible, pero solo muestra datos de carrito en vivo cuando se empareja con un terminal activo.

Aun así, considera usar el modo de navegador de kiosco en el dispositivo del cliente para evitar que los clientes naveguen a otras páginas.