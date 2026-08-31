---
title: Configuración de la tienda
---

La Configuración de la tienda es el lugar central para configurar la identidad, la localización, la marca y las preferencias operativas de su tienda. Vaya a **Configuración > Configuración de la tienda** para comenzar.

![Pestaña general de configuración de la tienda](/static/core/admin/img/help/store-settings/store-settings-general.webp)

## Pestaña General

La pestaña **General** contiene la configuración de identidad principal de su tienda.

### Identidad de la tienda

- **Nombre de la tienda** — El nombre de visualización mostrado en los títulos de las páginas, correos electrónicos y la cabecera del panel de administración.
- **Eslogan** — Una breve descripción de su tienda, utilizada en SEO y en el compartir en redes sociales.
- **URL del sitio** — La dirección web pública de su tienda. Se utiliza en correos electrónicos, generación de mapas del sitio y construcción de enlaces.

### Información de contacto

- **Correo de contacto** — Recibe notificaciones de pedidos y se muestra en las comunicaciones con los clientes.
- **Número de teléfono** — Número de teléfono de soporte opcional que se muestra en el pie de página y en los correos electrónicos.

### Dirección comercial

Introduzca su dirección completa (calle, ciudad, estado, código postal, país). Se utiliza para:
- Cálculos del origen del envío
- Cálculos de impuestos
- Requisitos legales y facturas

## Marca

### Logotipo

Suba el logotipo de su tienda (se recomienda PNG o SVG, ~200x50px con fondo transparente). El logotipo aparece en:
- La cabecera de la tienda
- Plantillas de correo electrónico
- El panel de administración

### Favicon

Suba un favicon cuadrado (ICO o PNG, 32x32px). Aparece como:
- Icono de la pestaña del navegador
- Icono de marcador
- Icono de la pantalla de inicio móvil

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
| Chino simplificado | zh-hans |
| Chino tradicional | zh-hant |
| Ruso | ru |
| Árabe | ar |

El idioma predeterminado controla el idioma de la interfaz de administración y el valor predeterminado para el contenido de la tienda.

### Zona horaria

Seleccione la zona horaria de su tienda para obtener marcas de tiempo de pedidos precisas, promociones programadas e informes.

### Moneda

- **Moneda predeterminada** — La moneda principal para precios y contabilidad.
- **Multimoneda** — Habilítelo para permitir que los clientes vean los precios en su moneda preferida con conversión automática utilizando tasas de cambio en tiempo real.

Configure monedas adicionales en **Configuración > Configuración de la tienda > Moneda**.

## Configuración de comercio electrónico

### Compra como invitado

Permita compras sin crear una cuenta:
- Flujo de compra más rápido
- Menor fricción para compradores por primera vez
- Captura menos datos del cliente

### Momento de creación de la cuenta

Controle cuándo se solicita a los clientes que creen una cuenta:

| Opción | Descripción |
|--------|-------------|
| **Después de la compra (Recomendado)** | Solicitar la creación de la cuenta después de un pedido exitoso — aprovecha la buena voluntad posterior a la compra para la mejor conversión |
| **Durante la compra** | Crear una cuenta antes de que se procese el pago |
| **Antes de la compra** | Requerir una cuenta antes de comprar (no recomendado — reduce la conversión) |

También puede configurar un **Mensaje de creación de cuenta** personalizado para explicar los beneficios del registro.

### Valores predeterminados de inventario

- **Seguimiento de inventario** — Habilitar el seguimiento de existencias globalmente
- **Umbral de stock bajo** — Nivel de stock en el que se envían alertas de stock bajo al correo del administrador (predeterminado: 10 unidades)

### Inteligencia de inventario

![Tarjeta de Inteligencia de inventario que muestra los campos Tiempo de reposición predeterminado, Multiplicador de stock de seguridad, Ventana de cálculo de velocidad, Permitir pedidos pendientes por defecto y Frecuencia de alerta de stock bajo](/static/core/admin/img/help/store-settings/ecommerce-inventory-intelligence.webp)

