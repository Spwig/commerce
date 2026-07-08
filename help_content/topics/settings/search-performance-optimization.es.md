---
title: Optimización del Rendimiento de Búsqueda
---

El rendimiento de la búsqueda afecta directamente la experiencia del cliente y las conversiones. Las búsquedas lentas frustran a los clientes y aumentan las tasas de rebote. Esta guía completa identifica los cuellos de botella comunes en el sistema de búsqueda nativo de la base de datos de Spwig, proporciona estrategias de optimización y establece objetivos de rendimiento. Utilice esta guía cuando los tiempos de respuesta de búsqueda excedan los umbrales aceptables o cuando esté planificando el crecimiento del catálogo.

Tiempos de respuesta objetivo: <200ms para autocompletar, <500ms para búsqueda completa. Siga la lista de verificación de optimización a continuación para alcanzar estos objetivos.

## Comprensión de las Métricas de Rendimiento

Supervise estas métricas en **Búsqueda > Análisis de Búsqueda**:

**Tiempo de Respuesta** - Milisegundos para ejecutar una consulta de búsqueda (solo lado del servidor, excluye la latencia de red)

**Tasa de Aciertos en la Caché** - Porcentaje de búsquedas servidas desde la caché vs base de datos

**Conteo de Consultas** - Número de consultas a la base de datos por búsqueda (menos es mejor)

**Tiempo de Consulta a la Base de Datos** - Tiempo invertido en la base de datos vs código de aplicación

## Objetivos de Rendimiento

| Tipo de Consulta | Objetivo | Aceptable | Requiere Optimización |
|------------------|--------|------------|----------------------|
| Autocompletar | <200ms | 200-300ms | >300ms consistentemente |
| Búsqueda Completa | <500ms | 500-800ms | >800ms consistentemente |
| Búsqueda de Administración | <1000ms | 1000-1500ms | >1500ms consistentemente |

Si sus tiempos de respuesta promedio exceden los umbrales de "Requiere Optimización", implemente las estrategias a continuación.

## Monitoreo del Rendimiento

**Tiempo de Respuesta Promedio del Panel de Análisis**

Navegue a **Búsqueda > Análisis de Búsqueda** para ver el tiempo de respuesta promedio en todas las búsquedas. Este es su métrica principal de monitoreo de rendimiento.

**Cuándo Investigar**: Tiempo de respuesta promedio >300ms para autocompletar o >800ms para búsqueda completa consistentemente durante varios días.

**Monitoreo Semanal**: Revise los análisis cada lunes para detectar degradación del rendimiento temprano.

## Cuellos de Botella de Rendimiento Conocidos

La búsqueda nativa de la base de datos de Spwig tiene varios cuellos de botella documentados para evitar:

### Cálculo de CTR con N+1 Consultas

**¿Qué Es**: El cálculo de la tasa de clics en AnalyticsService ejecuta consultas separadas para cada elemento de resultado agregado.

**Impacto**: Severo en tiendas de alto tráfico con muchas consultas rastreadas.

**Ubicación del Código**: `search/services/analytics_service.py` - método `get_click_through_rate()`

**Mitigación**: Evite llamar a los cálculos de CTR en producción. Esto es principalmente una característica de análisis de administración que debe calcularse de forma asincrónica, no durante solicitudes orientadas al cliente.

### Agregación de Existencias

**¿Qué Es**: `with_stock_totals()` calcula las existencias disponibles en todos los almacenes por producto.

**Impacto**: Costoso en catálogos >1,000 productos. Se llama cuando se usa el filtro `in_stock` o se muestra el estado de existencias en el autocompletar.

**Triggger**: **Configuración de Búsqueda > Autocompletar** - opción "Mostrar Estado de Existencias"

**Recomendación**: NUNCA habilite el estado de existencias en el autocompletar en catálogos grandes. Añade 200-500ms por solicitud.

### Úniones de Variantes

