---
title: Configuración de las opciones de la tienda
---

La configuración de la tienda es el lugar central para configurar la identidad, la localización, la marca y las preferencias operativas de su tienda. Navegue hasta **Configuración > Configuración de la tienda** para comenzar.

![Pestaña general de configuración de la tienda](/static/core/admin/img/help/store-settings/store-settings-general.webp)

## Pestaña General

La **pestaña General** contiene la configuración de identidad principal de la tienda.

### Identidad de la tienda

- **Nombre de la tienda** — El nombre que se muestra en los títulos de las páginas, correos electrónicos y encabezado del administrador.
- **Slogan** — Una descripción breve de su tienda, utilizada en SEO y en el intercambio en redes sociales.
- **URL del sitio** — La dirección web pública de su tienda. Se utiliza en correos electrónicos, generación de mapas del sitio y construcción de enlaces.

### Información de contacto

- **Correo electrónico de contacto** — Recibe notificaciones de pedidos y se muestra en las comunicaciones con los clientes.
- **Número de teléfono** — Número de teléfono opcional para soporte que se muestra en el pie de página y correos electrónicos.

### Dirección de la empresa

Ingrese su dirección completa (calle, ciudad, estado, código postal, país). Se utiliza para:
- Cálculos de origen de envío
- Cálculos de impuestos
- Requisitos legales e facturas

## Branding

### Logo

Suba el logotipo de su tienda (se recomienda PNG o SVG, ~200x50px con fondo transparente). El logotipo aparece en:
- Encabezado de la tienda
- Plantillas de correo electrónico
- Panel de administración

### Icono de la página (Favicon)

Suba un icono cuadrado (ICO o PNG, 32x32px). Aparece como:
- Icono de pestaña del navegador
- Icono de marcador
- Icono de pantalla de inicio móvil

## Localización

### Idioma predeterminado

Elija el idioma principal de su tienda entre 10 opciones compatibles:

| Idioma | Código |
|----------|------|
| Inglés | en |
| Español | es |
| Francés | fr |
| Alemán | de |
| Portugués | pt |
| Japonés | ja |
| Chino simplificado | zh-hans |
| Chino tradicional | zh-hant |
| Ruso | ru |
| Árabe | ar |

El idioma predeterminado controla el idioma de la interfaz de administración y el de respaldo para el contenido de la tienda.

### Zona horaria

Seleccione la zona horaria de su tienda para obtener marcas de tiempo de pedidos precisas, promociones programadas y informes.

### Moneda

- **Moneda predeterminada** — La moneda principal para precios y contabilidad.
- **Múltiples monedas** — Habilite para que los clientes vean precios en su moneda preferida con conversión automática utilizando tasas de cambio en tiempo real.

Configure monedas adicionales en **Configuración > Configuración de la tienda > Moneda**.

## Configuración de comercio electrónico

### Pago sin cuenta

Permita compras sin crear una cuenta:
- Flujo de pago más rápido
- Menos fricción para compradores por primera vez
- Captura menos datos de clientes

### Tiempo de creación de cuenta

Controle cuándo los clientes se le pide crear una cuenta:

| Opción | Descripción |
|--------|-------------|
| **Después de la compra (Recomendado)** | Solicitud de creación de cuenta después de un pedido exitoso — aprovecha la buena voluntad post-compra para la mejor conversión |
| **Durante el pago** | Crear una cuenta antes de procesar el pago |
| **Antes del pago** | Requerir una cuenta antes de comprar (no se recomienda, reduce la conversión) |

También puede configurar un mensaje personalizado de **Creación de cuenta** para explicar los beneficios de registrarse.

### Configuración predeterminada de inventario

- **Seguimiento de inventario** — Habilite el seguimiento de existencias a nivel mundial
- **Límite de existencias bajos** — Nivel de existencias en el que se envían alertas de existencias bajas al correo electrónico del administrador (por defecto: 10 unidades)

