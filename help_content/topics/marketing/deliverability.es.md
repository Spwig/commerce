---
title: Manual de ejecución para la entregabilidad de correo electrónico
---

Enviar un correo electrónico es fácil. Lograr que llegue a la bandeja de entrada en lugar de la carpeta de spam es el verdadero trabajo, y los proveedores de buzones como Gmail y Yahoo ahora aplican requisitos técnicos estrictos antes de siquiera considerarlo. Este manual de ejecución detalla qué configurar y en qué orden para que las confirmaciones de pedido y las campañas lleguen a donde los clientes puedan verlas.

Nada de lo que se menciona aquí es una tarea de una sola vez. La entregabilidad es un estatus que se construye con el tiempo y se puede perder rápidamente; la lista de verificación al final vale la pena revisarla cada vez que algo parezca incorrecto.

## Por qué es importante

Todos los principales proveedores de bandeja de entrada puntúan el correo entrante según la reputación del remitente antes de decidir si entregarlo, moverlo a la carpeta de spam o rechazarlo por completo. Desde 2024, Gmail y Yahoo formalizaron esto en **requisitos explícitos para remitentes masivos** para cualquiera que envíe un volumen significativo:

- **Autentique su dominio** — registros SPF, DKIM y DMARC válidos.
- **Facilite el proceso de baja** — una opción de exclusión funcional y de baja fricción en cada correo de marketing.
- **Mantenga bajas las quejas por spam** — los remitentes masivos que superan aproximadamente el 0,3% de quejas corren el riesgo de que su correo sea rechazado o movido directamente a la carpeta de spam; el objetivo más seguro es estar muy por debajo del 0,1%.

Si no cumple con estos requisitos, no solo las campañas de marketing se verán afectadas; una reputación de dominio dañada puede arrastrar también el correo transaccional (confirmaciones de pedido, restablecimientos de contraseña) al spam, ya que Gmail y Yahoo juzgan cada vez más la reputación a nivel de dominio de envío, no solo por tipo de mensaje. Los pasos a continuación son la forma de cumplir con los tres requisitos.

## Paso 1: Autentique su dominio de envío

SPF, DKIM y DMARC son registros TXT de DNS que demuestran a los servidores de correo receptores que el correo que afirma provenir de su dominio realmente fue enviado por usted. La forma en que los configure depende del modo de envío que utilice su tienda; los tres se configuran bajo **Configuración de correo electrónico** en la barra lateral de administración (esto abre la lista de cuentas de correo electrónico; consulte [Configuración de correo electrónico](email-configuration) para la guía completa de configuración de cuentas).

| Modo de envío | Cómo funciona la autenticación |
|---|---|
| **SMTP integrado** (el propio servidor de correo de Spwig) | Spwig genera automáticamente un par de claves DKIM para su dominio. Al agregar una cuenta de correo electrónico, el **Paso 4** del asistente de configuración muestra el estado de SPF, DKIM y DMARC, junto con el registro exacto que debe agregar, con opciones de copiar al portapapeles e instrucciones específicas para Cloudflare, GoDaddy, Namecheap y AWS Route 53. El mismo registro DNS de DKIM también se muestra más tarde en la propia página de administración de la cuenta, bajo **Claves DKIM configuradas**, si necesita encontrarlo de nuevo. |
| **SMTP genérico** (un proveedor propio como SendGrid, Mailgun, Amazon SES o Google Workspace, conectado mediante credenciales SMTP) | La autenticación ocurre parcialmente en el propio panel de ese proveedor. El paso de DNS del asistente de configuración incluye instrucciones con pestañas específicas para Gmail, Outlook, SendGrid, Mailgun y Amazon SES; cada una explica qué configurar en la consola del proveedor (por ejemplo, verificar un dominio de envío en SendGrid) y qué registros DNS resultantes agregar en su host de DNS. |
| **Pasarela de correo alojada por Spwig** | Disponible en los planes alojados por Spwig como una opción de envío administrada. Firma automáticamente el correo saliente con DKIM y envía de forma predeterminada desde una dirección en el propio dominio verificado de Spwig, por lo que funciona sin configuración. Si desea enviar desde su propio dominio a través de la pasarela, hable con su proveedor de alojamiento sobre su verificación; este es un servicio administrado, no un flujo de DNS de autoservicio. |

![Paso 4 del asistente de configuración de la cuenta de correo electrónico, mostrando la validación de SPF/DKIM/DMARC, pestañas de proveedores de DNS y un registro DKIM expandido listo para copiar](/static/core/admin/img/help/deliverability/wizard-dns-step.webp)

![Panel de claves DKIM configuradas de una cuenta de correo SMTP integrada existente, con el registro TXT de DNS y un botón para copiar el registro DNS](/static/core/admin/img/help/deliverability/dkim-dns-record.webp)

Independientemente del modo que utilice, **la adición del registro DNS en sí siempre es un paso externo**: lo realiza en su registrador de dominio o proveedor de DNS (Cloudflare, GoDaddy, Namecheap, Route 53, o donde apunten los servidores de nombres de su dominio), no dentro de Spwig.

