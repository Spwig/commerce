---
title: Cumplimiento de pedidos de productos personalizables
---

Cuando un cliente diseña un producto y coloca un pedido, su diseño se congela y se almacena junto con el pedido. Esta guía explica cómo los diseños personalizados fluyen a través del ciclo de vida del pedido y cómo acceder a los archivos listos para imprimir que necesita para el cumplimiento.

## Ciclo de vida del diseño

El diseño de un cliente pasa por varias etapas desde su creación hasta su cumplimiento:

### 1. Creación del diseño

El cliente utiliza el editor visual en la tienda para crear su diseño. Mientras trabajan, su progreso se guarda automáticamente en el navegador. Los clientes registrados también pueden guardar diseños en su cuenta para editarlos más tarde.

### 2. Borrador del diseño

Cuando el cliente hace clic en **Añadir al carrito**, el estado actual del diseño se guarda como **borrador de diseño**. El borrador incluye:

- El estado completo del lienzo para cada superficie (posiciones de elementos, contenido de texto, imágenes subidas, elementos gráficos, estilos)
- Un desglose de precios que muestra todas las tarifas aplicables del diseño
- Previsualizaciones en miniatura de cada superficie

El borrador se vincula al elemento del carrito mediante un token único. Esto garantiza que el diseño exacto que creó el cliente se preserve incluso si continúan comprando antes de finalizar la compra.

**Caducidad del borrador:** Los borradores de diseño caducan automáticamente después de 7 días si el cliente no completa el pedido. Esto evita la acumulación de diseños abandonados.

### 3. Captura del diseño

Cuando el cliente completa el proceso de pago y se coloca el pedido, el borrador de diseño se convierte en una **captura de diseño inmutable**. Esta es el registro permanente del diseño:

- La captura no puede ser modificada por el cliente después de la compra
- Contiene exactamente los mismos datos de diseño que el borrador
- Está permanentemente vinculada al elemento específico del pedido

Esta inmutabilidad es importante — garantiza que lo que el cliente ordenó sea exactamente lo que produces y envías, sin posibilidad de cambios después del pago.

### 4. Generación de archivos para cumplimiento

Después de que se coloca el pedido, el sistema genera automáticamente **archivos de cumplimiento de alta resolución** para cada superficie del diseño. Estos son imágenes compuestas que combinan todos los elementos del diseño (texto, imágenes, elementos gráficos) en un solo archivo listo para imprimir a la resolución en DPI configurada para cada superficie.

La generación ocurre de forma asincrónica en segundo plano. Para la mayoría de los diseños, la generación se completa en unos pocos segundos. El estado **Renderizado** de la captura indica si los archivos de cumplimiento están listos.

## Acceso a los datos del diseño en los pedidos

### Página de detalles del pedido

Cuando ves un pedido que contiene productos personalizables en el panel de administración:

1. Navega a **Pedidos > Todos los pedidos**
2. Abre el pedido que contiene el producto personalizado
3. El elemento del pedido del producto personalizable muestra la información del diseño, incluyendo previsualizaciones de superficies y un enlace a la captura del diseño

### Lista de capturas de diseño

También puedes navegar por todas las capturas de diseño directamente:

1. Navega a **Productos personalizables > Capturas de diseño**
2. La lista muestra todas las capturas vinculadas a elementos de pedido
3. Haz clic en una captura para ver los datos completos del diseño, imágenes renderizadas y archivos de cumplimiento

Cada captura muestra:

| Campo | Descripción |
|-------|-------------|
| **Elemento del pedido** | Enlace al elemento del pedido asociado |
| **Datos del diseño** | El estado completo del lienzo (JSON) |
| **Imágenes renderizadas** | Miniaturas de previsualización por superficie |
| **Archivos de cumplimiento** | Archivos compuestos de alta resolución para imprimir |
| **Renderizado** | Si el renderizado está completo |
| **Renderizado completado en** | Marca de tiempo de cuando se generaron los archivos |

## Descargar archivos de cumplimiento

Los archivos de cumplimiento son los que envías a tu proveedor de impresión o usas en tu proceso de producción.

**Para un pedido de camiseta personalizada:**
- Descarga el archivo de la superficie **Delante** (por ejemplo, imagen compuesta PNG a 300 DPI)
- Descarga el archivo de la superficie **Detrás**
- Descarga el archivo de la superficie **Brazo** (si se diseñó)
- Envía todos los archivos a tu impresor de pantalla o a tu impresor DTG (directo a prendas)



**Para un pedido de póster personalizado:**
- Descargue el archivo de la superficie **Front** en resolución de impresión
- El archivo incluye área de sangrado si se configuró sangrado para la superficie
- Envíelo a su impresor de pósters/tarjetas

