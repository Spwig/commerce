---
title: Actualizaciones y Mantenimiento
---

Spwig recibe actualizaciones periódicas con nuevas funciones, mejoras de rendimiento y correcciones de seguridad. Esta guía cubre cómo actualizar tu instalación, usar la herramienta de diagnóstico y manejar tareas de mantenimiento.

## Actualizando Spwig

### Antes de actualizar

1. **Crear una copia de seguridad** — ve a **Management > System Metrics > Create Full Backup** o ejecuta el script de copia de seguridad desde la línea de comandos. Esta es tu red de seguridad si algo sale mal.
2. **Verificar la versión actual** — visible en **Management > System Metrics** o en el pie de la página del panel de administración.
3. **Leer las notas de la versión** — disponibles en el panel de administración bajo **Management > Component Updates** cuando se detecta una nueva versión.

### Ejecutar una actualización

Conéctate por SSH a tu servidor y navega hasta el directorio de instalación de Spwig (normalmente `/opt/spwig`):

```bash
./upgrade.sh
```

El script de actualización:

1. **Comprobaciones previas** — verifica el espacio en disco, el estado de Docker y el estado de los servicios
2. **Migraciones de base de datos en modo seco** — prueba que los cambios en la base de datos se aplicarán limpiamente sin realizar cambios reales
3. **Ingresa al modo de mantenimiento** — tu tienda muestra una página de mantenimiento a los visitantes durante la actualización
4. **Crea una copia de seguridad** — copia de seguridad automática de seguridad antes de realizar cambios
5. **Drena los trabajadores en segundo plano** — espera a que las tareas en curso (envíos de correo electrónico, traducciones) finalicen de forma suave
6. **Descarga nuevas imágenes** — descarga la aplicación actualizada desde el registro de Spwig
7. **Aplica migraciones de base de datos** — actualiza el esquema de tu base de datos para la nueva versión
8. **Reinicia los servicios** — inicia la aplicación con la nueva versión
9. **Comprobación de salud** — verifica que todos los servicios estén funcionando correctamente
10. **Sale del modo de mantenimiento** — tu tienda vuelve a estar en línea

Si la comprobación de salud falla después de la actualización, el script **revertirá automáticamente** a la versión anterior y restaurará la copia de seguridad.

### Opciones de actualización

```bash
./upgrade.sh              # Actualización estándar con modo de mantenimiento
./upgrade.sh --dry-run    # Ver qué cambios se realizarían sin aplicarlos
```

## La herramienta de diagnóstico

Spwig incluye una herramienta de diagnóstico integrada que verifica toda tu instalación en busca de problemas:

```bash
./doctor.sh
```

El doctor verifica:

| Categoría | Qué verifica |
|----------|---------------|
| **Sistema** | Espacio en disco, uso de RAM, carga de CPU |
| **Docker** | Salud del motor de Docker, estados de contenedor, versiones de imagen |
| **Base de datos** | Conectividad a PostgreSQL, estado de migración, salud del pool de conexiones |
| **Caché** | Conectividad a Redis, uso de memoria |
| **Almacenamiento de objetos** | Conectividad a MinIO, accesibilidad del bucket |
| **Red** | Resolución de DNS, accesibilidad de puertos, validez del certificado SSL |
| **Aplicación** | Puntos de verificación de salud del servicio, estado de trabajadores en segundo plano |

Cada comprobación muestra un resultado de aprobado/rechazado con detalles si algo está mal.

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

El modo de mantenimiento muestra a los visitantes una página "la tienda está temporalmente no disponible" mientras realizas cambios. Tu panel de administración sigue siendo accesible.

### Habilitar el modo de mantenimiento

Desde el panel de administración: **Store Settings > Maintenance > Enable Maintenance Mode**

O desde la línea de comandos:

```bash
docker exec spwig_shop python manage.py maintenance on
```

### Deshabilitar el modo de mantenimiento

Desde el panel de administración: activa el interruptor de modo de mantenimiento para deshabilitarlo.

O desde la línea de comandos:

```bash
./go-live.sh
```

### Acceso alternativo durante el mantenimiento

Mientras el modo de mantenimiento esté activo, puedes acceder a la tienda normalmente añadiendo un parámetro secreto a la URL. El secreto de bypass se muestra en tu archivo de configuración `.env` bajo `MAINTENANCE_SECRET`.

## Administración de servicios

### Ver el estado de los servicios

# Verificar el estado de todos los servicios de Spwig:

```bash
docker compose ps
```

Esto muestra cada servicio, su estado (en ejecución, detenido, reiniciando) y su estado de salud.

### Ver logs

Ver los logs de un servicio específico:

```bash
docker logs spwig_shop          # Logs de la aplicación
docker logs spwig_celery         # Logs del worker en segundo plano
docker logs spwig_nginx          # Logs de acceso del servidor web
docker logs spwig_db             # Logs de la base de datos
```

Agrega `--tail 100` para ver las últimas 100 líneas, o `--follow` para ver los logs en tiempo real.

### Reiniciar un servicio

Si se necesita reiniciar un servicio específico:

```bash
docker compose restart shop      # Reiniciar la aplicación
docker compose restart celery    # Reiniciar los workers en segundo plano
docker compose restart nginx     # Reiniciar el servidor web
```

Para reiniciar todos los servicios:

```bash
docker compose restart
```

## Actualizaciones de componentes

Spwig tiene un mercado de componentes donde puedes instalar temas, proveedores de pago, integraciones de envío y otras extensiones. Los componentes se actualizan de forma independiente de la plataforma principal.

Navega a **Gestión > Actualizaciones de componentes** para revisar las actualizaciones disponibles. Las actualizaciones se descargan y aplican automáticamente cuando las apruebas.

## Consejos

- **Actualiza regularmente** — mantenerse en la última versión asegura que tengas correcciones de seguridad y acceso a nuevas funciones
- **Siempre haz una copia de seguridad primero** — aunque el script de actualización crea una copia de seguridad automática, tener tu propia copia brinda mayor seguridad
- **Ejecuta doctor después de problemas** — si tu tienda se comporta de forma inesperada, `./doctor.sh` es la forma más rápida de identificar problemas
- **Programa actualizaciones para tiempos de baja actividad** — el modo de mantenimiento interrumpe brevemente el acceso de los clientes, por lo que actualiza durante horas de baja actividad
- **Mantén espacio en disco disponible** — las actualizaciones necesitan espacio temporal para nuevas imágenes y copias de seguridad. Mantén al menos 5 GB libres.