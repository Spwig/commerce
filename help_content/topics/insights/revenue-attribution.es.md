---
title: Asignación de ingresos
---

La asignación de ingresos le muestra dónde realmente provienen sus ventas: no solo el único enlace al que hizo clic un cliente antes de comprar, sino cada canal que tuvo un papel en lograrlo. Si un cliente lee un artículo de blog que compartió en redes sociales, luego vuelve una semana después a través de una búsqueda de Google y finalmente compra después de hacer clic en un enlace de un boletín informativo, esos tres contactos contribuyeron a esa venta. Este panel le otorga crédito a todos ellos, utilizando un modelo que elija, para que pueda ver su marketing tal como realmente funciona en lugar de como "el último clic gana" pretende que funcione.

![El panel de asignación de ingresos: el selector de modelo de asignación, la cinta de KPI con el sello "Reconcilia a ingresos netos", ingresos por canal, ingresos en el tiempo, el flujo del viaje del cliente y la tabla de campañas](/static/core/admin/img/help/revenue-attribution/dashboard-overview.webp)

## Dónde encontrarlo

Navegue hasta **Conocimientos > Asignación de ingresos** en el menú lateral. Conocimientos es un grupo de menús dedicado por encima de Productos, por lo que Asignación de ingresos tiene su propio hogar separado de sus informes de pedidos y clientes.

Conocimientos está restringido por la categoría de permiso **Conocimientos y análisis**. Si no lo ve en su menú lateral, pida a un administrador de tienda que le otorgue ese permiso - consulte [Roles y permisos del personal](/help/staff-roles) para cómo administrar el acceso del personal.

## Comprendiendo la asignación de múltiples toques

La mayoría de las tiendas están acostumbradas a pensar en términos de "dónde vino este pedido?" como si hubiera una única respuesta. En la realidad, los clientes rara vez compran en su primera visita. Descubren su tienda de una manera, regresan de otra manera y convierten de una tercera manera - a veces a través de varias visitas distribuidas durante días o semanas. Cada una de esas visitas es un **tocado**: una llegada registrada a su tienda que lleva una señal sobre dónde vino (un enlace de correo electrónico, un resultado de búsqueda, un mensaje en redes sociales, un enlace de afiliado, etc.).

**La asignación de múltiples toques** significa reconocer cada toque en ese viaje y decidir cuánto crédito merece cada uno para la venta final, en lugar de otorgarle el 100% del crédito al canal que sucedió únicamente al último clic. Esto es importante porque la informe de único clic subestima sistemáticamente los canales que realizan el trabajo de descubrimiento temprano - su blog, su presencia en búsqueda orgánica, sus publicaciones en redes sociales - porque rara vez son el único clic antes de finalizar la compra.

## Elegir un modelo de asignación

El selector de modelo en la parte superior del panel es el control más importante de la página. Haga clic en cualquier modelo y cada número del panel - la cinta de KPI, las barras de canal, el gráfico, la tabla de campañas - se recredita instantáneamente para coincidir. Este es una vista previa en vivo: cambiar modelos aquí cambia la forma en que está mirando sus ingresos existentes, no reescribe registros ni cambia el modelo predeterminado guardado de su tienda.

![El selector de modelo de asignación - Último toque, Primer toque, Lineal, Decaimiento del tiempo y Posición 40/20/40 - con el indicador "Reasigna en vivo · sin procesamiento nuevamente"](/static/core/admin/img/help/revenue-attribution/model-switcher.webp)

| Modelo | Qué hace | Ideal para |
|-------|---------------|----------|
| **Último contacto** | Otorga el crédito completo al último canal antes del pedido, ignorando los contactos anteriores (excepto las visitas puras de "directo", que se omiten a favor del último origen real) | Una visión rápida y familiar: cómo suelen informar las herramientas básicas de análisis de ingresos |
| **Primer contacto** | Otorga el crédito completo al canal que primero trajo al cliente a tu tienda | Comprender qué está impulsando el descubrimiento de nuevos clientes y el crecimiento en la parte superior del embudo |
| **Lineal** | Distribuye el crédito de manera equitativa en cada contacto del viaje | Una visión equilibrada, sin opiniones, cuando no quieres favorecer ningún canal en particular |
| **Decaimiento del tiempo** | Otorga más crédito a los contactos más cercanos al pedido y menos a los más antiguos | Campañas con un plazo de consideración corto, donde los empujones recientes importan más |
| **Posición 40/20/40** | Otorga el 40% de crédito al primer contacto, el 40% al último contacto y se reparte el 20% restante entre todo lo demás | Reconocer tanto "quiénes nos encontraron" como "quiénes cerraron la venta", mientras se otorga crédito al medio del viaje |

