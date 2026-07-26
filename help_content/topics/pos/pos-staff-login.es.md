---
title: Inicio de sesión del personal de POS y autenticación biométrica
---

Cada persona que atiende clientes en un terminal de POS necesita una cuenta de personal con los permisos adecuados. Este tema explica cómo crear esa cuenta, asignar al miembro del personal a un terminal y luego configurar el inicio de sesión biométrico para que puedan desbloquear el terminal con una huella dactilar, escaneo facial o clave de hardware en lugar de escribir una contraseña cada vez.

Para códigos PIN, límites de descuento y configuraciones de bloqueo de terminal, consulte [Descuentos del personal de POS y seguridad del terminal](pos-staff-discounts).

## Qué necesita un miembro del personal para usar un terminal de POS

Para iniciar sesión en un terminal de POS, una persona necesita:

1. Una **cuenta de personal** — un usuario de Spwig con la bandera **Estado de personal** habilitada.
2. Un **rol que incluya acceso a POS** — los roles controlan lo que puede hacer un miembro del personal dentro del administrador. Se requiere un rol con permisos de POS para acceder al terminal.
3. **Asignación al terminal** — el terminal debe listarlos como un miembro de personal asignado, o deben asignarse a nivel de ubicación de la tienda.

## Crear una cuenta de personal elegible para POS

Navegue a **Personal y cuentas > Miembros del personal** (o vaya a `/admin/accounts/staffmember/`).

1. Haga clic en **+ Agregar miembro del personal**.
2. Rellene el **nombre**, **apellido** y **dirección de correo electrónico** del miembro del personal.
3. Establezca una contraseña temporal y pídale al miembro del personal que la cambie en su primer inicio de sesión.
4. Asegúrese de que **Estado de personal** esté marcado — esto es lo que le permite iniciar sesión en el administrador y en la aplicación de POS.
5. Haga clic en **Guardar**.

> **Nota:** No marque **Estado de superusuario** para cajeros normales o supervisores. El estado de superusuario ignora todas las verificaciones de permisos y debe reservarse para el propietario de la tienda.

### Asignar un rol con acceso a POS

Las cuentas de personal por sí solas no tienen permisos — los roles otorgan capacidades específicas. Después de crear la cuenta, abra el registro del miembro del personal y vaya a la sección **Roles**. Asigne un rol que incluya acceso a POS.

Para una explicación completa de cómo funcionan los roles y qué permisos incluir, consulte [Roles del personal](staff-roles).

<!-- screenshots-needed:
- url: /en/admin/accounts/staffmember/
  filename: staff-user-list.webp
  description: Lista de miembros del personal que muestra un usuario elegible para POS con su distintivo de rol
-->

![Lista de miembros del personal](/static/core/admin/img/help/pos-staff-login/staff-user-list.webp)

## Asignar personal a un terminal

Las configuraciones siguen una cascada: **Predeterminado del sitio → Grupo de tiendas → Ubicación de la tienda → Terminal individual**. Para la mayoría de las tiendas, el lugar correcto para asignar personal es a nivel de terminal.

1. Navegue a **POS > Terminales** (o vaya a `/admin/pos_app/posterminal/`).
2. Abra el terminal que desea configurar.
3. Vaya a la pestaña **Asignación de personal**.
4. En el campo **Personal asignado**, busque y agregue al miembro del personal.
5. Haga clic en **Guardar**.

Los miembros del personal que aparecen en la lista **Personal asignado** de un terminal pueden seleccionar su nombre en la pantalla de inicio de sesión de ese terminal. El personal no asignado a ningún terminal aún puede iniciar sesión escribiendo directamente su correo electrónico.

> **Consejo:** Si su tienda tiene muchos empleados que se rotan entre terminales, asígneles a nivel de ubicación de la tienda (almacén) en lugar de terminal por terminal. Cualquier miembro del personal asignado a la ubicación tiene automáticamente acceso a todos los terminales en esa ubicación.

## Iniciar sesión en el terminal de POS

Cuando un cajero abre la aplicación de POS (`/pos/`) en un terminal, ven una pantalla de selección de personal. El flujo de inicio de sesión funciona de la siguiente manera:

