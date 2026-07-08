---
title: Ponderaciones de Relevancia e Índice Profundo
---

Las ponderaciones de relevancia e índice profundo controlan cómo se clasifican los resultados de búsqueda y qué datos del producto se buscan. Las ponderaciones son multiplicadores de importancia - una ponderación de 2.0 significa que los coincidencias en ese campo son el doble de importantes que una ponderación de 1.0. El índice profundo determina si la búsqueda va más allá de los nombres básicos de los productos para incluir SKUs, atributos, reseñas e incluso el contenido de documentos. Esta guía explica ambos sistemas, cuándo ajustarlos y las implicaciones críticas de rendimiento.

Los valores predeterminados funcionan bien para la mayoría de las tiendas de comercio electrónico. Solo ajuste si tiene necesidades específicas de clasificación o indexación.

![Pestaña de Ponderaciones](/static/core/admin/img/help/search-settings-overview/search-settings-weights.webp)

## Entendiendo las Ponderaciones

Las ponderaciones son multiplicadores (escala de 0.0-2.0) aplicados cuando se encuentran coincidencias de texto en diferentes campos. Mayor ponderación significa que las coincidencias en ese campo obtienen una clasificación más alta en los resultados.

**Ejemplo**: Si un producto tiene "laptop" en su nombre (ponderación 1.50) y en su descripción (ponderación 0.80):
- La coincidencia en el nombre contribuye 1.50 al puntaje de relevancia
- La coincidencia en la descripción contribuye 0.80
- El puntaje combinado determina la clasificación frente a otros productos

Las ponderaciones le permiten priorizar ciertos campos sobre otros al clasificar los resultados de búsqueda.

## Categorías de Ponderaciones y Valores Predeterminados

Navegue a **Configuración de Búsqueda > Pestaña de Ponderaciones** para ver todas las configuraciones de ponderación:

| Campo | Ponderación Predeterminada | Razonamiento |
|-------|---------------|-----------|
| **weight_name** | 1.50 | Los nombres de los productos son lo más importante - los clientes esperan coincidencias exactas de nombres en la parte superior |
| **weight_sku** | 1.20 | Los SKUs son identificadores específicos - importantes para B2B y clientes recurrentes |
| **weight_description** | 0.80 | Las descripciones proporcionan contexto pero son menos importantes que las coincidencias exactas de nombres |
| **weight_categories** | 0.80 | Las coincidencias de categorías son útiles para la navegación pero no tan específicas como el nombre/SKU |
| **weight_attributes** | 0.70 | Búsquedas de color, tamaño, material - útiles pero información de apoyo |
| **weight_brands** | 0.70 | El filtrado por marca es importante pero no el criterio principal de búsqueda para la mayoría de las tiendas |
| **weight_blog_posts** | 0.60 | El contenido del blog es menos importante en búsquedas orientadas al comercio electrónico (prioridad más baja) |
| **weight_reviews** | 0.50 | El contenido generado por usuarios es el menos controlado - ponderación más baja |

Estos valores predeterminados asumen una tienda de comercio electrónico típica donde la descubrimiento de productos es el objetivo principal de búsqueda.

## Cuándo Ajustar Ponderaciones

Ajuste las ponderaciones cuando las prioridades de su tienda difieran de los patrones típicos de comercio electrónico:

**Tiendas con Alto Volumen de SKUs (B2B, Mayorista)** - Aumente `weight_sku` a 1.8-2.0 para que las búsquedas de códigos de producto dominen los resultados. Los clientes B2B suelen buscar por código SKU exacto.

**Tiendas Centradas en Marcas** - Aumente `weight_brands` a 1.2-1.5 cuando los clientes compren principalmente por marca (ropa de diseñador, productos de lujo).

**Tiendas con Alto Volumen de Contenido** - Aumente `weight_blog_posts` a 0.9-1.2 si es un editor de contenido o minorista educativo donde los artículos del blog son tan importantes como los productos.

**Tiendas con Alto Volumen de Atributos (Moda)** - Aumente `weight_attributes` a 1.0-1.2 cuando los clientes busquen con frecuencia por atributos de color, tamaño, estilo.

## Ejemplos de Ajuste de Ponderaciones

| Tipo de Tienda | Ajustes Recomendados |
|-----------|------------------------|
| **Minorista B2B** | weight_sku: 2.0, weight_name: 1.3, weight_description: 0.6 - Priorizar códigos de producto |
| **Boutique de Moda** | weight_attributes: 1.2, weight_brands: 1.2, weight_name: 1.4 - Color/estilo/marca importante |
| **Editor de Contenido** | weight_blog_posts: 1.2, weight_name: 1.3, weight_reviews: 0.7 - Contenido tan importante como productos |
| **Comercio Electrónico General** | Use defaults - Equilibrado para tiendas en línea típicas |