No existe un "modelo correcto" único — cada uno responde a una pregunta diferente. Un enfoque común es revisar **Primer contacto** para ver qué está impulsando el descubrimiento, luego **Último contacto** o **Posición 40/20/40** para ver qué está impulsando las conversiones, y usar ambas vistas juntas en lugar de elegir una y ignorar el resto.

## Leyendo la tira de KPI

Justo debajo del selector de modelo, cuatro cifras resumen el período seleccionado y el modelo:

- **Ingresos atribuidos** — el ingreso total creditado a través de todos los canales para el modelo actual. Lleva un sello de **Se ajusta al ingreso neto** cuando las cifras suman correctamente al ingreso neto real de tu tienda para el período — en otras palabras, el modelo está dividiendo los ingresos reales entre los canales, en lugar de inventar o perder alguno.
- **Pedidos** — cuántos pedidos caen en el rango de fechas seleccionado.
- **Promedio de contactos por pedido** — el número promedio de contactos registrados por pedido. Un número mayor a 1 confirma que la mayoría de los viajes de tus clientes involucran más de una visita, lo cual es exactamente por qué la atribución de múltiples contactos es importante para tu tienda.
- **Canal líder** — el canal que actualmente tiene la mayor parte de los ingresos atribuidos bajo el modelo seleccionado, con su porcentaje de participación y el ingreso.

## Ingresos por canal

La tarjeta **Ingresos por canal** muestra una barra horizontal por cada canal, con tamaño según los ingresos atribuidos. Cambia el modelo de atribución y observa cómo las barras se reordenan suavemente por orden de clasificación — esto es el mismo ingreso subyacente, solo que se vuelve a dividir según un conjunto diferente de reglas, por lo que un canal que parece fuerte bajo **Último contacto** puede bajar varios puestos bajo **Primer contacto** si principalmente juega un papel secundario.

## Ingresos con el tiempo

El gráfico **Ingresos con el tiempo** apila los ingresos atribuidos por canal en cada día del rango seleccionado, por lo que puedes ver no solo cuánto vale cada canal, sino también cuándo contribuye. Úsalo para detectar patrones estacionales, confirmar que el impacto de una campaña aterrizó en los días que esperabas o verificar si la contribución de un canal está creciendo o disminuyendo durante el período.

## Cómo llegan realmente los clientes

El panel **Cómo llegan realmente los clientes** es un gráfico de flujo de viaje que conecta el canal que primero trajo al cliente (a la izquierda) con el canal presente cuando convirtió (a la derecha). Cintas más gruesas significan que más ingresos fluyeron a través de ese camino. Esta es la forma más clara de ver viajes de varios pasos a simple vista — por ejemplo, una cinta gruesa de Búsqueda Orgánica a Correo electrónico te dice que la búsqueda trae personas, pero tu marketing por correo electrónico es lo que las vuelve a traer a comprar.

![El gráfico de flujo del viaje del cliente, con la lente "Influidos" seleccionada, mostrando canales de primer contacto en el lado izquierdo que fluyen al canal en el que cada pedido se convirtió](/static/core/admin/img/help/revenue-attribution/journey-flow-sankey.webp)

Usa el interruptor **Atribuido** / **Influido** ubicado arriba del gráfico para cambiar las lentes.

- **Asignado** divide los ingresos de cada pedido según el modelo que haya seleccionado, de modo que los totales sumen el 100 % de los ingresos asignados, que son los mismos que se muestran en otras partes del panel de control.
- **Influido** otorga *cada* canal que haya tenido contacto con un pedido con el *valor completo* del pedido, contabilizándolo una vez por pedido.

Esto no suma necesariamente el 100 %, ya que un canal puede estar *influido* por ingresos que también se cuentan completamente para otro canal.

Esto sirve para mostrar el alcance que tuvo un canal, algo que la informe de último clic oculta por completo, como un artículo de blog o un compartido en redes sociales que generó interés incluso aunque no se haya hecho clic en él durante la visita final.

## Campañas

La tabla **Campañas** desglosa los ingresos, pedidos y valor promedio de los pedidos (AOV) de cada una de tus campañas etiquetadas — enlaces o códigos que has etiquetado con el nombre de una campaña, incluyendo códigos de descuento etiquetados con campañas (véase [Ideas para campañas de cupones](/help/voucher-campaign-ideas)). Úsala para comparar el rendimiento de promociones individuales, códigos de influencers o campañas de marketing entre sí, independientemente de qué canal las haya llevado.

## Rango de fechas y exportación de tus datos

