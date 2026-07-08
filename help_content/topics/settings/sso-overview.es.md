---
title: Inicio de sesión único (SSO) para administradores
---

El Inicio de sesión único (SSO) permite que su personal inicie sesión en el panel de administración utilizando su proveedor de identidad de la organización en lugar de un nombre de usuario y contraseña separados. Spwig admite cualquier proveedor de identidad que utilice el protocolo OpenID Connect (OIDC), incluyendo Microsoft Entra ID, Google Workspace, Okta, Auth0, Keycloak y otros.

## ¿Qué es el SSO empresarial?

El SSO empresarial es diferente del inicio de sesión social (iniciar sesión con una cuenta personal de Google o Facebook). Con el SSO empresarial:

- El personal se autentica a través de su **proveedor de identidad de la organización** — el mismo sistema que usan para el correo electrónico, herramientas internas y otras aplicaciones empresariales
- Su equipo de TI controla el acceso centralmente — cuando alguien deja la organización, deshabilitar su cuenta en el proveedor de identidad revoca inmediatamente su acceso a Spwig
- La autenticación multifactor (MFA) se aplica mediante el proveedor de identidad, lo que le brinda una política de seguridad consistente en todas las aplicaciones
- El personal no necesita recordar una contraseña separada para Spwig

## ¿Cómo funciona?

Cuando el SSO está habilitado, la página de inicio de sesión de administrador muestra un botón **Iniciar sesión con [Proveedor]**. El flujo de autenticación funciona de esta manera:

1. El miembro del personal hace clic en el botón de SSO en la página de inicio de sesión de Spwig
2. Se les redirige a la página de inicio de sesión del proveedor de identidad (por ejemplo, inicio de sesión de Microsoft)
3. Se autentican con el proveedor de identidad (incluyendo cualquier MFA que requiera el proveedor)
4. El proveedor de identidad los redirige de vuelta a Spwig con un código de autorización seguro
5. Spwig intercambia el código por la información del usuario y crea una sesión
6. El miembro del personal llega al panel de administración, completamente autenticado

Esto utiliza el protocolo **OpenID Connect (OIDC)** estándar de la industria, que es compatible con casi todos los proveedores de identidad empresarial.

## Habilitar SSO

El SSO se configura en dos lugares:

1. **Configuración del sitio > pestaña de Seguridad** — Habilitar o deshabilitar SSO y controlar la visibilidad del inicio de sesión con contraseña
2. **Configuración del proveedor de SSO** — Ingresar los detalles de OIDC de su proveedor de identidad

### Paso 1: Configurar su proveedor de identidad

Antes de habilitar el SSO en Spwig, debe registrar a Spwig como una aplicación en su proveedor de identidad. Consulte las guías específicas del proveedor:

- **Microsoft Entra ID** — consulte la guía de configuración de Microsoft Entra ID
- **Google Workspace** — consulte la guía de configuración de Google Workspace
- **Okta** — consulte la guía de configuración de Okta
- **Otros proveedores** — cualquier proveedor compatible con OIDC funciona. Registre una aplicación web con la URL de redirección `https://your-store.com/oidc/callback/` y consulte la documentación de su proveedor para la URL de descubrimiento de OIDC, el ID de cliente y el secreto de cliente.

### Paso 2: Configurar el proveedor de SSO en Spwig

Navegue hasta la página **Configuración del proveedor de SSO** (enlazada desde la pestaña de Seguridad o accesible en **SSO empresarial > Configuración del proveedor de SSO** en el menú lateral de administrador). Ingrese:

1. **Nombre del proveedor** — mostrado en el botón de inicio de sesión (por ejemplo, "Microsoft Entra ID")
2. **URL de descubrimiento de OIDC** — la URL `.well-known/openid-configuration` de su proveedor. Haga clic en **Descubrimiento automático** para completar automáticamente los campos de punto final.
3. **ID de cliente** y **Secreto de cliente** — del registro de la aplicación de su proveedor de identidad

El secreto de cliente se almacena encriptado y nunca se muestra después de guardar.

### Paso 3: Habilitar SSO en la configuración del sitio

