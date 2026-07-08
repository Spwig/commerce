---
title: Gestion de sinónimos y redirecciones
---

Los sinónimos y las redirecciones hacen que tu búsqueda sea más inteligente al manejar términos equivalentes y enrutar consultas específicas a páginas específicas. Los sinónimos amplían las búsquedas para incluir términos relacionados ("laptop" también encuentra "notebook"), mientras que las redirecciones envían consultas como "sale" directamente a tu página de ventas. Esta guía explica cómo crear y gestionar ambas funciones para mejorar la relevancia de la búsqueda y la experiencia del cliente.

Utiliza sinónimos para equivalencia de términos y redirecciones para atajos de navegación.

![Lista de sinónimos](/static/core/admin/img/help/managing-synonyms-redirects/synonym-list.webp)

## Entendiendo los sinónimos

Los sinónimos le dicen al sistema de búsqueda que ciertos términos deben tratarse como equivalentes. Cuando un cliente busca un término, el sistema incluye automáticamente resultados que coinciden con los términos de sinónimos.

**Ejemplo**: Crea un mapeo de sinónimos "laptop" → "notebook", "portable computer". Ahora, cuando alguien busca "laptop", también obtiene resultados para productos que contienen "notebook" o "portable computer" en sus nombres o descripciones.

Los sinónimos son especialmente valiosos para:
- Inglés británico vs. estadounidense (jumper/sweater, trainers/sneakers)
- Términos de marca vs. términos genéricos (tissues/Kleenex)
- Errores comunes de escritura (accommodate/accomodate)
- Jerga de la industria vs. lenguaje común (CPU/processor)

## Creando sinónimos

Navega a **Search > Synonyms** y haz clic en **+ Add Synonym**.

![Formulario de agregar sinónimo](/static/core/admin/img/help/managing-synonyms-redirects/synonym-form.webp)

**Term** - El término de búsqueda original que desencadena la expansión de sinónimos

**Synonyms** - Matriz JSON de términos equivalentes, p. ej. `['sweater', 'pullover', 'jumper']`

**Bidirectional** - Por defecto: Marcado. Cuando está habilitado, las relaciones de sinónimos funcionan en ambas direcciones:
- Buscar "laptop" encuentra productos "notebook"
- Buscar "notebook" encuentra productos "laptop"

Desmarcar para mapeos unidireccionales (ver abajo).

**Language** - Opcional. Restringe este sinónimo a búsquedas en un idioma específico. Deja en blanco para aplicarlo a todos los idiomas.

**Engine** - Opcional. Restringe este sinónimo a un motor de búsqueda específico. Deja en blanco para aplicarlo globalmente.

**Active** - Si este sinónimo se está usando actualmente. Desmarcarlo para deshabilitarlo temporalmente sin eliminarlo.

## Ejemplos bidireccionales

La mayoría de los sinónimos deben ser bidireccionales - verdaderos equivalentes que funcionan en ambas direcciones:

| Término | Sinónimos | Caso de uso |
|--------|----------|------------|
| laptop | notebook, portable computer | Inglés británico/estadounidense + términos genéricos |
| sofa | couch, settee | Variaciones regionales |
| trainers | sneakers, running shoes | Inglés británico/estadounidense |
| mobile | cell phone, cellular | Variaciones internacionales |

Con el bidireccional habilitado, todos estos términos encuentran los mismos productos independientemente del término que use el cliente.

## Ejemplos unidireccionales

Desmarque "Bidirectional" para relaciones unidireccionales:

**Casos de uso comunes**:
- **Errores de escritura**: Término: "acco

mmodate" → Sinónimos: `['accommodate']` (unidireccional para que la escritura correcta no encuentre el error)
- **Específico → Genérico**: Término: "MacBook" → Sinónimos: `['laptop']` (los MacBooks son laptops, pero no todas las laptops son MacBooks)
- **Abreviaturas**: Término: "CPU" → Sinónimos: `['processor']` (CPU encuentra productos de procesador, pero las búsquedas de procesador no deben siempre incluir CPU)

