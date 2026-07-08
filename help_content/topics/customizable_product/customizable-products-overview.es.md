---
title: Productos personalizables
---

Los productos personalizables permiten a tus clientes diseñar sus propios productos utilizando un editor visual directamente en tu tienda en línea. Ya sea que vendas camisetas personalizadas, carteles personalizados, mercancía con marca o tarjetas de felicitación, esta función le da a los clientes las herramientas para agregar texto, subir imágenes y usar imágenes clipart para crear diseños únicos — todo sin salir de tu tienda.

## Cómo funciona

Un producto personalizable combina un producto estándar de Spwig con un **editor de diseño visual**. Tú defines las superficies diseñables del producto (como la parte delantera y trasera de una camiseta), subes imágenes de previsualización para que los clientes vean su diseño en contexto, y estableces las reglas sobre lo que los clientes pueden hacer en cada superficie.

Cuando un cliente visita un producto personalizable en tu tienda en línea, ven un editor de lienzo en vivo superpuesto en la imagen de previsualización del producto. Pueden agregar texto, subir sus propias imágenes y navegar por tu biblioteca de imágenes clipart para construir su diseño. El editor muestra el diseño exactamente como se verá en el producto terminado.

### Dos casos de uso

Los productos personalizables funcionan bien en dos escenarios comunes:

| Caso de uso | Ejemplo | Superficies | Configuración típica |
|-------------|---------|------------|---------------------|
| **Diseño de ropa** | Camisetas personalizadas, sudaderas, bolsas de compras | Múltiples (delantera, trasera, mangas) | Fuente en negrita, imágenes clipart de humor/deportes, restricciones por superficie |
| **Diseño de impresión** | Carteles, tarjetas de felicitación, tarjetas de negocios | Única (solo delantera) | Alta resolución, configuraciones de sangrado, fuentes elegantes, bordes decorativos |

El proceso de configuración es el mismo para ambos — la diferencia radica en cuántas superficies defines, qué imágenes clipart y fuentes proporcionas, y cómo configuras las opciones de impresión.

## Conceptos clave

### Configuración del diseño

Cada producto personalizable tiene una **configuración del diseño** que controla el comportamiento general del editor: qué herramientas están disponibles (texto, subida de imágenes, imágenes clipart), límites de subida y reglas de precios. Este es el panel de control principal para el editor de diseño del producto.

### Superficies

Una **superficie** es una cara diseñable de tu producto. Una camiseta típicamente tiene tres superficies (delantera, trasera, manga), mientras que un cartel tiene solo una. Cada superficie tiene su propia imagen de previsualización, posición del área de diseño, dimensiones físicas y configuraciones de calidad de impresión.

### Área de diseño

El **área de diseño** es el área rectangular en la imagen de previsualización donde los clientes pueden colocar sus elementos de diseño. Colocas esta zona visualmente en la página de configuración del administrador arrastrándola y redimensionándola sobre la imagen de previsualización. La zona define dónde aparecerán los diseños en el producto terminado.

### Plantillas

Las **plantillas de diseño** son diseños prehechos que creas para los clientes. En lugar de comenzar desde un lienzo en blanco, los clientes pueden navegar por tu galería de plantillas, elegir una que les guste y personalizarla. Las plantillas pueden incluir elementos bloqueados que los clientes no pueden modificar — por ejemplo, un logotipo de la empresa que siempre debe aparecer en la misma posición.

### Imágenes clipart y fuentes

Construyes una **biblioteca de imágenes clipart** de imágenes que los clientes pueden agregar a sus diseños, organizadas en categorías (por ejemplo, "Deportes", "Bordes", "Vacaciones"). También puedes subir **fuentes personalizadas** además de las fuentes del sistema estándar, ofreciendo a los clientes más opciones creativas.

### Precios

El editor de diseño admite un modelo de precios flexible con cuatro componentes de tarifa:

| Tipo de tarifa | Descripción |
|----------------|-------------|
| **Tarifa base de diseño** | Tarifa plana agregada cuando se aplica cualquier personalización |
| **Tarifa por superficie** | Tarifa adicional por cada superficie utilizada más allá de la primera |
| **Tarifa por subida** | Tarifa por cada imagen subida por el cliente |
| **Tarifa por texto** | Tarifa por cada elemento de texto agregado |

