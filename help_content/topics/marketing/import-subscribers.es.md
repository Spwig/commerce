---
title: Importar suscriptores desde un archivo CSV
---

Si ya tiene una lista de correos electrónicos en otro lugar: una herramienta de correo electrónico antigua, una hoja de cálculo con registros de suscripción al boletín, una pila de registros de tarjetas de ferias comerciales - no necesita agregar esos contactos uno por uno en Spwig. El importador de suscriptores de Campaign Studio lee un archivo CSV o Excel y agrega a cada contacto válido a su audiencia de una vez, listo para etiquetar, segmentar y enviar correos electrónicos.

## Antes de importar: consentimiento

Cada importación requiere que marque una casilla para confirmar: **"Estos contactos han aceptado recibir correos electrónicos de marketing de mi parte."** Esto no es un trámite formal: solo importe contactos que realmente se hayan suscrito a correos electrónicos de marketing de su parte. Importa por dos razones:

- **Es un requisito legal en la mayoría de los lugares.** Enviar correos electrónicos de marketing a personas que nunca aceptaron recibirlos viola las leyes de consentimiento en muchos países.
- **Protege su capacidad de entrega.** Enviar correos electrónicos a personas que nunca se suscribieron genera quejas de spam y rechazos, lo cual los proveedores de correo utilizan para decidir si *cualquier* correo electrónico - incluyendo a personas que sí se suscribieron - llega a la bandeja de entrada.

Si una lista no proviene claramente de registros de suscripción, no la importe.

## Preparando su archivo

El importador acepta un archivo `.csv` o `.xlsx` con una fila de encabezado. Solo se requiere una columna:

| Columna | ¿Requerido? | Notas |
|--------|-----------|-------|
| **Correo electrónico** | Sí | Debe ser una dirección de correo electrónico válida. |
| **Nombre** | No | Se utiliza para personalizar los correos electrónicos. |
| **Apellido** | No | Se utiliza para personalizar los correos electrónicos. |
| **Idioma** | No | El código de idioma preferido del suscriptor (por ejemplo, `en`, `es`). |

Las columnas se asignan a estos campos automáticamente por nombre de encabezado, por lo que no necesita renombrar nada primero: variaciones comunes como `Correo electrónico`, `Dirección de correo electrónico`, `Nombre`, `Nombre dado`, `Apellido` o `Ubicación` son todas reconocidas.

Cada importación tiene un límite de **5 MB** y **5.000 filas**. Si su lista es más grande que eso, divídala en archivos más pequeños e importe uno tras otro.

## Importando sus contactos

1. Abra **Campaign Studio > Suscriptores** y haga clic en **Importar CSV**.
2. Seleccione su archivo `.csv` o `.xlsx`.
3. Elija qué sucede **para los contactos que ya están en su lista** - véase [Manejo de duplicados](#manejo-de-duplicados) a continuación.
4. Opcionalmente, elija una etiqueta bajo **Etiquetar a los contactos importados como** para etiquetar a todos en esta importación (por ejemplo, `Evento 2026`) - véase [Etiquetas de suscriptores](/help/subscriber-tags) para más información sobre etiquetas.
5. Marque **Estos contactos han aceptado recibir correos electrónicos de marketing de mi parte**.
6. Haga clic en **Continuar**.

![El formulario de carga de importación con un archivo seleccionado, una etiqueta seleccionada y el consentimiento confirmado](/static/core/admin/img/help/import-subscribers/import-upload-form.webp)

Spwig muestra una vista previa antes de que se importe algo realmente:

![La vista previa de la importación que muestra los recuentos de nuevos, existentes y omitidos inválidos con sus motivos](/static/core/admin/img/help/import-subscribers/import-preview.webp)

- **Nuevos contactos** - filas que crearán un suscriptor nuevo.
- **Ya en su lista** - filas cuya dirección de correo electrónico coincide con un suscriptor existente.
- **Omitidos (inválido)** - filas que no se pudieron leer, cada una listada con su número de fila y el motivo (formato de correo electrónico inválido, celda de correo electrónico vacía o duplicado de una fila anterior en el mismo archivo).

Verifique estos números, luego haga clic en **Importar ahora** para confirmar la importación, o **Cancelar** para retroceder sin realizar cambios.

## Manejo de duplicados

Una fila se considera duplicada cuando su dirección de correo electrónico coincide con un suscriptor que ya tiene. Usted elige cómo Spwig trata esos registros en el formulario de carga:

| Opción | Qué ocurre |
|--------|--------------|
| **Dejarlos como están** *(predeterminado)* | El nombre y el idioma del suscriptor existente se mantienen como están. |
| **Actualizar su nombre / idioma** | El nombre, apellido y idioma del suscriptor existente se actualizan desde el archivo (solo para los campos que el archivo realmente proporcione). |

La etiqueta que elija para la importación se aplica a **todos los de la lista** - nuevos y existentes - independientemente de la opción de duplicado que elija.

Así que al importar su lista "VIP" con la etiqueta **VIP**, etiqueta también a las personas que ya tienen.

La opción de duplicado solo controla si el *nombre y el idioma* de un contacto existente se sobrescribe.

## Después de la importación

Cada contacto creado mediante una importación se registra con el origen **Importación**, y se marca como con consentimiento en el momento en que ejecutó la importación (no en una fecha anterior en la que podrían haberse suscrito en otro lugar). Su nombre y apellido, si el archivo los proporciona, se almacenan en su registro de suscriptor, lo que significa que los campos de combinación `[[first_name]]` y `[[last_name]]` en sus campañas ahora se personalizan correctamente para ellos, incluso aunque nunca hayan creado una cuenta de Spwig.

## Consejos

- Exporte su lista de origen a un CSV de una sola hoja o a un archivo `.xlsx` con una fila de encabezado limpia antes de subirlo: hojas adicionales, celdas combinadas o filas de resumen pueden confundir la coincidencia de columnas.
- Use **Etiquetar a los contactos importados como** para crear inmediatamente la audiencia exacta que querrá dirigir después - véase [Etiquetas de suscriptores](/help/subscriber-tags) para construir un segmento a partir de ella.
- Siempre lea las **razones de los omitidos (inválidos)** antes de asumir que la importación falló: un pequeño número de filas omitidas con razones claras es normal para la mayoría de las listas del mundo real.
- Volver a ejecutar el mismo archivo es seguro: los contactos que ya importó se tratan como duplicados la segunda vez, no se vuelven a crear.
- Si está consolidando varias listas pequeñas, etiquete cada importación de manera diferente (por ejemplo, `Importar: Evento de Enero`, `Importar: Feria comercial`) para poder distinguirlas más tarde incluso después de que todas estén mezcladas en su audiencia principal.
- Para listas con más de 5.000 filas, divíjala por un límite obvio (alfabético, por origen o por fecha de recopilación) en lugar de un corte arbitrario, para que cada lote permanezca fácil de identificar posteriormente.