### Inteligencia de inventario

![Tarjeta de inteligencia de inventario que muestra los campos de tiempo de reposición predeterminado y multiplicador de existencias de seguridad](/static/core/admin/img/help/store-settings/ecommerce-inventory-intelligence.webp)

Estas configuraciones ajustan los cálculos automáticos de reposición, existencias de seguridad y velocidad de ventas, y controlan cómo se manejan las situaciones de agotado o existencias bajas.

- **Tiempo de reposición predeterminado (días)** — Cuántos días normalmente toma recibir reposición de su proveedor una vez que coloca un pedido (por defecto: 14).

La predicción utiliza esto para marcar productos que necesitan reposición *ahora* para evitar un agotamiento antes de que llegue el nuevo stock.
- **Multiplicador de existencias de seguridad** — Un buffer aplicado sobre la demanda esperada para absorber picos de ventas o retrasos del proveedor.

Por ejemplo, un multiplicador de `1.5` incluye un 50% de margen por encima de su stock de seguridad calculado; `2.0` lo duplica.

Aumente este valor para productos donde se agote sea costoso (mejores ventas, artículos estacionales); córtelo para stock lento que no desee pedir en exceso.
- **Ventana de Cálculo de Velocidad (días)** — La ventana de retroalimentación que Spwig utiliza para calcular la velocidad de ventas de cada producto, lo que a su vez impulsa las sugerencias de reposición y los cálculos de días de suministro (por defecto: 30 días).

Una ventana más corta reacciona más rápido a los cambios recientes en la demanda; una ventana más larga suaviza los picos estacionales, de modo que una sola semana ocupada no distorsione la predicción.
- **Permitir Devoluciones por Defecto** — La configuración inicial de devoluciones aplicada a productos recién creados (desactivada por defecto).

Cada producto aún puede sobrescribirla individualmente en su propia página de producto, y los productos existentes mantienen cualquier configuración que ya tengan — cambiar esto solo cambia el valor predeterminado con el que empiezan los nuevos productos, no actualiza retroactivamente su catálogo.
- **Frecuencia de Alertas de Bajo Nivel de Stock** — Con qué frecuencia se notifica a la aplicación móvil de Spwig sobre bajo nivel de stock: **En tiempo real** envía una notificación de push en el momento en que un producto cruza su límite de bajo nivel de stock; **Resumen Diario** y **Resumen Semanal** envían en su lugar una notificación de push única que resume todos los productos con bajo nivel de stock en ese horario.

Este ajuste solo surte efecto mientras **Alertas de Bajo Nivel de Stock** (Configuración de Correo Electrónico, más abajo) esté habilitado — con las alertas apagadas, no se envían notificaciones en ningún momento.

### Documentos e Facturas

![Tarjeta de Documentos e Facturas que muestra los campos de Número de CUIT / IVA, Texto del Pie de Factura y Texto del Pie de Remito completados con valores de ejemplo](/static/core/admin/img/help/store-settings/ecommerce-documents-invoicing.webp)

Estos campos llenan las facturas y remitos que Spwig genera para los pedidos — por ejemplo, cuando un comerciante descarga o envía por correo una factura en PDF, o imprime un remito para un envío.

- **Número de CUIT / IVA** — Su número de identificación tributaria de su empresa. Se imprime en las facturas generadas para que cumplan con los requisitos de documentación tributaria local.
- **Texto del Pie de Factura** — Texto libre mostrado en la parte inferior de cada factura generada. Usos comunes: condiciones de pago ("Pago dentro de 30 días"), un mensaje de agradecimiento, o detalles de transferencia bancaria.
- **Texto del Pie de Remito** — Texto libre mostrado en la parte inferior de cada remito generado. Usos comunes: instrucciones de devolución o un mensaje al equipo de almacén/operaciones.
- **Ancho del Logo del Documento (px)** — El ancho de su logo de tienda tal como aparece en las facturas y remitos en PDF generados (por defecto: 200px). La altura se escala automáticamente para coincidir, de modo que se preserven las proporciones de su logo. La imagen del logo en sí misma proviene de su **Logo** (Branding, arriba) — los logotipos SVG no se dibujan en documentos PDF, así que suba una versión PNG o JPG de su logo si utiliza arte vectorial en la tienda en línea.

