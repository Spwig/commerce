---
title: Resumen del Programa de Afiliados
---

La función del programa de afiliados de Spwig le permite reclutar socios que promuevan sus productos a cambio de comisiones. Este canal de marketing extiende su alcance a través de influencers, bloggers, creadores de contenido y embajadores de marca que comparten enlaces de seguimiento únicos con su audiencia. Cuando alguien hace clic en un enlace de afiliado y realiza una compra, el afiliado gana una comisión y usted gana un cliente.

Este resumen explica qué es el programa de afiliados, para quién es y cómo los comerciantes lo utilizan para construir una red de socios que impulsa las ventas.

![Panel del comerciante](/static/core/admin/img/help/affiliate-program-overview/merchant-dashboard.webp)

## Conceptos clave

Entender estos términos clave le ayudará a configurar y gestionar su programa de afiliados:

| Término | Definición |
|---------|----------|
| **Afiliado** | Un socio que promueve sus productos y gana comisiones por ventas referidas |
| **Programa** | Una estructura de comisión con tasas, reglas y configuraciones (puede crear múltiples programas) |
| **Enlace de seguimiento** | Un URL único que contiene el código del afiliado (por ejemplo, `yourstore.com/?ref=CODE`) |
| **Comisión** | El pago que recibe un afiliado por una venta referida, calculado según las reglas del programa |
| **Duración de la cookie** | Cuántos días persiste la cookie de seguimiento después de que un cliente haga clic en un enlace de afiliado |
| **Pago** | Un pago masivo que liquida múltiples comisiones aprobadas a la vez |
| **Panel del comerciante** | Su interfaz de administración para gestionar programas, afiliados, comisiones y pagos |
| **Portal del afiliado** | El panel público donde los afiliados ven sus ganancias, obtienen enlaces de seguimiento y solicitan pagos |

## Cómo funciona

El flujo de trabajo de los afiliados sigue cuatro etapas principales:

### 1. Solicitar
Afiliados descubren su programa y envían solicitudes a través del portal público de afiliados en `/affiliate/` en su tienda. Puede habilitar **aprobación automática** para programas abiertos o **revisión manual** para alianzas por invitación.

### 2. Aprobar
Revise las solicitudes pendientes en **Marketing > Afiliados**. Verifique el sitio web, la presencia en redes sociales y la coincidencia de la audiencia de cada candidato antes de aprobar. Una vez aprobado, el afiliado recibe sus credenciales de inicio de sesión y puede acceder a su panel.

### 3. Promocionar
Los afiliados aprobados obtienen enlaces de referencia únicos desde su portal. Comparten estos enlaces en artículos de blog, redes sociales, boletines de correo electrónico o en cualquier lugar donde se conecten con su audiencia. Spwig establece una cookie de seguimiento cuando alguien hace clic en el enlace.

### 4. Ganar
Cuando un cliente referido completa una compra dentro del período de vida útil de la cookie, Spwig crea un registro de comisión. Revise y apruebe las comisiones en **Marketing > Comisiones**, luego procese los pagos cuando los afiliados alcancen el umbral mínimo de pago.

## Resumen del flujo de trabajo del comerciante

Como comerciante, gestiona el ciclo de vida completo del programa desde su panel de administración:

### Crear programas
Comience creando uno o más programas de afiliados en **Marketing > Programas de Afiliados**. Cada programa tiene su propia estructura de comisión, duración de la cookie y configuraciones de aprobación. Puede crear programas separados para influencers (comisión más alta) versus socios generales (comisión más baja).

### Revisar solicitudes
Nuevas solicitudes de afiliados aparecen en **Marketing > Afiliados** con un estado **Pendiente**. Revise cada solicitud para verificar que el socio sea adecuado para su marca. Apruebe para activar su cuenta o rechace con una razón.

### Aprobar comisiones
Cuando los afiliados generan ventas, las comisiones aparecen en **Marketing > Comisiones** con un estado **Pendiente**. Revise el pedido vinculado para verificar que sea legítimo (no una auto-referencia, no un pedido devuelto), luego apruebe o rechace según corresponda.

### Procesar pagos
Una vez que los afiliados acumulan comisiones aprobadas por encima del umbral mínimo de pago, procese pagos masivos en **Marketing > Pagos**. Spwig se integra con PayPal y Airwallex para pagos automatizados, o puede registrar transferencias bancarias manuales.

## Resumen del flujo de trabajo del afiliado

