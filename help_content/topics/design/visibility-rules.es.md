---
title: Reglas de visibilidad
---

# Reglas de visibilidad

Las reglas de visibilidad le permiten mostrar o ocultar partes de su tienda en línea según quién esté visitando y desde dónde. Puede restringir **elementos de página**, **elementos del menú** y **widgets del encabezado/pie de página** con las mismas condiciones: el mercado o región del cliente, el idioma o moneda en que está visualizando, la hora del día, o señales por visitante, como si está registrado o no.

Todo está construido a partir de **grupos de reglas**: un conjunto con nombre, reutilizable de uno o más condiciones. Crea un grupo de reglas una vez (por ejemplo, "mercado de Nueva Zelanda" o "miembros registrados") y luego lo adjuntas a cualquier elemento, elemento de menú o widget que desees que controle. Un elemento al que no se le hayan adjuntado grupos de reglas siempre es visible.

## Cómo se decide la visibilidad

Cuando a un elemento se le adjuntan más de un grupo de reglas, el elemento se muestra si **alguno** de los grupos adjuntos coincide (se combinan con OR). Dentro de un solo grupo, elige si **todos** o **alguno** de sus condiciones deben coincidir.

Las reglas se dividen en dos familias, y Spwig las maneja de manera diferente para que tu tienda se mantenga rápida y amigable con los motores de búsqueda:

- **Reglas de mercado** — condiciones basadas en región/mercado, idioma, moneda y hora. Estas se deciden en el servidor para cada URL de mercado, por lo que la misma página se entrega de la misma forma a cada visitante (y a cada motor de búsqueda) en esa dirección. Esto mantiene las páginas cachable y seguras para el SEO.
- **Reglas por visitante** — estado de registro, contenido del carrito, dispositivo y ubicación precisa. Estas dependen del visitante individual, por lo que Spwig las resuelve de forma privada para cada persona después de que se carga la página. Nunca se horadan en una página compartida, en caché.

Si deshabilitas un grupo de reglas, simplemente deja de aplicarse: el elemento al que estaba adjunto vuelve a ser visible. Deshabilitar un grupo no es una forma de ocultar algo.

## Crear y adjuntar reglas

Hay dos formas de trabajar con grupos de reglas.

### Ádjalos donde diseñes

En cualquier lugar donde puedas restringir contenido, verás un **control de visibilidad** (el icono del ojo):

- **Constructor de páginas** — selecciona un elemento, abre sus propiedades y usa el control de visibilidad.
- **Constructor de menú** — selecciona un elemento de menú y abre la pestaña **Visibilidad**. Esto funciona en **cualquier** elemento, incluido un elemento de submenú (desplegable) anidado bajo otro — una regla en un hijo oculta solo ese hijo, dejando el resto del menú intacto.
- **Constructor de encabezado y pie de página** — selecciona un widget y abre la sección **Grupos de reglas de visibilidad** de sus configuraciones.

Las reglas que dependen del visitante individual — si está registrado, qué hay en su carrito o su dispositivo — se resuelven para cada comprador sin hacer lenta tu tienda ni afectar a los motores de búsqueda. Tu tienda sigue rápida y cachable, y cada visitante ve solo la navegación correspondiente a él.

En el editor de visibilidad puedes:

- **Adjuntar** cualquier grupo de reglas existente marcándolo.
- **Regla rápida** — crear un grupo de reglas sencillo en el acto (por ejemplo, "solo miembros", un mercado único, una moneda, un dispositivo o un valor mínimo en el carrito) y adjuntarlo en un solo paso.
- **Administrar grupos de reglas** — ir al constructor completo para reglas avanzadas.

Haz clic en **Aplicar** y el elemento queda restringido inmediatamente.

### Crear reglas avanzadas

Para cualquier cosa más compleja — combinar varias condiciones, anidar grupos o usar operadores detallados — ve a **Diseño → Reglas de visibilidad** (grupos de reglas). Allí puedes ensamblar reglas con lógica AND/OR y reutilizarlas en toda tu tienda.

## Condiciones comunes

Preserve all markdown formatting, image paths, code blocks, and technical terms.

| Condition | Use it to… |
|-----------|------------|
| **Región / mercado** | Mostrar un bloque solo a los visitantes de un mercado específico (por ejemplo, Nueva Zelanda) |
| **Moneda seleccionada** | Mostrar notas de precios o ofertas solo cuando se active una cierta moneda |
| **Idioma seleccionado** | Mostrar contenido solo en un idioma específico |
| **Fecha / hora / día / horario comercial** | Ejecutar un banner durante una ventana de venta o solo durante horas de apertura |
| **Estado de inicio de sesión** | Mostrar contenido "solo para miembros", o un recordatorio de registro para invitados |
| **Tipo de dispositivo** | Mostrar o ocultar algo en dispositivos móviles, tabletas o escritorio |
| **Valor del carrito / artículos** | Mostrar una sugerencia de envío gratis una vez que el carrito supere un umbral |

## Vista previa

En la vista previa del Page Builder, puede **previsualizar como un mercado** y **previsualizar como un visitante** (con inicio de sesión o como invitado, con un carrito de ejemplo) para ver exactamente lo que vería cada audiencia — incluyendo las reglas por visitante que normalmente se resuelven de forma privada.

## Consejos

- Cree un pequeño conjunto de grupos de reglas bien nombrados ("mercado NZ", "Miembros", "Solo móvil") y úselos en todas partes: es más fácil de gestionar que reglas puntuales.
- Las reglas de mercado son la opción segura para cualquier cosa que desee que los motores de búsqueda indexen, porque el resultado es el mismo para todos en una URL de mercado dada.
- Si un artículo desaparece inesperadamente, verifique sus grupos de reglas adjuntos: un artículo está oculto solo cuando tiene un grupo activo y ninguno de sus grupos coincide con el visitante actual.