---
title: Visión general de POS
---

<!-- screenshots-needed:
- url: /en/admin/pos/
  filename: pos-dashboard-overview.webp
  description: The POS dashboard landing page — full page at 1440x900
- url: /en/admin/
  filename: admin-sidebar-pos-group.webp
  description: Admin sidebar zoomed to the "Point of Sale" group, showing the expanded submenu with all items visible
-->

Spwig POS es un punto de venta basado en el navegador que permite a su personal registrar ventas en tienda en cualquier tableta o laptop — sin necesidad de hardware o software dedicado. Dado que Spwig POS funciona en la misma plataforma que su tienda en línea, su catálogo de productos, niveles de stock, cuentas de clientes y historial de pedidos siempre estarán sincronizados en todos los canales. Una venta realizada en tienda reduce inmediatamente el stock y aparece en sus informes de pedidos junto con los pedidos en línea.

Spwig POS está incluido en todas las ediciones — Comunidad, Pro y Empresarial — sin costo adicional. No hay nada que desbloquear o actualizar.

![POS dashboard](/static/core/admin/img/help/pos/pos-dashboard-overview.webp)

## Donde se encuentra POS en el administrador

En el menú lateral, desplácese hasta el grupo **Point of Sale**. Haga clic en **POS Dashboard** para abrir el área de gestión de POS en `/admin/pos/`. Desde aquí puede supervisar sus terminales, revisar turnos recientes y acceder a cada sección de configuración de POS a través del submenú:

- **POS Dashboard** — Vista general del estado de los terminales, turnos activos y ventas recientes de POS
- **Terminals** — Dispositivos POS registrados y sus configuraciones
- **Shifts** — Registros de turnos abiertos y cerrados con datos de conciliación de efectivo
- **Store Groups** — Grupos de ubicaciones físicas que comparten configuraciones regionales
- **Receipt Templates** — Diseños de recibos personalizados por tienda o grupo
- **Promo Slides** — Imágenes promocionales mostradas en la pantalla del cliente cuando esté inactivo
- **Terminal Providers** — Conexiones a servicios de pago (p. ej., Stripe Terminal, Square)
- **Card Readers** — Dispositivos lectores de tarjetas físicos emparejados con sus terminales
- **Open POS** — Inicia la interfaz de POS en una nueva pestaña

![Admin sidebar — Point of Sale group](/static/core/admin/img/help/pos/admin-sidebar-pos-group.webp)

## La aplicación del terminal POS

Sus cajeros trabajan en la interfaz de POS, que funciona como una aplicación web progresiva (PWA) en `/pos/` en el dominio de su tienda. Puede instalarse en una tableta o laptop como una aplicación nativa — funcionará desde la pantalla de inicio y continuará operando en modo offline si la conexión a internet se interrumpe temporalmente.

La interfaz de POS es independiente del backend del administrador. Su personal inicia sesión en `/pos/` con sus credenciales de tienda, no en el administrador principal. El administrador es donde configura y supervisa todo; la aplicación de POS es donde se realizan las ventas.

La pantalla orientada al cliente funciona en `/pos/display/` — una segunda pantalla o tableta orientada hacia el cliente, mostrando el carrito actual, los precios y las diapositivas promocionales entre transacciones.

## Terminología clave

Entender estos términos hace que el resto de la documentación de POS sea más fácil de seguir.

| Término | ¿Qué significa? |
|--------|----------------|
| **Grupo de tienda** | Una colección con nombre de ubicaciones físicas que comparten ajustes regionales, como moneda, idioma y zona horaria. Por ejemplo, "Tiendas de Nueva Zelanda" o "Región de Singapur". |
| **Ubicación de tienda** | Una tienda individual o sucursal. En Spwig, las ubicaciones de tienda son registros de almacén marcados como ubicaciones de venta al por menor. |
| **Terminal de POS** | Un dispositivo (tableta, portátil) registrado en una ubicación de tienda. Cada terminal tiene su propio nombre, código de emparejamiento y asignación opcional de lector de tarjetas. |
| **Lector de tarjetas** | El hardware del terminal de pago conectado a un terminal de POS — por ejemplo, un lector Stripe S700 o una máquina de tarjetas Adyen. Procesa pagos sin contacto y con chip y PIN. |
| **Proveedor de pago** | El servicio detrás del lector de tarjetas — Stripe Terminal, Square, Adyen y otros. Configura un proveedor de pago por tienda y conecta tus lectores de tarjetas a través de él. |
| **Turno** | Un período de apertura/cierre en un terminal. Un cajero abre un turno al inicio de su sesión (ingresando el saldo en efectivo inicial) y lo cierra al final, contando el efectivo en la caja. Los informes de turno muestran ventas totales, devoluciones y cualquier variación en efectivo. |
| **Pantalla para el cliente** | Una segunda pantalla o tableta orientada al cliente que muestra el contenido del carrito en vivo, el total y diapositivas promocionales cuando el terminal está inactivo. Se conecta a un terminal de POS mediante un código de emparejamiento corto. |
| **Código de emparejamiento** | Un código de 8 caracteres utilizado para vincular un nuevo dispositivo a un registro de terminal en el administrador. Cuando registra un terminal, ingresa su código de emparejamiento la primera vez que abre `/pos/` en ese dispositivo. |
| **Carrito aparcado** | Una transacción pausada guardada para que el cajero atienda a otro cliente y luego regrese a la venta original. Los carritos aparcados se almacenan por terminal y caducan después de 24 horas. |

