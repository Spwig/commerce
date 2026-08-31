---
title: Manual de ejecución para la entregabilidad de correo electrónico
---

<!-- screenshots-needed:
- url: /admin/email_system/emailaccount/add/
  filename: wizard-dns-step.webp
  description: Step 4 (DNS Configuration) of the email account setup wizard for the built-in SMTP provider, showing the SPF/DKIM/DMARC validation one-liners and the DNS provider tabs (Cloudflare/GoDaddy/Namecheap/Route 53/Other) with at least one record's "Details" panel expanded so a copyable TXT record is visible.
  save-to: core/static/core/admin/img/help/deliverability/
  viewport: 1440x900
- url: /admin/email_system/emailaccount/{account_id}/change/
  filename: dkim-dns-record.webp
  description: An existing built-in SMTP EmailAccount's change form scrolled to the "DKIM keys configured" panel, showing the DNS TXT record Name/Value and the Copy DNS Record button.
  save-to: core/static/core/admin/img/help/deliverability/
  viewport: 1440x900
- url: /admin/campaigns/dashboard/
  filename: suppressed-addresses-card.webp
  description: The Campaign Studio dashboard's Suppressed addresses stat card, for the "monitor" section of this runbook.
  save-to: core/static/core/admin/img/help/deliverability/
  viewport: 1440x900
-->

Enviar un correo electrónico es fácil. Lograr que llegue a la bandeja de entrada en lugar de la carpeta de spam es el verdadero trabajo, y los proveedores de buzones como Gmail y Yahoo ahora aplican requisitos técnicos estrictos antes de siquiera considerarlo. Este manual de ejecución detalla qué configurar y en qué orden para que las confirmaciones de pedido y las campañas lleguen a donde los clientes pueden verlas.

Nada de lo que se menciona aquí es una tarea de una sola vez. La entregabilidad es un estatus que se construye con el tiempo y se puede perder rápidamente; la lista de verificación al final vale la pena revisarla siempre que algo parezca incorrecto.

## Por qué es importante

Todos los principales proveedores de buzones puntúan el correo entrante según la reputación del remitente antes de decidir si entregarlo, moverlo a la carpeta de spam o rechazarlo por completo. Desde 2024, Gmail y Yahoo formalizaron esto en **requisitos explícitos para remitentes masivos** para cualquiera que envíe un volumen significativo:

- **Autentique su dominio** — registros SPF, DKIM y DMARC válidos.
- **Facilite el desuscribirse** — un mecanismo de baja funcional y de baja fricción en cada correo de marketing.
- **Mantenga bajas las quejas de spam** — los remitentes masivos que superan aproximadamente el 0,3 % de quejas corren el riesgo de que su correo sea rechazado o movido a la carpeta de spam por completo; el objetivo más seguro es estar muy por debajo del 0,1 %.

Si no cumple con estos requisitos, no solo las campañas de marketing se verán afectadas; una reputación de dominio dañada puede arrastrar el correo transaccional (confirmaciones de pedido, restablecimientos de contraseña) al spam también, ya que Gmail y Yahoo cada vez más juzgan la reputación a nivel de dominio de envío, no solo por tipo de mensaje. Los pasos a continuación son la forma de cumplir con los tres requisitos.

## Paso 1: Autentique su dominio de envío

SPF, DKIM y DMARC son registros TXT de DNS que demuestran a los servidores de correo receptores que el correo que afirma ser de su dominio realmente fue enviado por usted. La forma en que los configura depende del modo de envío que use su tienda; los tres se configuran bajo **Configuración de correo electrónico** en la barra lateral de administración (esto abre la lista de cuentas de correo electrónico; consulte [Configuración de correo electrónico](email-configuration) para la guía completa de configuración de cuentas).

