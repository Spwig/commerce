---
title: Actualizaciones y Mantenimiento
---

Spwig recibe actualizaciones periódicas con nuevas funciones, mejoras de rendimiento y correcciones de seguridad. Esta guía cubre cómo actualizar tu instalación, usar la herramienta de diagnóstico y manejar tareas de mantenimiento.

## Actualizando Spwig

### Antes de actualizar

1. **Crear una copia de seguridad** — ve a **Gestión > Métricas del Sistema > Crear Copia de Seguridad Completa** o ejecuta el script de copia de seguridad desde la línea de comandos. Esta es tu red de seguridad si algo sale mal.
2. **Verificar la versión actual** — visible en **Gestión > Métricas del Sistema** o en el pie de la página del panel de administración.
3. **Revisar los cambios** — abre la página **Actualización del Sistema** para leer las notas completas de la versión nueva antes de instalarla, incluyendo cualquier paso adicional que la versión indique (ver más abajo).

### Revisando lo nuevo en la página de Actualización del Sistema

Cuando Spwig detecta una versión más reciente, **Panel de Control del Sistema** muestra una acción rápida **Actualización Disponible**. Haz clic en ella — o navega primero a **Panel de Control del Sistema > Actualizaciones de la Plataforma** para previsualizar el historial de cambios, luego continúa — para abrir la página **Actualización del Sistema**.

La página muestra:

- **Versión Actual** y **Versión Disponible** tarjetas, para que puedas confirmar exactamente entre qué versiones te estás moviendo
- Una sección **¿Qué es nuevo en {versión}** — un resumen breve de la liberación, seguido de las notas completas de la liberación formateadas con encabezados y listas de viñetas, exactamente como las escribieron los mantenedores
- **Verificaciones previas a la actualización** — espacio en disco, conexión a la base de datos, una copia de seguridad reciente, permisos de escritura y conectividad con el servidor de actualización de Spwig. Haz clic en **Ejecutar Verificaciones Iniciales**; el botón **Iniciar Actualización** permanece deshabilitado hasta que todas las verificaciones pasen
- Un banner **Antes de actualizar** que te recuerda que se crea automáticamente una copia de seguridad, tu tienda entra en modo de mantenimiento brevemente durante la actualización, y no deberías cerrar la página o navegar lejos mientras se ejecuta

Lee cuidadosamente las **Notas de actualización** en la sección ¿Qué es nuevo — algunas liberaciones indican pasos que debes realizar tú mismo después de la actualización. Por ejemplo, una liberación que agrega un nuevo formato de imagen podría pedirte que regeneres tus miniaturas de productos desde **Biblioteca de Medios > Procesamiento de Imágenes** para que las imágenes ya en tu biblioteca aprovechen la mejora; las nuevas subidas lo obtienen automáticamente, pero tu catálogo existente necesita una actualización manual.

Una vez que las verificaciones iniciales pasen, haz clic en **Iniciar Actualización** para comenzar desde el navegador. Una barra de progreso rastrea cada etapa, y la página se recarga automáticamente una vez que se complete la actualización. Este es el camino recomendado para la mayoría de los comerciantes — usa el script basado en SSH a continuación si necesitas un control más directo sobre el proceso.

### Ejecutando una actualización

Conéctate por SSH a tu servidor y navega a tu directorio de instalación de Spwig (normalmente `/opt/spwig`):

```bash
./upgrade.sh
```

El script de actualización:

1. **Verificaciones iniciales** — verifica el espacio en disco, el estado de Docker y el estado de los servicios
2. **Migraciones de base de datos en modo seco** — prueba que los cambios en la base de datos se aplicarán limpiamente sin realizar cambios reales
3. **Ingresa al modo de mantenimiento** — tu tienda muestra una página de mantenimiento a los visitantes durante la actualización
4. **Crea una copia de seguridad** — copia de seguridad automática antes de realizar cambios
5. **Drena los trabajadores en segundo plano** — espera a que las tareas en curso (envíos de correo electrónico, traducciones) finalicen de forma amable
6. **Descarga nuevas imágenes** — descarga la aplicación actualizada desde el registro de Spwig
7. **Aplica migraciones de base de datos** — actualiza el esquema de tu base de datos para la nueva versión
8. **Reinicia los servicios** — inicia la aplicación con la nueva versión
9. **Verificación de salud** — verifica que todos los servicios estén funcionando correctamente
10. **Sale del modo de mantenimiento** — tu tienda vuelve a estar en línea

Si la verificación de salud falla después de la actualización, el script **se revierte automáticamente** a la versión anterior y restaura la copia de seguridad.

### Opciones de actualización

```bash
./upgrade.sh              # Actualización estándar con modo de mantenimiento
./upgrade.sh --dry-run    # Verificar qué cambios se realizarían sin aplicarlos
```

## La herramienta de diagnóstico

