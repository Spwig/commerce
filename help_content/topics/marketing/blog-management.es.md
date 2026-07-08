---
title: Gestión de Blog
---

El blog le permite publicar artículos, guías y noticias para atraer tráfico y comprometer a su audiencia. El blog de Spwig incluye un editor de texto enriquecido, programación de publicación, notificaciones a suscriptores, compartido automáticamente en redes sociales, y herramientas de SEO.

![Blog posts](/static/core/admin/img/help/blog-management/blog-post-list.webp)

## Crear una entrada de blog

Navegue hasta **Marketing > Entradas de blog** y haga clic en **Agregar entrada**.

### Contenido de la entrada

Escriba su entrada usando el editor de texto enriquecido **CKEditor 5**, que admite:
- Formateo de texto (encabezados, negrita, cursiva, listas, citas)
- Imágenes y medios (cargados a través de la biblioteca de medios)
- Videos incrustados (YouTube, Vimeo)
- Tablas y bloques de código
- Enlaces a productos, categorías y URLs externas

Para diseños más complejos, active el interruptor **Page Builder** para usar el constructor de páginas de arrastrar y soltar en lugar del editor de texto.

### Configuración de la entrada

| Configuración | Descripción |
|---------|-------------|
| **Título** | El titular mostrado en el blog y en los resultados de búsqueda |
| **Slug** | Identificador amigable para URLs (generado automáticamente a partir del título, editable) |
| **Extracto** | Resumen corto mostrado en las tarjetas de lista del blog y en los feeds RSS |
| **Imagen destacada** | Imagen principal mostrada en la parte superior de la entrada y en las tarjetas de lista |
| **Categoría** | Categoría principal para la entrada |
| **Etiquetas** | Palabras clave para filtrar y contenido relacionado |
| **Autor** | Miembro del personal creditado como autor |
| **Estado** | Borrador, Programado, Publicado o Archivado |
| **Destacado** | Fije la entrada en la parte superior de la lista del blog |

### Configuración de SEO

Cada entrada incluye campos de SEO:
- **Título meta** — Título personalizado para los resultados de los motores de búsqueda (por defecto es el título de la entrada)
- **Descripción meta** — Resumen mostrado en los resultados de los motores de búsqueda
- **Imagen de Open Graph** — Imagen utilizada cuando la entrada se comparte en redes sociales

## Estados de la entrada

| Estado | Descripción |
|--------|-------------|
| **Borrador** | Trabajo en progreso, no visible para el público |
| **Programado** | Se publicará automáticamente en una fecha y hora establecidas |
| **Publicado** | Activo y visible para los visitantes |
| **Archivado** | Oculto de la lista del blog pero aún accesible a través de la URL directa |

### Programar entradas

Para programar una entrada para publicación futura:
1. Establezca el estado en **Programado**
2. Elija la **fecha y hora de publicación**
3. Guarde la entrada

Una tarea en segundo plano publica automáticamente la entrada en el tiempo programado y activa las notificaciones a los suscriptores.

## Categorías

Navegue hasta **Marketing > Categorías de blog** para organizar su contenido.

Las categorías admiten:
- **Jerarquía** — Cree categorías padre e hijo (por ejemplo, "Guías" > "Comenzando")
- **URLs personalizadas** — Cada categoría tiene su propio slug para URLs limpias
- **Descripciones** — Agregue descripciones de categorías mostradas en la página de archivo de categorías
- **Orden** — Controla el orden de visualización de las categorías en la navegación

## Etiquetas

Las etiquetas ofrecen una forma secundaria de clasificar el contenido. A diferencia de las categorías (que son jerárquicas), las etiquetas son etiquetas planas. Los visitantes pueden hacer clic en una etiqueta para ver todas las entradas con esa etiqueta.

## Suscriptores

Navegue hasta **Marketing > Suscriptores del blog** para administrar su lista de suscriptores.

### Cómo funcionan las suscripciones