| Modo de envío | Cómo funciona la autenticación |
|---|---|
| **SMTP integrado** (el propio servidor de correo de Spwig) | Spwig genera automáticamente un par de claves DKIM para su dominio. Al agregar una cuenta de correo, el **Paso 4** del asistente de configuración muestra el estado de SPF, DKIM y DMARC, junto con el registro exacto que debe agregarse, con opciones de copiar al portapapeles e instrucciones específicas para Cloudflare, GoDaddy, Namecheap y AWS Route 53. El mismo registro DNS de DKIM también se muestra en la propia página de administración de la cuenta, bajo **Claves DKIM configuradas**, si necesita encontrarlo nuevamente. |
| **SMTP genérico** (un proveedor propio como SendGrid, Mailgun, Amazon SES o Google Workspace, conectado mediante credenciales SMTP) | La autenticación ocurre parcialmente en el propio panel de control de ese proveedor. El paso de DNS del asistente de configuración incluye instrucciones con pestañas específicas para Gmail, Outlook, SendGrid, Mailgun y Amazon SES; cada una explica qué configurar en la consola del proveedor (por ejemplo, verificar un dominio de envío en SendGrid) y qué registros DNS resultantes debe agregar en su host DNS. |
| **Pasarela de correo alojada por Spwig** | Disponible en los planes alojados por Spwig como una opción de envío administrada. Firma automáticamente el correo saliente con DKIM y, por defecto, envía desde una dirección en el propio dominio verificado de Spwig, por lo que funciona sin configuración inicial. Si desea enviar desde su propio dominio a través de la pasarela, consulte con su proveedor de alojamiento sobre su verificación; se trata de un servicio administrado, no de un flujo DNS de autoservicio. |

Sea cual sea el modo que utilice, **agregar el registro DNS en sí mismo siempre es un paso externo**: lo realiza en su registrador de dominio o host DNS (Cloudflare, GoDaddy, Namecheap, Route 53 o donde apunten los servidores de nombres de su dominio), no dentro de Spwig. Spwig puede indicarle exactamente qué agregar y validar que esté activo, pero no puede acceder a su registrador para agregarlo por usted.

Hay algunas cosas que vale la pena saber antes de comenzar:

- **Los cambios en DNS no son instantáneos.** La propagación puede tardar desde unos minutos hasta 48 horas. El paso de validación del asistente mostrará un registro como fallido o ausente hasta que se haya propagado realmente; esto es esperado y no es una señal de que algo esté mal.
- **Solo se permite un registro SPF por dominio.** Si ya tiene uno (de Google Workspace, otro correo, etc.), agregue su nuevo remitente al registro existente con `include:` en lugar de crear un segundo registro TXT de SPF; dos registros SPF romperán la autenticación para todos.
- **DMARC requiere que SPF o DKIM ya estén pasando.** Configúrelo al final, una vez que tanto SPF como DKIM estén verificados.

## Paso 2: Usar una identidad de envío real

Una vez que su dominio esté autenticado, asegúrese de que lo que los destinatarios ven realmente lo respalde:

- **Dirección de remitente** — use una dirección en su propio dominio autenticado (`orders@yourstore.com`), nunca una dirección de un proveedor gratuito (`yourstore@gmail.com`). Una dirección de remitente de un proveedor gratuito no puede ser autenticada por sus registros SPF/DKIM/DMARC en absoluto, y los proveedores de bandeja de entrada la tratan como una fuerte señal de spam de una tienda.
- **Nombre de remitente** — use el nombre reconocible de su tienda, no una etiqueta genérica como "Notificaciones" o "No responder".
- **Responder a** — establezca una dirección monitoreada. Una dirección `noreply@` no monitoreada que rebota o descarta silenciosamente las respuestas es en sí misma una señal leve de reputación, y bloquea el único canal que los clientes tienen para decirle que algo salió mal.

Configure los tres bajo **Configuración de correo > (su cuenta) > Configuración del remitente** — consulte [Configuración de correo](email-configuration) para la descripción completa de los campos.

## Paso 3: Calentar antes de escalar

