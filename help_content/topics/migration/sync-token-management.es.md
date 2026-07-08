---
title: Gestión de Tokens de Sincronización
---

Los tokens de sincronización son credenciales seguras que permiten que dos instalaciones de Spwig se comuniquen entre sí. Antes de poder sincronizar configuraciones o migrar datos entre tiendas, debes generar un token en la tienda **receptora** y proporcionarlo a la tienda **emisora**.

## Cómo funcionan los tokens de sincronización

Un token de sincronización es una clave de API visible solo una vez que autentica las solicitudes entre dos instalaciones de Spwig. Cuando configuras una conexión, la tienda remota usa este token para demostrar que tiene permiso para leer de o escribir en tu tienda.

- Los tokens se generan en la tienda que será **conectada a** (el objetivo)
- Cada token solo puede verse una vez, inmediatamente después de su generación
- Los tokens pueden revocarse en cualquier momento para cortar inmediatamente el acceso
- Una tienda puede tener múltiples tokens activos para diferentes conexiones

## Generar un token

1. Navega a **Data Migration > Spwig-to-Spwig Sync** en el menú lateral de administración
2. Haz clic en **Manage Tokens** en el panel de sincronización
3. Ingresa un nombre descriptivo para el token (por ejemplo, "Staging Server" o "Production Sync")
4. Haz clic en **Generate Token**
5. **Copia el token inmediatamente** -- no se mostrará de nuevo

> **Importante:** Almacena el token de forma segura. Si lo pierdes, deberás generar uno nuevo.

## Usar un token

Una vez que tengas un token de la tienda objetivo:

1. Ve al panel de **Spwig-to-Spwig Sync** en la tienda que iniciará la conexión
2. Inicia una nueva **Settings Sync** o **Full Migration**
3. En el paso de conexión, ingresa la URL de la tienda objetivo y pega el token
4. Haz clic en **Test Connection** para verificar que funcione
5. La conexión se guardará para uso futuro

## Revocar un token

Si un token se compromete o ya no es necesario:

1. Ve a **Manage Tokens** en el panel de sincronización
2. Encuentra el token que deseas revocar
3. Haz clic en el botón **Revoke**
4. Confirma la revocación

Revocar un token tiene efecto inmediato. Cualquier conexión activa que use ese token dejará de funcionar y deberá reconfigurarse con un nuevo token.

## Buenas prácticas

- **Nombra los tokens de forma descriptiva** para saber a qué conexión pertenece cada token
- **Revoca los tokens no utilizados** para minimizar la exposición de seguridad
- **Genera tokens separados** para cada tienda conectada en lugar de compartir un solo token entre múltiples tiendas
- **Regenera tokens periódicamente** como parte de tu rutina de seguridad, especialmente después de cambios en el personal