---
title: Configuración de OAuth y inicio de sesión social
---

OAuth y el inicio de sesión social permiten a los clientes iniciar sesión en su tienda usando sus cuentas existentes de Google, Apple o Microsoft — no es necesario crear y recordar otro nombre de usuario y contraseña.

![Configuración de OAuth](/static/core/admin/img/help/oauth-social-login/oauth-settings.webp)

## ¿Qué es OAuth / Inicio de sesión social?

OAuth es un estándar de autenticación seguro que permite a los clientes iniciar sesión usando credenciales de proveedores de confianza como Google, Apple o Microsoft.

### Beneficios

- **Checkout más rápido** — Los clientes omiten el formulario de registro e inician sesión con un solo clic
- **Menos fricción** — No se requiere crear contraseñas, correos de verificación o flujos de recuperación de contraseña
- **Mejor conversión** — Estudios muestran que el inicio de sesión social puede aumentar las tasas de conversión en un 20-40%
- **Mayor seguridad** — Las credenciales nunca pasan por su tienda; la autenticación es manejada por el proveedor
- **Confianza del cliente** — Los clientes confían en proveedores establecidos con sus credenciales de inicio de sesión

### ¿Cómo funciona?

1. El cliente hace clic en "Iniciar sesión con Google" (o Apple/Microsoft) en su página de inicio de sesión
2. Se redirige a la página de inicio de sesión segura del proveedor
3. El cliente se autentica con sus credenciales del proveedor
4. El proveedor envía información de identidad verificada de vuelta a su tienda
5. El cliente inicia sesión automáticamente

En el primer inicio de sesión, se crea automáticamente una nueva cuenta de cliente usando su correo electrónico e información de perfil del proveedor.

## Proveedores admitidos

Spwig admite tres principales proveedores de OAuth:

| Proveedor | Caso de uso | Requisitos de credenciales |
|----------|----------|------------------------|
| **Google** | Más popular, más fácil de configurar | ID de cliente, secreto de cliente |
| **Apple** | Requerido para aplicaciones iOS, centrado en privacidad | ID de cliente, ID de equipo, ID de clave, clave privada |
| **Microsoft** | Clientes empresariales, usuarios de Office 365 | ID de cliente, secreto de cliente, ID de inquilino |

Puedes habilitar uno, dos o los tres proveedores. Cada uno funciona de forma independiente.

## Configuración de OAuth de Google

El OAuth de Google es la opción más popular y la más fácil de configurar.

### Requisitos previos

- Una cuenta de Google
- Acceso al Google Cloud Console

### Configuración paso a paso

1. **Navegue a la configuración de OAuth**
   - Vaya a **Configuración > Configuración de la tienda** en su panel de administración
   - Desplácese hasta la sección **Proveedores de OAuth**
   - Haga clic en **Configurar Google**

