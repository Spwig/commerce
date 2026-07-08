---
title: Configurando Autocomplete
---

Autocomplete, también llamado búsqueda predictiva o búsqueda mientras se escribe, muestra resultados mientras los clientes escriben sus consultas. Esto mejora significativamente la experiencia del usuario ayudando a los clientes a encontrar productos más rápido y reduciendo las búsquedas sin resultados. Esta guía explica cómo configurar el comportamiento de autocomplete, ajustes de visualización y compromisos de rendimiento.

El autocomplete está habilitado de forma predeterminada con ajustes sensibles. Solo ajuste estos si tiene preocupaciones específicas de rendimiento o preferencias de visualización.

![Configuración de Autocomplete](/static/core/admin/img/help/configuring-autocomplete/autocomplete-settings-main.webp)

## Habilitar Autocomplete

Navegue hasta **Búsqueda > Configuración de búsqueda** y haga clic en la pestaña **Autocomplete**.

**Habilitar Autocomplete** - Interruptor maestro para la búsqueda predictiva. Cuando está habilitado, los campos de búsqueda muestran un menú desplegable de resultados mientras los clientes escriben.

**Máximo de Resultados por Tipo** - Valor predeterminado: 8 elementos. ¿Cuántos resultados mostrar para cada tipo de contenido (productos, categorías, marcas, entradas de blog)? Los valores más bajos (5-6) reducen el tamaño de la carga de la API y renderizan más rápido. Los valores más altos (10-12) dan a los clientes más opciones, pero ralentizan la respuesta.

## Tiempo de Debounce

⚠️ **ADVERTENCIA DE RENDIMIENTO** - El tiempo de debounce afecta significativamente la carga del servidor.

**Retardo de Debounce** - Valor predeterminado: 300ms. ¿Cuánto tiempo esperar después del último teclado antes de desencadenar una solicitud de autocomplete?

Este ajuste equilibra la responsividad con la carga del servidor:

| Retardo | Experiencia del usuario | Impacto en el servidor |
|---------|------------------------|------------------------|
| **100ms** | Muy responsivo | 3x más llamadas a la API que 300ms - alta carga |
| **200ms** | Responsivo | 1.5x más llamadas a la API que 300ms |
| **300ms** | Buen equilibrio (recomendado) | Valor base |
| **400ms** | Ligeramente lento | Menos llamadas a la API - menor carga |
| **500ms** | Retraso notorio | 50% menos llamadas, pero se siente lento |

**Recomendación**: Mantenga entre 250-350ms. Solo aumente por encima de 350ms si su servidor tiene dificultades con la carga de autocomplete. Nunca vaya por debajo de 200ms a menos que tenga un servidor muy rápido y un catálogo pequeño.

## Configuraciones de Visualización para Productos

Estos interruptores controlan qué información aparece en los resultados de autocomplete de productos:

**Mostrar Miniatura** - Valor predeterminado: ACTIVADO. Muestra la imagen del producto junto al resultado. **Impacto en el rendimiento**: Añade una consulta de imagen e incrementa el tamaño de la carga de JSON. Désactivelo para un autocomplete más rápido en conexiones lentas.

**Mostrar Descripción** - Valor predeterminado: DESACTIVADO. Muestra la descripción corta del producto. **Impacto en el rendimiento**: Añade procesamiento de texto e incrementa significativamente el tamaño de la carga. Manténgalo desactivado a menos que las descripciones sean críticas para la selección del producto.

**Mostrar Precio** - Valor predeterminado: ACTIVADO. Muestra el precio del producto. **Impacto en el rendimiento**: Bajo - los datos de precio ya están cargados con el producto. Es seguro mantenerlo activado.

**Mostrar SKU** - Valor predeterminado: ACTIVADO. Muestra el SKU del producto. **Impacto en el rendimiento**: Bajo - el SKU ya está indexado. Esencial para tiendas B2B.

**Mostrar Estado de Stock** - Valor predeterminado: DESACTIVADO. ⚠️ **ADVERTENCIA DE RENDIMIENTO MAYOR**

Muestra los distintivos "En Stock", "Bajo Stock" o "Agotado". **NUNCA habilite esto en catálogos grandes**.

El estado del stock requiere la agregación `with_stock_totals()` - calcular las cantidades disponibles en todos los almacenes para cada producto en los resultados de autocomplete. Esto agrega:
- Carga significativa en la base de datos (consultas de agregación)
- 200-500ms de latencia adicional en catálogos >1,000 productos
- Posibles tiempos de espera en catálogos >10,000 productos