## Configuración de Correo Electrónico

Configure la configuración de entrega de correos electrónicos en **Configuración > Cuentas de Correo Electrónico** y **Configuración > Plantillas de Correo Electrónico**. Vea [Configuración de Correo Electrónico](/help/email-configuration) para más detalles.

Configuraciones clave de correo electrónico disponibles en Configuración de Tienda:

- **Correos Electrónicos de Confirmación de Pedido** — Activa o desactiva los correos electrónicos de confirmación automáticos
- **Correos Electrónicos de Notificación de Envío** — Activa o desactiva las notificaciones de actualizaciones de envío
- **Alertas de Bajo Nivel de Stock** — Enviar alertas al correo electrónico del administrador cuando el stock caiga por debajo del límite
- **Modo de Entrega de Correo Electrónico** — En vivo (entrega normal), En pausa (detener todos los correos), o Solo Registro (registrar pero nunca enviar)
- **Correo Electrónico de Redirección de Prueba** — Redirigir todos los correos salientes a una dirección única para pruebas

## Configuración de Seguridad

### Autenticación de Dos Factores (2FA)

Controle si los miembros del personal deben usar autenticación de dos factores:

| Configuración | Descripción |
|---------|-------------|
| **Opcional** | Los miembros del personal pueden elegir habilitar 2FA pero no es obligatorio |
| **Recomendado** | Los miembros del personal ven un recordatorio que los anima a configurar 2FA |
| **Requerido** | Los miembros del personal no pueden acceder al administrador hasta que se habilite 2FA |

Preserve all markdown formatting, image paths, code blocks, and technical terms.

- **Período de gracia (días)** — Cuántos días tiene el personal para configurar 2FA después de que se active el cumplimiento
- **Permitir dispositivos de confianza** — Permitir que el personal salte la verificación de 2FA en dispositivos reconocidos durante un número de días definido

## Consentimiento de cookies

Configure la franja de consentimiento de cookies que se muestra a los visitantes de la tienda:

- **Consentimiento de cookies activado** — Mostrar o ocultar el anuncio de cookies
- **Posición del anuncio** — Dónde aparece el anuncio en la pantalla (barra inferior, ventana emergente de esquina, etc.)
- **Modo de consentimiento** — Nota simple, opt-in o opt-out
- **Título y texto del anuncio** — Encabezado y descripción personalizables que se muestran a los visitantes
- **Descripciones de categorías** — Descripciones separadas para cookies de análisis, marketing y funcionales

Todos los campos de texto del anuncio admiten traducciones para tiendas multilingües.

## Comunicaciones

La pestaña **Comunicaciones** controla cómo su tienda obtiene, confirma y permite que los clientes gestionen el consentimiento para correos electrónicos y SMS de marketing. Estos ajustes definen su postura de cumplimiento legal (GDPR para correos electrónicos, TCPA para SMS), por lo que debe revisarlos con su asesor legal antes del lanzamiento: Spwig proporciona los controles, no el asesoramiento.

![Pestaña de comunicaciones que muestra los carteles de Consentimiento de correo electrónico de marketing, Preferencias y Darse de baja, y Consentimiento de SMS](/static/core/admin/img/help/store-settings/communications-tab.webp)

### Consentimiento de correo electrónico de marketing