Estas configuraciones ajustan los cálculos automáticos de reposición, stock de seguridad y velocidad de ventas, y controlan cómo se manejan las situaciones de stock agotado y stock bajo.

- **Tiempo de reposición predeterminado (Días)** — Cuántos días suele tardar en recibir el reposición de su proveedor una vez que realiza un pedido (predeterminado: 14).

El pronóstico utiliza esto para marcar los productos que necesitan reabastecimiento *ahora* para evitar un agotamiento de inventario antes de que llegue el nuevo stock.
- **Multiplicador de Stock de Seguridad** — Un colchón aplicado sobre la demanda esperada para absorber picos de ventas o retrasos del proveedor.

Por ejemplo, un multiplicador de `1.5` incorpora un colchón del 50% sobre el stock de seguridad calculado; `2.0` lo duplica.

Aumente este valor para productos donde el agotamiento es costoso (los más vendidos, artículos estacionales); bájelo para el stock de rotación lenta que no desea sobreordenar.
- **Ventana de Cálculo de Velocidad (Días)** — La ventana de retroceso que Spwig utiliza para calcular la velocidad de ventas de cada producto, lo cual a su vez impulsa las sugerencias de reabastecimiento y las cifras de días de suministro (predeterminado: 30).

Una ventana más corta reacciona más rápido a los cambios recientes en la demanda; una ventana más larga suaviza los picos estacionales para que una sola semana ocupada no distorsione el pronóstico.
- **Permitir Pedidos Pendientes por Defecto** — La configuración inicial de pedidos pendientes aplicada a los productos recién creados (desactivado por defecto).

Cada producto aún puede anularlo individualmente en su propia página de producto, y los productos existentes conservan la configuración que ya tengan — cambiar esto solo modifica el valor predeterminado con el que comienzan los nuevos productos, no actualiza retroactivamente su catálogo.
- **Frecuencia de Alertas de Stock Bajo** — Con qué frecuencia su aplicación móvil de Spwig se notifica sobre el stock bajo: **Tiempo real** envía una notificación push en el momento en que un producto cruza su umbral de stock bajo; **Resumen Diario** y **Resumen Semanal** en cambio envían una única notificación push que resume todos los productos actualmente con stock bajo según esa programación.

Esta configuración solo tiene efecto mientras **Alertas de Stock Bajo** (Configuración de Correo, abajo) esté habilitada — con las alertas desactivadas, no se envían notificaciones en ninguna frecuencia.

### Documentos y Facturación

![Tarjeta de Documentos y Facturación que muestra los campos de ID Fiscal / Número de IVA, Texto de Pie de Factura, Texto de Pie de Nota de Empaque y Ancho del Logotipo del Documento, llenados con valores de ejemplo](/static/core/admin/img/help/store-settings/ecommerce-documents-invoicing.webp)

Estos campos completan las facturas y notas de empaque que Spwig genera para los pedidos — por ejemplo, cuando un comerciante descarga o envía por correo electrónico una factura PDF, o imprime una nota de empaque para un envío.

- **ID Fiscal / Número de IVA** — Su número de identificación fiscal de la empresa. Impreso en las facturas generadas para que cumplan con los requisitos de documentación fiscal local.
- **Texto de Pie de Factura** — Texto libre mostrado en la parte inferior de cada factura generada. Usos comunes: términos de pago ("Pago debido dentro de 30 días"), un mensaje de agradecimiento o detalles de transferencia bancaria.
- **Texto de Pie de Nota de Empaque** — Texto libre mostrado en la parte inferior de cada nota de empaque generada. Usos comunes: instrucciones de devolución o una nota para el equipo de almacén/cumplimiento.
- **Ancho del Logotipo del Documento (px)** — El ancho de su logotipo de tienda tal como aparece en las facturas PDF y notas de empaque generadas (predeterminado: 200px). La altura se escala automáticamente para coincidir, por lo que las proporciones de su logotipo se preservan. La imagen del logotipo en sí proviene de su **Logotipo** (Marca, arriba) — los logotipos SVG no se dibujan en documentos PDF, por lo que cargue una versión PNG o JPG de su logotipo si usa arte vectorial en la tienda en línea.

