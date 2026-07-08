---
title: Trabajos de traducción
---

Los trabajos de traducción automatizan la traducción en masa de grandes cantidades de contenido. En lugar de traducir manualmente los productos uno por uno, cree un trabajo que traduzca su catálogo completo o subconjuntos específicos en segundo plano. Los trabajos se ejecutan de forma asincrónica, por lo que puede continuar trabajando mientras cientos o miles de campos se traducen automáticamente.

Use trabajos de traducción cuando active nuevos idiomas, importe nuevos productos o corrija contenido no traducido.

## ¿Qué son los trabajos de traducción?

Un trabajo de traducción es una tarea en segundo plano que:

1. **Escanea el contenido** en busca de campos traducibles (productos, páginas, entradas de blog, etc.)
2. **Identifica campos no traducidos o obsoletos** según el alcance de su trabajo
3. **Envía los campos al motor de traducción** (modelo de IA local o proveedor externo)
4. **Guarda las traducciones** de vuelta en su contenido
5. **Reporta la finalización** con estadísticas sobre los campos traducidos

Los trabajos se ejecutan a través de la cola de tareas Celery, por lo que no bloquean su interfaz de administración.

## ¿Cuándo usar trabajos de traducción

**Lanzamiento de un nuevo idioma**:
- Active el alemán como nuevo idioma
- Cree trabajo: Traduzca todos los productos del inglés al alemán
- Resultado: Catálogo completo disponible en alemán en minutos/horas (dependiendo del tamaño)

**Importación de nuevos productos**:
- Importe 500 nuevos productos en inglés
- Cree trabajo: Traduzca los nuevos productos a todos los idiomas activos
- Resultado: Nuevo inventario disponible inmediatamente en todos los mercados

**Corregir lagunas**:
- El informe de cobertura muestra que los productos solo están un 60% traducidos al francés
- Cree trabajo: Traduzca solo los campos de productos faltantes en francés
- Resultado: La cobertura en francés aumenta hasta ~100%

**Actualizar traducciones obsoletas**:
- El modelo de traducción se mejoró o hay un proveedor nuevo disponible
- Cree trabajo: Re-traduzca todos los productos al español
- Resultado: Traducciones de mayor calidad en todo el catálogo

## Crear un trabajo de traducción

Navegue hasta **Configuración > Trabajos de traducción** y haga clic en **+ Crear trabajo**.

### Configuración del trabajo

**Nombre del trabajo** - Etiqueta descriptiva (ej. "Traducir productos al alemán", "Nuevos artículos de blog - todos los idiomas")

**Tipo de contenido** - ¿Qué traducir?:
- Productos
- Categorías de productos
- Páginas
- Entradas de blog
- Metadatos de SEO
- Plantillas de correo electrónico
- Todos los tipos de contenido

**Idioma de origen** - El idioma del que se está traduciendo (normalmente su idioma predeterminado)

**Idioma(s) de destino** - Un o más idiomas a los que se traduce (seleccione varios para traducción paralela)

**Alcance** - ¿Qué subconjunto de contenido?:
- **Todos los elementos** - Traduzca todo, independientemente de las traducciones existentes
- **Solo los no traducidos** - Salte los campos que ya tienen traducciones
- **Creados/actualizados desde una fecha** - Solo contenido nuevo o recientemente cambiado
- **Elementos específicos** - Seleccione productos/páginas individuales (filtrado avanzado)

**Motor de traducción** - ¿Qué servicio usar?:
- Modelo de IA local (predeterminado, sin costos de API)
- Proveedor externo específico (DeepL, Google, Azure, AWS)
- Auto-seleccionar (usa la preferencia configurada)

**Bloquear traducciones** - ¿Bloquear los campos traducidos contra la sobrescritura futura automática? (útil para traducciones revisadas)

### Opciones avanzadas

**Saltar campos bloqueados** - Si está habilitado, respeta las traducciones bloqueadas existentes (recomendado)

**Sobrescribir existentes** - Re-traducir incluso si existen traducciones (use para mejoras de calidad)

**Filtros de campos** - Traducir solo campos específicos (ej. nombres y descripciones de productos, saltar atributos)

**Tamaño de lote** - ¿Cuántos elementos procesar a la vez? (predeterminado: 50, aumente para un procesamiento más rápido si el servidor puede manejarlo)

**Prioridad** - Los trabajos de alta prioridad se ejecutan antes que los de prioridad normal (use con moderación)

## Ciclo de vida y estado del trabajo

Los trabajos pasan por estos estados:

**En cola** - Trabajo creado, esperando que un trabajador lo recoja

**Procesando** - Trabajador traduciendo activamente el contenido

**Completado** - Todas las traducciones finalizadas con éxito

**Fallido** - El trabajo encontró errores (ver registro de errores)

**Cancelado** - Detenido manualmente por el administrador

**Pausado** - Pausado temporalmente (se puede reanudar)

## Monitoreo del progreso del trabajo

La página de detalles del trabajo muestra:

**Barra de progreso** - Porcentaje completado