Navegue hasta **Configuración del sitio > pestaña de Seguridad** y marque **Habilitar SSO para el inicio de sesión de administrador**. El botón de SSO aparecerá inmediatamente en la página de inicio de sesión de administrador.

## Configuración de SSO

| Configuración | Descripción |
|---------|-------------|
| **Habilitar SSO para el inicio de sesión de administrador** | Muestra el botón de SSO en la página de inicio de sesión de administrador. No afecta el inicio de sesión con contraseña a menos que también lo deshabilite. |
| **Permitir inicio de sesión con contraseña en la página de administrador** | Cuando está deshabilitado, el formulario de contraseña se oculta detrás de un botón de alternancia. El personal ve solo el botón de SSO de forma predeterminada. El formulario de contraseña aún puede accederse haciendo clic en "Iniciar sesión con cuenta local" o agregando `?password=1` a la URL de inicio de sesión. |

### Comportamiento de la página de inicio de sesión


| SSO habilitado | Inicio de sesión con contraseña | Resultado |
|-------------|---------------|--------|
| Apagado | Encendido | Página de inicio de sesión estándar con solo un formulario de nombre de usuario/contraseña |
| Encendido | Encendido | Botón SSO en la parte superior, divisor "o", luego formulario de contraseña debajo |
| Encendido | Apagado | Solo el botón SSO. El formulario de contraseña está detrás de un interruptor "Iniciar sesión con cuenta local" |
| Apagado | Apagado | No es posible — el inicio de sesión con contraseña se reactiva automáticamente si SSO está deshabilitado o no está configurado |

## Asignación de usuarios

Cuando un miembro del personal inicia sesión mediante SSO, Spwig lo asigna a una cuenta de usuario existente mediante **dirección de correo electrónico** (sin distinguir mayúsculas y minúsculas). El correo electrónico de las afirmaciones del proveedor de identidad debe coincidir con el correo electrónico de la cuenta de Spwig del miembro del personal.

Si no se encuentra un usuario coincidente:

- **Crear usuarios automáticamente deshabilitado** (por defecto) — el inicio de sesión se deniega. Debe crear primero la cuenta del personal en Spwig con una dirección de correo electrónico coincidente.
- **Crear usuarios automáticamente habilitado** — se crea automáticamente una nueva cuenta de usuario con el nombre y correo electrónico de las afirmaciones del proveedor de identidad.

La configuración **Restringir a personal** (habilitada por defecto) agrega una verificación adicional: incluso si existe una cuenta de usuario, el inicio de sesión se deniega a menos que el usuario tenga el estatus de personal. Esto evita que las cuentas no de personal accedan al panel de administración mediante SSO.

## Mapeo de roles

Si su proveedor de identidad envía información de membresía de grupo en las afirmaciones OIDC, Spwig puede establecer automáticamente el estatus de personal y superusuario según la membresía de grupo.

Para configurar el mapeo de roles:

1. En la Configuración del proveedor de SSO, establezca el campo **Afirmación de grupos** en el nombre de la afirmación que su proveedor utiliza (por defecto: `groups`)
2. En **Grupos de personal**, ingrese nombres o identificadores de grupo separados por comas. Los usuarios en cualquiera de estos grupos se otorgan el estatus de personal.
3. En **Grupos de superusuario**, ingrese nombres o identificadores de grupo separados por comas. Los usuarios en cualquiera de estos grupos se otorgan el estatus de superusuario.

El mapeo de roles se evalúa cada vez que un usuario inicia sesión mediante SSO. Si un usuario se elimina de un grupo en el proveedor de identidad, su estatus de personal o superusuario se actualiza en su próxima sesión de inicio de sesión mediante SSO.

**Importante:** Microsoft Entra ID envía por defecto los **identificadores de objeto** (UUID) de los grupos, no los nombres de los grupos. Copie el identificador de objeto desde el portal de Azure al configurar el mapeo de roles. Otros proveedores como Okta suelen enviar nombres de grupo.

## Mapeo de afirmaciones

Spwig lee la información del usuario desde afirmaciones OIDC estándar. Los valores predeterminados funcionan con la mayoría de los proveedores, pero puede personalizar los nombres de los campos de afirmación en la Configuración del proveedor de SSO:

