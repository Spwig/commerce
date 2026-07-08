---
title: Panel de análisis de búsqueda
---

El panel de análisis de búsqueda registra cada consulta de búsqueda en su tienda, proporcionando información sobre qué buscan los clientes, qué búsquedas tienen éxito o fracasan y qué tan rápido responde su sistema de búsqueda. Use estos datos para identificar productos populares, descubrir inventarios faltantes, crear sinónimos y optimizar el rendimiento de búsqueda.

El seguimiento de análisis debe estar habilitado en **Configuración de búsqueda > pestaña de análisis** para que los datos aparezcan.

![Panel de análisis](/static/core/admin/img/help/search-analytics-dashboard/analytics-dashboard.webp)

## Visión general del panel

Navegue a **Búsqueda > Análisis de búsqueda** para acceder al panel. La página muestra:

**Tarjetas de estadísticas** - Métricas rápidas para hoy y la semana pasada:
- Total de búsquedas de hoy
- Total de búsquedas de esta semana
- Consultas sin resultados (búsquedas que devuelven ningún producto)
- Tiempo de respuesta promedio en milisegundos

**Tabla de consultas principales** - Términos de búsqueda más frecuentes con conteos de resultados

**Consultas sin resultados** - Búsquedas que devolvieron ningún resultado (críticas para la mejora)

**Lista de consultas** - Todos los registros de búsqueda individuales con filtros

## Estadísticas del día

**Total de búsquedas de hoy** - Cantidad de todas las solicitudes de búsqueda desde la medianoche en la zona horaria de su tienda. Incluye tanto las solicitudes de autocompletar como las de página de búsqueda completa.

**Consultas únicas de hoy** - Cantidad de términos de búsqueda distintos utilizados hoy. Si 5 clientes buscan "laptop", esto se cuenta como 1 consulta única a pesar de 5 búsquedas totales.

**Sin resultados hoy** - Búsquedas de hoy que devolvieron ningún producto. Un alto número de consultas sin resultados indica productos faltantes o una cobertura de sinónimos pobre.

Las actualizaciones de datos en tiempo real ocurren a medida que se realizan las búsquedas.

## Estadísticas semanales

**Total de la semana** - Total de búsquedas en los últimos 7 días

**Consultas únicas** - Términos de búsqueda distintos utilizados esta semana

**Crecimiento semanal** - Cambio porcentual en comparación con la semana anterior (si se muestra)

Use los datos semanales para detectar tendencias: un aumento en el volumen de búsqueda suele correlacionarse con un crecimiento en el tráfico o campañas de marketing.

## Tiempo de respuesta promedio

⚠️ **MONITOREO DE RENDIMIENTO**

Tiempo promedio (en milisegundos) para ejecutar consultas de búsqueda. Tiempos objetivo de respuesta:

| Tipo de consulta | Objetivo | Umbral de advertencia |
|------------------|--------|---------------------|
| Autocompletar | < 200ms | > 300ms consistentemente |
| Búsqueda completa | < 500ms | > 800ms consistentemente |

Si el tiempo de respuesta promedio supera los umbrales de advertencia:
1. Revise **Configuración de búsqueda > pestaña de caché** - aumente los TTL de caché
2. Revise **pestaña de Índice profundo** - desactive características costosas (índice de documentos, índice de reseñas en catálogos grandes)
3. Consulte la guía [Optimización del rendimiento de búsqueda](/en/admin/help/search-performance-optimization/)

## Consultas principales

La tabla de consultas principales muestra los términos de búsqueda más frecuentes:

**Use estos datos para**:
- **Destacar productos populares** - Si "auriculares inalámbricos" es una consulta principal, destaque esos productos en su página de inicio
- **Decisiones de inventario** - Un alto volumen de búsqueda en una categoría indica demanda
- **Identificar tendencias** - Las búsquedas estacionales revelan qué es popular actualmente
- **Creación de contenido** - Escriba artículos de blog o guías sobre temas frecuentemente buscados

Revise las consultas principales mensualmente para alinear su merchandising con los intereses de los clientes.

## Consultas sin resultados

**CRÍTICO PARA LA MEJORA** - Las consultas sin resultados son un tesoro para optimizar su tienda.

Las consultas sin resultados ocurren por tres razones principales:

### 1. Productos faltantes

Los clientes buscan productos que no vende.

**Ejemplo**: Búsquedas repetidas por "alfombras de yoga" pero solo vende equipo de fitness, no suministros de yoga.

**Acción**: Considere agregar estos productos a su catálogo si las búsquedas son frecuentes.

### 2. Sinónimos faltantes

Los clientes usan términos que no coinciden con sus descripciones de productos.

**Ejemplo**: Los clientes buscan "laptop" pero todos sus productos dicen "ordenador portátil".

**Acción**: Cree un mapeo de sinónimos que asocie los términos de los clientes con el lenguaje de sus productos. Consulte [Gestión de sinónimos y redirecciones](/en/admin/help/managing-synonyms-redirects/).