## Sinónimos específicos de idioma

Utilice el campo de idioma para crear sinónimos adecuados a la región:

**Ejemplo**: Tienda de inglés británico
- Término: "jumper", Sinónimos: `['sweater', 'pullover']`, Idioma: Inglés (Reino Unido)
- Término: "trainers", Sinónimos: `['sneakers']`, Idioma: Inglés (Reino Unido)

**Ejemplo**: Tienda multilingüe
- Término: "ordinateur portable", Sinónimos: `['laptop', 'notebook']`, Idioma: Francés
- Término: "zapatos", Sinónimos: `['shoes']`, Idioma: Español

Los sinónimos específicos de idioma solo se aplican cuando un cliente navega en ese idioma.

## Sinónimos específicos del motor

La mayoría de los sinónimos deben aplicarse globalmente (dejar el campo del motor en blanco). Utilice sinónimos específicos del motor solo cuando diferentes contextos de búsqueda necesiten diferentes mapeos de términos:

**Ejemplo**: Tienes motores separados de "shop" y "blog"
- Sinónimo del blog: Término: "tutorial" → Sinónimos: `['guide', 'how-to']`, Motor: blog
- Este sinónimo solo se aplica a búsquedas de blog, no a búsquedas de productos

## Entendiendo las redirecciones

Las redirecciones de búsqueda envían consultas específicas directamente a páginas designadas, saltando los resultados de búsqueda normales. Usa redirecciones cuando sepas exactamente a dónde debe ir un cliente.

**Ejemplo**: Crea una redirección para "sale" → "/products/sale/". Ahora, cuando alguien busca "sale", salta los resultados de búsqueda y llega directamente a tu página de ventas.

Las redirecciones son perfectas para:
- Atajos de navegación comunes ("returns" → página de política de devoluciones)
- Promociones estacionales ("summer sale" → colección de verano)
- Categorías populares ("laptops" → página de categoría de laptops)
- Páginas de política ("shipping" → información de envío)

![Lista de redirecciones](/static/core/admin/img/help/managing-synonyms-redirects/redirect-list.webp)

## Tipos de coincidencia

Las redirecciones admiten cuatro tipos de coincidencia que controlan cuán estrictamente la consulta de búsqueda debe coincidir:

**Exacta** - Coincidencia exacta insensible a mayúsculas. La consulta debe coincidir exactamente con el término (ignorando mayúsculas).
- Término: "sale"
- Coincide: "sale", "SALE", "Sale"
- No coincide: "summer sale", "on sale"

**Contiene** - La consulta contiene el término en cualquier lugar.
- Término: "sizing"
- Coincide: "sizing guide", "help with sizing", "what sizing"
- No coincide: "size chart" (palabra diferente)

**Comienza con** - La consulta comienza con el término.
- Término: "return"
- Coincide: "returns", "return policy", "returning items"
- No coincide: "how to return" (no comienza con el término)

**Regex** - Coincidencia de patrones usando expresiones regulares. **⚠️ Cuidado con el rendimiento** - los patrones de regex complejos ralentizan las búsquedas. Use con moderación.
- Patrón: `^(laptop|notebook)s?$`
- Coincide: "laptop", "laptops", "notebook", "notebooks"
- Use solo si otros tipos de coincidencia no funcionan

## Creando redirecciones

Navega a **Search > Redirects** y haz clic en **+ Add Redirect**.

![Formulario de agregar redirección](/static/core/admin/img/help/managing-synonyms-redirects/redirect-form.webp)

**Term** - La consulta de búsqueda a coincidir

**Match Type** - Exacto, Contiene, Comienza con o Regex (ver arriba)

**Redirect URL** - A dónde enviar al cliente. Puede ser relativo (`/products/sale/`) o absoluto (`https://example.com/page/`)

