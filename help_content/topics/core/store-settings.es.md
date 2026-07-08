---
title: Configuración de la tienda
---

La Configuración de la tienda es el lugar central para configurar la identidad, localización, branding y preferencias operativas de su tienda. Navegue a **Configuración > Configuración de la tienda** para comenzar.

![pestaña general de configuración de tienda](/static/core/admin/img/help/store-settings/store-settings-general.webp)

## Pestaña General

La pestaña **General** contiene la configuración de identidad básica de su tienda.

### Identidad de la tienda

- **Nombre de la tienda** — El nombre que se muestra en los títulos de página, correos electrónicos y el encabezado de la administración.
- **Lema** — Una breve descripción de su tienda, utilizada en SEO y compartir en redes sociales.
- **URL del sitio** — La dirección web pública de su tienda. Se utiliza en correos electrónicos, generación de mapas de sitio y construcción de enlaces.

### Información de contacto

- **Correo electrónico de contacto** — Recibe notificaciones de pedidos y se muestra en las comunicaciones con los clientes.
- **Número de teléfono** — Número de teléfono de soporte opcional mostrado en el pie de página y correos electrónicos.

### Dirección de la empresa

Introduzca su dirección completa (calle, ciudad, estado, código postal, país). Se utiliza para:
- Cálculos de origen de envío
- Cálculos de impuestos
- Requisitos legales y facturas

## Branding

### Logo

Cargue el logotipo de su tienda (se recomienda PNG o SVG, ~200x50px con fondo transparente). El logotipo aparece en:
- El encabezado del almacén
- Plantillas de correo electrónico
- El panel de administración

### Favicon

Cargue un favicon cuadrado (ICO o PNG, 32x32px). Aparece como:
- El icono de la pestaña del navegador
- El icono de marcador de página
- El icono de la pantalla de inicio móvil

## Localización

### Idioma predeterminado

Elija el idioma principal de su tienda entre 10 opciones admitidas:

| Idioma | Código |
|----------|------|
| Inglés | en |
| Español | es |
| Francés | fr |
| Alemán | de |
| Portugués | pt |
| Japonés | ja |
| Chino Simplificado | zh-hans |
| Chino Tradicional | zh-hant |
| Ruso | ru |
| Árabe | ar |

El idioma predeterminado controla el idioma de la interfaz de administración y el idioma de respaldo para el contenido del almacén.

### Zona horaria

Elija la zona horaria de su tienda para obtener marcas de tiempo precisas de los pedidos, promociones programadas y reportes.

### Moneda

- **Moneda predeterminada** — La moneda principal para precios y contabilidad.
- **Moneda múltiple** — Active para permitir que los clientes vean los precios en su moneda preferida con conversión automática usando tasas de cambio en tiempo real.

Configure monedas adicionales en **Configuración > Configuración de la tienda > Moneda**.

## Configuración de comercio electrónico

### Pago como invitado

Permita compras sin crear una cuenta:
- Flujo de pago más rápido
- Menos fricción para compradores primerizos
- Captura menos datos del cliente

### Formato de número de pedido

Personalice cómo aparecen los números de pedido:
- **Prefijo** — p. ej., "ORD-"
- **Número de inicio** — El primer número de pedido
- **Relleno** — p. ej., 00001

### Configuraciones de inventario predeterminadas

- **Seguimiento de inventario** — Active el seguimiento de stock a nivel global
- **Umbral de stock bajo** — Nivel de alerta (por defecto: 5 unidades)
- **Permitir pedidos de stock agotado** — Aceptar pedidos cuando se agote el stock

## Configuración de correo electrónico

### Información del remitente

- **Nombre del remitente** — Aparece como el remitente del correo electrónico (normalmente el nombre de su tienda)
- **Correo electrónico del remitente** — Debe ser de un dominio verificado
- **Correo electrónico de respuesta** — Donde se dirigen las respuestas del cliente

### Proveedor de correo electrónico

Configure su servicio de entrega de correo electrónico en **Configuración > Configuración de correo electrónico**. Los proveedores admitidos incluyen SMTP, SendGrid, Mailgun y Amazon SES.

## Legal y cumplimiento

Agregue las políticas de su tienda para cumplir con los requisitos legales:

- **Términos y condiciones** — Requerido para el checkout; los clientes deben aceptar antes de comprar
- **Política de privacidad** — Cumplimiento con GDPR/CCPA; vinculado en el pie de página
- **Política de devolución** — Defina su ventana de devolución, condiciones y proceso de reembolso

## Modo de mantenimiento

Active el modo de mantenimiento para desconectar temporalmente su tienda:
- Muestra un mensaje personalizado de mantenimiento a los visitantes
- Restringe el acceso solo a usuarios de administración
- Útil durante actualizaciones importantes o migraciones

## Configuración de impuestos

Configure la recopilación de impuestos en **Configuración > Configuración de impuestos**:

1. **Método de cálculo** — Por dirección de envío, dirección de facturación o ubicación de la tienda
2. **Tasas de impuesto** — Defina tasas por región y clase de impuesto del producto
3. **Mostrar impuestos** — Muestre precios con impuestos, sin impuestos o ambos

## Consejos

- Establezca correctamente su zona horaria antes de procesar cualquier pedido — afecta a todas las marcas de tiempo y reportes.
- Active el pago como invitado para mejorar las tasas de conversión.
- Rellene su dirección de la empresa para cálculos precisos de envío e impuestos.
- Suba tanto un logotipo como un favicon para una experiencia profesional y con branding.
- Revise regularmente sus páginas legales para mantenerse conforme con las regulaciones locales.

## Solución de problemas

**Cambios no apareciendo en el almacén:**
- Limpie la caché del navegador
- Ejecute una limpieza de caché desde el panel de administración
- Verifique si el modo de mantenimiento se activó accidentalmente

**Correos electrónicos no enviando:**
- Verifique la configuración de su proveedor de correo electrónico en Configuración de correo electrónico
- Verifique que el dominio del correo electrónico "From" esté verificado
- Pruebe la conexión desde la página de configuración del proveedor

**Conversión de moneda no funcionando:**
- Verifique que su proveedor de tasas de cambio esté conectado
- Verifique las credenciales de API en la configuración de tasas de cambio
- Intente actualizar las tasas manualmente

