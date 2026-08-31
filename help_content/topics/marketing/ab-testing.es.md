---
title: Pruebas A/B
---

La función de **pruebas A/B** de Campaign Studio te permite probar de dos a cuatro **variantes** —diferentes versiones de la misma campaña— en una parte de tu audiencia antes de comprometerte con el envío completo. Cambia solo la línea de asunto o diseña contenido completamente diferente para cada variante. Spwig divide una muestra de tu lista equitativamente entre las variantes, observa el rendimiento de cada una y envía automáticamente la variante con mejor rendimiento a todas las personas que no vieron la prueba.

## Configuración de una prueba

Primero, crea tu campaña de forma habitual en el creador visual de Campaign Studio: escribe una línea de asunto, diseña tu contenido y elige el **Segmento** al que deseas llegar. Esa campaña se convierte en el **contenedor** de la prueba. Una vez que adjuntas una prueba A/B a ella, el contenedor en sí nunca se envía directamente; su función es mantener la configuración, y la audiencia a la que está configurado para llegar es exactamente el grupo contra el que se ejecuta la prueba.

Hay dos lugares que abren el asistente de pruebas A/B:

- El botón **Prueba A/B** en la barra de herramientas del creador visual.
- El icono de **Prueba A/B** en la tarjeta de la campaña en **Campaign Studio > Campañas**.

Una vez que existe una prueba en una campaña, ese mismo botón te lleva directamente a sus resultados en lugar del asistente, y la tarjeta de la campaña adquiere una pequeña insignia **A/B** para que puedas identificarla de un vistazo en la lista.

## Qué probar

El primer paso del asistente pregunta qué debe diferir entre las variantes:

| Opción | Qué cambia | Medido por |
|--------|--------------|-------------|
| **Línea de asunto** | Cada variante envía exactamente el mismo contenido; solo difiere la línea de asunto. La prueba más común. | Tasa de apertura |
| **Contenido** | Cada variante es un diseño separado que tú mismo creas en el creador visual. | Tasa de clics |

![El paso "¿Qué quieres probar?", con Línea de asunto seleccionada](/static/core/admin/img/help/ab-testing/ab-test-what-to-test.webp)

## Elección de tus variantes

Lo que ingreses a continuación depende de lo que hayas elegido:

- **Línea de asunto** — escribe un asunto para cada variante (2–4). Se muestran dos filas al inicio; haz clic en **Agregar otro asunto** para un tercero o cuarto.
- **Contenido** — simplemente elige cuántas variantes quieres (2–4). Cada variante comienza como una copia exacta del diseño actual de tu contenedor, por lo que solo necesitas cambiar lo que estás probando.

En cualquier caso, Spwig etiqueta las variantes como **A**, **B**, **C** y **D** en el orden en que las ingreses; las verás como "Variante A", "Variante B", y así sucesivamente a partir de aquí.

![El paso de Variantes con tres líneas de asunto ingresadas para las variantes A, B y C](/static/core/admin/img/help/ab-testing/ab-test-variants.webp)

Para una prueba de contenido, no diseñas las variantes en el propio asistente; después de crear la prueba, la tarjeta de cada variante en el centro de resultados tiene un pequeño icono de lápiz que la abre en el mismo creador visual que usaste para el contenedor. Esto solo está disponible mientras la prueba sigue en **Borrador**; una vez que inicies la prueba, los diseños se bloquean para que lo que estás midiendo no cambie a mitad de la prueba.

## Configuración de la prueba

El último paso del asistente cubre cómo se ejecuta y decide la prueba:

| Configuración | Qué hace |
|---------|--------------|
| **Muestra de prueba** | El porcentaje de tu audiencia utilizado para la prueba, dividido equitativamente entre las variantes: 20%, 30%, 50% o 100%. El resto —el **grupo de control** (holdout)— recibe al ganador después. Elegir 100% prueba tu lista completa de una vez, por lo que no queda grupo de control al que enviar al ganador. |
| **Ganador determinado por** | **Tasa de apertura** o **Tasa de clics**. Por defecto, es la tasa de apertura para una prueba de línea de asunto y la tasa de clics para una prueba de contenido, ya que es lo que cada una realmente mide, pero puedes cambiarlo en cualquier dirección. |
| **Ventana de prueba (horas)** | Cuánto tiempo recopilar aperturas y clics antes de elegir un ganador, desde 1 hasta 168 horas (una semana completa). |
| **Enviar automáticamente al ganador al resto de la audiencia** | Activado por defecto. Cuando está marcado, Spwig envía por correo electrónico la variante ganadora al grupo de control en cuanto termina la ventana, sin ninguna acción adicional por tu parte. |

Una breve tarjeta de revisión en la parte inferior resume tus elecciones antes de que te comprometas.