1. Los visitantes se suscriben a través de un formulario en el blog (requiere dirección de correo electrónico)
2. Se envía un correo electrónico de **confirmación de doble opt-in**
3. Una vez confirmado, el suscriptor recibe notificaciones cuando se publiquen nuevas entradas

### Frecuencia de notificación

Los suscriptores eligen con qué frecuencia reciben notificaciones:

| Frecuencia | Descripción |
|-----------|-------------|
| **Inmediata** | Correo electrónico enviado tan pronto como se publique una nueva entrada |
| **Resumen semanal** | Un resumen semanal de todas las nuevas entradas |
| **Resumen mensual** | Un resumen mensual de todas las nuevas entradas |

Las tareas en segundo plano manejan automáticamente la compilación y entrega de resúmenes.

### Administrar suscriptores

- Ver el recuento de suscriptores, el estado de confirmación y la fecha de registro
- Exportar listas de suscriptores para su uso en herramientas de marketing por correo electrónico externas
- Eliminar o dar de baja direcciones individuales
- Cada correo electrónico de notificación incluye un enlace de **darse de baja** con un solo clic

## Compartido automáticamente en redes sociales

Spwig puede compartir automáticamente nuevas entradas en sus cuentas de redes sociales cuando se publican.

### Conectar cuentas de redes sociales

Navegue hasta **Marketing > Conectores de redes sociales** para conectar sus cuentas:

| Plataforma | Autenticación |
|----------|---------------|
| **Facebook** | OAuth — conecte su Página de Facebook |
| **Instagram** | OAuth — conecte su cuenta empresarial |
| **LinkedIn** | OAuth — conecte su página de la empresa |

### Cómo funciona el compartir automático

1. Conecte una o más cuentas de redes sociales
2. Al crear una entrada, habilite **Compartir Automático** para cada cuenta conectada
3. Personalice el mensaje de compartir (por defecto es el título y el extracto de la entrada)
4. Cuando la entrada se publica (o alcanza su hora programada), se comparte automáticamente

El compartir automático también funciona con entradas programadas — el compartir en redes sociales se envía en el mismo momento en que la entrada se vuelve activa.

## RSS Feed

El blog genera automáticamente un feed RSS en `/blog/feed/`. Esto permite a los visitantes y agregadores suscribirse a su contenido. El feed incluye:
- Título y extracto de la entrada
- Fecha de publicación
- Información del autor
- Enlace directo a la entrada completa

## Configuración del blog

Navegue hasta **Marketing > Configuración del blog** para configurar opciones globales del blog:

- **Entradas por página** — Número de entradas mostradas por página en la lista
- **Permitir comentarios** — Habilitar o deshabilitar comentarios en las entradas
- **Categoría por defecto** — Categoría de respaldo para entradas sin una asignada
- **Botones de compartir en redes sociales** — Mostrar botones de compartir en páginas de entradas individuales

## Consejos

- Escriba entradas con **SEO en mente** — use títulos descriptivos, complete las descripciones meta y incluya palabras clave relevantes de forma natural en el contenido.
- Use **publicación programada** para mantener un ritmo de publicación consistente sin esfuerzo manual.
- Active **compartido automáticamente** para maximizar el alcance — las entradas compartidas en redes sociales poco después de la publicación obtienen más interacciones.
- Incentive a los visitantes a **suscribirse** colocando el formulario de suscripción de forma destacada en su blog y usando una llamada a la acción convincente.
- Use **categorías** para agrupar contenido amplio y **etiquetas** para temas específicos — esto ayuda a los visitantes a encontrar contenido relacionado.
- Agregue una **imagen destacada** a cada entrada — las entradas con imágenes tienen un mejor rendimiento en los resultados de búsqueda y en las compartidas en redes sociales.
- Use la opción de **resumen semanal o mensual** para suscriptores que no deseen recibir correos frecuentes — reduce las tasas de darse de baja.