**Redirect Type** - Código de estado HTTP:
- **302 (Temporal)**: Recomendado. El navegador no lo almacena en caché, puedes cambiar el destino más tarde
- **301 (Permanente)**: El navegador y los motores de búsqueda lo almacenan en caché. Solo úsalo para redirecciones permanentes

**Engine** - Opcional. Restringe a un motor de búsqueda específico

**Hit Count** - Se incrementa automáticamente cada vez que se usa esta redirección. Ayuda a identificar atajos de navegación más usados.

**Active** - Habilitar/deshabilitar esta redirección

## Ejemplos de redirección

| Término | Tipo de coincidencia | URL | Caso de uso |
|--------|---------------------|-----|------------|
| sale | Exacta | `/products/sale/` | Redirección directa de "sale" a la página de ventas |
| clearance | Exacta | `/clearance/` | Saltar la búsqueda para artículos de liquidación |
| sizing | Contiene | `/pages/size-guide/` | Cualquier consulta sobre tallas va al guía |
| return | Comienza con | `/pages/returns/` | Consultas relacionadas con devoluciones van a la política |

Todos usan redirecciones 302 (temporales) para flexibilidad.

## Tipo de redirección: 302 vs 301

**302 (Temporal)** - Recomendado para la mayoría de las redirecciones
- El navegador hace una solicitud fresca cada vez
- Puedes cambiar la URL de destino en cualquier momento
- Elección más segura si no estás seguro

**301 (Permanente)** - Úsalo con moderación
- El navegador almacena la redirección
- Los motores de búsqueda actualizan sus índices
- Más difícil de cambiar después

**Recomendación**: Usa 302 a menos que estés absolutamente seguro de que la redirección nunca cambiará.

## Análisis de conteo de aciertos

El campo de conteo de aciertos se incrementa automáticamente cada vez que se dispara una redirección. Úsalo para:
- Identificar los atajos de navegación más usados
- Encontrar redirecciones que nunca se usan (considera eliminarlas)
- Descubrir patrones populares de búsqueda

Revisa los conteos de aciertos mensualmente para optimizar tu estrategia de redirección.

## Encontrando oportunidades de sinónimos

**Usa consultas con cero resultados**: Navega a **Search > Search Analytics** y filtra por consultas con cero resultados. Estas revelan:
- Términos que los clientes usan que no coinciden con las descripciones de tus productos
- Variaciones regionales que no has considerado
- Errores comunes de escritura

**Flujo de trabajo**:
1. Revisa las consultas con cero resultados semanalmente
2. Identifica patrones (términos que aparecen repetidamente)
3. Añade sinónimos para mapear el lenguaje del cliente a los nombres de tus productos
4. Monitorea si las consultas con cero resultados disminuyen

## Consejos

- **Monitorea las consultas con cero resultados semanalmente para ideas de sinónimos** - Revelan brechas entre el lenguaje del cliente y las descripciones de tus productos
- **Empieza con sinónimos comunes, expande basado en datos** - Comienza con variaciones regionales obvias, luego añade basado en el comportamiento real de búsqueda
- **Usa bidireccional para verdaderos equivalentes** - La mayoría de los sinónimos deben funcionar en ambas direcciones (laptop ↔ notebook)
- **Evita patrones de regex complejos** - La coincidencia de regex es más lenta que otros tipos de coincidencia; úsala solo cuando sea necesario
- **Usa redirecciones 302 (temporales) por defecto** - Te da flexibilidad para cambiar destinos más tarde
- **Prueba sinónimos con consultas reales** - Busca por términos de sinónimos para verificar que devuelvan los resultados esperados
- **Sinónimos específicos de idioma para tiendas multilingües** - Crea mapeos de términos adecuados a la región para cada idioma que soportes

Recuerda: Preserva todo el formato de markdown, rutas de imágenes, bloques de código y términos técnicos exactamente como se muestran en las reglas de preservación.