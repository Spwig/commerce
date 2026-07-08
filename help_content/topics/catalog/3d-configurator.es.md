---
title: Configurador 3D de productos
---

El Configurador 3D permite que tus clientes vean productos configurables en un visor 3D interactivo directamente en la página del producto. A medida que los clientes seleccionan opciones, como colores, materiales o variaciones de componentes, el modelo 3D se actualiza en tiempo real para reflejar sus elecciones. En dispositivos móviles compatibles, los clientes también pueden ver el producto en realidad aumentada (AR), colocándolo virtualmente en su propio espacio antes de comprar.

El Configurador 3D funciona con productos configurables. Cada producto configurable puede tener una configuración de escena 3D que vincule un archivo de modelo GLB con las opciones de configuración del producto.

## Antes de comenzar

Para configurar una escena 3D, necesitas:

- Un **producto configurable** ya creado en tu catálogo
- Un **modelo 3D base** cargado en tu Biblioteca de medios como un archivo GLB — este es el modelo ensamblado que aparece por defecto
- Opcionalmente, archivos GLB adicionales para intercambios de geometría (por ejemplo, formas de cuello diferentes), y imágenes de textura para variaciones de materiales

Si aún no has creado el producto configurable y sus opciones de configuración, hazlo primero antes de configurar la escena 3D.

## Crear una configuración de escena

1. Navega a **Catálogo > Configuraciones de escena 3D**
2. Haz clic en **+ Añadir configuración de escena 3D**
3. Selecciona el **Producto** al que pertenece esta escena — solo están disponibles productos configurables
4. Elige el **Modelo 3D base** de tu Biblioteca de medios — este es el archivo GLB que se carga por defecto
5. Configura la configuración del visor (ver más abajo)
6. Guarda el registro

Después de guardar, el campo **Árbol de nodos** se rellena automáticamente. Este es el gráfico de escena analizado extraído de tu archivo GLB — enumera cada nodo con nombre dentro del modelo, que harás referencia cuando agregues mapeos de nodos.

## Configuración del visor

Estas configuraciones controlan cómo aparece el visor 3D en tu página de producto.

### Cámara y iluminación

| Campo | Descripción | Valor predeterminado |
|-------|-------------|---------|
| **Orbita de la cámara** | Posición inicial de la cámara en el formato `ángulo elevación distancia` (por ejemplo, `0deg 75deg 2m`) | `0deg 75deg 2m` |
| **Punto de enfoque de la cámara** | El punto al que la cámara mira, en metros desde el centro del modelo (por ejemplo, `0m 0m 0m`) | `0m 0m 0m` |
| **Imagen del entorno** | Una imagen HDR de tu Biblioteca de medios utilizada para la iluminación basada en imágenes — da reflejos y sombras más realistas | Ninguna |
| **Exposición** | Brillo general de la escena — valores más bajos son más oscuros, valores más altos son más brillantes | `1.0` |

### Sombras

| Campo | Descripción | Valor predeterminado |
|-------|-------------|---------|
| **Intensidad de la sombra** | Cuán fuerte es la sombra proyectada debajo del modelo — `0` no hay sombra, `1` es intensidad completa | `0.5` |
| **Dureza de la sombra** | Cuán borrosos son los bordes de la sombra — `0` es nítido, `1` es muy suave | `0.5` |

### Corrección de color

| Campo | Descripción |
|-------|-------------|
| **Mapa de tonos** | El algoritmo de corrección de color aplicado a la escena. **Comercio** produce colores vibrantes y amigables para productos. **Neutro** es preciso en colores. **ACES** da un aspecto cinematográfico de película. |
| **Fuerza del brillo** | Añade un efecto de brillo a las partes emisoras (iluminadas por sí mismas) del modelo. `0` desactiva el brillo. Los valores entre `1` y `5` producen un brillo sutil a dramático. |

### Comportamiento y fondo

| Campo | Descripción | Valor predeterminado |
|-------|-------------|---------|
| **Rotación automática** | Si el modelo gira lentamente al cargar para llamar la atención del cliente | Activado |
| **AR habilitado** | Si los clientes en dispositivos compatibles ven un botón **Ver en AR** | Activado |
| **Fondo** | El color de fondo o gradiente CSS del visor — ingresa un color hexadecimal (por ejemplo, `#f5f5f5`) o un valor de gradiente CSS | `#ffffff` |

### Miniatura

El campo **Miniatura** contiene una captura de pantalla previa del visor 3D, mostrada antes de que se cargue el visor. Puedes capturar una captura de pantalla desde la página del producto en vivo y subirla a tu Biblioteca de medios, luego vincularla aquí para una experiencia de carga de página más suave.

## Habilitar y deshabilitar el visor 3D

El interruptor **Habilitado** controla si el visor 3D se muestra en la página del producto.

Cuando está deshabilitado, el producto recurre al configurador de imágenes 2D estándar.

Esto le permite preparar una configuración de escena antes de hacerla visible para los clientes.

## Conectar opciones de configuración a acciones 3D

Una vez que la escena base está configurada, puede vincular cada opción de configuración a un cambio visual en el modelo 3D. Estos vínculos se llaman **Node Mappings** y se agregan en la sección **Node Mappings** en la parte inferior del formulario de configuración de la escena.

