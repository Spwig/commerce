---
title: Copia de seguridad de la base de datos
---

Las copias de seguridad periódicas protegen los datos de tu tienda — pedidos, clientes, productos y configuración — contra fallos de hardware, eliminaciones accidentales y otros eventos inesperados. El sistema de copia de seguridad de Spwig te permite crear copias de seguridad a demanda, establecer horarios automáticos, descargar copias de seguridad localmente, restaurar desde cualquier copia de seguridad guardada y copiar copias de seguridad a destinos de almacenamiento remoto como Amazon S3 o Google Drive.

Navega a **Gestión > Métricas del sistema** y usa los enlaces de la barra de herramientas para acceder a las herramientas de copia de seguridad.

![Panel de sistema con herramientas de copia de seguridad](/static/core/admin/img/help/database-backups/system-dashboard.webp)

## Crear una copia de seguridad manual

Ejecuta una copia de seguridad en cualquier momento antes de realizar cambios importantes — como una importación de productos, una actualización de tema o una actualización de la plataforma.

1. Navega a **Gestión > Métricas del sistema**
2. Haz clic en **Crear copia de seguridad completa** desde la barra de herramientas
3. Ingresa un nombre descriptivo para la copia de seguridad (ej. `before-july-import`)
4. Opcionalmente, agrega una **Descripción** para recordarte por qué se realizó esta copia de seguridad
5. Elige un **Tipo de copia de seguridad**:
   - **Sistema completo** — copia de seguridad de la base de datos y todos los archivos multimedia (recomendado)
   - **Solo base de datos** — copia de seguridad de los datos de la tienda, excluyendo imágenes y archivos cargados
6. Elige **Compresión** (`gzip` es el valor predeterminado y funciona bien para la mayoría de las tiendas)
7. Haz clic en **Crear copia de seguridad**

Spwig crea la copia de seguridad en segundo plano. Un indicador de progreso muestra la etapa actual. Cuando se complete, la copia de seguridad aparecerá en la lista **Copia de seguridad de la base de datos** con un estado **Completado** y su tamaño de archivo.

## Descargar una copia de seguridad

Puedes descargar cualquier copia de seguridad completada para tener una copia local en tu computadora.

1. Navega a **Gestión > Copias de seguridad de la base de datos**
2. Encuentra la copia de seguridad que deseas descargar
3. Haz clic en el botón **Descargar** junto a ella

El archivo de copia de seguridad se descarga como un archivo comprimido. Almacénalo en un lugar seguro — en un dispositivo separado o en almacenamiento en la nube — para que tengas una copia independiente de tu servidor.

## Programar copias de seguridad automáticas

Las copias de seguridad automáticas se ejecutan en segundo plano sin que debas hacer nada, por lo que tus datos están protegidos incluso si olvidas crear copias de seguridad manuales.

1. Navega a **Gestión > Métricas del sistema**
2. Haz clic en **Programa de copia de seguridad**
3. Marca **Habilitar copias de seguridad automáticas**
4. Establece la **Frecuencia**:
   - **Diaria** — se ejecuta una vez al día en el horario que especifiques
   - **Semanal** — se ejecuta una vez por semana en el día que elijas
   - **Mensual** — se ejecuta en un día específico del mes
5. Establece la **Hora** en la que debe ejecutarse la copia de seguridad (hora del servidor, generalmente UTC — 03:00 AM es un buen momento de baja actividad)
6. Elige el **Tipo de copia de seguridad** (Sistema completo o Solo base de datos)
7. Establece **Días de retención** — las copias de seguridad antiguas a este número de días se eliminan automáticamente (valor predeterminado: 30 días)
8. Opcionalmente, marca **Cifrar copia de seguridad** para cifrar el archivo de copia de seguridad en reposo
9. Si tienes destinos de almacenamiento remoto configurados, selecciona los que desees bajo **Destinos remotos** para subir automáticamente las copias de seguridad programadas
10. Haz clic en **Guardar programa**

La marca de tiempo **Próxima ejecución** se actualiza inmediatamente y muestra cuándo ocurrirá la próxima copia de seguridad automática.

## Restaurar desde una copia de seguridad

La restauración reemplaza los datos actuales de tu tienda con el contenido de una copia de seguridad. Úsala para recuperar datos perdidos o para deshacer cambios no deseados.

