---
title: Públicos
---

Un **Segmento** es un público guardado al que puedes apuntar una campaña, un recorrido o una prueba A/B — la lista de segmentos propios de Campaign Studio los llama "públicos dirigidos", y esta guía utiliza ambos términos para lo mismo. Cada segmento es o bien **dinámico**, definido por reglas que Spwig vuelve a evaluar cada vez que se usa, o bien **estático**, una lista explícita de suscriptores que eliges manualmente.

Esta guía cubre la creación de las reglas de un segmento dinámico — incluyendo campos más nuevos que apuntan a los grupos de valor de clientes de tu tienda, el programa de lealtad y los socios afiliados — y el botón **Añadir públicos iniciales** de un solo clic que crea un conjunto de segmentos listos para usar a partir de cualquier dato que ya tenga tu tienda.

## Segmentos dinámicos frente a estáticos

| Tipo | Cómo funciona | Para qué sirve |
|---|---|---|
| **Dinámico (reglas)** | Estableces condiciones — por ejemplo, "Gastó al menos 500 dólares." Spwig recalcula quiénes coinciden cada vez que se usa el segmento, por lo que la membresía se actualiza automáticamente a medida que cambian tus suscriptores. | Públicos continuos que siempre deben estar actualizados, como "clientes VIP" o "no ha comprado en 90 días."
| **Estático (lista fija)** | Una lista explícita de suscriptores que añades o eliminas manualmente. La membresía nunca cambia a menos que lo hagas tú. | Una lista única — todos de un evento específico, o un grupo seleccionado manualmente para un envío único. |

Elige el tipo con el campo **Tipo** al crear un segmento. El resto de esta guía se trata de segmentos dinámicos — los estáticos son simplemente una lista de miembros sin reglas para configurar.

## Crear un segmento dinámico

Abre **Campaign Studio > Segmentos**, luego haz clic en **+ Nuevo segmento** (o abre un segmento dinámico existente) para llegar al constructor de **Reglas del público**. Haz clic en **+ Añadir condición** para añadir una regla, elige qué comprobar y cómo, y establece si un suscriptor debe cumplir **todos** o **algunos** de tus condiciones. Un recuento en vivo en la esquina superior derecha — por ejemplo, "8 suscriptores coincidentes" — se actualiza un momento después de cada cambio, para que veas exactamente a quién califica antes de guardar.

![El constructor de reglas del público con los campos de segmento de cliente, nivel de lealtad, valor de por vida y condiciones de afiliado configurados, y un recuento de suscriptores que coinciden en tiempo real](/static/core/admin/img/help/audiences/rule-builder-new-fields.webp)

Una condición con una comprobación de estilo **es verdadero** — **Ha comprado**, **Optó por el marketing**, **Miembro de lealtad**, **Afiliado** — solo necesita seleccionar el campo en sí; no hay operador o valor que configurar.

## A qué puedes apuntar

| Campo | A qué se refiere |
|---|---|
| **Gasto total** | Total de pedidos a lo largo de la vida. |
| **Número de pedidos** | Cantidad de pedidos completados. |
| **Valor de por vida** | Valor calculado del cliente a lo largo de su vida. |
| **Valor promedio del pedido** | Cantidad promedio por pedido completado. |
| **Días desde el último pedido** | Cuánto tiempo ha pasado desde el último pedido del cliente — apunta a 90+ días para un público de recuperación. |
| **Ha comprado** | Si el cliente tiene al menos un pedido completado. |
| **Optó por el marketing** | Si el suscriptor ha consentido recibir correos electrónicos de marketing. |
| **Idioma** | El idioma almacenado del suscriptor. |
| **Origen** | Cómo se unió el suscriptor — registro en tienda, importación, pedido, añadido manualmente o API. |
| **Se unió después de** | Suscriptores que se unieron el día elegido o posterior. |
| **Tiene etiqueta** | Si el suscriptor tiene una [etiqueta](/help/subscriber-tags) que has creado. |
| **Segmento de cliente** | Si el cliente cae en uno de los [segmentos de cliente](/help/customer-segments) propios de tu tienda — Cliente de invitado, Cliente nuevo, Cliente regular, Comprador frecuente, Cliente de alto valor, Cliente VIP, Buscador de ofertas, Cliente en riesgo o Inactivo. |
| **Miembro de lealtad** | Si el cliente es miembro activo de tu programa de lealtad. |
| **Puntos de lealtad** | El saldo actual de puntos disponibles del miembro. |
| **Nivel de lealtad** | A qué nivel de lealtad pertenece actualmente el miembro. |
| **Afiliado** | Si el cliente es uno de tus socios afiliados activos. |

**Segmento de clientes**, los dos campos de valor **Lealtad**, **Nivel de lealtad** y **Afiliado** son adiciones más recientes, y cada uno solo aparece en el selector de condiciones una vez que su tienda realmente tenga ese tipo de datos: los campos de lealtad aparecen una vez que su programa de lealtad tiene miembros y al menos un nivel activo, **Afiliado** aparece una vez que tenga al menos un afiliado, y **Segmento de clientes** aparece una vez que tenga al menos un segmento de clientes activo configurado.

No verá una opción en una tienda recién creada que no pueda coincidir con nadie.

Un límite actual que vale la pena conocer: para cualquier condición con un menú desplegable de opciones — **Idioma**, **Origen**, **Tener etiqueta**, **Segmento de clientes**, **Nivel de lealtad** — el operador **es alguno de** aún solo le permite elegir un valor a la vez. Si quiere coincidir con varios (por ejemplo, clientes en su segmento VIP o de Alto Valor), agregue una condición por valor y establezca **Coincidir** en **cualquiera**.