Entender cómo los afiliados experimentan su programa le ayuda a diseñar una mejor onboarding y soporte:

### Solicitar
Los afiliados visitan su portal de afiliados, leen los detalles del programa (tasa de comisión, duración de la cookie, términos de pago) y envían una solicitud con su información de contacto y canales de promoción.

### Crear enlaces
Después de la aprobación, los afiliados inician sesión en su panel para generar enlaces de seguimiento. Pueden crear enlaces generales de la tienda o enlaces a productos/categorías específicos que deseen promover.

### Promocionar
Los afiliados comparten sus enlaces de seguimiento en cualquier lugar donde se conecten con posibles clientes — artículos de blog, videos de YouTube, historias de Instagram, boletines de correo electrónico o sitios de comparación.

### Solicitar pagos
Los afiliados rastrean sus ganancias en tiempo real a través del panel del portal de afiliados. Cuando su saldo aprobado alcanza el umbral mínimo de pago, pueden solicitar un pago.

## Dónde encontrar cada función

| Función | Ubicación en el administrador | Descripción |
|--------|-----------------------------|-----------|
| **Programas** | Marketing > Programas de Afiliados | Crear y configurar estructuras de comisión |
| **Afiliados** | Marketing > Afiliados | Revisar solicitudes, gestionar cuentas de afiliados |
| **Comisiones** | Marketing > Comisiones | Revisar y aprobar comisiones pendientes |
| **Pagos** | Marketing > Pagos | Procesar pagos masivos a afiliados |
| **Configuraciones** | Marketing > Configuraciones de Afiliados | Configuraciones globales, proveedores de pago, personalización del portal |
| **Panel** | Marketing > Panel de Afiliados | Vista general de análisis con clics, pedidos y totales de comisión |

El portal orientado a afiliados está disponible automáticamente en `/affiliate/` en la URL pública de su tienda.

## Casos de uso comunes

Estos son cuatro métodos probados que los comerciantes utilizan para aprovechar el programa de afiliados de Spwig y crecer su negocio:

### Alianzas con influencers
Aliéncese con influencers de redes sociales que tengan audiencias comprometidas en su nicho. Ofrezca tasas de comisión más altas (15–20%) para atraer influencers de calidad que puedan generar tráfico significativo. Use enlaces de seguimiento para medir el ROI de cada alianza.

### Embajadores de marca
Construya una red de clientes leales que se conviertan en embajadores de la marca. Ofrezca a estos clientes recurrentes cuentas de afiliados para que puedan ganar comisiones cuando refieran a amigos y familiares. Esto funciona especialmente bien para productos de nicho con comunidades apasionadas.

### Creadores de contenido
Contrate bloggers, YouTubers y podcasters que creen guías de compra, reseñas o contenido de comparación. Los afiliados con contenido de larga duración pueden generar referidos consistentes mes tras mes.

### Redes de referidos
Permita que los clientes existentes se unan a su programa y ganen comisiones al compartir productos que les gustan. Esto crea un bucle viral donde los clientes satisfechos se convierten en promotores, trayendo nuevos clientes que también pueden convertirse en afiliados.

## Consejos

- **Empiece con un solo programa** — Cree un programa de socios general con una tasa de comisión del 10% y una duración de cookie de 30 días. Puede agregar programas especializados más tarde una vez que entienda qué socios funcionan mejor.
- **Establezca expectativas claras** — Documente su proceso de aprobación, cronograma de comisiones y horario de pagos en el portal de afiliados. La transparencia construye confianza y reduce las solicitudes de soporte.
- **Supervise fraudes** — Revise cuidadosamente las comisiones en busca de señales de alerta como auto-referencias (afiliados comprando desde sus propios enlaces), tasas de devolución inusualmente altas o patrones de clics sospechosos. Rechace inmediatamente las comisiones fraudulentas.
- **Comunique regularmente** — Envíe actualizaciones mensuales a sus afiliados con noticias del programa, resaltados del calendario promocional y reconocimiento a los principales colaboradores. La comunicación activa mantiene a los afiliados comprometidos y promoviendo.
- **Optimice para móviles** — La mayoría de los afiliados comparten enlaces en redes sociales donde la mayoría de los clics provienen de dispositivos móviles. Pruebe su flujo de pago en teléfonos para asegurar una experiencia fluida para los clientes referidos.
- **Proporcione activos creativos** — Haga fácil para los afiliados promocionar sus productos proporcionando imágenes de banner, fotos de productos y copia preescrita que puedan usar en su contenido.