| Configuración | Valor predeterminado | Descripción |
|---------|---------|-------------|
| **Afirmación de correo electrónico** | `email` | La afirmación que contiene la dirección de correo electrónico del usuario |
| **Afirmación de nombre de pila** | `given_name` | La afirmación que contiene el nombre de pila del usuario |
| **Afirmación de apellido** | `family_name` | La afirmación que contiene el apellido del usuario |
| **Afirmación de grupos** | `groups` | La afirmación que contiene las membresías de grupo (deje en blanco para deshabilitar el mapeo de roles) |

## Comportamiento de MFA

Cuando un miembro del personal inicia sesión mediante SSO, la requisición de autenticación de dos factores (2FA) integrada de Spwig se omite automáticamente. Esto se debe a que el proveedor de identidad es responsable de hacer cumplir el MFA como parte del flujo de inicio de sesión de SSO.

Si su organización requiere MFA, configurelo en las políticas de acceso condicional del proveedor de identidad en lugar de en la configuración de 2FA de Spwig. Esto le brinda un manejo centralizado de MFA en todas sus aplicaciones.

## Acceso de recuperación

Si su proveedor de identidad experimenta un corte de servicio o una configuración incorrecta, aún puede acceder al formulario de inicio de sesión de administración:

- **Haga clic en el interruptor** — Si el inicio de sesión con contraseña está deshabilitado, haga clic en "Iniciar sesión con cuenta local" en la página de inicio de sesión para mostrar el formulario de contraseña
- **Parámetro de URL** — Agregue `?password=1` a la URL de inicio de sesión de administración (por ejemplo, `https://your-store.com/en/admin/login/?password=1`) para mostrar directamente el formulario de contraseña
- **El inicio de sesión con contraseña siempre está disponible** — Incluso cuando esté oculto en la interfaz de usuario, el backend de autenticación con contraseña sigue activo. Solo la visibilidad del formulario se ve afectada.

Spwig también evita que deshabilites el inicio de sesión con contraseña a menos que SSO esté habilitado y configurado correctamente — no puedes bloquearte accidentalmente a ti mismo.

## Proveedores compatibles

Spwig funciona con cualquier proveedor de identidad que admita el protocolo OpenID Connect (OIDC). Están disponibles guías de configuración detalladas para:

- **Microsoft Entra ID** (anteriormente Azure Active Directory)
- **Google Workspace** (Google Cloud Identity)
- **Okta**

Para otros proveedores compatibles con OIDC (Auth0, Keycloak, OneLogin, Ping Identity, JumpCloud, etc.), los pasos de configuración de Spwig son los mismos — necesitas la URL de descubrimiento OIDC del proveedor, el ID de cliente y el secreto del cliente. Consulta la documentación de tu proveedor sobre cómo registrar una aplicación web y obtener estas credenciales. La URI de redirección que debes usar siempre es `https://your-store.com/oidc/callback/`.

## Consejos

- **Comienza con el inicio de sesión con contraseña habilitado** — Habilita SSO junto con el inicio de sesión con contraseña. Una vez que hayas confirmado que SSO funciona para tu equipo, puedes deshabilitar opcionalmente el inicio de sesión con contraseña.
- **Prueba en una ventana incógnita** — Usa una ventana del navegador privada/incógnita para probar SSO sin verse afectado por tu sesión actual de administrador.
- **Crea cuentas de personal primero** — A menos que habilites la creación automática de usuarios, los miembros del personal necesitan tener una cuenta existente en Spwig con una dirección de correo electrónico coincidente antes de poder iniciar sesión mediante SSO.
- **Usa el botón de descubrimiento automático** — Ingresa la URL de descubrimiento OIDC de tu proveedor y haz clic en Auto-Discover para completar automáticamente todos los campos de punto final. Esto es más rápido y menos propenso a errores que ingresar los puntos finales manualmente.
- **Mantén una cuenta de administrador local** — Siempre mantén al menos una cuenta de administrador local con contraseña como opción de recuperación en caso de problemas con el proveedor de identidad.
- **Supervisa la expiración del secreto del cliente** — Algunos proveedores (notablemente Microsoft Entra ID) emiten secretos de cliente con fechas de vencimiento. Establece un recordatorio en el calendario para rotar el secreto antes de que expire.