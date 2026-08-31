---
title: Etiquetas de suscriptores
---

Las etiquetas son sus propias marcas para organizar la audiencia de su Campaign Studio: marcadores cortos como `VIP`, `wholesale` o `event-2026` que usted define y aplica a los suscriptores que correspondan. Una vez que existe una etiqueta, puede filtrar su lista de Suscriptores por ella, aplicarla o quitarla de cualquier número de personas a la vez y, lo más útil, usarla como una condición al crear un Segmento, de modo que sus campañas y recorridos puedan dirigirse exactamente a las personas que ha etiquetado.

## Qué son las etiquetas

Una etiqueta no es más que un nombre que usted elige. Spwig no incluye etiquetas integradas y nunca aplica una automáticamente: usted decide cómo se llaman y quién las recibe. Esto las hace adecuadas para cualquier cosa específica de su propio negocio que no corresponda a un estado que Spwig ya rastree: un nivel de lealtad, una cuenta mayorista, todos los que se registraron en una feria comercial o una lista de evento única como `event-2026`.

Cada etiqueta también recibe un **Slug**: una versión simplificada y segura para URL de su nombre, generada automáticamente al crearla. Los Segmentos y los filtros usan el slug internamente; como comerciante, casi nunca necesitará verlo.

## Crear una etiqueta

Las etiquetas tienen su propia sección de administración. Abra **Campaign Studio > Subscribers**, luego haga clic en **Campaign Studio** en la parte superior de la página para ver la lista completa de secciones de Campaign Studio y elija **Subscriber tags**.

1. Haga clic en **Add subscriber tag**.
2. Introduzca un **Name** (Nombre): lo más claro es que sea corto y específico, p. ej. `VIP`, `Wholesale` o `Event 2026`.
3. Spwig rellena un **Slug** correspondiente mientras escribe. Puede dejarlo como se generó.
4. También está disponible un campo opcional **Colour** (Color) si desea registrar un color hexadecimal (p. ej. `#2563eb`) junto a la etiqueta para su propia referencia.
5. Haga clic en **Save** (Guardar).

Tampoco tiene que dejar lo que está haciendo para crear una: un **+** verde junto al campo **Tags** (Etiquetas) en la página de edición de cualquier suscriptor abre el mismo formulario de "añadir una etiqueta" en una ventana emergente. Y si intenta etiquetar en bloque a suscriptores antes de haber creado etiquetas, el selector de etiquetas ofrece un acceso directo **Create a tag** (Crear una etiqueta) que lo lleva directamente allí.

## Etiquetar suscriptores

La forma más común de aplicar una etiqueta es en bloque, desde la lista de Suscriptores:

1. Abra **Campaign Studio > Subscribers**.
2. Marque la casilla de verificación de cada suscriptor al que desea etiquetar (o **Select all on this page** (Seleccionar todos en esta página)).
3. Desde el menú desplegable **Bulk actions** (Acciones en bloque), elija **Add tag to selected…** (Añadir etiqueta a los seleccionados…) (o **Remove tag from selected…** (Quitar etiqueta de los seleccionados…) para desetiquetar personas).
4. Haga clic en **Go** (Ir).
5. Elija la etiqueta de la lista y haga clic en **Add tag** (Añadir etiqueta) (o **Remove tag** (Quitar etiqueta)).

![El selector de etiquetas en bloque después de elegir "Add tag to selected…" para cuatro suscriptores](/static/core/admin/img/help/subscriber-tags/bulk-tag-picker.webp)

Una vez aplicada, una etiqueta se muestra como una pequeña insignia en la tarjeta del suscriptor en la lista, junto a sus insignias de estado y origen. Un filtro **Tag** (Etiqueta) también aparece en el panel de filtros de la lista de Suscriptores una vez que tiene al menos una etiqueta, de modo que puede reducir la lista a todos los que llevan una etiqueta específica: útil para comprobar quién está en una audiencia antes de crear una campaña en torno a ella.

![La lista de Suscriptores filtrada por la etiqueta VIP, con el botón Import CSV y las insignias de etiquetas visibles](/static/core/admin/img/help/subscriber-tags/subscriber-list-tag-chips.webp)

También puede añadir o quitar las etiquetas de un solo suscriptor directamente desde su página de edición, usando el mismo campo **Tags** (Etiquetas) que gestiona la acción en bloque.

## Usar etiquetas en segmentos

Los Segmentos son las audiencias guardadas y basadas en reglas a las que dirige sus campañas y recorridos. Una vez que ha creado al menos una etiqueta, una condición **Has tag** (Tiene etiqueta) se vuelve disponible en el creador de reglas del segmento: no aparece en una instalación nueva sin etiquetas definidas, por lo que no verá una opción inactiva antes de que sea útil para usted.

Para usarla, abra **Campaign Studio > Segments**, añada (o edite) un segmento dinámico y haga clic en **+ Add condition** (Añadir condición):

1. Establezca el campo de la condición en **Has tag** (Tiene etiqueta).
2. Elija un operador: **is** (es) para una sola etiqueta, o **is any of** (es cualquiera de) si prefiere formularlo así.
3. Elija la etiqueta del menú desplegable.

![Una condición "Tiene etiqueta" configurada en VIP, mostrando un recuento en vivo de los suscriptores que coinciden](/static/core/admin/img/help/subscriber-tags/segment-has-tag-rule.webp)

El recuento en la esquina superior derecha se actualiza a medida que construyes la regla, por lo que puedes ver exactamente cuántos suscriptores cumplen actualmente los criterios antes de guardar. Cada condición **Tiene etiqueta** coincide actualmente con una etiqueta a la vez; si deseas una audiencia que coincida con *cualquiera* de varias etiquetas (por ejemplo, `VIP` o `Wholesale`), añade una condición **Tiene etiqueta** por cada etiqueta y configura **Coincidencia** en **cualquiera**.

Esto es lo que hace que las etiquetas sean útiles más allá de la organización: un segmento construido sobre **Tiene etiqueta** se convierte en una audiencia que puedes seleccionar como **Segmento** en una campaña de difusión o recurrente, o como la configuración **Solo para segmento** de un recorrido; así, "todos los etiquetados como VIP" pueden tener su propia serie de bienvenida, su propio boletín recurrente, o simplemente ser quienes selecciones la próxima vez que envíes un anuncio único.

## Consejos

- Mantén los nombres de las etiquetas cortos y específicos: se muestran como chips compactos en las tarjetas de suscriptores, por lo que `VIP` se lee mejor que `Very Important Person - Tier 1`.
- Usa el filtro **Etiqueta** para verificar quién está realmente etiquetado antes de construir un segmento o enviar una campaña basada en él.
- El etiquetado es aditivo: eliminar una etiqueta de un suscriptor nunca afecta a ninguna otra etiqueta que tenga, y nunca modifica su estado, origen o consentimiento.
- Combina etiquetas con otras condiciones del constructor de reglas (como **Optó por marketing** o **Gasto total**) en el mismo segmento para obtener una audiencia más precisa, no solo una etiqueta por sí sola.
- Un suscriptor puede tener tantas etiquetas como desees: no hay límite, por lo que es adecuado usarlas para varios fines superpuestos (un nivel de lealtad *y* una lista de eventos *y* una nota de origen).
- Si una etiqueta deja de ser útil, eliminarla desde **Etiquetas de suscriptores** la quita de todos los suscriptores a los que se aplicó y de cualquier regla de segmento que la referenciara; los segmentos que la usen simplemente dejarán de coincidir en esa condición.