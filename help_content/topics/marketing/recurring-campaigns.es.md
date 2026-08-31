---
title: Campañas recurrentes
---

Las **Campañas recurrentes** de Campaign Studio te permiten configurar un boletín una sola vez —un resumen semanal de productos, un resumen mensual del blog— y que Spwig lo envíe automáticamente según un programa repetitivo, en lugar de crear y enviar una nueva campaña manualmente cada vez.

## Difusión vs. recurrente

Cada campaña en Campaign Studio tiene un **Tipo de campaña**:

| Tipo | Comportamiento |
|------|-----------|
| **Difusión** | Se envía una sola vez —inmediatamente o en una fecha y hora programada específicas. Úsalo para un anuncio, una venta o un correo de lanzamiento de producto único. |
| **Recurrente** | Actúa como una plantilla que se envía según un programa repetitivo. Cada envío es una copia nueva y fechada llamada **ocurrencia** — la propia plantilla nunca se "envía" directamente. |

Para convertir una campaña en recurrente, ábrela en **Campaign Studio > Campañas** y establece el **Tipo de campaña** como **Recurrente**, luego guarda. Una sección **Programa** aparece en la campaña cuando la vuelves a abrir — solo se muestra para las campañas recurrentes.

![Tipo de campaña establecido como Recurrente](/static/core/admin/img/help/recurring-campaigns/campaign-type-selector.webp)

## Establecer un programa

Una vez que una campaña es recurrente, su sección **Programa** controla cuándo se ejecuta:

| Campo | Descripción |
|-------|-------------|
| **Activo** | Activa o desactiva la recurrencia sin eliminar el programa. |
| **Frecuencia** | **Diaria**, **Semanal** o **Mensual**. |
| **Intervalo** | Enviar cada N unidades de frecuencia — p. ej., intervalo `2` con frecuencia **Semanal** significa cada 2 semanas. |
| **Día de la semana** | Qué día enviar para una frecuencia semanal (`0` = lunes … `6` = domingo). |
| **Día del mes** | Qué día enviar para una frecuencia mensual (`1`–`28`, para que cada mes tenga ese día). |
| **Hora de envío** | La hora del día en que se envía la campaña. |
| **Zona horaria** | Un nombre de zona horaria IANA, p. ej. `Europe/London` o `America/New_York` — la hora de envío se interpreta en esta zona, no en la del servidor. |

![Sección de programa semanal en una campaña recurrente](/static/core/admin/img/help/recurring-campaigns/schedule-section.webp)

En cuanto guardes un programa activo, se **activa** — Spwig calcula la próxima hora de ejecución y la muestra en **Próxima ejecución**. No necesitas activar nada manualmente; una tarea en segundo plano verifica los programas vencidos y envía la ocurrencia cuando llega el momento. **Última ejecución** y **Ocurrencias enviadas** se actualizan automáticamente después de cada envío para que puedas ver que el programa está activo.

## La política de sin nuevo contenido

Los boletines recurrentes a menudo incluyen contenido dinámico — más comúnmente un bloque de **Publicaciones del blog** (o una **Cuadrícula de productos**) configurado como **Nuevo desde el último envío** en el editor visual, que solo incorpora las publicaciones publicadas — o los productos agregados — desde el envío anterior de la campaña. Esto plantea una pregunta obvia: ¿qué sucede si llega una ejecución programada y no hay nada nuevo para destacar?

Spwig responde a esto con la **Política de sin nuevo contenido** del programa:

| Política | Qué sucede | Ideal para |
|--------|---------------|----------|
| **Omitir este envío** *(predeterminado)* | La ocurrencia se omite por completo: no se envía nada. El calendario pasa directamente a su próxima ejecución programada. | Un resumen de blog o de productos, para que a los suscriptores nunca se les envíe un correo que simplemente repita lo que ya vieron. |
| **Enviar de todos modos (omitir bloques vacíos)** | El correo se envía según el calendario, sin importar nada. Cualquier bloque que no tenga contenido nuevo —como un bloque de publicaciones de blog «Nuevas desde el último envío» vacío— simplemente no muestra nada en ese lugar. | Boletines que siempre tienen otro contenido que vale la pena enviar (un mensaje de bienvenida, secciones permanentes o varios bloques dinámicos), incluso si un bloque resulta estar vacío. |
| **Retener y enviar tarde** | El envío se pospone. Spwig vuelve a comprobar una vez al día si hay contenido nuevo, hasta el **Período de retención (días)**. Si aparece contenido nuevo dentro de ese período, la ocurrencia se envía tarde; si el período expira sin nada nuevo, esa ocurrencia se descarta y el calendario pasa a su siguiente hueco. | Una cadencia que se desea proteger (p. ej., enviar *algo* eventualmente) sin disparar un número vacío en el momento en que no haya nada nuevo que publicar esa semana. |

