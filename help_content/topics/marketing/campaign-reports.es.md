---
title: Informes de campañas
---

<!-- screenshots-needed:
- url: /admin/campaigns/{campaign_id}/report/
  filename: engagement-over-time-chart.webp
  description: The report page scrolled to the "Engagement over time" chart card, with a campaign that has several days of send history so all three lines (Sent, Opened, Clicked) show a realistic shape.
  save-to: core/static/core/admin/img/help/campaign-reports/
  viewport: 1440x900
- url: /admin/campaigns/{campaign_id}/report/
  filename: top-links-table.webp
  description: The report page's "Top links" card, with a campaign whose email contains at least 3 distinct links and a realistic spread of Clicks/Unique/CTR values.
  save-to: core/static/core/admin/img/help/campaign-reports/
  viewport: 1440x900
- url: /admin/campaigns/{campaign_id}/recipients/
  filename: recipients-list.webp
  description: The Recipients page with the filters panel open and a mixed list of rows (some opened, some clicked, some bounced) so the engagement states are visibly distinct.
  save-to: core/static/core/admin/img/help/campaign-reports/
  viewport: 1440x900
- url: /admin/campaigns/{campaign_id}/recipients/
  filename: recipient-activity-modal.webp
  description: The Recipients page with the "Recipient activity" modal open for a recipient who has multiple event types (delivered, opened, at least one clicked entry naming a link).
  save-to: core/static/core/admin/img/help/campaign-reports/
  viewport: 1440x900
- url: /admin/campaigns/{campaign_id}/report/
  filename: attributed-revenue-card.webp
  description: A close-up of the report page's "Attributed revenue" stat card, for a campaign with a logged Spend so the orders/AOV/revenue-per-email/ROAS sub-line is fully populated.
  save-to: core/static/core/admin/img/help/campaign-reports/
  viewport: 1440x900
- url: /admin/campaigns/dashboard/
  filename: dashboard-attributed-revenue-kpi.webp
  description: The Campaign Studio dashboard's stat card grid, scrolled/cropped to show the "Attributed revenue (30d)" tile alongside its neighboring cards, with a non-zero revenue figure.
  save-to: core/static/core/admin/img/help/campaign-reports/
  viewport: 1440x900
- url: /admin/campaigns/{campaign_id}/report/
  filename: report-stat-cards.webp
  description: 'RECAPTURE NEEDED: the existing report-stat-cards.webp only shows 6 cards (Recipients, Delivered, Open rate, Click rate, Bounce rate, Spam complaints). The stat grid now has a 7th "Attributed revenue" card — recapture this shot with a campaign that has both attribution data and a logged Spend so all 7 cards are visible in a realistic state.'
  save-to: core/static/core/admin/img/help/campaign-reports/
  viewport: 1440x900
-->

Cada campaña que envíes a través de Campaign Studio tiene su propia página de **Informe**: un resumen en una sola página de cuántas personas alcanzó, cuántos correos electrónicos llegaron realmente y cómo respondieron los destinatarios. Úsalo para verificar que un envío se realizó sin problemas, detectar un problema de entregabilidad a tiempo o comparar el rendimiento de diferentes campañas a lo largo del tiempo.

## Abrir un informe

Desde **Campaign Studio > Campaigns**, busca la campaña que deseas revisar y haz clic en el icono de gráfico (**Report**) en su tarjeta.

![La cuadrícula de tarjetas de estadísticas de la página de informe de la campaña, mostrando destinatarios, entregados, tasa de apertura, tasa de clics, tasa de rebote y quejas de spam](/static/core/admin/img/help/campaign-reports/report-stat-cards.webp)

Un informe solo tiene números para mostrar una vez que la campaña se ha enviado realmente: una campaña que aún está en **Draft** muestra todas las estadísticas como cero, ya que aún no hay nada que medir.

## Las tarjetas de estadísticas

