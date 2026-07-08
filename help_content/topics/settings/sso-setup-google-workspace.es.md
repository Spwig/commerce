---
title: 'Configuración de SSO: Google Workspace'
---

Esta guía le guiará a través del proceso de conexión de Spwig con Google Workspace para el inicio de sesión único de administradores. Una vez configurado, su personal podrá iniciar sesión en el panel de administración de Spwig usando su cuenta de Google Workspace.

**Nota:** Google puede actualizar la interfaz del Cloud Console con el tiempo. Estas instrucciones se escribieron basándose en la interfaz como de principios de 2026. Si algunos pasos difieren de lo que ve, consulte la documentación oficial de Google sobre [configuración de OAuth 2.0](https://support.google.com/cloud/answer/6158849).

## Requisitos previos

- Una suscripción a Google Workspace (Google Workspace Business, Enterprise o Education)
- Acceso de administrador a la [Google Cloud Console](https://console.cloud.google.com)
- Su URL de tienda de Spwig (por ejemplo, `https://your-store.com`)
- Los miembros del personal deben tener direcciones de correo electrónico en Spwig que coincidan con sus cuentas de Google Workspace

## Paso 1: Crear o seleccionar un proyecto de Google Cloud

1. Vaya a la [Google Cloud Console](https://console.cloud.google.com)
2. Haga clic en el selector de proyectos en la barra superior
3. Haga clic en **Nuevo proyecto** (o seleccione un proyecto existente si lo prefiere)
4. Ingrese un nombre de proyecto (por ejemplo, `Spwig SSO`)
5. Seleccione su organización
6. Haga clic en **Crear**

## Paso 2: Configurar la pantalla de consentimiento de OAuth

1. En el Cloud Console, vaya a **APIs & Services > OAuth consent screen**
2. Seleccione **Internal** como tipo de usuario — esto restringirá el inicio de sesión a usuarios dentro de su organización de Google Workspace
3. Haga clic en **Crear**
4. Rellene los campos obligatorios:

| Campo | Valor |
|-------|-------|
| **Nombre de la aplicación** | `Spwig Admin` (o el nombre de su tienda) |
| **Correo electrónico de soporte del usuario** | Su dirección de correo electrónico de administrador |
| **Dominios autorizados** | `your-store.com` (el dominio de su tienda, sin `https://`) |
| **Correo electrónico de contacto del desarrollador** | Su dirección de correo electrónico de administrador |

5. Haga clic en **Guardar y continuar**
6. En la página **Scopes**, haga clic en **Add or Remove Scopes** y agregue:
   - `openid`
   - `email`
   - `profile`
7. Haga clic en **Guardar y continuar**
8. Revise la resumen y haga clic en **Back to Dashboard**

## Paso 3: Crear credenciales de OAuth

1. Vaya a **APIs & Services > Credentials**
2. Haga clic en **Create Credentials > OAuth client ID**
3. Configure el cliente:

| Campo | Valor |
|-------|-------|
| **Tipo de aplicación** | Aplicación web |
| **Nombre** | `Spwig SSO` |
| **URLs de redirección autorizadas** | `https://your-store.com/oidc/callback/` |

4. Haga clic en **Crear**
5. Un diálogo muestra su **Client ID** y **Client Secret** — copie ambos valores. También puede descargueles como JSON para su seguridad.

**Importante:** La URL de redirección debe coincidir exactamente con `https://your-store.com/oidc/callback/` — incluyendo la barra final y el esquema `https://`. Reemplace `your-store.com` con su dominio real de tienda.

## Paso 4: Obtener la URL de descubrimiento

Google usa una única URL de descubrimiento estándar para todos los inquilinos de Workspace:

```
https://accounts.google.com/.well-known/openid-configuration
```

Esta URL es la misma para cada organización de Google Workspace — no es necesario personalizarla con un inquilino o dominio.

## Paso 5: Configurar en Spwig

1. En el panel de administración de Spwig, vaya a **Enterprise SSO > SSO Provider Configuration**
2. Establezca **Provider Name** en `Google Workspace`
3. Ingrese la URL de descubrimiento: `https://accounts.google.com/.well-known/openid-configuration`
4. Haga clic en **Auto-Discover** — esto rellena automáticamente todos los campos de punto final
5. Ingrese el **Client ID** del Paso 3
6. Ingrese el **Client Secret** del Paso 3
7. Haga clic en **Save**

### Mapeo de reclamaciones

Google usa nombres estándar de reclamaciones OIDC, por lo tanto, la configuración predeterminada de Spwig funciona de inmediato:

| Configuración de Spwig | Reclamación de Google | Valor predeterminado |
|---------------|-------------|---------------|
| Reclamación de correo electrónico | `email` | `email` |
| Reclamación de nombre de pila | `given_name` | `given_name` |
| Reclamación de apellido | `family_name` | `family_name` |

No se necesitan cambios en el mapeo de reclamaciones.

## Paso 6: Habilitar y probar

1.

Navegue a **Site Settings > Security** tab
2.

Marque **Enable SSO for admin login**
3.

Haga clic en **Save**
4.



Abra la página de inicio de sesión de administrador en una **ventana privada/incógnito**
5.

Deberías ver un botón **Iniciar sesión con Google Workspace**
6.

Haz clic en él — deberías ser redirigido a la página de inicio de sesión de Google
7.

Inicia sesión con una cuenta de Google Workspace cuyo correo electrónico coincida con un usuario de personal en Spwig
8.

Deberías ser redirigido de vuelta al panel de administrador de Spwig

## Mapeo de roles basado en grupos

A diferencia de Microsoft Entra ID o Okta, Google no incluye la membresía de grupos en los tokens OIDC estándar de forma predeterminada. Implementar afirmaciones de grupo con Google requiere la API de directorio de Google Workspace y una configuración adicional más allá del OIDC básico.

Para la mayoría de las implementaciones de Google Workspace, recomendamos gestionar el estado de personal y superusuario directamente en Spwig en lugar de hacerlo a través del mapeo automático de roles:

1. Crea cuentas de personal en Spwig con los permisos adecuados
2. Usa el sistema de roles de personal de Spwig para controlar los niveles de acceso
3. El personal inicia sesión mediante SSO, y Spwig usa sus permisos existentes

Si necesitas un mapeo automático de roles basado en grupos, consulta la [documentación de la API de directorio del SDK de administración de Google Workspace](https://developers.google.com/admin-sdk/directory) para configurar afirmaciones personalizadas.

## Problemas comunes

| Problema | Causa | Solución |
|---------|-------|----------|
| **Error 400: redirect_uri_mismatch** | La URI de redirección en Google Cloud no coincide exactamente | Verifica que la URI de redirección sea `https://your-store.com/oidc/callback/` con la barra final. Comprueba HTTP vs HTTPS. |
| **Error 403: access_denied** | El usuario no pertenece a la organización de Google Workspace | Con el tipo de usuario "Interno", solo los usuarios de su organización pueden iniciar sesión. Verifica que la cuenta del usuario forme parte de su dominio de Workspace. |
| **La pantalla de consentimiento de OAuth muestra "Esta app no está verificada"** | Normal para aplicaciones internas | Esta advertencia es esperada para aplicaciones internas y no afecta la funcionalidad. Los usuarios de su organización aún pueden iniciar sesión. |
| **Inicio de sesión exitoso en Google pero falla en Spwig** | No hay usuario coincidente en Spwig | Asegúrate de que exista una cuenta de personal en Spwig con el mismo correo electrónico que la cuenta de Google Workspace. Verifica que "Restringir a personal" esté configurado correctamente. |
| **"Acceso bloqueado: Esta solicitud de la app es inválida"** | Los alcances no están configurados correctamente | Verifica que los alcances `openid`, `email` y `profile` se hayan agregado a la pantalla de consentimiento de OAuth. |

## Consejos

- **Usa el tipo de usuario "Interno"** — esto restringe el inicio de sesión a tu organización de Google Workspace y no requiere el proceso de verificación de aplicaciones de Google.
- **Los secretos del cliente de Google no caducan** — a diferencia de Microsoft Entra ID, los secretos de cliente de OAuth de Google no tienen fecha de caducidad. Sin embargo, puedes rotarlos en cualquier momento desde la página de credenciales.
- **Un proyecto para múltiples aplicaciones** — puedes crear múltiples IDs de cliente OAuth dentro del mismo proyecto de Google Cloud si tienes múltiples instalaciones de Spwig.
- **Prueba con una cuenta no administradora** — crea una cuenta de personal de prueba en Spwig y usa un usuario normal de Google Workspace (no un superadministrador) para verificar que SSO funcione como se espera.