Solo las campañas que utilizan contenido consciente de diferencias —un bloque de publicaciones de blog o una cuadrícula de productos configurada en **Nuevas desde el último envío**— activan esta comprobación. Una campaña recurrente sin dichos bloques siempre se considera que tiene contenido nuevo y se envía normalmente según el calendario.

**Período de retención (días)** solo se aplica a la política **Retener y enviar tarde**: establece cuántos días Spwig seguirá reintentando antes de descartar esa ocurrencia.

## Pruebas A/B de cada ocurrencia

Un boletín recurrente es un lugar natural para realizar pruebas A/B de sus **asuntos** —se envía a una cadencia regular a la misma audiencia, por lo que se puede seguir aprendiendo qué redacción genera más aperturas. Spwig puede ejecutar una prueba A/B de asuntos nueva en **cada ocurrencia** automáticamente.

Configúrelo en la sección **Calendario**:

1. En **Asuntos A/B**, introduzca **dos a cuatro** asuntos, uno por línea. Déjelo en blanco para enviar las ocurrencias normalmente con el asunto propio de la plantilla.
2. Establezca el **% de muestra de prueba A/B**: la proporción de la audiencia de cada ocurrencia utilizada para la prueba, dividida equitativamente entre los asuntos. El resto es el grupo de control que recibe al ganador.
3. Elija la **métrica de ganador A/B** (tasa de apertura o de clic), la **ventana de prueba A/B (horas)** para recopilar resultados antes de decidir, y si **enviar automáticamente al ganador** al grupo de control.

A partir de entonces, cada vez que el calendario se activa, esa ocurrencia divide su audiencia, envía cada asunto a un segmento, espera la ventana de prueba y luego elige el asunto ganador y lo envía a todos los demás, sin ninguna acción adicional por su parte. Cada ocurrencia es una prueba independiente y autónoma, por lo que obtiene una lectura fresca en cada envío y puede observar qué asuntos ganan a lo largo de las semanas. El resultado de cada ocurrencia aparece en **Historial de ocurrencias** a continuación, enlazando directamente a su página de resultados con las tasas por variante, el ganador y el nivel de confianza de Spwig (vea [Pruebas A/B](ab-testing) para saber cómo interpretar esos resultados).

Dos cosas que conviene saber:

- **La prueba A/B aquí es solo de asuntos.** Para comparar diseños completamente diferentes, use una prueba A/B de difusión única: el asistente completo, que admite variantes de contenido, es para campañas de difusión.
- Si la audiencia de una ocurrencia es **demasiado pequeña para dividirse** entre las variantes, Spwig envía esa ocurrencia como un boletín normal en su lugar: una semana de poca actividad nunca significa un envío perdido.

## Historial de ocurrencias

Cada vez que una campaña recurrente se envía realmente, Spwig crea una **ocurrencia** con fecha: un registro de campaña real e independiente con su propio asunto, destinatarios y estadísticas de envío (enviados, fallidos, omitidos, aperturas, clics). La ocurrencia se nombra según la plantilla con la fecha de envío añadida, p. ej., «Resumen semanal de blog — 2026-08-19».

La página de edición de la campaña recurrente muestra su **Historial de ocurrencias**: las ocurrencias más recientes, cada una enlazada a su propio registro de campaña para que puedas revisar exactamente lo que se envió y cómo se desempeñó.

![Lista de historial de ocurrencias en una campaña recurrente](/static/core/admin/img/help/recurring-campaigns/occurrence-history.webp)

## Consejos

- Combina una campaña recurrente con un bloque de **Publicaciones del blog** configurado en **Nuevas desde el último envío** para crear un resumen autoadministrado de "nuevas publicaciones de esta semana": tú escribes las publicaciones y Spwig se encarga del envío por correo.
- Comienza con **Omitir este envío** para los resúmenes de contenido. Es la opción predeterminada más segura: los suscriptores nunca reciben una repetición del contenido de la última vez.
- Cambia a **Enviar de todos modos** solo si tu plantilla tiene otro contenido que valga la pena enviar por sí solo, incluso cuando el bloque dinámico está vacío.
- Usa **Retener y enviar tarde** cuando perder ocasionalmente un ciclo de envío no sea un problema, pero perderlo durante semanas seguidas sí lo sea: configura la ventana de retención según la duración de la pausa con la que estés cómodo.
- Revisa **Próxima ejecución en** después de guardar un horario para confirmar que se estableció en el día y la hora esperados, especialmente al trabajar en diferentes zonas horarias.
- Revisa el **Historial de ocurrencias** periódicamente: una plantilla que sigue omitiendo envíos es una señal de que tu fuente de contenido dinámico (p. ej., el blog) ha dejado de publicar.