**Estadísticas**:
- Elementos totales a traducir
- Elementos completados
- Elementos restantes
- Tiempo estimado restante

**Registro en tiempo real** - Flujo de actividad de traducción (útil para solucionar problemas)

**Conteo de errores** - ¿Cuántos campos fallaron en la traducción? (con razones)

## Resultados y estadísticas del trabajo

Cuando un trabajo se completa, la página de resultados muestra:

**Resumen**:
- Campos procesados en total
- Traducciones exitosas
- Traducciones fallidas
- Saltados (ya traducidos, bloqueados o excluidos por filtros)

**Desglose por elemento**:
- ¿Qué productos/páginas se tradujeron?
- ¿Cuántos campos por elemento?
- Cualquier error encontrado

**Métricas de rendimiento**:
- Tiempo total transcurrido
- Promedio de traducciones por segundo
- Motor de traducción usado

## Manejo de traducciones fallidas

Si algunas traducciones fallan:

**Revisar el registro de errores** - Identifica qué campos fallaron y por qué

**Causas comunes de falla**:
- Límite de tasa de API alcanzado (proveedor externo)
- Tiempo de espera del motor de traducción (texto muy largo)
- Formato de campo inválido (error de análisis JSON)
- Modelo no admite el par de idiomas

**Opciones de reintento**:
- Corrija el problema subyacente
- Cree un nuevo trabajo solo para los elementos fallidos
- Use un motor de traducción diferente

## Cancelar y pausar trabajos

**Cancelar** - Detiene el trabajo inmediatamente, descarta cualquier traducción en proceso (las traducciones completadas se guardan)

**Pausar** - Detiene temporalmente el trabajo, puede reanudar más tarde desde donde lo dejó

**Reanudar** - Continúa un trabajo pausado

Use pausar/reanudar cuando necesite liberar recursos del servidor temporalmente.

## Estrategias de trabajos en masa

**Estrategia 1: Idioma por idioma**:
- Cree trabajos separados para cada idioma de destino
- Más fácil monitorear el progreso por idioma
- Puede priorizar idiomas importantes
- Distribuye la carga con el tiempo

**Estrategia 2: Todo a la vez**:
- Un solo trabajo traduciendo a todos los idiomas activos
- Finalización más rápida en general
- Mayor carga del servidor durante el procesamiento
- Gestión de trabajos más simple

**Estrategia 3: Tipo de contenido por tipo de contenido**:
- Traduzca primero los productos (prioridad más alta)
- Luego categorías, páginas, entradas de blog
- Permite un despliegue progresivo
- Más fácil probar y verificar traducciones

Elija según su capacidad del servidor, urgencia y tamaño del catálogo.

## Programación de trabajos

Programar trabajos recurrentes para manejar automáticamente el contenido nuevo:

**Trabajos diarios** - Traduzca cualquier producto creado/actualizado en las últimas 24 horas

**Trabajos semanales** - Corrija lagunas de traducción semanalmente

**Después de la importación** - Inicie el trabajo automáticamente después de la importación en masa de productos

**Al activar un idioma** - Cree automáticamente el trabajo al activar un nuevo idioma

Los trabajos programados mantienen las traducciones actualizadas sin intervención manual.

## Consideraciones de rendimiento

**Modelo de IA local**:
- ~100-500 traducciones/segundo (dependiendo del servidor)
- Intensivo en CPU durante el procesamiento
- Sin límites de tasa de API
- Gratis (sin costo por traducción)

**Proveedores externos**:
- Los límites de tasa varían (DeepL: 500k caracteres/mes en la versión gratuita)
- Latencia de API agrega sobrecarga
- Mejor calidad pero cuesta dinero
- Límites de solicitudes concurrentes

**Trabajos grandes** (>10,000 campos):
- Ejecute durante horas de poca demanda
- Monitoree los recursos del servidor
- Considere dividir en lotes más pequeños
- Pruebe con un subconjunto primero

## Consejos

- **Empiece pequeño** - Pruebe trabajos en un subconjunto (ej. 10 productos) antes de ejecutar la traducción del catálogo completo
- **Use el alcance "Solo los no traducidos"** - Más rápido y evita re-traducir contenido ya bueno
- **Monitorea el primer trabajo cuidadosamente** - Observe errores o problemas de calidad antes de lanzar trabajos más grandes
- **Programa trabajos durante períodos de baja demanda** - La traducción es intensiva en CPU/API
- **Bloquee traducciones revisadas** - Evita que los trabajos masivos sobrescriban sus ediciones manuales
- **Mantenga los trabajos enfocados** - Los trabajos más pequeños y específicos son más fáciles de solucionar que los trabajos masivos "traduzca todo"
- **Revisa muestras después de la finalización** - Verifique traducciones aleatorias para la calidad antes de considerar el trabajo exitoso
- **Exporta/copia de seguridad antes de trabajos importantes** - En caso de que necesite revertir cambios masivos

Recuerde: preserve all markdown formatting, image paths, code blocks, and technical terms exactly as shown in the preservation rules.