Ajuste una ponderación a la vez y pruebe antes de hacer cambios adicionales.

## Visión General del Índice Profundo

⚠️ **ADVERTENCIA DE RENDIMIENTO** - Cada opción de índice profundo agrega complejidad y sobrecarga a las consultas.

El índice profundo extiende la búsqueda más allá del nombre y descripción básicos del producto hacia otros datos:

![Pestaña de Índice Profundo](/static/core/admin/img/help/search-settings-overview/search-settings-deep-indexing.webp)

Navegue a **Configuración de Búsqueda > Pestaña de Índice Profundo** para configurar.

## Índice de SKUs

**Predeterminado**: ACTIVADO, **Impacto en Rendimiento**: Bajo

Incluye SKUs de productos y variantes en el índice de búsqueda. Activa unión de variantes (costo menor).

**Cuándo mantener ACTIVADO**: Esencial para tiendas B2B donde los clientes conocen los códigos de producto. También es útil para clientes recurrentes que recuerdan el SKU de pedidos anteriores.

**Cuándo desactivar**: Nunca, a menos que literalmente no tenga SKUs asignados. El impacto en el rendimiento es insignificante.

## Índice de Atributos

**Predeterminado**: ACTIVADO, **Impacto en Rendimiento**: Medio

Incluye atributos del producto (color, tamaño, material, atributos personalizados) en el índice de búsqueda. Realiza unión a la tabla de atributos.

**Cuándo mantener ACTIVADO**: Importante para tiendas de moda, productos configurables o cualquier tienda donde los clientes busquen por características del producto ("vestido rojo", "camisa grande").

**Cuándo desactivar**: Catálogos >20,000 productos con muchos atributos por producto pueden experimentar un sobrecarga de 50-100ms. Solo desactive si el rendimiento es crítico y los clientes no buscan por atributos.

## Índice de Campos Personalizados

**Predeterminado**: ACTIVADO, **Impacto en Rendimiento**: Medio

Incluye campos personalizados definidos por el comerciante de JSONField en la búsqueda. Requiere recorrido de JSONField.

**Cuándo mantener ACTIVADO**: Si utiliza campos personalizados para datos del producto buscables (información de garantía, especificaciones, detalles de compatibilidad).

**Cuándo desactivar**: Si no utiliza campos personalizados, o los campos personalizados contienen datos no buscables (notas internas, códigos contables). Desactivar ahorra sobrecarga de procesamiento de JSONField.

## Índice de Reseñas

**Predeterminado**: ACTIVADO, **Impacto en Rendimiento**: Medio-Alto

Incluye títulos y comentarios de reseñas aprobadas en la búsqueda. Realiza unión a la tabla de reseñas y agrega sobrecarga de búsqueda de texto.

**Cuándo mantener ACTIVADO**: Catálogos con muchas reseñas donde los clientes buscan productos basados en el contenido de las reseñas ("bolsa de laptop impermeable" podría aparecer en el texto de la reseña).

**Cuándo desactivar**: Catálogos >20,000 productos o tiendas con muchas reseñas por producto. Añade 100-200ms de sobrecarga en catálogos grandes.

## Índice de Documentos

**Predeterminado**: DESACTIVADO, **Impacto en Rendimiento**: MUY ALTO 🚨

**NUNCA ACTIVAR DE FORMA CASUAL** - Característica de búsqueda más costosa.

El índice de documentos extrae texto de archivos PDF, DOCX y XLSX adjuntos a productos digitales, haciendo que el contenido de los archivos sea buscable.

**Detalles Técnicos**:
- Usa bibliotecas PyPDF2, python-docx y openpyxl
- E/S de archivos y extracción de texto sincrónicos en la búsqueda
- Rastrea archivos mediante checksum MD5 (reíndice solo cuando el archivo cambie)
- Posibles tiempos de espera en archivos grandes (>10MB PDFs)

**Impacto en Rendimiento**:
- Muy costoso índice inicial (minutos a horas para bibliotecas grandes)
- Sobrecarga significativa de consulta (latencia adicional de 100-500ms)
- Intensivo en memoria para documentos grandes

**Solo active si**:
- Vende productos digitales con documentos buscables (libros electrónicos, informes, manuales)
- Catálogo es pequeño (<500 productos digitales)
- El servidor tiene recursos suficientes
- Ha probado el impacto exhaustivamente

