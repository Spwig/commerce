---
title: Configuración de un producto personalizable
---

Esta guía le guía a través del proceso completo de configuración de un producto personalizable, desde la creación del producto hasta la configuración de superficies, precios y restricciones de carga. Se utilizan dos ejemplos prácticos a lo largo del documento: una **camiseta personalizada** (prendido de múltiples superficies) y un **cartel personalizado** (impresión de una sola superficie).

## Paso 1: Crear el producto

1. Navegue a **Productos > Todos los productos** y haga clic en **+ Agregar producto**
2. Establezca **Tipo de producto** en **Producto personalizable**
3. Rellene el nombre del producto, descripción, imágenes y precios como lo haría para cualquier producto
4. Guarde el producto

Después de guardar, aparece un nuevo botón **Abrir editor de diseño** en el formulario del producto. Esto lo lleva a la página dedicada de configuración donde configura el editor de diseño visual.

## Paso 2: Acceder a la configuración del editor de diseño

1. Abra el producto que acaba de crear en el administrador
2. Haga clic en el botón **Abrir editor de diseño** (en la sección Producto personalizable)
3. La página de configuración se abre con tres pestañas: **Superficies**, **Configuración** y **Precios**

La página de configuración es donde define todo sobre el editor de diseño para este producto.

## Paso 3: Agregar superficies de diseño

Una superficie representa una cara diseñable de su producto. Haga clic en **+ Agregar superficie** para crear cada superficie.

### Ejemplo de camiseta: 3 superficies

| Superficie | Nombre | Dimensiones | Zona de diseño | Notas |
|-----------|--------|-------------|----------------|-------|
| 1 | Frente | 300 x 400 mm | Área central del pecho | Área principal de diseño |
| 2 | Detrás | 300 x 400 mm | Área superior de la espalda | Área secundaria de diseño |
| 3 | Manga izquierda | 100 x 100 mm | Área superior del brazo | Solo área para logotipo pequeño |

### Ejemplo de cartel: 1 superficie

| Superficie | Nombre | Dimensiones | Zona de diseño | Notas |
|-----------|--------|-------------|----------------|-------|
| 1 | Frente | 210 x 297 mm (A4) | Área imprimible completa | Una sola superficie, alta resolución |

### Configuración de cada superficie

Para cada superficie, configure lo siguiente:

**Información básica:**
- **Nombre** — Lo que ven los clientes en las pestañas de la superficie (por ejemplo, "Frente", "Detrás")
- **Slug** — Identificador seguro para URL, generado automáticamente a partir del nombre
- **Orden de clasificación** — Controla el orden en que aparecen las superficies (los números más bajos primero)

**Imagen de previsualización:**
- Haga clic en el área de imagen de previsualización para abrir la Biblioteca de medios y seleccionar una foto del producto que muestre esta superficie
- Use una foto de alta calidad de su producto desde el ángulo correcto

**Posicionamiento de la zona de diseño:**
- Después de seleccionar una imagen de previsualización, aparece un recuadro superpuesto en la vista previa
- **Arrastre** el recuadro para posicionar donde debe estar la zona de diseño en la previsualización
- **Redimensione** el recuadro arrastrando sus bordes para definir los límites de la zona de diseño
- La zona se almacena como coordenadas basadas en porcentaje, por lo que se escala a cualquier tamaño de pantalla

La zona de diseño le dice al editor exactamente dónde en la imagen del producto aparecerá el diseño del cliente. Posicíonela cuidadosamente para coincidir con el área imprimible real de su producto.

**Dimensiones físicas:**
- **Ancho** y **Altura** — Las dimensiones reales del área de diseño
- **Unidad** — Milímetros, pulgadas o píxeles
- Estas dimensiones determinan la proporción del lienzo de diseño y se usan para calcular la resolución de impresión DPI

**Configuración de impresión:**
- **DPI mínimo** — La resolución mínima aceptable en puntos por pulgada. Los clientes ven una advertencia si sus imágenes cargadas son inferiores a esta. Valor predeterminado: 150
- **DPI recomendado** — La resolución ideal para la mejor calidad de impresión. Valor predeterminado: 300
- **Bleed (mm)** — Márgen adicional fuera del área de diseño para la impresión de bleed. Establezca en 0 si no se necesita bleed (común en prendas), o 3 mm para productos de impresión profesional
- **Máximo de colores** — Para la impresión en serigrafía, puede limitar el número de colores. Deje en blanco para ilimitado (impresión digital)
- **Color de fondo** — Color de fondo predeterminado del lienzo