- **Habilitar el doble opt-in para correos electrónicos de marketing** — Cuando está activado, un cliente que se registre para recibir correos electrónicos de marketing recibirá un correo de confirmación y deberá hacer clic en el enlace para que Spwig le envíe cualquier mensaje de marketing. Cuando está desactivado, marcar la casilla de opt-in para marketing es suficiente. Está activado por defecto, según las mejores prácticas de GDPR.
- **Estado predeterminado de opt-in de marketing** — El estado inicial de opt-in de marketing aplicado a las nuevas cuentas de clientes. Está desactivado por defecto (opt-out de GDPR), por lo que los nuevos clientes comienzan sin suscribirse a correos electrónicos de marketing hasta que se registren activamente.

Cuando el doble opt-in está activado, optar por el marketing activa un correo electrónico de confirmación con un enlace de verificación. Hasta que el cliente haga clic en él, se registra como optado por el marketing pero no confirmado, y los envíos de marketing los omiten — los correos electrónicos transaccionales (confirmaciones de pedidos, actualizaciones de envío, restablecimiento de contraseña) nunca se ven afectados por esta configuración.

### Preferencias y darse de baja

- **Habilitar el Centro de preferencias del cliente** — Cuando está activado, los clientes pueden gestionar sus preferencias de correo electrónico y SMS desde una página de servicio de autoatención vinculada desde el panel de control de su cuenta. Cuando está desactivado, esa página y su API de soporte devuelven no disponible y el enlace del panel de control se oculta. Los enlaces de darse de baja de un solo clic en sus correos electrónicos siguen funcionando de cualquier manera: ese escape es requerido para el cumplimiento y no se ve afectado por este interruptor.
- **Recopilar razones de baja** — Cuando está activado, la página de baja de un solo clic pregunta al cliente una breve razón antes de confirmar: *Recibo demasiados correos electrónicos*, *El contenido no es relevante para mí*, *Nunca me registré para esto*, *Ya no estoy interesado*, u *Otra*. La razón que el cliente seleccione se registra en el registro de auditoría de consentimiento para que pueda revisar los patrones de baja con el tiempo.

### Consentimiento de SMS

- **Requerir verificación de SMS** — Cuando está activado (por defecto), un cliente debe verificar su número de teléfono con un código único antes de que Spwig le envíe cualquier SMS, incluyendo mensajes de marketing. Cuando está desactivado, marcar la casilla de opt-in de SMS es suficiente para comenzar a enviar. Este valor predeterminado se cambió a **activado** para la seguridad de TCPA — cámbielo a **desactivado** solo si tiene otro paso de verificación en su flujo de registro.

## Modo de mantenimiento

Habilite el modo de mantenimiento para mantener su tienda fuera de línea temporalmente:
- Muestra un mensaje de mantenimiento personalizado a los visitantes
- Puede vincular una **Página de mantenimiento** creada en el constructor de páginas para una experiencia de marca completa durante el mantenimiento
- Restringe el acceso solo a usuarios administrativos
- Útil durante actualizaciones o migraciones importantes

## Redes sociales

Vincule los perfiles de redes sociales de su tienda. Aparecen en el pie de página y en las plantillas de correo electrónico:

- **URL de Facebook**
- **URL de Twitter**
- **URL de Instagram**
- **URL de LinkedIn**

## Configuraciones de SEO predeterminadas

Preserve all markdown formatting, image paths, code blocks, and technical terms.

Establezca las etiquetas meta predeterminadas que se usan cuando las páginas no tienen sus propias configuraciones de SEO:

- **Título Meta** — Título predeterminado de la página (máximo 60 caracteres)
- **Descripción Meta** — Descripción predeterminada que se muestra en los resultados de búsqueda (máximo 160 caracteres)
- **Palabras Clave Meta** — Palabras clave separadas por comas predeterminadas

## Configuración de Impuestos

Configure la recaudación de impuestos en **Configuración > Configuración de Impuestos**:

1. **Método de Cálculo** — Por dirección de envío, dirección de facturación o ubicación de la tienda
2. **Tasas de Impuestos** — Defina tasas por región y clase de impuesto de producto
3. **Visualización de Impuestos** — Mostrar precios con impuestos, sin impuestos o ambos

