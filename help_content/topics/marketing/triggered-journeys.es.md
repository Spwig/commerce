---
title: Trayectos activados
---

<!-- screenshots-needed:
- url: /admin/campaigns/journeys/{journey_id}/report/
  filename: journey-report.webp
  description: The Journey report page for a journey with meaningful enrollment history — the enrollment funnel cards (Enrolled/Active now/Completed/Exited) and Attributed revenue card both showing non-zero numbers, plus the "Revenue by step" table (Step/Revenue/Orders/Sent/Opens/Clicks) with at least one plain step and one A/B step, both showing real Sent/Opens/Clicks counts.
  save-to: core/static/core/admin/img/help/triggered-journeys/
  viewport: 1440x900
-->

Los **Trayectos** de Campaign Studio son secuencias de correos electrónicos automatizadas y de varios pasos que se inician por sí mismas cada vez que un cliente realiza una acción específica: se registra, realiza un pedido, deja artículos en su carrito, se mantiene inactivo durante un tiempo o tiene un pedido entregado. En lugar de recordar enviar manualmente un correo de bienvenida, un recordatorio de recuperación de carrito o una solicitud de reseña, construyes la secuencia una vez y Spwig la ejecuta para cada cliente que cumpla los requisitos, mientras el trayecto siga activo.

## Tres formas de enviar correos

Campaign Studio ahora cubre tres patrones de envío distintos:

| Tipo | Comportamiento |
|------|-----------|
| **Difusión** | Se envía una sola vez: de inmediato o en una fecha y hora programada específicas. Úsalo para un anuncio o una venta puntual. |
| **Recurrente** | Una plantilla que se envía según un horario repetitivo (ver [Campañas recurrentes](/help/recurring-campaigns)). |
| **Trayecto** | Una secuencia de varios pasos que se inicia automáticamente para un cliente cuando ocurre un evento del ciclo de vida, y luego distribuye sus pasos a lo largo de horas o días. |

Un trayecto no tiene su propio botón de "enviar" ni un horario que configurar; reacciona a eventos en lugar de a un reloj.

## Disparadores

Cada trayecto escucha exactamente un evento, configurado como el **Disparador** del trayecto:

| Disparador | Se activa cuando |
|---------|-----------|
| **El cliente se registra** | Se crea una nueva cuenta de cliente. |
| **Se realiza un pedido** | Se realiza cualquier pedido, ya sea por un cliente nuevo o recurrente. |
| **Se realiza el primer pedido** | Específicamente el primer pedido de un cliente. |
| **Carrito abandonado** | Un comprador añade algo a su carrito y luego se mantiene inactivo sin finalizar la compra. |
| **Cliente inactivo (recuperación)** | Un cliente no ha realizado un pedido en un tiempo. |
| **Pedido entregado** | El estado de un pedido cambia a Entregado. |
| **Producto de nuevo en stock** | Un producto sobre el que un cliente solicitó ser notificado vuelve a estar disponible. |

## Los disparadores de recuperación y reactivación, en detalle

**Pedido entregado** y **Producto de nuevo en stock** se activan de inmediato, de la misma manera que **Se realiza un pedido**. **Carrito abandonado** y **Cliente inactivo (recuperación)** funcionan de manera diferente: en lugar de reaccionar a un momento único, Spwig realiza comprobaciones periódicas para detectar compradores y clientes que cumplan los criterios, por lo que puede haber un breve retraso entre que un carrito se quede inactivo (o un cliente se vuelva inactivo) y su inscripción.

**Carrito abandonado** — inscribe a un comprador que añadió algo a su carrito y luego se mantuvo inactivo sin completar la compra. Por defecto, esto ocurre después de aproximadamente una hora de inactividad; la ventana exacta de inactividad (y hasta qué punto en el pasado Spwig buscará) es un umbral que tu host puede ajustar para tu tienda. Funciona tanto para compradores registrados como para invitados; para un invitado, Spwig utiliza la dirección de correo electrónico capturada al finalizar la compra. Si el comprador vuelve y completa su pedido, se le retira automáticamente del trayecto, por lo que una compra completada nunca recibe un correo de "¿olvidaste algo?". Añade un bloque de contenido de **Carrito abandonado** al correo de recuperación para mostrar exactamente lo que se dejó atrás, con precios en vivo, imágenes y un enlace de vuelta al carrito, o usa un bloque de **Producto destacado** para resaltar un artículo en particular.