### Configuración de impresión para camiseta vs cartel

| Configuración | Camiseta | Cartel |
|---------------|--------|--------|
| DPI mínimo | 150 | 200 |
| DPI recomendado | 300 | 300 |
| Bleed | 0 mm | 3 mm |
| Máximo de colores | 6 (serigrafía) | Vacío (ilimitado) |
| Color de fondo | Coincida con el color de la prenda | `#ffffff` (blanco) |

## Paso 4: Restricciones por superficie

Cada superficie puede anular las configuraciones globales de características. Esto le permite permitir herramientas diferentes en superficies diferentes.

Las opciones de restricción son:

| Configuración | Opciones | Descripción |
|---------|---------|-------------|
| **Permitir texto** | Heredar / Sí / No | ¿Los clientes pueden agregar texto en esta superficie? |
| **Permitir carga de imagen** | Heredar / Sí / No | ¿Los clientes pueden cargar imágenes a esta superficie? |
| **Permitir clipart** | Heredar / Sí / No | ¿Los clientes pueden usar clipart en esta superficie? |
| **Máximo de elementos** | Número o en blanco | Número máximo de elementos de diseño permitidos en esta superficie |

Cuando se establece en **Heredar**, la superficie usa lo configurado en la configuración global (Paso 6). Cuando se establece en **Sí** o **No**, anula la configuración global para esa superficie específica.

### Ejemplo: Restricción de manga de camiseta

Para la superficie de la manga de la camiseta, podría desear restringir la personalización solo a un logotipo pequeño:

| Configuración | Valor | Razón |
|---------|-------|--------|
| Permitir texto | No | Demasiado pequeño para texto legible |
| Permitir carga de imagen | Sí | Permitir carga de un logotipo pequeño |
| Permitir clipart | No | Mantenerlo simple |
| Máximo de elementos | 1 | Solo un logotipo |

Las superficies delantera y trasera permanecerían configuradas en **Heredar**, permitiendo todas las herramientas según se definió en la configuración global.

### Ejemplo: Restricción de póster

Para un póster, normalmente todas las superficies heredan de la configuración global, ya que solo hay una superficie y todas las herramientas deben estar disponibles. No se necesitan anulaciones por superficie.

## Paso 5: Configurar restricciones de carga

En la pestaña **Configuración**, configure cómo los clientes pueden cargar archivos:

| Configuración | Descripción | Ejemplo de camiseta | Ejemplo de póster |
|---------|-------------|-----------------|----------------|
| **Tamaño máximo de carga** | Tamaño máximo de archivo por carga | 10 MB | 20 MB |
| **Máximo de cargas por superficie** | ¿Cuántas imágenes por superficie? | 5 | 3 |
| **Tipos de carga permitidos** | Formatos de archivo aceptados | JPG, PNG, WebP | JPG, PNG, WebP |

Se recomienda un límite de tamaño de archivo más grande para productos de impresión donde los clientes necesiten cargar imágenes de alta resolución.

## Paso 6: Configuración del editor

En la pestaña **Configuración**, configure el comportamiento global del editor:

**Modo del editor:**
- **Editor de lienzo** — Editor visual completo con vista previa en vivo del lienzo. Recomendado para la mayoría de los productos.
- **Formulario simple** — Campos de formulario tradicionales para personalización básica (por ejemplo, solo texto grabado).

**Conmutadores de características (valores globales por defecto):**
- **Permitir texto** — Permitir que los clientes agreguen elementos de texto
- **Permitir carga de imagen** — Permitir que los clientes carguen sus propias imágenes
- **Permitir clipart** — Permitir que los clientes naveguen y usen su biblioteca de clipart

Estas configuraciones globales se aplican a todas las superficies, a menos que se anulen con restricciones por superficie (Paso 4).

## Paso 7: Configurar precios

En la pestaña **Precios**, establezca las tarifas de diseño que se agregan al precio base del producto:

