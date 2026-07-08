---
title: Clipart y fuentes para productos personalizables
---

El editor de diseños cuenta con dos tipos de activos creativos que puedes proporcionar a los clientes: **clipart** (gráficos listos para usar que pueden agregar a sus diseños) y **fuentes personalizadas** (más allá de las fuentes del sistema estándar). Construir una biblioteca de activos bien curada hace que el editor sea más útil y ayuda a los clientes a crear mejores diseños más rápido.

## Biblioteca de clipart

El clipart le da a los clientes una biblioteca de gráficos prehechos que pueden agregar a sus diseños con un solo clic. En lugar de requerir que los clientes encuentren y suban sus propias imágenes para elementos comunes como iconos, bordes o gráficos decorativos, tú les proporcionas imágenes listas para usar.

### Crear categorías de clipart

El clipart se organiza en categorías que los clientes pueden navegar. Las categorías ayudan a los clientes a encontrar lo que necesitan rápidamente.

1. Navega a **Productos personalizables > Categorías de clipart**
2. Haz clic en **+ Añadir categoría de clipart**
3. Rellena:
   - **Nombre de la categoría** — Lo que ven los clientes (por ejemplo, "Deportes", "Bordes", "Vacaciones")
   - **Slug** — Generado automáticamente a partir del nombre
   - **Icono** — Una clase de icono de Font Awesome para la pestaña de la categoría (por ejemplo, `fas fa-football-ball`)
   - **Orden de clasificación** — Controla el orden en que aparecen las categorías en el editor
4. Haz clic en **Guardar**

**Ejemplos de categorías para una tienda de camisetas:**

| Categoría | Icono | Ejemplo de clipart |
|----------|------|-----------------|
| Deportes | `fas fa-football-ball` | Logos de equipos, equipo deportivo, símbolos deportivos |
| Humor | `fas fa-laugh` | Memes, frases graciosas, personajes de dibujos animados |
| Naturaleza | `fas fa-leaf` | Animales, flores, paisajes |
| Geométrico | `fas fa-shapes` | Patrones, formas abstractas, diseños tribales |

**Ejemplos de categorías para una tienda de impresión/posters:**

| Categoría | Icono | Ejemplo de clipart |
|----------|------|-----------------|
| Bordes | `fas fa-border-all` | Marcos decorativos, adornos de esquinas |
| Temporales | `fas fa-snowflake` | Iconos de vacaciones, motivos temporales |
| Iconos | `fas fa-icons` | Estrellas, corazones, flechas, marcas de verificación |
| Fondo | `fas fa-image` | Texturas, degradados, patrones |

### Añadir activos de clipart

Cada activo de clipart es un archivo de imagen (PNG o SVG) que los clientes pueden colocar en su lienzo.

1. Navega a **Productos personalizables > Activos de clipart**
2. Haz clic en **+ Añadir activo de clipart**
3. Rellena:
   - **Nombre** — Nombre descriptivo (por ejemplo, "Estrella de oro", "Casco de fútbol")
   - **Categoría** — Selecciona de tus categorías de clipart
   - **Activo de imagen** — Haz clic para abrir la Biblioteca de medios y seleccionar o subir el archivo de imagen
   - **Ámbito** — Elige disponibilidad (ver más abajo)
   - **Etiquetas** — Palabras clave buscables para este clipart (por ejemplo, `['estrella', 'oro', 'decoración']`)
   - **Orden de clasificación** — Controla la posición dentro de la categoría
4. Haz clic en **Guardar**

### Entender el ámbito del clipart

Cada activo de clipart tiene un ámbito que controla dónde está disponible:

| Ámbito | Descripción | Caso de uso |
|-------|-------------|----------|
| **Disponible para todos los productos** | Aparece en el navegador de clipart para cada producto personalizable | Gráficos de uso general como estrellas, bordes e iconos comunes |
| **Solo para un producto específico** | Aparece solo para un producto seleccionado | Gráficos específicos de producto como logotipos de marca o arte temático del producto |

Para la mayoría de los activos, usa **Disponible para todos los productos**. Reserva el ámbito específico del producto para activos que solo tengan sentido en el contexto de un solo producto — por ejemplo, logotipos específicos de equipo para un producto de merchandising de equipo.

### Guías de archivos de clipart

- **Formato:** Usa PNG para gráficos raster y SVG para gráficos vectoriales. Los archivos SVG se escalan sin pérdida de calidad, lo que los hace ideales para clipart que los clientes puedan redimensionar significativamente
- **Resolución:** Los archivos PNG deben tener al menos 500x500 píxeles para una buena calidad de impresión
- **Fondo:** Usa fondos transparentes (PNG con canal alfa o SVG) para que el clipart se integre naturalmente con el diseño
- **Tamaño de archivo:** Mantén los archivos de clipart individuales por debajo de 500KB para una carga rápida en el editor

## Fuentes personalizadas

Las fuentes personalizadas extienden el selector de fuentes en el editor de diseños más allá de las fuentes del sistema estándar.