**Cliente inactivo (recuperación)** — inscribe a un cliente que no ha realizado un pedido en un tiempo, para darle una razón para volver.

Por defecto, son 90 días sin una compra (también un umbral ajustable por el host).

Un cliente solo se vuelve a incluir en un recorrido de recuperación de clientes una vez como máximo por esa ventana, por lo que alguien que sigue inactivo no se vuelve a inscribir inmediatamente después.

**Pedido entregado** — inscribe a un cliente una vez que el estado de su pedido cambia a **Entregado**, lo cual es un momento natural para solicitar una reseña unos días después. Se dispara una vez por pedido, en la transición a Entregado; las ediciones posteriores a un pedido ya entregado no lo disparan de nuevo. Tenga en cuenta que la acción masiva **Marcar pedidos seleccionados como Entregados** de la lista de pedidos actualiza los pedidos directamente y no dispara este disparador (ni el correo de confirmación de entrega); actualice los pedidos uno a la vez, o a través de la aplicación móvil de Spwig, para que se dispare.

**Producto de nuevo en stock** — cuando un producto sobre el que un cliente solicitó ser notificado vuelve a estar en stock, Spwig comprueba si tiene un recorrido activo que esté escuchando este disparador. Si lo hay, el cliente se inscribe en ese recorrido en lugar de la alerta única simple, lo que le permite añadir un retraso, un bloque de **Producto destacado** que muestre el artículo reabastecido, o un correo de seguimiento. Si no hay ningún recorrido de reabastecimiento activo, los clientes siguen recibiendo el correo de notificación única estándar exactamente como antes, por lo que activar un recorrido para este disparador es completamente opcional.

## Crear un recorrido

Vaya a **Campaign Studio > Journeys** y haga clic en **Add Journey**.