Spwig puede indicarle exactamente qué debe agregar y validar que esté activo, pero no puede acceder a su registrador para agregarlo por usted.

Hay algunas cosas que conviene saber antes de comenzar:

- **Los cambios en DNS no son instantáneos.** La propagación puede tardar desde unos pocos minutos hasta 48 horas. El paso de validación del asistente mostrará un registro como fallido o ausente hasta que se haya propagado realmente; esto es esperado y no es una señal de que algo esté mal.
- **Solo se permite un registro SPF por dominio.** Si ya tiene uno (de Google Workspace, otro proveedor de correo, etc.), agregue su nuevo remitente al registro existente con `include:` en lugar de crear un segundo registro TXT de SPF: dos registros SPF romperán la autenticación para todos.
- **DMARC necesita que SPF o DKIM ya estén pasando.** Configúrelo al final, una vez que tanto SPF como DKIM estén verificados.

## Paso 2: Usar una identidad de envío real

Una vez que su dominio esté autenticado, asegúrese de que lo que los destinatarios ven realmente lo respalde:

- **Dirección de remitente** — use una dirección en su propio dominio autenticado (`orders@yourstore.com`), nunca una dirección de un proveedor gratuito (`yourstore@gmail.com`). Una dirección de remitente de un proveedor gratuito no puede ser autenticada por sus registros SPF/DKIM/DMARC en absoluto, y los proveedores de bandeja de entrada la tratan como una fuerte señal de spam proveniente de una tienda.
- **Nombre de remitente** — use el nombre reconocible de su tienda, no una etiqueta genérica como "Notificaciones" o "No responder".
- **Responder a** — configure una dirección supervisada. Una dirección `noreply@` no supervisada que rebota o descarta silenciosamente las respuestas es en sí misma una leve señal de reputación, y bloquea el único canal que los clientes tienen para decirle que algo salió mal.

Configure los tres en **Configuración de correo electrónico > (su cuenta) > Configuración del remitente** — consulte [Configuración de correo electrónico](email-configuration) para la descripción completa de los campos.

## Paso 3: Calentar antes de escalar

Un dominio o IP sin historial de envío no tiene reputación todavía — buena o mala — y los proveedores de bandeja de entrada son cautelosos con lo desconocido. Enviar un primer gran envío desde un dominio nuevo parece estadísticamente idéntico a un spammer que inicia una nueva campaña, y puede terminar en la carpeta de correo masivo aunque se cumplan todos los requisitos técnicos.

- Comience más pequeño. Envíe sus primeras campañas a su audiencia más comprometida y con mayor probabilidad de abrir, en lugar de a su lista completa de una vez — consulte [Audiencias](audiences) para crear un segmento inicial dirigido.
- Aumente el volumen gradualmente durante las primeras semanas en lugar de saltar directamente a envíos a la lista completa.
- Si está migrando una lista existente desde otra plataforma, trátela como el primer día a efectos de reputación también: el historial de envío de su antigua plataforma no se transfiere con el dominio.

## Paso 4: Mantenga su lista limpia

Cada queja o rebote le cuesta reputación, y ambos son en gran parte una función de quién está en su lista y cómo llegó allí:

- **Solo envíe correos a personas que dieron su consentimiento.** Los contactos importados, las listas compradas y las direcciones raspadas son la forma más rápida de aumentar las quejas de spam y los rebotes duros.
- **Use doble confirmación (double opt-in).** El flujo de consentimiento de marketing de Spwig verifica la dirección de correo electrónico de un suscriptor antes de enviarle correo de marketing — consulte [Preferencias de comunicación](communication-preferences) para ver cómo se configura esto.
- **Deje que la supresión automática de Spwig haga su trabajo.** Spwig vigila los rebotes duros, las quejas de spam y los rebotes suaves repetidos y deja de enviar correos a esas direcciones automáticamente, sin necesidad de configuración — consulte [Higiene de listas y supresiones](list-hygiene) para ver exactamente cómo funciona esto y cuándo (raramente) anularlo.
- **Pode a los suscriptores inactivos periódicamente** en lugar de enviar correos a las mismas direcciones desinteresadas indefinidamente: una lista que se reduce pero abre y hace clic vale más para su reputación que una grande que no lo hace.

## Paso 5: Monitorear


Los problemas de entregabilidad aparecen en los números antes de que un cliente alguna vez te diga que un correo electrónico no llegó.

Abre el [Informe](campaign-reports) de una campaña después de cada envío y observa:

| Métrica | Qué vigilar |
|---|---|
| **Tasa de rebote** | Unos rebotes suaves en su mayoría es normal; un aumento en la **tasa de rebote duro** significa que tu lista tiene direcciones obsoletas o inválidas acumulándose. |
| **Quejas de spam** | Debería estar cerca de cero en cada envío. Mantén el número bien por debajo del umbral de aproximadamente 0.3% que activa el cumplimiento de remitentes masivos en Gmail y Yahoo — trata incluso un pequeño pico como algo que merezca investigarse inmediatamente. |
| **Tasa de apertura / tasa de clic en apertura** | Una caída repentina y no explicada en los envíos a la misma lista (no solo en una campaña) puede ser una señal temprana de que el correo está aterrizando en spam en lugar de en la bandeja de entrada, incluso antes de que los números de rebote o quejas cambien. |

