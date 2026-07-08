---
title: Configuración SSL
---

SSL (Secure Sockets Layer) encripta la conexión entre los navegadores de tus clientes y tu tienda. Cuando SSL está activo, la URL de tu tienda comienza con `https://` y los navegadores muestran un icono de candado. El SSL es esencial para aceptar pagos, proteger los datos de los clientes y obtener un buen posicionamiento en los motores de búsqueda.

Spwig admite varios modos de SSL para adaptarse a diferentes configuraciones de alojamiento. Esta guía explica cada modo y te ayuda a elegir el adecuado.

## Elegir un modo SSL

| Modo | Mejor para | Costo del certificado | Renovación |
|------|----------|-----------------|---------|
| **Let's Encrypt** | La mayoría de las tiendas | Gratis | Automática |
| **Cloudflare Origin CA** | Tiendas que usan el proxy de Cloudflare | Gratis | Manual (hasta 15 años) |
| **Certificado personalizado** | Tiendas con certificados comprados | Varía | Manual |
| **Gestionado externamente** | Balanceadores de carga, Cloudflare Flexible | N/A | N/A |
| **Autofirmado** | Desarrollo y pruebas | Gratis | Manual |
| **Ninguno (HTTP)** | Solo desarrollo local | N/A | N/A |

Si no estás seguro de qué modo usar, **Let's Encrypt** es la mejor opción para la mayoría de las tiendas. Es gratis, automático y confiable en todos los navegadores.

## Let's Encrypt

Let's Encrypt proporciona certificados SSL gratuitos y confiables que se renuevan automáticamente cada 60-90 días. Este es la opción recomendada para la mayoría de los comerciantes.

**Requisitos:**
- Tu dominio debe apuntar a tu servidor (registro A en DNS)
- El puerto 80 debe estar accesible desde Internet (para la verificación del certificado)
- Una dirección de correo electrónico para notificaciones de vencimiento del certificado

**Pasos de configuración:**
1. Ve a **Configuración > Configuración del sitio** y abre la pestaña **Dominio y SSL**
2. Ingresa tu nombre de dominio
3. Selecciona **Let's Encrypt**
4. Ingresa tu dirección de correo electrónico de administrador
5. Haz clic en **Aplicar configuración**

Spwig maneja todo lo demás automáticamente: verificar tu dominio, obtener el certificado, configurar NGINX y establecer la renovación automática.

## Cloudflare Origin CA

Los certificados de Cloudflare Origin CA encriptan la conexión entre los servidores de borde de Cloudflare y tu tienda. Estos certificados son gratuitos y pueden durar hasta 15 años, pero solo son **confiables para Cloudflare** — los navegadores que se conecten directamente a tu servidor verán una advertencia de certificado.

Este modo es ideal si usas Cloudflare como proxy (nube naranja activa) para tu dominio. Cloudflare presenta su propio certificado confiable a los visitantes, y el certificado Origin CA asegura la conexión entre Cloudflare y tu servidor.

**Requisitos:**
- Una cuenta de Cloudflare con tu dominio agregado
- Un certificado Origin CA y una clave privada generada desde el panel de Cloudflare
- El modo SSL/TLS de Cloudflare establecido en **Completo (Estricto)**

**Generar el certificado Origin CA:**
1. Inicia sesión en tu panel de Cloudflare
2. Selecciona tu dominio
3. Ve a **SSL/TLS > Servidor de origen**
4. Haz clic en **Crear certificado**
5. Elige RSA o ECC (RSA es más compatible)
6. Añade tu dominio (por ejemplo, `example.com` y `*.example.com`)
7. Elige un período de validez (se recomienda 15 años)
8. Haz clic en **Crear** y copia tanto el certificado como la clave privada

**Configurar en Spwig:**
1. Ve a **Configuración > Configuración del sitio** y abre la pestaña **Dominio y SSL**
2. Ingresa tu nombre de dominio
3. Selecciona **Cloudflare Origin CA**
4. Pega el certificado en el campo **Certificado (PEM)**
5. Pega la clave privada en el campo **Clave privada (PEM)**
6. Haz clic en **Aplicar configuración**