## Configuración de Correo

Configure los ajustes de envío de correo en **Configuración > Cuentas de Correo** y **Configuración > Plantillas de Correo**. Consulte [Configuración de Correo](/help/email-configuration) para obtener todos los detalles.

Ajustes clave de correo disponibles en Configuración de Tienda:

- **Correos de Confirmación de Pedido** — Activar o desactivar los correos de confirmación automáticos
- **Correos de Notificación de Envío** — Activar o desactivar las notificaciones de actualización de envío
- **Alertas de Stock Bajo** — Enviar alertas al correo del administrador cuando el stock cae por debajo del umbral
- **Modo de Entrega de Correo** — En vivo (entrega normal), Pausado (retener todos los correos) o Solo Registro (registrar pero nunca enviar)
- **Correo de Redirección de Prueba** — Redirigir todos los correos salientes a una única dirección para pruebas

## Configuración de Seguridad

### Autenticación de Dos Factores (2FA)

Controlar si el personal está obligado a usar la autenticación de dos factores:


| Configuración | Descripción |
|---------|-------------|
| **Opcional** | El personal puede elegir habilitar 2FA, pero no es obligatorio |
| **Recomendado** | El personal recibe un aviso que los anima a configurar 2FA |
| **Requerido** | El personal no puede acceder al administrador hasta que se habilite 2FA |

- **Período de Gracia (días)** — Cuántos días tiene el personal para configurar 2FA después de activar la aplicación
- **Permitir Dispositivos Conocidos** — Permitir que el personal salte 2FA en dispositivos reconocidos durante un número determinado de días

## Consentimiento de Cookies

Configure la franja de anuncio de consentimiento de cookies mostrada a los visitantes de la tienda:

- **Consentimiento de Cookies Habilitado** — Mostrar o ocultar el anuncio de cookies
- **Posición del Anuncio** — Dónde aparece el anuncio en la pantalla (barra inferior, ventana emergente de esquina, etc.)
- **Modo de Consentimiento** — Nota simple, opt-in o opt-out
- **Título y Texto del Anuncio** — Encabezado y descripción personalizables mostrados a los visitantes
- **Descripciones de Categorías** — Descripciones separadas para cookies de análisis, marketing y funcionales

Todos los campos de texto del anuncio admiten traducciones para tiendas multilingües.

## Comunicaciones

La pestaña **Comunicaciones** controla cómo su tienda obtiene, confirma y permite que los clientes gestionen el consentimiento para correos electrónicos y SMS de marketing. Estas configuraciones definen su postura de cumplimiento legal (GDPR para correos electrónicos, TCPA para SMS), por lo que debe revisarlas con su asesor legal antes del lanzamiento — Spwig proporciona los controles, no el asesoramiento.

![Pestaña de Comunicaciones que muestra los carteles de Consentimiento de Marketing por Correo Electrónico, Preferencias y Darse de Baja, y Consentimiento de SMS](/static/core/admin/img/help/store-settings/communications-tab.webp)

### Consentimiento de Marketing por Correo Electrónico

- **Habilitar Confirmación Doble para Correos Electrónicos de Marketing** — Cuando está activado, un cliente que se registre para recibir correos electrónicos de marketing recibirá un correo de confirmación y deberá hacer clic en el enlace para que Spwig le envíe cualquier mensaje de marketing. Cuando está desactivado, marcar la casilla de opt-in para marketing es suficiente. Está activado por defecto, de acuerdo con las mejores prácticas de GDPR.
- **Estado predeterminado de opt-in para marketing** — El estado inicial de opt-in para marketing aplicado a nuevas cuentas de clientes. Está desactivado por defecto (opt-out de GDPR), por lo que los nuevos clientes comienzan sin suscribirse a correos electrónicos de marketing hasta que se registren activamente.

Cuando la confirmación doble está activada, optar por el marketing activa un correo electrónico de confirmación con un enlace de verificación. Hasta que el cliente haga clic en él, se registra como optado por el marketing pero no confirmado, y los envíos de marketing los omiten — los correos electrónicos transaccionales (confirmaciones de pedidos, actualizaciones de envío, restablecimiento de contraseña) nunca se ven afectados por esta configuración.