**¿Qué Es**: Las búsquedas de SKU desencadenan JOIN en la tabla de variantes para buscar SKU de variantes.

**Impacto**: 2-3 veces más lento en productos con muchas variantes (10+ variantes por producto).

**Mitigación**: Usa `.distinct()` para evitar duplicados, lo cual añade sobrecarga. Necesario para la funcionalidad de SKU - no lo deshabilite a menos que no se usen SKU.

### Conteo de Productos en Autocompletar

**¿Qué Es**: Los resultados de autocompletar de categoría/marca muestran conteos de productos ("Electrónicos (234)")

**Impacto**: Cada tipo de contenido con conteos habilitados añade 2 consultas adicionales. Las consultas incluyen únicas y agregaciones.

**Triggger**: **Configuración de Búsqueda > Autocompletar** - "Mostrar Conteo de Productos" para categorías/marcas

**Recomendación**: Deshabilite los conteos de productos. Ahorra 2-4 consultas por solicitud de autocompletar. La optimización más grande de autocompletar.

### Índice de Documentos

**¿Qué Es**: Extracción de texto de archivos PDF/DOCX/XLSX durante consultas de búsqueda.

**Impacto**: Muy costoso (E/S de archivos + extracción de texto). Operaciones bloqueantes sincrónicas.

**Triggger**: **Configuración de Búsqueda > Índice Profundo** - "Índice de Documentos"

**Recomendación**: Casi nunca vale la pena el costo de rendimiento. SOLO habilite para catálogos pequeños de productos digitales (<500 productos) después de pruebas exhaustivas.

## Configuración de Caché

La caché es la optimización de rendimiento más efectiva.

**Caché de Autocompletar** - Por defecto: 60s
- **Rango Recomendado**: 45-90s
- **TTL Mayor (90-120s)**: Mejor rendimiento si los cambios de inventario son infrecuentes
- **TTL Menor (30-45s)**: Resultados más recientes si agrega productos cada hora

**Caché de Resultados** - Por defecto: 300s (5 minutos)
- **Rango Recomendado**: 180-600s
- **TTL Mayor (600s/10min)**: Mejora significativa del rendimiento para catálogos estáticos
- **TTL Menor (180s)**: Más recientes si actualiza frecuentemente datos del producto

**Estrategia de Optimización**: Si las búsquedas son lentas, duplique el TTL de la caché antes de deshabilitar funciones. Ir de 60s → 120s de caché de autocompletar reduce la carga de la base de datos a la mitad.

## Lista de Verificación de Optimización de Autocompletar

Aplicar estos cambios a la configuración de autocompletar para el máximo rendimiento:

**1. Aumentar Debounce a 300-400ms**
- Ubicación: **Configuración de Búsqueda > Autocompletar** - "Retardo de Debounce"
- Impacto: Reduce las llamadas a la API esperando más tiempo entre teclados
- Contra: Ligeramente menos responsive (imperceptible para la mayoría de usuarios)

**2. Reducir Max Results de 8 a 5-6**
- Ubicación: **Configuración de Búsqueda > Autocompletar** - "Máximo de Resultados por Tipo"
- Impacto: Resultados más pequeños = consultas más rápidas y payloads JSON más pequeños
- Contra: Menos opciones mostradas (normalmente suficiente)

**3. Deshabilitar Conteo de Productos (GANANCIA MAYOR)**
- Ubicación: **Configuración de Búsqueda > Autocompletar** - Desmarcar "Mostrar Conteo de Productos" para categorías/marcas
- Impacto: Ahorra 2-4 consultas por solicitud de autocompletar
- Contra: Sin conteos de productos en el menú desplegable (raramente necesarios)

**4. Deshabilitar Estado de Existencias**
- Ubicación: **Configuración de Búsqueda > Autocompletar** - Desmarcar "Mostrar Estado de Existencias"
- Impacto: Elimina la agregación costosa de existencias
- Contra: Sin insignias de existencias (no críticas en el contexto de autocompletar)