Cada archivo es una sola imagen compuesta que contiene todos los elementos del diseño fusionados, renderizados a la DPI que configuró para esa superficie.

## Diseños guardados

Los clientes registrados pueden guardar sus diseños en su cuenta para editarlos más tarde. Como comerciante, puede ver estos diseños guardados en una lista de solo lectura:

1. Navegue hasta **Productos personalizables > Diseños guardados**
2. La lista muestra todos los diseños guardados por el cliente con el nombre del cliente, producto, nombre del diseño y fecha

Los diseños guardados son:
- **Propios del cliente** — Pertenecen a la cuenta del cliente
- **Solo lectura para comerciantes** — Puede verlos pero no modificarlos
- **Separados de los pedidos** — Un diseño guardado solo se convierte en un pedido cuando el cliente lo agrega al carrito y finaliza la compra
- **Reutilizables** — Los clientes pueden cargar un diseño guardado, modificarlo y pedirlo varias veces

## Flujo de cumplimiento

### Flujo de trabajo estándar

1. **Recibir pedido** — El pedido aparece en su lista de pedidos con los artículos personalizados
2. **Verificar renderizado** — Compruebe que la captura del diseño muestre **Renderizado: Sí**. Si el renderizado aún no se ha completado, espere unos minutos y actualice
3. **Descargar archivos** — Descargue el archivo de cumplimiento para cada superficie diseñada
4. **Revisar calidad** — Abra los archivos y verifique que el diseño cumpla con sus estándares de calidad de impresión (verifique la DPI, la posición de los elementos y la legibilidad del texto)
5. **Enviar a producción** — Envíe los archivos a su proveedor de impresión o equipo de producción
6. **Enviar y completar** — Después de la producción, envíe el producto y marque el pedido como cumplido

### Ejemplo de cumplimiento de camisetas

1. Pedido recibido: "Camiseta de equipo personalizada" con diseños en la parte delantera y trasera
2. Abrir pedido → ver captura del diseño
3. Descargar `front.png` (300 DPI, 300x400mm) y `back.png` (300 DPI, 300x400mm)
4. Envíe ambos archivos a su impresora DTG con el color de la prenda y el tamaño seleccionados en la variante del pedido
5. Después de la impresión y revisión de calidad, envíe al cliente

### Ejemplo de cumplimiento de pósters

1. Pedido recibido: "Póster personalizado A4" con una sola superficie diseñada
2. Abrir pedido → ver captura del diseño
3. Descargar `front.png` (300 DPI, 210x297mm con 3mm de sangrado)
4. Envíelo a su servicio de impresión de pósters
5. Después de la impresión y recorte, envíelo al cliente

## Solución de problemas

**Problema:** La captura del diseño muestra "Renderizado: No" y el renderizado aún no se ha completado

- **Causa:** La tarea de renderizado en segundo plano podría haber fallado o aún está en proceso
- **Solución:** Espere unos minutos. Si el renderizado no se completa, revise los registros de las tareas en segundo plano. También puede ver los datos del diseño directamente en la captura para confirmar que el diseño del cliente se ha conservado

**Problema:** El archivo de cumplimiento parece de menor calidad de lo esperado

- **Causa:** El cliente podría haber subido imágenes de baja resolución
- **Solución:** Revise la configuración de DPI de la superficie. Si se configuraron advertencias de DPI mínima, el cliente habría recibido una advertencia durante el proceso de diseño. Para futuros productos, considere aumentar el requisito de DPI mínimo

**Problema:** El cliente solicita un cambio en su diseño después de realizar el pedido

- **Solución:** Las capturas de diseño son inmutables por diseño. Si el cliente necesita cambios, debe realizar un nuevo pedido con el diseño actualizado. Si acepta hacer una excepción, el cliente puede usar su diseño guardado (si lo guardó) como punto de partida para un nuevo pedido

## Consejos

- Siempre verifique que el renderizado esté completo antes de iniciar la producción.

Verifique el campo **Renderizado** en la captura del diseño.
- Mantenga las configuraciones de DPI adecuadas para su método de impresión.

Una mayor DPI produce una mejor calidad pero tamaños de archivo más grandes. 300 DPI es estándar para la mayoría de los productos de impresión profesional.
- Incentive a los clientes a guardar sus diseños antes de realizar el pedido.

Consérvese todo el formato de markdown, rutas de imágenes, bloques de código y términos técnicos.

Si hay un problema en la producción y se necesita volver a realizar el pedido, el diseño guardado hace que el reordenar sea sencillo.
- Crea un margen en tu cronograma de producción para productos personalizables.

A diferencia de los productos estándar, cada artículo requiere un manejo de archivos individual.
- Si procesas altos volúmenes de pedidos personalizables, considera automatizar el paso de descarga de archivos integrando con la API de tu proveedor de impresión.