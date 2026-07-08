---
title: 'Configuración de SSO: Okta'
---

Esta guía te lleva a través de la conexión de Spwig con Okta para el inicio de sesión único de administradores. Una vez configurado, tu personal puede iniciar sesión en el panel de administración de Spwig usando su cuenta de Okta.

**Nota:** Okta puede actualizar su interfaz de consola de administración con el tiempo. Estas instrucciones se escribieron basándose en la consola de administración de Okta como de principios de 2026. Si algunos pasos difieren de lo que ves, consulta la documentación oficial de Okta sobre [crear una integración de aplicación OIDC](https://developer.okta.com/docs/guides/sign-into-web-app-redirect/main/).

## Requisitos previos

- Una organización de Okta (cualquier nivel — las cuentas gratuitas para desarrolladores funcionan para pruebas)
- Rol de **Super Administrador** o **Administrador de Aplicaciones** en Okta
- Tu URL de tienda de Spwig (por ejemplo, `https://your-store.com`)
- Los miembros del personal deben tener direcciones de correo electrónico en Spwig que coincidan con sus cuentas de Okta

## Paso 1: Crear una aplicación

1. Inicia sesión en la [Consola de administración de Okta](https://your-org-admin.okta.com)
2. Navega a **Aplicaciones > Aplicaciones**
3. Haz clic en **Crear integración de aplicación**
4. Selecciona:

| Campo | Valor |
|-------|-------|
| **Método de inicio de sesión** | OIDC - OpenID Connect |
| **Tipo de aplicación** | Aplicación web |

5. Haz clic en **Siguiente**

## Paso 2: Configurar la aplicación

Rellena la configuración de la aplicación:

| Campo | Valor |
|-------|-------|
| **Nombre de la integración de la aplicación** | `Spwig Admin SSO` (o cualquier nombre que prefieras) |
| **Tipo de concesión** | Código de autorización (debería seleccionarse por defecto) |
| **URI de redirección de inicio de sesión** | `https://your-store.com/oidc/callback/` |
| **URI de redirección de cierre de sesión** | `https://your-store.com/en/admin/login/` |
| **Acceso controlado** | Elige según tus necesidades (ver más abajo) |

Para **Acceso controlado**, elige una de las siguientes:

- **Permitir que todos en tu organización accedan** — todos los usuarios de Okta pueden iniciar sesión (aún puedes controlar el acceso a Spwig con la configuración Restringir a personal)
- **Limitar el acceso a grupos seleccionados** — solo los usuarios en grupos específicos de Okta pueden iniciar sesión
- **Saltar la asignación de grupos por ahora** — asignarás usuarios o grupos manualmente más tarde

Haz clic en **Guardar**.

**Importante:** El URI de redirección de inicio de sesión debe coincidir exactamente con `https://your-store.com/oidc/callback/` — incluyendo la barra final.

## Paso 3: Obtener las credenciales del cliente

Después de guardar, la pestaña **General** de la aplicación muestra tus credenciales:

| Valor | Dónde encontrarlo |
|-------|-----------------|
| **ID de cliente** | Pestaña General, sección Credenciales del cliente |
| **Secreto del cliente** | Pestaña General, sección Credenciales del cliente (haz clic en el icono de ojo para revelarlo) |

Copia ambos valores — los necesitarás para Spwig.

## Paso 4: Construir la URL de descubrimiento

La URL de descubrimiento depende de tu organización de Okta y servidor de autorización:

**Servidor de autorización predeterminado (más común):**
```
https://your-org.okta.com/.well-known/openid-configuration
```

**Servidor de autorización personalizado (si se configuró):**
```
https://your-org.okta.com/oauth2/{authorization-server-id}/.well-known/openid-configuration
```

Reemplaza `your-org.okta.com` con tu dominio real de Okta. Puedes encontrar tu dominio de Okta en la barra de direcciones de la consola de administración o bajo **Configuración > Cuenta**.

**Consejo:** La mayoría de las organizaciones usan el Servidor de Autorización de la Organización (el predeterminado). Solo usa una URL de servidor de autorización personalizado si tu administrador de Okta ha configurado una específicamente.

## Paso 5: Asignar usuarios o grupos

Si elegiste "Saltar la asignación de grupos" en el Paso 2, debes asignar usuarios antes de que puedan iniciar sesión:

1. En la pestaña **Asignaciones** de la aplicación, haz clic en **Asignar**
2. Elige **Asignar a personas** o **Asignar a grupos**
3. Selecciona los usuarios o grupos y haz clic en **Asignar**
4. Haz clic en **Hecho**

Los usuarios que no se asignen a la aplicación verán un error al intentar SSO.

## Paso 6: Configurar reclamaciones de grupo (opcional)

Si deseas que Spwig establezca automáticamente el estado de personal o superusuario basado en la membresía de grupo de Okta:

1.

Navega a **Seguridad > API** en la consola de administración
2.

Selecciona tu **Servidor de autorización** (usa "default" si no has creado uno personalizado, o el Servidor de autorización de la Organización)
3.

Ve a la pestaña **Reclamaciones**
4.

Preserva todo el formato de markdown, rutas de imágenes, bloques de código y términos técnicos.

Haz clic en **Agregar reclamación**
5.

Configura la reclamación:

| Campo | Valor |
|-------|-------|
| **Nombre** | `grupos` |
| **Incluir en tipo de token** | ID Token, Siempre |
| **Tipo de valor** | Grupos |
| **Filtro** | Coincide con regex: `.*` (para incluir todos los grupos) |
| **Incluir en** | Cualquier ámbito (o `openid` si deseas limitarlo) |

6. Haz clic en **Crear**

**Consejo:** A diferencia de Microsoft Entra ID, que envía Object IDs, Okta envía **nombres de grupo** de forma predeterminada. Esto hace que el mapeo de roles sea más intuitivo — puedes usar directamente los nombres de visualización de tus grupos de Okta en los campos Grupos de personal y Grupos de superusuario de Spwig.

### Filtros de grupos

Si tus usuarios pertenecen a muchos grupos de Okta y solo deseas incluir algunos específicos en el token:

- Cambia el filtro de `.*` a una expresión regular más específica, por ejemplo, `^Spwig.*` para incluir solo grupos que comiencen con "Spwig"
- O usa los filtros **Comienza con**, **Igual a** o **Contiene** en lugar de regex

## Paso 7: Configurar en Spwig

1. En el administrador de Spwig, navega a **Enterprise SSO > Configuración del proveedor de SSO**
2. Establece **Nombre del proveedor** en `Okta`
3. Ingresa la URL de descubrimiento del paso 4
4. Haz clic en **Descubrir automáticamente** — esto completa automáticamente todos los campos de punto final
5. Ingresa el **ID de cliente** del paso 3
6. Ingresa el **Secreto de cliente** del paso 3
7. Si configuraste reclamaciones de grupos en el paso 6:
   - Establece **Reclamación de grupos** en `grupos`
   - En **Grupos de personal**, ingresa los nombres de los grupos de Okta cuyos miembros deben ser personal (separados por comas)
   - En **Grupos de superusuario**, ingresa los nombres de los grupos de Okta cuyos miembros deben ser superusuarios (separados por comas)
8. Haz clic en **Guardar**

## Paso 8: Habilitar y probar

1. Navega a **Configuración del sitio > pestaña Seguridad**
2. Marca **Habilitar SSO para inicio de sesión de administrador**
3. Haz clic en **Guardar**
4. Abre la página de inicio de sesión de administrador en una **ventana privada/incógnita**
5. Deberías ver un botón **Iniciar sesión con Okta**
6. Haz clic en él — deberías ser redirigido a la página de inicio de sesión de Okta
7. Inicia sesión con una cuenta de Okta que esté asignada a la aplicación y cuyo correo coincida con un usuario de personal en Spwig
8. Deberías ser redirigido de vuelta al panel de administración de Spwig

## Problemas comunes

| Problema | Causa | Solución |
|---------|-------|----------|
| **La URI de redirección no está permitida** | La URI de redirección no coincide con la configuración de la aplicación | Verifica que la URI de redirección de inicio de sesión sea exactamente `https://your-store.com/oidc/callback/` con la barra final |
| **El usuario no está asignado al cliente de la aplicación** | El usuario no está asignado a la aplicación de Okta | Asigna al usuario o a su grupo a la aplicación en la pestaña Asignaciones |
| **El inicio de sesión tiene éxito en Okta pero falla en Spwig** | No hay usuario coincidente en Spwig | Asegúrate de que exista una cuenta de personal en Spwig con el mismo correo. Verifica la configuración Restringir a personal. |
| **La reclamación de grupos está vacía** | La reclamación de grupos no está configurada en el servidor de autorización | Sigue el paso 6 para agregar una reclamación de grupos. Asegúrate de que estés agregándola al servidor de autorización correcto. |
| **Servidor de autorización incorrecto** | La URL de descubrimiento usa un servidor de autorización diferente al donde se configuró la reclamación de grupos | Verifica que la URL de descubrimiento coincida con el servidor de autorización donde configuraste la reclamación de grupos |
| **"El client_id proporcionado es inválido"** | El ID de cliente no coincide o la aplicación está inactiva | Verifica que el ID de cliente sea correcto y que el estado de la aplicación sea Activo en Okta |

## Consejos

- **Okta envía nombres de grupo, no IDs** — esto hace que el mapeo de roles sea directo.

Ingresa el nombre exacto de visualización del grupo (por ejemplo, `Spwig Admins`) en los campos Grupos de personal o Grupos de superusuario de Spwig.
- **Usa la asignación de grupos para el control de acceso** — asigna grupos específicos de Okta a la aplicación de Spwig en lugar de permitir a todos los usuarios.

# Configuración de SSO con Okta

De esta manera, solo el personal previamente autorizado podrá iniciar sesión.
- **Los secretos del cliente de Okta no caducan por defecto** — pero puedes rotarlos en cualquier momento desde la pestaña General de la aplicación para seguir las mejores prácticas de seguridad.
- **Prueba con una cuenta no administradora** — usa un usuario normal de Okta (no un superadministrador) asignado a la aplicación para verificar que SSO funcione como se espera.
- **MFA en Okta** — configura la política de sesión global de Okta o las políticas de autenticación para requerir MFA.

Esto se aplicará a todas las sesiones de inicio de sesión con SSO en Spwig sin necesidad de configurar MFA por separado en Spwig.