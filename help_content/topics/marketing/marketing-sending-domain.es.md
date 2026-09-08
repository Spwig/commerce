---
title: Dominio de envío de marketing
---

# Dominio de envío de marketing

Tu tienda envía dos tipos de correo electrónico muy diferentes:

- **Transaccional** — confirmaciones de pedido, actualizaciones de envío, restablecimientos de contraseña. Estos
  deben llegar siempre a la bandeja de entrada.
- **Marketing** — boletines, promociones, recuperación de carrito, alertas de reposición.

Por defecto, ambos se envían bajo la misma identidad de envío, lo que significa que **comparten una
reputación de remitente**. Si una campaña de marketing genera quejas de spam o llega a direcciones
obsoletas, esa reputación disminuye — y tus confirmaciones de pedido y restablecimientos de contraseña pueden
empezar a caer en la carpeta de spam también.

Un **dominio de envío de marketing** soluciona esto. Configuras una segunda identidad de envío — en su
propio subdominio, como `news.yourstore.com` — y la marcas para marketing. Spwig luego envía
cada campaña desde esa identidad y mantiene el correo transaccional en tu dominio principal. Una campaña
pobre ya no puede arrastrar hacia abajo el correo que tus clientes *necesitan* recibir.

> Esto se aplica a tiendas autoalojadas. En los planes alojados por Spwig, la reputación de envío se
> gestiona por ti.

## Cómo Spwig decide qué identidad usar

Una vez que existe una cuenta de envío de marketing, la enrutación es automática — no tienes que etiquetar nada:

- **Correo de marketing** (campañas, recorridos, boletines, recuperación de carrito, reposición) →
  el dominio de envío de marketing.
- **Correo transaccional** (pedidos, envío, restablecimientos de contraseña, verificación) → tu dominio
  principal.

Si nunca configuras un dominio de marketing, no cambia nada: todo continúa enviándose
 desde tu cuenta predeterminada exactamente como antes.

## Configúralo

Puedes comenzar desde cualquiera de estos puntos de entrada:

- El botón **"Configurar dominio de marketing"** en el banner del panel de Campaign Studio, o
- **Cuentas de correo → "Dominio de envío de marketing"**.

![El panel de Campaign Studio con el banner "Protege tu correo transaccional" y su botón Configurar dominio de marketing](/static/core/admin/img/help/marketing-sending-domain/marketing-domain-nudge.webp)

![El botón Dominio de envío de marketing en la lista de Cuentas de correo, junto a Explorar proveedores](/static/core/admin/img/help/marketing-sending-domain/marketing-domain-button.webp)

Ambos abren el asistente de configuración de correo premarcado para una cuenta de marketing. Luego:

1. **Elige un subdominio.** Usa algo como `news.yourstore.com` o
   `mail.yourstore.com`. Este es el paso más importante: la identidad de marketing debe ser un
   **(sub)dominio diferente** del que usa tu correo transaccional — esa separación
   es exactamente lo que protege tu reputación transaccional. Enviar marketing desde tu
   dominio principal no te da ningún aislamiento.
2. **Introduce la dirección del remitente** en ese subdominio, p. ej. `news@news.yourstore.com`.
3. **Añade los registros DNS.** El asistente genera registros SPF, DKIM y DMARC para el
   subdominio — incluyendo una clave DKIM que es única para esta identidad de marketing. Añádelos en
   tu proveedor de DNS (el asistente tiene botones de copiar y pestañas por proveedor), luego ejecuta la
   comprobación hasta que todos los registros pasen.
4. **Termina.** La cuenta se crea y se marca como **Solo marketing**. A partir de ahora tus
   campañas se enviarán desde ella.

Puedes confirmar que funcionó en la lista de **Cuentas de correo**: verás una segunda cuenta con
un propósito de **Solo marketing**, y el banner de Campaign Studio desaparece.

## Bueno saber

- **No puedes romper accidentalmente el correo transaccional.** Spwig no te permitirá establecer tu única
  cuenta como "Solo marketing", ni deshabilitar/eliminar tu última cuenta transaccional — siempre
  habrá un lugar para las confirmaciones de pedido y los restablecimientos de contraseña.
- **Calienta gradualmente.** Un dominio de envío nuevo no tiene reputación aún.

Aumenta tu
  volumen a lo largo de un par de semanas en lugar de enviar a toda tu lista el primer día.
- **Mantén el DNS del subdominio saludable.** SPF, DKIM y DMARC en el subdominio de marketing
  deben permanecer válidos, igual que tu dominio principal.

Vea el [Email Deliverability Runbook](deliverability) para obtener una visión completa.
- **El consentimiento sigue vigente.** El correo de marketing solo se envía a suscriptores que se hayan dado de alta,
  y cada campaña incluye un enlace de cancelación de suscripción — separar el dominio no cambia nada de eso.