## Añadir audiencias iniciales

Construir una regla desde cero para cada audiencia obvia — sus VIP, sus miembros de lealtad, todos los que se han vuelto silenciosos — es tedioso cuando Spwig ya puede ver quién califica. En la lista de Segmentos, haga clic en **Añadir audiencias iniciales** y Spwig crea un conjunto de segmentos dinámicos listos para editar a partir de cualquier dato de cliente, lealtad y afiliado que ya tenga su tienda.

![La lista de Segmentos con los botones Nuevo segmento y Añadir audiencias iniciales](/static/core/admin/img/help/audiences/segments-changelist.webp)

| Iniciador | Objetivos | Necesidades |
|---|---|---|
| **Clientes VIP** | Su segmento de clientes VIP | Un segmento de clientes VIP activo |
| **Clientes de alto valor** | Sus segmentos de clientes VIP y Alto Valor | Un segmento de clientes VIP o Alto Valor activo |
| **Compradores recurrentes** | Sus segmentos de clientes Frecuentes y Regulares | Un segmento de clientes Frecuentes o Regulares activo |
| **Nuevos clientes** | Su segmento de clientes nuevos | Un segmento de clientes nuevos activo |
| **Clientes que se han vuelto silenciosos** | Clientes que han hecho pedidos anteriormente pero no en los últimos 90 días | Cualquier historial de pedidos de cliente |
| **Miembros de lealtad** | Todos los que están activos en su programa de lealtad | Un programa de lealtad activo con miembros |
| **Nivel de lealtad más alto** | Miembros en su nivel de lealtad más alto | Al menos un nivel de lealtad activo |
| **Afiliados** | Sus socios afiliados activos | Al menos un afiliado |

Spwig solo crea los inicios para los que realmente tiene datos: una tienda sin programa de lealtad aún simplemente no recibirá un iniciador de **Miembros de lealtad**, sino que en lugar de eso, recibirá uno vacío que nunca podría coincidir con nadie. Spwig confirma exactamente lo que agregó, por ejemplo: "Agregados 7 audiencias iniciales: Clientes de alto valor, Compradores recurrentes, Nuevos clientes, Clientes que se han vuelto silenciosos, Miembros de lealtad, Nivel de lealtad más alto, Afiliados."

![Mensaje de éxito que confirma qué audiencias iniciales acaban de agregarse](/static/core/admin/img/help/audiences/starter-audiences-added.webp)

Es seguro hacer clic en **Añadir audiencias iniciales** más de una vez. Spwig nunca crea un duplicado de un iniciador que ya existe, por lo que hacer clic en él nuevamente después de configurar (por ejemplo) su programa de lealtad por primera vez solo agrega lo que está disponible recién — si todo está configurado, simplemente lo indica.

![Mensaje de información mostrado cuando cada audiencia inicial ya existe](/static/core/admin/img/help/audiences/starter-audiences-already-set-up.webp)

Si elimina un iniciador que no quiera, hacer clic en **Añadir audiencias iniciales** nuevamente no lo recuperará — Spwig lo trata como un segmento que eliminó intencionadamente, no como uno que se vaya a recrear.

Una vez que se ha creado, un iniciador es un segmento dinámico ordinario: ábralo desde la lista para revisar o ajustar sus reglas, renombrarlo o eliminarlo, exactamente como lo haría con cualquier segmento que haya creado usted mismo.

## Quienes alcanzan realmente estas audiencias

Las condiciones de cliente, lealtad y afiliado anteriores solo coinciden con suscriptores cuyo correo electrónico esté vinculado a una cuenta de cliente; una suscripción anónima a la boletín no coincidirá con una condición de **Miembro de lealtad** o **VIP**, y con razón, ya que Spwig no tiene historial de pedidos ni de lealtad contra el cual verificarlos.

Si muchos de sus clientes tienen cuentas pero aún no se han suscrito, pida a quien gestione su instalación de Spwig que ejecute una sincronización de suscriptores: crea un registro de Suscriptor para cada cuenta de cliente existente en un solo paso, de modo que estas audiencias tengan personas reales con las que coincidir.

Sin importar cuántos suscriptores cuente un segmento, ese número describe a quienes *podrían* recibir una campaña, no a quienes la recibirán. Cada envío verifica primero el consentimiento de marketing de cada suscriptor, por lo que un segmento nunca es una forma de eludirlo.

## Consejos

- Comience con una audiencia inicial y ajústela en lugar de construir la misma regla manualmente: una vez creada, una audiencia inicial no difiere de ningún segmento que haya construido usted mismo.
- Las condiciones booleanas como **Miembro de lealtad**, **Afiliado** y **Ha realizado un pedido** no requieren operador ni valor: solo agregue la condición y estará listo.
- Combine los campos más nuevos con los originales para un segmentación más precisa, por ejemplo, **Miembro de lealtad** más **Se ha suscrito al marketing**, en lugar de depender de una sola condición por sí sola.
- Si las reglas de un segmento hacen referencia a algo que se ha eliminado desde entonces —un segmento de cliente eliminado, una etiqueta vaciada, etc.—, Spwig lo trata como que no coincide con nadie, en lugar de volver a su lista completa de suscriptores. Una segmentación rota envía menos; nunca envía a todos por accidente.
- Si el recuento de miembros de un segmento parece desactualizado, ábralo y guárdelo de nuevo, o use la acción masiva **Recalcular recuentos de miembros** desde la lista de Segmentos, para recalcularlo de inmediato.
- Observe el recuento en vivo de "suscriptores coincidentes" mientras construye una regla: es la forma más rápida de detectar una condición que es más estrecha (o más amplia) de lo que pretendía antes de guardar.