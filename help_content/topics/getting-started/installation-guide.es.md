---
title: Guía de instalación
---

Esta guía te guía a través de la instalación de Spwig en tu propio servidor. El proceso completo es automático — un solo comando maneja la configuración de Docker, la creación de la base de datos, la configuración de servicios y los certificados SSL.

## Antes de comenzar

Necesitas:

- Un servidor ejecutando **Ubuntu 22.04 o 24.04** (también se admite Debian 12)
- **Acceso de root o sudo** al servidor
- Al menos **4 GB de RAM** y **20 GB de espacio en disco** (se recomienda 8 GB de RAM)
- Un **token de licencia** de tu compra de Spwig (verifica tu recibo de correo electrónico)
- Opcionalmente, un **nombre de dominio** apuntando a la dirección IP de tu servidor

> **Consejo:** Puedes instalar sin un dominio y agregar uno más tarde usando la herramienta de configuración de dominios. Tu tienda estará accesible a través de la dirección IP del servidor en el medio tiempo.

## Ejecutar el instalador

Conéctate a tu servidor mediante SSH y ejecuta el comando de instalación desde tu correo electrónico de confirmación de compra. Tiene este aspecto:

```bash
curl -fsSL https://spwig.com/install.sh | sudo bash -s -- --token YOUR_LICENSE_TOKEN
```

Reemplaza `YOUR_LICENSE_TOKEN` con el token de tu correo electrónico.

El instalador pasa por ocho fases automáticamente:

1. **Comprobaciones previas** — verifica que tu servidor cumple con los requisitos (sistema operativo, disco, RAM, puertos)
2. **Validación del token** — confirma tu licencia y extrae la configuración de tu tienda
3. **Detección del modo** — determina el mejor modo de instalación para tu servidor (ver más abajo)
4. **Configuración** — genera contraseñas seguras, credenciales de base de datos y configuración de servicios
5. **Descarga de imágenes** — obtiene las imágenes de la aplicación Spwig desde el registro
6. **Inicio del servicio** — inicia la base de datos, el caché, la aplicación y los trabajadores en segundo plano en orden
7. **Configuración de SSL** — obtiene un certificado SSL si tienes un dominio configurado
8. **Finalización** — crea tu cuenta de administrador y genera scripts de conveniencia

El proceso toma 5–15 minutos dependiendo de la velocidad de internet de tu servidor.

## Modos de instalación

El instalador detecta automáticamente el entorno del servidor y selecciona el mejor modo. También puedes especificar uno manualmente con la bandera `--mode`.

### Modo independiente

**Recomendado para:** servidores dedicados e instancias VPS donde Spwig es la única aplicación web.

- Usa directamente los puertos 80 y 443
- Maneja automáticamente los certificados SSL a través de Let's Encrypt
- Este es el modo más común y recomendado

### Modo sidecar

**Recomendado para:** servidores que ya ejecutan otra aplicación web (WordPress, un sitio web de la empresa, etc.) en los puertos 80/443.

- Spwig se ejecuta en un puerto alternativo (detectado automáticamente, generalmente 8080 o 8443)
- El instalador genera un bloque de configuración de proxy de nginx para que lo agregues a tu servidor web existente
- Tu servidor web existente maneja SSL y proxyea el tráfico a Spwig

### Modo local

**Recomendado para:** desarrollo y pruebas en tu propia computadora.

- Solo accesible en `localhost` o `127.0.0.1`
- Usa un certificado SSL autofirmado (tu navegador mostrará una advertencia de seguridad — esto es normal)
- Se habilitan características de depuración
- No se requiere validación de licencia

## ¿Qué ocurre durante la instalación

### Docker

Si Docker no está ya instalado, el instalador ofrece instalarlo para ti. Spwig se ejecuta completamente dentro de contenedores de Docker — nada se instala directamente en el sistema operativo de tu servidor fuera de Docker.

### Servicios creados

El instalador crea estos servicios:

| Servicio | Propósito |
|---------|---------|
| **Base de datos** (PostgreSQL 16) | Almacena todos los datos de tu tienda — productos, pedidos, clientes, configuraciones |
| **Caché** (Redis) | Acelera la carga de páginas y gestiona colas de tareas en segundo plano |
| **Conector de conexiones** (PgBouncer) | Gestiona eficientemente las conexiones a la base de datos |
| **Almacenamiento de objetos** (MinIO) | Almacena imágenes, archivos y medios cargados |
| **Aplicación** (Spwig) | La tienda en sí — panel de administración y tienda en línea |
| **Servidor web** (Nginx) | Proporciona tu tienda a los visitantes con compresión y almacenamiento en caché |
| **Trabajador en segundo plano** (Celery) | Procesa correos electrónicos, traducciones, análisis y otras tareas en segundo plano |
| **Programador de tareas** (Celery Beat) | Ejecuta tareas programadas como copias de seguridad automatizadas y campañas de correo electrónico |
| **Traductor** | Servicio de traducción impulsado por IA para tiendas multilingües |
| **Actualizador** | Maneja actualizaciones de componentes desde el mercado Spwig |

### Cuenta de administrador

Al finalizar la instalación, se te solicita crear una cuenta de administrador. Esta es la cuenta que usarás para iniciar sesión en el panel de administración de tu tienda.

### Modo de mantenimiento

Tu tienda comienza en **modo de mantenimiento** — los visitantes ven una página "Próximamente". Esto te da tiempo para configurar tu tienda (añadir productos, configurar métodos de pago, personalizar tu tema) antes de lanzarla.

Cuando estés listo, ejecuta el script de conveniencia que creó el instalador:

```bash
./go-live.sh
```

O desactiva el modo de mantenimiento desde **Administrador > Configuración de la tienda > Mantenimiento**.

## Después de la instalación

Una vez que el instalador finalice, verás un resumen con:

- Tu URL de tienda
- Tu URL del panel de administración (normalmente `https://yourdomain.com/en/admin/`)
- La ubicación de tus archivos de configuración
- Scripts de conveniencia disponibles

### Scripts de conveniencia

El instalador crea estos scripts en tu directorio de instalación:

- **`./go-live.sh`** — saca tu tienda del modo de mantenimiento
- **`./configure-domain.sh`** — agrega o cambia tu dominio y obtiene un certificado SSL

### Pasos siguientes

1. Inicia sesión en tu panel de administración
2. Completa el **Asistente de configuración** — te guía a través del nombre de la tienda, moneda, zona horaria y configuraciones básicas
3. Añade tus productos
4. Configura un método de pago
5. Elige y personaliza un tema
6. Ejecuta `./go-live.sh` cuando estés listo

## Instalación en mercados en la nube

Spwig está disponible como una aplicación de un solo clic en varios proveedores de nube:

- **DigitalOcean** — despliega desde el Mercado de DigitalOcean
- **Akamai (Linode)** — despliega desde el Mercado de Linode
- **Vultr** — despliega desde el Mercado de Vultr

Estas imágenes del mercado vienen con el instalador precargado. Después de crear el servidor, inicia sesión por SSH y sigue las instrucciones en pantalla para completar la configuración con tu token de licencia.

## Obtener ayuda

Si la instalación falla o encuentras un error:

1. Ejecuta la **herramienta de diagnóstico**: `./doctor.sh` (creada durante la instalación)
2. El doctor verifica todos los servicios, conectividad, SSL y problemas comunes
3. Usa `./doctor.sh --fix` para intentar reparaciones automáticas
4. Contacta al soporte de Spwig con la salida del doctor si el problema persiste