### Campos de mapeo de nodos

| Campo | Descripción |
|-------|-------------|
| **Opción de ranura** | La opción de configuración que desencadena este cambio (por ejemplo, "Cuero rojo") |
| **Tipo de acción** | Qué cambio visual ocurre (vea los tipos de acción a continuación) |
| **Nodo objetivo** | El nombre del nodo del árbol de escena que cambia — elija entre los nombres enumerados en su **Árbol de nodos** |
| **Datos de acción** | Datos específicos de la acción, como un código de color en hexadecimales, una URL de textura o una URL de archivo GLB |
| **Orden de clasificación** | Controla el orden en el que se aplican múltiples mapeos para la misma opción |

### Tipos de acción

| Acción | Qué hace |
|--------|-------------|
| **Color de material** | Cambia el color de un material en el nodo objetivo — proporcione un color en hexadecimales en **Datos de acción** |
| **Textura de material** | Intercambia la textura aplicada a un material — vincule a una imagen de textura en **Datos de acción** |
| **Intercambio de geometría** | Reemplaza una parte del modelo con un archivo GLB diferente — útil para cambios estructurales como una forma diferente de mango |
| **Visibilidad** | Muestra o oculta un nodo en la escena — establezca `visible: true` o `visible: false` en **Datos de acción** |

Se pueden agregar múltiples mapeos para una sola opción de ranura. Por ejemplo, seleccionar "Azul vaquero" podría cambiar el color del material *y* ocultar un nodo de cuero al mismo tiempo.

## Activos de geometría

Si su configuración incluye acciones de **Intercambio de geometría**, debe registrar los archivos GLB de reemplazo como Activos de geometría. Estos se agregan en la sección **Activos de geometría** del formulario de configuración de la escena.

| Campo | Descripción |
|-------|-------------|
| **Etiqueta** | Nombre descriptivo para este activo de geometría, por ejemplo, "Cuello en V" |
| **Archivo GLB** | El archivo GLB de reemplazo de su Biblioteca de medios |
| **Nodo objetivo** | ¿Qué nodo en el modelo base este activo de geometría reemplaza? |

Después de guardar un activo de geometría, los nombres de los nodos se analizan desde el GLB y se almacenan en **Datos de nodo**, haciendo que estén disponibles como nodos objetivo en sus mapeos.

## Activos de textura

Las imágenes de textura utilizadas en los mapeos de **Textura de material** pueden registrarse como Activos de textura para una referencia más fácil. Estos se agregan en la sección **Activos de textura**.

| Campo | Descripción |
|-------|-------------|
| **Etiqueta** | Nombre descriptivo, por ejemplo, "Cuero rojo" |
| **Imagen de textura** | La imagen de textura de su Biblioteca de medios |
| **Tipo de textura** | El canal PBR al que se aplica esta textura — Color base, Mapa normal, Mapa de rugosidad, Mapa de metalicidad, Occlusión ambiental o Mapa emisor |

## Ejemplo: chaqueta configurable con opciones de color

**Escenario:** Una chaqueta que se puede pedir en Negro, Azul marino o Burdeos, con cada color aplicado a la malla del cuerpo de la chaqueta.

**Configuración:**

1. Cree una configuración de escena para el producto de chaqueta con el archivo GLB de la chaqueta ensamblada como modelo base
2. Establezca **Tone Mapping** en Commerce y **Auto Rotate** en encendido
3. En Node Mappings, agregue tres entradas — una por opción de color:

| Opción de ranura | Tipo de acción | Nodo objetivo | Datos de acción |
|----------------|---------------|---------------|----------------|
| Negro | Color de material | JacketBody | `{"color": "#1a1a1a"}` |
| Azul marino | Color de material | JacketBody | `{"color": "#1b2a4a"}` |
| Burdeos | Color de material | JacketBody | `{"color": "#6b2737"}` |

Cuando un cliente selecciona Azul marino en la página del producto, el visor actualiza instantáneamente el material de JacketBody al color azul marino.

## Consejos

Conservar todo el formato de markdown, rutas de imagen, bloques de código y términos técnicos.

- Asigne nombres claros a sus nodos GLB al crear su modelo 3D — nombres de nodos como "JacketBody" o "CollarMesh" son mucho más fáciles de trabajar que nombres generados automáticamente como "Mesh_023"
- Use el mapeo de tonos **Commerce** para la mayoría de los productos — está ajustado para una presentación de productos vibrante y atractiva
- Désablele **Auto Rotate** para productos donde el ángulo de cámara predeterminado ya muestra las características más importantes, para evitar desorientar al cliente al cargar
- Pruebe el botón de AR en un dispositivo móvil real antes de promocionarlo — la disponibilidad de AR depende del dispositivo y navegador del cliente (iOS Safari y Android Chrome con soporte WebXR son los más confiables)
- Suba una imagen de **Thumbnail** para cada configuración de escena — esto evita que aparezca una caja blanca en blanco mientras se carga el visor 3D
- Si el visor 3D aún no está listo, desactívelo con el interruptor **Enabled** para que los clientes vean el configurador de imágenes estándar en su lugar