**Para tiendas de productos digitales**: Considere si los clientes realmente necesitan buscar el contenido de los documentos, o si buscar el nombre/descripción del producto es suficiente.

## Tabla de Impacto de Rendimiento

| Función | Predeterminado | Impacto | Usar Cuando |
|---------|---------|--------|----------|
| Índice de SKUs | ACTIVADO | Bajo | Siempre (esencial para B2B) |
| Índice de Atributos | ACTIVADO | Medio | Productos configurables |
| Índice de Campos Personalizados | ACTIVADO | Medio | Usando campos personalizados |
| Índice de Reseñas | ACTIVADO | Medio-Alto | Tienda con muchas reseñas |
| Índice de Documentos | DESACTIVADO | Muy Alto | Solo productos digitales (pruebe primero) |

El impacto asume catálogos típicos. Catálogos grandes (>50,000 productos) experimentan un sobrecarga proporcionalmente más alta.

## Pruebas de Cambios en Ponderaciones

Cuando ajuste las ponderaciones, siga este flujo de trabajo de pruebas:

1. **Cambie una ponderación a la vez** - No ajuste múltiples ponderaciones simultáneamente; no sabrá qué cambio causó los resultados
2. **Incrementos pequeños** - Ajuste en ±0.2 a la vez (por ejemplo, 1.0 → 1.2, no 1.0 → 1.8)
3. **Pruebe con consultas reales** - Use términos de búsqueda reales de clientes de análisis, no pruebas aleatorias
4. **Monitoree análisis** - Compare la relevancia de los resultados antes y después usando las consultas principales
5. **Espere 1-2 semanas** - Dé a los clientes tiempo para interactuar con los nuevos rankings
6. **Mida las tasas de clics** - ¿Los clientes están haciendo clic en los resultados más/menos que antes?

## Compromiso entre Rendimiento y Precisión

Más indexación = mejores resultados de búsqueda pero menor rendimiento:

**Escenario: Catálogo Pequeño (<1,000 productos)**
- Active todas las opciones de indexación (SKUs, atributos, campos personalizados, reseñas)
- Impacto en el rendimiento mínimo
- Capacidad de búsqueda completa

**Escenario: Catálogo Mediano (1,000-10,000 productos)**
- Mantenga SKUs, atributos, campos personalizados ACTIVADOS
- Considere desactivar reseñas si el promedio es >10 reseñas por producto
- Monitoree tiempos de respuesta

**Escenario: Catálogo Grande (>10,000 productos)**
- Mantenga SKUs ACTIVADOS (bajo impacto)
- Desactive el indexado de reseñas (alto impacto)
- Desactive campos personalizados si no se usan
- NUNCA active el indexado de documentos
- Considere Elasticsearch a partir de >50,000 productos

Equilibre según el tamaño de su catálogo y los recursos del servidor.

## Sobrescrituras de Ponderaciones Específicas del Motor

Cuando cree un motor de búsqueda mediante el asistente (Paso 3), puede sobrescribir las ponderaciones globales para ese motor específico.

**Caso de uso**: Motor centrado en blogs
- Cree el motor "blog"
- Sobrescriba `weight_blog_posts` a 1.5 (vs. global 0.60)
- El contenido del blog ahora tiene un rango más alto en búsquedas del motor de blog

La mayoría de los motores NO deben sobrescribir ponderaciones - deje en blanco para heredar las configuraciones globales.

## Consejos

- **NUNCA active el índice de documentos a menos que sea absolutamente crítico** - Mayor costo de rendimiento de cualquier característica de búsqueda
- **Tiendas B2B: Aumente weight_sku a 2.0** - Los códigos de producto son el método principal de búsqueda
- **Pruebe cambios en ponderaciones durante horas de baja afluencia** - Observe el impacto en el rendimiento antes de horas pico
- **Monitoree tiempos de respuesta después de activar el índice** - Revise el panel de análisis para detectar ralentizaciones
- **Desactive el índice de reseñas en catálogos >20K productos** - Impacto significativo en el rendimiento
- **Un cambio a la vez en ponderaciones para pruebas** - No se puede determinar causa/efecto con cambios simultáneos
- **La extracción de documentos requiere PyPDF2/docx/openpyxl** - Verifique que estas bibliotecas estén instaladas antes de activar el índice de documentos

Recuerde: Preserve all markdown formatting, image paths, code blocks, and technical terms exactly as shown in the preservation rules.