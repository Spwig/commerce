---
title: 'Configuración de SSO: Microsoft Entra ID'
---

Esta guía te lleva paso a paso a conectar Spwig con Microsoft Entra ID (anteriormente Azure Active Directory) para el inicio de sesión único de administradores. Una vez configurado, tu personal podrá iniciar sesión en el panel de administración de Spwig usando su cuenta de trabajo de Microsoft.

**Nota:** Microsoft puede actualizar la interfaz del centro de administración de Entra con el tiempo. Estas instrucciones se escribieron basándose en la interfaz como de principios de 2026. Si algunos pasos difieren de lo que ves, consulta la documentación oficial de Microsoft sobre [registro de una aplicación con la plataforma de identidad de Microsoft](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-register-app).

## Requisitos previos

- Una suscripción a Azure con acceso a Microsoft Entra ID
- Rol de **Administrador de aplicaciones** o **Administrador global** en tu inquilino de Entra ID
- Tu URL de tienda de Spwig (ej. `https://your-store.com`)
- Los miembros del personal deben tener direcciones de correo electrónico en Spwig que coincidan con sus cuentas de Microsoft

## Paso 1: Registrar una aplicación

1. Inicia sesión en el [centro de administración de Microsoft Entra](https://entra.microsoft.com)
2. Navega a **Identidad > Aplicaciones > Registros de aplicaciones**
3. Haz clic en **Nuevo registro**
4. Configura el registro:

| Campo | Valor |
|-------|-------|
| **Nombre** | `Spwig Admin SSO` (o cualquier nombre que prefieras) |
| **Tipos de cuenta admitidos** | **Cuentas en este directorio organizacional solo** (Un solo inquilino) |
| **URI de redirección** | Plataforma: **Web**, URI: `https://your-store.com/oidc/callback/` |

5. Haz clic en **Registrar**

**Importante:** El URI de redirección debe coincidir exactamente con `https://your-store.com/oidc/callback/` — incluyendo la barra final. Reemplaza `your-store.com` con tu dominio real de tienda.

## Paso 2: Anotar los IDs de la aplicación

Después del registro, verás la página **Vista general** de la aplicación. Anota estos dos valores — los necesitarás más adelante:

| Valor | Dónde encontrarlo | Para qué sirve |
|-------|-----------------|---------------|
| **Application (client) ID** | Página de vista general, sección superior | Ingresa como **Client ID** en Spwig |
| **Directory (tenant) ID** | Página de vista general, sección superior | Se usa para construir la URL de descubrimiento |

## Paso 3: Crear un secreto de cliente

1. En el registro de la aplicación, navega a **Certificados y secretos**
2. Haz clic en **Nuevo secreto de cliente**
3. Ingresa una descripción (ej. `Spwig SSO`) y elige un período de vencimiento
4. Haz clic en **Agregar**
5. **Copia el Valor inmediatamente** — se muestra solo una vez. Este es el secreto de cliente que ingresarás en Spwig.

**No copies el ID del secreto** — necesitas la **columna Valor**, no la columna ID.

**Establece un recordatorio** para rotar el secreto antes de que expire. Cuando un secreto expire, el SSO dejará de funcionar hasta que crees uno nuevo y lo actualices en Spwig.

## Paso 4: Configurar permisos de API

1. Navega a **Permisos de API**
2. Verifica que **Microsoft Graph > User.Read** (delegado) esté en la lista. Esto se agrega por defecto.
3. Si los permisos `openid`, `email` y `profile` no están en la lista, haz clic en **Agregar un permiso > Microsoft Graph > Permisos delegados** y agrégalos.
4. Haz clic en **Conceder el consentimiento de administrador para [tu organización]** si se te pide.

## Paso 5: Construir la URL de descubrimiento

La URL de descubrimiento de OIDC sigue este formato:

```
https://login.microsoftonline.com/{tenant-id}/v2.0/.well-known/openid-configuration
```

Reemplaza `{tenant-id}` con el **Directory (tenant) ID** del Paso 2.

Ejemplo: si tu ID de inquilino es `a1b2c3d4-e5f6-7890-abcd-ef1234567890`, la URL de descubrimiento es:

```
https://login.microsoftonline.com/a1b2c3d4-e5f6-7890-abcd-ef1234567890/v2.0/.well-known/openid-configuration
```

## Paso 6: Configurar reclamaciones de grupo (opcional)

Si deseas que Spwig asigne automáticamente el estado de personal o superusuario según la membresía de grupo en Entra ID:

1. En el registro de la aplicación, navega a **Configuración de token**
2. Haz clic en **Agregar reclamación de grupo**
3. Selecciona los tipos de grupo que deseas incluir (normalmente **Grupos de seguridad**)
4. Bajo **Personalizar propiedades del token por tipo**, para el **token ID**, selecciona **Group ID**
5. Haz clic en **Agregar**

**Importante:** Entra ID envía **Object IDs** de grupo (UUIDs como `a1b2c3d4-...`), no nombres de visualización de grupo.

Al configurar el mapeo de roles en Spwig, debes usar estos Object IDs.

Para encontrar el Object ID de un grupo:
1. En el centro de administración de Entra, ve a **Identity > Groups > All groups**
2. Haz clic en el grupo
3. Copia el **Object ID** de la página de vista general del grupo

### Límite de grupo

Microsoft Entra ID incluye un máximo de **200 grupos** en el token. Si un usuario pertenece a más de 200 grupos, la reclamación de grupos se reemplaza con un enlace a la API Microsoft Graph. Para organizaciones con muchos grupos, considera crear un grupo de seguridad dedicado para el acceso a Spwig y usar [filtrado de grupos](https://learn.microsoft.com/en-us/entra/identity-platform/optional-claims-reference) para limitar qué grupos se incluyen.

## Paso 7: Configurar en Spwig

1. En la administración de Spwig, navega a **Enterprise SSO > SSO Provider Configuration**
2. Establece **Provider Name** en `Microsoft Entra ID`
3. Pega la URL de descubrimiento del Paso 5 en **OIDC Discovery URL**
4. Haz clic en **Auto-Discover** — esto completa automáticamente todos los campos de punto final
5. Ingresa el **Client ID** del Paso 2
6. Ingresa el **Client Secret** (el Valor) del Paso 3
7. Si configuraste reclamaciones de grupo en el Paso 6:
   - Establece **Groups Claim** en `groups`
   - En **Staff Groups**, ingresa los Object IDs de los grupos cuyos miembros deben ser personal (separados por comas)
   - En **Superuser Groups**, ingresa los Object IDs de los grupos cuyos miembros deben ser superusuarios (separados por comas)
8. Haz clic en **Save**

## Paso 8: Habilitar y probar

1. Navega a **Site Settings > Security**
2. Marca **Enable SSO for admin login**
3. Haz clic en **Save**
4. Abre la página de inicio de sesión de administración en una **ventana privada/incógnita**
5. Deberías ver un botón **Sign in with Microsoft Entra ID**
6. Haz clic en él — deberías ser redirigido a la página de inicio de sesión de Microsoft
7. Inicia sesión con una cuenta de Microsoft cuyo correo coincida con un usuario de personal en Spwig
8. Deberías ser redirigido de vuelta al panel de administración de Spwig

## Problemas comunes

| Problema | Causa | Solución |
|---------|-------|----------|
| **AADSTS50011: La URI de redirección no coincide** | La URI de redirección en Entra no coincide exactamente | Verifica que la URI de redirección sea `https://your-store.com/oidc/callback/` con la barra final. Comprueba si hay un desacuerdo entre HTTP y HTTPS. |
| **AADSTS700016: Aplicación no encontrada** | Client ID incorrecto o inquilino | Verifica el Client ID y asegúrate de que la URL de descubrimiento use el ID de inquilino correcto |
| **Inicio de sesión exitoso en Microsoft pero falla en Spwig** | No hay usuario coincidente en Spwig | Asegúrate de que exista una cuenta de personal en Spwig con la misma dirección de correo que la cuenta de Microsoft. Verifica que el usuario tenga el estado de personal si está habilitada la opción Restrict to Staff. |
| **La reclamación de grupos está vacía** | Las reclamaciones de grupo no están configuradas | Sigue el Paso 6 para agregar una reclamación de grupos a la configuración del token |
| **La reclamación de grupos devuelve una URL en lugar de IDs** | El usuario está en más de 200 grupos | Usa el filtrado de grupos para limitar los grupos en el token, o asigna grupos específicos |
| **SSO deja de funcionar después de unos meses** | El secreto del cliente ha expirado | Crea un nuevo secreto del cliente en Entra y actualízalo en la configuración del proveedor de SSO de Spwig |

## Consejos

- **Usa grupos de seguridad** para el mapeo de roles, no grupos de Microsoft 365 ni listas de distribución.

Los grupos de seguridad están diseñados para el control de acceso y funcionan con mayor fiabilidad con reclamaciones OIDC.
- **Se recomienda un solo inquilino** — seleccionar "Cuentas en este directorio organizacional solo" restringe el SSO a los usuarios de su organización.

Las configuraciones multitenant requieren validación adicional.
- **Establece una expiración prolongada del secreto** — elige 24 meses al crear el secreto del cliente, y establece un recordatorio en el calendario a los 22 meses para rotarlo.
- **Acceso condicional** — puedes crear políticas de acceso condicional en Entra ID que se apliquen específicamente a la inscripción de la aplicación Spwig.

Por ejemplo, requiere MFA, bloquee el inicio de sesión desde ubicaciones no confiables o requiera dispositivos compatibles.
- **Pruebe con una cuenta no administradora** — cree una cuenta de personal de prueba en Spwig para verificar que SSO funcione antes de implementarla en todo su equipo.