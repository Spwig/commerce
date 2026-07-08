---
title: "Productos Configurables"
---

Los productos configurables permiten a los clientes construir su propio producto eligiendo opciones de diferentes ranuras de configuracion. Esto es ideal para articulos hechos a pedido como PCs personalizadas, cajas de regalo personalizadas o muebles a medida donde cada componente es un producto real de tu catalogo.

![Product configurator admin](/static/core/admin/img/help/configurable-products/product-configurator.webp)

## Como Funciona

Un producto configurable esta compuesto por **ranuras** (categorias de opciones) y **opciones** (los productos reales que los clientes pueden elegir). Por ejemplo, una PC personalizada podria tener ranuras para Procesador, Tarjeta Grafica, RAM y Almacenamiento, cada ranura conteniendo varias opciones de producto para elegir.

## Estrategias de Precios

Elige como se calcula el precio final:

| Estrategia | Descripcion |
|------------|-------------|
| **Suma de Componentes** | Precio final = total de todos los precios de las opciones seleccionadas. No se necesita precio base. |
| **Precio Base + Ajustes** | Comienza con el precio base del producto, luego suma/resta ajustes de precio por opcion. |
| **Precio Fijo** | Un precio unico sin importar que opciones seleccione el cliente. |

## Configuracion de un Producto Configurable

### Paso 1: Crear el Producto

1. Navega a **Productos > Todos los Productos** y haz clic en **+ Agregar Producto**
2. Establece el **Tipo de Producto** como **Producto Configurable**
3. Elige tu **Estrategia de Precios** (Suma de Componentes es la mas comun)
4. Completa el nombre del producto, la descripcion y otros detalles basicos
5. Guarda el producto

### Paso 2: Agregar Ranuras de Configuracion

Despues de guardar, cambia a la pestana **Configuracion** para configurar tus ranuras.

1. Haz clic en **+ Agregar Ranura** para crear una nueva categoria de configuracion
2. Para cada ranura, configura:
   - **Nombre** — Lo que el cliente ve (ej., "Procesador", "Color")
   - **Icono** — Clase de icono Font Awesome para identificacion visual
   - **Requerido** — Si el cliente debe hacer una seleccion
   - **Selecciones Min/Max** — Cuantas opciones puede elegir el cliente (por defecto: exactamente 1)
   - **Orden** — Controla el orden en que las ranuras aparecen en el asistente de configuracion

### Paso 3: Agregar Opciones a Cada Ranura

Cada ranura necesita opciones de producto para que los clientes elijan:

1. Haz clic en **Gestionar Opciones** en una ranura
2. Busca y agrega productos existentes de tu catalogo
3. Para cada opcion, configura:
   - **Ajuste de Precio** — Cantidad a sumar o restar (usado con la estrategia de Precio Base + Ajustes)
   - **Predeterminado** — Preseleccionar esta opcion cuando se carga el configurador
   - **Popular** — Mostrar una insignia "Popular" para ayudar a los clientes a decidir
   - **Cantidad** — Cuantas unidades de este componente se incluyen
   - **Etiquetas de Compatibilidad** — Etiquetas usadas para la generacion masiva de reglas de compatibilidad

**Consejo:** Los productos componentes pueden ocultarse de la tienda marcando **Ocultar de la Tienda** en la pestana de Informacion Basica del producto componente. Esto los mantiene disponibles como opciones del configurador sin saturar tu catalogo de productos.

### Paso 4: Definir Reglas de Compatibilidad

Las reglas de compatibilidad evitan que los clientes seleccionen combinaciones incompatibles:

| Tipo de Regla | Descripcion |
|---------------|-------------|
| **Requiere** | Cuando se selecciona la opcion A, solo las opciones listadas estan disponibles en la ranura objetivo |
| **Excluye** | Cuando se selecciona la opcion A, las opciones listadas se ocultan de la ranura objetivo |

Para agregar reglas:

1. Desplazate hasta la seccion **Reglas de Compatibilidad** en la pestana de Configuracion
2. Haz clic en **+ Agregar Regla**
3. Selecciona la **opcion de origen** (el disparador)
4. Elige el **tipo de regla** (Requiere o Excluye)
5. Selecciona la **ranura objetivo** y las **opciones afectadas**

Tambien puedes generar reglas automaticamente a partir de las etiquetas de compatibilidad asignadas a las opciones, lo cual es mas rapido cuando se gestionan muchas combinaciones.

### Paso 5: Crear Preajustes (Opcional)

Los preajustes son configuraciones predefinidas que ofrecen a los clientes un punto de partida rapido:

1. Desplazate hasta la seccion **Preajustes de Configuracion**
2. Haz clic en **+ Agregar Preajuste**
3. Dale al preajuste un nombre y descripcion (ej., "Build Gaming", "Inicio Economico")
4. Selecciona las opciones para cada ranura
5. Opcionalmente sube una imagen de vista previa y marcalo como **Destacado**

Los clientes pueden comenzar desde un preajuste y luego personalizar ranuras individuales segun sus preferencias.

## Experiencia del Cliente

Cuando un cliente ve un producto configurable en tu tienda:

1. **Interfaz de Asistente** — Las ranuras se presentan como pasos, guiando al cliente a traves de cada eleccion
2. **Filtrado** — Las opciones incompatibles se ocultan automaticamente segun las reglas de compatibilidad
3. **Insignias de Popular** — Las opciones marcadas como populares muestran una insignia para facilitar la decision
4. **Preajustes** — Los preajustes destacados aparecen como opciones de inicio rapido
5. **Actualizaciones de Precio** — El precio total se actualiza en tiempo real a medida que se seleccionan opciones
6. **Resumen** — Un paso de revision muestra todas las opciones seleccionadas antes de agregar al carrito

## Consejos

- Comienza con la estrategia de precios "Suma de Componentes" — es la mas intuitiva para los clientes y la mas facil de mantener.
- Usa reglas de compatibilidad para prevenir configuraciones invalidas en lugar de depender del conocimiento del cliente.
- Crea 2-3 preajustes para tus configuraciones mas populares para reducir la fatiga de decision.
- Oculta los productos componentes de la tienda si solo deben estar disponibles a traves del configurador.
- Prueba el flujo completo de configuracion en el frontend despues de la configuracion para asegurar que todas las reglas funcionen como se espera.