Un dominio o IP sin historial de envío no tiene reputación todavía — buena o mala — y los proveedores de bandeja de entrada son cautelosos con lo desconocido. Enviar un primer mensaje masivo desde un dominio nuevo se ve estadísticamente idéntico a un spammer que inicia una nueva campaña, y puede terminar en la carpeta de correo masivo aunque todas las casillas técnicas estén marcadas.

- Comience con menos.

Envía tus primeras campañas a tu audiencia más comprometida y más propensa a abrir correos, en lugar de a toda tu lista de inmediato — consulta [Audiencias](audiences) para crear un segmento inicial orientado.
- Aumenta el volumen gradualmente durante las primeras semanas en lugar de saltarte directamente a enviar a toda la lista.
- Si estás migrando una lista existente desde otra plataforma, córtale la misma importancia que al primer día para el aspecto de reputación — el historial de envío de tu antigua plataforma no se traslada con el dominio.

## Paso 4: Mantén tu lista limpia

Cada queja o rechazo cuesta reputación, y ambos son en su mayor parte función de quién está en tu lista y cómo llegaron allí:

- **Envía solo a personas que hayan consentido.** Los contactos importados, listas compradas y direcciones extraídas son la forma más rápida de incrementar las quejas de spam y los rechazos permanentes.
- **Usa el registro doble.** El flujo de consentimiento para el marketing de Spwig verifica la dirección de correo electrónico de un suscriptor antes de enviarle correos de marketing — consulta [Preferencias de comunicación](communication-preferences) para ver cómo se configura este proceso.
- **Deja que el supresión automática de Spwig haga su trabajo.** Spwig vigila los rechazos permanentes, las quejas de spam y los rechazos suaves repetidos y deja de enviar a esas direcciones automáticamente, sin necesidad de configuración — consulta [Higiene de lista y supresiones](list-hygiene) para ver exactamente cómo funciona y cuándo (raramente) es necesario anularlo.
- **Poda a los suscriptores inactivos periódicamente** en lugar de enviar a las mismas direcciones no comprometidas indefinidamente — una lista que se va reduciendo y que abre y hace clic es más valiosa para tu reputación que una lista grande que no lo hace.

## Paso 5: Supervisa

Los problemas de entrega aparecen en los números antes de que un cliente te diga que un correo electrónico no llegó.

Abre el [Informe](campaign-reports) de una campaña después de cada envío y observa:

| Métrica | Qué observar | 
|---|---| 
| **Tasa de rechazo** | Una tasa mayoritariamente de rechazo suave es normal; un aumento en la proporción de **rechazo permanente** significa que tu lista tiene direcciones obsoletas o inválidas que se acumulan. | 
| **Quejas de spam** | Debería estar cerca de cero en cada envío. Manténla bien por debajo del umbral de aproximadamente 0.3% que activa la aplicación de reglas para remitentes en masa en Gmail y Yahoo — trata incluso un pequeño aumento como algo que merece investigarse inmediatamente. | 
| **Tasa de apertura / tasa de clic en apertura** | Una caída repentina y no explicada en los envíos a la misma lista (no solo en una campaña) puede ser una señal temprana de que los correos están llegando al spam en lugar de a la bandeja de entrada, incluso antes de que los números de rechazo o quejas cambien. | 

También revisa periódicamente la tarjeta **Direcciones suprimidas** del panel de control de Campaign Studio — un flujo constante es una decadencia normal de la lista, pero un aumento repentino merece investigarse antes de tu próximo envío (consulta [Higiene de lista](list-hygiene)).

Si algo aumenta bruscamente: detén y verifica primero que tus registros DNS sigan siendo válidos (una renovación de dominio caducada o un cambio accidental en los registros DNS puede romper silenciosamente SPF/DKIM), luego revisa qué cambió en el contenido o la audiencia del envío que lo provocó.

## Paso 6: Higiene del contenido

La autenticación y la calidad de la lista te abren la puerta; el contenido aún afecta cómo te tratan una vez que estás allí.

