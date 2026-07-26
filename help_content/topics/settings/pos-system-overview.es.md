---
title: Visión general del sistema POS
---

El sistema POS de Spwig transforma tu tienda en una solución de retail completa con terminales de punto de venta modernos. Está incluido en todas las ediciones — Community, Pro y Enterprise — con un número ilimitado de terminales en ubicaciones ilimitadas sin costo adicional. Cada terminal es una Aplicación Web Progresiva (PWA) que funciona sin conexión, sincroniza automáticamente y se integra de forma fluida con tu inventario, datos de clientes y procesamiento de pagos. Gestiona todo desde el panel de administración: configuración de terminal, conciliación de turnos, personalización de recibos e integración de hardware.

Utiliza el sistema POS cuando cuentes con ubicaciones de retail físicas, tiendas pop-up, ferias comerciales o cualquier entorno donde los clientes realicen compras en persona en lugar de en línea.

![Panel de POS](/static/core/admin/img/help/pos-system-overview/dashboard.webp)

## ¿Qué es Spwig POS?

Spwig POS es un sistema de punto de venta completamente integrado diseñado para comerciantes que venden tanto en línea como en ubicaciones físicas. A diferencia de los sistemas de punto de venta de terceros que requieren integraciones complejas, Spwig POS está construido directamente en tu plataforma, asegurando una sincronización perfecta de datos en todos los canales de venta.

**Características clave**:
- **Terminales ilimitados** - Despliega tantos terminales como necesites sin costo adicional
- **Arquitectura orientada a la operación sin conexión** - Continúa procesando ventas incluso cuando se pierda la conexión a internet
- **Aplicación Web Progresiva** - Sin instalaciones en tiendas de aplicaciones; accede desde cualquier dispositivo mediante el navegador (tabletas, computadoras, terminales dedicados)
- **Sincronización de stock real** - Reservas de stock (TTL de 15 minutos) previenen la sobreventa en canales
- **Soporte para pagos divididos** - Acepta múltiples métodos de pago por transacción (efectivo + tarjeta + tarjeta de regalo)
- **Integración de hardware** - Impresoras térmicas ESC/POS, escáneres de códigos de barras, cajones de efectivo, pantallas para clientes
- **Gestión de turnos** - Conciliación de efectivo con conteos de apertura/cierre y seguimiento de discrepancias
- **Listo para múltiples ubicaciones** - Grupos de tiendas con herencia de configuraciones para gestión de franquicias y regiones

## Ediciones

El POS está incluido en todas las ediciones de Spwig — Community, Pro y Enterprise — desde Spwig 1.5.8. No hay licencia de POS separada, no hay paso de activación y no hay tarifa por terminal.

**Lo que incluye cada edición**:
- Registros ilimitados de terminales
- Asignaciones ilimitadas de personal
- Todas las funciones de POS (turnos, gestión de efectivo, personalización de recibos, pantallas para clientes)
- Integraciones con proveedores de pago (Stripe Terminal y otros proveedores compatibles)
- Soporte de integración de hardware

Los comerciantes que operan tiendas alojadas en Spwig o pagan por una licencia Pro/Enterprise obtienen límites más altos en los servicios alojados en Spwig opcionales (GeoIP, geocodificador, notificaciones push) y soporte prioritario, pero el conjunto de funciones de POS es idéntico en todas las ediciones.

## Arquitectura del sistema

**Frontend** - Aplicación Web Progresiva de React 18:
- Primero sin conexión con caché de Service Worker (funciona sin internet)
- Sistema de construcción Vite para carga rápida
- Módulos CSS + tokens de diseño (coherentes con el tema de tu tienda)
- IndexedDB para persistencia de datos locales
- 10 idiomas admitidos (inglés, chino simplificado/tradicional, francés, alemán, español, portugués, japonés, ruso, árabe)

**Backend** - Integración del backend:
- 13 modelos de POS (POSTerminal, POSShift, CashMovement, ReceiptTemplate, PromoSlide, etc.)
- 43+ puntos de conexión REST para operaciones de terminal
- Sistema de reservas de stock con gestión de TTL
- Tareas de Celery para sincronización en segundo plano
- Almacenamiento encriptado de credenciales para proveedores de pago