**5. Deshabilitar Descripciones de Productos**
- Ubicación: **Configuración de Búsqueda > Autocompletar** - Desmarcar "Mostrar Descripción"
- Impacto: Reduce el procesamiento de texto y el tamaño del payload
- Contra: Menos texto de vista previa (nombre del producto normalmente suficiente)

**6. Aumentar TTL de Caché a 90s**
- Ubicación: **Configuración de Búsqueda > Caché** - "TTL de Caché de Autocompletar"
- Impacto: Más solicitudes servidas desde la caché
- Contra: Resultados hasta 90 segundos desactualizados (aceptable para la mayoría de tiendas)

**Mejora Esperada**: Aplicar todas las 6 optimizaciones normalmente reduce el tiempo de respuesta de autocompletar en un 50-70%.

## Optimización del Índice Profundo

Cada opción de índice profundo añade sobrecarga. Désablela según el tamaño del catálogo:

| Tamaño del Catálogo | Índice Profundo Recomendado |
|---------------------|---------------------------|
| **<1,000 productos** | Todo EN (impacto mínimo) |
| **1,000-10,000** | Mantener SKUs, Atributos, Campos Personalizados EN; Désable Reviews |
| **10,000-20,000** | Mantener SKUs, Atributos EN; Désable Campos Personalizados, Reviews |
| **20,000-50,000** | Mantener SKUs EN solo; Désable todo lo demás |
| **>50,000** | Mantener SKUs EN; Considerar migración a Elasticsearch |

**Índice de Documentos**: SIEMPRE DESHABILITADO a menos que sea crítico (productos digitales con documentos buscables Y <500 productos totales).

## Optimización de Tipos de Contenido

Deshabilite tipos de contenido no utilizados en **Configuración de Búsqueda > Tipos de Contenido**:

- **¿No hay blog?** Deshabilite "Posts de Blog" - ahorra consultas
- **¿No hay filtrado por marca?** Deshabilite "Marcas" - ahorra consultas
- **¿Tienda solo de compras?** Deshabilite "Categorías" y "Posts de Blog"

Cada tipo de contenido deshabilitado elimina consultas a la base de datos de cada búsqueda.

## Optimización de Base de Datos

Spwig crea índices necesarios a través de migraciones. Confíe en ellos - no cree índices adicionales sin perfilaje.

**Mantenimiento de PostgreSQL** (si está usando PostgreSQL):
- Ejecute `VACUUM ANALYZE` semanalmente para actualizar estadísticas del planificador de consultas
- Catálogos grandes benefician de `VACUUM FULL` mensual (requiere tiempo de inactividad)

**Supervise el Tiempo de Consulta a la Base de Datos**: Durante el desarrollo, identifique consultas lentas usando herramientas de perfilaje. La mayoría de la optimización de consultas ya está implementada:
- `.select_related('brand', 'category')` en productos
- `.prefetch_related('images')` para miniaturas
- `.distinct()` para búsquedas de variantes

## Rendimiento de Coincidencia Fuzzy

La distancia de Levenshtein es computacionalmente costosa (complejidad O(m*n)):

**Optimización del Umbral**:
- **Umbral más alto (0.85 vs 0.80)**: Más rápido pero captura menos errores de escritura
- **Umbral más bajo (0.75 vs 0.80)**: Más lento pero más tolerante

**Optimización del Máximo de Edits**:
- **Máximo de edits más bajo (1 vs 2)**: Más rápido pero falla más errores de escritura
- **Máximo de edits más alto (2 vs 3)**: Más lento pero captura más errores de escritura

**Rendimiento de la Biblioteca**: Spwig usa `rapidfuzz` si está disponible (10 veces más rápido que Python puro). Asegúrese de que esté instalado: `pip install rapidfuzz`

## Rendimiento de Síntesis y Redirección

**Expansión de Consultas de Síntesis**: Cada síntesis añade cláusulas OR a la consulta de búsqueda. Límite a 10-20 síntesis por término máximo.