1. El cajero toca o hace clic en su nombre en la lista (o escribe su correo electrónico si no está listado).
2. Introducen su contraseña.
3. Se inician sesión y el terminal se abre para su turno.

Para desbloqueo basado en PIN (después de que el terminal se bloquee durante un turno), consulte [Descuentos del personal de POS y seguridad del terminal](pos-staff-discounts).

## Inicio de sesión biométrico

El inicio de sesión biométrico permite a un cajero tocar un sensor de huella dactilar, mirar una cámara facial o tocar una clave de hardware en lugar de escribir una contraseña. En un terminal ocupado, esto ahorra varios segundos por turno y evita errores durante las horas pico.

Spwig utiliza el estándar del navegador **WebAuthn** para el inicio de sesión biométrico.

Un "credencial WebAuthn" es un par de claves acoplado al dispositivo: la clave privada se almacena en el hardware seguro del dispositivo y nunca sale de él.

La aplicación POS comunica con ese hardware a través del navegador.

### Dispositivos y navegadores que admiten el inicio de sesión biométrico

WebAuthn es compatible con todos los navegadores modernos — Chrome, Edge, Firefox y Safari — en dispositivos que tengan hardware compatible. Configuraciones comunes que funcionan bien:

| Dispositivo | Autenticador |
|--------|---------------|
| iPad (Touch ID) | Huella dactilar a través de Safari o Chrome |
| Tableta Android | Huella dactilar o rostro a través de Chrome |
| Tableta o PC de Windows | Windows Hello (huella dactilar, rostro o PIN) |
| Cualquier dispositivo + clave de seguridad | Clave FIDO2 USB, NFC o Bluetooth (por ejemplo, YubiKey) |
| iPhone (Face ID) | Rostro a través de Safari |

La aplicación POS solo mostrará la opción de inicio de sesión biométrico cuando el navegador haya confirmado que una credencial está registrada para el usuario actual en ese dispositivo.

### Cómo funciona el registro

El registro ocurre en el terminal POS, no en el administrador. El miembro del personal debe completar primero un inicio de sesión normal con contraseña, luego elegir configurar el inicio de sesión biométrico desde dentro de la aplicación POS. El navegador luego le pedirá que verifique su identidad usando el sensor biométrico del dispositivo (o una contraseña de acceso guardada en su cuenta en iOS/macOS/Windows). Una vez confirmado, la credencial se almacena y el inicio de sesión biométrico estará disponible para futuros turnos en ese dispositivo.

Un solo miembro del personal puede registrarse en múltiples dispositivos — por ejemplo, una tableta personal y un registrador compartido — y cada dispositivo almacena su propia credencial.

> **Nota:** La exacta redacción del mensaje de registro ("Registrar biométrico", "Configurar inicio de sesión con huella dactilar", etc.) proviene de la aplicación POS y puede variar según el navegador y el dispositivo.

### Iniciar sesión con biométrico

Una vez registrado, el nombre del cajero en la pantalla de inicio de sesión mostrará un botón de inicio de sesión biométrico (icono de huella dactilar o similar). El cajero:

1. Toca su nombre en la pantalla de inicio de sesión del terminal.
2. Toca **Iniciar sesión con huella dactilar** (o equivalente).
3. Toca el sensor o mira la cámara.
4. El terminal se desbloquea inmediatamente.

Si la verificación biométrica falla (dedo no reconocido, rostro oculto), el cajero recurre a ingresar su contraseña.

### Revocar una credencial

Si un dispositivo se pierde, se roba o un miembro del personal deja, debe eliminar inmediatamente sus credenciales biométricas.

1. Navegue a **Personal y Cuentas > Miembros del Personal**.
2. Abra el registro del miembro del personal.
3. Desplácese hasta la sección **Configuración de POS**.
4. En la fila **Desbloqueo Biométrico**, haga clic en **Eliminar Todo**.
5. Confirme la acción.

Esto elimina todas las credenciales WebAuthn registradas para ese miembro del personal en todos los dispositivos. La próxima vez que intenten usar el inicio de sesión biométrico en cualquier terminal, se les requerirá iniciar sesión con su contraseña en su lugar.