Solo habilite si es absolutamente crítico y tiene <500 productos.

## Configuraciones de Visualización para Entradas de Blog

**Mostrar Imagen Destacada** - Valor predeterminado: ACTIVADO. Miniatura del blog en los resultados de autocomplete.

**Mostrar Extracto** - Valor predeterminado: ACTIVADO. Texto previo breve del contenido de la entrada.

**Longitud del Extracto** - Valor predeterminado: 60 caracteres. ¿Cuánto texto previo mostrar?

Estos ajustes tienen un impacto mínimo en el rendimiento ya que las entradas de blog suelen ser pocas en comparación con los productos.

## Configuraciones de Visualización para Categorías y Marcas

**Mostrar Miniatura/Logo** - Valor predeterminado: ACTIVADO. Imagen de categoría o marca en los resultados.

**Mostrar Cantidad de Productos** - Valor predeterminado: DESACTIVADO. ⚠️ **ADVERTENCIA DE RENDIMIENTO**

Muestra cuántos productos hay en cada categoría o marca (por ejemplo, "Electrónicos (234)").

**NUNCA habilite esto en catálogos grandes**. Las cantidades de productos se recalculan en cada solicitud de autocomplete:
- Cada tipo de contenido con cantidades habilitadas agrega 2 consultas adicionales
- Las consultas incluyen uniones y agregaciones
- Latencia adicional típica de 100-300ms
- Aumenta linealmente con el número de categorías/marcas

Solo habilite si tiene <50 categorías/marcas Y <1,000 productos en total.

## Caché

**Tiempo de Vida del Caché de Autocomplete** - Valor predeterminado: 60 segundos (configurado en la pestaña de Caché).

Los resultados de autocomplete se almacenan en caché para mejorar el rendimiento. El TTL de 60 segundos significa:
- El primer cliente que busca "laptop" desencadena una consulta a la base de datos
- Durante los próximos 59 segundos, todas las búsquedas de "laptop" devuelven resultados en caché
- Después de 60 segundos, el caché expira y la próxima búsqueda actualiza los datos

**Recomendación para TTL**:
- **45-60s**: Buen equilibrio para la mayoría de las tiendas (predeterminado)
- **90-120s**: Mejor rendimiento si el inventario de productos cambia raramente
- **30s**: Resultados más recientes si agrega productos con frecuencia

Aumentar el TTL del caché es la forma más sencilla de mejorar el rendimiento de autocomplete.

## Autocomplete Multilingüe

Si tiene configuradas múltiples lenguas, el autocomplete busca automáticamente el contenido traducido almacenado en campos JSONField de traducciones.

**Cómo funciona**:
- El cliente busca en español: "zapatos"
- El sistema busca traducciones de nombres de productos en español
- Los resultados muestran nombres de productos en español desde los datos de JSONField
- Si no hay traducción en español, se recurre al idioma base

**Rendimiento**: Overhead mínimo para 1-3 idiomas. Con 5+ idiomas, un ligero aumento en la complejidad de las consultas.

## Pruebas de Autocomplete

Después de configurar los ajustes, pruebe la experiencia de autocomplete:

1. **Abra la página de inicio de su tienda** en una ventana incógnito
2. **Haga clic en el cuadro de búsqueda** para enfocarlo
3. **Escriba el nombre de un producto común** lentamente (por ejemplo, "laptop")
4. **Observe**:
   - ¿Cuán rápido aparecen los resultados después de dejar de escribir? (¿funciona el debounce?)
   - ¿Qué información se muestra? (miniaturas, precios, SKUs según la configuración)
   - ¿Los resultados son relevantes? (verifique los pesos de relevancia si no lo son)
5. **Pruebe en móvil** - Asegúrese de que el menú desplegable sea amigable para tocar y legible

## Consejos

- **Deshabilite descripciones de productos para mayor velocidad** - Las descripciones aumentan significativamente el tamaño de la carga con un valor mínimo en el contexto de autocomplete
- **NUNCA habilite el estado de stock en catálogos grandes** - La agregación de stock destruye el rendimiento de autocomplete
- **Pruebe en móvil con objetivos de toque** - Los resultados de autocomplete deben ser fácilmente tachables en teléfonos
- **Monitorea los tiempos de respuesta semanalmente** - Objetivo: <200ms para las solicitudes de autocomplete
- **Aumente el TTL del caché si es lento** - Optimización de rendimiento más sencilla
- **Las cantidades de productos son costosas - deshabilítelas a menos que sea crítico** - Cada cantidad de categoría/marca agrega 2 consultas a cada solicitud de autocomplete