**Tipo de Coincidencia con Expresiones Regulares**: Las redirecciones con expresiones regulares son más lentas que exactas/contiene/comienza_con. Evite patrones complejos.

**Recomendación**: Use tipos de coincidencia simples siempre que sea posible. Reserve expresiones regulares para casos donde otros tipos de coincidencia no funcionen.

## Optimización para Catálogos Grandes (>10,000 productos)

Estrategias específicas para catálogos grandes:

**1. Caché Agresivo**
- Autocompletar: TTL de 90-120s
- Resultados: TTL de 600s (10min)
- Acepte la desactualización para el rendimiento

**2. Índice Profundo Mínimo**
- Solo SKUs (deshabilite atributos, campos personalizados, reseñas)
- Pruebe el rendimiento con y sin atributos

**3. Resultados de Autocompletar Reducidos**
- Máximo 5 resultados por tipo (de 8)
- Reduce la sobrecarga de consulta

**4. Deshabilitar Estado de Existencias en Todos Lados**
- En autocompletar
- En resultados de búsqueda si se muestran

**5. Considerar Elasticsearch a partir de >50K Productos**
- La búsqueda nativa de la base de datos es adecuada hasta ~50,000 productos
- Más allá de eso, Elasticsearch se recomienda para:
  - Búsqueda facetada compleja
  - Alta carga de búsqueda concurrente (>100 búsquedas/segundo)
  - Tiempos de respuesta consistentemente >500ms incluso después de la optimización

## Rendimiento Multilingüe

El índice JSONField JSONB (PostgreSQL) hace que el multilingüe sea eficiente:

- **1-3 idiomas**: Sobrecarga mínima (5-10ms)
- **5+ idiomas**: Aumento menor en la complejidad de la consulta (20-40ms)
- **10+ idiomas**: Sobrecarga notable (50-100ms)

La sobrecarga aumenta linealmente con el número de idiomas.

## Correcciones de Rendimiento de Emergencia

Si las búsquedas son críticamente lentas (>2s tiempos de respuesta), aplique estas correcciones inmediatas en orden:

**Inmediato** (aplique ahora):
1. Deshabilite el índice de documentos
2. Deshabilite los conteos de productos en el autocompletar
3. Aumente los TTL de caché a 120s autocompletar / 600s resultados

**Rápido** (aplique dentro de 24 horas):
4. Deshabilite el estado de existencias en el autocompletar
5. Reduzca el máximo de resultados de autocompletar a 5
6. Deshabilite las descripciones de productos en el autocompletar

**Medio** (aplique dentro de una semana):
7. Deshabilite el índice de reseñas si >20K productos
8. Revise y deshabilite tipos de contenido no utilizados
9. Aumente el debounce a 400ms

**Mejora Esperada**: Estas 9 correcciones normalmente reducen los tiempos de respuesta en un 60-80% en catálogos grandes.

## Consejos

- **Supervise los tiempos de respuesta semanalmente** - Detecte la degradación del rendimiento temprano
- **Aumentos de caché son la primera optimización** - Duplicar el TTL de caché es la ganancia más fácil
- **Conteo de productos en autocompletar = costoso** - El mayor asesino de rendimiento de autocompletar
- **Índice de documentos casi nunca vale la pena** - El costo de rendimiento rara vez justifica el beneficio
- **Pruebe un cambio a la vez** - No se puede identificar causa/efecto con cambios simultáneos
- **Benchmark con volúmenes de datos realistas** - Pruebe con catálogos de tamaño de producción
- **La agregación de existencias destruye el rendimiento en catálogos grandes** - Evite mostrar existencias en el autocompletar
- **Considere Elasticsearch a partir de 50K+ productos** - La búsqueda nativa de la base de datos tiene límites

Recuerde: preserve all markdown formatting, image paths, code blocks, and technical terms exactly as shown in the preservation rules.