> **Importante:** La restauración reemplazará todos los datos actuales con los datos de la copia de seguridad. Tu tienda se colocará en modo de mantenimiento durante la restauración. Informa a tu equipo antes de realizar una restauración.

1. Navega a **Gestión > Métricas del sistema**
2. Haz clic en **Restaurar** desde la barra de herramientas
3. La lista de restauración muestra todas las copias de seguridad disponibles con sus fechas y tamaños
4. Haz clic en **Restaurar** junto a la copia de seguridad que desees usar
5. Revisa la pantalla de confirmación — muestra exactamente qué se reemplazará
6. Ingresa la frase de confirmación si se te solicita, luego haz clic en **Ejecutar restauración**

Spwig muestra una barra de progreso mientras la restauración avanza por sus etapas (haciendo una copia de seguridad del estado actual, descargando la copia de seguridad si es remota, restaurando la base de datos, restaurando archivos multimedia). Cuando se complete, la tienda sale automáticamente del modo de mantenimiento.

## Configuración de almacenamiento remoto

El almacenamiento remoto copia automáticamente tus copias de seguridad a un destino externo — Amazon S3, Google Drive, Dropbox o un servidor SFTP. Esto te protege contra fallos a nivel de servidor.

1. Navega a **Management > System Metrics**
2. Haz clic en **Remote Storage**
3. Haz clic en **Add Destination**
4. El asistente de configuración te guía a través de tres pasos:
   - **Paso 1**: Elige tu tipo de almacenamiento (S3, Google Drive, Dropbox o SFTP)
   - **Paso 2**: Ingresa las credenciales para tu proveedor elegido (ver detalles a continuación)
   - **Paso 3**: Nombra el destino y prueba la conexión
5. Después de que la prueba de conexión tenga éxito, haz clic en **Save**

### Amazon S3 (y servicios compatibles con S3)

Necesitarás:
- **Access Key ID** y **Secret Access Key** de tu usuario AWS IAM
- **Bucket Name** — el bucket S3 al que se subirán las copias de seguridad
- **Region** — la región AWS donde se encuentra el bucket (por ejemplo, `us-east-1`)
- Opcionalmente un **Prefix** (ruta de carpeta dentro del bucket, por ejemplo, `spwig-backups/`)

Los servicios compatibles con S3 (Backblaze B2, Wasabi, MinIO, etc.) funcionan de la misma manera — ingresa la URL del punto final personalizado cuando se te pida.

### Google Drive

Haz clic en **Connect with Google** en el paso de credenciales. Spwig abre una ventana de OAuth de Google — inicia sesión y otorga permiso para subir archivos. No hay credenciales que copiar manualmente.

### Dropbox

Haz clic en **Connect with Dropbox** en el paso de credenciales. Inicia sesión en Dropbox y aprueba el acceso. Las copias de seguridad se suben a una carpeta `Apps/Spwig` en tu Dropbox.

### SFTP

Necesitarás:
- **Hostname** de tu servidor SFTP
- **Port** (por defecto: 22)
- **Username** y **Password** (o clave privada SSH)
- **Remote Path** — el directorio en el servidor al que se subirán las copias de seguridad

### Establecer un destino como predeterminado

En la página **Remote Storage**, haz clic en el interruptor junto a cualquier destino para hacerlo el **predeterminado**. El destino predeterminado recibe automáticamente cada copia de seguridad — manual y programada — sin necesidad de seleccionarlo cada vez.

## Consejos

- Realiza una copia de seguridad manual antes de cada cambio significativo: importaciones de productos, ediciones de temas, actualizaciones de la plataforma o campañas de descuentos
- Programa copias de seguridad diarias en un momento de baja actividad (por ejemplo, a las 03:00 AM) para minimizar cualquier impacto en el rendimiento
- Configura al menos un destino de almacenamiento remoto para que las copias de seguridad sobrevivan incluso si el servidor mismo tiene un problema
- La configuración **Retention Days** controla cuánto tiempo se conservan las copias de seguridad locales — 30 días es un valor predeterminado razonable para la mayoría de tiendas, pero aumenta este valor si el espacio de almacenamiento lo permite
- Después de una restauración, verifica algunos pedidos y productos para confirmar que los datos parezcan correctos antes de salir del modo de mantenimiento manualmente
- Las copias de seguridad encriptadas añaden una capa de seguridad pero requieren la clave de descifrado para restaurarlas — no la pierdas