2. **Crear un proyecto de Google Cloud**
   - Visite [Google Cloud Console](https://console.cloud.google.com/)
   - Haga clic en **Crear proyecto**
   - Ingrese un nombre de proyecto (por ejemplo, "Mi OAuth de tienda")
   - Haga clic en **Crear**

3. **Habilitar la API de Google+**
   - En el menú de la izquierda, vaya a **APIs y servicios > Biblioteca**
   - Busque "API de Google+"
   - Haga clic en **Habilitar**

4. **Crear credenciales de OAuth**
   - Vaya a **APIs y servicios > Credenciales**
   - Haga clic en **Crear credenciales > ID de cliente OAuth**
   - Seleccione tipo de aplicación: **Aplicación web**
   - Ingrese un nombre (por ejemplo, "Inicio de sesión de tienda")

5. **Configurar URI de redirección**
   - Bajo **URI de redirección autorizados**, agregue:
     ```
     https://yourdomain.com/accounts/google/login/callback/
     ```
   - Reemplace `yourdomain.com` con su dominio real
   - Haga clic en **Crear**

6. **Copiar credenciales**
   - Copie el **ID de cliente** y **Secreto de cliente** del cuadro de diálogo

7. **Ingresar credenciales en Spwig**
   - Vuelva a la configuración de OAuth de su administrador de Spwig
   - Pegue el ID de cliente y el secreto de cliente
   - Haga clic en **Guardar**
   - Active el interruptor **Habilitar OAuth de Google** para activar

### Pruebas

- Visite la página de inicio de sesión de su tienda
- Busque el botón "Iniciar sesión con Google"
- Haga clic en él y autentíquese con su cuenta de Google
- Debería iniciar sesión y redirigirse a su panel de control de cliente

## Configuración de OAuth de Apple

El OAuth de Apple es más complejo que el de Google debido a su sistema de autenticación basado en claves.

### Requisitos previos

- Una cuenta de desarrollador de Apple (requiere membresía de pago)
- Acceso al portal de desarrollador de Apple

### Configuración paso a paso

1. **Navegar a la configuración de OAuth**
   - Vaya a **Configuración > Configuración de la tienda > Proveedores de OAuth**
   - Haga clic en **Configurar Apple**

2. **Crear un ID de servicio**
   - Inicie sesión en [Apple Developer](https://developer.apple.com/account/)
   - Vaya a **Certificados, Identificadores y Perfiles**
   - Haga clic en **Identificadores** y luego en el botón **+**
   - Seleccione **IDs de servicio** y haga clic en **Continuar**
   - Ingrese una descripción (por ejemplo, "Inicio de sesión de tienda")
   - Ingrese un identificador (por ejemplo, `com.yourstore.login`)
   - Haga clic en **Continuar** y luego en **Registrar**

3. **Configurar el ID de servicio**
   - Haga clic en su nuevo ID de servicio creado
   - Marque **Iniciar sesión con Apple**
   - Haga clic en **Configurar**
   - Agregue su dominio y URL de retorno:
     - **Dominios**: `yourdomain.com`
     - **URLs de retorno**: `https://yourdomain.com/accounts/apple/login/callback/`
   - Haga clic en **Guardar** y luego en **Continuar** y **Guardar** nuevamente

4. **Crear una clave**
   - En el menú de la izquierda, haga clic en **Claves** y luego en el botón **+**
   - Ingrese un nombre de clave (por ejemplo, "Clave de OAuth de tienda")
   - Marque **Iniciar sesión con Apple**
   - Haga clic en **Configurar** y seleccione su ID de aplicación principal
   - Haga clic en **Guardar**, luego en **Continuar** y **Registrar**
   - **Descargue el archivo de clave** (.p8) — no podrá descargarlo nuevamente

5. **Reunir la información requerida**
   Necesita:
   - **ID de cliente** (ID de servicio): El identificador que creó (por ejemplo, `com.yourstore.login`)
   - **ID de equipo**: Encontrado en la parte superior derecha del portal de desarrollador de Apple
   - **ID de clave**: Mostrado cuando creó la clave
   - **Clave privada**: El contenido del archivo .p8 que descargó

6. **Ingresar credenciales en Spwig**
   - Vuelva a la configuración de OAuth de Spwig
   - Pegue el ID de cliente, ID de equipo y ID de clave
   - Abra el archivo .p8 en un editor de texto y copie su contenido
   - Pegue toda la clave (incluyendo encabezados) en el campo de clave privada
   - Haga clic en **Guardar**
   - Active el interruptor **Habilitar OAuth de Apple** para activar

### Pruebas

- Visite la página de inicio de sesión de su tienda en un dispositivo con una cuenta de Apple ID
- Haga clic en "Iniciar sesión con Apple"
- Autentíquese con su cuenta de Apple ID
- Debería iniciar sesión con éxito

## Configuración de OAuth de Microsoft

El OAuth de Microsoft es ideal para tiendas que se dirigen a clientes empresariales que usan Office 365 o Azure AD.

### Requisitos previos

- Una cuenta de Microsoft
- Acceso al portal de Azure

### Configuración paso a paso

1. **Navegar a la configuración de OAuth**
   - Vaya a **Configuración > Configuración de la tienda > Proveedores de OAuth**
   - Haga clic en **Configurar Microsoft**

2. **Registrar una aplicación en Azure**
   - Visite [Azure Portal](https://portal.azure.com/)
   - Vaya a **Azure Active Directory > Registros de aplicaciones**
   - Haga clic en **Nuevo registro**
   - Ingrese un nombre (por ejemplo, "OAuth de tienda")
   - Seleccione **Cuentas en cualquier directorio organizacional y cuentas personales de Microsoft**
   - Bajo **URI de redirección**, seleccione **Web** y ingrese:
     ```
     https://yourdomain.com/accounts/microsoft/login/callback/
     ```
   - Haga clic en **Registrar**

3. **Copiar el ID de la aplicación**
   - En la página de vista general de la aplicación, copie el **ID de la aplicación (cliente)**

4. **Crear un secreto de cliente**
   - En el menú de la izquierda, haga clic en **Certificados y secretos**
   - Haga clic en **Nuevo secreto de cliente**
   - Ingrese una descripción (por ejemplo, "Secreto de OAuth")
   - Seleccione un período de vencimiento (recomendado: 24 meses)
   - Haga clic en **Agregar**
   - **Copie el valor del secreto inmediatamente** — no se mostrará de nuevo

5. **Ingresar credenciales en Spwig**
   - Vuelva a la configuración de OAuth de Spwig
   - Pegue el ID de la aplicación (cliente) como ID de cliente
   - Pegue el valor del secreto como secreto de cliente
   - Opcionalmente ingrese un ID de inquilino (para aplicaciones de un solo inquilino; deje en blanco para aplicaciones de múltiples inquilinos)
   - Haga clic en **Guardar**
   - Active el interruptor **Habilitar OAuth de Microsoft** para activar

### Pruebas

- Visite la página de inicio de sesión de su tienda
- Haga clic en "Iniciar sesión con Microsoft"
- Autentíquese con su cuenta de Microsoft
- Debería iniciar sesión con éxito

## Administración de conexiones OAuth

### Vista del cliente

Los clientes pueden ver y administrar sus proveedores OAuth conectados desde su panel de control de cuenta:

- Navegue a **Mi cuenta > Cuentas conectadas**
- Ve los proveedores vinculados (Google, Apple, Microsoft)
- Desconecte un proveedor haciendo clic en **Desconectar**
- Reconecte iniciando sesión nuevamente con ese proveedor

### Múltiples proveedores

Una sola cuenta de cliente puede estar vinculada a múltiples proveedores OAuth. Por ejemplo, un cliente puede conectar tanto Google como Apple a la misma cuenta.

Si un cliente intenta iniciar sesión con un proveedor OAuth diferente usando la misma dirección de correo electrónico, Spwig vincula automáticamente a su cuenta existente.

### Administración por parte del administrador

Como administrador, puede ver las conexiones OAuth de los clientes:

- Vaya a **Clientes > Clientes**
- Abra un registro de cliente
- Desplácese hasta la sección **Cuentas conectadas**
- Ve los proveedores vinculados y cuándo se conectaron

No puede desconectar proveedores en nombre de los clientes — deben hacerlo ellos mismos por razones de seguridad.

## Solución de problemas

### Mismatch de URI de redirección

**Error**: "Mismatch de URI de redirección" o "redirect_uri inválido"

**Solución**:
- Asegúrese de que la URI de redirección en la configuración de su proveedor coincida exactamente con la de Spwig
- Verifique si hay barras inclinadas al final — deben coincidir
- Verifique que esté usando `https://` (no `http://`)
- Limpie la caché del navegador y vuelva a intentarlo

### Credenciales inválidas

**Error**: "ID de cliente inválido" o "Autenticación fallida"

**Solución**:
- Verifique que haya copiado correctamente el ID de cliente y el secreto de cliente
- Asegúrese de que no haya espacios adicionales o saltos de línea
- Verifique que las credenciales provengan del proyecto/aplicación correcto
- Para Apple, asegúrese de que la clave privada incluya el contenido completo del archivo .p8

### API del proveedor no habilitada

**Error**: "API no habilitada" o "Acceso no configurado"

**Solución**:
- Para Google: Asegúrese de que haya habilitado la API de Google+ en su proyecto de Google Cloud
- Para Microsoft: Verifique que su registro de aplicación esté aprobado y activo
- Para Apple: Verifique que "Iniciar sesión con Apple" esté habilitado para su ID de servicio

### Requerido SSL

**Error**: "OAuth requiere HTTPS" o "URI de redirección insegura"

**Solución**:
- Los proveedores de OAuth requieren SSL/TLS (HTTPS) para la seguridad
- Asegúrese de que su tienda tenga un certificado SSL válido instalado
- Actualice sus URI de redirección para usar `https://` en lugar de `http://`
- Si está probando localmente, use un servicio como ngrok para crear un túnel HTTPS

### Botón no aparece

**Problema**: El botón "Iniciar sesión con Google/Apple/Microsoft" no aparece en la página de inicio de sesión

**Solución**:
- Verifique que el proveedor esté habilitado en la configuración de OAuth
- Limpie la caché del navegador y recargue la página
- Verifique que su tema incluya la plantilla de inicio de sesión social
- Revise la consola del navegador para errores de JavaScript

## Consejos y mejores prácticas

### Seguridad

- **Rotar secretos regularmente** — Actualice los secretos de cliente cada 12-24 meses
- **Monitorear intentos de inicio de sesión fallidos** — Vigile patrones de autenticación inusuales
- **Usar credenciales separadas por entorno** — Credenciales diferentes para entornos de pruebas y producción
- **Restringir URI de redirección** — Agregue solo las URI exactas que necesita

### Experiencia del usuario

- **Habilitar los tres proveedores** — Dê a los clientes elección; diferentes demografías prefieren diferentes proveedores
- **Colocar los botones de forma destacada** — Los botones de inicio de sesión social deben estar por encima del formulario de correo electrónico/contraseña
- **Usar branding reconocible** — Mantenga los estilos estándar de los botones de Google/Apple/Microsoft
- **Probar en móvil** — Los flujos de OAuth funcionan de forma diferente en navegadores móviles

### Cumplimiento

- **Política de privacidad** — Divulgue que usa proveedores de OAuth y qué datos recibe
- **Términos de servicio** — Cumpla con los términos del proveedor (Google, Apple, Microsoft cada uno tiene requisitos)
- **Minimización de datos** — Solo solicite la información de perfil que realmente necesite

### Lista de verificación de pruebas

Antes de ir en línea, pruebe:

- [ ] Inicio de sesión con cada proveedor en el escritorio
- [ ] Inicio de sesión con cada proveedor en móvil
- [ ] Inicio de sesión por primera vez (creación de cuenta)
- [ ] Inicios de sesión posteriores (vinculación de cuenta)
- [ ] Inicio de sesión con el mismo correo electrónico en diferentes proveedores
- [ ] Desconectar y reconectar un proveedor
- [ ] El flujo de restablecimiento de contraseña aún funciona para usuarios no OAuth

Recuerde: preserve all markdown formatting, image paths, code blocks, and technical terms exactly as shown in the preservation rules.