### Preferencias y Darse de Baja

- **Habilitar Centro de Preferencias del Cliente** — Cuando está activado, los clientes pueden gestionar sus preferencias de correo electrónico y SMS desde una página de auto-servicio vinculada a su tablero de usuario. Cuando está desactivado, esa página y su API de soporte devuelven no disponible y el enlace del tablero de usuario se oculta. Los enlaces de baja de un clic en sus correos siguen funcionando de cualquier manera — ese escape es requerido para el cumplimiento y no se ve afectado por este interruptor.
- **Recopilar Razones de Baja** — Cuando está activado, la página de baja de un clic pregunta al cliente una breve razón antes de confirmar: *Recibo demasiados correos electrónicos*, *El contenido no es relevante para mí*, *Nunca me registré para esto*, *Ya no estoy interesado*, u *Otra*. La razón que el cliente seleccione se registra en el registro de auditoría de consentimiento para que pueda revisar los patrones de baja con el tiempo.

### Consentimiento de SMS

- **Requerir Verificación de SMS** — Cuando está activado (por defecto), un cliente debe verificar su número de teléfono con un código de un solo uso antes de que Spwig le envíe cualquier SMS, incluyendo mensajes de marketing. Cuando está desactivado, marcar la casilla de opt-in para SMS es suficiente para comenzar a enviar. Este valor predeterminado se cambió a **activado** para la seguridad de TCPA — cámbielo a **desactivado** solo si tiene otro paso de verificación en su flujo de registro.

## Modo de Mantenimiento

Habilite el modo de mantenimiento para mantener su tienda fuera de línea temporalmente:
- Muestra un mensaje de mantenimiento personalizado a los visitantes
- Puede vincular una **Página de Mantenimiento** construida en el Page Builder para una experiencia de marca completa de mantenimiento
- Restringe el acceso solo a usuarios administradores
- Útil durante actualizaciones o migraciones importantes

## Redes Sociales

Vincule los perfiles de redes sociales de su tienda. Aparecen en el pie de página y plantillas de correo electrónico:

- **URL de Facebook**
- **URL de Twitter**
- **URL de Instagram**
- **URL de LinkedIn**

## Configuración por Defecto de SEO

Establezca etiquetas meta predeterminadas que se usan cuando las páginas no tienen sus propias configuraciones de SEO:

- **Título Meta** — Título de página predeterminado (máximo 60 caracteres)
- **Descripción Meta** — Descripción predeterminada que se muestra en los resultados de búsqueda (máximo 160 caracteres)
- **Palabras Clave Meta** — Palabras clave separadas por comas predeterminadas

## Configuración de Impuestos

Configure la recaudación de impuestos en **Configuración > Configuración de Impuestos**:

1. **Método de Cálculo** — Por dirección de envío, dirección de facturación o ubicación de la tienda
2. **Tasas de Impuestos** — Defina tasas por región y clase de producto de impuestos
3. **Visualización de Impuestos** — Mostrar precios con impuestos, sin impuestos o ambos

## Consejos