También revise periódicamente la tarjeta **Direcciones suprimidas** del panel de control de Campaign Studio — un flujo constante es una decadencia normal de la lista, pero un pico repentino merece investigarse antes de tu próximo envío (consulte [Higiene de listas](list-hygiene)).

![La tarjeta de estadísticas de direcciones suprimidas en el panel de control de Campaign Studio](/static/core/admin/img/help/deliverability/suppressed-addresses-card.webp)

Si algo sube bruscamente: deténgase y verifique primero que sus registros DNS sigan siendo válidos (una renovación de dominio caducada o un cambio accidental en los registros DNS puede romper silenciosamente SPF/DKIM), luego revise qué cambió en el contenido o el público del envío que lo provocó.

## Paso 6: Higiene del contenido

La autenticación y la calidad de la lista te permiten entrar; el contenido aún afecta cómo te tratan una vez que estás allí.

- **Evite patrones que desencadenen spam** en los asuntos — todo en mayúsculas, puntuación excesiva ("!!!"), y frases como "actúa ahora" o "dinero gratis" aún te perjudican con los filtros de spam, incluso desde un dominio autenticado.
- **No envíe correos electrónicos solo con imágenes.** Un correo electrónico que es solo una imagen sin texto real es un patrón clásico de spam; mantenga una cantidad significativa de contenido de texto real junto con cualquier imagen.
- **Vaya a la vista previa antes de enviar.** Verifique cómo se ve el correo electrónico en realidad — incluyendo en dispositivos móviles — antes de enviarlo a toda la lista.
- **El enlace de cancelación de suscripción ya está gestionado.** Spwig agrega automáticamente un enlace de cancelación de suscripción funcional, sin necesidad de iniciar sesión, en el pie de página de cada correo de marketing — no necesita agregar su propio (consulte [Preferencias de comunicación](communication-preferences) para ver exactamente cómo funciona este flujo). No lo elimine ni lo oculte; un enlace de cancelación de suscripción faltante o roto es una violación de políticas con las reglas de remitentes masivos de Gmail y Yahoo, sin importar otros números.

## "Mis correos electrónicos van a spam" — lista de verificación para resolver problemas

Trabaje a través de estos en orden:

1. **Vuelva a revisar sus registros DNS.** Abra la configuración del asistente de configuración de la cuenta (o el panel DKIM en la página de administración de la cuenta para SMTP integrado) y confirme que SPF, DKIM y DMARC aún muestren que pasaron.

Una renovación de dominio, una migración del proveedor de DNS, o un cambio no relacionado en su archivo de zona puede romper silenciosamente uno de estos.
2. **Verifique los números de rebote y quejas del informe de campaña** para el envío afectado (s) — consulte [Informes de campaña](campaign-reports).

Un pico en los puntos indica una cuestión de calidad de la lista o contenido, más que un problema de autenticación.
3. **Verifique la lista de supresiones** ([Higiene de listas](list-hygiene)) en busca de un salto repentino: si un gran número de direcciones de su lista ha estado fallando durante mucho tiempo, la entregabilidad al resto también se verá afectada.
4. **Asegúrese de que la dirección de envío esté en su dominio autenticado**, no en una dirección de proveedor gratuito o en un dominio que no coincida con el que se configuró para SPF/DKIM/DMARC.
5. **Envíe un correo de prueba a una dirección de Gmail y a una de Yahoo/Outlook que usted controle** y verifique en qué carpeta realmente cae, no solo si llegó.
6. **Si recientemente cambió drásticamente el volumen de envío o el público objetivo**, trátelo como un calentamiento nuevo: reduzca el volumen y aumente gradualmente.
7. **Si todo lo anterior está en orden y el problema persiste**, podría tratarse de una limitación específica del proveedor, en lugar de un error en su configuración: esto puede tardar algún tiempo en resolverse por sí solo una vez que se haya resuelto la causa subyacente (normalmente quejas o rechazos).

## Consejos

- Corrija la autenticación DNS antes que cualquier otra cosa: cualquier otro factor de entregabilidad (contenido, higiene de listas, calentamiento) es menos importante si SPF/DKIM/DMARC no pasan.
- Trate la validación de DNS del asistente de configuración como una comprobación en un momento dado, no como un único paso: vuélala a ejecutar cada vez que cambie de proveedor de DNS o renueve un dominio a través de un registrador diferente.
- Una lista limpia que abra y haga clic siempre superará a una lista más grande que no lo haga: resista la tentación de importar una lista antigua y no verificada "por si acaso".
- Vigile sus números en relación con sus envíos anteriores, no con una pauta genérica de la industria: su propio historial es la señal más confiable de un problema real.
- Si está en un plan alojado por Spwig, la firma DKIM y la gestión de reputación del gateway de correo alojado se realizan por usted: su responsabilidad restante es la calidad de la lista y el contenido, no DNS.