[![]( /static/core/admin/img/help/ab-testing/ab-test-settings.webp )

## Iniciando la prueba

Haga clic en **Crear prueba** para guardar la configuración — esto aún no envía nada. Llega al panel de resultados de la prueba en estado **Borrador**, mostrando cada variante con cero destinatarios hasta el momento y dos botones: **Iniciar prueba** y **Cancelar prueba**.

[![]( /static/core/admin/img/help/ab-testing/ab-test-draft.webp )

Haga clic en **Iniciar prueba** cuando esté listo. Spwig divide la muestra de la prueba de forma equitativa entre las variantes y envía por correo electrónico cada una inmediatamente: no necesita hacer nada más; un trabajo en segundo plano revisa una vez que haya finalizado la ventana de la prueba y decide al ganador por sí mismo. El estado de la campaña contenedora permanece **Borrador** durante todo este proceso — eso es esperado, ya que son las variantes (y posteriormente el ganador) las que realmente se envían, nunca la campaña contenedora.

Su audiencia debe ser lo suficientemente grande como para que cada variante obtenga un número significativo de destinatarios. Spwig bloquea el inicio de una prueba si alguna variante terminaría con cero personas, pero una prueba realmente digna de leer necesita más que un mínimo — apunte a varios cientos de destinatarios o más antes de confiar en el resultado.

## Mientras se ejecuta la prueba

Una vez iniciada, el panel pasa a **En ejecución** y muestra "Prueba en curso — el ganador se decide automáticamente alrededor de" la fecha y hora en que finaliza la ventana. Los recuentos de destinatarios y las tasas de apertura/clic actualizan cada vez que visita, junto con un gráfico de barras que compara las tasas de apertura y clic de cada variante lado a lado — no solo en la métrica que haya elegido para decidir el ganador.

[![]( /static/core/admin/img/help/ab-testing/ab-test-running.webp )

También puede vigilar cada prueba desde el **tablero de la Studio de Campañas**: su panel *Pruebas A/B recientes* muestra sus pruebas en ejecución y recientemente decididas — cada una con su confianza a simple vista — y enlaces directos a los resultados, junto con tarjetas que indican cuántas pruebas están en ejecución y cuántas se han decidido en los últimos 30 días.

## Leyendo los resultados

Cuando finaliza la ventana de la prueba, Spwig elige la variante con la tasa más alta en la métrica elegida, marca la prueba **Completada** y — si **Enviar automáticamente al ganador** estaba marcado y hay un grupo de control para enviar — envía esa variante a todos los que no formaron parte de la prueba. La tarjeta de la variante ganadora está resaltada y lleva un sello de **Ganador**; el gráfico de comparación permanece en su lugar para que pueda ver cómo se compararon las variantes.

[![]( /static/core/admin/img/help/ab-testing/ab-test-complete.webp )

Tenga en cuenta que los números de esta página siempre se refieren a la muestra de la prueba, no a toda la lista — con una muestra del 20%, está leyendo cómo respondió una quinta parte de su audiencia, no a todos.

## ¿Qué tan segura es el resultado?

Una tasa de apertura o clic más alta no siempre significa que una variante sea mejor en realidad — con una audiencia pequeña, una variante puede salirse con la suya simplemente por casualidad. Por lo tanto, junto con el ganador, Spwig muestra **qué tan segura está de que el resultado es real**, basándose en el tamaño de la brecha y la cantidad de destinatarios. Verá uno de tres resultados:

- **Un resultado claro** — Spwig tiene al menos un 95% de confianza de que la variante líder supera genuinamente a las demás. Este es un resultado en el que puede actuar.
- **Demasiado cercano para decidir** — hay un líder, pero la brecha es lo suficientemente pequeña como para que pueda tratarse de una casualidad. El porcentaje mostrado es la confianza que Spwig tiene, por debajo del 95%. Considere repetir la prueba con una audiencia más grande o con una ventana de prueba más larga antes de sacar conclusiones.
- **Aún no hay suficientes datos** — demasiados destinatarios (o demasiados clics y aperturas) para distinguir las variantes en absoluto. Esto es común en listas pequeñas; aumente la audiencia o deje que la prueba se ejecute por más tiempo.

Preserve all markdown formatting, image paths, code blocks, and technical terms.

[![](A completed test showing a clear result — the winning variant carries a confidence badge and the summary reads "statistically clear"](/static/core/admin/img/help/ab-testing/ab-test-confidence.webp))

La misma lectura aparece mientras un test aún se está ejecutando, por lo que puedes ver cómo se va consolidando un resultado — o no — antes de que finalice el período. Debido a que la confianza depende en gran medida del tamaño de la audiencia, ésta es la razón práctica para apuntar a cientos o más destinatarios por prueba: en una lista muy pequeña, incluso una diferencia aparentemente grande normalmente se leerá como "demasiado cercana para decidir".

Ten en cuenta que cuando el envío automático está activado, Spwig sigue enviando la variante con mayor tasa a el resto de tu audiencia incluso si el resultado es inconcluyente: la lectura de confianza está allí para decirte cuánto confiar en el resultado, no para detener el envío.

## Cancelar una prueba

**Cancelar prueba** está disponible mientras una prueba se encuentra en **Borrador** o **Prueba**, y la detiene sin que se envíe nunca un ganador. Está allí para cuando has cambiado de opinión o has cometido un error en la configuración — no algo que usar con ligereza, ya que una vez que una prueba es cancelada (o se completa normalmente), no hay botón para configurar una nueva en la misma campaña. Si quieres realizar otra comparación más tarde, crea una nueva campaña para ella.

## Consejos

- Elige primero una prueba de **Asunto** — es la más sencilla de configurar y la razón más común para realizar una prueba A/B en absoluto.
- Usa una prueba de **Contenido** cuando quieras comparar diseños o ofertas genuinamente diferentes, no solo el texto del asunto.
- Termina de diseñar cada variante de una prueba de contenido — usando el icono de lápiz en cada tarjeta — antes de hacer clic en **Iniciar prueba**. No puedes editar el diseño de una variante una vez que la prueba esté en marcha.
- Mantén el **Muestra de prueba** por debajo del 100% si quieres que Spwig envíe automáticamente al ganador al resto de la lista después — al 100% no queda ninguna muestra para que llegue.
- Da a la ventana de prueba suficiente tiempo para abarcar los hábitos normales de lectura de tus suscriptores (24 horas cubre cómodamente un día completo de husos horarios e inbox) en lugar de decidir un ganador solo con la primera hora o dos.