**Después de la configuración:**
- En Cloudflare, establece el modo SSL/TLS en **Completo (Estricto)**
- Activa el proxy de Cloudflare (nube naranja) para el registro DNS de tu dominio
- Tu tienda estará accesible mediante HTTPS con el certificado confiable de Cloudflare

## Certificado personalizado

Usa este modo si has comprado un certificado SSL de una autoridad de certificación (CA) como DigiCert, Sectigo o GoDaddy, o si tu proveedor de alojamiento lo ha emitido para ti.

**Pasos de configuración:**
1.

Ve a **Configuración > Configuración del sitio** y abre la pestaña **Dominio y SSL**
2.

Ingresa tu nombre de dominio
3.

Selecciona **Certificado personalizado**
4.

Mantén todo el formato de markdown, rutas de imágenes, bloques de código y términos técnicos.

Pega tu cadena de certificados (incluyendo certificados intermedios) en el campo **Certificate (PEM)**
5.

Pega tu clave privada en el campo **Private Key (PEM)**
6.

Haz clic en **Apply Configuration**

Tu certificado debe incluir la cadena completa: tu certificado de dominio seguido de cualquier certificado intermedio. La clave privada debe estar en formato PEM (que comience con `-----BEGIN PRIVATE KEY-----` o `-----BEGIN RSA PRIVATE KEY-----`).

## Managed Externally

Elige este modo cuando el SSL se termine en un servicio externo antes de que el tráfico llegue a tu servidor. En esta configuración, tu servidor solo recibe tráfico HTTP plano — no se instala ningún certificado en el servidor en sí.

**Escenarios comunes:**
- **Cloudflare Flexible SSL** -- Cloudflare encripta el tráfico del navegador a Cloudflare, pero envía HTTP a tu servidor
- **Balanceadores de carga en la nube** -- AWS ALB, Google Cloud Load Balancer o DigitalOcean Load Balancer terminan el SSL y reenvían HTTP
- **Proxy inverso** -- Otro servidor frente a Spwig maneja el SSL

**Pasos de configuración:**
1. Ve a **Settings > Site Settings** y abre la pestaña **Domain & SSL**
2. Ingresa tu nombre de dominio
3. Selecciona **Managed Externally**
4. Haz clic en **Apply Configuration**

Spwig configurará NGINX para servir solo HTTP y confiará en el encabezado `X-Forwarded-Proto` de tu proxy para detectar correctamente a los visitantes de HTTPS.

## Self-Signed Certificate

Los certificados autofirmados encriptan la conexión pero no son confiados por los navegadores. Los visitantes verán una advertencia de seguridad que deben ignorar manualmente. Este modo es adecuado solo para servidores de desarrollo y pruebas internas.

**Pasos de configuración:**
1. Ve a **Settings > Site Settings** y abre la pestaña **Domain & SSL**
2. Ingresa tu nombre de dominio
3. Selecciona **Self-Signed**
4. Haz clic en **Apply Configuration**

Spwig genera automáticamente un certificado autofirmado. No uses este modo para una tienda en producción.

## Troubleshooting

**Certificado no funciona después de la configuración:**
- Verifica que el registro A de tu dominio apunte a la dirección IP de tu servidor
- Asegúrate de que los puertos 80 y 443 estén abiertos en tu firewall
- Espera unos minutos para que los cambios de DNS se propaguen

**Let's Encrypt no logra emitir un certificado:**
- Verifica que tu dominio resuelva a la dirección IP de este servidor
- Asegúrate de que el puerto 80 no esté bloqueado por un firewall
- Si estás detrás de Cloudflare, establece temporalmente el DNS en "DNS only" (nube gris) durante la emisión del certificado

**Cloudflare muestra "Error 526" (Certificado SSL inválido):**
- Asegúrate de haber seleccionado el modo **Cloudflare Origin CA** (no Managed Externally)
- Verifica que el modo SSL/TLS de Cloudflare esté configurado en **Full (Strict)**
- Verifica que el certificado de Origin CA no haya expirado

**El navegador muestra "No seguro" a pesar de tener SSL:**
- Algunas páginas pueden cargar imágenes o scripts a través de HTTP (contenido mixto). Verifica la consola de desarrollador de tu navegador para advertencias de contenido mixto.
- Asegúrate de que la URL de tu sitio en Configuración use `https://`