| Tarjeta | Qué muestra |
|------|---------------|
| **Destinatarios** | Cuántos suscriptores fueron el objetivo de esta campaña, más una línea secundaria que indica cuántos se omitieron y, de esos, cuántos se omitieron específicamente porque la dirección está en su [lista de supresión](list-hygiene). Un omisión no siempre es una supresión; Spwig también omite a un suscriptor que no tiene una dirección de correo electrónico utilizable, por ejemplo, por lo que se muestran las dos cifras por separado. |
| **Entregados** | Cuántos correos electrónicos fueron aceptados realmente por el servidor de correo receptor y no rebotaron, más la **tasa de entrega** — entregados como proporción de cada envío que Spwig *intentó* (aceptado por su servidor de correo o proveedor, independientemente de si rebotó después). |
| **Tasa de apertura** | La proporción de correos *entregados* que fueron abiertos, más el recuento bruto de **abiertos**. |
| **Tasa de clics** | La proporción de correos *entregados* que fueron clicados, más el recuento bruto de **clics** y la **tasa de clics por apertura** — clics como proporción de aperturas, una lectura de lo atractivo que fue su contenido para las personas que ya lo abrieron. |
| **Tasa de rebote** | La proporción de envíos *intentados* que rebotaron, desglosada en rebotes **duros** y **blandos**. |
| **Denuncias de spam** | Cuántos destinatarios marcaron el correo como spam o basura, más la **tasa de denuncias** — denuncias como proporción del correo *entregado*. |
| **Ingresos atribuidos** | Ingresos de pedidos que Spwig puede rastrear hasta esta campaña, más el número de pedidos, el valor medio del pedido (**AOV**), los ingresos por correo entregado y — una vez que haya registrado el costo de la campaña — su **ROAS**. Vea [Ingresos atribuidos](#attributed-revenue) a continuación. |

## Por qué las tasas usan denominadores diferentes

La tasa de apertura, la tasa de clics y la tasa de denuncias se miden todas contra el correo **entregado** — los destinatarios que realmente pudieron ver el correo — mientras que la tasa de entrega y la tasa de rebote se miden contra los envíos **intentados**. Esta es la práctica estándar de la industria del correo electrónico, y es la razón por la que ninguna de estas tasas puede superar el 100%: un correo que rebotó nunca fue entregado, por lo que no puede contar contra su tasa de apertura o clics, y un correo que ni siquiera se intentó (una omisión) no cuenta contra ninguna de ellas.

## Rebotes duros vs. rebotes blandos

- **Rebote duro** — la dirección es permanentemente no entregable. No existe, o el dominio se niega a aceptar correo para ella por completo.
- **Rebote blando** — un problema temporal: una bandeja de entrada llena, un servidor receptor que estuvo brevemente no disponible, y similares. Los rebotes blandos a menudo se resuelven solos.

Observe la división, no solo el total. Un aumento en el recuento de **rebotes duros** generalmente significa que su lista tiene direcciones obsoletas o mal escritas; un aumento en el recuento de **rebotes blandos** es más a menudo un tropiezo temporal en el extremo del destinatario. Cualquier rebote duro, cualquier denuncia de spam y una dirección que acumule rebotes blandos repetidos alimentan la [lista de supresión](list-hygiene) automática de Spwig — no necesita actuar sobre ellos usted mismo, pero el informe es donde notará primero un pico que vale la pena investigar.

## Ingresos atribuidos

Como su tienda y Campaign Studio viven en el mismo sistema, Spwig no necesita una plataforma de análisis externa ni un píxel de seguimiento para decirle si una campaña realmente generó ventas. Cuando un cliente hace clic en un enlace en el correo de esta campaña y llega a su tienda, Spwig puede seguir esa visita hasta la finalización de la compra y atribuir los ingresos del pedido resultante a la campaña — eso es lo que muestra la tarjeta de **Ingresos atribuidos**.

La línea secundaria de la tarjeta desglosa la cifra aún más:

- **Pedidos** — cuántos pedidos se atribuyen a esta campaña.
- **AOV** — el valor medio del pedido entre esos pedidos.
- **Ingresos por correo** — ingresos atribuidos divididos por el número de correos *entregados*, el mismo denominador que el informe usa para la tasa de apertura y la tasa de clics.
- **ROAS** — retorno sobre el gasto publicitario, mostrado solo una vez que ha ingresado un monto de **Gasto** en la propia campaña.

Se calcula como ingresos atribuidos divididos por el gasto.

Si el gasto se registró en una moneda diferente a la predeterminada de tu tienda, Spwig oculta el ROAS en lugar de mostrar una cifra que no se compara realmente de forma equivalente: ingresa el gasto en la moneda base de tu tienda para verlo.

Hay algunas cosas que vale la pena saber sobre cómo se calcula esta cifra:

- **Se basa en clics, no en aperturas.** Un cliente debe hacer clic en un enlace rastreado en el correo electrónico y llegar a tu tienda: una sola apertura nunca atribuye ingresos. Esto es intencional: el seguimiento de aperturas es cada vez menos fiable ahora que servicios como Apple Mail Privacy Protection precargan imágenes para casi todos los mensajes, inflando las cuentas de aperturas sin importar si alguien realmente leyó el correo.
- **Sigue el modelo de atribución de tu tienda.** Por defecto, es **último toque no directo** con una ventana de retroceso de 90 días: el mismo clic debe conducir a un pedido dentro de esa ventana para ser contado, y una visita directa posterior no borra el crédito ya ganado por el clic de esta campaña.
- **Respeta el consentimiento de analíticas.** Solo se rastrean los visitantes que aceptaron el consentimiento de analíticas en la barra de cookies de tu tienda (si no ejecutas una barra de consentimiento, el seguimiento sigue la política predeterminada de tu tienda). Un cliente que rechazó el consentimiento aún puede comprar: su pedido simplemente no se atribuirá a ningún canal, incluido este.
- **No es retroactivo.** El seguimiento de ingresos solo cubre las campañas enviadas después de que el seguimiento de atribución se activó para tu tienda. Una campaña enviada antes de eso no mostrará ingresos atribuidos aquí, incluso si generó ventas reales, simplemente porque Spwig no tiene datos de clics registrados para ella.
- **Las pruebas A/B y las campañas recurrentes también agrupan sus ingresos atribuidos** — consulta [Informes sobre una prueba A/B](#informes-sobre-una-prueba-ab) a continuación.

También encontrarás una tarjeta de **Ingresos atribuidos (30d)** en el propio panel de Campaign Studio, que suma los ingresos atribuidos por correo electrónico de todas las campañas durante los 30 días anteriores: una comprobación rápida sin abrir un informe individual. Para una vista a nivel de tienda que incluya todos los canales, no solo el correo electrónico — búsqueda orgánica, redes sociales, afiliados y más — consulta el panel de [Atribución de ingresos](/help/revenue-attribution) bajo **Insights**.

## Participación en el tiempo

Debajo de las tarjetas de estadísticas, el gráfico **Participación en el tiempo** traza tres líneas — **Enviados**, **Abiertos** y **Clics** — un punto por día, cubriendo los 30 días anteriores a hoy (o menos, si la campaña no ha estado enviando durante tanto tiempo: el gráfico nunca comienza antes del día del primer envío de la campaña).

Hay algunas cosas que saber sobre cómo se cuentan las líneas:

- **Abiertos** y **Clics** cuentan a cada destinatario una vez: el día de su *primera* apertura o *primer* clic, no cada vez que vuelven a abrir el correo o hacen clic en un enlace de nuevo. Esto evita que el gráfico se distorsione por un puñado de personas que abren el mismo correo repetidamente.
- Los totales detrás de este gráfico coinciden con las tarjetas de estadísticas anteriores: **Enviados** refleja el correo que Spwig intentó entregar, mientras que **Abiertos** y **Clics** se miden en relación con el correo entregado, igual que las tarjetas de **Tasa de apertura** y **Tasa de clics**.
- El gráfico solo aparece una vez que la campaña tiene al menos un envío registrado: una campaña aún en **Borrador** muestra el mensaje "Aún no hay envíos" en su lugar, igual que las tarjetas de estadísticas.

Usa este gráfico para ver la *forma* de un envío, no solo sus números finales: una campaña que se envía a una lista grande a menudo muestra un pico agudo en aperturas durante los primeros uno o dos días, disminuyendo después. Un segundo aumento días después puede indicar que el servidor de correo del destinatario está encolando tu mensaje, o que tu línea de asunto se notó más tarde de lo habitual.

## Enlaces principales

Si tu correo electrónico contiene enlaces y al menos un destinatario ha hecho clic en uno, aparece una tabla de **Enlaces principales** debajo del gráfico, que lista todos los enlaces rastreados ordenados por popularidad.

| Columna | Qué muestra |
|--------|---------------|
| **Enlace** | La URL de destino tal como apareció en su correo electrónico. |
| **Clics** | El número total de veces que se hizo clic en ese enlace, incluidos los clics repetidos del mismo destinatario. |
| **Únicos** | Cuántos destinatarios distintos hicieron clic en ese enlace en particular al menos una vez. |
| **CTR** | La **tasa de clics** de ese enlace: su recuento de **Únicos** como proporción de los correos entregados. Esto utiliza el mismo denominador que la tarjeta **Tasa de clics** principal del informe, por lo que puede comparar el atractivo de un solo enlace directamente con el rendimiento general de clics de la campaña. |

Si su correo electrónico enlaza a varios productos o a una mezcla de botones de llamada a la acción, esta tabla es la forma más rápida de ver cuál de ellos realmente obtuvo el clic, lo cual es útil para decidir qué destacar más la próxima vez.

## Destinatarios

Haga clic en **Destinatarios** en la parte superior del informe para abrir una lista completa y buscable de todas las personas a las que se envió esta campaña, con el resultado de entrega y la interacción de cada persona.

Dos formas de filtrar la lista:

- **Buscar** — filtra por dirección de correo electrónico (funciona con coincidencia parcial, por lo que escribir parte de un dominio o nombre es suficiente).
- **Interacción** — filtra por un estado a la vez: **Abierto**, **Clic**, **Entregado, no abierto** o **Rebotado**. Déjelo en **Todos** para ver la lista completa.

La lista muestra los 100 destinatarios coincidentes más recientes a la vez, del más nuevo al más antiguo; el recuento sobre la lista siempre refleja el total real que coincide con sus filtros actuales, incluso si es mayor que lo mostrado. Para un envío grande, filtre la lista primero con Buscar o Interacción en lugar de desplazarse por todos.

### Ver la línea de tiempo de actividad de un destinatario

Haga clic en el icono de actividad en la fila de cualquier destinatario para abrir su línea de tiempo de **Actividad del destinatario**: todos los eventos rastreados para la copia del correo electrónico de esa persona, en orden: entregado, abierto, clic (indicando qué enlace), rebotado (con la razón del rebote), marcado como spam o dado de baja, cada uno con su propia marca de tiempo.

Esta es la forma más rápida de responder a una pregunta específica sobre un cliente: por ejemplo, confirmar si un suscriptor en particular recibió realmente una campaña antes de seguir en contacto con él por otro canal, o verificar qué enlace hizo clic un cliente antes de realizar un pedido.

## Informes sobre una prueba A/B

Si la campaña que está viendo es el contenedor de una [prueba A/B](ab-testing), su informe agrega datos de **todas las variantes**: la prueba completa, combinada, incluido el **Ingresos atribuidos**, en lugar de mostrar una variante por separado. Para ver cómo se desempeñó cada variante individual, abra la página de resultados de la prueba en lugar del informe. Una [campaña recurrente](recurring-campaigns) funciona de la misma manera: su informe resume todas las ocurrencias que ha enviado.

## Qué se considera un buen resultado

No existe un único número saludable que se ajuste a cada tienda o lista: la audiencia, la industria y el contenido cambian la línea base, pero hay algunos patrones que vale la pena observar en cualquier campaña:

- Una **tasa de rebote** que consiste principalmente en rebotes suaves, con rebotes duros poco frecuentes, indica una lista limpia y bien mantenida. Un aumento repentino en los rebotes duros merece una investigación antes del próximo envío.
- Las **quejas de spam** cercanas a cero son el objetivo en cada envío. Las quejas dañan su reputación de remitente más que casi cualquier otra cosa; consulte [Higiene de la lista](list-hygiene) para saber por qué son importantes más allá de esta campaña.
- Una **tasa de clics por apertura** saludable en relación con su tasa de apertura le indica que las personas que abrieron el correo encontraron el contenido digno de acción; una tasa de clics por apertura baja junto con una tasa de apertura fuerte generalmente indica que la línea de asunto funcionó mejor que el contenido interno.

## Consejos

- Compruebe el informe un poco después del envío, no inmediatamente: las aperturas y clics (y algunos informes de rebote) pueden tardar en llegar desde su proveedor de correo.
- Si **Entregado** parece más bajo de lo esperado, revise primero el desglose de omisiones de la tarjeta **Destinatarios**: un lote de omisiones por supresión suele ser la verdadera causa, no un problema de entrega.
- Use el informe para comparar una campaña con sus propios envíos anteriores, en lugar de con una cifra genérica del sector: su lista, contenido y audiencia son lo que establecen su línea base realista.
- Un aumento de quejas en un envío en particular merece un examen más detallado del contenido o la segmentación de esa campaña, no solo una nota para pasar al siguiente.
- Para una campaña con prueba A/B, lea este informe para el resultado general y la página [Resultados de la prueba A/B](ab-testing) para saber qué variante ganó realmente y por cuánto.
- Use la tabla **Enlaces principales** para encontrar el enlace con más clics y luego verifique si coincide con lo que *quería* que los destinatarios hicieran: si un enlace secundario supera a su llamada a la acción principal, puede valer la pena moverlo más arriba en el correo la próxima vez.
- Los filtros **Abierto** y **Clic** de la página **Destinatarios** son una forma rápida de crear una audiencia para seguimiento: por ejemplo, verificar quién abrió pero no hizo clic antes de planificar un envío de recordatorio al resto de la lista.
- Si pagó por una promoción alrededor de un envío — una publicación social impulsada, una mención de un influencer, alquiler de lista pagado — regístrelo como **Gasto** de la campaña para desbloquear **ROAS** en el informe.

Es la forma más rápida de ver qué tipos de envíos realmente valen la pena repetir.