Spwig incluye una herramienta de diagnóstico integrada que verifica toda su instalación en busca de problemas:

```bash
./doctor.sh
```

El doctor verifica:

| Categoría | Qué verifica |
|----------|---------------|
| **Sistema** | Espacio en disco, uso de RAM, carga de CPU |
| **Docker** | Salud del motor de Docker, estados de contenedor, versiones de imagen |
| **Base de datos** | Conectividad de PostgreSQL, estado de migración, salud del pool de conexiones |
| **Caché** | Conectividad de Redis, uso de memoria |
| **Almacenamiento de objetos** | Conectividad de MinIO, accesibilidad del bucket |
| **Red** | Resolución de DNS, accesibilidad de puertos, validez del certificado SSL |
| **Aplicación** | Puntos de finalización de salud del servicio, estado de trabajadores en segundo plano |

Cada verificación muestra un resultado de aprobado/rechazado con detalles si algo está mal.

### Modo de reparación automática

Para problemas comunes, el doctor puede intentar reparaciones automáticas:

```bash
./doctor.sh --fix
```

La reparación automática puede resolver:

- Contenedores detenidos (los reinicia)
- Conexiones de base de datos obsoletas (recicla el pool de conexiones)
- Certificados SSL caducados (inicia la renovación)
- Disco lleno por imágenes de Docker antiguas (elimina imágenes no utilizadas)

El doctor siempre explica qué va a reparar antes de tomar medidas.

## Modo de mantenimiento

El modo de mantenimiento muestra a los visitantes una página "la tienda está temporalmente no disponible" mientras realiza cambios. Su panel de administración sigue siendo accesible.

### Habilitar el modo de mantenimiento

Desde el panel de administración: **Configuración de la tienda > Mantenimiento > Habilitar modo de mantenimiento**

O desde la línea de comandos:

```bash
docker exec spwig_shop python manage.py maintenance on
```

### Deshabilitar el modo de mantenimiento

Desde el panel de administración: desactive el interruptor de modo de mantenimiento.

O desde la línea de comandos:

```bash
./go-live.sh
```

### Acceso alternativo durante el mantenimiento

Mientras el modo de mantenimiento esté activo, puede acceder a la tienda normalmente agregando un parámetro secreto a la URL. El secreto de bypass se muestra en su archivo de configuración `.env` bajo `MAINTENANCE_SECRET`.

## Administración de servicios

### Ver el estado de los servicios

Verifique el estado de todos los servicios de Spwig:

```bash
docker compose ps
```

Esto muestra cada servicio, su estado (en ejecución, detenido, reiniciando) y su estado de salud.

### Ver los registros

Ver los registros de un servicio específico:

```bash
docker logs spwig_shop          # Registros de la aplicación
docker logs spwig_celery         # Registros de trabajadores en segundo plano
docker logs spwig_nginx          # Registros de acceso del servidor web
docker logs spwig_db             # Registros de la base de datos
```

Agregue `--tail 100` para ver las últimas 100 líneas, o `--follow` para ver los registros en tiempo real.

### Reiniciar un servicio

Si un servicio específico necesita reiniciarse:

```bash
docker compose restart shop      # Reiniciar la aplicación
docker compose restart celery    # Reiniciar trabajadores en segundo plano
docker compose restart nginx     # Reiniciar el servidor web
```

Para reiniciar todos los servicios:

```bash
docker compose restart
```

## Actualizaciones de componentes

Spwig tiene un mercado de componentes donde puede instalar temas, proveedores de pago, integraciones de envío y otras extensiones. Los componentes se actualizan de forma independiente de la plataforma principal.

Navegue a **Gestión > Actualizaciones de componentes** para verificar las actualizaciones de componentes disponibles. Las actualizaciones se descargan y se aplican automáticamente cuando las aprueba.

## Consejos

- **Actualice regularmente** — mantenerse en la última versión le asegura tener correcciones de seguridad y acceso a nuevas funciones
- **Lea la sección "¿Qué es nuevo" antes de hacer clic en "Iniciar actualización"** — es la forma más rápida de detectar una migración de base de datos requerida, una corrección de seguridad o una **Nota de actualización** que necesite actuar después
- **Siempre haga una copia de seguridad primero** — aunque el script de actualización crea una copia de seguridad automática, tener su propia copia brinda una seguridad adicional
- **Ejecute doctor después de los problemas** — si su tienda se comporta de forma inesperada, `./doctor.sh` es la forma más rápida de identificar problemas
- **Programe las actualizaciones para tiempos de baja actividad** — el modo de mantenimiento interrumpe brevemente el acceso de los clientes, por lo tanto, actualice durante horas de poca actividad
- **Mantenga espacio en disco disponible** — las actualizaciones necesitan espacio temporal para nuevas imágenes y copias de seguridad. Mantenga al menos 5 GB libres.