1. Asigne un **Name** al recorrido; esto es solo para su referencia; los clientes nunca lo ven.
2. Elija el evento de **Trigger**.
3. Opcionalmente, establezca **Only for segment** en un Segmento; cuando se establece, solo se inscriben los suscriptores que pertenecen a ese segmento. Déjelo en blanco para inscribir a todos los suscriptores elegibles.
4. Establezca **Once per subscriber** y **Re-enrollment cooldown (days)**; consulte [Protección contra el sobre-almacenamiento](#guarding-against-over-enrollment) a continuación.
5. Establezca **Status** en **Active** para activar el recorrido. Déjelo como **Draft** mientras aún lo esté diseñando, o establézcalo en **Paused** para detener nuevas inscripciones sin perder su configuración.
6. Haga clic en **Save**; Spwig le lleva directamente al [Journey Builder](/help/journey-builder), el lienzo visual donde diseña la secuencia real: qué correos se envían, cuánto tiempo esperar entre ellos y si diferentes suscriptores deben seguir diferentes rutas.

Una serie de bienvenida simple de tres pasos, una vez diseñada en el lienzo, podría verse así:

| Paso | Espera | Envía |
|------|-------|-------|
| 1 | Inmediatamente | Correo de bienvenida |
| 2 | 3 días después | Consejos para empezar |
| 3 | 7 días después de eso | Descuento para el primer pedido |

Los correos en sí son campañas ordinarias que diseña en el mismo constructor visual que usaría para una transmisión (Broadcast): línea de asunto, bloques de contenido, todo. No hay necesidad de programar ni enviar uno usted mismo; déjelo como **Draft** y simplemente selecciónelo desde el menú desplegable del paso en el constructor. El recorrido lo envía por usted, una vez por cada suscriptor que llegue a ese paso.

Consulte [Journey Builder](/help/journey-builder) para la guía completa sobre el diseño de pasos en el lienzo, la ramificación de un recorrido con una condición **Sí/No** y el inicio desde una plantilla lista para usar en lugar de un lienzo en blanco.

## Pruebas A/B de un paso

Cualquier paso de **Send email** puede convertirse en una prueba A/B, de modo que un recorrido descubre automáticamente —y luego sigue usando— el correo que tiene mejor rendimiento. Dado que un recorrido se ejecuta de forma continua (los suscriptores llegan con el tiempo), Spwig no prueba un lote fijo y se detiene; en cambio, **divide a los inscritos equitativamente entre las variantes a medida que llegan, observa cómo rinde cada una y, una vez que una es una ganadora estadística clara, fija esa variante para todos los inscritos futuros.** Los suscriptores que ya están a mitad de camino conservan la versión que se les envió primero.

Abra un paso de Send email en el [Journey Builder](/help/journey-builder) y establezca **Step type**:

- **Correo único** — el comportamiento normal: todos reciben el correo que elijas.
- **A/B: correos diferentes** — elige **dos a cuatro** correos (diseños, ofertas o maquetas diferentes); cada inscrito recibe uno.
- **A/B: líneas de asunto diferentes** — elige un correo e ingresa **dos a cuatro** líneas de asunto; cada inscrito recibe ese correo con un asunto diferente.

Luego elige **Elegir al ganador por** — **Tasa de apertura** (generalmente lo mejor para una prueba de asunto) o **Tasa de clics** — y listo. Establece el recorrido como **Activo** y los inscritos comenzarán a dividirse entre las variantes.

El panel del paso muestra un **marcador en vivo** a medida que llegan los datos: los destinatarios de cada variante, la tasa de apertura y la tasa de clics, además de la confianza de Spwig en el líder ("Liderando con 92% de confianza"). Un ganador solo se bloquea cuando Spwig tiene al menos **95% de confianza** *y* hay suficientes datos para confiar en ello, por lo que un recorrido con poco tráfico no sacará conclusiones apresuradas. Una vez bloqueado, el paso muestra **"Ganador bloqueado: Variante B"** y cada nuevo inscrito recibe esa variante; en el lienzo, la tarjeta muestra **"A/B · N correos"** durante la prueba y luego **"Ganador A/B: B"** una vez decidido.

Algunas cosas a tener en cuenta:

- **Dale tráfico.** La confianza depende del volumen: un paso al que solo llegan unas pocas personas puede permanecer en "Aún no hay suficientes datos" durante un tiempo. Las pruebas A/B brillan en recorridos con inscripciones constantes.
- **Editar las variantes o la métrica del ganador inicia una prueba nueva** — un ganador previamente bloqueado se limpia para que la nueva configuración obtenga su propio resultado.
- Un paso A/B con menos de dos variantes **bloquea el recorrido para que se active** hasta que lo completes (o lo cambies de vuelta a un correo único).

Consulta [Pruebas A/B](ab-testing) para más información sobre cómo Spwig lee la confianza y la significancia.

## Cómo funciona la inscripción

Cuando ocurre el evento de activación para un cliente, Spwig verifica cada recorrido activo que esté escuchando ese evento y, para cada uno para el cual el cliente sea elegible, lo **inscribe** en el punto de inicio del flujo. Desde allí, Spwig avanza al suscriptor a través de lo que diseñaste en el lienzo: esperando cada paso de **Espera**, enviando el correo de cada paso de **Enviar correo** y siguiendo el camino correcto de **Sí**/**No** en cualquier **Rama** — hasta que alcanzan un paso de **Salida**, en cuyo punto el recorrido se marca como **Completado** para ese suscriptor.

**El consentimiento siempre se respeta.** Un suscriptor que no se haya suscrito al correo de marketing, o que se haya dado de baja desde entonces, simplemente se omite: el recorrido no se detiene para otros suscriptores, y las bajas a mitad de recorrido detienen automáticamente los envíos restantes de ese suscriptor. Nunca necesitas filtrar tus recorridos por estado de consentimiento tú mismo.

## Protección contra la sobreinscripción

Dos ajustes en el recorrido controlan con qué frecuencia un suscriptor puede pasar por él:

| Ajuste | Qué hace | Uso típico |
|---------|--------------|-------------|
| **Una vez por suscriptor** *(activado por defecto)* | Cada suscriptor se inscribe como máximo una vez, para siempre, sin importar cuántas veces vuelva a ocurrir el evento de activación para ellos. | Una serie de bienvenida: un cliente solo debería recibirla una vez. |
| **Enfriamiento de reinscripción (días)** | Cuando **Una vez por suscriptor** está desactivado, establece un número mínimo de días que deben transcurrir desde la última inscripción de un suscriptor antes de que pueda inscribirse de nuevo. Establece en `0` para no tener enfriamiento. | Una serie activada por pedido que debería ejecutarse de nuevo para un nuevo pedido, pero no volver a activarse por cada pedido realizado la misma semana. |

Desactiva **Una vez por suscriptor** para un recorrido que quieras ejecutar por pedido (como un agradecimiento post-compra) y combínalo con un enfriamiento para que un cliente que hace dos pedidos el mismo día solo se inscriba una vez. Un suscriptor que ya esté trabajando activamente en un recorrido nunca se inscribirá en una segunda ejecución superpuesta de ese mismo recorrido, sin importar estos ajustes.

## Monitoreo de recorridos


La lista **Campaign Studio > Journeys** muestra el **Trigger** (disparador), el **Status** (estado), el número de **Emails** (correos) que envía cada journey (secuencia) y los totales en curso de **Enrolled** (inscritos) / **Completed** (completados), para que puedas ver de un vistazo si una secuencia está llegando realmente a las personas.

![La lista de Journeys mostrando dos secuencias activas con recuentos de inscripción y finalización](/static/core/admin/img/help/triggered-journeys/journey-list.webp)

Para ver suscriptores individuales en lugar de totales, abre la lista **Journey Enrollments** en `/admin/email_marketing/journeyenrollment/`. Cada fila muestra el progreso de un suscriptor a través de una secuencia: en qué **Journey** (secuencia) se encuentra, su **Current step** (paso actual), **Status** (estado: Active, Completed o Cancelled) y cuándo vence su **Next step** (próximo paso). Usa los filtros para acotarlo a una secuencia o un estado específico; por ejemplo, filtrar por **Active** muestra a todos los que están actualmente en medio de la secuencia.

![La lista de Journey Enrollments mostrando el progreso de los suscriptores a través de dos secuencias](/static/core/admin/img/help/triggered-journeys/journey-enrollments.webp)

## Informe de la secuencia

Cada secuencia tiene su propia página de **Report** (informe), que se abre haciendo clic en el botón **Report** en la tarjeta de la secuencia en **Campaign Studio > Journeys**, o en la página de configuración de la propia secuencia. Es un resumen de una sola página de hasta dónde llegan los inscritos en la secuencia y, si tus correos contienen enlaces rastreados, cuántos ingresos ha generado la secuencia.

![La página del informe de la secuencia mostrando el embudo de inscripción, la tarjeta de ingresos atribuidos y la tabla de ingresos por paso](/static/core/admin/img/help/triggered-journeys/journey-report.webp)

### Embudo de inscripción

Cuatro tarjetas muestran dónde se encuentran actualmente los inscritos:

| Tarjeta | Qué muestra |
|------|---------------|
| **Enrolled** | El número total de suscriptores que alguna vez han entrado en esta secuencia. |
| **Active now** | Inscritos que están actualmente a mitad de la secuencia, esperando o trabajando en su próximo paso. |
| **Completed** | Inscritos que alcanzaron el paso **Exit** (salida) de la secuencia. |
| **Exited** | Inscritos que fueron retirados de la secuencia antes de completarla; por ejemplo, un comprador que finalizó la compra a mitad de una secuencia de carrito abandonado, o un suscriptor que se dio de baja. |

Si la secuencia aún no tiene inscripciones, las cuatro tarjetas muestran cero y una nota te recuerda que las métricas aparecen una vez que los clientes comienzan a entrar en la secuencia.

### Ingresos atribuidos

La tarjeta **Attributed revenue** (ingresos atribuidos) funciona de la misma manera que la de un [informe de campaña](campaign-reports): Spwig rastrea los pedidos hasta los clics en los enlaces de los correos de la secuencia, la misma atribución por clic y con consentimiento descrita en [Ingresos atribuidos](campaign-reports#attributed-revenue) en esa página. Se aplican las mismas advertencias aquí: la atribución es solo por clic (una sola apertura nunca atribuye ingresos), sigue el modelo de atribución activo y la ventana de revisión de tu tienda, respeta el consentimiento de analítica y no es retroactiva: una secuencia solo muestra ingresos de correos enviados después de que se activó el rastreo de atribución para tu tienda.

La línea secundaria de la tarjeta desglosa el total en:

- **Orders** (pedidos): cuántos pedidos se acreditan a esta secuencia, combinando los correos de todos los pasos.
- **AOV** (valor medio del pedido): el valor medio del pedido entre esos pedidos.
- **Revenue per enrollee** (ingresos por inscrito): los ingresos atribuidos divididos por el total de **Enrolled**. Una secuencia no tiene un único "gasto" como lo hace una campaña, ya que se ejecuta de forma continua en lugar de tener un costo único, por lo que no hay una cifra de ROAS aquí. **Revenue per enrollee** es el equivalente más cercano: una medida estable y comparable de la eficiencia con la que la secuencia convierte una inscripción en una venta, que puedes seguir con el tiempo o comparar con otra secuencia.

### Ingresos por paso

Cuando la secuencia tiene al menos un paso **Send email** (enviar correo), una tabla **Revenue by step** (ingresos por paso) desglosa el total aún más, una fila por paso, para que puedas ver qué correo de la secuencia está realmente justificando su existencia:


| Columna | Qué muestra |
|--------|---------------|
| **Paso** | El correo del paso, con una insignia **A/B** si ese paso está ejecutando una [prueba A/B](ab-testing). |
| **Ingresos** | Ingresos atribuidos de pedidos trazados de vuelta al correo de ese paso. |
| **Pedidos** | El número de pedidos detrás de esa cifra de ingresos. |
| **Enviados** | Cuántas veces se ha enviado el correo de este paso. |
| **Aperturas** / **Clics** | Cuántos de esos envíos fueron abiertos y cuántos fueron clicados. Spwig rastrea aperturas y clics para los envíos de cada paso, tanto planos como A/B. |

Use esta tabla para detectar un eslabón débil en un viaje de lo contrario saludable; por ejemplo, una serie de bienvenida donde el primer correo genera la mayor parte de los ingresos y un paso posterior contribuye poco podría ser un candidato para una oferta más fuerte o una reescritura, en lugar de asumir que toda la secuencia necesita una reevaluación.

## Consejos

- La forma más rápida de iniciar un viaje de abandono de carrito, recuperación, solicitud de revisión posterior a la entrega o alerta de reposición es una plantilla inicial; cuando guarda un nuevo viaje con uno de estos desencadenantes, el selector de **Plantillas** del [Constructor de viajes](/help/journey-builder) ofrece un flujo listo para usar (**Recuperación de carrito abandonado**, **Recuperación de clientes inactivos**, **Solicitud de revisión posterior a la entrega** o **Alerta de reposición**) que puede ajustar en lugar de construir desde cero.
- Comience cada viaje como **Borrador** mientras construye sus pasos, luego cambie el **Estado** a **Activo** una vez que haya verificado los correos y los retrasos; nada se inscribe hasta que esté Activo.
- Mantenga **Una vez por suscriptor** activado para todo lo vinculado a un hito único (registro, primer pedido); desactívelo con un tiempo de espera razonable para todo lo que debería repetirse, como una serie posterior a la compra.
- Use **Solo para segmento** para ejecutar una serie de bienvenida diferente para una audiencia específica; por ejemplo, un segmento VIP recibe una secuencia más rica que el resto.
- Establezca la espera del primer paso en `0` si desea que el primer correo se envíe inmediatamente después de que se dispare el desencadenante, en lugar de esperar.
- Revise la lista de **Inscripciones en viajes** después de activar un nuevo viaje para confirmar que los suscriptores están siendo inscritos y avanzando a través de sus pasos como se espera.
- Pausar un viaje (**Estado: Pausado**) detiene nuevas inscripciones pero no cancela a los suscriptores que ya están a mitad de camino; siguen recibiendo sus pasos restantes.