### 3. Emparejamiento difuso pobre

Errores de escritura o errores ortográficos no coinciden incluso con el emparejamiento difuso habilitado.

**Ejemplo**: La búsqueda "accomodate" no encuentra productos de "accommodate".

**Acción**:
- Reduzca el umbral de similitud en **Configuración de búsqueda > pestaña de emparejamiento difuso** (de 0.80 a 0.75)
- Agregue sinónimos unidireccionales para errores ortográficos comunes

**Flujo de trabajo semanal**:
1. Revise las consultas sin resultados cada lunes
2. Clasifique: productos faltantes, sinónimos faltantes o errores de escritura
3. Agregue sinónimos para términos frecuentemente buscados
4. Anote las lagunas de productos para la planificación del inventario

## Detalles de la consulta

Haga clic en cualquier consulta de la lista para ver los detalles completos:

**Campos seguidos**:
- **Texto de la consulta** - Qué buscó el cliente
- **Marca de tiempo** - Cuándo ocurrió la búsqueda
- **Conteo de resultados** - Cuántos resultados se devolvieron
- **Tiempo de respuesta** - Milisegundos para ejecutar (monitoreo de rendimiento)
- **Usuario** - Cliente conectado (si el seguimiento de usuarios está habilitado)
- **ID de sesión** - Identificador de sesión anónimo
- **Idioma** - Idioma de la tienda durante la búsqueda
- **Motor** - Qué motor de búsqueda procesó la consulta

## Filtros y búsqueda

Use filtros para analizar segmentos específicos:

**Jerarquía de fechas** - Filtre por fecha, mes o año

**Filtro de idioma** - Ve las búsquedas por idioma (útil para tiendas multilingües)

**Filtro de motor** - Compare el comportamiento de búsqueda entre diferentes motores

**Conmutador de resultados nulos** - Muestra solo consultas que devolvieron ningún resultado

**Cuadro de búsqueda** - Encuentre texto de consulta específico

## Exportar datos

Haga clic en **Exportar** para descargar los datos de consulta como CSV para un análisis más profundo en Excel o herramientas de datos.

**CSV incluye**:
- Todo el texto de consulta
- Marcas de tiempo
- Conteos de resultados
- Tiempos de respuesta
- Datos de idioma y motor

Use las exportaciones para:
- Análisis de tendencias con el tiempo
- Identificar patrones de búsqueda estacionales
- Auditoría de rendimiento
- Presentación a partes interesadas

## Consideraciones de privacidad

El seguimiento de análisis de búsqueda respeta la privacidad:

**Seguimiento de usuarios** (opcional) - Vincula las búsquedas a cuentas de clientes conectados. Désablelo para cumplir con GDPR/CCPA en **Configuración de búsqueda > pestaña de análisis**.

**Seguimiento de sesiones** (por defecto) - Usa IDs de sesión anónimos para seguir patrones de búsqueda sin identificar a los clientes. Amigable con la privacidad.

**Retención de datos** - Las consultas de búsqueda permanecen en la base de datos de forma indefinida. Implemente una política de retención personalizada si es necesaria para cumplir con normativas.

## Usando el análisis para mejorar la búsqueda

Insights accionables del análisis de búsqueda:

**Tareas semanales**:
- Revise los resultados nulos y agregue sinónimos para términos comunes
- Monitorea los tiempos de respuesta y optimiza si son consistentemente lentos
- Identifica las búsquedas principales y asegúrate de que esos productos estén bien surtidos

**Tareas mensuales**:
- Analiza las consultas principales para informar la selección de productos
- Exporta datos para identificar tendencias estacionales
- Revisa patrones de búsqueda específicos de idioma
- Rastrea el número de clics en redirecciones para optimizar atajos de navegación

**Tareas trimestrales**:
- Revisa la efectividad de los sinónimos (¿han disminuido los resultados nulos?)
- Compara el crecimiento del volumen de búsqueda con el tráfico general
- Prueba A/B cambios de peso y mide la relevancia de los resultados
- Revisa si se deben agregar nuevas categorías de productos basado en la demanda de búsqueda

## Consejos

- **Las consultas sin resultados son tesoros para la mejora** - Indican directamente qué quieren los clientes y no proporcionan
- **Revise el análisis los lunes por la mañana** - Comience su semana optimizando según los datos de la semana anterior
- **Tiempo de respuesta >300ms consistentemente = investigar** - Revise primero la configuración de caché, luego las características de índice profundo
- **Exporte CSV para el análisis de tendencias** - El análisis en hojas de cálculo revela patrones no obvios en la interfaz de administración
- **Cree sinónimos antes de agregar productos** - Si los clientes buscan "fundas para tabletas" pero usted las llama "cubiertas protectoras", agregue el sinónimo primero
- **Rastree patrones de búsqueda estacionales** - "Botas de invierno" en octubre, "traje de baño" en marzo - ajuste el inventario según corresponda