| Tarifa | Descripción |
|-----|-------------|
| **Tarifa de diseño base** | Tarifa plana agregada cuando se aplica cualquier personalización |
| **Tarifa por superficie** | Tarifa adicional por cada superficie utilizada más allá de la primera |
| **Tarifa por carga** | Tarifa por cada imagen cargada por el cliente |
| **Tarifa por texto** | Tarifa por cada elemento de texto agregado |

### Ejemplo: Precios de camiseta

| Tarifa | Cantidad | Razonamiento |
|-----|--------|-----------|
| Tarifa de diseño base | $5.00 | Cubre el costo de configuración para cualquier pedido personalizado |
| Tarifa por superficie | $2.00 | Cada superficie adicional agrega un costo de impresión |
| Tarifa por carga | $1.00 | Las imágenes personalizadas requieren procesamiento |
| Tarifa por texto | $0.50 | El texto es más sencillo de producir que las imágenes |

**Ejemplo de cálculo:** Un cliente diseña una camiseta con texto en la parte delantera y un logotipo en la parte trasera:
- Tarifa de diseño base: $5.00
- 1 superficie adicional (trasera): $2.00
- 1 logotipo cargado: $1.00
- 1 elemento de texto: $0.50
- **Tarifa de diseño total: $8.50** (agregada al precio base del producto)

### Ejemplo: Precios de póster


| Tarifa | Monto | Rationale |
|-----|--------|-----------|
| Tarifa de Diseño Básico | $0.00 | No hay tarifa básica — el precio del producto la cubre |
| Tarifa por Superficie | $0.00 | Una sola superficie, no aplica |
| Tarifa por Carga | $2.00 | Procesamiento de alta resolución |
| Tarifa por Texto | $0.00 | El texto está incluido en la experiencia básica |

**Ejemplo de cálculo:** Un cliente crea un póster con 2 fotos cargadas y 3 elementos de texto:
- Tarifa de diseño básico: $0.00
- 2 fotos cargadas: $4.00
- 3 elementos de texto: $0.00
- **Tarifa total de diseño: $4.00**

La tarifa de diseño se muestra a los clientes en tiempo real mientras agregan elementos, por lo que pueden ver el impacto de costo de cada adición antes de agregar al carrito.

## Comparación de configuración a primera vista

| Aspecto | Camiseta personalizada | Póster personalizado |
|--------|---------------|---------------|
| Superficies | 3 (delante, detrás, manga) | 1 (delante) |
| Imágenes de previsualización | 3 fotos del producto | 1 foto del producto |
| Posicionamiento de zonas | Áreas del pecho/detrás/brazo | Área imprimible completa |
| Dimensiones | 300x400mm, 100x100mm | 210x297mm (A4) |
| DPI mínimo | 150 | 200 |
| Sangrado | 0 mm | 3 mm |
| Máximo de colores | 6 | Ilimitado |
| Restricciones por superficie | Manga restringida | Ninguna necesaria |
| Modelo de precios | Básico + superficie + carga + texto | Solo tarifas por carga |

## Consejos

- Siempre prueba el editor de diseño desde la perspectiva del cliente después de completar la configuración. Visita la página del producto en la tienda y prueba agregar texto, cargar una imagen y cambiar de superficies.
- Carga imágenes de previsualización que se acerquen al aspecto real del producto. Para camisetas, fotografa cada ángulo por separado. Para pósters, usa una foto plana limpia o una previsualización en marco.
- Posiciona la zona de diseño de forma conservadora — es mejor definir una zona ligeramente más pequeña que tener diseños que impriman en costuras o bordes.
- Establece el DPI mínimo según tu método de impresión: 150 para impresión en serigrafía, 200 para impresión digital estándar, 300 para impresión offset de alta calidad.
- Usa 3 mm de sangrado para cualquier producto que se recorte después de la impresión (pósters, tarjetas de negocios, folletos). Establece el sangrado en 0 para productos donde el diseño se aplica a una superficie existente (camisetas, tazas, fundas para teléfonos).
- Comienza con un precio simple y ajusta según la retroalimentación del cliente. Muchos comerciantes comienzan con solo una tarifa de diseño básica y agregan tarifas por elemento más tarde.