- **Evita patrones que desencadenen spam** en los asuntos — mayúsculas en exceso, puntuación excesiva ("!!!"), y frases como "actúa ahora" o "dinero gratis" aún te perjudican con los filtros de spam, incluso desde un dominio autenticado.
- **No envíes correos solo con imágenes.** Un correo electrónico que es solo una imagen sin texto real es un patrón clásico de spam; mantén una cantidad significativa de contenido de texto real junto a cualquier imagen.
- **Prueba antes de enviar.** Verifica cómo se ve el correo realmente — incluyendo en dispositivos móviles — antes de enviarlo a toda tu lista.
- **El enlace de cancelación de suscripción ya está resuelto.** Spwig agrega automáticamente un enlace de cancelación de suscripción funcional, sin necesidad de iniciar sesión, en el pie de cada correo de marketing — no necesitas agregar uno propio (consulta [Preferencias de comunicación](communication-preferences) para ver exactamente cómo funciona este proceso). No lo borres ni lo ocultes; un enlace de cancelación de suscripción faltante o roto es una violación de políticas con las reglas para remitentes en masa de Gmail y Yahoo, sin importar tus otros números.

## "Mis correos electrónicos van a spam" — lista de verificación para resolver problemas

Revisa estos pasos en orden:

1. **Vuelve a revisar tus registros DNS.** Abre el asistente de configuración de la cuenta en la sección DNS (o el panel DKIM en la página de administración de la cuenta para el SMTP integrado) y confirma que SPF, DKIM y DMARC sigan mostrando que están pasando. Una renovación de dominio, un cambio de proveedor de DNS o un cambio no relacionado en tu archivo de zona puede romper uno de estos de forma silenciosa.
2. **Revisa los números de rebotes y quejas del informe de campaña** para el envío afectado: consulta [Informes de campañas](campaign-reports). Un aumento repentino en cualquiera de estos puntos indica un problema de calidad de lista o contenido, en lugar de un problema de autenticación.
3. **Revisa la lista de supresiones** ([Higiene de listas](list-hygiene)) en busca de un salto repentino: si una gran parte de tu lista ha estado fallando durante mucho tiempo, la entrega al resto también se degrada.
4. **Confirma que tu dirección de remitente esté en tu dominio autenticado**, en lugar de una dirección de proveedor gratuito o un dominio que no coincida con lo que se configuró para SPF/DKIM/DMARC.
5. **Envía un correo de prueba a una dirección de Gmail y a una de Yahoo/Outlook que controlas** y verifica en qué carpeta realmente cae, no solo si llegó.
6. **Si recientemente cambias la cantidad de envíos o el público de forma drástica**, trata esto como un calentamiento nuevo: reduce el volumen y aumenta gradualmente.
7. **Si todo lo anterior está en orden y el problema persiste**, podría tratarse de un control específico del proveedor en lugar de un error en tu configuración: esto puede tardar algún tiempo en resolverse por sí solo una vez que se haya arreglado la causa subyacente (normalmente quejas o rebotes).

## Consejos

- Corrige la autenticación DNS antes que cualquier otra cosa: cualquier otro factor de entrega (contenido, higiene de listas, calentamiento) es menos importante si SPF/DKIM/DMARC no están pasando.
- Trata la validación DNS del asistente de configuración como una comprobación en un momento dado, no como un único paso: vuélvela a ejecutar cada vez que migras a un proveedor de DNS diferente o renovas un dominio a través de un registrador distinto.
- Una lista limpia que abra y haga clic siempre superará a una lista más grande que no lo haga: resiste la tentación de importar una lista antigua y no verificada "por si acaso".
- Vigila tus números en relación con tus envíos anteriores, no con una pauta genérica de la industria: tu historial es la señal más confiable de un problema real.
- Si estás en un plan alojado por Spwig, la firma DKIM y la gestión de reputación del gateway de correo alojado se realizan por ti: tu responsabilidad restante es la calidad de la lista y el contenido, no los DNS.