> **Importante:** Eliminar credenciales aquí no impide que el miembro del personal inicie sesión con su contraseña. Para revocar completamente el acceso, también desactive su cuenta de personal o elimínelo de la lista de personal asignada al terminal.

<!-- screenshots-needed:
- url: /en/admin/accounts/staffmember/
  filename: webauthn-credential-list.webp
  description: Formulario de cambio de miembro del personal mostrando la sección de Configuración de POS con recuento de credenciales biométricas y botón Eliminar Todo
-->

## Notas de seguridad

- **Las credenciales están acopladas al hardware.** La clave privada nunca abandona el elemento seguro del dispositivo.

Si una tableta es robada, un atacante no puede extraer la clave biométrica — aún tendría que superar la pantalla de bloqueo del dispositivo antes de que el navegador liberara la clave.
- **Perder un dispositivo no filtra una contraseña.** WebAuthn reemplaza la contraseña para ese dispositivo; la contraseña del miembro del personal es independiente y no se ve afectada.
- **Revocar inmediatamente cuando el personal deje el puesto.** Elimine las credenciales biométricas y desactive la cuenta del miembro del personal en la misma sesión al desvincular a un miembro del personal.
- **La información biométrica en sí nunca se transmite.** La huella dactilar o el escaneo facial se procesa completamente mediante el hardware del dispositivo.

Spwig solo recibe una respuesta de desafío firmada, no ningún dato biométrico.

## Solución de problemas

### El botón "Iniciar sesión con huella dactilar" no se muestra

La opción biométrica solo aparece cuando:
- El miembro del personal tiene una credencial registrada en este dispositivo específico.
- El navegador admite WebAuthn (todos los navegadores modernos lo hacen — actualice si está usando una versión antigua).

Si el botón no aparece, el miembro del personal aún no se ha registrado en este dispositivo. Debería iniciar sesión con su contraseña y configurar el inicio de sesión biométrico a través de la aplicación POS.

### Registro fallido

Razones comunes:
- **Permiso denegado en el navegador.** El navegador solicitó permiso para acceder al autenticador y el miembro del personal lo rechazó. Debería intentarlo de nuevo y tocar **Permitir** cuando se le pida.
- **No se encontró un autenticador compatible.** El dispositivo no tiene un sensor de huella dactilar, una cámara para la cara o una llave de seguridad adjunta. Verifique el hardware del dispositivo.
- **Credencial duplicada.** Es posible que el miembro del personal ya se haya registrado en este dispositivo. Las credenciales existentes se excluyen durante el registro de nuevo para evitar duplicados.

### La biométrica funcionó en un dispositivo pero no en otro

Cada dispositivo almacena su propia credencial. Registrarse en una tableta no funciona automáticamente en una segunda tableta. El miembro del personal debe completar el registro por separado en cada dispositivo que utilizará.

### Claves de paso entre dispositivos

Algunos sistemas operativos (iOS 16+, macOS Ventura+, Windows 11 con una cuenta de Microsoft) pueden sincronizar claves de paso entre dispositivos a través de iCloud Keychain o Windows Hello. Si el miembro del personal se registró usando una clave de paso sincronizada, podría funcionar automáticamente en varios dispositivos. El comportamiento depende del sistema operativo y del navegador, no de Spwig.

## Consejos

- Configure el inicio de sesión biométrico en los registros compartidos antes de que llegue el personal para su turno — el proceso de registro de dos minutos es mucho más suave cuando se realiza sin que los clientes estén esperando.
- Asigne un rol con permisos limitados en el POS a los cajeros y un rol separado para los supervisores. Mantenga sus cuentas distintas de la cuenta del propietario de la tienda.
- Cuando un miembro del personal cambie de dispositivo (nueva tableta, nuevo teléfono), hágale que se registre en el nuevo dispositivo primero, y luego revogue la credencial antigua desde el administrador si el dispositivo ya no se usa.
- Para tiendas con alta rotación de personal, revise periódicamente la lista de **Personal asignado** en cada terminal y elimine a los miembros del personal que ya no trabajan en la ubicación.
- Si utiliza claves de seguridad hardware (YubiKey u otras similares), una clave puede registrarse en múltiples terminales sin realizar ningún cambio en el administrador — simplemente conecte la clave y complete el registro en cada terminal.