**Seguridad**:
- Emparejamiento de terminal mediante códigos de 8 caracteres (generados en el servidor, caducan después de su uso)
- Control de asignación de personal que determina qué usuarios pueden acceder a qué terminales
- Capacidad de bloqueo/desbloqueo remoto para emergencias de administración
- Credenciales encriptadas de proveedores de pago
- Autenticación basada en sesión con soporte para desbloqueo biométrico (dependiente del navegador)

## Flujo de trabajo para comenzar

Sigue estos 4 pasos para desplegar tu primer terminal POS.

Para obtener una lista completa de verificación paso a paso que incluye la configuración del personal, proveedores de pago y la ejecución de su primera venta, consulte [Getting Started with POS](getting-started-with-pos).

**Paso 1: Crear almacén**
- Navegue a **Catálogo > Almacenes**
- Cree un almacén que represente su ubicación de venta al por menor
- Configure la dirección y la información de contacto
- Este almacén registrará el inventario físico para ventas de POS

**Paso 2: Registrar terminal**
- Navegue a **POS > Terminales**
- Haga clic en **+ Agregar terminal**
- Establezca el nombre del terminal (ej. "Caja principal", "Cobro 1")
- Asigne el almacén del Paso 2
- Configure la configuración del hardware (impresora, escáner, caja registradora)
- Guarde para generar un código de emparejamiento de 8 caracteres

**Paso 3: Asignar personal**
- En la configuración del terminal, desplácese hasta **Usuarios asignados**
- Seleccione los miembros del personal autorizados para usar este terminal
- Solo los usuarios asignados pueden iniciar sesión en el terminal
- Los usuarios deben tener permisos POS adecuados en su rol de personal

**Paso 4: Emparejar dispositivo**
- En su dispositivo terminal (tableta/ordenador), navegue a la URL `/pos/`
- Ingrese el código de emparejamiento de 8 caracteres del Paso 3
- El terminal descarga la configuración y sincroniza los datos iniciales
- Inicie sesión con las credenciales del personal asignado
- El terminal está listo para ventas

Después del emparejamiento, los terminales se sincronizan automáticamente cada 5 minutos (configurable). El modo sin conexión permite continuar operando cuando no haya conexión a Internet — las ventas se sincronizan automáticamente cuando se restablezca la conectividad.

## Características principales de POS

**Procesamiento de ventas**:
- Búsqueda de productos por nombre, SKU o código de barras
- Pago dividido (múltiples métodos de pago por pedido)
- Carritos de compras guardados (guardar transacciones incompletas)
- Devoluciones y anulaciones con seguimiento de razones
- Aplicación de descuentos (cupones, tarjetas regalo, promociones)
- Búsqueda de clientes y redención de puntos de lealtad

**Gestión de efectivo**:
- Apertura de turno con conteo inicial de efectivo
- Cierre de turno con reconciliación entre lo esperado y lo real
- Movimientos de efectivo (añadir efectivo, retiros de efectivo con razones)
- Cálculo automático del efectivo esperado basado en ventas en efectivo
- Seguimiento y reportes de discrepancias

**Integración de hardware**:
- Impresoras de recibos térmicas ESC/POS (red o serie)
- Escáneres de códigos de barras USB
- Triggers de caja registradora a través de pulsos de impresora
- Pantallas para clientes (carusel promocional durante el inactividad)
- Lectoras de tarjetas Stripe Terminal (S700, WisePOS E, P400)

**Capacidades sin conexión**:
- El Service Worker almacena todos los activos del terminal
- IndexedDB almacena pedidos recientes (configurable: 7-30 días, 200-1000 pedidos)
- Reservas de inventario con TTL de 15 minutos previenen la sobreventa
- Cola de ventas para sincronización cuando se restablezca la conectividad
- Detección automática de reconexión

## Páginas de administración de POS

Acceda a estas páginas de administración para gestionar todos los aspectos de su implementación de POS:

**Panel de control de POS** (`/admin/pos/`)
- Vista general del sistema y estadísticas rápidas
- Actividad reciente de terminales
- Resumen de turnos activos
- Mosaicos de uso de servicios hospedados (GeoIP, geocodificador, push — consulte [Spwig Hosted Services](hosted-services))