## Cómo se conectan el inventario y los pedidos

Cada producto que vende a través del POS proviene de su catálogo principal. El inventario se deduce del mismo almacén al que se le asigna el terminal, por lo que la disponibilidad en línea y en tienda permanece precisa. Los pedidos de POS aparecen en **Pedidos** junto con sus pedidos web, con un distintivo de POS para distinguirlos. Las cuentas de clientes creadas en el mostrador son las mismas cuentas utilizadas en su tienda en línea — si un cliente ha comprado en línea antes, el cajero puede encontrarlo por nombre o correo electrónico y adjuntar el pedido en tienda a su cuenta.

## Jerarquía de configuración

La configuración de POS se propaga desde lo general a lo específico, por lo que solo necesita configurar lo que difiere en cada nivel:

1. **Predeterminado del sitio** — La moneda, el idioma y la zona horaria generales de su tienda desde **Configuración > Configuración de la tienda**
2. **Grupo de tienda** — Sobrescribe la moneda, el idioma o la zona horaria para todas las ubicaciones del grupo
3. **Ubicación de tienda** — Sobrescribe adicional para una sucursal específica (configurado en su registro de almacén)
4. **Terminal** — Sobrescribe de nivel de dispositivo para moneda o hardware en un solo mostrador

Si opera una tienda de una sola ubicación, puede omitir completamente los grupos de tienda y permitir que todo herede de los predeterminados del sitio.

## Lo que puede hacer desde el administrador de POS

| Tarea | Dónde |
|--------|-------|
| Registrar un nuevo dispositivo de POS | **Punto de venta > Terminales** |
| Conectar un proveedor de pago (Stripe, Square, etc.) | **Punto de venta > Proveedores de terminal** |
| Emparejar un lector de tarjetas físico con un terminal | **Punto de venta > Lectores de tarjetas** |
| Revisar o cerrar un turno abierto | **Punto de venta > Turnos** |
| Personalizar el diseño de su recibo | **Punto de venta > Plantillas de recibos** |
| Agregar imágenes promocionales a la pantalla para el cliente | **Punto de venta > Diapositivas promocionales** |
| Organizar sucursales por región | **Punto de venta > Grupos de tienda** |
| Iniciar la interfaz del cajero | **Punto de venta > Abrir POS** (se abre en una nueva pestaña) |

## Consejos

- No necesitas un grupo de tienda si operas una sola ubicación.

# Grupos de tienda

Los grupos de tienda son útiles cuando tienes múltiples sucursales con configuraciones regionales diferentes — por ejemplo, tiendas en diferentes países que usan monedas diferentes.
- Asigna a cada terminal un nombre claro y descriptivo (por ejemplo, "Caja frontal" o "Caja del café") para que los informes de turnos y los recibos sean fáciles de leer.
- Configura tu plantilla de recibo antes de tu primer turno — puedes personalizar el logotipo, la dirección de la tienda, el mensaje del pie de página e incluso agregar un código QR que enlace a una página de reseñas o un programa de fidelidad.
- La pantalla del cliente en `/pos/display/` funciona en cualquier dispositivo con un navegador.

Una tableta o monitor de repuesto es todo lo que necesitas — no se requiere la compra de hardware adicional.
- Si un lector de tarjetas se desconecta durante un período ocupado, el POS puede aceptar efectivo y pagos de tarjetas introducidos manualmente como alternativa, para que las ventas puedan continuar sin interrupciones.
- Los informes de turnos del POS están vinculados al cajero que los abrió, lo que facilita la conciliación del efectivo al final de cada sesión de cada persona.