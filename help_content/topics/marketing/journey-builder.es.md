---
title: Constructor de Viajes
---

<!-- screenshots-needed:
- url: /admin/campaigns/journeys/  (open any journey's builder, click Templates)
  filename: journey-builder-templates.webp
  description: El selector de plantillas con los ocho comienzos visibles (serie de bienvenida,
    onboarding de primer pedido, revisión posterior a la compra y comentario, oferta VIP frente a estándar, recuperación de carrito abandonado, recuperación de clientes que no se han conectado, solicitud de revisión posterior a la entrega, alerta de reposición en stock) — reemplaza la captura de pantalla de cuatro plantillas existentes en la misma ruta, que ahora está obsoleta.
  save-to: core/static/core/admin/img/help/journey-builder/
  viewport: 1440x900
-->

El **Constructor de Viajes** es el lienzo visual, con arrastrar y soltar, donde diseñas lo que hace realmente un [Viaje](/help/triggered-journeys) — qué correos electrónicos se envían, cuánto tiempo esperar entre ellos y si diferentes suscriptores deben seguir caminos diferentes. En lugar de rellenar un formulario, construyes el flujo como un diagrama de flujo: cajas conectadas en un lienzo que puedes reorganizar, ramificar y previsualizar a simple vista.

## Abrir el constructor

Cada viaje tiene su propio lienzo del constructor. Puedes acceder a él de dos maneras:

- Crear un nuevo viaje: completa su **Nombre**, **Disparador** y audiencia en la página de configuración y haz clic en **Guardar** — te lleva directamente al constructor para que comiences a diseñar de inmediato.
- Abrir la página de configuración de un viaje existente y hacer clic en **Diseñar viaje** en la parte superior.

El constructor es un espacio de trabajo de pantalla completa con tres áreas: un **paleta** de tipos de paso en el lado izquierdo, el **lienzo** en el centro y un panel de **configuración del paso** en el lado derecho que aparece cuando seleccionas algo.

![El lienzo del constructor de viajes que muestra una serie de bienvenida con una rama Sí/No](/static/core/admin/img/help/journey-builder/journey-builder-canvas.webp)

En la parte superior del lienzo, un encabezado repite el **Disparador** del viaje y la **audiencia** (o "Todos los suscriptores" si no se establece un segmento) para que siempre sepas a quién estás diseñando sin salir del constructor. Usa el botón **Atrás** para regresar a la página de configuración del viaje.

## Los tipos de paso

Arrastra un paso desde la paleta izquierda al lienzo, o haz clic en un elemento de la paleta para colocarlo automáticamente. Están disponibles cuatro tipos de paso:

| Paso | Lo que hace |
|------|--------------|
| **Enviar correo electrónico** | Envía una de tus campañas al suscriptor. |
| **Esperar** | Pausa durante un número definido de horas o días antes de continuar. |
| **Rama** | Divide el camino en dos — **Sí** o **No** — según si el suscriptor pertenece a un segmento que elijas. |
| **Salir** | Finaliza el viaje para el suscriptor. |

Todo viaje comienza con un único paso de **Entrada**, creado automáticamente la primera vez que abres el constructor. Muestra el disparador del viaje y no se puede borrar: simplemente es el punto donde los suscriptores ingresan al flujo.

## Conectar pasos

Cada paso tiene un pequeño círculo **puerto**: uno en la parte superior (entrada) y uno o más en la parte inferior (salida). Para conectar dos pasos, arrastra desde el puerto inferior de un paso al puerto superior de otro — aparece una línea curva que los conecta.

Un paso de **Rama** tiene dos puertos de salida en lugar de uno: un **Sí** verde y un **No** rojo. Conecta cada uno a cualquier lugar que deba seguir ese camino — pueden unirse nuevamente en el mismo paso (como en el ejemplo anterior, donde ambos caminos llevan de vuelta al mismo **Salir**) o pueden seguir caminos completamente separados.

Para reorganizar el diseño, arrastra un paso por su cuerpo para reubicarlo — las líneas conectadas siguen automáticamente. Arrastra una parte vacía del fondo del lienzo para navegar, y usa la rueda de desplazamiento para acercar o alejar. Si pierdes la pista del flujo, haz clic en **Ajustar** en la barra de herramientas para recenter y acercar para que todo se vea en la pantalla.

## Configurar un paso

Haz clic en cualquier paso para abrir su configuración en el panel de la derecha:

| Paso | Configuración |
|------|---------|
| **Enviar correo electrónico** | Seleccione el **Correo electrónico a enviar** de un menú desplegable de sus campañas. |
| **Esperar** | Establezca **Esperar a** — un número más **horas** o **días**. |
| **Rama** | Elija **Si el suscriptor está en un segmento** — el segmento que decide Sí vs. No. |
| **Salida** | No hay configuraciones — es solo un punto final. |

![El panel de la derecha que configura un paso de Rama, con el lienzo oscurecido detrás](/static/core/admin/img/help/journey-builder/journey-builder-branch-config.webp)

Los cambios se guardan automáticamente tan pronto elige un valor — no hay un botón **Guardar** separado en el lienzo. Cada paso excepto **Entrada** tiene un botón **Eliminar paso** en la parte inferior de su panel de configuración.

Los correos electrónicos que elija para los pasos **Enviar correo electrónico** son campañas ordinarias que diseña en el constructor visual regular de Campaign Studio — línea de asunto, bloques de contenido, todo. Déjelos como **Borrador** y simplemente eléjalo del menú desplegable aquí; el trayecto los envía por usted, usted nunca hace clic en Enviar en ellos mismo.

## Empezar desde una plantilla

No siempre es necesario construir un flujo desde cero — haga clic en **Plantillas** en la barra de herramientas (o **Buscar plantillas** en un lienzo vacío) para abrir un selector con ocho iniciadores listos:

| Plantilla | Lo que crea |
|----------|-----------------|
| **Serie de bienvenida** | Salude a los suscriptores nuevos, comparta lo que usted está haciendo, luego una sugerencia de primer pedido. |
| **Onboarding de primer pedido** | Convierta a un comprador por primera vez en un cliente repetido con una secuencia de onboarding suave. |
| **Post-compra y revisión** | Diga gracias después de cualquier pedido, luego pida una revisión una vez que haya llegado. |
| **Oferta VIP vs. estándar** | Después de un pedido, ramas en su segmento VIP para enviar la oferta de seguimiento adecuada a cada grupo. |
| **Recuperación de carrito abandonado** | Recuerde a un comprador que dejó artículos atrás, luego un recordatorio posterior un día después. |
| **Recuperación de clientes abandonados** | Reconecte a un cliente que no ha comprado en un tiempo con un motivo para regresar. |
| **Solicitud de revisión después de la entrega** | Pida una revisión unos días después de que un pedido se marque como Entregado. |
| **Alerta de reposición de stock** | Dígale a un comprador que espera el momento en que un producto que quería esté disponible nuevamente. |

Cada plantilla está conectada previamente al disparador correspondiente — por ejemplo, aplicar **Recuperación de clientes abandonados** a un nuevo trayecto también espera que el **Disparador** de ese trayecto sea **Cliente abandonado (recuperación)**. Vea [Trayectos disparados](/help/triggered-journeys) para ver qué activa cada uno de estos eventos de disparo y cómo se comportan las que tienen enfoque de recuperación (ventanas de inactividad, compras de invitados, solicitudes de revisión por pedido, y cómo un trayecto de reposición de stock reemplaza al alerta simple).

![El selector de plantillas que muestra los trayectos iniciales listos](/static/core/admin/img/help/journey-builder/journey-builder-templates.webp)

Aplicar una plantilla **reemplaza el flujo actual** en el lienzo, así que úsela al comienzo de la creación de un trayecto en lugar de en medio. Spwig vuelve a conectar cada paso a un correo electrónico o segmento real donde los nombres coincidan con algo que ya tenga; en cualquier lugar donde no pueda encontrar una coincidencia, el encabezado informa cuántos pasos aún necesitan que se elija un correo electrónico o segmento para que sepa exactamente qué terminar antes de ponerlo en marcha.

## Compartir trayectos

Dos botones de barra de herramientas le permiten mover el diseño de un trayecto entre pasos o entre tiendas:

- **Exportar** descarga el trayecto como un archivo `.journey.json` — una descripción portátil de la forma del flujo (sus pasos, tiempos de espera, ramas y caminos Sí/No) más los *nombres* de los correos electrónicos y segmentos que utiliza cada paso. No incluye los diseños de los correos electrónicos ni ningún dato de suscriptores.
- **Importar** carga un archivo `.journey.json` en el trayecto actual, reemplazando lo que hay en el lienzo.

Esto es útil para respaldar un flujo del que esté orgulloso, entregar una serie de bienvenida probada a otra tienda Spwig, o reconstruir un trayecto después de clonar su tienda a una instalación nueva.


Al igual que con las plantillas, Spwig vuelve a enlazar correos electrónicos y segmentos por nombre donde exista una coincidencia en la tienda de destino, y marca cualquier cosa que no pueda coincidir para que puedas completar la configuración.

## Activando tu recorrido

Cuando el flujo esté listo, use el control de estado en la esquina superior derecha del constructor. Una pestaña muestra el estado actual del recorrido: **Borrador**, **Activo** o **Pausado** junto con un botón de **Activar**.

Hacer clic en **Activar** **verifica primero el flujo**. Si algo impediría que funcione, la activación se bloquea y una cinta muestra los problemas: por ejemplo, un paso de **Enviar correo electrónico** sin ningún correo electrónico seleccionado, un **Rama** sin segmento o sin camino Sí/No, un correo electrónico o segmento que desde entonces ha sido eliminado, o un bucle que se ejecutaría eternamente. Cada problema es clickeable: al seleccionarlo, salta al paso correspondiente, el cual se encuentra con un recuadro rojo hasta que lo corrija. Las alertas (por ejemplo, un paso inalcanzable o un **Esperar** sin un retraso definido) también se listan, pero no bloquean la activación.

![Activación bloqueada, con el problema listado en una cinta y el paso ofensivo resaltado en rojo](/static/core/admin/img/help/journey-builder/journey-builder-activate-blocked.webp)

Una vez que el flujo pasa, la pestaña cambia a **Activo** y el recorrido comienza a inscribir suscriptores cada vez que se active su disparador. El botón se convierte en **Pausar**, que detiene nuevas inscripciones: los suscriptores que ya estén en el recorrido continuarán recibiendo sus pasos restantes. Vea [Recorridos disparados](/help/triggered-journeys) para saber cómo interactúan la inscripción, los períodos de gracia y el estado.

## Viendo quién está en el recorrido

Una vez que el recorrido esté en marcha, cada paso muestra un pequeño **badge de recuento** en su esquina: la cantidad de suscriptores que se encuentran en ese paso en este momento. Es una forma rápida de ver hacia dónde fluyen las personas y hacia dónde se acumulan: un número grande en un paso de **Esperar** es esperado, mientras que una acumulación justo antes de un correo electrónico en particular podría merecer una revisión. Los recuentos se actualizan cada vez que regrese a la pestaña del constructor.

![El lienzo con los recuentos en vivo en los pasos y el botón de Activar en la barra de herramientas](/static/core/admin/img/help/journey-builder/journey-builder-live-counts.webp)

## Consejos

- Diseñe el flujo mientras aún esté en **Borrador** - nadie se inscribe hasta que active el flujo. Activar desde el constructor ejecuta una verificación rápida primero y no permitirá que un flujo defectuoso se active, por lo que no hay riesgo de que un recorrido a medias inscriba a suscriptores.
- Comience desde una **Plantilla** incluso si planea personalizarla en gran medida - es más rápido editar un flujo existente que construir uno desde cero, y demuestra el patrón de rama si aún no lo ha usado antes.
- Después de aplicar una plantilla o importar un archivo, revise el encabezado en busca de una nota sobre pasos sin coincidir y complete cualquier paso de **Enviar correo electrónico** o **Rama** que no pudiera coincidir antes de activar.
- Haga clic en **Ajustar** cada vez que un flujo se vuelva ancho (especialmente las ramas) - es la forma más rápida de ver nuevamente toda la forma después de acercar o alejar.
- Mantenga los nombres de los pasos fáciles de revisar, manteniendo cada paso de **Esperar** inmediatamente antes del correo electrónico que retrasa, en lugar de agrupar varios pasos de espera juntos.
- **Exportar** un recorrido funcional antes de realizar cambios importantes en él - es una forma rápida de mantener una copia de respaldo que pueda volver a importar si no le gusta el resultado.