- Establezca correctamente su zona horaria antes de procesar cualquier pedido — afecta a todos los registros de hora y informes.
- Habilite el pago sin registrarse para mejorar las tasas de conversión.
- Complete su dirección de negocio para cálculos precisos de envío y impuestos.
- Suba un logotipo y favicon para una experiencia profesional y con marca.
- Use el momento de creación de cuenta **Después de la compra** para obtener mejores tasas de registro.
- Habilite la aplicación de autenticación de dos factores para el personal para proteger su administración de la tienda.
- Pruebe los flujos de correo electrónico usando la configuración **Redirección de Prueba de Correo** antes de ir en vivo.
- Establezca el **Tiempo de Reorden Predeterminado** para que coincida con su proveedor más lento regular — la predicción de reorden aplica este valor único en todo su catálogo, así que sea conservador con el valor más largo de sus productos.
- Acortar la **Ventana de Cálculo de Velocidad** si tiene promociones o reposiciones frecuentes y quiere que la predicción reaccione rápidamente a las ventas de los últimos días; alargue si quiere una vista más estable y menos propensa a picos de demanda.
- Si activa **Permitir Pedidos de Devolución por Defecto**, recuerde que solo establece el punto de partida para productos creados *después* del cambio — vuelva a revisar productos individuales si quiere que los pedidos de devolución estén habilitados en todo su catálogo actual también.
- Ajuste **Frecuencia de Alerta de Bajo Stock** según qué tan activamente gestione el stock: **En Tiempo Real** para catálogos de movimiento rápido donde cada riesgo de agotamiento de stock requiera atención inmediata, **Resumen Diario** o **Resumen Semanal** para evitar el agotamiento de alertas en un catálogo más grande.
- Complete su **ID de Impuesto / Número de IVA** y texto del pie de página antes de que salga su primer comprobante real a un cliente — ambos campos están en blanco por defecto.
- Si su **Logotipo** es un SVG, suba una versión PNG o JPG también — **Ancho del Logotipo del Documento** no tiene efecto en PDFs porque Spwig no puede dibujar arte de SVG en facturas y hojas de envío generadas.
- Deje **Habilitar Confirmación Doble para Correos de Marketing** en activado, a menos que tenga una razón específica para desactivarlo — es la configuración predeterminada más segura para el RGPD y protege su reputación de remitente al mantener direcciones no verificadas fuera de sus envíos de marketing.
- Deje **Estado Predeterminado de Consentimiento para Marketing** en desactivado. Marcar como predeterminado el consentimiento para marketing para nuevas cuentas socava el requisito de registro de opt-in del RGPD, incluso si un cliente podría técnicamente desmarcarlo.
- No desactive **Habilitar Centro de Preferencias de Clientes** solo para simplificar su panel de control de cuenta — sin él, los clientes aún pueden darse de baja de un tipo de mensaje, pero pierden la capacidad de ajustar con precisión las preferencias (por ejemplo, mantener actualizaciones de envío pero dejar de recibir el boletín).
- Mantenga **Requerir Verificación por SMS** activado, a menos que su flujo de registro ya confirme los números de teléfono de otra manera (por ejemplo, un inicio de sesión basado en SMS) — el ajuste existe específicamente para mantenerse dentro de las reglas TCPA.

## Solución de Problemas

**Los cambios no aparecen en la tienda:**
- Borre la caché de su navegador
- Ejecute una limpieza de caché desde el panel de administración
- Verifique si el modo de mantenimiento está activado accidentalmente

**Correos electrónicos no se envían:**
- Verifique la configuración de su proveedor de correo electrónico en Configuración de Correo Electrónico
- Asegúrese de que **El modo de Entrega de Correo** esté configurado en **En Vivo**
- Asegúrese de que **Correo de Redirección de Prueba** esté en blanco si quiere que los correos se envíen a destinatarios reales

**No funciona la conversión de moneda:**
- Verifique que su proveedor de tasas de cambio esté conectado
- Revise las credenciales de la API en la configuración de tasas de cambio
- Intente actualizar las tasas manualmente

**Los correos electrónicos de marketing no llegan a los clientes que se suscribieron:**
- Verifique si **Habilitar el doble consentimiento para correos electrónicos de marketing** está activado: si es así, el cliente debe hacer clic en el enlace de confirmación en el correo electrónico de verificación antes de que los correos electrónicos de marketing continúen
- Pida al cliente que revise el correo electrónico de spam/basura en busca del correo electrónico de confirmación
- Confirme que la suscripción del cliente a correos electrónicos de marketing esté activa en sus preferencias: hacer clic en "darse de baja" la desactiva

**Los clientes dicen que no pueden encontrar el centro de preferencias:**
- Verifique que **Habilitar el centro de preferencias del cliente** esté activado: cuando esté desactivado, el enlace del panel de control está oculto y la página no está disponible por diseño
- El enlace de darse de baja en cualquier correo electrónico de marketing siempre funciona independientemente de este ajuste, así que indique a los clientes que vayan allí como alternativa