Los precios se actualizan en tiempo real a medida que el cliente agrega elementos, por lo que no hay sorpresas al momento del pago.

## Modos del editor

Spwig ofrece dos modos del editor:

- **Editor de lienzo** — Un editor de diseño visual completo con un lienzo en vivo, herramientas de texto, subida de imágenes, navegador de imágenes clipart y vista previa en tiempo real en la imagen de previsualización del producto.

# Modo recomendado para la mayoría de los productos personalizables

Este es el modo recomendado para la mayoría de los productos personalizables.
- **Formulario simple** — Un enfoque basado en formularios tradicionales donde los clientes completan campos de texto y suben imágenes sin un lienzo visual.

Adecuado para productos con personalización mínima (por ejemplo, grabar un nombre en una pieza de joyería).

## Flujo de trabajo del comerciante

Configurar un producto personalizable sigue este flujo de trabajo:

1. **Crear el producto** — Agregar un nuevo producto con el tipo establecido en **Producto personalizable**
2. **Configurar superficies** — Definir cada cara diseñable, cargar imágenes de maquetas y posicionar las zonas de diseño
3. **Configurar ajustes** — Elegir qué herramientas habilitar, establecer límites de carga y configurar el precio
4. **Agregar activos** — Construir tu biblioteca de imágenes y cargar fuentes personalizadas
5. **Crear plantillas** — Diseñar puntos de inicio prehechos con controles de bloqueo opcionales
6. **Probar y publicar** — Previsualizar el editor en la tienda y verificar que todo funcione

Para instrucciones detalladas de configuración, consulte [Configuración de un Producto Personalizable](/admin/customizable-product/).

## Experiencia del cliente

Cuando un cliente visita un producto personalizable en su tienda:

1. **Explorar plantillas** — Pueden comenzar desde una plantilla prehecha o empezar con un lienzo en blanco
2. **Cambiar superficies** — Las pestañas en la parte superior les permiten cambiar entre superficies (por ejemplo, frente y espalda de una camiseta)
3. **Añadir elementos** — El panel de herramientas proporciona herramientas de texto, carga de imágenes y imágenes clipart
4. **Personalizar** — Pueden ajustar fuentes, colores, tamaños, posiciones y aplicar filtros de imagen
5. **Ver precios** — La tarifa de diseño se actualiza en tiempo real a medida que añaden elementos
6. **Guardar diseños** — Los clientes registrados pueden guardar diseños para continuar editando más tarde
7. **Añadir al carrito** — El diseño se vincula al elemento del carrito y se congela cuando se coloca el pedido

## ¿Qué ocurre después de realizar un pedido

Cuando un cliente coloca un pedido que contiene un producto personalizado:

- El diseño se **congela como una captura de pantalla** — no se puede modificar después de la compra
- El sistema genera **archivos de cumplimiento de alta resolución** para cada superficie
- Puedes descargar estos archivos listos para imprimir desde la página de detalles del pedido en tu panel de administración
- Los archivos se renderizan a la DPI que configuraste para cada superficie

Para obtener detalles sobre el cumplimiento de pedidos personalizados, consulte [Cumplimiento de Pedidos de Productos Personalizables](/admin/orders/).

## Consejos

- Comienza con un producto simple (una superficie, como un póster) para aprender el proceso de configuración antes de abordar productos de múltiples superficies como camisetas.
- Carga imágenes de maquetas de alta calidad — son la primera cosa que ven los clientes y establecen la expectativa de calidad para toda la experiencia.
- Crea 3-5 plantillas de diseño para cada producto para reducir la intimidación del "lienzo en blanco" e inspirar a los clientes.
- Usa restricciones por superficie para controlar lo que los clientes pueden hacer en cada superficie. Por ejemplo, permite solo la carga de un logotipo pequeño en la manga de una camiseta, mientras que permite una libertad total de diseño en la parte frontal.
- Establece requisitos mínimos de DPI adecuados para tu método de impresión — 150 DPI para impresión en serigrafía, 300 DPI para impresión digital de alta calidad.
- Prueba el flujo completo del cliente (diseño, guardar, añadir al carrito, checkout) antes de publicar un producto personalizable.