Usa el selector de rango de fechas en la esquina superior derecha para cambiar entre **Últimos 7 días**, **Últimos 14 días**, **Últimos 30 días**, **Últimos 90 días** y **Mes hasta la fecha**. El panel de control completo se vuelve a cargar para el nuevo período.

Haz clic en **Exportar CSV** para descargar el desglose por canal para el modelo y rango de fechas seleccionados actualmente — útil para extraer los datos en una hoja de cálculo o compartirlos con una agencia colaboradora.

## Cómo se registran los contactos

Spwig captura automáticamente un contacto cada vez que un visitante llega a tu tienda con una señal de origen reconocible, y solo cuando el visitante haya dado su **consentimiento de análisis** en el aviso de cookies de tu tienda (si no usas un aviso de consentimiento, el seguimiento está activado por defecto, según lo que determine la política de tu tienda). Esto mantiene la atribución de ingresos en el mismo nivel de privacidad que el resto de las analíticas de tu tienda.

Varios orígenes se etiquetan automáticamente, sin necesidad de configuración:

| Canal | Cómo se identifica |
|---------|----------------------|
| **Email** | Enlaces en tus correos de marketing (no en correos de pedidos o envíos) |
| **Búsqueda orgánica / de pago** | Referrers de motores de búsqueda, o valores de `utm_medium` que marcan una campaña de búsqueda de pago |
| **Redes sociales orgánicas / de pago** | Referrers de redes sociales, o valores de `utm_medium` de redes sociales |
| **Afiliado** | Enlaces generados a través de tu programa de afiliados |
| **Invita a un amigo** | Enlaces generados a través de tu programa de referidos de clientes |
| **Campaña** | Cualquier enlace o código que lleve una etiqueta de campaña, incluyendo códigos de descuento etiquetados con campañas |
| **Enlace externo** | Un enlace entrante desde otro sitio web que no se clasifica de otra manera |
| **Directo** | No había señal de origen — el visitante escribió la dirección, usó un marcador o llegó desde una aplicación sin referrer |

Los artículos de blog que se compartieron automáticamente a tus cuentas de redes sociales conectadas se etiquetan automáticamente, por lo que el tráfico que generen aparece bajo el canal de redes sociales correspondiente, en lugar de perderse en Directo o Enlace externo.

También puedes etiquetar tus propios enlaces manualmente usando parámetros estándar `utm_source`, `utm_medium` y `utm_campaign` en cualquier URL que apunte a tu tienda — útil para materiales impresos, boletines de socios o cualquier canal que Spwig no etiquete automáticamente.

## Limitaciones a tener en cuenta

- **La atribución sigue un navegador, no a una persona.** Si un cliente investiga en su teléfono y compra en su portátil, son dos viajes separados en cuanto a seguimiento se refiere — no hay forma de vincular la actividad entre dispositivos diferentes.

Esto significa que algún crédito que "debería" ir a un toque anterior en otro dispositivo terminará en Directo en lugar de en el canal de origen.
- **Directo es donde aterriza el ingreso no registrado.** Un alto porcentaje de Directo no necesariamente significa que la gente esté escribiendo su URL de memoria: también puede significar que los toques anteriores de un cliente hayan ocurrido en otro dispositivo, o que un enlace que usaron no esté etiquetado.
- **El rechazo del consentimiento significa que no se registra ningún toque.** Los visitantes que rechacen el consentimiento de análisis en su banner de cookies no se rastrean, por lo que sus pedidos aparecerán como Directo incluso si llegaron a través de un canal que normalmente reconocería.

## Consejos

- Revise más de un modelo antes de sacar conclusiones: un canal que parece débil bajo **Último toque** puede ser su principal motor de descubrimiento bajo **Primer toque**.
- Si **Directo** representa una parte grande de sus ingresos, revise si más de sus enlaces de marketing podrían etiquetarse con `utm_source`/`utm_medium`/`utm_campaign` — el tráfico no etiquetado no tiene otro lugar al que llegar.
- Use la lente **Influidas** en el gráfico de flujo de la jornada cuando esté decidiendo si es conveniente seguir invirtiendo en un canal como búsqueda orgánica o contenido de blog que rara vez obtenga el último clic, pero que invariablemente inicie jornadas.
- Compare el **Promedio de toques por pedido** con el tiempo — un número creciente generalmente significa que los clientes tardan más en decidirse, lo cual es una señal útil al planificar el horario de correos electrónicos de seguimiento o de retargeting.
- Exporte el CSV del modelo y período en los que esté realizando el informe antes de volver a cambiar de modelo, ya que la exportación refleja el modelo seleccionado en el momento en que haga clic en **Exportar CSV**.