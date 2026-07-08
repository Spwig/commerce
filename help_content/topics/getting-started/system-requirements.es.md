---
title: Requisitos del sistema
---

Spwig funciona en la mayoría de los servidores Linux modernos. Esta página cubre las especificaciones mínimas y recomendadas, qué ocurre en servidores más pequeños y cuáles son los proveedores de nube que funcionan bien.

## Requisitos mínimos

| Recurso | Mínimo | Recomendado |
|----------|---------|-------------|
| **Sistema operativo** | Ubuntu 22.04 LTS, Ubuntu 24.04 LTS o Debian 12 | Ubuntu 24.04 LTS |
| **RAM** | 4 GB | 8 GB o más |
| **Espacio en disco** | 20 GB | 40 GB o más |
| **CPU** | 1 vCPU | 2+ vCPUs |
| **Arquitectura** | x86_64 (AMD64) | x86_64 |
| **Red** | Dirección IP pública (para modo independiente) | IP pública estática |
| **Puertos** | 80 y 443 (independiente) o cualquier puerto alternativo (sidecar) | 80 y 443 |

> **Nota:** Los servidores basados en ARM (por ejemplo, AWS Graviton, Oracle Ampere) no están actualmente soportados.

## Niveles de recursos

El instalador detecta automáticamente la RAM disponible en su servidor y selecciona el nivel de recursos adecuado.

### Nivel estándar (6 GB+ de RAM)

Todos los servicios funcionan con todas sus capacidades:

- Servicio de **traducción impulsado por IA** habilitado — traduzca descripciones de productos, contenido de páginas y texto SEO a múltiples idiomas directamente desde su panel de administración
- Asignación completa de memoria para la aplicación, base de datos y trabajadores en segundo plano
- Concurrencia optimizada para los trabajadores en segundo plano según la cantidad de CPU

### Nivel pequeño (4–6 GB de RAM)

El instalador se adapta para conservar memoria:

- El servicio de traducción por IA está **deshabilitado** para ahorrar aproximadamente 2 GB de RAM. Aún puede gestionar traducciones manualmente o usar herramientas de traducción externas — solo el traductor de IA integrado se ve afectado.
- Los límites de memoria para la aplicación y los trabajadores se reducen
- Todas las demás características funcionan exactamente igual que en el nivel estándar

> **Consejo:** Si comienza con un servidor pequeño y luego actualiza a 6 GB+ de RAM, vuelva a ejecutar el instalador para habilitar el servicio de traducción.

## Proveedores de nube recomendados

Spwig funciona en cualquier servidor Linux que cumpla con los requisitos. Estos proveedores han sido probados y ofrecen un buen valor:

| Proveedor | Plan recomendado | RAM | Disco | Costo aproximado |
|----------|-----------------|-----|------|-----------------|
| **DigitalOcean** | Droplet básico | 4 GB | 80 GB | $24/mes |
| **Linode (Akamai)** | 4 GB compartido | 4 GB | 80 GB | $24/mes |
| **Vultr** | Computación en la nube | 4 GB | 100 GB | $24/mes |
| **Hetzner** | CX31 | 8 GB | 80 GB | €8/mes |
| **OVH** | VPS de inicio | 4 GB | 80 GB | €7/mes |

Para tiendas que esperan un tráfico significativo o catálogos de productos grandes (10,000+ productos), comience con 8 GB de RAM y 2+ vCPUs.

## Uso del espacio en disco

Una instalación reciente de Spwig utiliza aproximadamente 8 GB de espacio en disco:

| Componente | Tamaño |
|-----------|------|
| Imágenes de Docker | ~4 GB |
| Base de datos (tienda vacía) | ~200 MB |
| Modelos de traducción por IA (si están habilitados) | ~2 GB |
| Archivos de la aplicación y configuración | ~500 MB |
| Sistema operativo y motor de Docker | ~3 GB |

Planee espacio adicional para:

- **Imágenes y medios de productos** — depende del tamaño de su catálogo. Presupuestar 1–5 GB para una tienda típica con cientos de productos.
- **Crecimiento de la base de datos** — crece con pedidos, clientes y datos de análisis. Una tienda que procesa 100 pedidos al día crece aproximadamente 1 GB al año.
- **Copia de seguridad** — si almacena copias de seguridad localmente, cada copia de seguridad completa es aproximadamente el tamaño de su base de datos más los medios. Con una política de retención de 30 días, presupuestar 2–3× el tamaño de sus datos actuales.

## Dominio y DNS

Un nombre de dominio es opcional durante la instalación, pero es necesario para el uso en producción. Necesita:

- Un dominio o subdominio (por ejemplo, `shop.example.com`)
- Un **registro A** que apunte a la dirección IP pública de su servidor
- Propagación del DNS completada (normalmente 5–60 minutos después de agregar el registro)

El instalador obtiene automáticamente un certificado SSL gratuito de Let's Encrypt cuando se detecta un dominio válido. También puede agregar un dominio después de la instalación usando el script `./configure-domain.sh`.

## Firewall

Si su servidor tiene un firewall (la mayoría de los proveedores de nube lo habilitan por defecto), asegúrese de que estos puertos estén abiertos:

| Puerto | Protocolo | Propósito |
|-------|-----------|----------|
| **22** | TCP | Acceso SSH (para que puedas administrar el servidor) |
| **80** | TCP | HTTP (requerido para la validación del certificado Let's Encrypt) |
| **443** | TCP | HTTPS (tráfico seguro de su tienda) |

En el modo sidecar, abra el puerto alternativo asignado por el instalador en lugar de 80/443.

## Requisitos de software

El instalador maneja automáticamente la instalación de todo el software. Para referencia, estos son los componentes que instala o verifica:

- **Docker Engine** — tiempo de ejecución de contenedores (se instala automáticamente si falta)
- **Docker Compose** — orquestación de servicios (incluido con Docker Engine)
- **curl** — utilizado por el instalador mismo (presente en casi todos los sistemas Linux)

No se necesita instalar ningún otro software previamente. Spwig no requiere que instale Python, Node.js, PostgreSQL, Redis o Nginx manualmente — todo funciona dentro de contenedores Docker.