**Gestión de terminales** (`/admin/pos_app/posterminal/`)
- Registre y configure terminales
- Asigne personal y almacenes
- Supervise el estado en línea/pendiente (seguimiento de latido)
- Desbloquee terminales de forma remota
- [Más información: Managing POS Terminals](managing-pos-terminals)

**Gestión de turnos** (`/admin/pos_app/posshift/`)
- Ver todos los turnos (abiertos, cerrados, históricos)
- Revisar informes de reconciliación de efectivo
- Seguir movimientos de efectivo y discrepancias
- Auditoría de la actividad del turno
- [Más información: POS Shifts and Cash Management](pos-shifts-cash-management)

**Grupos de tiendas** (`/admin/pos_app/storegroup/`)
- Organice terminales por ubicación/ región
- Configure ajustes a nivel de grupo (moneda, idioma, huso horario)
- Implemente una jerarquía de herencia de ajustes
- [Más información: POS Store Groups](pos-store-groups)

**Plantillas de recibos** (`/admin/pos_app/receipttemplate/`)
- Personaliza los recibos impresas (ancho del papel, logotipo, encabezado/pie de página)
- Configura campos de cumplimiento (identificación fiscal, registro empresarial)
- Añade códigos QR para promociones
- Asigna plantillas a tiendas o grupos específicos
- [Más información: Personalización de plantillas de recibos](receipt-template-customization)

**Diapositivas promocionales** (`/admin/pos_app/promoslide/`)
- Crea contenido de carrusel para pantallas de clientes
- Asigna diapositivas a tiendas o grupos específicos
- Programa promociones estacionales
- [Más información: Diapositivas promocionales para pantallas de clientes](customer-display-promo-slides)

**Proveedores de pago** (`/admin/pos_app/posterminalprovider/`)
- Configura la integración de Terminal de Stripe
- Gestiona las credenciales de los proveedores de pago
- Supervisa el estado de la conexión
- [Más información: Proveedores de terminales de pago](payment-terminal-providers)

**Lectores de tarjetas** (`/admin/pos_app/posterminalreader/`)
- Registra lectores físicos de tarjetas
- Asigna lectores a terminales
- Personaliza pantallas de inicio (branding de la pantalla orientada al cliente)
- Supervisa el estado del lector (en línea/ fuera de línea/ ocupado)
- [Más información: Gestión de lectores de tarjetas](card-reader-management)

## Implementación en múltiples ubicaciones

Para comerciantes con múltiples ubicaciones de venta al por menor, Spwig POS admite la herencia de configuraciones jerárquicas:

**Jerarquía de configuraciones** (de mayor prioridad a menor):
1. Configuraciones específicas del terminal (sobrescribe todo)
2. Configuraciones específicas de la tienda (sobrescribe grupo y sitio)
3. Configuraciones del grupo (sobrescribe los valores predeterminados del sitio)
4. Valores predeterminados del sitio (valor predeterminado para todo)

Configura configuraciones compartidas en el nivel de grupo (por ejemplo, moneda regional, idioma) y sobrescribe según sea necesario para tiendas o terminales específicos. Consulte [Grupos de tiendas de POS](pos-store-groups) para obtener orientación detallada sobre la configuración.

## Consejos

- **Empieza con un solo terminal** - Prueba la configuración y el flujo de trabajo del POS con un solo terminal antes de implementar a toda la flota
- **Asigna almacén antes de emparejar** - Los terminales no pueden procesar ventas sin una asignación de almacén
- **Configura plantillas de recibos con anticipación** - Los campos de cumplimiento (identificaciones fiscales) varían según la región; configúralas antes de iniciar operaciones
- **Prueba el modo sin conexión** - Desconecta la internet y verifica que las ventas continúen; confirma la sincronización cuando se reconecte
- **Usa grupos de tiendas para múltiples ubicaciones** - Simplifica la gestión de configuraciones para implementaciones de franquicias o regionales
- **Supervisa el estado del pulso** - Los terminales pingen al servidor cada 5 minutos; los terminales sin conexión aparecen en el panel de administración
- **Configura límites de sincronización para el rendimiento** - Los terminales con conexiones lentas se benefician de configuraciones de sync_days/sync_limit más bajas
- **Haz copia de seguridad de la configuración del hardware** - Documenta las direcciones IP de las impresoras, configuraciones de escáneres, configuración del cajón de efectivo para recuperación ante desastres