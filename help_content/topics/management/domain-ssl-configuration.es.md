---
title: Configuración de dominio y SSL
---

Esta guía explica cómo conectar un dominio personalizado a tu tienda Spwig y configurar certificados SSL para acceder mediante HTTPS seguro. Puedes configurar un dominio durante la instalación o agregar uno más tarde.

## Añadir un dominio después de la instalación

Si instalaste Spwig sin un dominio (usando la dirección IP del servidor), puedes agregar uno en cualquier momento.

### Paso 1: Configurar DNS

Con tu registrador de dominios o proveedor de DNS:

1. Crea un **registro A** que apunte tu dominio (o subdominio) a la dirección IP de tu servidor
2. Si usas un subdominio como `shop.example.com`, crea el registro A para `shop`
3. Espera la propagación del DNS — esto suele tomar 5–60 minutos

Verificar que el registro DNS funcione:

```bash
 dig +short shop.example.com
```

Esto debe devolver la dirección IP de tu servidor.

### Paso 2: Ejecutar el script de configuración del dominio

Accede por SSH a tu servidor y navega hasta el directorio de instalación de Spwig:

```bash
 ./configure-domain.sh
```

El script:

1. Preguntará por tu nombre de dominio
2. Verificará que el DNS apunte a tu servidor
3. Actualizará la configuración de la tienda
4. Obtendrá un certificado SSL gratuito de Let's Encrypt
5. Configurará el servidor web para usar HTTPS
6. Reiniciará los servicios relevantes

Tu tienda ahora está accesible en `https://yourdomain.com`.

### Paso 3: Actualizar la configuración de la tienda

Después de agregar un dominio, inicia sesión en tu panel de administración y ve a **Configuración de la tienda**. Verifica que la **URL de la tienda** coincida con tu nuevo dominio. Esto asegura que los correos, facturas y enlaces usen la dirección correcta.

## Certificados SSL

### SSL automático (Let's Encrypt)

En **modo standalone**, el instalador obtiene automáticamente un certificado SSL gratuito de Let's Encrypt. Estos certificados:

- Son confiados por todos los navegadores principales
- Son válidos por 90 días
- Se renuevan automáticamente — una verificación de renovación se ejecuta diariamente, y los certificados se renuevan cuando tengan menos de 30 días restantes
- Cubren tu dominio exacto (por ejemplo, `shop.example.com`)

No necesitas gestionar la renovación manualmente.

### Certificados autofirmados

En algunos casos, Spwig usa un certificado autofirmado en su lugar:

- **Instalaciones en modo local** (desarrollo/pruebas)
- Cuando Let's Encrypt no puede alcanzar tu servidor (puerto 80 bloqueado por firewall, DNS aún no propagado)
- Cuando no se ha configurado ningún dominio (acceso solo por IP)

Los certificados autofirmados encriptan el tráfico pero no son confiados por los navegadores — los visitantes verán una advertencia de seguridad. Esto es aceptable para pruebas, pero no debe usarse en producción.

### SSL en modo sidecar

En **modo sidecar**, tu servidor web existente (Apache, Nginx, Caddy, etc.) maneja el cierre de SSL. Spwig se ejecuta en un puerto HTTP detrás de tu proxy. Configura SSL en tu servidor web principal como lo harías normalmente.

El instalador genera un bloque de configuración de proxy que puedes agregar a tu servidor web. Para Nginx, se parece a:

```nginx
 location / {
     proxy_pass http://127.0.0.1:8080;
     proxy_set_header Host $host;
     proxy_set_header X-Real-IP $remote_addr;
     proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
     proxy_set_header X-Forwarded-Proto $scheme;
 }
```

## Cambiar tu dominio

Para cambiar a un dominio diferente:

1. Configura el DNS para el nuevo dominio (registro A apuntando a tu servidor)
2. Ejecuta `./configure-domain.sh` nuevamente con el nuevo dominio
3. El script actualiza toda la configuración, obtiene un nuevo certificado y reinicia los servicios
4. Actualiza **Configuración de la tienda** en el panel de administración con la nueva URL

Tu antiguo dominio dejará de funcionar una vez que se actualice la configuración.

## Solución de problemas

### "Validación de DNS fallida"

El script configure-domain verifica que tu dominio apunte a tu servidor antes de solicitar un certificado. Si esta verificación falla:

- Verifica que el registro A sea correcto con `dig +short yourdomain.com`
- Espera unos minutos más para la propagación del DNS
- Verifica que estés configurando el dominio o subdominio exacto (no un comodín)

### "Límite de tasa de Let's Encrypt alcanzado"

Let's Encrypt limita las solicitudes de certificados a 5 por dominio por semana. Si alcanzas este límite:

Preservar todo el formato markdown, rutas de imágenes, bloques de código y términos técnicos.

- Espere 7 días antes de intentarlo nuevamente
- Use un subdominio diferente en el transcurso
- La tienda sigue siendo accesible mediante HTTP o con un certificado autofirmado mientras espera

### "El puerto 80 no es alcanzable"

Let's Encrypt debe conectarse a su servidor en el puerto 80 para verificar la propiedad del dominio. Asegúrese de:

- Que su firewall permita el tráfico entrante TCP en el puerto 80
- Que ninguna otra aplicación esté bloqueando el puerto 80
- Que el grupo de seguridad o firewall de su proveedor de nube permita el puerto 80

### Fallos en la renovación del certificado

Si la renovación automática falla, el certificado expirará después de 90 días. Para renovar manualmente:

```bash
docker exec spwig_nginx certbot renew
docker exec spwig_nginx nginx -s reload
```

Revise el registro de renovación para obtener detalles si esto falla. La causa más común es el puerto 80 estar bloqueado por un cambio en el firewall después de la instalación inicial.