## Consejos

- Establezca correctamente su zona horaria antes de procesar cualquier pedido — afecta a todos los registros de hora y informes.
- Habilite el pago como invitado para mejorar las tasas de conversión.
- Complete su dirección de negocio para cálculos precisos de envío y impuestos.
- Suba tanto un logotipo como un favicon para una experiencia profesional y con marca.
- Use el momento de creación de cuenta **Después de la compra** para obtener mejores tasas de registro.
- Habilite la aplicación de autenticación de dos factores para el personal para proteger su administración de la tienda.
- Pruebe los flujos de correo electrónico usando la configuración **Redirección de Prueba de Correo** antes de ir en vivo.
- Establezca el **Tiempo Predeterminado de Reorden** para que coincida con su proveedor más lento — la predicción de reorden aplica este valor único en todo su catálogo, así que sea conservador con el producto con mayor tiempo de espera.
- Complete su **ID de Impuesto / Número de IVA** y texto del pie de página antes de que salga su primer comprobante real a un cliente — ambos campos están en blanco por defecto.
- Deje **Habilitar Confirmación Doble para Correos de Marketing** en activo, a menos que tenga una razón específica para desactivarlo — es la opción predeterminada más segura para el RGPD y protege la reputación de remitente al mantener direcciones no verificadas fuera de sus envíos de marketing.
- Deje **Estado Predeterminado de Consentimiento para Marketing** en desactivado. Marcar como predeterminado el consentimiento para marketing para nuevas cuentas socava el requisito de registro del RGPD, incluso si un cliente podría técnicamente desmarcarlo.
- No desactive **Habilitar Centro de Preferencias de Clientes** solo para simplificar su panel de cuenta — sin él, los clientes aún pueden darse de baja de un tipo de mensaje, pero pierden la capacidad de ajustar sus preferencias (por ejemplo, mantener actualizaciones de envío pero dejar de recibir el boletín).
- Mantenga **Requerir Verificación por SMS** en activo, a menos que su flujo de registro ya confirme los números de teléfono de otra manera (por ejemplo, un inicio de sesión basado en SMS) — el ajuste existe específicamente para mantenerse dentro de las reglas TCPA.

## Solución de Problemas

**Los cambios no aparecen en la tienda:**
- Borre la caché de su navegador
- Ejecute una limpieza de caché desde el panel de administración
- Verifique si el modo de mantenimiento está activado accidentalmente

**Los correos electrónicos no se envían:**
- Verifique la configuración de su proveedor de correo electrónico en la configuración de correo electrónico
- Asegúrese de que **El modo de entrega de correo** esté configurado en **En vivo**
- Asegúrese de que **Correo de redirección de prueba** esté en blanco si quiere que los correos se envíen a destinatarios reales

**La conversión de moneda no funciona:**
- Verifique que su proveedor de tasas de cambio esté conectado
- Revise las credenciales de la API en la configuración de tasas de cambio
- Intente actualizar las tasas manualmente

**Los correos electrónicos de marketing no llegan a los clientes que se registraron:**
- Verifique si **Habilitar Confirmación Doble para Correos de Marketing** está activo — si es así, el cliente debe hacer clic en el enlace de confirmación en el correo de verificación antes de que los envíos de marketing continúen
- Pida al cliente que revise el correo basura/en la carpeta de spam
- Confirme que la opción de marketing del cliente esté activa en sus preferencias — un clic de darse de baja la desactiva

**Los clientes dicen que no pueden encontrar el centro de preferencias:**
- Verifique que **Habilitar Centro de Preferencias de Clientes** esté activo — cuando esté desactivado, el enlace del panel de control se oculta y la página no está disponible por diseño
- El enlace de darse de baja en cualquier correo de marketing siempre funciona independientemente de este ajuste, así que apunte a los clientes allí como alternativa