Esto le permite ofrecer tipografía curada que se ajuste a su marca o estilo de producto.

### Añadiendo una fuente personalizada

1. Navegue hasta **Productos personalizables > Fuentes personalizadas**
2. Haga clic en **+ Añadir fuente personalizada**
3. Rellene:
   - **Nombre de la fuente** — Nombre de visualización mostrado en el selector de fuentes (p. ej., "Playfair Display")
   - **Familia de fuentes** — Nombre de la familia de fuentes CSS usado internamente (p. ej., `PlayfairDisplay`)
   - **Regular** — Haga clic para cargar el archivo de peso regular de la fuente (WOFF2 o TTF) a través de la Biblioteca de medios
   - **Negrita** — Variante opcional de peso negrita
   - **Cursiva** — Variante opcional cursiva
   - **Negrita Cursiva** — Variante opcional negrita cursiva
4. Haga clic en **Guardar**

El peso **Regular** es obligatorio para fuentes personalizadas. Las variantes negrita, cursiva y negrita cursiva son opcionales — si no se proporcionan, el navegador intentará sintetizar estos estilos a partir de la fuente regular, aunque los resultados pueden no verse tan pulidos como archivos de fuente dedicados.

### Fuentes del sistema vs. fuentes personalizadas

También puede registrar fuentes del sistema que ya están preinstaladas en la mayoría de los dispositivos:

1. Añada una nueva entrada de fuente personalizada
2. Marque **Fuente del sistema**
3. Introduzca el nombre de la familia de fuentes exactamente como aparece en CSS (p. ej., `Georgia`, `Courier New`)
4. No es necesario cargar ningún archivo para fuentes del sistema

Las fuentes del sistema se cargan de inmediato ya que ya están en el dispositivo del cliente. Las fuentes subidas personalmente necesitan descargarse primero, lo que añade un pequeño retraso cuando se selecciona por primera vez la fuente.

### Recomendaciones de fuentes por tipo de producto

**Para camisetas y ropa de vestir:**
- Las fuentes en negrita y con impacto funcionan mejor: Impact, Anton, Bebas Neue, Oswald
- Las letras en bloque y las fuentes sans-serif son más legibles en tejidos
- Evite fuentes delgadas o delicadas que puedan no imprimirse bien en superficies texturizadas

**Para carteles y productos de impresión:**
- Fuentes serif elegantes para diseños formales: Playfair Display, Merriweather, Lora
- Fuentes de escritura para invitaciones y tarjetas: Great Vibes, Dancing Script, Pacifico
- Fuentes sans-serif limpias para diseños modernos: Montserrat, Raleway, Open Sans

### Formatos de archivos de fuentes

| Formato | Extensión | Recomendación |
|--------|-----------|----------------|
| WOFF2 | `.woff2` | Preferido — tamaño de archivo más pequeño, carga más rápida |
| TrueType | `.ttf` | Buena alternativa — ampliamente compatible |

Los archivos WOFF2 suelen ser un 30-50% más pequeños que los archivos TTF, por lo que se cargan más rápido en el editor del cliente. Use WOFF2 cuando esté disponible.

## Gestionar su biblioteca de activos

### Organizar para los clientes

El orden en que aparecen los activos en el editor se controla mediante el campo **Orden de clasificación** en las categorías y en los activos individuales. Los números más bajos aparecen primero. Use esto para:

- Colocar las categorías de clipart más populares primero
- Colocar el clipart más destacado y versátil en la parte superior de cada categoría
- Ordenar las fuentes con las opciones más utilizadas primero

### Mantener la biblioteca actualizada

- Añada clipart estacional antes de las fiestas (Halloween, Navidad, Día de San Valentín) y desactive después
- Use el cuadro de verificación **Activo** para ocultar temporalmente activos sin eliminarlos
- Supervise qué clipart y fuentes usan los clientes con más frecuencia y amplíe esas categorías

## Consejos

- Empiece pequeño — 20-30 clipart de alta calidad distribuidos en 3-4 categorías es mejor que cientos de opciones mediocres. Puede siempre añadir más a medida que aprenda qué es lo que desean los clientes.
- Use el formato SVG para el clipart siempre que sea posible. Los archivos SVG son más pequeños, se escalan perfectamente a cualquier tamaño y producen impresiones más nítidas que las imágenes raster.
- Pruebe cada fuente subida en el editor de diseño para asegurarse de que todos los caracteres se rendericen correctamente, especialmente caracteres especiales y acentos si sus clientes usan varios idiomas.
- Etiquele el clipart de forma completa — los clientes buscan por palabras clave, por lo que etiquetas descriptivas como "oro", "estrella", "de cinco puntas", "decoración" le ayudan a encontrar el activo correcto rápidamente.
- Agrupe el clipart relacionado en la misma categoría. Si vende merchandising de equipos, cree una categoría por deporte en lugar de una gran categoría "Deportes".
- Revise regularmente su biblioteca de clipart desde la perspectiva del cliente visitando el editor de diseño en el almacén.